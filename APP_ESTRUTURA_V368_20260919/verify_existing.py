"""Reconcile concurrent installed release, without importing um.py or web server."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.request

WORK = Path(__file__).resolve().parent
APP = Path(r'C:\IALD\projetos_pyhton\IALD')
OTHER = WORK.parents[1]/'work/iald_tgl_cluster_20260919'
sys.path.insert(0, str(APP))
os.environ['TIKTOKEN_CACHE_DIR'] = str(APP/'.iald_runtime/tokenizer_cache')
from iald_kernel import KernelCatalog
from iald_memoria_canonica import CanonicalMemory
from iald_core_indexado import DocumentCorpus

sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
installed = json.loads((OTHER/'installed.json').read_bytes())
assert all(sha(APP/name) == digest for name,digest in installed['files'].items())
manifest_path = APP/'iald_nucleo_fixo.json'
manifest = json.loads(manifest_path.read_bytes())
cfg = manifest['active_cluster']
catalog = KernelCatalog(cfg['kernel_bundle'], cfg['kernel_verification'])
ours = json.loads((WORK/'estrutura_v368.json').read_bytes())
assert catalog.source_sha == ours['source_sha256']
for name, digest in ours['source_hashes'].items():
    assert name in catalog.records, name
    assert catalog.records[name]['sha256'] == digest, name
queries = ['the_master_fires','qgStrongCertificate_frame','UnifiedRecordedPreparation','SmoothSelectedAtlasGluing']
retrieved = {}
for query in queries:
    result = catalog.search(query, 5)
    assert result['results'], query
    assert any(query in r['excerpt']['text'] or query in r['path'] for r in result['results']), query
    retrieved[query] = [{'path':r['path'],'line':r['line']} for r in result['results']]
docs = DocumentCorpus(manifest_path)._load()
result = json.loads(docs['resultado_publicado_integral']['text'])
prep = json.loads((OTHER/'prepared.json').read_bytes())
assert set(prep['coverage']) == set(result['core'])
for row in prep['detail_containers']:
    val = result
    for part in row['pointer'].split('/')[1:]:
        key = part.replace('~1','/').replace('~0','~')
        val = val[int(key)] if isinstance(val,list) else val[key]
    assert len(val) == row['items']
memory = CanonicalMemory(WORK/'unused_private_atlas.md', 'nucleo_kernel', nucleus_manifest=manifest_path)
prompt, meta = memory.prompt('', catalog, public=True)
assert meta['cluster_always_present'] and meta['published_evidence_checked']
assert meta['private_atlas_included'] is False
for item in ('mother_instruction', 'operational_core'):
    assert Path(manifest[item]['path']).read_text(encoding='utf-8-sig') in prompt
health = urllib.request.build_opener(urllib.request.ProxyHandler({})).open('http://127.0.0.1:8082/health', timeout=10)
assert health.status == 200
report = {'at':datetime.now().astimezone().isoformat(), 'status':'EXISTING_DEPLOYMENT_VERIFIED__NO_DUPLICATE_INSTALL',
          'release':cfg['release'], 'source_sha256':catalog.source_sha,
          'installed_files_hashes_checked':len(installed['files']),
          'our_lean_sources_identical_and_already_installed':len(ours['sources']),
          'installed_catalog_files':len(catalog.records),
          'installed_lean_sources':sum(p.endswith('.lean') for p in catalog.records),
          'result_sections':len(result['core']), 'topics':cfg['topics'],
          'detail_pointers_checked':len(prep['detail_containers']),
          'public_context_tokens':meta['context_tokens'],
          'private_atlas_included':meta['private_atlas_included'],
          'v5_and_memory_core_preserved':True, 'retrieval':retrieved,
          'http_health':health.status, 'provider_inference_called':False,
          'production_changes_this_verification':False,
          'peer_test_results':json.loads((OTHER/'test_results.json').read_bytes()),
          'scope':'App ChatGPT mode, existing release and retrieval verified; no new Lean compilation or physics verdict.'}
out = WORK/'reconciliacao_instalada.json'
assert not out.exists()
temp = out.with_suffix('.tmp')
temp.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8'))
assert temp.stat().st_size > 100
temp.replace(out)
print(json.dumps(report,ensure_ascii=False))
