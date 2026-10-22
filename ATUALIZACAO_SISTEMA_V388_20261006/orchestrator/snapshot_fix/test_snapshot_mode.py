"""Offline snapshot regressions. Fixture certificates are synthetic, never scientific evidence."""
from pathlib import Path
import copy,hashlib,importlib.util,json,os,sys,unittest,uuid
from unittest.mock import patch
W=Path(__file__).resolve().parent;BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.dont_write_bytecode=True;sys.path.insert(0,str(BASE))
from iald_orchestrator.safe_files import replace_bytes,save_json
spec=importlib.util.spec_from_file_location('iald_orchestrator.snapshot_candidate',W/'patch/canonical_memory.py');memory=importlib.util.module_from_spec(spec);spec.loader.exec_module(memory)
def deny_external(event,args):
 if event.startswith(('socket.','subprocess.')) or event in ('os.system','os.startfile'):raise RuntimeError('External operations forbidden in tests')
 if event=='import' and str(args[0]).split('.')[0] in ('um','numpy','camb','bilby'):raise RuntimeError('Science import forbidden')
sys.addaudithook(deny_external)
sha=lambda b:hashlib.sha256(b).hexdigest()
def encoded(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def fixture(bad_seal=False,bad_proof=False):
 root=W/'f'/uuid.uuid4().hex[:8];directory=root/'memory';formal=sha(b'SYNTHETIC TEST ONLY NOT A COMPILED PROOF')
 payloads={n:('# SYNTHETIC TEST ONLY\nCartan: omega(I)=1; partial documentary retrieval.\n'+n+'\n').encode() for n in sorted(memory.SNAPSHOT_NAMES)}
 payloads['um_absoluto.json']=encoded({'fixture':True})
 payloads['tgl_kernel_proof_manifest.json']=encoded({'formal_source_hash':sha(b'OTHER') if bad_proof else formal})
 seal={'um_version':'v388','fail_closed_selftest':'FAIL_CLOSED_SELFTEST_PASSED','formal_source_hash':formal,'fixture_only':True,'sha256':{n:sha(payloads[n]) for n in ('um.py','um_absoluto.json','tgl_kernel_proof_manifest.json')}}
 if bad_seal:seal['sha256']['um.py']='0'*64
 payloads['um_absoluto_selo.json']=encoded(seal)
 generation=sha(json.dumps([(n,sha(b)) for n,b in payloads.items()],ensure_ascii=False).encode())
 snapshot=directory/'snapshots'/('v388_'+generation[:16])
 for n,b in payloads.items():replace_bytes(snapshot/n,b)
 catalog=root/'catalog.json';save_json(catalog,{'files':[{'source':str(snapshot/n),'sha256':sha(b)} for n,b in payloads.items()]})
 m=memory.build(directory,catalog)
 b={'schema':1,'source_mode':memory.SNAPSHOT_MODE,'release':'v388','generation':m['generation'],'index_sha256':m['index_sha256'],'documents':[{k:d[k] for k in ('name','sha256','bytes')} for d in m['documents']],'formal_source_hash':formal}
 save_json(snapshot/'SEALED_SNAPSHOT.json',b)
 m.update(source_mode=memory.SNAPSHOT_MODE,snapshot_root=str(snapshot),snapshot_manifest_sha256=sha((snapshot/'SEALED_SNAPSHOT.json').read_bytes()))
 save_json(directory/'manifest.json',m)
 return directory,snapshot,m,b,catalog
class SnapshotTests(unittest.TestCase):
 def setUp(self):self.directory,self.snapshot,self.m,self.binding,self.catalog=fixture()
 def save(self):save_json(self.directory/'manifest.json',self.m)
 def test_01_valid_snapshot_is_hashed_without_build(self):
  with patch.object(memory,'build',side_effect=AssertionError('No rebuild')) as build:
   m,status=memory.load(self.directory);self.assertEqual(status,'SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED');self.assertEqual(m['generation'],self.m['generation']);build.assert_not_called()
 def test_02_source_tamper_same_size_and_mtime_refused(self):
  p=self.snapshot/'DA_IRMA.md';stamp=p.stat();raw=p.read_bytes();replace_bytes(p,b'!'+raw[1:]);os.utime(p,ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
  with patch.object(memory,'build',side_effect=AssertionError('No fallback')) as build:
   with self.assertRaisesRegex(ValueError,'Integridade da fonte'):memory.load(self.directory)
   build.assert_not_called()
 def test_03_mtime_only_change_does_not_rebuild(self):
  p=self.snapshot/'DA_IRMA.md';st=p.stat();os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns+1000000000))
  with patch.object(memory,'build',side_effect=AssertionError('No rebuild')):
   m,status=memory.load(self.directory);self.assertEqual(m['generation'],self.m['generation']);self.assertIn('ALL_SOURCE_HASHES',status)
 def test_04_missing_source_no_fallback(self):
  p=self.snapshot/'DA_IRMA.md';missing=p.with_name('missing_DA_IRMA.md');assert p.resolve().is_relative_to(W/'f') and missing.resolve().is_relative_to(W/'f');p.rename(missing)
  with patch.object(memory,'build',side_effect=AssertionError('No fallback')):
   with self.assertRaises(OSError):memory.load(self.directory)
 def test_05_external_document_path_refused_before_read(self):
  self.m['documents'][0]['path']=str(self.directory.parent/'outside.py');self.save()
  with self.assertRaisesRegex(ValueError,'Caminho fora'):memory.load(self.directory)
 def test_06_external_snapshot_root_refused(self):
  self.m['snapshot_root']=str(self.directory.parent/self.snapshot.name);self.save()
  with self.assertRaisesRegex(ValueError,'Caminho fora'):memory.load(self.directory)
 def test_07_descriptor_tamper_refused(self):
  p=self.snapshot/'SEALED_SNAPSHOT.json';replace_bytes(p,p.read_bytes()+b' ')
  with self.assertRaisesRegex(ValueError,'contrato de snapshot'):memory.load(self.directory)
 def test_08_generation_mismatch_refused(self):
  self.m['generation']='0'*64;self.save()
  with self.assertRaisesRegex(ValueError,'geração'):memory.load(self.directory)
 def test_09_index_tamper_refused(self):
  p=self.directory/'index.sqlite3';replace_bytes(p,p.read_bytes()+b'!')
  with self.assertRaisesRegex(ValueError,'Integridade do índice'):memory.load(self.directory)
 def test_10_wrong_seal_binding_refused(self):
  directory,*_=fixture(bad_seal=True)
  with self.assertRaisesRegex(ValueError,'Programa, selo'):memory.load(directory)
 def test_11_wrong_formal_report_binding_refused(self):
  directory,*_=fixture(bad_proof=True)
  with self.assertRaisesRegex(ValueError,'Programa, selo'):memory.load(directory)
 def test_12_explicit_build_blocked_before_catalog_read(self):
  pins={p.name:sha(p.read_bytes()) for p in (self.directory/'manifest.json',self.directory/'index.sqlite3')}
  with self.assertRaisesRegex(ValueError,'atualização deliberada'):memory.build(self.directory,self.directory/'absent_catalog.json')
  for p in (self.directory/'manifest.json',self.directory/'index.sqlite3'):self.assertEqual(sha(p.read_bytes()),pins[p.name])
 def test_13_refresh_false_also_checks_all_bytes(self):
  p=self.snapshot/'DA_IRMA.md';replace_bytes(p,b'bad')
  with self.assertRaisesRegex(ValueError,'Integridade da fonte'):memory.load(self.directory,refresh=False)
 def test_14_mode_removed_cannot_enable_legacy_fallback(self):
  self.m.pop('source_mode');self.save()
  with self.assertRaisesRegex(ValueError,'incompleto'):memory.load(self.directory)
  with self.assertRaisesRegex(ValueError,'atualização deliberada'):memory.build(self.directory,self.catalog)
 def test_15_unknown_mode_refused(self):
  self.m['source_mode']='TRUST_ME';self.save()
  with self.assertRaisesRegex(ValueError,'desconhecido'):memory.load(self.directory)
 def test_16_duplicate_manifest_field_refused(self):
  p=self.directory/'manifest.json';raw=p.read_bytes().rstrip();replace_bytes(p,raw[:-1]+b',"source_mode":"SEALED_IMMUTABLE_SNAPSHOT"}')
  with self.assertRaisesRegex(ValueError,'duplicado'):memory.load(self.directory)
 def test_17_admission_name_substitution_refused(self):
  self.m['documents'][0]['name']='unadmitted.py';self.save()
  with self.assertRaisesRegex(ValueError,'treze identidades'):memory.load(self.directory)
 def test_18_packet_keeps_generation_sourcepins_and_partial_coverage(self):
  p=memory.prepare('Cartan',self.directory);r=p['receipt'];self.assertEqual(r['generation'],self.m['generation']);self.assertEqual(r['freshness'],'SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED');self.assertEqual(r['coverage'],'PARTIAL_RETRIEVAL_NOT_FULL_CORPUS');self.assertTrue(r['sources'])
 def test_19_historical_build_and_retrieval_unchanged(self):
  root=W/'f'/uuid.uuid4().hex[:8];src=root/'source.md';replace_bytes(src,b'Cartan explicit historical fixture\n');catalog=root/'catalog.json';save_json(catalog,{'files':[{'source':str(src),'sha256':sha(src.read_bytes())}]});directory=root/'legacy'
  m=memory.build(directory,catalog);self.assertNotIn('source_mode',m);p=memory.prepare('Cartan',directory);self.assertEqual(p['receipt']['freshness'],'SOURCE_METADATA_CHECKED')
  replace_bytes(src,b'changed historical content\n')
  with self.assertRaisesRegex(ValueError,'desatualizada'):memory.load(directory,refresh=False)
 def test_20_historical_missing_source_still_uses_verified_index(self):
  root=W/'f'/uuid.uuid4().hex[:8];src=root/'source.md';replace_bytes(src,b'Cartan legacy\n');catalog=root/'catalog.json';save_json(catalog,{'files':[{'source':str(src),'sha256':sha(src.read_bytes())}]});directory=root/'legacy';memory.build(directory,catalog)
  dest=root/'source_absent.md';assert src.resolve().is_relative_to(W/'f') and dest.resolve().is_relative_to(W/'f');src.rename(dest)
  _,fresh=memory.load(directory);self.assertEqual(fresh,'SOURCE_ACCESS_UNAVAILABLE_USING_VERIFIED_SNAPSHOT')
 def test_21_changed_original_path_is_not_read(self):
  self.m['documents'][0]['original_path']=str(self.directory/'unavailable_original.py');self.save()
  with patch.object(memory,'build',side_effect=AssertionError('No auto build')):self.assertEqual(memory.load(self.directory)[0]['generation'],self.m['generation'])
 def test_22_malformed_contract_refused_as_value_error(self):
  self.m['documents'][0].pop('sha256');self.save()
  with self.assertRaises(ValueError):memory.load(self.directory)
