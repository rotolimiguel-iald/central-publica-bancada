"""T12 explicit engineering fixtures, never physical data/test evidence."""
from pathlib import Path
from datetime import datetime, timezone
import ast,copy,hashlib,json,math,shutil,sys,tempfile,unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[1];B=D.parents[1];ROOT=B.parent
sys.path.insert(0,str(D/'producer'))
import tgl_ringdown_ampliacao as m
import numpy as np

def fixture_chain(dest):
    paths=[B/'RINGDOWN_5SIGMA_V1.json', B/'RINGDOWN_5SIGMA_V1_1.json',
       ROOT/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_E2_REGISTRO_V1.md',
       ROOT/'TUNEL/DO_CHATGPT/ENTREGA_015_E2_REGISTRO_V1_1.md']
    for p in paths:
        target=dest/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,target)
    reg=m.read_json(D/'CANDIDATE_V1_1_1_v3.json')
    rp=dest/'ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1_1_1.json'
    m.publish_new(rp,reg)
    note=dest/reg['witness_relative_to_Chatgpt']
    note.write_text('registro_sha256: '+m.sha(rp)+'\nregistered_utc: '+datetime.now(timezone.utc).isoformat()+'\n')
    noise=ROOT/reg['e7']['nuisance_path'];npth=dest/reg['e7']['nuisance_path']
    shutil.copyfile(noise,npth)
    return reg,rp,npth,note


