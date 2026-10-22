"""Diagnose changes across completed phase-integrated proposals, not acceptance."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
import argparse
import json
import numpy as np
import source_evidence as se
from audit_phase_source import load_run, direct_statistics


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("old_folder")
    parser.add_argument("new_folder")
    args=parser.parse_args()
    before=se.ROOT/args.old_folder
    after=se.ROOT/args.new_folder
    old,old_u,old_q,old_inside,old_ll,old_stats=load_run(before)
    new,new_u,new_q,new_inside,new_ll,new_stats=load_run(after)
    old_independent,_=direct_statistics(old_ll,old_q)
    new_independent,p=direct_statistics(new_ll,new_q)
    arithmetic=max(float(np.max(np.abs(new_stats[k]-new_independent[k]))) for k in new_stats)
    if arithmetic>1e-9:raise ValueError("New run direct sum differs")
    if old["family"]!=new["family"]:raise ValueError("Different recovery families")
    change=new_stats["lnB"]-old_stats["lnB"]
    combined=np.hypot(new_stats["lnB_MC_sd"],old_stats["lnB_MC_sd"])
    labels=se.load_state()["labels"]
    rows=[]
    for cell in [r["cell"] for r in new["rows"]]:
        indices=np.array([i for i,l in enumerate(labels) if all(l[k]==v for k,v in cell.items())])
        both=np.r_[indices,1200+indices]
        rows.append(dict(cell=cell,new_min_ESS=float(new_stats["ESS"][both].min()),
            new_median_ESS=float(np.median(new_stats["ESS"][both])),
            old_median_ESS=float(np.median(old_stats["ESS"][both])),
            change_lnB_mean=float(change[indices].mean()),max_abs_lnB_change=float(np.abs(change[indices]).max()),
            median_abs_lnB_change=float(np.median(np.abs(change[indices]))),
            draws_changing_more_than_point2=int(np.sum(np.abs(change[indices])>.2))))
    summary=dict(status="PROPOSAL_COMPARISON_NOT_SCIENTIFIC_ACCEPTANCE",rows=rows,
        old_draws=old["draws"],new_draws=new["draws"],old_passing=old["draws_passing_precision"],new_passing=new["draws_passing_precision"],
        old_ESS_quantiles=np.quantile(old_stats["ESS"],[0,.25,.5,.75,1]).tolist(),
        new_ESS_quantiles=np.quantile(new_stats["ESS"],[0,.25,.5,.75,1]).tolist(),
        old_median_ESS_per_draw=float(np.median(old_stats["ESS"])/old["draws"]),
        new_median_ESS_per_draw=float(np.median(new_stats["ESS"])/new["draws"]),
        max_abs_lnB_change=float(np.abs(change).max()),
        changes_over_point2=int(np.sum(np.abs(change)>.2)),
        naive_combined_MC_residual_quantiles=np.quantile(np.abs(change)/np.maximum(combined,1e-15),[0,.5,.9,1]).tolist(),
        independent_arithmetic_max_error=arithmetic,
        caveat="Low ESS can make delta-method MC error misleading. Agreement alone is insufficient; pilot data are training, not scientific acceptance. Draws were independent conditional on each frozen proposal.",
        physical_prior_changed=False,pooled_integral_created=False,scientific_acceptance=False,
        hashes={"old_result":se.sha(before/"RESULT.json"),"new_result":se.sha(after/"RESULT.json"),"source":se.sha(se.Path(__file__))})
    se.write(after/"PROPOSAL_COMPARISON.json",summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ("rows","hashes")}),flush=True)


if __name__=="__main__":main()
