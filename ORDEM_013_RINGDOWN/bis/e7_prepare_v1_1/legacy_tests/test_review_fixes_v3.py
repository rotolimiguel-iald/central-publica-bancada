"""Finite deterministic review regressions; no real extraction or campaign."""
import copy
from datetime import datetime
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'producer'))
import numpy as np
import h5py
import tgl_ringdown_ampliacao as m
import extrai_posteriores_pseob as ex


def fixture():
    planned = dict(event_id='SYNTHETIC', role='calibration', source_path='source.h5',
                   source_sha256='1'*64, tar_path='source.tar', tar_sha256='2'*64,
                   dataset='samples', model='SYNTHETIC', mass_frame='detector',
                   mass_unit='solar_mass', N_source=8, fields={k:k for k in m.FIELDS},
                   prior_paths={k:['prior/'+k] if k in ('df220','dtau220') else [] for k in m.FIELDS})
    event = {k:v for k,v in planned.items() if k not in ('fields','prior_paths')}
    event.update(N=8, source_field_mapping=copy.deepcopy(planned['fields']),
                 thinning=dict(factor=1,seed=None,method='none'), sample_weights='equal_as_stored',
                 samples={'df220':np.linspace(-.1,.1,8).tolist(), 'dtau220':np.linspace(-.2,.1,8).tolist(),
                          'Mfdet':list(range(60,68)), 'af':np.linspace(.6,.7,8).tolist(),
                          'z':np.linspace(.1,.2,8).tolist()}, priors={})
    for k, paths in planned['prior_paths'].items():
        event['priors'][k] = dict(status='DECLARADO_TEXT_NOT_NORMALIZED' if paths else
                                 'OPEN_DERIVED_PRIOR_NOT_DECLARED', joint_factorization='OPEN', density=None,
                                 declarations=[dict(path=p,text=['Uniform(-1, 2)']) for p in paths])
    plan = dict(status='READY_FOR_REGISTERED_CALIBRATION_EXTRACTION', catalogue='SYNTHETIC', events=[planned])
    spec = dict(plan_sha256='3'*64, producer_tree_sha256={'synthetic.py':'4'*64},
                plan_path='plan.json', nuisance_path='nuisance.json', nuisance_sha256='5'*64,
                prediction_source_sha256='6'*64,
                readings={r:dict(N_target_information=None,status='OPEN') for r in m.READINGS})
    payload = dict(schema='POSTERIORES_PSEOB_V1',catalogue=plan['catalogue'],events=[event],
                   registration_sha256='7'*64,plan_sha256=spec['plan_sha256'],
                   producer_tree_sha256=spec['producer_tree_sha256'],authorization_sha256='8'*64)
    return payload, plan, spec


