"""Execute the pinned NU4 pilot against the installed Bench; no observed fit."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,math,time,urllib.request
import numpy as np
R=Path(__file__).resolve().parent
P=json.loads((R/'PREREGISTRO_R1.json').read_bytes())
def digest(b):return hashlib.sha256(b).hexdigest()
def save(name,obj):
 with (R/name).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2,allow_nan=False)
def http(path,body=None):
 raw=None if body is None else json.dumps(body,allow_nan=False).encode()
 req=urllib.request.Request('http://127.0.0.1:18777'+path,data=raw,headers={'Content-Type':'application/json','X-Cliente':'F8.2.NU4-preregistered-pilot'})
 with urllib.request.urlopen(req,timeout=60) as f:return json.loads(f.read())
if (R/'RESULTADOS_R1.json').exists():raise FileExistsError('results already exist')
for pin in P['source_pins']:
 assert digest(Path(pin['path']).read_bytes())==pin['sha256'],pin['path']
start=time.perf_counter();before=http('/api/estado');identity=P['canonical_manifest_sha256']
assert before['pronta'] and before['canone']['canonical_manifest_sha256']==identity
beta=before['canone']['beta_tgl'];alpha=before['canone']['alpha'];c=P['constants'];inp=P['reference_inputs'];hbar=P['hbar_implementation_eV_s']
tau=math.sqrt((c['h_J_s']/(2*math.pi))*c['G_SI']/c['c_m_s']**5)
time_s=P['protocol']['reactor_baseline_km']*1000/c['c_m_s']
m2=[0,inp['dm21_eV2'],inp['dm31_eV2']]
w=np.array([(1-inp['sin2theta12'])*(1-inp['sin2theta13']),inp['sin2theta12']*(1-inp['sin2theta13']),inp['sin2theta13']]);v=np.sqrt(w)
rho=np.outer(v,v)
def encode(a):return np.stack((np.asarray(a).real,np.asarray(a).imag),axis=-1).tolist()
calls=[]
def call(name,payload):
 out=http('/api/neutrino/sintetico',payload)
 assert out['synthetic'] and out['nature_sigma'] is None and out['gate_effect']=='NONE'
 assert out['canonical']['canonical_manifest_sha256']==identity
 assert out['canonical_at_delivery']['canonical_manifest_sha256']==identity
 save('CALL_'+name+'.json',dict(request=payload,response=out))
 calls.append(dict(name=name,path='CALL_'+name+'.json',sha256=digest((R/('CALL_'+name+'.json')).read_bytes())))
 x=out['result']
 if 'rho' in x:
  assert abs(x['trace_real']-1)<=2e-12 and abs(x['trace_imag'])<=2e-12
  assert x['min_eigenvalue']>=-2e-12
 if 'conserved_diagonal_generator_before' in x:
  assert abs(x['conserved_diagonal_generator_before']-x['conserved_diagonal_generator_after'])<1e-22
 return x
def physical(E,tau_value,state):
 return dict(channel='physical_mass_gap_dephasing',mass_squared_eV2=m2,energy_eV=E*1e6,tau_star_s=tau_value,Kfac=1,time_s=time_s,rho=encode(state))
parity=[]
for s in P['protocol']['parity_s']:
 a=np.zeros((4,4));a[0,0]=1;x=call('parity_'+str(s).replace('.','p'),dict(channel='boundary_parity_4state',s=s,rho=encode(a)))
 parity.append(dict(s=s,flip_probability=x['flip_probability'],trace=x['trace_real']))
mod=call('modular',dict(channel='modular_root_dephasing',modular_eigenvalues=P['protocol']['modular_eigenvalues'],s=P['protocol']['modular_s'],rho=encode(rho)))
rows=[]
def pee(a):
 a=np.array(a);z=a[:,:,0]+1j*a[:,:,1];return float((v@z@v).real)
def stable_delta(x,E):
 h=np.array(m2)/(2*E*1e6)
 return float(sum(-2*w[i]*w[j]*math.cos((h[i]-h[j])*time_s/hbar)*x['coherence_loss'][i][j] for i in range(3) for j in range(i+1,3)))
for E in P['protocol']['energies_MeV']:
 x=call('planck_'+str(E),physical(E,tau,rho));z=call('zero_'+str(E),physical(E,0,rho))
 rows.append(dict(E_MeV=E,gamma21_s=x['gamma'][0][1],gamma31_s=x['gamma'][0][2],gamma32_s=x['gamma'][1][2],loss21=x['coherence_loss'][0][1],loss31=x['coherence_loss'][0][2],Pee_zero=pee(z['rho']),delta_Pee_stable=stable_delta(x,E),delta_Pee_by_double_subtraction=pee(x['rho'])-pee(z['rho']),trace=x['trace_real'],energy_drift_eV=x['conserved_diagonal_generator_after']-x['conserved_diagonal_generator_before']))
for a,b in zip(rows,rows[1:]):assert math.isclose(a['gamma21_s']/b['gamma21_s'],(b['E_MeV']/a['E_MeV'])**2,rel_tol=2e-12)
control_tau=0.2/(beta*(m2[2]/(2*4e6*hbar))**2*time_s)
positive=call('positive_control',physical(4,control_tau,rho));positive_delta=stable_delta(positive,4)
zero4=next(r for r in rows if r['E_MeV']==4)
assert abs((pee(positive['rho'])-zero4['Pee_zero'])-positive_delta)<2e-12
assert abs(positive['coherence_loss'][0][2]-(-math.expm1(-0.1)))<2e-12
diag=np.diag(P['protocol']['diagonal_populations']);diagonal=[]
for label,t in [('zero',0),('planck',tau),('positive',control_tau)]:
 x=call('diagonal_'+label,physical(4,t,diag));a=np.array(x['rho']);z=a[:,:,0]+1j*a[:,:,1]
 diagonal.append(dict(case=label,max_state_change=float(abs(z-diag).max()),energy_drift_eV=x['conserved_diagonal_generator_after']-x['conserved_diagonal_generator_before']))
 assert np.array_equal(z,diag)
scales=[]
for label,chi in [('bulk_zero',0),('frontier',2*math.acosh(1/alpha))]:
 x=call('scale_'+label,dict(channel='beta_scale',chi=chi));scales.append(dict(case=label,chi=chi,**x))
assert math.isclose(scales[1]['beta_bulk'],beta,rel_tol=2e-12)
after=http('/api/estado');assert after['canone']['canonical_manifest_sha256']==identity
result=dict(unit='F8.2.NU4',verdict='INSTALLED_BENCH_CONDITIONAL_PILOT_PASS',started_server=before['no_ar_desde'],canonical=after['canone'],preregister_sha256=digest((R/'PREREGISTRO_R1.json').read_bytes()),runner_sha256=digest(Path(__file__).read_bytes()),finished_utc=datetime.now(timezone.utc).isoformat(),seconds=time.perf_counter()-start,calls=calls,beta_runtime=beta,tau_star_s=tau,tau_scope='Planck-time conditional instance; not physical determination',Kfac=1,baseline_km=P['protocol']['reactor_baseline_km'],hbar_eV_s=hbar,reactor=rows,parity=parity,modular=mod,positive_control=dict(tau_star_s=control_tau,delta_Pee=positive_delta,loss31=positive['coherence_loss'][0][2],physical_prediction=False),diagonal=diagonal,scales=scales,nature_sigma=None,observed_data_fit=False,luminosity_or_chandrasekhar_shift=None,gate_effect='NONE')
save('RESULTADOS_R1.json',result)
print(json.dumps(dict(verdict=result['verdict'],calls=len(calls),reactor=rows,positive_control=result['positive_control'],diagonal=diagonal),ensure_ascii=False,indent=2))
