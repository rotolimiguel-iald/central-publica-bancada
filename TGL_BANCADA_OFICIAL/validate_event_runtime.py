"""Validate registered real event against original samples without changing sources."""
from pathlib import Path
import hashlib,json,sys,time
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'adapters')]
import h5py,numpy as np
from event_sources import build_event_manifest,DEFAULT_ROOT
from resident_worker import ResidentDomain,verify_models
from event_runtime import event_view

m=build_event_manifest(root=DEFAULT_ROOT,inspect_hdf5=True)
if not m['ready_for_source_use']:raise ValueError(m['errors'])
a=m['analysis'];p={'event':m['event'],'reference_peak_gps':m['reference_peak_gps'],
 'starts_tm':a['start_times_tM'],'primary_start_tm':a['primary_start_tM'],'reference_tM_seconds':a['reference_tM_seconds'],
 'reference_mass_detector_solar':a['reference_mass_detector_solar_for_start'],'redshift':m['reference_redshift'],
 'samples':a['interval_samples'],'sample_rate_hz':a['analysis_sample_rate_hz'],'stride':a['sample_stride'],
 'input_sample_rate_hz':a['analysis_sample_rate_hz']*a['sample_stride'],'required_dq':a['quality_required'],
 'required_injections':a['injection_flags_required'],'sources':{},'noise_sources':{},
 'physical_gate':{'status':m['scientific_status']},'provenance':{'registration':m['sources']['REGISTRO_C6.json']}}
items=[]
for det,info in m['detectors'].items():
 s=m['sources'][info['strain']['source']];n=m['sources'][info['noise']['source']]
 p['sources'][det]={'name':Path(s['path']).name,'path':s['path'],'sha256':s['sha256']}
 p['noise_sources'][det]={'path':n['path'],'sha256':n['sha256']}
 items.append({'id':det,'path':s['path'],'source':s['path'],'name':Path(s['path']).name,'expected_sha256':s['sha256']})
d=ResidentDomain();d.load({'domain':'gw_strain','sources':items,'budget_bytes':1024**3})
while d.status()['status']=='LOADING':time.sleep(.05)
if d.status()['status']!='READY':raise ValueError(d.status()['errors'])
r={'profile':p,'reading':'R-B','start_tm':10,'mass_source_solar':65,'spin':.7,'redshift':.086,
 'detectors':{'H1':{'amplitude':1e-21,'phase':0},'L1':{'amplitude':1e-21,'phase':0}}}
measurements=[]
for start in p['starts_tm']:
 q=event_view(d,{**r,'start_tm':start},verify_models)
 for c in q['channels']:
  s=p['sources'][c['detector']];first=c['first_sample_index']
  with h5py.File(s['path'],'r') as f:expected=f['strain/Strain'][first:first+p['samples']*p['stride']:p['stride']]
  np.testing.assert_array_equal(c['strain'],expected)
  assert c['quality']['passed'] and c['noise']['whitener_shape']==[407,410]
 measurements.append({'start_tm':start,'worker_ms':q['elapsed_ms'],'strain_reads':q['data_reads_since_load'],
  'detectors':[{'detector':c['detector'],'first_sample_gps':c['first_sample_gps'],'first_index':c['first_sample_index'],
   'rows':len(c['strain']),'quality_passed':c['quality']['passed'],'raw_slice_identical':True} for c in q['channels']]})
zero=event_view(d,{**r,'reading':'R-GLOBAL'},verify_models)
assert all(c['gr']==c['tgl'] for c in zero['channels'])
result={'status':'REAL_EVENT_OVERLAY_VALIDATED_NOT_INFERENCE','event':p['event'],
 'registration_sha256':m['sources']['REGISTRO_C6.json']['sha256'],'physical_gate':p['physical_gate'],
 'full_domain_loaded':False,'resident_event_files':2,'measurements':measurements,'r_global_matches_gr':True,
 'source_hashes_verified':True,'mask_epochs_verified':True,'source_manifest':m,
 'code_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['event_sources.py','adapters/event_runtime.py','adapters/resident_worker.py']}}
out=ROOT/'state'/'validation_event_runtime.json';raw=json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2).encode()
tmp=out.with_suffix('.new');tmp.write_bytes(raw);assert tmp.stat().st_size==len(raw);tmp.replace(out)
print(json.dumps({k:v for k,v in result.items() if k not in ('source_manifest','code_sha256')},ensure_ascii=False))
d.release()
