"""Finite matrix checks of low-energy identities; no physical or local-mode fit."""
import ast
import hashlib
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run():
    plan=json.loads((ROOT/'PRE_REGISTRO_R71.json').read_text(encoding='utf-8'))
    for row in plan['sources']:
        assert digest(row['path'])==row['sha256']
    prior=json.loads(Path(plan['parameter_plan']).read_text(encoding='utf-8'))
    constants={}
    for n in ast.parse(Path(plan['alpha_source']).read_text(encoding='utf-8')).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            if n.targets[0].id in {'ALPHA_FINE_CODATA_2018','_SEALED_ALPHA_CODATA_2018'}:
                constants[n.targets[0].id]=ast.literal_eval(n.value)
    assert constants['ALPHA_FINE_CODATA_2018']==constants['_SEALED_ALPHA_CODATA_2018']
    beta=constants['ALPHA_FINE_CODATA_2018']*math.sqrt(math.e)
    p=prior['model']['parameters'];lam=beta*prior['model']['gamma_Lambda']
    d=plan['photon_dimension']; eye=np.eye(d); oh=np.eye(2)
    a=np.diag(np.sqrt(np.arange(1,d)),1).astype(complex)
    ai=np.kron(np.kron(a,eye),oh);ao=np.kron(np.kron(eye,a),oh)
    sm=np.kron(np.eye(d*d),np.array([[0,1],[0,0]],complex));sp=sm.conj().T
    z=np.kron(np.eye(d*d),np.diag([1.,-1.]));ne=sp@sm
    nfield=ai.conj().T@ai+ao.conj().T@ao
    vacuum=np.zeros(d*d*2,complex);vacuum[0]=1
    rho=np.outer(vacuum,vacuum.conj())
    rows=[];energy=[]
    for ri,ro in plan['squeezing_inputs']:
        bi=math.cosh(ri)*ai+math.sinh(ri)*ai.conj().T
        bo=math.cosh(ro)*ao+math.sinh(ro)*ao.conj().T
        j=bo.conj().T@sm+sp@bi
        h=p['omega_c']*(bi.conj().T@bi+bo.conj().T@bo)+p['omega_OH']*ne
        h+=p['g_JC']*(bi.conj().T@sm+sp@bi)+p['Omega']*(sm+sp)
        jumps=[math.sqrt(p['kappa_in'])*bi,math.sqrt(p['kappa_out'])*bo,
               math.sqrt(p['gamma_OH'])*sm,math.sqrt(p['gamma_dephasing'])*z,math.sqrt(lam)*j]
        dr=-1j*(h@rho-rho@h)
        for l in jumps:
            ld=l.conj().T
            dr+=l@rho@ld-(ld@l@rho+rho@ld@l)/2
        cost=(p['kappa_in']+lam)*math.sinh(ri)**2+p['kappa_out']*math.sinh(ro)**2
        rows.append({'ri':ri,'ro':ro,'predicted_cost':cost,
          'purity_derivative':float((2*np.trace(rho@dr)).real),
          'vacuum_survival_derivative':float(np.trace(rho@dr).real),
          'field_number_derivative':float(np.trace(nfield@dr).real),
          'imaginary_trace_residual':float(abs(np.trace(dr).imag))})
        for m in plan['energy_cuts']:
            indices=[((ni*d+no)*2+e) for ni in range(d) for no in range(d) for e in range(2) if ni+no+e<=m]
            for name,b,target,r in [('in',bi,ai,ri),('out',bo,ao,ro)]:
                observed=float(np.linalg.norm((b-target)[:,indices],2))
                bound=abs(math.cosh(r)-1)*math.sqrt(m)+abs(math.sinh(r))*math.sqrt(m+1)
                energy.append({'ri':ri,'ro':ro,'mode':name,'m':m,'observed':observed,'bound':bound})
    tol=plan['absolute_tolerance']
    checks=[
      {'name':'original_vacuum_cost_zero','passed':max(abs(rows[0][k]) for k in ['purity_derivative','vacuum_survival_derivative','field_number_derivative'])<=tol},
      {'name':'purity_and_survival_match_cost','passed':all(abs(r['purity_derivative']+2*r['predicted_cost'])<=tol and abs(r['vacuum_survival_derivative']+r['predicted_cost'])<=tol for r in rows)},
      {'name':'field_number_derivative_matches_cost','passed':all(abs(r['field_number_derivative']-r['predicted_cost'])<=tol for r in rows)},
      {'name':'nonzero_creation_control_detected','passed':all(r['predicted_cost']>plan['detection_floor'] and r['purity_derivative'] < -2*plan['detection_floor'] for r in rows[1:])},
      {'name':'finite_energy_norm_bounds','passed':all(r['observed']<=r['bound']+tol for r in energy)},
    ]
    return {'status':'SYNTHETIC_LOW_ENERGY_IDENTITIES','passed':all(x['passed'] for x in checks),'checks':checks,
       'beta_runtime':beta,'lambda_runtime':lam,'rows':rows,'energy_bounds':energy,
       'scope':'Synthetic squeezed mode pairs, not localized test functions or geometry of device; full five-jump algebra on vacuum/low-energy sectors; no ODE or physical measurement.'}

if __name__=='__main__':
    result=run();print(json.dumps(result,indent=2,allow_nan=False));raise SystemExit(0 if result['passed'] else 1)
