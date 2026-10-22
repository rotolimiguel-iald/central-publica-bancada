from pathlib import Path
import hashlib,json,math,datetime
B=Path(__file__).resolve().parent
def read(name):return json.loads((B/name).read_text(encoding='utf8'))
def pin(p):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
verified=[]
def walk(v):
 if isinstance(v,dict):
  if isinstance(v.get('path'),str) and isinstance(v.get('sha256'),str):
   p=Path(v['path']);raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==v['sha256'],str(p)
   if 'bytes' in v:assert len(raw)==v['bytes'],str(p)
   verified.append(pin(p))
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
roots=['construction/DELIVERY_CONSTRUCTION_R66.json','construction/FREEZE_R66.json','construction/PLAN_COLLISION_R66.json','PREEXEC_REVIEW_BOSONIC_R66.json','FREEZE_BOSONIC_R66.json','PLAN_BOSONIC_R66.json','BOSONIC_COMMAND_RESULT_R66.json','sources/DELIVERY_R66.json','sources/KNOWN_SEMIGROUPS_R66.json','CANONICAL_PINS_R66.json']
for n in roots:walk(read(n))
sp=read('sources/SOURCE_PINS_R66.json');ranges=0
for row in sp['sources']:
 walk(row);lines=Path(row['path']).read_text(encoding='utf8').splitlines()
 for e in row['excerpts']:
  txt='\n'.join(lines[e['line_start']-1:e['line_end']])
  assert txt==e['text'];assert hashlib.sha256(txt.encode()).hexdigest()==e['excerpt_utf8_lf_sha256'];ranges+=1
c=read('construction/RESULT_COLLISION_R66.json');cb=read('BOSONIC_COMMAND_RESULT_R66.json');cc=read('construction/COMMAND_COLLISION_R66.json');s=read('RESULT_BOSONIC_R66.json')
assert cc['exit_code']==cb['exit_code']==0
for x in c['checks']:
 assert math.isfinite(x['value']);actual=(x['value']<=x['bound']) if x['relation']=='le' else (x['value']>x['bound']);assert x['passed']==actual and actual
for x in s['checks']:
 assert math.isfinite(x['value']);actual=(x['value']>x['limit']) if x['id'].startswith('negative_') else (x['value']<=x['limit']);assert x['pass']==actual and actual
assert len(c['checks'])==115 and len(s['checks'])==68
p=read('construction/PLAN_COLLISION_R66.json');ratios={}
for name,rows in c['branches'].items():
 values=[]
 for j in [2,3]:
  a,z=rows[j-1],rows[j]
  local=a['local_channel_error_F']/z['local_channel_error_F'];global_=a['global_error_F']/z['global_error_F'];der=a['generator_derivative_error_F']/z['generator_derivative_error_F']
  assert 3.2<local<=4.8 and 1.6<global_<=2.4 and 1.6<der<=2.4
  values.append({'N':z['N'],'local':local,'global':global_,'derivative':der})
 assert rows[-1]['global_relative_error_F']<=.01 and rows[-1]['generator_derivative_relative_F']<=.05
 ratios[name]=values
# Independent scalar expression for the infinite Dyson tail; no matrices/trajectories.
tails=[]
for row in s['cutoff_comparisons']:
 x=2*abs(s['parameters']['Omega'])*row['t'];q=row['cut']-2
 analytic=2*(math.expm1(x)-sum(x**k/math.factorial(k) for k in range(1,q+1)))
 assert abs(analytic-row['analytic_bound'])<1e-14
 assert row['trace_norm_difference']<=analytic+1e-10
 tails.append({'cut':row['cut'],'t':row['t'],'tail_independent':analytic,'difference':row['trace_norm_difference']})
for state in s['states']:
 assert state['min_eigenvalue']>=-1e-10 and abs(complex(*state['trace'])-1)<=1e-10
 assert state['mean_N']<=2+abs(s['parameters']['Omega'])*state['t']+1e-10
f=read('construction/FREEZE_R66.json');r=read('construction/PREEXEC_REVIEW_R66.json');fb=read('FREEZE_BOSONIC_R66.json');rb=read('PREEXEC_REVIEW_BOSONIC_R66.json')
dt=datetime.datetime.fromisoformat
assert dt(r['created_utc'])<dt(f['created_utc'])<dt(c['started_utc'])<dt(c['ended_utc'])
assert dt(rb['created_utc'])<dt(fb['utc'])<dt(s['started_utc'])<dt(s['finished_utc'])
mp=read('MEMORY_PLAN_R66.json');walk(mp['applier']);walk(mp['report']);surfaces=[]
for row in mp['surfaces']:
 raw=Path(row['path']).read_bytes();extra=Path(row['append']['path']).read_bytes()
 assert pin(row['path'])==row['before'] and pin(row['append']['path'])==row['append']
 assert len(raw)==row['before_bytes'] and hashlib.sha256(raw+extra).hexdigest()==row['after_sha256']
 assert mp['marker'].encode() not in raw
 surfaces.append({'path':row['path'],'before_sha256':row['before']['sha256'],'before_bytes':len(raw),'append_bytes':len(extra),'prefix_planned':True,'expected_after':row['after_sha256']})
assert len(surfaces)==8
out={'status':'PASS_INDEPENDENT_CUSTODY_AND_RECORDED_ARITHMETIC','reviewer':'codex-mission-memory-review','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script':pin(__file__),'pin_occurrences_verified':len(verified),'unique_pins_verified':len({(x['path'],x['sha256']) for x in verified}),'source_files':len(sp['sources']),'source_ranges':ranges,'campaign_recorded_checks':{'collision':115,'bosonic':68},'convergence_ratios_recomputed':ratios,'dyson_tails_independent_scalar':tails,'preexec_freeze_start_order':True,'memory_baselines':surfaces,'canonical_pin_count':len(read('CANONICAL_PINS_R66.json')['checks']),'limits':['Recorded comparisons/pins checked, not 183 independently rerun experiments.','No expm, trajectory, provider, Lean or original model executed.','Scalar tails/ratios recomputed independently from recorded parameters only.']}
with (B/'INDEPENDENT_CUSTODY_R66.json').open('x',encoding='utf8',newline='\n') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['memory_baselines','convergence_ratios_recomputed','dyson_tails_independent_scalar']},ensure_ascii=False))
