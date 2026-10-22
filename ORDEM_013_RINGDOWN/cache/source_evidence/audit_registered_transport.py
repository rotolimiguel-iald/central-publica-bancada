"""Independent proposal-density and source-prior transport audit of a run."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
import argparse
import json
import numpy as np
from scipy.stats import multivariate_t
import source_evidence as se
import ringdown_source_coordinates as rc
import transport_phase_source as tp
from audit_phase_source import load_run,direct_statistics


def main():
    parser=argparse.ArgumentParser();parser.add_argument("run_name");parser.add_argument("--stage",default="phase_ringdown_transport");args=parser.parse_args()
    stage=(se.ROOT/args.stage).resolve()
    if stage.parent!=se.ROOT.resolve():raise ValueError("Expected direct task stage directory")
    tp.STAGE=stage
    proposal=tp.check();folder=tp.STAGE/args.run_name
    result,u,logq,inside,values,stats=load_run(folder)
    if result["transport_registration_sha256"]!=se.sha(tp.STAGE/"REGISTRATION.json"):
        raise ValueError("Transport run points to another registration")
    independent,weights=direct_statistics(values,logq)
    arithmetic=max(float(np.max(np.abs(independent[k]-stats[k]))) for k in independent)
    with np.load(folder/"PROPOSALS.npz") as f:
        y=f["transport_y"].copy();jac=f["forward_Jacobian"].copy();q_y=f["logq_y"].copy();cemetery=f["cemetery"].copy()
    if not np.array_equal(cemetery,~inside):raise ValueError("Invalid cemetery mask")
    densities=np.zeros(len(y))
    for c in proposal["components"]:
        # Direct density sum is independent of production logsumexp assembly.
        densities+=c["weight"]*multivariate_t.pdf(y,loc=c["mean"],shape=c["shape"],df=proposal["df"])
    direct_y=densities.copy();direct_y[inside]+=proposal["defensive_weight"]/jac[inside]
    direct_u=densities[inside]*jac[inside]+proposal["defensive_weight"]
    density_error=max(float(np.max(np.abs(np.log(direct_y)-q_y))),float(np.max(np.abs(np.log(direct_u)-logq[inside]))))
    inverse_error=0.;forward_error=0.
    for i in range(len(y)):
        inverse=rc.inverse(proposal["family"],y[i])
        if (inverse is not None)!=bool(inside[i]):raise ValueError("Transport support flag differs")
        if inside[i]:
            reconstructed,jac2=inverse
            inverse_error=max(inverse_error,float(np.max(np.abs(reconstructed-u[i]))))
            got,j=rc.forward(proposal["family"],u[i])
            forward_error=max(forward_error,float(np.max(np.abs(got-y[i]))),abs(j/jac[i]-1))
        elif not np.all(u[i]==2.):raise ValueError("Outside point was disguised as physical coordinates")
    selected=np.unique(np.argmax(weights,axis=0));checks=[]
    for index in selected:
        v=u[index];distance=min(v.min(),(1-v).min());step=min(1e-5,distance/4)
        if step<=1e-10:raise ValueError("Dominant point too close to boundary for finite-difference audit")
        matrix=np.empty((6,6))
        for j in range(6):
            delta=np.zeros(6);delta[j]=step
            matrix[:,j]=(rc.forward(proposal["family"],v+delta)[0]-rc.forward(proposal["family"],v-delta)[0])/(2*step)
        relative=abs(abs(np.linalg.det(matrix))/jac[index]-1)
        checks.append(dict(index=int(index),relative_Jacobian_error=float(relative)))
    if arithmetic>1e-9 or density_error>1e-9 or inverse_error>1e-10 or forward_error>1e-10 or max(c["relative_Jacobian_error"] for c in checks)>1e-6:
        raise ValueError("Independent source transport audit differs")
    out=dict(status="PASS_TRANSPORT_DENSITY_NOT_PRECISION",draws=len(u),inside=int(inside.sum()),outside=int(cemetery.sum()),
        direct_density_log_error=density_error,forward_error=forward_error,inverse_error=inverse_error,
        direct_integral_arithmetic_error=arithmetic,Jacobian_checks=checks,
        max_independent_Jacobian_relative_error=max(c["relative_Jacobian_error"] for c in checks),
        draws_passing_precision=result["draws_passing_precision"],scientific_acceptance=False,
        scope=f"All{len(u)} proposals and omitted-support mass checked; numerical source evidence still needs convergence and rate/coverage controls",
        hashes={"RESULT.json":se.sha(folder/"RESULT.json"),"source":se.sha(se.Path(__file__))})
    se.write(folder/"DENSITY_AUDIT.json",out)
    print(json.dumps({k:v for k,v in out.items() if k not in ("Jacobian_checks","hashes")}),flush=True)


if __name__=="__main__":main()
