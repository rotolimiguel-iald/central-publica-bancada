"""Run only extracted guard/writer AST with an in-memory filesystem, including -O."""
from pathlib import Path
import ast
import hashlib
import io
import json
import os
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent


class MemoryFS:
    def __init__(self):
        self.files = {}
        self.writes = 0
        self.race = False

    def path(self, name):
        return MockPath(self, name)

    def link(self, source, destination):
        if self.race:
            self.files[destination.name] = b'concurrent-result'
        if destination.name in self.files:
            raise FileExistsError(destination.name)
        self.files[destination.name] = self.files[source.name]
        self.writes += 1


class MockPath:
    def __init__(self, fs, name):
        self.fs, self.name = fs, name

    def __truediv__(self, name):
        return MockPath(self.fs, name)

    @property
    def suffix(self):
        return Path(self.name).suffix

    def with_suffix(self, suffix):
        return MockPath(self.fs, str(Path(self.name).with_suffix(suffix)))

    def exists(self):
        return self.name in self.fs.files

    def read_bytes(self):
        return self.fs.files[self.name]

    def unlink(self):
        del self.fs.files[self.name]

    def open(self, mode):
        if mode != 'xb':
            raise RuntimeError('Unexpected mode')
        if self.exists():
            raise FileExistsError(self.name)
        outer = self

        class Buffer(io.BytesIO):
            def __exit__(self, *args):
                outer.fs.files[outer.name] = self.getvalue()
                outer.fs.writes += 1
                self.close()
        return Buffer()


def run_block(nodes, namespace):
    tree = ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[]))
    exec(compile(tree, '<guard-only-mock>', 'exec', optimize=2), namespace)


def must_raise(kind, callback):
    try:
        callback()
    except kind:
        return
    raise RuntimeError('Expected refusal absent: ' + kind.__name__)


def main():
    cases = []
    manifest = json.loads((ROOT/'MANIFEST.json').read_bytes())
    for name in manifest['scripts']:
        path = ROOT/name
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest['scripts'][name]:
            raise ValueError('Script pin mismatch')
        tree = ast.parse(raw)
        if any(isinstance(n, ast.Assert) for n in ast.walk(tree)):
            raise RuntimeError('assert survived')
        fs = MemoryFS()
        ns = {'OUT': fs.path('out'), 'json': json}
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'new', 'publish_exclusive'}]
        run_block(functions, ns)
        fs.files['result.json'] = b'original-result'
        before = dict(fs.files)
        if 'new' in ns:
            argument = 'mock' if name == 'write_report.py' else {'mock': True}
            must_raise(FileExistsError, lambda: ns['new']('result.json', argument))
        else:
            guard = next(n for n in tree.body if isinstance(n, ast.If) and 'p.exists()' in ast.unparse(n.test))
            ns['p'] = fs.path('result.json')
            must_raise(FileExistsError, lambda: run_block([guard], ns))
        if fs.files != before or fs.writes:
            raise RuntimeError('Existing target was touched')
        cases.append({'script': name, 'test': 'existing_destination', 'refused': True, 'writes': 0})

        pin = next(n for n in tree.body if isinstance(n, ast.If) and
                   any(term in ast.unparse(n.test) for term in ('sha(src)', 'sha(source)', 'digest ==', 'source_hash ==')))
        pin_ns = {'sha': lambda p: 'BAD', 'src': fs.path('source'), 'source': fs.path('source'),
                  'meta': {'sha256': 'GOOD'}, 'd': {'source_sha256': 'GOOD'},
                  'entry': [{'sha256': 'GOOD'}], 'digest': 'BAD', 'source_hash': 'BAD'}
        must_raise(ValueError, lambda: run_block([pin], pin_ns))
        if fs.files != before or fs.writes:
            raise RuntimeError('Bad pin changed output')
        cases.append({'script': name, 'test': 'bad_source_pin', 'refused': True, 'writes': 0})

        fs.files.clear()
        fs.files['result.json.tmp'] = b'candidate'
        fs.race = True
        with patch.object(os, 'link', fs.link):
            must_raise(FileExistsError, lambda: ns['publish_exclusive'](fs.path('result.json.tmp'), fs.path('result.json')))
        if fs.files != {'result.json': b'concurrent-result'}:
            raise RuntimeError('Publication race overwrote target or retained temp')
        cases.append({'script': name, 'test': 'concurrent_destination_at_final_publish', 'refused': True, 'target_preserved': True})

    for relative, expected in manifest['originals'].items():
        original = ROOT.parents[1]/relative
        if hashlib.sha256(original.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Original changed: ' + relative)
    result = {'status': 'PASS_GUARD_ONLY_MOCK', 'python_optimization': sys.flags.optimize,
              'compiled_blocks_optimization': 2, 'cases': cases,
              'generators_executed': False, 'posterior_opened': False,
              'original_files_unchanged': len(manifest['originals']),
              'test_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    payload = (json.dumps(result, indent=2)+'\n').encode()
    out = ROOT/'GUARD_TEST_RESULTS.json'
    with out.open('xb') as stream:
        stream.write(payload)
    print(json.dumps({'status': result['status'], 'cases': len(cases), 'optimization': sys.flags.optimize}))


if __name__ == '__main__':
    main()