class ReviewFixes(unittest.TestCase):
    def contract(self, mutate=None):
        payload,plan,spec=fixture()
        if mutate:mutate(payload, payload['events'][0])
        return m.validate_payload_contract(payload,plan,spec,'7'*64,'8'*64)

    def test_valid_fullsample_contract(self):
        self.assertEqual(self.contract()[0]['N'],8)

    def test_truncated_self_consistent_payload(self):
        def cut(p,e):
            e['samples']={k:v[:2] for k,v in e['samples'].items()};e['N']=e['N_source']=2
        with self.assertRaisesRegex(ValueError,'count'):self.contract(cut)

    def test_each_frame_unit_model_mapping_mismatch(self):
        for key,value in [('mass_frame','source'),('mass_unit','kilogram'),('model','WRONG'),
                          ('source_field_mapping',{k:'wrong' for k in m.FIELDS})]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                self.contract(lambda p,e:e.update({key:value}))

    def test_schema_authorization_catalogue_mismatch(self):
        for key in ('schema','authorization_sha256','catalogue'):
            with self.subTest(key=key),self.assertRaises(ValueError):
                self.contract(lambda p,e:p.update({key:'WRONG'}))
        with self.assertRaises(ValueError):self.contract(lambda p,e:p.pop('authorization_sha256'))

    def test_each_prior_provenance_mutation(self):
        mutations=[lambda d:d.update(status='ANY_STRING',declarations=None),
                   lambda d:d.update(declarations=[]),
                   lambda d:d['declarations'][0].update(path='wrong'),
                   lambda d:d['declarations'][0].update(text=['']),
                   lambda d:d['declarations'][0].update(text=[3]),
                   lambda d:d['declarations'][0].update(text=['x'*100001]),
                   lambda d:d.update(density=1),lambda d:d.update(joint_factorization='PAID')]
        for i,change in enumerate(mutations):
            with self.subTest(i=i),self.assertRaises(ValueError):
                self.contract(lambda p,e:change(e['priors']['dtau220']))

    def test_derived_priors_stay_open(self):
        with self.assertRaises(ValueError):
            self.contract(lambda p,e:e['priors']['Mfdet'].update(status='PAID'))

    def test_end_to_end_contract_before_diagnostics(self):
        payload,plan,spec=fixture()
        reg=dict(e7=spec,registered_utc='2026-01-01T00:00:00+00:00',
                 statistics=dict(maximum_information_weight_INPUT=.2,split_null_seed=1))
        guard=types.SimpleNamespace(utc=datetime.fromisoformat,authorize_event=lambda *a:True)
        auth=dict(status='AUTHORIZED_BY_PRINCIPAL_AFTER_E2',registration_sha256='7'*64,
                  plan_sha256=spec['plan_sha256'],producer_tree_sha256=spec['producer_tree_sha256'],
                  registered_utc='2026-01-02T00:00:00+00:00')
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root=Path(tmp)
            for name,obj in [('plan.json',plan),('nuisance.json',{'gate':{}}),('auth.json',auth)]:
                m.publish_new(root/name,obj)
            ah=m.sha(root/'auth.json');payload['authorization_sha256']=ah
            m.publish_new(root/'payload.json',payload)
            original_pin=m.require_pin
            def pin(path,wanted):
                if Path(path).name in ('source.h5','source.tar'):return
                original_pin(path,wanted)
            with patch.object(m,'checked_context',return_value=(reg,guard)),patch.object(m,'require_pin',side_effect=pin):
                result=m.run(root,'unused','7'*64,root/'payload.json',m.sha(root/'payload.json'),root/'auth.json',ah)
                self.assertEqual(result['fullsample_diagnostics']['events'][0]['N'],8)
                self.assertIsNone(result['lnB'])
                event=payload['events'][0];event['N']=event['N_source']=2
                event['samples']={k:v[:2] for k,v in event['samples'].items()}
                m.publish_new(root/'truncated.json',payload)
                with patch.object(m,'fullsample_diagnostics',side_effect=AssertionError('diagnostics reached')):
                    with self.assertRaisesRegex(ValueError,'count'):
                        m.run(root,'unused','7'*64,root/'truncated.json',m.sha(root/'truncated.json'),root/'auth.json',ah)
                with self.assertRaisesRegex(ValueError,'authorization path'):
                    m.run(root,'unused','7'*64,root/'payload.json',m.sha(root/'payload.json'))
                with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):
                    m.run(root,'unused','7'*64,root/'payload.json',m.sha(root/'payload.json'),root/'auth.json','0'*64)
                auth['registered_utc']='2025-01-01T00:00:00+00:00'
                m.publish_new(root/'early.json',auth)
                with self.assertRaisesRegex(ValueError,'predates'):
                    m.run(root,'unused','7'*64,root/'payload.json',m.sha(root/'payload.json'),root/'early.json',m.sha(root/'early.json'))

    def prior(self, kind):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            path=Path(tmp)/'synthetic_prior.h5'
            with h5py.File(path,'w') as h:
                if kind=='virtual':
                    layout=h5py.VirtualLayout(shape=(1,),dtype='S10')
                    layout[:]=h5py.VirtualSource(str(Path(tmp)/'NEVER_OPEN.h5'),'data',shape=(1,))
                    h.create_virtual_dataset('prior',layout)
                elif kind=='external':
                    h.create_dataset('prior',shape=(1,),dtype='S10',external=[(str(Path(tmp)/'NEVER_READ.bin'),0,10)])
                elif kind=='object_reference':h.create_dataset('prior',shape=(1,),dtype=h5py.ref_dtype)
                elif kind=='vlen_numeric':h.create_dataset('prior',shape=(1,),dtype=h5py.vlen_dtype(np.dtype('int32')))
                elif kind=='softlink':h['prior']=h5py.SoftLink('/NEVER_READ')
                elif kind=='empty':h.create_dataset('prior',data=np.bytes_(''))
                elif kind=='oversize':h.create_dataset('prior',shape=(1,),dtype='S100001')
                elif kind=='vlen_text':h.create_dataset('prior',data=['Uniform(-1,2)'],dtype=h5py.string_dtype())
                else:h.create_dataset('prior',data=np.bytes_('Uniform(-1,2)'))
                entry={'prior_paths':{k:['prior'] if k in ('df220','dtau220') else [] for k in m.FIELDS}}
                return ex.prior_metadata(h,entry)

    def test_prior_virtual_refused_without_external_read(self):
        with self.assertRaisesRegex(ValueError,'Unsupported'):self.prior('virtual')

    def test_prior_external_storage_refused_without_external_read(self):
        with self.assertRaisesRegex(ValueError,'Unsupported'):self.prior('external')

    def test_prior_object_reference_refused(self):
        with self.assertRaisesRegex(ValueError,'Unsupported'):self.prior('object_reference')

    def test_prior_vlen_numeric_refused(self):
        with self.assertRaisesRegex(ValueError,'Unsupported'):self.prior('vlen_numeric')

    def test_prior_softlink_refused(self):
        with self.assertRaisesRegex(ValueError,'unpinned'):self.prior('softlink')

    def test_prior_empty_and_oversize_refused(self):
        for kind in ('empty','oversize'):
            with self.subTest(kind=kind),self.assertRaises(ValueError):self.prior(kind)

    def test_prior_actual_text_types_accepted(self):
        for kind in ('fixed_text','vlen_text'):
            self.assertEqual(self.prior(kind)['df220']['declarations'][0]['text'],['Uniform(-1,2)'])

    def test_stale_guard_pin_refused_before_import(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root=Path(tmp);m.publish_new(root/'reg.json',dict(e7=dict(producer_directory='producer',
                producer_tree_sha256={},guard_path='guard.py',guard_sha256='0'*64)))
            with (root/'guard.py').open('xb') as f:f.write(b"raise AssertionError('guard executed')")
            real_producer=Path(m.__file__).resolve().parent
            original=m.contained
            with patch.object(m,'validate_design'),patch.object(m,'contained',side_effect=lambda r,p:
                              real_producer if p=='producer' else original(r,p)),patch.object(m,'sha',side_effect=lambda p:
                              '9'*64 if Path(p).suffix=='.py' else __import__('hashlib').sha256(Path(p).read_bytes()).hexdigest()):
                reg=m.read_json(root/'reg.json')
                reg['e7']['producer_tree_sha256']={p.name:'9'*64 for p in real_producer.glob('*.py')}
                m.publish_new(root/'reg2.json',reg)
                with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):
                    m.checked_context(root,root/'reg2.json',m.sha(root/'reg2.json'))


if __name__=='__main__':unittest.main(verbosity=2)
