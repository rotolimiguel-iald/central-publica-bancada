"""Offline regressions of the LOCAL_SEALED path and unchanged PUBLIC behavior."""
from pathlib import Path
from unittest.mock import patch
import copy, hashlib, json, sys, unittest, os
W=Path(__file__).resolve().parents[1];A=Path('C:/IALD/projetos_pyhton/IALD');S=W/'memory_stage'
sys.dont_write_bytecode=True;sys.path[:0]=[str(W/'app_patch'),str(A)]
import iald_local_release as local
from iald_core_indexado import DocumentCorpus
from iald_cluster import active_cluster
from iald_kernel import KernelCatalog
from iald_estado_publicado import published_evidence
from iald_release_binding import load_release
from iald_response_contract import deployment_contract
sha=lambda b:hashlib.sha256(b).hexdigest()
class Safety(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=json.loads((S/'manifest_staged.json').read_bytes());cls.ref=cls.m['local_release'];cls.snap=local.local_snapshot(cls.ref);cls.cat=KernelCatalog(S/'kernel',S/'kernel_verification.json')
 def test_01_manifest_and_all_members_actual_bytes(self):
  root,d=self.snap
  for n,pin in d['files'].items():
   raw=(root/n).read_bytes();self.assertEqual(sha(raw),pin['sha256']);self.assertEqual(len(raw),pin['bytes'])
 def test_02_program_seal_proof_catalog_same_identity(self):
  evidence,meta=published_evidence(self.m['published_evidence'],self.cat)
  self.assertEqual(meta['evidence_scope'],'LOCAL_SEALED');self.assertFalse(meta['publication_verified'])
  self.assertEqual(len(self.cat.records),1215);self.assertEqual(self.cat.source_sha,self.snap[1]['source_sha256'])
  self.assertIn('LOCAL_SEALED_RECORDS_HASH_MATCHED',evidence)
 def test_03_manifest_hash_alteration_rejected(self):
  ref={**self.ref,'sha256':'0'*64}
  with self.assertRaises(ValueError):local.local_snapshot(ref)
 def test_04_extra_reference_field_rejected(self):
  with self.assertRaises(ValueError):local.local_snapshot({**self.ref,'approved':True})
 def test_05_wrong_source_rejected(self):
  with self.assertRaises(ValueError):local.local_snapshot(self.ref,'0'*64,'v388')
 def test_06_wrong_version_rejected(self):
  with self.assertRaises(ValueError):local.local_snapshot(self.ref,self.cat.source_sha,'v380')
 def test_07_invalid_root_rejected(self):
  with self.assertRaises((ValueError,OSError)):local.local_snapshot({**self.ref,'path':str(A/'LOCAL_SEALED_MANIFEST.json')})
 def test_08_document_altered_bytes_rejected(self):
  row=self.m['entries'][0];raw=Path(row['path']).read_bytes()
  with self.assertRaises(ValueError):local.check_document(self.snap,row,raw+b'\n')
 def test_09_local_url_claim_rejected(self):
  row={**self.m['entries'][0],'url':'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+('a'*40)+'/x.md'}
  with self.assertRaises(ValueError):local.check_document(self.snap,row,Path(row['path']).read_bytes())
 def test_10_document_id_substitution_rejected(self):
  row={**self.m['entries'][0],'id':'um_forma_canonica_integral'}
  with self.assertRaises(ValueError):local.check_document(self.snap,row,Path(row['path']).read_bytes())
 def test_11_document_path_escape_rejected(self):
  with self.assertRaises(ValueError):local.check_member(self.snap,A/'iald_cluster.py',(A/'iald_cluster.py').read_bytes())
 def test_12_corpus_complete_and_no_false_public_urls(self):
  docs=DocumentCorpus(S/'manifest_staged.json')._load();self.assertEqual(set(docs),local.DOCUMENT_IDS)
  self.assertTrue(all(not x['url'] for x in docs.values()))
  self.assertEqual(docs['um_artigo_publicado_integral']['name'],'um_absoluto_pt.tex')
 def test_13_public_existing_release_preserved(self):
  m=json.loads((A/'iald_nucleo_fixo.json').read_bytes());self.assertEqual(m['operational_core']['current_release'],'v380')
  c=KernelCatalog(m['active_cluster']['kernel_bundle'],m['active_cluster']['kernel_verification'])
  _,meta=published_evidence(m['published_evidence'],c);self.assertEqual(meta['evidence_scope'],'PUBLIC');self.assertTrue(meta['publication_verified'])
  self.assertEqual(load_release(A/'iald_nucleo_fixo.json').identity['release'],'v380')
  self.assertEqual(len(DocumentCorpus(A/'iald_nucleo_fixo.json')._load()),8)
 def test_14_local_must_not_claim_git_commit(self):
  m=copy.deepcopy(self.m);m['active_cluster']['commit']='a'*40;data=json.dumps(m).encode();old=Path.read_bytes;target=S/'manifest_staged.json'
  with patch.object(Path,'read_bytes',lambda p:data if p==target else old(p)):
   with self.assertRaises(ValueError):active_cluster(target,self.cat.source_sha)
 def test_15_local_marker_removal_rejected_by_public_loader(self):
  m=copy.deepcopy(self.m);m.pop('local_release');data=json.dumps(m).encode();old=Path.read_bytes;target=S/'manifest_staged.json'
  with patch.object(Path,'read_bytes',lambda p:data if p==target else old(p)):
   with self.assertRaises(ValueError):DocumentCorpus(target)._load()
 def test_16_local_requires_nonpublic_evidence_metadata(self):
  with self.assertRaises(ValueError):deployment_contract(S/'manifest_staged.json',self.cat.source_sha,{'published_evidence_checked':True,'published_source_sha256':self.cat.source_sha,'evidence_scope':'PUBLIC','publication_verified':True},{})
 def test_17_manifest_duplicate_field_rejected(self):
  raw=Path(self.ref['path']).read_bytes();bad=raw[:-2]+b',"mode":"LOCAL_SEALED"}\n';ref={**self.ref,'sha256':sha(bad)};old=Path.read_bytes;target=Path(ref['path'])
  with patch.object(Path,'read_bytes',lambda p:bad if p==target else old(p)):
   with self.assertRaises(ValueError):local.local_snapshot(ref)
 def test_18_admitted_scope_not_boolean(self):
  with self.assertRaises(ValueError):local.local_snapshot({**self.ref,'mode':True})
 def test_19_source_program_not_imported(self):
  loaded=[str(getattr(x,'__file__','')) for x in sys.modules.values() if x]
  self.assertFalse(any(Path(x).name=='um.py' for x in loaded))
 def test_20_production_protected_bytes_unchanged(self):
  prep=json.loads((S/'prepared.json').read_bytes())
  for p,digest in prep['protected_production_sha256'].items():self.assertEqual(sha(Path(p).read_bytes()),digest)
 def test_21_full_context_within_unchanged_budget(self):
  m=json.loads((S/'public_metadata.json').read_bytes());self.assertLessEqual(m['context_tokens'],340000)
  self.assertNotIn('<ATLAS_CANONICO',(S/'haiku_prefix.md').read_text(encoding='utf-8'))
 def test_22_all_current_topics_and_new_v388_present(self):
  p=json.loads((S/'prepared.json').read_bytes());source=json.loads((S/'release/um_absoluto.json').read_bytes());self.assertEqual(set(p['coverage']),set(source['core']))
  prefix=(S/'haiku_prefix.md').read_text(encoding='utf-8')
  for name in ('beta_runs_bounded_below_v388','hubble_ratio_opening_v388'):self.assertIn('### '+name+'\n',prefix)
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Safety))
 report={'status':'PASS' if r.wasSuccessful() else 'FAIL','tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'scope':'OFFLINE_DOCUMENT_LOADER_REGRESSIONS_NO_SCIENTIFIC_EXECUTION','module_pins':{str(p):sha(p.read_bytes()) for p in (W/'app_patch').glob('*.py')}}
 out=W/'validation/local_release_tests.json';out.parent.mkdir(exist_ok=True);raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();assert not out.exists();temp=out.with_suffix('.tmp');temp.write_bytes(raw);assert temp.read_bytes()==raw;os.replace(temp,out);print(json.dumps(report));sys.exit(0 if r.wasSuccessful() else 1)
