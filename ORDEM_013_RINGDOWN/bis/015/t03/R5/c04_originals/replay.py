"""Replay bilby prior draws with the pilot seed (same method as the bench's diagnostic_child --replay), N draws."""
import os,sys,json
for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"): os.environ[k]="1"
B="/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN"
sys.path.insert(0,B+"/bis/e2_code")
import numpy as np, bilby
from pe_runner import build_priors
cfg=json.load(open(B+"/bis/e3_pilot_failure_diagnostic/PLAN_INPUTS.json"))["pilot_configuration_INPUT"]
N=int(sys.argv[1]); priors=build_priors(cfg)
bilby.core.utils.random.seed(cfg['sampler']['seed']); np.random.seed(cfg['sampler']['seed'])
keys=[k for k,p in priors.items() if isinstance(p,bilby.core.prior.Prior) and p.is_fixed is False]
rows=[]
for n in range(N):
    theta=priors.sample_subset_constrained_as_array(keys,size=1)[:,0]
    rows.append({"draw":n+1,"parameters":dict(zip(keys,map(float,theta)))})
ref=json.load(open(B+"/bis/e3_pilot_failure_diagnostic/PRIOR_REPLAY.json"))["draws"]
match=all(abs(rows[i]["parameters"][k]-ref[i]["parameters"][k])<1e-12 for i in range(8) for k in ref[i]["parameters"])
json.dump({"first8_match_bench_replay":match,"seed":cfg['sampler']['seed'],"keys":keys,"draws":rows},open(sys.argv[2],"w"),indent=1)
print("first8_match",match,"N",N)