class RiteTests(unittest.TestCase):
    def chain(self,mutator=None,expected=None):
        with tempfile.TemporaryDirectory(dir=D) as tmp:
            root=Path(tmp);reg,rp,noise,note=fixture_chain(root)
            if mutator:mutator(root,reg,rp,noise,note)
            if expected:
                with self.assertRaises(expected):m.embedded_context(root,rp,m.sha(rp),noise,m.sha(noise))
            else:return m.embedded_context(root,rp,m.sha(rp),noise,m.sha(noise))

    def rewrite(self,reg,rp,note):
        rp.write_text(json.dumps(reg,allow_nan=False))
        note.write_text('registro_sha256: '+m.sha(rp)+'\nregistered_utc: '+datetime.now(timezone.utc).isoformat()+'\n')

    def test_valid_witnessed_chain(self):self.assertEqual(self.chain()[0]['e7_rite_v1_1']['scope'],'HISTORICAL_CALIBRATION_REPLAY_ONLY')
    def test_parent_mutation(self):
        def mutate(root,reg,rp,noise,note):reg['parent_registration_sha256']='0'*64;self.rewrite(reg,rp,note)
        self.chain(mutate,ValueError)
    def test_statistical_mutation(self):
        def mutate(root,reg,rp,noise,note):reg['statistics']['LRT_IV_threshold_strict_greater']=24.;self.rewrite(reg,rp,note)
        self.chain(mutate,ValueError)
    def test_conditional_target_mutation(self):
        def mutate(root,reg,rp,noise,note):reg['e7']['readings']['R-B']['conditional_E0_targets'][0]['N90_mixture_illustration_not_selection']=1.;self.rewrite(reg,rp,note)
        self.chain(mutate,ValueError)
    def test_operational_target_promotion(self):
        def mutate(root,reg,rp,noise,note):reg['e7']['readings']['R-B']['N_target_information']=1.;self.rewrite(reg,rp,note)
        self.chain(mutate,ValueError)
    def test_stale_amendment(self):self.chain(lambda root,r,rp,n,note:(rp.parent/'RINGDOWN_5SIGMA_V1_1_2.json').write_text('{}'),ValueError)
    def test_malformed_amendment(self):self.chain(lambda root,r,rp,n,note:(rp.parent/'RINGDOWN_5SIGMA_V1_1_02.json').write_text('{}'),ValueError)
    def test_manifest_identity_mutations(self):
        for field in ('producer_directory','guard_path','guard_sha256'):
            def mutate(root,reg,rp,noise,note):reg['e7'][field]='wrong';self.rewrite(reg,rp,note)
            self.chain(mutate,ValueError)
    def test_unused_extractor_manifest_changed(self):
        def mutate(root,reg,rp,noise,note):reg['e7']['producer_tree_sha256']['extrai_posteriores_pseob.py']='0'*64;self.rewrite(reg,rp,note)
        self.chain(mutate,ValueError)
    def test_paired_T05_scope_and_negative(self):
        reg=m.read_json(D/'CANDIDATE_V1_1_1_v3.json')
        result=m.paired_qnm_diagnostics(ROOT,reg,[])
        self.assertEqual(len(result['mode440']['rows']),10)
        real=m.read_json
        def altered(path):
            value=real(path)
            if str(path).replace('\\','/').endswith('t05/RESULT.json'):
                value['paired_predictions'][-1]['event']='NOT_CALIBRATION'
            return value
        with patch.object(m,'read_json',side_effect=altered),self.assertRaises(ValueError):
            m.paired_qnm_diagnostics(ROOT,reg,[])
    def test_missing_witness(self):self.chain(lambda root,r,rp,n,note:note.unlink(),FileNotFoundError)
    def test_ambiguous_witness(self):self.chain(lambda root,r,rp,n,note:note.write_text(note.read_text()+'registro_sha256: '+m.sha(rp)+'\n'),ValueError)
    def test_nuisance_mutation(self):self.chain(lambda root,r,rp,n,note:n.write_text('{}'),ValueError)
    def test_source_pin_missing_and_present(self):
        with tempfile.TemporaryDirectory(dir=D) as tmp:
            root=Path(tmp);p=root/'a';p.write_bytes(b'fixture')
            event=dict(event_id='FIXTURE',source_path='a',source_sha256=m.sha(p),tar_path='absent',tar_sha256='1'*64)
            r=m.verify_source_pins(root,[event]);self.assertEqual(r[0]['status'],'FILE_HASH_VERIFIED_HERE');self.assertEqual(r[1]['status'],'DECLARADO_NOT_VERIFIED_HERE')
            p.write_bytes(b'changed')
            with self.assertRaises(ValueError):m.verify_source_pins(root,[event])
    def test_missing_source_hash_not_excused(self):
        with self.assertRaises(ValueError):m.verify_source_pins(D,[dict(event_id='F',source_path='absent',source_sha256=None)])
    def test_matrix_planning_is_not_test(self):
        reg=m.read_json(D/'CANDIDATE_V1_1_1_v3.json');rows,count=m.matrix_rite(reg,{'gate':{}},[{'role':'calibration'}],[])
        self.assertEqual(count['blind_test'],0);self.assertEqual(len(rows),20)
        for r in rows:
            self.assertIsNone(r['N_target_information']);self.assertEqual(r['systematic_gate'],'red');self.assertTrue(r['gate_reasons'])
            self.assertEqual(r['verdict'],'AWAITING_DATA')
            self.assertEqual(r['conditional_E0_targets'][0]['scope_label'],'CONDITIONAL_PLANNING_ONLY')
        wanted={'R-B':3328,'R-MOD':1056,'R-RAIZ-0':976}
        for r in rows:
            if r['reading'] in wanted:self.assertEqual(r['conditional_E0_targets'][0]['N90_ceiling'],wanted[r['reading']])
    def test_blind_roles_refused(self):
        with self.assertRaises(ValueError):m.matrix_rite({}, {'gate':{}},[{'role':'blind_test'}],[])
    def test_formula_ast_identity_and_mutation_control(self):
        old=ast.parse((B/'bis/e7_prepare/producer/tgl_ringdown_ampliacao.py').read_text())
        new=ast.parse(Path(m.__file__).read_text())
        for name in ('conditional_projection','prediction_draws','reading_diagnostics','fullsample_diagnostics'):
            a=[n for n in old.body if isinstance(n,ast.FunctionDef) and n.name==name]
            b=[n for n in new.body if isinstance(n,ast.FunctionDef) and n.name==name]
            self.assertEqual(len(b),1);self.assertEqual(ast.dump(a[0]),ast.dump(b[0]))
            c=copy.deepcopy(b[0]);c.body.append(ast.Pass());self.assertNotEqual(ast.dump(a[0]),ast.dump(c))
    def test_no_external_importlib_or_producer_dir_guard(self):
        text=Path(m.__file__).read_text();self.assertNotIn('import importlib',text)
        self.assertNotIn('spec_from_file_location',text);self.assertNotIn("producer.rglob",text)
    def test_qnm_coefficients_match_scipy_and_grid(self):
        from scipy.interpolate import CubicSpline
        coeff=m.read_json(D/'QNM_CUBIC_COEFFICIENTS.json');grid=m.read_json(B/'QNM_GRID.json')
        self.assertEqual(coeff['grid_sha256'],m.sha(B/'QNM_GRID.json'))
        for mode in ('220','440'):
            g=grid['modes'][mode];x=np.linspace(min(g['spins']),max(g['spins']),2199)
            scipy=CubicSpline(g['spins'],np.asarray(g['real'])+1j*np.asarray(g['imag']),extrapolate=False)
            np.testing.assert_allclose(m.spline_qnm(x,coeff,mode),scipy(x),rtol=3e-15,atol=1e-15)
            self.assertIsNone(m.spline_qnm([min(g['spins'])-.001],coeff,mode))
            self.assertIsNone(m.spline_qnm([max(g['spins'])+.001],coeff,mode))

if __name__=='__main__':unittest.main()
