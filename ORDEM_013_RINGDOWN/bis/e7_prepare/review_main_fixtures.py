"""Independent finite review: no MC, PE, waveform, strain or network access."""
from pathlib import Path
import sys,json,hashlib,math,copy,types,tempfile
from unittest.mock import patch
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;BASE=OUT.parents[1];ROOT=BASE.parent;CODE=BASE/'bis/e2_code'
sys.path.insert(0,str(CODE))
import numpy as np
from scipy.stats import norm
import synthetic_null as sn
import null_runner as nr
import pe_runner as pe
import injection_design as inj
import fetch_registered as fetch
import remnant_conversion as remnant

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[CODE/n for n in ['null_runner.py','synthetic_null.py','route_iv_null.py','fetch_registered.py',
                       'injection_design.py','remnant_conversion.py','registration_guard.py','strain_io.py','pe_runner.py']]
paths += [BASE/n for n in ['bis/E2_DESIGN_DRAFT_001.json','refeito/prepare_e2_design_013bis.py',
                          'bis/e0_core/DATASET.json','NUISANCE_V1.json','PORTAO_DA_AMPLIACAO_V1.json',
                          'bis/e2_publication_census/PUBLICATION_CENSUS.json','bis/e2_publication_census/FREEZE_RECEIPT.json',
                          'refeito/e0_mc_guarded_013bis.py','refeito/e0_route_iv_power_013bis_v2.py']]
pins={p.relative_to(BASE).as_posix():sha(p) for p in paths}
draft=json.loads((BASE/'bis/E2_DESIGN_DRAFT_001.json').read_bytes())
gate=json.loads((BASE/'PORTAO_DA_AMPLIACAO_V1.json').read_bytes())
census=json.loads((BASE/'bis/e2_publication_census/PUBLICATION_CENSUS.json').read_bytes())
out={'no_mc_pe_waveform_strain_network':True,'pins':pins}
cells=draft['nulls']['cells'];seeds=[v['seed'] for v in cells.values()]
out['cell_counts']={k:sum(v['kind']==k for v in cells.values()) for k in ['matched_projection','route_IV']}
out['unique_seed_count']=len(set(seeds));out['cells_total']=len(cells)
out['scheduled_draws_NOT_EXECUTED']=sum(v['draws'] for v in cells.values())
tailcontrols=[]
for key,cell in cells.items():
    if cell['kind']!='matched_projection' or cell['model']!='gaussian':continue
    expected=next(t for t in gate['planning_targets'] if t['population']==cell['population'] and t['reading']==cell['reading'])
    assert cell['N_target_balanced_catalog']==math.ceil(expected['N90_mixture_illustration_not_selection'])
    comp=nr.projection_inputs(draft,cell)
    power=float(norm.sf(5-math.sqrt(comp['signal_information_with_nuisance'])))
    tailcontrols.append({'cell':key,'N':comp['N'],'source_events':comp['source_events'],
                          'information_with_INPUT_nuisance':comp['signal_information_with_nuisance'],
                          'Gaussian_conditional_power_at_amplitude1':power,
                          'scope':'Analytic declared synthetic covariance ONLY; not physical significance'})
out['fixed_target_nuisance_diagnostics']=tailcontrols
d=np.array([.1,.3,-.2,.4]);s=np.array([.2,.5,.3,.7]);X=np.column_stack([np.ones(4),s]);V=np.array([[.02,-.003],[-.003,.01]])
comp=sn.projected_components(d,s,X,V);C=np.diag(s*s)+X@V@X.T
out['woodbury_dense_absolute_error']=abs(comp['signal_information_with_nuisance']-float(d@np.linalg.solve(C,d)))
out['binomial_zero_1M']=sn.binomial_result(0,1000000)
pilot=draft['pe_jobs']['GW250114_PILOT']
try:pe.validate_config(pilot);out['draft_pilot_validate']='PASS'
except Exception as exc:out['draft_pilot_validate']=type(exc).__name__+': '+str(exc)
out['draft_pilot_duration']=pilot['duration_s']
out['missing_pilot_fields']=[k for k in ['privacy_mode','fixed_deformation_parameters','remnant_conversion_INPUT'] if k not in pilot]
out['publication']={'summary':census['summary'],'draft_candidates':len(draft['test_candidates']),
    'pin_in_draft':any('PUBLICATION_CENSUS.json' in p for p in draft['input_pins_relative_to_Chatgpt']),
    'known_published_still_in_draft':[e['event'] for e in census['events'] if e['known_delta_publication'] is True and e['event'] in draft['test_candidates']]}
out['allocation_policy_present']='allocation_policy' in draft
out['extra_code_keys']=[k for k in draft if k.startswith('extra_code')]

