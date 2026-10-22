"""Full-support importance proposal in ringdown coordinates, same likelihood/prior."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
import argparse
from datetime import datetime,timezone
import json
import multiprocessing as mp
import time
import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_t
import source_evidence as se
import phase_marginal_source as pm
import ringdown_source_coordinates as rc
from audit_phase_source import load_run,direct_statistics
from adapt_phase_source import weighted_fit
from importance_source_evidence import importance_statistics

STAGE=se.ROOT/"phase_ringdown_transport"


def fit():
    validation=json.loads((se.ROOT/"RINGDOWN_COORDINATES_VALIDATION.json").read_bytes())
    if validation["status"]!="PASS_NUMERICAL_PRIOR_TRANSPORT":raise ValueError("Unvalidated prior transport")
    folder=se.ROOT/"phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048"
    result,u,logq,inside,values,stats=load_run(folder)
    independent,p=direct_statistics(values,logq)
    weights=p.mean(axis=1)[inside]
    transformed=np.array([rc.forward(result["family"],v)[0] for v in u[inside]])
    components,history=weighted_fit(transformed,weights,count=12,floor=1e-4,seed=130840)
    for c in components:c["weight"]*=.9/.7
    proposal=dict(components=components,defensive_weight=.1,df=5.,family=result["family"],history=history,
        physical_prior_changed=False,training_accepted_as_science=False,
        coordinates="log f220 and log tau220 plus q,spin2,cosi,time; all seven original source parameters still integrated")
    STAGE.mkdir(exist_ok=False)
    se.write(STAGE/"PROPOSAL.json",proposal)
    names=["ringdown_source_coordinates.py","validate_ringdown_coordinates.py","RINGDOWN_COORDINATES_VALIDATION.json",
        "transport_phase_source.py","adapt_phase_source.py","phase_marginal_source.py","phase_ringdown_transport/PROPOSAL.json",
        "phase_runs/REGISTRATION.json","phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/RESULT.json"]
    reg=dict(status="REGISTERED_COORDINATE_TRANSPORT_ONLY",date_utc=datetime.now(timezone.utc).isoformat(),
        physical_prior_changed=False,likelihood_changed=False,physical_clock_selected=False,C6_changed=False,
        full_prior_component=.1,independent_new_draws_required=True,
        failed_inverse="Zero integrand, counted in total draws; keep original proposed transport point and cemetery marker",
        acceptance="Original component ESS100,maxweight.05,MCsdlnB.2,independent repeats and rate/calibration controls",
        hashes={n:se.sha(se.ROOT/n) for n in names})
    se.write(STAGE/"REGISTRATION.json",reg)
    print(json.dumps(dict(status=reg["status"],components=len(components))),flush=True)


def check():
    pm.check()
    reg=json.loads((STAGE/"REGISTRATION.json").read_bytes())
    for name,expected in reg["hashes"].items():
        if se.sha(se.ROOT/name)!=expected:raise ValueError("Transport registration changed: "+name)
    return json.loads((STAGE/"PROPOSAL.json").read_bytes())


def draw(proposal,count,seed):
    rng=np.random.default_rng(seed)
    weights=[proposal["defensive_weight"]]+[c["weight"] for c in proposal["components"]]
    if abs(sum(weights)-1)>1e-12:raise ValueError("Proposal mass differs from1")
    groups=rng.choice(len(weights),count,p=weights)
    y=np.empty((count,6));u=np.full((count,6),2.)
    # u=2 is an explicit cemetery marker, NOT a proposed physical source.
    jac=np.full(count,np.nan);inside=np.zeros(count,dtype=bool)
    for k in range(len(weights)):
        ids=np.flatnonzero(groups==k)
        if k==0:
            for i in ids:
                u[i]=rng.uniform(size=6)
                y[i],jac[i]=rc.forward(proposal["family"],u[i]);inside[i]=True
        elif len(ids):
            c=proposal["components"][k-1]
            v=rng.normal(size=(len(ids),6))@np.linalg.cholesky(c["shape"]).T
            v/=np.sqrt(rng.chisquare(proposal["df"],len(ids))/proposal["df"])[:,None]
            y[ids]=v+np.array(c["mean"])
            for i in ids:
                inverse=rc.inverse(proposal["family"],y[i])
                if inverse is not None:u[i],jac[i]=inverse;inside[i]=True
    logprior_y=np.full(count,-np.inf)
    logprior_y[inside]=-np.log(jac[inside])
    terms=[np.log(proposal["defensive_weight"])+logprior_y]
    for c in proposal["components"]:
        terms.append(np.log(c["weight"])+multivariate_t.logpdf(y,loc=c["mean"],shape=c["shape"],df=proposal["df"]))
    logq_y=logsumexp(np.column_stack(terms),axis=1)
    logq_u=logq_y.copy()
    logq_u[inside]+=np.log(jac[inside])
    if np.any(~np.isfinite(logq_u)):raise ValueError("Invalid proposal density")
    return dict(unit_cube=u,logq=logq_u,inside=inside,transport_y=y,forward_Jacobian=jac,
                logq_y=logq_y,proposal_component=groups,cemetery=~inside)


def oracle():
    proposal=check()
    samples=draw(proposal,32768,130850)
    good=samples["inside"]
    w=np.zeros(len(good));w[good]=np.exp(-samples["logq"][good])
    u=samples["unit_cube"]
    quantities=np.column_stack([w]+[w*u[:,i] for i in range(6)]+[w*u[:,i]**2 for i in range(6)])
    expected=np.array([1.]+[.5]*6+[1/3]*6)
    mean=quantities.mean(axis=0);sd=quantities.std(axis=0,ddof=1)/np.sqrt(len(w))
    z=np.abs(mean-expected)/sd
    result=dict(status="PASS_TRANSPORT_PROPOSAL_MOMENTS" if np.max(z)<5 else "PROPOSAL_MOMENTS_FAILED",
        N=len(w),seed=130850,inside=int(good.sum()),mean=mean.tolist(),expected=expected.tolist(),
        MC_standard_errors=sd.tolist(),standardized_errors=z.tolist(),max_standardized_error=float(z.max()),
        maximum_prior_weight=float(w.max()),physical_prior_changed=False,
        scope="Independent Monte Carlo normalization and13 uniform-prior moments, not astrophysical evidence",
        registration_sha256=se.sha(STAGE/"REGISTRATION.json"))
    se.write(STAGE/"PROPOSAL_ORACLE.json",result)
    print(json.dumps(result),flush=True)
    if result["status"]!="PASS_TRANSPORT_PROPOSAL_MOMENTS":raise ValueError("Proposal transport moment check failed")


def run(args):
    proposal=check()
    oracle_result=json.loads((STAGE/"PROPOSAL_ORACLE.json").read_bytes())
    if oracle_result["status"]!="PASS_TRANSPORT_PROPOSAL_MOMENTS":raise ValueError("Unvalidated proposal")
    folder=STAGE/f"{proposal['family']}_seed{args.seed}_N{args.draws}"
    folder.mkdir(exist_ok=False)
    samples=draw(proposal,args.draws,args.seed)
    se.save_arrays(folder/"PROPOSALS.npz",**samples)
    se.write(folder/"START.json",dict(date_utc=datetime.now(timezone.utc).isoformat(),family=proposal["family"],seed=args.seed,
        draws=args.draws,transport_registration_sha256=se.sha(STAGE/"REGISTRATION.json"),physical_prior_changed=False,
        phase_registration_sha256=se.sha(pm.REG),proposal_sha256=se.sha(STAGE/"PROPOSAL.json")))
    values=np.full((args.draws,2400),-np.inf)
    jobs=[(int(i),samples["unit_cube"][i]) for i in np.flatnonzero(samples["inside"])]
    metadata=[];chunk=[];done=0;number=0;start=time.monotonic()
    with mp.get_context("fork").Pool(args.processes,initializer=se.initialize,initargs=(proposal["family"],)) as pool:
        for index,value,meta in pool.imap_unordered(pm.evaluate,jobs,chunksize=1):
            values[index]=value;chunk.append((index,value));metadata.append(dict(index=index,**meta));done+=1
            if len(chunk)==16 or done==len(jobs):
                se.save_arrays(folder/f"chunk_{number:05d}.npz",indices=np.array([c[0] for c in chunk]),components=np.stack([c[1] for c in chunk]))
                chunk=[];number+=1
                progress=dict(done=done,valid_draws=len(jobs),seconds=time.monotonic()-start,date_utc=datetime.now(timezone.utc).isoformat())
                se.write(folder/"PROGRESS.json",progress,replace=True);print(json.dumps(progress),flush=True)
    stats=importance_statistics(values,samples["logq"])
    se.save_arrays(folder/"RESULT_ARRAYS.npz",**stats)
    passing=(np.minimum(stats["ESS"][:1200],stats["ESS"][1200:])>=100)&(np.maximum(stats["max_weight"][:1200],stats["max_weight"][1200:])<=.05)&(stats["lnB_MC_sd"]<=.2)
    labels=se.load_state()["labels"];rows=[]
    for label in labels:
        cell={k:label[k] for k in ("psd","source","injection_family","injection_a","snr")}
        if any(r["cell"]==cell for r in rows):continue
        ids=np.array([i for i,l in enumerate(labels) if all(l[k]==v for k,v in cell.items())]);both=np.r_[ids,1200+ids]
        v=stats["lnB"][ids]
        rows.append(dict(cell=cell,N=len(ids),lnB_mean=float(v.mean()),lnB_sd_noise=float(v.std(ddof=1)),
            lnB_quantiles=np.quantile(v,[.05,.5,.95]).tolist(),min_component_ESS=float(stats["ESS"][both].min()),
            max_weight=float(stats["max_weight"][both].max()),max_lnB_MC_sd=float(stats["lnB_MC_sd"][ids].max()),draws_passing_precision=int(passing[ids].sum())))
    report=dict(status="RINGDOWN_COORDINATE_PILOT_NOT_ACCEPTED",family=proposal["family"],seed=args.seed,draws=args.draws,
        evaluations=done,rows=rows,integration_controls=metadata,all_precision_pass=bool(passing.all()),
        draws_passing_precision=int(passing.sum()),ESS_range=[float(stats["ESS"].min()),float(stats["ESS"].max())],
        registration_sha256=se.sha(pm.REG),transport_registration_sha256=se.sha(STAGE/"REGISTRATION.json"),
        source_parameters_integrated=7,source_parameters_sampled=6,physical_prior_changed=False,original_C6_changed=False,
        independent_repeat=False,scientific_acceptance=False,
        hashes={p.name:se.sha(p) for p in folder.glob("*.npz")})
    se.write(folder/"RESULT.json",report)
    print(json.dumps({k:report[k] for k in ("status","draws","evaluations","draws_passing_precision","ESS_range")}),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("command",choices=["fit","oracle","run"])
    parser.add_argument("--seed",type=int,default=130841);parser.add_argument("--draws",type=int,default=2048);parser.add_argument("--processes",type=int,default=6)
    args=parser.parse_args()
    if args.command=="fit":fit()
    elif args.command=="oracle":oracle()
    else:run(args)
