"""Verify the preregistered finite contract; originals are read, never imported.

Writes a new exclusive result file in this directory. Refuses an existing result.
No network, observed data, production, memory or canonical-kernel mutation.
"""
import hashlib
import importlib.util
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_new(path, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    with path.open("xb") as f:
        f.write(data)
    if path.read_bytes() != data:
        raise RuntimeError("write verification failed")


def main():
    out = BASE / "RESULTADO_PHYSICAL_R1.json"
    if out.exists():
        raise RuntimeError("result already exists; choose a new evidence version")
    started = datetime.now(timezone.utc).isoformat()
    pin = json.loads((BASE / "PREREGISTRO_PIN_R1.json").read_text(encoding="utf-8"))
    for name, digest in pin["files"].items():
        if sha(BASE / name) != digest:
            raise RuntimeError("preregistered file changed: " + name)
    spec = json.loads((BASE / "PREREGISTRO_PHYSICAL_R1.json").read_text(encoding="utf-8"))
    modspec = importlib.util.spec_from_file_location("v394_physical_candidate", BASE / "physical_parameters.py")
    mod = importlib.util.module_from_spec(modspec)
    modspec.loader.exec_module(mod)
    derive = mod.v394_physical_parameters
    hb = 6.62607015e-34 / (2*math.pi)
    p = derive(hb, 2*hb)
    kg = mod.v394_kms_clock(p, spec["reference"]["kappa_s_inv"])
    tol = spec["tolerances"]["matrix_abs"]
    rtol = spec["tolerances"]["relative_scalar"]
    checks = []
    def check(name, residual, bound=tol):
        val = float(residual)
        checks.append({"name": name, "residual": val, "bound": bound,
                       "pass": bool(math.isfinite(val) and abs(val) <= bound)})
    def norm(x):
        return float(np.linalg.norm(x))
    I = np.eye(2, dtype=complex)
    sx = np.array([[0,1],[1,0]], dtype=complex)
    sy = np.array([[0,-1j],[1j,0]], dtype=complex)
    sz = np.diag([1.,-1.]).astype(complex)
    C = np.diag([1.,1j])
    pp, pm = (I+sy)/2, (I-sy)/2
    basis = [np.eye(4, dtype=complex)[k].reshape(2,2) for k in range(4)]
    def pinching(X):
        return pp@X@pp + pm@X@pm
    def dissipator(L,X):
        ld = L.conj().T
        return L@X@ld - (ld@L@X + X@ld@L)/2
    def unitary(t,pars=p):
        phase = pars["Omega_rad_s"]*t
        return math.cos(phase)*I + 1j*math.sin(phase)*sy
    def channel(X,t,pars=p):
        E = pinching(X)
        U = unitary(t,pars)
        return U@(E+math.exp(-pars["gamma_s_inv"]*t)*(X-E))@U.conj().T
    H = p["Eref_J"]*I - p["V0_J"]*sy
    rootH = math.sqrt(p["energies_J"][0])*pp + math.sqrt(p["energies_J"][1])*pm
    L = math.sqrt(p["beta"]/hb)*rootH
    Lq = math.sqrt(p["beta"]*p["tau_eff_s"])*(-p["Omega_rad_s"]*sy)
    check("C_sigma_x_Cdag_sigma_y", norm(C@sx@C.conj().T-sy))
    check("C_preserves_parity", norm(C@sz@C.conj().T-sz))
    check("rootH_square", norm(rootH@rootH-H)/norm(H))
    for k,X in enumerate(basis):
        check("root_dissipator_basis_%d"%k, norm(dissipator(L,X)-p["gamma_s_inv"]*(pinching(X)-X)))
        check("quadratic_same_gap_basis_%d"%k, norm(dissipator(Lq,X)-dissipator(L,X)))
    ground = derive(hb,hb)
    check("ground_rate_beta_Omega", abs(ground["gamma_s_inv"]/(ground["beta"]*ground["Omega_rad_s"])-1), rtol)
    check("ground_Hpos", norm((hb*I-hb*sy)-2*hb*pm)/hb)
    A = math.sqrt(1-p["beta"])*pp+math.sqrt(p["beta"])*pm
    B = math.sqrt(p["beta"])*pp+math.sqrt(1-p["beta"])*pm
    for k,X in enumerate(basis):
        current = X.copy()
        Ustep = unitary(p["echo_dt_s"])
        for n in spec["echo_steps"]:
            check("matched_echo_%d_basis_%d"%(n,k), norm(current-channel(X,n*p["echo_dt_s"])))
            Y=Ustep@current@Ustep.conj().T
            current=A@Y@A+B@Y@B
    for scale in spec["clock_rescalings"]:
        scaled = derive(scale*hb,scale*2*hb)
        kscaled = mod.v394_kms_clock(scaled, scale*kg["kappa_s_inv"])
        for field in ("Omega_rad_s","gamma_s_inv"):
            check("scale_%s_%s"%(scale,field), abs(scaled[field]/(scale*p[field])-1), rtol)
        for field in ("tau_eff_s","echo_dt_s"):
            check("scale_%s_%s"%(scale,field), abs(scaled[field]/(p[field]/scale)-1), rtol)
        check("scale_%s_gibbs"%scale, norm(np.array(kscaled["gibbs_weights_low_high"])-kg["gibbs_weights_low_high"]))
        check("scale_%s_kms_period"%scale, abs(kscaled["kms_period_s"]/(kg["kms_period_s"]/scale)-1), rtol)
        for t in spec["time_grid_s"]:
            for k,X in enumerate(basis):
                check("scale_%s_t%s_basis%d"%(scale,t,k), norm(channel(X,t,p)-channel(X,t/scale,scaled)))
    gl,gh=kg["gibbs_weights_low_high"]
    rho=gl*pp+gh*pm
    for s in spec["time_grid_s"]:
        R=np.exp(1j*s*math.log(gl))*pp+np.exp(1j*s*math.log(gh))*pm
        # alpha_t(X)=U(-t)XU(-t)^dag; t=-P*s gives U(P*s).
        U=unitary(kg["kms_period_s"]*s)
        for k,X in enumerate(basis):
            check("kms_rescale_s%s_basis%d"%(s,k), norm(R@X@R.conj().T-U@X@U.conj().T))
        check("gibbs_fixed_t%s"%s, norm(channel(rho,s)-rho))
    # No-go witnesses are mathematical checks, not observed physical exclusions.
    old_omega=.5*1.30
    old_gamma=-math.log(p["eta"])/.35
    nogos={
        "old_echo_same_clock": {"gamma":old_gamma,"Omega":old_omega,
            "gamma_over_Omega":old_gamma/old_omega,"root_max_ratio":p["beta"],
            "root_equality_impossible":old_gamma/old_omega>p["beta"]},
        "three_levels": {"energies_in_unit_E":[0,1,4],
            "tau_eff_in_hbar_over_E":[1,1/9,1/4], "no_common_tau":len({1,1/9,1/4})==3},
        "zero_choice": {"ground_gamma":ground["gamma_s_inv"],"reference_gamma":p["gamma_s_inv"],
            "different_root_rates":ground["gamma_s_inv"]!=p["gamma_s_inv"],
            "same_gibbs_weights":mod.v394_kms_clock(ground,kg["kappa_s_inv"])["gibbs_weights_low_high"]==kg["gibbs_weights_low_high"]},
    }
    lower=np.array([[0,1],[0,0]], dtype=complex)
    def tensor(a,b,c):return np.kron(np.kron(a,b),c)
    J=tensor(I,lower.conj().T,lower)+tensor(lower,I,lower.conj().T)
    nonunital=J@J.conj().T-J.conj().T@J
    nogos["device_jump"]={"D_J_identity_hs_norm":norm(nonunital),"unitary_equivalence_to_root_impossible":norm(nonunital)>tol}
    nogos["old_echo_full16"]={"matrix_unit":"|0><2|", "H_energy_gap":0.0,
        "mirror_factor":p["eta"], "f_H_dephasing_factor":1.0,
        "equality_impossible":p["eta"]!=1.0}
    invalid=[]
    base={"V0_J":hb,"Eref_J":2*hb,"hbar_J_s":hb,"alpha":7.2973525693e-3}
    for name in base:
        for label,value in [("nan",float("nan")),("inf",float("inf")),("-inf",-float("inf")),("true",True),("false",False),("zero",0.0),("negative",-1.0),("text","1")]:
            args=dict(base);args[name]=value
            try:
                derive(**args); refused=False
            except mod.V394PhysicalContractError:
                refused=True
            invalid.append({"field":name,"value":label,"refused":refused})
    extra=[{"V0_J":2*hb,"Eref_J":hb},
           {"V0_J":1e308,"Eref_J":1e308,"hbar_J_s":1e-308},
           {"V0_J":hb,"Eref_J":1e308,"hbar_J_s":1e-308},
           {"V0_J":1e308,"Eref_J":1e308,"hbar_J_s":1e308},
           {"V0_J":hb,"Eref_J":2*hb,"alpha":.5/math.sqrt(math.e)}]
    for index,args in enumerate(extra):
        try:derive(**args);refused=False
        except mod.V394PhysicalContractError:refused=True
        invalid.append({"extra":index,"refused":refused})
    for label,value in [("nan",float("nan")),("inf",float("inf")),("bool",True),("zero",0.0),("negative",-1.0),("overflow_period",1e-308),("lost_faithfulness",.001)]:
        try:mod.v394_kms_clock(p,value);refused=False
        except mod.V394PhysicalContractError:refused=True
        invalid.append({"kms":label,"refused":refused})
    # Large energy origin is represented by center+half-gap, avoiding subtraction.
    large=derive(hb,1.0)
    check("large_offset_stable_tau",abs(large["tau_eff_s"]/(hb/4)-1),rtol)
    flags=[nogos["old_echo_same_clock"]["root_equality_impossible"],nogos["three_levels"]["no_common_tau"],
           nogos["zero_choice"]["different_root_rates"],nogos["zero_choice"]["same_gibbs_weights"],
           nogos["device_jump"]["unitary_equivalence_to_root_impossible"],nogos["old_echo_full16"]["equality_impossible"]]
    result={"schema":"f1-tempo-v394-physical-result/v1","started_utc":started,
        "finished_utc":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),"numpy":np.__version__,
        "preregistration_pin_sha256":sha(BASE/"PREREGISTRO_PIN_R1.json"),
        "script_sha256":sha(Path(__file__)),"reference":p,"finite_kms":kg,"ground":ground,
        "checks":checks,"checks_passed":sum(c["pass"] for c in checks),"checks_total":len(checks),
        "negative_witnesses":nogos,"invalid_input_checks":invalid,"large_offset_representation":large,
        "all_passed":all(c["pass"] for c in checks) and all(flags) and all(c["refused"] for c in invalid),
        "statute":"REAL numerical checks; DERIVED finite identities; INPUT synthetic scales",
        "scope":"No observed data, no production, no nature confirmation, no gate movement"}
    save_new(out,result)
    print(json.dumps({"result":str(out),"sha256":sha(out),"all_passed":result["all_passed"],
                      "checks":len(checks),"invalid_inputs":len(invalid)},ensure_ascii=False))
    if not result["all_passed"]:raise SystemExit(1)


if __name__=="__main__":main()
