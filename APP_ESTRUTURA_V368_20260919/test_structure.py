"""Offline tests against the staged module and actual extracted server functions."""
import ast
import hashlib
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import iald_estrutura_torre as structure

ROOT = Path(__file__).parent
SOURCE = (ROOT/'iald_web_server.py').read_text(encoding='utf-8')


class StructureTests(unittest.TestCase):
    def test_sources_and_retrieval(self):
        data, _ = structure._snapshot()
        self.assertEqual(len(data['sources']), 1020)
        for name, content in data['sources'].items():
            self.assertEqual(hashlib.sha256(content.encode()).hexdigest(), data['source_hashes'][name])
        results = structure.search('the_master_fires')['results']
        self.assertTrue(any('the_master_fires' in r['excerpt'] for r in results))
        self.assertTrue(structure.route('StrongAssembly')['module_imports'])
        self.assertTrue(structure.route('master')['recorded_axioms'])

    def test_complete_paginated_source(self):
        data, _ = structure._snapshot()
        name = next(p for p in data['sources'] if p.endswith('/TheMasterFires.lean'))
        pages, line = [], 1
        while line is not None:
            r = structure.read(name, line, 12)
            pages.extend(r['text'].split('\n'))
            self.assertTrue(r['next_line'] is None or r['next_line'] > line)
            line = r['next_line']
        self.assertEqual(pages, data['sources'][name].splitlines())
        with self.assertRaises(ValueError):
            structure.read('../.env')

    def test_context_scope(self):
        text, meta = structure.context('the_master_fires')
        self.assertIn('v368', text)
        self.assertIn('full_plan_complete=False', text)
        self.assertLess(len(text), 18000)
        self.assertTrue(meta['public_release_unchanged'])

    def test_corruption_and_traversal_refused(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            base = Path(temp)
            cfg = json.loads(structure.MANIFEST.read_bytes())
            cfg['bundle'] = 'broken.json'
            (base/'broken.json').write_bytes(b'{}')
            mf = base/'manifest.json'
            mf.write_text(json.dumps(cfg), encoding='utf-8')
            with patch.object(structure, 'MANIFEST', mf):
                with self.assertRaisesRegex(ValueError, 'integridade'):
                    structure.status()
                cfg['bundle'] = '../outside.json'
                mf.write_text(json.dumps(cfg), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'autorizado'):
                    structure.status()

    def test_server_access_and_context(self):
        names = {'_estrutura_operador', '_contexto_externo', 'execute_public_tool', 'estrutura_tgl_status', '_ferramentas_externas'}
        tree = ast.parse(SOURCE)
        selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        self.assertEqual(len(selected), 5)
        for node in selected:
            node.decorator_list = []
        ns = {'iald_estrutura_torre':structure, 'json':json, 'hashlib':hashlib,
              'load_users_estrito':lambda:{'owner':{'admin':True}, 'guest':{'admin':False}},
              'MOTORES_CFG':types.SimpleNamespace(memoria_modo='nucleo_kernel'),
              'PROMPT_EXTERNO':'legacy', 'PROMPT_EXTERNO_SHA':'old',
              'ERRO_MEMORIA_EXTERNA':None, 'KERNEL_EXTERNO':object(),
              'MEMORIA_EXTERNA':types.SimpleNamespace(prompt=lambda *a, **kw:('v357 baseline', {'context_sha256':'old'})),
              'session':{}, 'jsonify':lambda x:x}
        for module in ('iald_kernel','iald_memoria_canonica','iald_fontes_publicas','iald_core_indexado'):
            ns[module] = types.SimpleNamespace(tool_definitions=lambda:[])
        exec(compile(ast.Module(body=selected, type_ignores=[]), '<staged-server>', 'exec'), ns)
        cfg = types.SimpleNamespace(memoria_modo='nucleo_kernel', gratuito_atlas=False)
        for user, free, count in [('owner', False, 3), ('owner', True, 0), ('guest', False, 0)]:
            offered = ns['_ferramentas_externas'](cfg, {}, 'app', free, structure_user=user)
            self.assertEqual(len(offered), count)
        for username in ('guest', '?', ''):
            denied = ns['execute_public_tool'](structure.NAMES[0], {'query':'tower'}, username, True)
            self.assertEqual(json.loads(denied)['status'], 'FORBIDDEN')
            self.assertEqual(ns['_contexto_externo'](structure_user=username)[0], 'v357 baseline')
        self.assertEqual(ns['_contexto_externo'](public=True, structure_user='owner')[0], 'v357 baseline')
        prompt, meta = ns['_contexto_externo'](structure_user='owner', structure_query='the_master_fires')
        self.assertIn('ESTRUTURA ATUAL', prompt)
        self.assertEqual(meta['context_sha256'], hashlib.sha256(prompt.encode()).hexdigest())
        self.assertEqual(ns['estrutura_tgl_status']()[1], 403)
        ns['session']['username'] = 'owner'
        self.assertEqual(ns['estrutura_tgl_status']()['release'], 'v368')
        result = ns['execute_public_tool'](structure.NAMES[0], {'query':'the_master_fires'}, 'owner')
        self.assertTrue(json.loads(result)['results'])
        with patch.object(structure, 'context', side_effect=OSError('private/path')):
            with self.assertRaisesRegex(ValueError, '^Estrutura v368'):
                ns['_contexto_externo'](structure_user='owner')
        with patch.object(structure, 'execute', side_effect=OSError('private/path')):
            result = ns['execute_public_tool'](structure.NAMES[0], {'query':'x'}, 'owner')
            self.assertNotIn('private/path', result)
            self.assertEqual(json.loads(result)['status'], 'UNAVAILABLE')


if __name__ == '__main__':
    unittest.main(verbosity=2)
