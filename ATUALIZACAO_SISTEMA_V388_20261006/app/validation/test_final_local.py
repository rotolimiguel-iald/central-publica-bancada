"""Final offline checks after Jev linkage; no transport or scientific execution."""
from pathlib import Path
import sys,unittest,importlib.util,hashlib,json,os,ast
W=Path(__file__).resolve().parents[1];S=W/'memory_stage';A=Path('C:/IALD/projetos_pyhton/IALD')
sys.dont_write_bytecode=True;sys.path[:0]=[str(W/'app_patch'),str(A)]
spec=importlib.util.spec_from_file_location('local_regressions',W/'validation/test_local_release.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
sha=lambda b:hashlib.sha256(b).hexdigest()
class Linkage(unittest.TestCase):
 def test_23_jev_real_loader_same_program_result_proof(self):
  import iald_jev_control as control
  contract=control.load_contract(S)
  self.assertEqual(contract,json.loads((W/'controller/jev_control_v388.json').read_bytes()))
  self.assertEqual(contract['source_sha256'],json.loads((S/'manifest_staged.json').read_bytes())['active_cluster']['release_source_sha256'])
 def test_24_prefix_bytes_identical_to_blocked_count_plan(self):
  self.assertEqual(sha((S/'haiku_prefix.md').read_bytes()),json.loads((W/'COUNT_PLAN.json').read_bytes())['prefix_sha256'])
 def test_25_scripts_parse_without_execution(self):
  for p in [W/'transaction.py',W/'prepare_install.py',W/'count_memory.py',*sorted((W/'app_patch').glob('*.py'))]:ast.parse(p.read_bytes())
 def test_26_plan_allowlisted_paths_and_manifest_last(self):
  plan=json.loads((W/'install_plan_candidate.json').read_bytes());self.assertEqual(plan['status'],'STATIC_CANDIDATE_NOT_ACTIVATABLE')
  dest=[]
  for r in plan['files']:
   src,p=Path(r['source']),Path(r['destination']);self.assertTrue(src.resolve().is_relative_to(W));self.assertTrue(p.resolve().is_relative_to(A))
   self.assertEqual(sha(src.read_bytes()),r['sha256']);self.assertNotIn('.bak_',p.name);dest.append(str(p))
  self.assertEqual(len(dest),len(set(dest)));self.assertEqual(dest[-1],str(A/'iald_nucleo_fixo.json'));self.assertEqual(len(plan['native_files_pending']),2)
 def test_27_count_did_not_start(self):
  self.assertFalse((W/'COUNT_STARTED.json').exists());self.assertFalse((W/'COUNT_RESULT.json').exists())
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(base.Safety),unittest.defaultTestLoader.loadTestsFromTestCase(Linkage)])
r=unittest.TextTestRunner(verbosity=2).run(suite)
report={'status':'PASS' if r.wasSuccessful() else 'FAIL','tests':r.testsRun,'errors':len(r.errors),'failures':len(r.failures),'scope':'OFFLINE_LOCAL_SEALED_PUBLIC_REGRESSIONS_AND_JEV_DEPLOYMENT_LINKAGE_NO_SCIENTIFIC_EXECUTION','module_pins':{str(p):sha(p.read_bytes()) for p in (W/'app_patch').glob('*.py')},'staged_manifest_sha256':sha((S/'manifest_staged.json').read_bytes()),'install_candidate_sha256':sha((W/'install_plan_candidate.json').read_bytes()),'count_status':'AUTO_REVIEW_REJECTED_BEFORE_PROCESS'}
out=W/'validation/final_local_tests.json';assert not out.exists();temp=out.with_suffix('.tmp');raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert temp.read_bytes()==raw;os.replace(temp,out)
print(json.dumps(report));sys.exit(0 if r.wasSuccessful() else 1)
