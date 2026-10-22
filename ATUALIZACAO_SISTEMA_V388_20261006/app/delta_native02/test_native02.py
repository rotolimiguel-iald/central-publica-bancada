"""Offline transport regressions. No science, credentials, provider or child process."""
import copy,json,sys,unittest
from pathlib import Path
sys.dont_write_bytecode=True
import build_candidate as b
class Tests(unittest.TestCase):
    def test_full_roundtrip(self):
        old=(b.S/'haiku_prefix.md').read_bytes();new=(b.D/'haiku_prefix.md').read_text(encoding='utf-8')
        self.assertEqual(b.restore(new).encode(),old)
    def test_deterministic_reproduction(self):
        m=json.loads((b.S/'manifest_staged.json').read_bytes())
        out,_=b.convert((b.S/'haiku_prefix.md').read_text(encoding='utf-8'),m)
        self.assertEqual(out.encode(),(b.D/'haiku_prefix.md').read_bytes())
    def test_nested_table_roundtrip(self):
        x=[{'long_column_name_number':i,'long_column_name_statement':{'status':'OPEN','formula':'x=y'}} for i in range(12)]
        changes=[];y=b.encode(x,changes)
        self.assertIn('@TBL',y);self.assertEqual(b.dump(b.decode(y)),b.dump(x))
    def test_pointer_prefix_roundtrip_and_order(self):
        x={'fields':{'/a/long_component_name/'+str(i)+'/status':'OPEN' for i in range(20)}}
        changes=[];y=b.encode(x,changes)
        self.assertIn('@PATH',y['fields']);self.assertEqual(b.dump(b.decode(y)),b.dump(x))
    def test_interleaved_pointer_order_preserved(self):
        x={'fields':{'/one/a/long/status':'OPEN','/other/status':'KNOWN','/one/b/long/status':'INPUT'}}
        self.assertEqual(b.dump(b.decode(b.encode(x,[]))),b.dump(x))
    def test_reserved_key_refused(self):
        with self.assertRaises(ValueError):b.collision({'fields':{'@PATH':'bad'}})
    def test_duplicate_columns_refused(self):
        with self.assertRaises(ValueError):b.decode({'@TBL':{'columns':['x','x'],'rows':[[1,2]]}})
    def test_bad_width_refused(self):
        with self.assertRaises(ValueError):b.decode({'@TBL':{'columns':['x'],'rows':[[1,2]]}})
    def test_unknown_table_field_refused(self):
        with self.assertRaises(ValueError):b.decode({'@TBL':{'columns':['x'],'rows':[[1]],'extra':1}})
    def test_path_collision_refused(self):
        with self.assertRaises(ValueError):b.decode({'/a/b':'A','@PATH':{'prefix':'/a/','values':{'b':'B'}}})
    def test_path_malformed_refused(self):
        with self.assertRaises(ValueError):b.decode({'@PATH':{'prefix':'a','values':{'b':'B'}}})
    def test_all_pinned_originals_unchanged(self):
        for row in json.loads((b.D/'SOURCE_PINS.json').read_bytes())['files']:
            self.assertEqual(b.read_pin(row['path']),row)
    def test_protected_content_and_no_false_native_claim(self):
        r=json.loads((b.D/'TRANSFORMATION_MAP.json').read_bytes())
        self.assertTrue(r['mother_and_core_exact'] and r['exposition_bytes_unchanged'])
        self.assertEqual(r['removed_scientific_fields'],0);self.assertEqual(r['topic_count'],377)
        self.assertEqual(r['new_topics_count'],15)
        self.assertIsNone(r['offline_proxy']['native_tokens'])
        self.assertFalse(r['offline_proxy']['native_fit_verified'])
        self.assertGreater(r['offline_proxy']['native_estimate_UNVALIDATED'],183406)
if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    run=unittest.TextTestRunner(verbosity=2).run(suite)
    r={'status':'PASS' if run.wasSuccessful() else 'FAIL','tests':run.testsRun,'failures':len(run.failures),'errors':len(run.errors),
       'scope':'Pure transport structure/byte roundtrip and artifact integrity; no inference or scientific calculations',
       'provider_calls':0,'science_imports':0}
    b.fresh(b.D/'TEST_REPORT.json',b.json_bytes(r))
    sys.exit(0 if run.wasSuccessful() else 1)