class ActualSnapshot(unittest.TestCase):
 def test_23_actual_13_pins_generation_index_and_retrieval(self):
  directory=W/'candidate_memory';baseline=json.loads((W/'baseline/manifest.json').read_bytes());m,fresh=memory.load(directory)
  self.assertEqual([(d['name'],d['bytes'],d['sha256']) for d in m['documents']],[(d['name'],d['bytes'],d['sha256']) for d in baseline['documents']]);self.assertEqual(m['generation'],baseline['generation']);self.assertEqual(m['index_sha256'],baseline['index_sha256'])
  p=memory.prepare('Hubble razão v388',directory);self.assertEqual(p['receipt']['generation'],baseline['generation']);self.assertTrue(p['receipt']['sources'])
  prep=json.loads((W/'PREPARATION.json').read_bytes());self.assertEqual(sha((BASE/'state/canonical_memory/index.sqlite3').read_bytes()),prep['index_sha256']);self.assertEqual(sha((BASE/'state/canonical_memory/manifest.json').read_bytes()),prep['baseline_manifest_sha256']);self.assertEqual(sha((BASE/'iald_orchestrator/canonical_memory.py').read_bytes()),prep['baseline_module_sha256']);self.assertEqual(sha((BASE/'project_fisica/MANIFESTO_LOCAL.json').read_bytes()),prep['historical_catalog_sha256'])
  self.assertFalse(any(Path(str(getattr(x,'__file__',''))).name=='um.py' for x in sys.modules.values() if x))
if __name__=='__main__':
 suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(SnapshotTests),unittest.defaultTestLoader.loadTestsFromTestCase(ActualSnapshot)]);r=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'status':'PASS' if r.wasSuccessful() else 'FAIL','tests':r.testsRun,'errors':len(r.errors),'failures':len(r.failures),'scope':'OFFLINE_SYNTHETIC_GUARD_REGRESSIONS_PLUS_REAL_13_SOURCE_BYTES_READ_ONLY','patch_sha256':sha((W/'patch/canonical_memory.py').read_bytes()),'candidate_manifest_sha256':sha((W/'candidate_memory/manifest.json').read_bytes()),'test_sha256':sha(Path(__file__).read_bytes()),'network_calls':0,'executors_called':0,'source_program_imported':False,'index_rebuilt_in_production':False}
 save_json(W/'validation/TEST_REPORT.json',report);print(json.dumps(report));sys.exit(0 if r.wasSuccessful() else 1)
