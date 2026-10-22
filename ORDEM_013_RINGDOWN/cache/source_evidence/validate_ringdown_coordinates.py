"""Check prior transport, its independent Jacobian and conditional integrals."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
from datetime import datetime,timezone
import json
import numpy as np
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
import source_evidence as se
import phase_marginal_source as pm
import ringdown_source_coordinates as rc
from audit_phase_source import load_run,direct_statistics


def conditional_prior(family,uq,us2):
    q,s2=1+2*uq,-.4+.8*us2
    def lr(s1):return rc.spectral(rc.remnant_at_unit_mass(family,q,s1,s2)[1])[1]
    low,high=lr(-.4),lr(.4)
    totals=[]
    for order in (16,32):
        nr,wr=leggauss(order)
        nm,wm=leggauss(12)
        answer=np.zeros(5)
        bare=0.
        for n,w in zip(nr,wr):
            r=(low+high)/2+n*(high-low)/2
            s1=brentq(lambda s:lr(s)-r,-.4,.4,xtol=1e-13,rtol=1e-14)
            fraction,spin=rc.remnant_at_unit_mass(family,q,s1,s2)
            mode,_,_=rc.spectral(spin)
            ylo=np.log(mode.real/(2*np.pi*rc.TSUN*fraction*110*rc.FREF))
            yhi=np.log(mode.real/(2*np.pi*rc.TSUN*fraction*50*rc.FREF))
            for m,v in zip(nm,wm):
                y0=(ylo+yhi)/2+m*(yhi-ylo)/2
                y=np.array([y0,r-rc.LOG_RATIO_REFERENCE-y0,uq,us2,.5,.5])
                inverse=rc.inverse(family,y)
                if inverse is None:raise ValueError("Physical conditional-domain point rejected")
                u,jac=inverse
                weight=w*v*(high-low)*(yhi-ylo)/4
                answer+=weight/jac*np.array([1.,u[0],u[2],u[0]*u[2],u[0]**2*u[2]**2])
                bare+=weight
        totals.append(answer)
    expected=np.array([1.,.5,.5,.25,1/9])
    error=float(np.max(np.abs(totals[-1]-expected)))
    convergence=float(np.max(np.abs(totals[-1]-totals[0])))
    if error>1e-8 or convergence>1e-8:raise ValueError("Transport changed conditional physical prior")
    return dict(family=family,q=q,s2=s2,integrals=totals[-1].tolist(),expected=expected.tolist(),
                error=error,quadrature_change=convergence,normalization_if_Jacobian_omitted=bare)


def main():
    pm.check()
    destination=se.ROOT/"RINGDOWN_COORDINATES_VALIDATION.json"
    if destination.exists():raise FileExistsError("Create-once coordinate validation")
    rng=np.random.default_rng(130830)
    point_checks=[]
    for family in se.FAMILIES:
        for i in range(256):
            u=rng.uniform(.01,.99,6)
            y,jac=rc.forward(family,u)
            reverse=rc.inverse(family,y)
            if reverse is None:raise ValueError("Valid source has no inverse")
            reconstructed,jac2=reverse
            roundtrip=float(np.max(np.abs(reconstructed-u)))
            matrix=np.empty((6,6))
            for j in range(6):
                delta=np.zeros(6);delta[j]=1e-5
                matrix[:,j]=(rc.forward(family,u+delta)[0]-rc.forward(family,u-delta)[0])/2e-5
            numerical=abs(np.linalg.det(matrix))
            jacobian_error=abs(numerical/jac-1)
            mass,q,s1,s2=50+60*u[0],1+2*u[1],-.4+.8*u[2],-.4+.8*u[3]
            mf,spin=se.model.remnant(family,mass*q/(1+q),mass/(1+q),s1,s2)
            fraction,chi=rc.remnant_at_unit_mass(family,q,s1,s2)
            scale_error=max(abs(mf/mass-fraction),abs(spin-chi))
            if roundtrip>1e-10 or jacobian_error>1e-6 or scale_error>1e-12:
                raise ValueError("Source coordinate/Jacobian/remnant scaling failed")
            point_checks.append(dict(family=family,roundtrip_error=roundtrip,Jacobian_relative_error=jacobian_error,
                                     remnant_scaling_error=scale_error,Jacobian=jac))
    # This is a numerical monotonicity audit over the full prior grid, not a
    # formal proof of the fit. Inference must keep pointwise Jacobian checks.
    slopes=[]
    for family in se.FAMILIES:
        for q in np.linspace(1,3,17):
            for s2 in np.linspace(-.4,.4,9):
                for s1 in np.linspace(-.4,.4,17):
                    _,spin=rc.remnant_at_unit_mass(family,q,s1,s2)
                    slopes.append(rc.spin_derivative(family,q,s1,s2)*rc.spectral(spin)[2])
    integrals=[conditional_prior(f,q,s2) for f in se.FAMILIES for q in (0.,.5,1.) for s2 in (0.,.5,1.)]
    report=dict(status="PASS_NUMERICAL_PRIOR_TRANSPORT",date_utc=datetime.now(timezone.utc).isoformat(),
        coordinates="log(f220/250Hz),log(tau220/.004s),u_q,u_spin2,u_cosi,u_t0; full source retained",
        analytic_absolute_Jacobian="48/M_total * (dchi_final/dspin1z) * dlog(omega_R/abs(omega_I))/dchi_final",
        original_prior_changed=False,physical_clock_selected=False,source_parameters_fixed=False,
        point_checks=point_checks,monotonicity_grid_points=len(slopes),minimum_quality_slope_wrt_spin1=float(min(slopes)),
        conditional_prior_integrals=integrals,scientific_acceptance=False,
        numerical_scope="Round-trip and independent finite-difference determinant, conditional moments and numerical monotonicity grid; no formal global theorem or forecast convergence claim",
        hashes={p.name:se.sha(p) for p in (se.Path(__file__),se.ROOT/"ringdown_source_coordinates.py",se.ROOT/"QNM_GRID.json",se.ROOT/"coherent_imr_model.py",pm.REG)})
    se.write(destination,report)
    print(json.dumps(dict(status=report["status"],roundtrips=len(point_checks),
        max_roundtrip_error=max(c["roundtrip_error"] for c in point_checks),
        max_Jacobian_relative_error=max(c["Jacobian_relative_error"] for c in point_checks),
        max_conditional_integral_error=max(c["error"] for c in integrals),monotonicity_points=len(slopes),
        minimum_quality_slope=float(min(slopes)))),flush=True)


if __name__=="__main__":main()
