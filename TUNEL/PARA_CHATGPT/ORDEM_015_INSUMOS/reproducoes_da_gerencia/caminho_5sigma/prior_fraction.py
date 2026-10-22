"""Fracao da prior REGISTRADA do piloto (PLAN_INPUTS.json, sha16 bd5e1a56537cc842) que (a) recusa por EDOM em fmax_gen=1024 com RG (dtau=0)
e (b) aborta nativamente em fmax_gen=2048 com deformacoes amostradas da prior. Subprocessos isolados; semente fixa; nada da bancada executado."""
import json, subprocess, sys, time, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); CHILD=open(os.path.join(HERE,'child.py')).read()
rng=np.random.default_rng(20260923)
def draw():
    while True:
        m1=rng.uniform(15,100); m2=rng.uniform(10,100)
        if m2<=m1 and m2/m1>=0.125: break
    return dict(mass_1=m1,mass_2=m2,chi_1=rng.uniform(-0.99,0.99),chi_2=rng.uniform(-0.99,0.99),
        luminosity_distance=rng.uniform(100,2000),theta_jn=float(np.arccos(rng.uniform(-1,1))),phase=rng.uniform(0,2*np.pi))
def run(p,fmax):
    r=subprocess.run([sys.executable,'-c',CHILD,json.dumps(p),str(fmax)],capture_output=True,text=True,timeout=120)
    if r.returncode!=0: return 'NATIVE_ABORT_rc%d'%r.returncode
    try: return json.loads(r.stdout.strip().splitlines()[-1])['status']
    except Exception: return 'UNPARSED'
N=120; res={'GR_fmax1024':{}, 'GR_fmax2048':{}, 'PRIOR_DEFORM_fmax2048':{}, 'PRIOR_DEFORM_220only_fmax2048':{}}
t0=time.perf_counter()
for i in range(N):
    p=draw(); g=dict(p,dtau220=0.,dtau440=0.,domega220=0.,domega440=0.)
    for lab,fm in (('GR_fmax1024',1024),('GR_fmax2048',2048)):
        s=run(g,fm); res[lab][s]=res[lab].get(s,0)+1
    d=dict(p,dtau220=rng.uniform(-0.8,2),dtau440=rng.uniform(-0.8,4),domega220=rng.uniform(-0.8,2),domega440=rng.uniform(-0.8,2))
    s=run(d,2048); res['PRIOR_DEFORM_fmax2048'][s]=res['PRIOR_DEFORM_fmax2048'].get(s,0)+1
    d2=dict(p,dtau220=rng.uniform(-0.8,2),dtau440=0.,domega220=rng.uniform(-0.8,2),domega440=0.)
    s=run(d2,2048); res['PRIOR_DEFORM_220only_fmax2048'][s]=res['PRIOR_DEFORM_220only_fmax2048'].get(s,0)+1
    if i%20==19: print(i+1,res,round(time.perf_counter()-t0,1),'s',flush=True)
res['N']=N; res['wall_s']=time.perf_counter()-t0; res['prior_source']='PLAN_INPUTS.json pilot_configuration_INPUT.priors (sha16 bd5e1a56537cc842)'
json.dump(res,open(os.path.join(HERE,'prior_fraction_result.json'),'w'),indent=1); print(json.dumps(res,indent=1))
