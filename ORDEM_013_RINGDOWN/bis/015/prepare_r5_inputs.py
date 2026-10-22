"""Freeze source-only R5 inputs before native evaluation, using the amended runner."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,copy
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN');D=B/'bis/015/t03/R5';ROOT=B.parent
sys.path.insert(0,str(B/'bis/e2_code_v1_1'))
import bilby,numpy as np
from pe_runner import build_priors
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
def main():
    D.mkdir(exist_ok=False);(D/'c04_originals').mkdir()
    inputs=ROOT/'TUNEL/PARA_CHATGPT/ORDEM_015_INSUMOS/reproducoes_da_gerencia/cetico_C04'
    provenance=[]
    for name in ['supervise.py','child.py','make_items.py','replay.py','draws400.json']:
        p=inputs/name;out=D/'c04_originals'/name;raw=p.read_bytes()
        with out.open('xb') as f:f.write(raw)
        assert out.read_bytes()==raw;provenance.append(dict(path=str(p),sha256=sha(p)))
    cfg=copy.deepcopy(json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes())['pe_jobs']['GW250114_PILOT'])
    cfg.update(label='GW250114_PILOT_V2_S220',generation_sample_rate_hz=4096,generation_maximum_frequency_hz=2048,
      variant='registered_fixed_deformation_variant',fixed_deformation_parameters=dict(dtau440=0.,domega440=0.))
    cfg['priors'].update(dtau440=0.,domega440=0.);cfg['sampler']['seed']=15260302
    priors=build_priors(cfg);qualification_seed=15260301
    bilby.core.utils.random.seed(qualification_seed);np.random.seed(qualification_seed)
    keys=[k for k,p in priors.items() if isinstance(p,bilby.core.prior.Prior) and p.is_fixed is False]
    source_keys=('mass_1','mass_2','chi_1','chi_2','luminosity_distance','theta_jn','phase','geocent_time','dtau220','dtau440','domega220','domega440')
    items=[]
    for n in range(1000):
        theta=priors.sample_subset_constrained_as_array(keys,size=1)[:,0]
        params=dict(zip(keys,map(float,theta)));params.update(cfg['fixed_deformation_parameters'])
        assert .125<params['mass_2']/params['mass_1']<1
        items.append(dict(label=f's220_draw_{n+1:04d}',origin='amended_build_priors',parameters={k:params[k] for k in source_keys}))
    historical=json.loads((D/'c04_originals/draws400.json').read_bytes())['draws']
    for number in (8,16,20):
        p=dict(historical[number-1]['parameters']);p.update(dtau440=0.,domega440=0.)
        items.append(dict(label=f'required_V1_draw_{number}_440_fixed',origin='authorized_C04_input_draws400',parameters={k:p[k] for k in source_keys}))
    mid=(cfg['priors']['geocent_time']['minimum']+cfg['priors']['geocent_time']['maximum'])/2
    for m1,m2 in [(15.,10.),(79.9,10.),(100.,99.9)]:
        for chi in [-.99,.99]:
            for dtau in [-.8,2.]:
                p=dict(mass_1=m1,mass_2=m2,chi_1=chi,chi_2=chi,luminosity_distance=500.,theta_jn=1.,phase=0.,geocent_time=mid,dtau220=dtau,dtau440=0.,domega220=0.,domega440=0.)
                assert .125<m2/m1<1
                items.append(dict(label=f'corner_m{m1}_{m2}_chi{chi}_dtau{dtau}',origin='R5_exact_prior_corners',mass_ratio=m2/m1,parameters=p))
    put(D/'CONFIG_2048_INPUT.json',cfg)
    cfg2=copy.deepcopy(cfg);cfg2.update(generation_sample_rate_hz=8192,generation_maximum_frequency_hz=4096);build_priors(cfg2)
    put(D/'CONFIG_4096_RESERVED_INPUT.json',cfg2);put(D/'ITEMS.json',items)
    m=dict(at=datetime.now(timezone.utc).isoformat(),status='R5_INPUTS_FROZEN_NOT_EVALUATED',qualification_seed=qualification_seed,pilot_seed_INPUT=cfg['sampler']['seed'],
      random_draws=1000,required_historical=3,prior_corners=12,total=len(items),box='a:440 fixed GR',
      on_2048_EDOM='Run exactly same frozen items at4096/8192; never reject physical prior by EDOM',
      inputs={p.name:sha(p) for p in D.glob('*.json')},source_tree={p.name:sha(p) for p in (B/'bis/e2_code_v1_1').glob('*.py')},C04_sources=provenance,
      reads_strain=False,reads_blind_seed=False,launches_PE=False,heavy_machine_hours=0)
    put(D/'INPUT_MANIFEST.json',m);print(json.dumps({k:m[k] for k in ['status','random_draws','required_historical','prior_corners','total']}))
if __name__=='__main__':main()