# Reach the generator boundary, but never construct or compute a waveform.
class WaveformBoundary(Exception):pass
def boundary(**kwargs):raise WaveformBoundary('REACHED_GENERATOR_NO_WAVEFORM')
fake_bilby=types.SimpleNamespace(gw=types.SimpleNamespace(WaveformGenerator=boundary))
ifo=types.SimpleNamespace(name='H1',strain_data=types.SimpleNamespace(start_time=100.,time_within_data=lambda t:100<=t<108))
params={'dtau220':0.,'dtau440':0.,'domega220':0.,'domega440':0.,'geocent_time':104.,'luminosity_distance':400.}
config={'mode':'calibration','event':'EXAMPLE','event_GPS':104.,'segment_start_GPS':100.,'duration_s':8,
        'offsource_exclusion_s':16.,'sample_rate_hz':4096,'minimum_frequency_hz':20.,'maximum_frequency_hz':1024.,'reference_frequency_hz':20.,
        'data':{'H1':{'onsource_path':'same','offsource_path':'same','onsource_sha256':'same','offsource_sha256':'same'}},
        'injection':{'family':'IMRPhenomXPHM','noise_kind':'REAL_OFFSOURCE','parameters':params,'target_network_optimal_SNR':20}}
with patch.dict(sys.modules,{'bilby':fake_bilby}):
    try:inj.inject_into_ifos([ifo],config,{'calibration_event_ids':['EXAMPLE']})
    except WaveformBoundary:out['analysis_window_overlaps_real_event_passes_pre_waveform_guards']=True
    except Exception as exc:out['analysis_window_overlaps_real_event_passes_pre_waveform_guards']=False;out['injection_guard_exception']=str(exc)
    nonGR=copy.deepcopy(config);nonGR['injection']['parameters']['dtau220']=.01
    try:inj.inject_into_ifos([ifo],nonGR,{'calibration_event_ids':['EXAMPLE']});out['non_GR_second_family_rejected']=False
    except ValueError:out['non_GR_second_family_rejected']=True

# Fake truncated HTTP response; no network calls. Temporary bytes remain in E7.
class Response:
    headers={'Content-Length':'10'}
    def __init__(self):self.used=False
    def __enter__(self):return self
    def __exit__(self,*a):pass
    def geturl(self):return 'https://gwosc.org/synthetic'
    def read(self,n):
        if self.used:return b''
        self.used=True;return b'abc'
with tempfile.TemporaryDirectory(dir=OUT) as temp:
    cfg={'event':'EXAMPLE','mode':'calibration','kind':'public_strain','url':'https://gwosc.org/synthetic',
         'filename':'fixture.bin','maximum_bytes':100,'license_source':'fixture','license_status':'INPUT',
         'provider_checksum':None,'provider_checksum_algorithm':None}
    with patch.object(fetch,'time_guard',lambda r:None),patch.object(fetch,'authorize_event',lambda *a:True),\
         patch.object(fetch,'output_path',lambda n:Path(temp)/n),\
         patch.object(fetch.urllib.request,'build_opener',lambda *a:types.SimpleNamespace(open=lambda *a,**k:Response())):
        try:
            rec=fetch.fetch({},'0'*64,'fixture',{'fixture':cfg})
            out['truncated_no_checksum_download']=rec
            out['truncated_receipt']=json.loads((Path(temp)/'fixture.bin.receipt.json').read_bytes())
        except Exception as exc:out['truncated_no_checksum_download']={'rejected':type(exc).__name__,'reason':str(exc)}

# Exactly two GR remnant fit calls + distance inversions, never a waveform.
import astropy
from astropy.cosmology import Planck18
source=next((Path(astropy.__file__).parent/'cosmology').rglob('Planck18.ecsv'))
p=Planck18.parameters
pars={'H0_km_s_Mpc':float(p['H0'].value),'Om0':float(p['Om0']),'Tcmb0_K':float(p['Tcmb0'].value),
      'Neff':float(p['Neff']),'m_nu_eV':p['m_nu'].value.tolist(),'Ob0':float(p['Ob0'])}
cfg={'remnant_conversion_INPUT':{'remnant_fit':'LAL_SEOBNRv4_aligned_NR_fit','cosmology_name':'Planck18_external_INPUT',
       'cosmology_source_path':str(source),'cosmology_source_sha256':sha(source),'cosmology_parameters':pars}}
cols={'mass_1':[40.,30.],'mass_2':[30.,5.],'chi_1':[.2,-.9],'chi_2':[-.1,-.9],'luminosity_distance':[400.,800.]}
converted,receipt=remnant.derive(cols,cfg,lambda:None)
out['two_row_remnant']={'columns':{k:v.tolist() for k,v in converted.items()},'receipt':receipt,
                        'cosmology_source_path':str(source),'waveforms':0}
runtime=json.loads((BASE/'bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json').read_bytes())
out['astropy_cosmology_code_in_runtime_manifest']=any('/astropy/cosmology/' in k for k in runtime['files'])
out['changed_during_fixtures']=[p.relative_to(BASE).as_posix() for p in paths if sha(p)!=pins[p.relative_to(BASE).as_posix()]]
raw=(json.dumps(out,indent=2,allow_nan=False)+'\n').encode()
with (OUT/'MAIN_CODE_REVIEW_FIXTURES.json').open('xb') as f:f.write(raw)
print(json.dumps({k:v for k,v in out.items() if k not in ('pins','truncated_receipt')},indent=2))
