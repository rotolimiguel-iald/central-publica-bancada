"""Preregistered reduced device integration. Only synthetic 8-dimensional states."""
from __future__ import annotations
import ast
import datetime
import hashlib
import itertools
import json
import math
import platform
from pathlib import Path
import sys
import time
import numpy as np
import scipy
from scipy.linalg import expm

BASE = Path(__file__).resolve().parent

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_new(path, obj):
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")
def residual(a): return float(np.linalg.norm(a, ord="fro"))
def vec(a): return a.reshape(-1, order="F")
def unvec(a, d): return a.reshape((d, d), order="F")
def projector(x): return np.outer(x, x.conj())
def check(name, metric, bound):
    return {"name": name, "value": float(metric), "bound": float(bound),
            "passed": bool(math.isfinite(float(metric)) and metric <= bound)}

def rate(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Rate must be a finite real non-boolean number")
    if not math.isfinite(value) or value < 0:
        raise ValueError("Rate must be finite and nonnegative")
    return float(value)

def validate_density(rho, tol):
    if not np.isfinite(rho).all(): raise ValueError("Nonfinite density")
    if residual(rho-rho.conj().T) > tol: raise ValueError("Density not Hermitian")
    if abs(np.trace(rho)-1) > tol: raise ValueError("Density not normalized")
    m = float(np.linalg.eigvalsh(rho).min())
    if m < -tol: raise ValueError(f"Density not positive semidefinite: {m}")
    return m

def embed(a, region, dims):
    """Actual local matrix algebra embedding, identity on complementary factors."""
    region = tuple(region)
    local_dims = tuple(dims[i] for i in region)
    ld = math.prod(local_dims)
    if a.shape != (ld, ld): raise ValueError("Local operator dimension mismatch")
    n = math.prod(dims)
    tuples = list(itertools.product(*[range(d) for d in dims]))
    out = np.zeros((n,n), complex)
    for i, ii in enumerate(tuples):
        li = int(np.ravel_multi_index(tuple(ii[k] for k in region), local_dims)) if region else 0
        for j, jj in enumerate(tuples):
            if all(ii[k] == jj[k] for k in range(len(dims)) if k not in region):
                lj = int(np.ravel_multi_index(tuple(jj[k] for k in region), local_dims)) if region else 0
                out[i,j] = a[li,lj]
    return out

def units(d):
    return {(i,j): np.eye(d, dtype=complex)[:,i,None] @ np.eye(d, dtype=complex)[None,j,:]
            for i in range(d) for j in range(d)}

def algebra_measurements(dims):
    regions = [tuple(i for i in range(len(dims)) if mask & (1<<i)) for mask in range(1<<len(dims))]
    local = {r: units(math.prod(dims[i] for i in r)) for r in regions}
    embedded = {r: {ij: embed(e,r,dims) for ij,e in local[r].items()} for r in regions}
    errors = {"unit": 0., "star": 0., "multiplication": 0., "isotony": 0., "disjoint_commutator": 0.}
    counts = {k: 0 for k in errors}
    zero = np.zeros((math.prod(dims),)*2, complex)
    for r in regions:
        local_dimension = math.prod(dims[i] for i in r)
        errors["unit"] = max(errors["unit"], residual(embed(np.eye(local_dimension),r,dims)-np.eye(math.prod(dims))))
        counts["unit"] += 1
        for (i,j),a in embedded[r].items():
            errors["star"] = max(errors["star"], residual(a.conj().T-embedded[r][j,i]))
            counts["star"] += 1
            for (k,l),b in embedded[r].items():
                target = embedded[r][i,l] if j == k else zero
                errors["multiplication"] = max(errors["multiplication"],residual(a@b-target))
                counts["multiplication"] += 1
        for s in regions:
            if set(r).issubset(s):
                inside_s = tuple(s.index(i) for i in r)
                for ij, a in local[r].items():
                    nested = embed(embed(a,inside_s,tuple(dims[i] for i in s)),s,dims)
                    errors["isotony"] = max(errors["isotony"],residual(nested-embedded[r][ij]))
                    counts["isotony"] += 1
            if set(r).isdisjoint(s):
                for a in embedded[r].values():
                    for b in embedded[s].values():
                        errors["disjoint_commutator"] = max(errors["disjoint_commutator"],residual(a@b-b@a))
                        counts["disjoint_commutator"] += 1
    return {"regions": [list(r) for r in regions], "errors": errors, "counts": counts,
            "dimensions_over_complex": {str(r): len(local[r]) for r in regions}}

def liouvillian(h, jumps):
    d = len(h); eye = np.eye(d)
    out = -1j*(np.kron(eye,h)-np.kron(h.T,eye))
    for raw_rate, j in jumps:
        gamma = rate(raw_rate)
        q = j.conj().T@j
        out += gamma*(np.kron(j.conj(),j)-.5*np.kron(eye,q)-.5*np.kron(q.T,eye))
    return out

def direct_generator(h,jumps,rho):
    out = -1j*(h@rho-rho@h)
    for gamma,j in jumps:
        q = j.conj().T@j
        out += gamma*(j@rho@j.conj().T-.5*(q@rho+rho@q))
    return out

def heisenberg_energy(h,jumps):
    out = np.zeros_like(h)
    for gamma,j in jumps:
        q = j.conj().T@j
        out += gamma*(j.conj().T@h@j-.5*(q@h+h@q))
    return out

def choi(channel,d):
    c = np.zeros((d*d,d*d),complex)
    for (i,j),e in units(d).items():
        c[i*d:(i+1)*d,j*d:(j+1)*d] = unvec(channel@vec(e),d)
    return c

def phase_root(psi):
    magnitudes = np.abs(psi)
    phase = np.divide(psi,magnitudes,out=np.zeros_like(psi),where=magnitudes>0)
    out = phase*np.sqrt(magnitudes)
    return out/np.linalg.norm(out)

def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat(); timer = time.perf_counter()
    pre = BASE/"PREREGISTRO_DEVICE_R1.json"; freeze_path=BASE/"FREEZE_DEVICE_R1.json"
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    if sha(pre)!=freeze["preregister"]["sha256"] or sha(__file__)!=freeze["runner"]["sha256"]:
        raise RuntimeError("Preregister or runner changed after freeze")
    p = json.loads(pre.read_text(encoding="utf-8"))
    for k,source in p["source_pins"].items():
        if sha(source["path"])!=source["sha256"]: raise RuntimeError("Source pin differs: "+k)
    if datetime.datetime.fromisoformat(freeze["created_utc"]) >= datetime.datetime.fromisoformat(started):
        raise RuntimeError("Preregister must precede run")
    m=p["model"]; nm=p["numerics"]; checks=[]
    tree=ast.parse(Path(p["source_pins"]["alpha_source"]["path"]).read_bytes().decode("utf-8"))
    constants={n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
               if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)
               and n.targets[0].id in {"ALPHA_FINE_CODATA_2018","_SEALED_ALPHA_CODATA_2018"}}
    alpha=constants["ALPHA_FINE_CODATA_2018"]
    if isinstance(alpha,bool) or not math.isfinite(alpha) or alpha!=constants["_SEALED_ALPHA_CODATA_2018"]:
        raise ValueError("Alpha source failed validation")
    beta=alpha*math.sqrt(math.e)
    if not 0<beta<.5: raise ValueError("Unexpected beta range")
    coords=list(itertools.product(p["geometry"]["coordinates"],repeat=3))
    names={3:"vertex",2:"edge",1:"face",0:"center"}
    sites=[{"id":i,"coordinates":list(x),"kind":names[sum(v!=0 for v in x)]} for i,x in enumerate(coords)]
    edges=[[i,j] for i,x in enumerate(coords) for j,y in enumerate(coords) if i<j and sum(abs(a-b) for a,b in zip(x,y))==1]
    counts={name:sum(site["kind"]==name for site in sites) for name in names.values()}
    checks.append({"name":"geometry","passed":len(set(coords))==27 and counts==p["geometry"]["counts"] and len(edges)==54})
    dims=tuple(m["factor_dims"]); d=math.prod(dims)
    algebra=algebra_measurements(dims)
    checks += [check("local_algebra_"+k,v,nm["algebra_tolerance"]) for k,v in algebra["errors"].items()]
    lower=np.array([[0,1],[0,0]],complex); z=np.diag([1.,-1.]).astype(complex)
    ai=embed(lower,(0,),dims); ao=embed(lower,(1,),dims); sm=embed(lower,(2,),dims); sp=sm.conj().T
    h=m["omega_c"]*(ai.conj().T@ai+ao.conj().T@ao)+m["omega_OH"]*(sp@sm)
    h+=m["g_JC"]*(ai.conj().T@sm+sp@ai)+m["Omega"]*(sp+sm)
    jump=ao.conj().T@sm+sp@ai
    conventional=[(m["kappa_in"],ai),(m["kappa_out"],ao),(m["gamma_OH"],sm),
                  (m["gamma_dephasing"],embed(z,(2,),dims))]
    checks.append(check("hamiltonian_hermitian",residual(h-h.conj().T),nm["algebra_tolerance"]))
    rng=np.random.default_rng(nm["seed"]); states=[]
    for i in range(nm["random_mixed_states"]):
        a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); r=a@a.conj().T
        states.append((f"mixed_{i}",r/np.trace(r)))
    for i in range(nm["random_pure_states"]):
        v=rng.normal(size=d)+1j*rng.normal(size=d); states.append((f"pure_{i}",projector(v/np.linalg.norm(v))))
    states += [(f"basis_{i}",projector(np.eye(d,dtype=complex)[:,i])) for i in range(d)]
    states.append(("maximally_mixed",np.eye(d)/d))
    for _,rho in states: validate_density(rho,nm["state_tolerance"])
    channel_rows=[]; energy_rows=[]; generator_rows=[]
    for gamma_lambda in m["gamma_Lambda_values"]:
        jumps=conventional+[(beta*rate(gamma_lambda),jump)]
        gen=liouvillian(h,jumps); hd=heisenberg_energy(h,jumps)
        trvec=vec(np.eye(d)); energyvec=vec(h.T)
        direct_error=max(residual(unvec(gen@vec(r),d)-direct_generator(h,jumps,r)) for _,r in states)
        trace_error=float(np.linalg.norm(trvec@gen))
        dual_error=max(abs(np.trace(h@direct_generator(h,jumps,r))-np.trace(r@hd)) for _,r in states)
        generator_rows.append({"gamma_Lambda":gamma_lambda,"gamma_holo":beta*gamma_lambda,
                               "direct_error":direct_error,"trace_error":trace_error,"energy_duality_error":float(dual_error),
                               "energy_observable_derivative_norm":residual(hd)})
        checks += [check(f"generator_direct_{gamma_lambda}",direct_error,nm["algebra_tolerance"]),
                   check(f"generator_trace_{gamma_lambda}",trace_error,nm["channel_tolerance"]),
                   check(f"energy_duality_{gamma_lambda}",dual_error,nm["energy_identity_tolerance"])]
        eps=nm["finite_difference_step"]
        fd=(expm(eps*gen)-expm(-eps*gen))/(2*eps)
        augmented=np.zeros((d*d+1,d*d+1),complex); augmented[:-1,:-1]=gen; augmented[-1,:-1]=energyvec@gen
        for t in nm["times"]:
            channel=expm(t*gen); cj=choi(channel,d)
            herm=residual(cj-cj.conj().T); eig=float(np.linalg.eigvalsh((cj+cj.conj().T)/2).min())
            tp=residual(np.trace(cj.reshape(d,d,d,d),axis1=1,axis2=3)-np.eye(d))
            mins=[]; trace_res=[]; herm_res=[]; derivative_res=[]
            for _,rho in states:
                evolved=unvec(channel@vec(rho),d)
                mins.append(float(np.linalg.eigvalsh((evolved+evolved.conj().T)/2).min()))
                trace_res.append(float(abs(np.trace(evolved)-1)))
                herm_res.append(residual(evolved-evolved.conj().T))
                derivative_res.append(float(abs(energyvec@fd@vec(evolved)-np.trace(evolved@hd))))
            row={"gamma_Lambda":gamma_lambda,"t":t,"choi_min_eigenvalue":eig,"choi_hermiticity":herm,
                 "trace_preservation_residual":tp,"output_min_eigenvalue":min(mins),
                 "output_trace_residual":max(trace_res),"output_hermiticity":max(herm_res),
                 "energy_derivative_error":max(derivative_res),"states":len(states)}
            channel_rows.append(row)
            checks += [check(f"choi_hermitian_{gamma_lambda}_{t}",herm,nm["channel_tolerance"]),
                       check(f"choi_cp_{gamma_lambda}_{t}",max(0.,-eig),nm["channel_tolerance"]),
                       check(f"channel_tp_{gamma_lambda}_{t}",tp,nm["channel_tolerance"]),
                       check(f"output_psd_{gamma_lambda}_{t}",max(0.,-min(mins)),nm["state_tolerance"]),
                       check(f"output_trace_{gamma_lambda}_{t}",max(trace_res),nm["state_tolerance"]),
                       check(f"output_hermitian_{gamma_lambda}_{t}",max(herm_res),nm["state_tolerance"]),
                       check(f"energy_derivative_{gamma_lambda}_{t}",max(derivative_res),nm["energy_derivative_tolerance"])]
            rho0=states[0][1]; augout=expm(t*augmented)@np.concatenate([vec(rho0),[0j]])
            initial=float(np.trace(h@rho0).real); final=float((energyvec@augout[:-1]).real)
            flux=float(augout[-1].real); ledger=abs(final-initial-flux)
            energy_rows.append({"gamma_Lambda":gamma_lambda,"t":t,"initial_system_energy":initial,
                                "final_system_energy":final,"integrated_flux_into_system":flux,
                                "opposite_environment_bookkeeping":-flux,"ledger_residual":ledger,
                                "scope":"fixed Hamiltonian open-system balance; environment is bookkeeping, not microscopic bath construction"})
            checks.append(check(f"integrated_energy_{gamma_lambda}_{t}",ledger,nm["energy_identity_tolerance"]))
    negative_rates=[]
    for bad in [-.1,float("nan"),float("inf"),True]:
        try: liouvillian(h,[(bad,jump)]); rejected=False; message="accepted"
        except ValueError as exc: rejected=True; message=str(exc)
        negative_rates.append({"input":repr(bad),"rejected":rejected,"message":message})
    checks.append({"name":"invalid_rates_refused","passed":all(x["rejected"] for x in negative_rates)})
    invalid=np.array([[.5,1-beta],[1-beta,.5]],complex)
    try: validate_density(invalid,nm["state_tolerance"]); rejected=False; reason="accepted"
    except ValueError as exc: rejected=True; reason=str(exc)
    checks.append({"name":"literal_rho01_refused","passed":rejected})
    normalized=np.array([[.5,(1-beta)/2],[(1-beta)/2,.5]],complex)
    normalized_min=validate_density(normalized,nm["state_tolerance"])
    checks.append(check("normalized_coherence",abs(2*abs(normalized[0,1])-(1-beta)),nm["algebra_tolerance"]))
    zero=np.array([1.,0.],complex); plus=np.array([1.,1.],complex)/math.sqrt(2)
    density=.5*projector(zero)+.5*projector(plus)
    e,v=np.linalg.eigh(density)
    first=.5*projector(phase_root(zero))+.5*projector(phase_root(plus))
    second=sum((e[i]*projector(phase_root(v[:,i])) for i in range(2)),np.zeros((2,2),complex))
    root_diff=residual(first-second)
    checks.append({"name":"root_code_quantum_channel_refused","passed":root_diff>nm["negative_witness_threshold"]})
    classical=np.array([-2.,-.3,0.,.7,3.]); decoded=np.sign(classical)*np.sqrt(np.abs(classical))**2
    checks.append(check("classical_root_decode",float(np.max(np.abs(decoded-classical))),nm["algebra_tolerance"]))
    ccr=lower@lower.conj().T-lower.conj().T@lower
    checks.append({"name":"truncated_ccr_control","passed":residual(ccr-np.eye(2))>nm["negative_witness_threshold"]})
    result={"unit":"F1.REDE","verdict":"PASSA" if all(c["passed"] for c in checks) else "FALHA",
            "statute":"REAL numerical structural checks of a declared finite truncation; no physical verdict",
            "started_utc":started,"finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "seconds":time.perf_counter()-timer,"python":sys.executable,"python_version":platform.python_version(),
            "numpy_version":np.__version__,"scipy_version":scipy.__version__,
            "preregister_sha256":sha(pre),"freeze_sha256":sha(freeze_path),"runner_sha256":sha(__file__),
            "source_pins":p["source_pins"],"alpha_runtime":alpha,"beta_runtime":beta,
            "geometry":{"sites":sites,"edges":edges,"counts":counts,"edge_count":len(edges)},
            "quantum_dimensions":{"Hilbert":d,"Liouville":d*d,"Choi":d*d,"factors":list(dims)},
            "local_algebras":algebra,"generators":generator_rows,"channels":channel_rows,"energy_ledger":energy_rows,
            "controls":{"negative_rates":negative_rates,"invalid_literal_coherence":{"minimum_eigenvalue":float(np.linalg.eigvalsh(invalid).min()),"rejected":rejected,"reason":reason},
                        "normalized_coherence":{"C":float(2*abs(normalized[0,1])),"rho01":float(normalized[0,1].real),"minimum_eigenvalue":normalized_min,"not_a_dynamical_plateau_prediction":True},
                        "root_nonlinearity":{"same_input_density_residual":residual(density-v@np.diag(e)@v.conj().T),"different_output_frobenius_norm":root_diff,"interpretation":"ensemble dependence of the source amplitude-root rule when promoted to a normalized pure-state map; classical encode/decode remains allowed"},
                        "truncation_ccr":{"commutator_diagonal":np.diag(ccr).real.tolist(),"distance_from_identity":residual(ccr-np.eye(2))}},
            "checks":checks,"checks_passed":sum(c["passed"] for c in checks),"checks_total":len(checks),
            "physical_verdict_allowed":False,"no_claims":p["no_claims"]}
    write_new(BASE/"RESULTADO_DEVICE_R1.json",result)
    print(json.dumps({"verdict":result["verdict"],"checks":f"{result['checks_passed']}/{len(checks)}",
                      "beta":beta,"root_ensemble_difference":root_diff,"seconds":result["seconds"]},ensure_ascii=False))
    if not all(c["passed"] for c in checks): raise SystemExit(1)

if __name__ == "__main__": main()
