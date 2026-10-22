"""Small deterministic fixtures ONLY. No campaign or real data access."""
from pathlib import Path
import ast
import copy
import json
import sys
import tempfile
import unittest
import importlib.util
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'producer'))
import numpy as np
import h5py
import tgl_ringdown_ampliacao as m
import extrai_posteriores_pseob as ex


def fixture():
    return dict(event_id='SYNTHETIC_ONLY', role='calibration', N=4, N_source=4,
                source_sha256='synthetic', dataset='samples',
                samples=dict(df220=[-.1, 0, .1, .2], dtau220=[.2, .1, 0, -.1],
                             Mfdet=[60, 61, 62, 63], af=[.6, .61, .62, .63], z=[.1, .2, .3, .4]),
                priors={k: dict(status='OPEN', declarations=[]) for k in m.FIELDS},
                thinning=dict(factor=1, seed=None, method='none'), sample_weights='equal_as_stored')


class UnitTests(unittest.TestCase):
    def test_runtime_beta(self):
        self.assertEqual(m.beta_runtime(), m.ALPHA_FINE_CODATA_2018*np.sqrt(np.e))

    def test_no_forbidden_consumer_import(self):
        tree = ast.parse(Path(m.__file__).read_text())
        imports = [x.name.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for x in node.names]
        imports += [node.module.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        self.assertFalse(set(imports) & {'h5py', 'scipy', 'extrai_posteriores_pseob'})

    def test_pairing(self):
        self.assertEqual(m.validate_events([fixture()])[0]['N'], 4)

    def test_fullsample_covariance_and_weight_diagnostics(self):
        a=fixture(); b=fixture(); b['event_id']='SECOND'; b['source_sha256']='different'
        b['samples']['dtau220']=[2*v for v in a['samples']['dtau220']]
        stats={'maximum_information_weight_INPUT':.2,'split_null_seed':132299}
        result=m.fullsample_diagnostics([a,b],stats)
        self.assertAlmostEqual(result['events'][0]['paired_covariance'][0][1],-1/60)
        np.testing.assert_allclose(result['tau_inverse_variance']['shares'],[.8,.2])
        self.assertIsNone(result['split_null_p'])
        self.assertIsNone(result['lnB'])
        self.assertEqual(len(result['leave_one_out_descriptive_means']),2)

    def test_draft_refused(self):
        with self.assertRaises(ValueError): m.validate_design({'status':'DRAFT'})

    def test_vector_prediction_against_pinned_scalar_source(self):
        base=HERE.parents[2]
        path=base/'tgl_ringdown_prediction.py'
        expected=json.loads((base/'bis/e0_core/DATASET.json').read_bytes())['prediction_module_sha256']
        m.require_pin(path,expected)
        spec=importlib.util.spec_from_file_location('_source_oracle',path)
        source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
        mass=np.array([40.,60.,80.,100.]);spin=np.array([0.,.4,.7,.9]);z=np.array([0.,.1,.5,1.])
        for reading in ('R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-GLOBAL'):
            got=m.prediction_draws(mass,spin,z,reading)['delta_tau']
            wanted=[source.prediction(float(mm),float(aa),reading,redshift=float(zz))['delta_tau'] for mm,aa,zz in zip(mass,spin,z)]
            np.testing.assert_allclose(got,wanted,rtol=2e-14,atol=0)
        q=np.array([.38-.09j,.46-.08j,.55-.08j,.75-.06j])
        got=m.prediction_draws(mass,spin,z,'R-MOD',q)['delta_tau']
        wanted=[source.prediction(float(mm),float(aa),'R-MOD',redshift=float(zz),qnm_dimensionless=qq)['delta_tau']
                for mm,aa,zz,qq in zip(mass,spin,z,q)]
        np.testing.assert_allclose(got,wanted,rtol=2e-14,atol=0)

    def test_mod_requires_exact_qnm(self):
        self.assertIsNone(m.prediction_draws([60,70],[.6,.7],[.1,.2],'R-MOD')['delta_tau'])

    def test_prop_coherent_remain_open(self):
        for reading in ('R-PROP','R-RAIZ-COHERENT'):
            self.assertEqual(m.prediction_draws([60,70],[.6,.7],[.1,.2],reading)['status'],'OPEN')

    def test_invalid_exact_qnm_rejected(self):
        with self.assertRaises(ValueError): m.prediction_draws([60,70],[.6,.7],[.1,.2],'R-MOD',[.5+.1j,.5-.1j])

    def test_negative_corotation_rejected(self):
        with self.assertRaises(ValueError): m.prediction_draws([60,70],[.9,.9],[.1,.2],'R-MOD',[.1-.1j,.1-.1j])

    def test_no_negative_spin_bcw_extrapolation(self):
        self.assertEqual(m.prediction_draws([60,70],[-.1,.7],[.1,.2],'R-B')['status'],'OPEN')

    def test_paired_reading_summaries_and_440_open(self):
        a=fixture();b=fixture();b['event_id']='SECOND';b['source_sha256']='different'
        b['samples']['af']=[.1,.2,.3,.4]
        got=m.reading_diagnostics([a,b])
        self.assertGreater(got['R-B']['geometric_free_intercept_information']['projected_information'],0)
        self.assertEqual(got['R-GLOBAL']['geometric_free_intercept_information']['projected_information'],0)
        self.assertEqual(got['R-MOD']['events'][0]['status'],'OPEN')
        self.assertTrue(all('OPEN' in row['mode_440']['status'] for row in got.values()))
        self.assertIsNone(got['R-B']['lnB'])

    def test_tiny_projection_information_not_erased(self):
        got=m.conditional_projection([1e-40,2e-40,4e-40],np.ones(3),np.ones((3,1)))
        self.assertGreater(got['projected_information'],0.)

    def test_unequal_pairing(self):
        event=fixture(); event['samples']['z'].pop()
        with self.assertRaises(ValueError): m.validate_events([event])

    def test_nonfinite(self):
        event=fixture(); event['samples']['af'][0]=float('nan')
        with self.assertRaises(ValueError): m.validate_events([event])

    def test_duplicate_event(self):
        with self.assertRaises(ValueError): m.validate_events([fixture(), fixture()])

    def test_duplicate_product_alias(self):
        other=fixture(); other['event_id']='ALIAS'
        with self.assertRaises(ValueError): m.validate_events([fixture(), other])

    def test_no_thinning(self):
        event=fixture(); event['thinning']['factor']=2
        with self.assertRaises(ValueError): m.validate_events([event])

    def test_invalid_spin(self):
        event=fixture(); event['samples']['af'][1]=1.
        with self.assertRaises(ValueError): m.validate_events([event])

    def test_weighted_samples_rejected(self):
        event=fixture(); event['sample_weights']='unknown'
        with self.assertRaises(ValueError): m.validate_events([event])

    def test_projection_constant_is_absorbed(self):
        x=np.column_stack([np.ones(5), np.arange(5.)])
        result=m.conditional_projection(np.ones(5), np.ones(5), x)
        self.assertEqual(result['projected_information'], 0.)
        self.assertIsNone(result['z_physical'])

    def test_projection_nonconstant_control(self):
        x=np.ones((4,1)); d=np.array([1.,-1.,1.,-1.])
        self.assertAlmostEqual(m.conditional_projection(d,np.ones(4),x)['projected_information'],4.)

    def test_projection_singular(self):
        with self.assertRaises(ValueError): m.conditional_projection(np.ones(4),np.ones(4),np.ones((4,2)))

    def test_matrix_verdicts(self):
        reg={'e7': {'readings': {r: {'N_target_information': None, 'status':'OPEN'} for r in m.READINGS}}}
        for count, verdict in [(0, 'AWAITING_DATA'), (1, 'INCONCLUSIVE_SYSTEMATICS')]:
            rows=m.verdict_matrix(reg,{'gate': {}},count)
            self.assertEqual(len(rows),20)
            self.assertEqual({r['reading'] for r in rows},set(m.READINGS))
            self.assertTrue(all(r['verdict']==verdict and r['lnB'] is None and r['z_physical'] is None for r in rows))

    def test_fake_green_cannot_create_likelihood(self):
        reg={'e7': {'readings': {r: {'N_target_information': None, 'status':'OPEN'} for r in m.READINGS}}}
        gate=dict(systematic_calibration_paid=True,physical_likelihood_paid=True,
                  sigma_c_physically_calibrated=0,selection_efficiency=1,global_restricted_prior_normalization=1)
        self.assertTrue(all(r['lnB'] is None and r['verdict']=='INCONCLUSIVE_SYSTEMATICS'
                            for r in m.verdict_matrix(reg,{'gate':gate},1)))

    def test_path_escape(self):
        with self.assertRaises(ValueError): m.contained(HERE,'../escape')

    def test_missing_hash(self):
        with self.assertRaises(ValueError): m.require_pin(__file__,None)

    def test_wrong_hash(self):
        with self.assertRaises(ValueError): m.require_pin(__file__,'0'*64)

    def test_missing_registration(self):
        with self.assertRaises(FileNotFoundError): m.checked_context(HERE,HERE/'NOT_PRESENT','0'*64)

    def test_atomic_no_overwrite_and_duplicate_json(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            p=Path(tmp)/'result.json'; m.publish_new(p,{'a':1})
            with self.assertRaises(FileExistsError): m.publish_new(p,{'a':2})
            self.assertEqual(m.read_json(p),{'a':1})
            p.write_text('{"x":1,"x":2}')
            with self.assertRaises(ValueError): m.read_json(p)

    def test_synthetic_hdf5_full_pairing_and_source_mutation(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root=Path(tmp); path=root/'synthetic.h5'; tar=root/'synthetic.tar'
            tar.write_bytes(b'SYNTHETIC ARCHIVE HASH FIXTURE ONLY')
            data=np.zeros(4,dtype=[(k,'f8') for k in m.FIELDS])
            for k,v in fixture()['samples'].items(): data[k]=v
            with h5py.File(path,'w') as h:
                h.create_dataset('samples',data=data)
                h.create_dataset('prior',data=np.bytes_('Uniform(minimum=-1,maximum=2)'))
            entry=dict(event_id='SYNTHETIC_ONLY',role='calibration',source_path=path.name,
                       source_sha256=m.sha(path),tar_path=tar.name,tar_sha256=m.sha(tar),
                       dataset='samples',model='SYNTHETIC_ONLY',mass_frame='detector',mass_unit='solar_mass',
                       N_source=4,fields={k:k for k in m.FIELDS},prior_paths={k:[] for k in m.FIELDS})
            entry['prior_paths']['df220']=['prior']; entry['prior_paths']['dtau220']=['prior']
            got=ex.extract_one(root,entry)
            self.assertEqual(got['samples'],fixture()['samples'])
            self.assertEqual(got['thinning'],fixture()['thinning'])
            tar.write_bytes(b'CHANGED')
            with self.assertRaises(ValueError): ex.extract_one(root,entry)


if __name__=='__main__':
    unittest.main(verbosity=2)
