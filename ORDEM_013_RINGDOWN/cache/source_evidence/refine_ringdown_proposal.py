"""Fit fewer proposal components to a completed transported pilot.

Numerical hypothesis: a sparse pilot can overfit a12-component six-dimensional
mixture. A three-component proposal tests that possibility with fresh draws.
No physical parameter or prior is removed, fixed, or narrowed.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
from datetime import datetime,timezone
import argparse
import json
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import transport_phase_source as tp
from adapt_phase_source import weighted_fit
from audit_phase_source import load_run,direct_statistics

STAGE=se.ROOT/"phase_ringdown_regularized"


def fit():
    tp.check()
    folder=tp.STAGE/"IMRPhenomXPHM_seed130841_N2048"
    result,u,logq,inside,values,stats=load_run(folder)
    density=json.loads((folder/"DENSITY_AUDIT.json").read_bytes())
    rate=json.loads((folder/"AUDIT_RATE.json").read_bytes())
    if density["status"]!="PASS_TRANSPORT_DENSITY_NOT_PRECISION" or not rate["rate_control_pass"]:
        raise ValueError("Completed pilot has not passed its numerical audit")
    independent,p=direct_statistics(values,logq)
    with np.load(folder/"PROPOSALS.npz") as f:y=f["transport_y"].copy()
    weights=p.mean(axis=1)
    components,history=weighted_fit(y[inside],weights[inside],count=3,floor=1e-4,seed=130860)
    for c in components:c["weight"]*=.9/.7
    proposal=dict(components=components,defensive_weight=.1,df=5.,family=result["family"],history=history,
        physical_prior_changed=False,training_accepted_as_science=False,
        computational_change="Three fitted6D Student-t components instead of12;10% original-prior component retained",
        training_pooled_ESS=float(1/np.sum(weights**2)),training_result_sha256=se.sha(folder/"RESULT.json"))
    STAGE.mkdir(exist_ok=False)
    se.write(STAGE/"PROPOSAL.json",proposal)
    paths=[se.Path(__file__),se.ROOT/"transport_phase_source.py",se.ROOT/"ringdown_source_coordinates.py",se.ROOT/"adapt_phase_source.py",
        pm.REG,folder/"RESULT.json",folder/"DENSITY_AUDIT.json",folder/"AUDIT_RATE.json",STAGE/"PROPOSAL.json"]
    reg=dict(status="REGISTERED_REGULARIZED_NUMERICAL_PROPOSAL",date_utc=datetime.now(timezone.utc).isoformat(),
        components=3,source_parameters_integrated=7,physical_prior_changed=False,likelihood_changed=False,
        inference_draws=8192,inference_seed=130861,scientific_acceptance=False,C6_changed=False,
        hypothesis="Sparse training may overfit12 mixture components; fewer proposal components may improve sampling. This is to be measured, not asserted as solved.",
        acceptance="Unchanged ESS100,maxweight.05,MCsdlnB.2,repeat and waveform-rate/calibration controls",
        hashes={str(p.relative_to(se.ROOT)):se.sha(p) for p in paths})
    se.write(STAGE/"REGISTRATION.json",reg)
    print(json.dumps(dict(status=reg["status"],components=3,training_pooled_ESS=proposal["training_pooled_ESS"])),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("command",choices=["fit","oracle","run"])
    parser.add_argument("--draws",type=int,default=8192);parser.add_argument("--seed",type=int,default=130861);parser.add_argument("--processes",type=int,default=6)
    args=parser.parse_args()
    if args.command=="fit":fit()
    else:
        tp.STAGE=STAGE
        if args.command=="oracle":tp.oracle()
        else:tp.run(args)
