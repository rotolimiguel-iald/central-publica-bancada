"""Recompute released-posterior analyses in fresh, hash-checked work directories.

The manifest declares every source file. Never execute a release notebook or
reuse reference results as calculation inputs. Downloading is opt-in. A copied
analysis program runs unchanged, so the frozen experiment is not rewritten.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parent


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def checked(root, name):
    relative = PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or '\\' in name:
        raise ValueError('Unsafe manifest path: ' + name)
    result = (root / name).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError('Path escapes declared root: ' + name)
    return result


def verify(path, row):
    if path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
        raise ValueError('Input custody mismatch: ' + str(path))


def atomic(path, value):
    if path.exists():
        raise FileExistsError('Preserve previous result: ' + str(path))
    raw = json.dumps(value, indent=2, ensure_ascii=False).encode('utf-8')
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_bytes(raw)
    if temporary.stat().st_size != len(raw):
        raise ValueError('Short write')
    temporary.replace(path)


def download_archive(row, folder):
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / row['filename']
    if target.exists():
        verify(target, row)
        return target
    partial = target.with_name(target.name + '.partial')
    if partial.exists():
        raise FileExistsError('Preserve partial download and inspect: ' + str(partial))
    with urllib.request.urlopen(row['url'], timeout=60) as response, partial.open('xb') as stream:
        shutil.copyfileobj(response, stream, 4 * 1024 * 1024)
    verify(partial, row)
    partial.replace(target)
    return target


def numeric_comparison(actual, expected, path='', errors=None):
    """Compare all numerical leaves in declared scientific subtrees.

    Counts/booleans and decision strings are exact. Real tolerances are explicit
    to permit independent BLAS versions; byte hashes are checked separately.
    """
    errors = [] if errors is None else errors
    if isinstance(expected, dict):
        for key, value in expected.items():
            # These are provenance, not measured quantities; current manifests
            # check them without borrowing old hashes or absolute source paths.
            if key in ('code_sha256', 'dependency_hashes', 'dependencies', 'source_sha256'):
                continue
            if key not in actual:
                raise ValueError('Missing result field: ' + path + '/' + key)
            numeric_comparison(actual[key], value, path + '/' + key, errors)
    elif isinstance(expected, list):
        if len(actual) != len(expected):
            raise ValueError('Changed result length: ' + path)
        for index, value in enumerate(expected):
            numeric_comparison(actual[index], value, path + '/' + str(index), errors)
    elif isinstance(expected, bool) or expected is None:
        if actual != expected:
            raise ValueError('Changed decision/null: ' + path)
    elif isinstance(expected, (int, float)):
        if not math.isfinite(expected) or not math.isfinite(actual):
            raise ValueError('Nonfinite result: ' + path)
        if isinstance(expected, int):
            if actual != expected:
                raise ValueError('Changed count: ' + path)
        elif not math.isclose(actual, expected, rel_tol=2e-7, abs_tol=1e-10):
            raise ValueError(f'Changed measured value at {path}: {actual} != {expected}')
        errors.append((path, abs(actual - expected)))
    elif path.endswith('/verdict') and actual != expected:
        raise ValueError('Changed verdict: ' + path)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', help='A stage explicitly listed in MANIFEST.json')
    parser.add_argument('--imr-python', type=Path, help='Separate PyCBC interpreter for IMR generation, if required')
    parser.add_argument('--source-root', type=Path, help='Existing task cache; only manifest paths are read')
    parser.add_argument('--archive-cache', type=Path, help='Public archives, laid out as RECORD/filename')
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--prepare-only', action='store_true',help='Verify/copy inputs, record preparation, then remove temporary data')
    parser.add_argument('--work-root',type=Path,required=True)
    parser.add_argument('--output-root',type=Path,required=True)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'MANIFEST.json').read_bytes())
    for row in manifest['shipped_files']:
        verify(checked(ROOT, row['path']), row)
    spec = manifest['stages'][args.stage]
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    workroot=args.work_root.resolve();workroot.mkdir(parents=True,exist_ok=True)
    outputroot=args.output_root.resolve();outputroot.mkdir(parents=True,exist_ok=True)
    if outputroot.is_relative_to(ROOT.resolve()) or workroot.is_relative_to(ROOT.resolve()):
        raise ValueError('Work/output directories must be outside immutable package')
    preserved=outputroot/(ROOT.name+'_'+args.stage+'_'+stamp)
    preserved.mkdir()
    parent=Path(tempfile.mkdtemp(prefix='replay_'+args.stage+'_',dir=workroot)).resolve()
    run = parent / 'ORDEM_013_RINGDOWN'
    try:
        if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe temporary')
        run.mkdir(parents=True)
        (run / 'cache').mkdir()
        for row in manifest['assets']:
            target = checked(parent, row['destination'])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(checked(ROOT, row['path']), target)
        external = [r for r in manifest['external_inputs'] if args.stage in r['stages']]
        archives = {r['id']: r for r in manifest['archives']}
        archive_handles = {}
        try:
            for row in external:
                target = checked(run, row['path'])
                target.parent.mkdir(parents=True, exist_ok=True)
                source = checked(args.source_root, row['path']) if args.source_root else None
                if source is not None and source.exists():
                    verify(source, row)
                    shutil.copyfile(source, target)
                elif 'url' in row:
                    if not args.download:
                        raise FileNotFoundError('Provide --source-root or --download for ' + row['path'])
                    downloaded = download_archive(dict(row, filename=target.name), target.parent)
                    if downloaded != target:
                        raise ValueError('Unexpected direct download target')
                else:
                    info = archives[row['archive']]
                    archive = (args.archive_cache / str(info['record']) / info['filename']) if args.archive_cache else None
                    if row['archive'] not in archive_handles:
                        if archive is not None and archive.exists():
                            verify(archive, info)
                        elif args.download:
                            archive = download_archive(info, parent / 'download_cache' / str(info['record']))
                        else:
                            raise FileNotFoundError('Provide --source-root, --archive-cache, or --download for ' + row['path'])
                        archive_handles[row['archive']] = tarfile.open(archive, 'r:gz')
                    handle = archive_handles[row['archive']]
                    member = handle.getmember(row['member'])
                    if not member.isfile() or member.size != row['bytes']:
                        raise ValueError('Archive member is not the declared regular file')
                    with handle.extractfile(member) as stream, target.open('xb') as dest:
                        shutil.copyfileobj(stream, dest)
                verify(target, row)
        finally:
            for handle in archive_handles.values():
                handle.close()
        receipt = dict(stage=args.stage, run=str(run), date_utc=datetime.now(timezone.utc).isoformat(),
            manifest_sha256=sha(ROOT / 'MANIFEST.json'), external_inputs=len(external),
            reference_results_copied_as_inputs=False, commands=spec['commands'])
        atomic(parent / 'PREPARED.json', receipt)
        print(json.dumps(receipt), flush=True)
        if args.prepare_only:
            return
        env = os.environ.copy()
        env.update(PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
        for command in spec['commands']:
            log = parent / (Path(command[0]).stem + '.log')
            with log.open('xb') as stream:
                interpreter = str(args.imr_python) if command[0] == 'prepare_imr_controls.py' and args.imr_python else sys.executable
                process = subprocess.run([interpreter, '-B'] + command, cwd=run,
                    env=env, stdout=stream, stderr=subprocess.STDOUT)
            print(json.dumps(dict(command=command, exit_code=process.returncode, log=str(log))), flush=True)
            if process.returncode:
                atomic(parent / 'FAILED.json', dict(**receipt, failed_command=command, exit_code=process.returncode))
                raise RuntimeError('Calculation failed; preserved log: ' + str(log))
        comparisons = []
        for output in spec['outputs']:
            actual = json.loads((run / output['name']).read_bytes())
            expected = json.loads((ROOT / 'reference' / output['name']).read_bytes())
            errors = []
            for key in output['fields']:
                numeric_comparison(actual[key], expected[key], key, errors)
            comparisons.append(dict(output=output['name'], numerical_leaves=len(errors),
                max_absolute_difference=max((v for _, v in errors), default=0),
                output_sha256=sha(run / output['name']), checked_fields=output['fields']))
        atomic(parent / 'RESULT.json', dict(**receipt, status='PASS', comparisons=comparisons,
            tolerance=dict(relative=2e-7, absolute=1e-10), numpy_version=__import__('numpy').__version__,
            scipy_version=__import__('scipy').__version__, h5py_version=__import__('h5py').__version__))
        print(json.dumps(dict(status='PASS', stage=args.stage, comparisons=comparisons, run=str(run))), flush=True)

    finally:
        # Preserve only generated reports/logs; never retain raw copied inputs.
        try:
            for p in list(parent.glob('*.json'))+list(parent.glob('*.log')):
                if p.is_file() and not p.is_symlink():shutil.copyfile(p,preserved/p.name)
            atomic(preserved/'CLEANUP_INTENT.json',dict(temporary=str(parent),manifest_sha256=sha(ROOT/'MANIFEST.json'),
              scope='Preparation and numeric reports only; not physical certification'))
        finally:
            if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe cleanup target')
            shutil.rmtree(parent)
            if parent.exists():raise RuntimeError('Temporary cleanup failed')
            atomic(preserved/'TEMPORARY_REMOVED.json',dict(removed=True,temporary=str(parent),utc=datetime.now(timezone.utc).isoformat()))


if __name__ == '__main__':
    main()
