"""Event adapter controls in the installed scientific runtime."""
import hashlib, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'adapters'))
try:
 import h5py, numpy as np
 from resident_worker import ResidentDomain, verify_models
 from event_runtime import event_view, NOISE_CACHE, quality_for_window
 AVAILABLE=True
except ImportError: AVAILABLE=False

@unittest.skipUnless(AVAILABLE,'Scientific WSL runtime required')
class EventTests(unittest.TestCase):
 def make(self,root):
  root=Path(root);d=ResidentDomain();d.state.update(status='READY',load_id='fixture',reads_after_load=0)
  p=dict(event='FIXTURE',reference_peak_gps={'H1':1000.5,'L1':1000.503},starts_tm=[6,10,12],primary_start_tm=10,
   samples=410,stride=2,input_sample_rate_hz=4096,sample_rate_hz=2048,reference_tM_seconds=.001,
   reference_mass_detector_solar=65,redshift=.1,required_dq=['DATA'],required_injections=['NO_HW'],
   sources={},noise_sources={},physical_gate={'status':'INCONCLUSIVE_SYSTEMATICS'},provenance={'fixture':True})
  for det in ['H1','L1']:
   name=det+'.h5'; path=root/name; sha=hashlib.sha256(det.encode()).hexdigest()
   y=np.sin(np.arange(8192)*.01)*1e-21
   attrs={'Xstart':1000,'Xspacing':1,'Xunits':'second'}
   d.arrays[det]={'/strain/Strain':y,'/quality/simple/DQmask':np.ones(2,dtype='u4'),'/quality/injections/Injmask':np.ones(2,dtype='u4')}
   d.records.append(dict(id=det,name=name,source_path=str(path),source_sha256=sha,strain_array_sha256=hashlib.sha256(y.tobytes()).hexdigest(),
    detector=det,dt_s=1/4096,gps_start=1000,rows=8192,metadata={'/quality/simple/DQShortnames':['DATA'],'/quality/injections/InjShortnames':['NO_HW']},
    dataset_attributes={'/quality/simple/DQmask':attrs,'/quality/injections/Injmask':dict(attrs)}))
   p['sources'][det]={'name':name,'path':str(path),'sha256':sha}
   n=root/(det+'.npz');np.savez(n,whitener_scaled=np.eye(407,410),frequency_hz=np.arange(32.),median_psd_strain=np.ones(32)*1e-44)
   p['noise_sources'][det]={'path':str(n),'sha256':hashlib.sha256(n.read_bytes()).hexdigest()}
  r=dict(profile=p,start_tm=10,reading='R-GLOBAL',mass_source_solar=65/1.1,spin=.7,redshift=.1,
   detectors={'H1':{'amplitude':1e-21,'phase':0},'L1':{'amplitude':2e-21,'phase':.3}})
  return d,p,r
 def test_same_samples_and_model_control_with_noise_in_ram(self):
  with tempfile.TemporaryDirectory() as root:
   d,p,r=self.make(root);a=event_view(d,r,verify_models)
   self.assertEqual(a['data_reads_since_load'],0);self.assertEqual(a['physical_gate']['status'],'INCONCLUSIVE_SYSTEMATICS')
   for c in a['channels']:
    self.assertEqual(len(c['strain']),410);self.assertTrue(c['quality']['passed']);self.assertEqual(c['noise']['whitener_shape'],[407,410])
    np.testing.assert_array_equal(c['gr'],c['tgl']);self.assertAlmostEqual(np.diff(c['time_s'])[0],1/2048)
    self.assertEqual(len(c['normalized']['strain']),410)
    self.assertTrue(c['normalization']['mixes_samples_nonlocally'])
    self.assertLess(c['normalization']['norm_relative_errors']['residual_gr'],1e-8)
    np.testing.assert_allclose(np.array(c['normalized']['strain'])-np.array(c['normalized']['gr']),c['normalized']['residual_gr'],atol=1e-12)
    self.assertAlmostEqual(c['gr'][0],r['detectors'][c['detector']]['amplitude']*np.cos(r['detectors'][c['detector']]['phase']))
   # Source strain paths deliberately do not exist; the resident arrays are sufficient.
   for n in p['noise_sources'].values():Path(n['path']).unlink()
   b=event_view(d,{**r,'reading':'R-B','mass_source_solar':80},verify_models)
   for before,after in zip(a['channels'],b['channels']):
    np.testing.assert_array_equal(before['strain'],after['strain']);np.testing.assert_array_equal(before['time_s'],after['time_s'])
    self.assertFalse(np.array_equal(after['gr'],after['tgl']))
   json.dumps(b,allow_nan=False)
 def test_missing_quality_and_wrong_source_are_refused(self):
  with tempfile.TemporaryDirectory() as root:
   d,p,r=self.make(root);d.arrays['H1']['/quality/simple/DQmask'][0]=0
   with self.assertRaisesRegex(ValueError,'quality|DQ'):event_view(d,r,verify_models)
   d.arrays['H1']['/quality/simple/DQmask'][0]=1;d.records[0]['source_sha256']='wrong'
   with self.assertRaisesRegex(ValueError,'uniquely resident'):event_view(d,r,verify_models)
 def test_quality_uses_own_epoch_and_noise_pin_is_checked(self):
  with tempfile.TemporaryDirectory() as root:
   d,p,r=self.make(root);d.records[0]['dataset_attributes']['/quality/simple/DQmask']['Xstart']=2000
   with self.assertRaisesRegex(ValueError,'coverage'):event_view(d,r,verify_models)
   d.records[0]['dataset_attributes']['/quality/simple/DQmask']['Xstart']=1000
   n=p['noise_sources']['H1'];Path(n['path']).write_bytes(b'changed')
   with self.assertRaisesRegex(ValueError,'noise cache changed'):event_view(d,r,verify_models)
 def test_partial_domain_with_complete_registered_pair_is_usable(self):
  with tempfile.TemporaryDirectory() as root:
   d,p,r=self.make(root);d.state['status']='PARTIAL'
   q=event_view(d,r,verify_models)
   self.assertEqual(q['domain_load_status'],'PARTIAL');self.assertEqual(len(q['channels']),2)
 def test_quality_covers_bins_between_endpoints(self):
  with tempfile.TemporaryDirectory() as root:
   d,p,r=self.make(root)
   d.arrays['H1']['/quality/simple/DQmask']=np.array([1,0,1],dtype='u4')
   d.arrays['H1']['/quality/injections/Injmask']=np.ones(3,dtype='u4')
   with self.assertRaisesRegex(ValueError,'DQ'):
    quality_for_window(d.arrays['H1'],d.records[0],np.array([1000.5,1002.5]),p)

 def test_unregistered_start_and_loading_refused(self):
  with tempfile.TemporaryDirectory() as root:
   d,p,r=self.make(root)
   with self.assertRaisesRegex(ValueError,'registered'):event_view(d,{**r,'start_tm':9.1},verify_models)
   d.state['status']='LOADING'
   with self.assertRaisesRegex(ValueError,'Complete'):event_view(d,r,verify_models)

if __name__=='__main__':unittest.main()
