"""Write explicit finite case inputs before native children; no waveform calls."""
import hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
plan=json.loads((HERE/'PLAN_INPUTS.json').read_bytes())
replay=json.loads((HERE/'PRIOR_REPLAY.json').read_bytes())
rawlog=(HERE/'sources/original_PRIVATE.log').read_text()
masspairs=[tuple(map(float,m)) for m in re.findall(r"'mass_1': np.float64\(([^)]+)\), 'mass_2': np.float64\(([^)]+)\)",rawlog)]
matches=[]
for pair in masspairs:
    candidates=[r for r in replay['draws'] if (r['mass_1_kg_using_Bilby'],r['mass_2_kg_using_Bilby'])==pair]
    if len(candidates)!=1:raise ValueError('No exact physical mass match to log')
    matches.append(candidates[0]['draw_index_starting_1'])
def save(name,data):
    with (HERE/name).open('xb') as stream:stream.write((json.dumps(data,indent=2)+'\n').encode())
save('REPLAY_MATCHES.json',{'status':'TWO_LOGGED_DOMAIN_ERRORS_MATCH_DRAW_MASS_PAIRS_EXACTLY','draw_indices':matches,
       'limitation':'Matching logged errors does not identify the subsequent crash call; log omits deformation fields.',
       'replay_sha256':hashlib.sha256((HERE/'PRIOR_REPLAY.json').read_bytes()).hexdigest()})
required=['mass_1','mass_2','chi_1','chi_2','luminosity_distance','theta_jn','phase','geocent_time','dtau220','dtau440','domega220','domega440']
draws=[{k:r['parameters'][k] for k in required} for r in replay['draws']]
common=plan['common_diagnostic_parameters']
representatives=[]
for x in plan['planned_waveform_inputs']:
    p={k:v for k,v in x.items() if k!='case'}
    p.update({k:common[k] for k in ('luminosity_distance','theta_jn','phase','geocent_time')})
    representatives.append(p)
folder=HERE/'cases';folder.mkdir(exist_ok=True)
cases=[('SEQUENCE_8_ORIGINAL',draws[0],1024,draws),
       ('DRAW2_1024',draws[1],1024,None),('DRAW8_1024',draws[7],1024,None),
       ('DRAW2_2048',draws[1],2048,None),('DRAW8_2048',draws[7],2048,None),
       ('LOW_GR_1024',representatives[0],1024,None),('LOW_GR_2048',representatives[0],2048,None),
       ('DRAW2_8192',draws[1],8192,None),('LOW_DEFORMED_8192',representatives[1],8192,None)]
for name,params,fmax,seq in cases:
    obj={'plan_sha256':hashlib.sha256((HERE/'PLAN_INPUTS.json').read_bytes()).hexdigest(),'parameters':params,
         'generation_fmax':fmax,'analysis_band_unchanged_for_comparison':[20,1024],
         'scope':'Source-only diagnostic, not registered config change'}
    if seq:obj['sequence']=seq
    save('cases/'+name+'.json',obj)
print(json.dumps({'logged_matches':matches,'cases':[x[0] for x in cases]}))
