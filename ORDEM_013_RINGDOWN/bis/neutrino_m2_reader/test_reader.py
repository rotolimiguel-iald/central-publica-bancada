"""T11 controls. All added measurements are explicitly synthetic FIXTURE data."""
from pathlib import Path
import copy,json,unittest,uuid
import reader
S=Path(__file__).resolve().parent

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pin=json.loads((S/'EXTRACTION_RECEIPT.json').read_bytes())['snapshot_sha256']
        cls.snapshot=reader.load_snapshot(S/'EXTRACTED_RULES.json',cls.pin)
    def row(self,group='JUNO (reator, baseline media)',autonomous=True):
        return dict(fonte='FIXTURE — never experimental data',data='2027-01-01',grupo=group,autonoma=autonomous,indep=True,
                    independence_note='FIXTURE assumption for testing only',dm21_1e5=7.53,sig_1e5=0.02)
    def evaluate(self,extra):return reader.evaluate(self.snapshot,self.snapshot['legacy_determinations']+extra,fixture=True)
    def test_frozen_hash(self):self.assertEqual(reader.sha_obj(self.snapshot['frozen']),self.snapshot['registry_frozen_hash'])
    def test_registry_tension_reproduced(self):
        result=reader.evaluate(self.snapshot,self.snapshot['legacy_determinations'])
        self.assertEqual(result['tensao_atual_sigma'],self.snapshot['registry_tension'])
        self.assertAlmostEqual(result['tensao_atual_sigma'],2.9528540277344604,places=13)
        self.assertEqual(result['verdict'],self.snapshot['registry_verdict'])
        self.assertFalse(result['registry_changed'])
    def test_one_autonomous_five_sigma_not_kill(self):
        r=self.evaluate([self.row()]);self.assertGreater(r['tensao_atual_sigma'],5)
        self.assertEqual(r['verdict'],'TGL_NU_M2_TENSION');self.assertTrue(r['tensao_global_5sigma_sem_2a_determinacao'])
    def test_global_combination_not_second(self):
        r=self.evaluate([self.row(),self.row('global contains JUNO',False)])
        self.assertEqual(len(r['grupos_autonomos_5sigma']),1);self.assertFalse(r['kill_rule_satisfeita'])
    def test_two_autonomous_groups_kill(self):
        r=self.evaluate([self.row(),self.row('KamLAND+solar (pre-JUNO)')])
        self.assertEqual(r['verdict'],'TGL_NU_M2_FALSIFIED');self.assertEqual(r['status'],'FIXTURE_NOT_DATA');self.assertFalse(r['gate_changed'])
    def test_repeated_same_group_not_two(self):
        r=self.evaluate([self.row(),self.row()]);self.assertFalse(r['kill_rule_satisfeita'])
    def test_zero_uncertainty_refused(self):
        row=self.row();row['sig_1e5']=0
        with self.assertRaises(ValueError):self.evaluate([row])
    def test_negative_mass_squared_refused(self):
        row=self.row();row['dm21_1e5']=-1
        with self.assertRaises(ValueError):self.evaluate([row])
    def test_nonfinite_refused(self):
        row=self.row();row['dm21_1e5']=float('nan')
        with self.assertRaises(ValueError):self.evaluate([row])
    def test_boolean_number_refused(self):
        row=self.row();row['sig_1e5']=True
        with self.assertRaises(ValueError):self.evaluate([row])
    def test_string_autonomy_refused(self):
        row=self.row();row['autonoma']='False'
        with self.assertRaises(ValueError):self.evaluate([row])
    def test_snapshot_pin_refused(self):
        with self.assertRaisesRegex(ValueError,'SNAPSHOT_HASH_MISMATCH'):reader.load_snapshot(S/'EXTRACTED_RULES.json','0'*64)
    def fixture_file(self):
        root=S/'fixtures'/uuid.uuid4().hex;root.mkdir(parents=True)
        doc=root/'FIXTURE_SOURCE.txt';doc.write_text('FIXTURE ONLY — NO EXPERIMENTAL PUBLICATION\n',encoding='utf-8')
        release=dict(schema='TGL_NEUTRINO_RELEASE_V1',fixture=True,release_date='2027-01-01',determinations=[self.row()],
            primary_source=dict(url='https://example.invalid/fixture',citation='FIXTURE NOT A CITATION',document_path=doc.name,document_sha256=reader.sha_file(doc)))
        p=root/'FIXTURE_RELEASE.json';p.write_text(json.dumps(release),encoding='utf-8');return p,doc,release
    def test_fixture_ingestion_requires_explicit_mode(self):
        p,_,_=self.fixture_file()
        with self.assertRaisesRegex(ValueError,'FIXTURE_NOT_SCIENTIFIC_DATA'):reader.load_release(p,reader.sha_file(p))
        r,meta=reader.load_release(p,reader.sha_file(p),True);self.assertTrue(r['fixture']);self.assertTrue(meta['fixture'])
    def test_release_hash_refused(self):
        p,_,_=self.fixture_file()
        with self.assertRaisesRegex(ValueError,'RELEASE_HASH_MISMATCH'):reader.load_release(p,'0'*64,True)
    def test_document_hash_refused(self):
        p,doc,_=self.fixture_file();doc.write_bytes(doc.read_bytes()+b'TAMPER')
        with self.assertRaisesRegex(ValueError,'PRIMARY_DOCUMENT_HASH_MISMATCH'):reader.load_release(p,reader.sha_file(p),True)
    def test_outside_source_refused(self):
        p,_,d=self.fixture_file();d['primary_source']['document_path']='../outside.txt';p.write_text(json.dumps(d),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'SOURCE_OUTSIDE_RELEASE_DIRECTORY'):reader.load_release(p,reader.sha_file(p),True)
    def test_invalid_date_refused(self):
        p,_,d=self.fixture_file();d['release_date']='2027-99-99';p.write_text(json.dumps(d),encoding='utf-8')
        with self.assertRaises(ValueError):reader.load_release(p,reader.sha_file(p),True)
    def test_duplicate_json_keys_refused(self):
        p,_,_=self.fixture_file();p.write_text('{"fixture":true,"fixture":false}',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY'):reader.load_release(p,reader.sha_file(p),True)
    def test_nonstandard_json_nan_refused(self):
        p,_,_=self.fixture_file();p.write_text('{"x":NaN}',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'NONFINITE_JSON'):reader.strict_json(p)
if __name__=='__main__':unittest.main(verbosity=2)
