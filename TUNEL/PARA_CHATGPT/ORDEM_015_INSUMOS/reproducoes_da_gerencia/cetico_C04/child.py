"""Isolated waveform child (auditor test, scratchpad only). Reads a job JSON, evaluates draws sequentially,
writes PRECALL before each native call so a crash is attributable. Never touches original dirs (read-only import)."""
import os
for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS"): os.environ[k]="1"
import sys, json, time, resource
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
job=json.load(open(sys.argv[1])); out=sys.argv[2]
B="/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN"
sys.path.insert(0,B+"/bis/e2_code")
import numpy as np, bilby
from pseob_source import pseob_frequency_domain
cfg=json.load(open(B+"/bis/e3_pilot_failure_diagnostic/PLAN_INPUTS.json"))["pilot_configuration_INPUT"]
grid=np.fft.rfftfreq(16*4096,1/4096)
kw=dict(minimum_frequency=20.,reference_frequency=20.,catch_waveform_errors=True,
        analysis_time_contract={'start_GPS':cfg['segment_start_GPS'],'duration_s':cfg['duration_s'],'roll_off_s':cfg['onsource_roll_off_s']})
with open(out,"a") as f:
    for item in job["items"]:
        p=item["parameters"]; f.write(json.dumps({"precall":item["label"],"fmax":item["fmax"]})+"\n"); f.flush(); os.fsync(f.fileno())
        t=time.perf_counter()
        try:
            w=pseob_frequency_domain(grid,**p,maximum_frequency=item["fmax"],**kw)
            st="DOMAIN_RETURNED_NONE" if w is None else "FINITE_WAVEFORM"
        except Exception as e:
            st="PYTHON_EXCEPTION:"+type(e).__name__+":"+str(e)[:80]
        f.write(json.dumps({"return":item["label"],"status":st,"wall_s":time.perf_counter()-t})+"\n"); f.flush(); os.fsync(f.fileno())
