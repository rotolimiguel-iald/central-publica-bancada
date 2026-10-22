"""APP-01 provenance regression; local readers only, unchanged egress candidate."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,os,sys,unittest
D=Path(__file__).resolve().parent;W=D.parent;S=W/'memory_stage';A=Path('C:/IALD/projetos_pyhton/IALD')
sys.dont_write_bytecode=True;sys.path[:0]=[str(D),str(W/'app_patch'),str(A)]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
old=load(W/'app_patch/iald_core_indexado.py','core_before_APP01');new=load(D/'iald_core_indexado.py','iald_core_indexado')
base=load(W/'validation/test_local_release.py','base_local_release_tests')
sha=lambda b:hashlib.sha256(b).hexdigest()
class ScopeTests(unittest.TestCase):
 def test_23_local_context_bytes_and_metadata_identical(self):
  for public in (True,False):self.assertEqual(old.DocumentCorpus(S/'manifest_staged.json').context(public),new.DocumentCorpus(S/'manifest_staged.json').context(public))
 def test_24_local_search_scope_and_every_result(self):
  r=new.DocumentCorpus(S/'manifest_staged.json').search('Hubble',2)
  self.assertEqual(r['scope'],'LOCAL_SEALED_DOCUMENTS');self.assertEqual(r['source_scope'],'LOCAL_SEALED');self.assertTrue(r['results'])
  for row in r['results']:self.assertEqual(row['source_scope'],'LOCAL_SEALED');self.assertEqual(row['url'],'')
 def test_25_local_fetch_identifies_scope_and_preserves_bytes(self):
  before,after=old.DocumentCorpus(S/'manifest_staged.json'),new.DocumentCorpus(S/'manifest_staged.json')
  for ident in before._load():
   previous=before.fetch(ident,0,300);current=after.fetch(ident,0,300);self.assertEqual(current.pop('source_scope'),'LOCAL_SEALED');self.assertEqual(current,previous)
 def test_26_public_scope_preserved(self):
  after=new.DocumentCorpus(A/'iald_nucleo_fixo.json');r=after.search('Hubble',2);self.assertEqual(r['scope'],'PUBLISHED_DOCUMENTS');self.assertEqual(r['source_scope'],'PUBLIC')
  for row in r['results']:self.assertEqual(row['source_scope'],'PUBLIC')
  self.assertEqual(after.fetch('um_forma_canonica_integral',0,100)['source_scope'],'PUBLIC')
 def test_27_tools_and_pending_prefix_unchanged(self):
  self.assertEqual(new.tool_definitions(),old.tool_definitions());self.assertEqual(sha((S/'haiku_prefix.md').read_bytes()),json.loads((W/'COUNT_PLAN.json').read_bytes())['prefix_sha256'])
 def test_28_empty_local_search_still_reports_local(self):
  r=new.DocumentCorpus(S/'manifest_staged.json').search('qzxvzzqqkkkrandomunmatchabletoken',1);self.assertEqual(r['scope'],'LOCAL_SEALED_DOCUMENTS');self.assertEqual(r['source_scope'],'LOCAL_SEALED')
 def test_29_successor_plan_changes_only_one_loader(self):
  oldplan=json.loads((W/'install_plan_candidate.json').read_bytes());newplan=json.loads((D/'install_plan_candidate.json').read_bytes());changed=[]
  for a,b in zip(oldplan['files'],newplan['files']):
   if a!=b:changed.append((a,b))
  self.assertEqual(len(oldplan['files']),len(newplan['files']));self.assertEqual(len(changed),1)
  a,b=changed[0];self.assertEqual(Path(b['destination']).name,'iald_core_indexado.py');self.assertEqual(a['baseline'],b['baseline']);self.assertEqual(b['sha256'],sha((D/'iald_core_indexado.py').read_bytes()));ast.parse((D/'prepare_install.py').read_bytes())
 def test_30_original_1300_review_members_unchanged(self):
  members=json.loads((W/'REVIEW_MANIFEST.json').read_bytes())['members'];self.assertEqual(len(members),1300)
  for row in members:
   raw=Path(row['path']).read_bytes();self.assertEqual(len(raw),row['bytes']);self.assertEqual(sha(raw),row['sha256'])
if __name__=='__main__':
 suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(base.Safety),unittest.defaultTestLoader.loadTestsFromTestCase(ScopeTests)]);r=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'status':'PASS' if r.wasSuccessful() else 'FAIL','tests':r.testsRun,'errors':len(r.errors),'failures':len(r.failures),'scope':'OFFLINE_DOC_SCOPE_FIX_PLUS_LOCAL_PUBLIC_REGRESSIONS','patch_sha256':sha((D/'iald_core_indexado.py').read_bytes()),'prefix_sha256':sha((S/'haiku_prefix.md').read_bytes()),'context_bytes_unchanged':r.wasSuccessful(),'tool_definitions_unchanged':r.wasSuccessful(),'original_review_members_unchanged':r.wasSuccessful(),'models_called':0,'production_changes':0}
 p=D/'TEST_REPORT.json';assert not p.exists();t=p.with_suffix('.tmp');raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
 with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==raw;os.replace(t,p);print(json.dumps(report));sys.exit(0 if r.wasSuccessful() else 1)
