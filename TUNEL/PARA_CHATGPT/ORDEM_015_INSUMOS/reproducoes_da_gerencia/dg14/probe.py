"""DG-14 refutation probe: replay prior to draw 24, run each draw at fmax 1024 in a subprocess, then a 2-D dtau grid."""
import os,sys,json,subprocess,time
for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"):os.environ[k]="1"
B="/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis"
DIAG=B+"/e3_pilot_failure_diagnostic"
OUT=os.path.dirname(os.path.abspath(__file__))+"/out"
sys.path.insert(0,B+"/e2_code")
import numpy as np
plan=json.load(open(DIAG+"/PLAN_INPUTS.json"))
cfg=plan["pilot_configuration_INPUT"]

def replay(n):
    import bilby
    from pe_runner import build_priors
    priors=build_priors(cfg)
    bilby.core.utils.random.seed(cfg['sampler']['seed']);np.random.seed(cfg['sampler']['seed'])
    keys=[k for k,p in priors.items() if isinstance(p,bilby.core.prior.Prior) and p.is_fixed is False]
    rows=[]
    for i in range(n):
        theta=priors.sample_subset_constrained_as_array(keys,size=1)[:,0]
        rows.append(dict(zip(keys,map(float,theta))))
    return rows

def child(params,fmax):
    import lal,lalsimulation as ls
    from pseob_source import pseob_frequency_domain
    grid=np.fft.rfftfreq(16*4096,1/4096)
    kw=dict(minimum_frequency=20.,maximum_frequency=fmax,reference_frequency=20.,
            analysis_time_contract={'start_GPS':cfg['segment_start_GPS'],'duration_s':cfg['duration_s'],'roll_off_s':cfg['onsource_roll_off_s']},
            catch_waveform_errors=True)
    p={k:v for k,v in params.items() if k not in ('ra','dec','psi')}
    try:
        w=pseob_frequency_domain(grid,**p,**kw)
        print("RESULT",json.dumps({"status":"NONE" if w is None else "FINITE"}))
    except Exception as e:
        print("RESULT",json.dumps({"status":"EXC","type":type(e).__name__,"msg":str(e)[:200]}))

def run(params,fmax,tag):
    cmd=[sys.executable,"-B",__file__,"--child",json.dumps(params),str(fmax)]
    t=time.perf_counter()
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
    dt=time.perf_counter()-t
    status=None
    for line in r.stdout.splitlines():
        if line.startswith("RESULT"):status=json.loads(line[6:])
    tail=[l for l in r.stderr.splitlines() if l.strip()][-2:]
    return {"tag":tag,"rc":r.returncode,"status":status,"wall":round(dt,2),"stderr_tail":tail}

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="--child":
        child(json.loads(sys.argv[2]),float(sys.argv[3]));sys.exit(0)
    mode=sys.argv[1]
    if mode=="replay":
        rows=replay(24)
        json.dump(rows,open(OUT+"/replay24.json","w"),indent=1)
        for i,r in enumerate(rows,1):
            print(i,round(r['mass_1'],3),round(r['mass_2'],3),round(r['dtau220'],4),round(r['dtau440'],4),round(r['domega220'],4),round(r['domega440'],4))
    elif mode=="draws":
        rows=json.load(open(OUT+"/replay24.json"))
        res=[]
        for i,r in enumerate(rows,1):
            x=run(r,1024,f"DRAW{i}_1024");x["dtau220"]=r['dtau220'];x["dtau440"]=r['dtau440'];x["m1"]=r['mass_1'];x["m2"]=r['mass_2']
            print(json.dumps(x),flush=True);res.append(x)
        json.dump(res,open(OUT+"/draws24_1024.json","w"),indent=1)
    elif mode=="grid":
        rows=json.load(open(OUT+"/replay24.json"))
        base=dict(rows[int(sys.argv[2])-1])  # 1-based draw as base point
        fmax=float(sys.argv[3])
        d220=[-0.8,-0.6,-0.3,0.0,0.5,1.0,2.0];d440=[-0.8,-0.5,0.0,0.5,1.0,2.0,3.0,4.0]
        res=[]
        for a in d220:
            for b in d440:
                p=dict(base);p['dtau220']=a;p['dtau440']=b
                x=run(p,fmax,f"g_{a}_{b}");x["dtau220"]=a;x["dtau440"]=b
                print(json.dumps(x),flush=True);res.append(x)
        json.dump(res,open(OUT+f"/grid_draw{sys.argv[2]}_fmax{int(fmax)}.json","w"),indent=1)
