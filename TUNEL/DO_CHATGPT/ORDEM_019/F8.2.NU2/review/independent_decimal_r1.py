"""Independent Decimal review of fixed-beta synthetic neutrino diagnostics.

This script does not import the builder or execute scientific originals.
It reads a single alpha assignment and evaluates all functions independently.
"""
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from decimal import Decimal as D, localcontext
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "INDEPENDENT_DECIMAL_R1.json"
if OUT.exists():
    raise FileExistsError(OUT)

def pin(path):
    b = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

def atan_series(x):
    total = x
    power = x
    n = 1
    while True:
        power *= -x*x
        term = power / (2*n+1)
        updated = total + term
        if updated == total:
            return total
        total = updated
        n += 1

with localcontext() as ctx:
    ctx.prec = 95
    pi = 16*atan_series(D(1)/5)-4*atan_series(D(1)/239)

    def cos(x):
        x %= 2*pi
        if x > pi:
            x -= 2*pi
        total = term = D(1)
        n = 1
        while True:
            term *= -x*x / ((2*n-1)*(2*n))
            updated = total + term
            if updated == total:
                return total
            total = updated
            n += 1

    plan_path = BASE / "PLANO_R1.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"), parse_float=D)
    result_path = BASE / "CALCULOS_ESPECTRAIS_R1.json"
    result = json.loads(result_path.read_text(encoding="utf-8"), parse_float=D)
    source = Path(plan["alpha_source"])
    source_text = source.read_text(encoding="utf-8-sig")
    match = re.findall(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*(?:#.*)?$", source_text, re.M)
    if len(match) != 1:
        raise ValueError("nonunique alpha assignment")
    alpha = D(match[0])
    beta = alpha*D("0.5").exp()
    cc = plan["constants"]
    c = cc["c_m_s"]
    hbJ = cc["h_J_s"]/(2*pi)
    hbeV = hbJ/cc["eV_J"]
    tp = (hbJ*cc["G_SI"]/c**5).sqrt()
    q = plan["inputs_reference_not_fitted"]
    s12, s13, s23 = [q[k].sqrt() for k in ["sin2theta12", "sin2theta13", "sin2theta23"]]
    c12, c13, c23 = [(1-q[k]).sqrt() for k in ["sin2theta12", "sin2theta13", "sin2theta23"]]

    def mm(a,b):
        return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

    r12 = [[c12,s12,0],[-s12,c12,0],[0,0,1]]
    r13 = [[c13,0,s13],[0,1,0],[-s13,0,c13]]
    r23 = [[1,0,0],[0,c23,s23],[0,-s23,c23]]
    U = mm(r23, mm(r13,r12))
    unitary_error = max(abs(sum(U[i][k]*U[j][k] for k in range(3))-D(i==j)) for i in range(3) for j in range(3))
    w = [u*u for u in U[0]]
    diag = [D(".2"),D(".3"),D(".5")]
    diag_probs = [sum(U[k][i]**2*diag[i] for i in range(3)) for k in range(3)]
    masses = [D(0),q["dm21_eV2"],q["dm31_eV2"]]
    pairs = [(0,1),(0,2),(1,2)]
    gaps = [abs(masses[j]-masses[i]) for i,j in pairs]
    texture = [(gap/gaps[0])**2 for gap in gaps]

    def rate(E,L,gap):
        omega = gap/(2*E*D(10)**6*hbeV)
        gamma = beta*tp*omega**2/2
        return omega, gamma, gamma*L/c

    reference_rates = []
    max_rate_relerror = D(0)
    for row in result["rate_examples"]:
        calc = []
        for k,gap in enumerate(gaps):
            omega,gamma,a = rate(row["E_MeV_INPUT"],row["L_m_INPUT"],gap)
            rel = abs(gamma/row["channels"][k]["gamma_per_s"]-1)
            max_rate_relerror = max(max_rate_relerror,rel)
            calc.append({"pair":row["channels"][k]["pair"],"omega_s_inv":str(omega),"gamma_s_inv":str(gamma),"gamma_t":str(a),"one_minus_damping":str(1-(-a).exp())})
        reference_rates.append({"source":row["source"],"energy_MeV":str(row["E_MeV_INPUT"]),"channels":calc})

    L = q["reactor_baseline_km"]*1000
    samples = []
    delta_relerrors = []
    for n in range(121):
        E = D(2)+D(n)/20
        p0 = sum(x*x for x in w)
        dp = D(0)
        for k,(i,j) in enumerate(pairs):
            omega,gamma,a = rate(E,L,gaps[k])
            cross = 2*w[i]*w[j]*cos(omega*L/c)
            p0 += cross
            dp += cross*((-a).exp()-1)
        samples.append((p0,dp))
        old = result["ideal_reactor"]["samples"][n]
        assert abs(p0-old["P0"]) < D("1e-12")
        delta_relerrors.append(abs(dp/old["deltaP_stable"]-1))
    meanP = sum(x[0] for x in samples)/121
    meanD = sum(x[1] for x in samples)/121
    coefficient = meanD/meanP
    fixed = sum(dp*dp/p0 for p0,dp in samples)/121
    profiled = sum((dp-coefficient*p0)**2/p0 for p0,dp in samples)/121
    n5 = 25/profiled
    n5_error = abs(n5/result["ideal_reactor"]["N_unoscillated_for_nominal_5_profile"]-1)
    assert n5_error < D("1e-11")
    assert max_rate_relerror < D("1e-12")
    assert unitary_error < D("1e-90")
    assert max(delta_relerrors) < D("1e-9")

    # Generic log-slope identity, evaluated independently at a nontrivial r(E).
    # log Gamma = -2x + log tau + log beta + beta log r.
    slope_rows = []
    chi0 = 2*(1/alpha+((1/alpha)**2-1).sqrt()).ln()
    for kappa in [D("-.1"),D(".1")]:
        def lg(x):
            halfchi = (chi0+kappa*x)/2
            bh = D(".5").exp() / ((halfchi.exp()+(-halfchi).exp())/2)
            return -2*x + D(".2")*x + bh.ln() + bh*D(".3")*x
        for x in [-D(2).ln(),D(0),D(2).ln()]:
            hc = (chi0+kappa*x)/2
            b = D(".5").exp()/((hc.exp()+(-hc).exp())/2)
            tanh = (hc.exp()-(-hc).exp())/(hc.exp()+(-hc).exp())
            bprime = -b*tanh*kappa/2
            analytic = -2+D(".2")+bprime/b+bprime*D(".3")*x+b*D(".3")
            dx = D("1e-20")
            numerical = (lg(x+dx)-lg(x-dx))/(2*dx)
            assert abs(analytic-numerical)<D("1e-37")
            slope_rows.append({"x":str(x),"chi_slope":str(kappa),"analytic":str(analytic),"independent_difference":str(numerical-analytic)})

    bridge = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex")
    bridge_lines = bridge.read_text(encoding="utf-8-sig").splitlines()
    out = {
        "reviewer":"nu2_skeptic independent Decimal implementation",
        "utc":datetime.now(timezone.utc).isoformat(),
        "verdict":"PASS_WITH_SCOPE_LIMITS_NO_PHYSICAL_SIGNIFICANCE",
        "precision_decimal_digits":95,
        "pi_method":"Machin formula, atan Taylor series",
        "pins":[pin(plan_path),pin(BASE/"PLANO_RECONCILIACAO_R1.json"),pin(BASE/"spectral_operator_r1.py"),pin(result_path),pin(source),pin(bridge),pin(Path(__file__))],
        "source_fixed_beta_lines_1367_1371":bridge_lines[1366:1371],
        "beta0":str(beta),"hbar_eV_s":str(hbeV),"tP_s":str(tp),
        "pmns_orthogonality_error":str(unitary_error),
        "diagonal_flavor_probabilities":[str(x) for x in diag_probs],
        "diagonal_stationary":"exactly, since all off-diagonal entries are zero and diagonal damping/phase factors are 1",
        "texture":[str(x) for x in texture],
        "rate_rows":reference_rates,"max_rate_relative_difference":str(max_rate_relerror),
        "max_spectral_deltaP":str(max(abs(dp) for _,dp in samples)),
        "max_deltaP_relative_difference":str(max(delta_relerrors)),
        "fixed_fisher_per_unoscillated_exposure":str(fixed),
        "profiled_fisher_per_unoscillated_exposure":str(profiled),
        "N5_profiled_unoscillated":str(n5),"N5_relative_difference":str(n5_error),
        "mean_P0":str(meanP),"slope_checks":slope_rows,
        "scope":["tau_star=tP and Kfac=1 are conditional inputs", "vacuum no-smearing flat grid is not a JUNO forecast", "running beta(E) is a counterfactual extension under the current fixed-beta source", "a diagonal mass state is stationary only in that same basis", "pair texture does not match JUNO gamma21=gamma31 gamma32=0; published bound cannot be directly transferred", "no neutrino-star luminosity functional or observed significance was obtained"]
    }
    with OUT.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(out,f,ensure_ascii=False,indent=2,allow_nan=False)
        f.write("\n")
    print(json.dumps({"file":pin(OUT),"max_deltaP":out["max_spectral_deltaP"],"N5_profiled":out["N5_profiled_unoscillated"],"N5_relative_difference":out["N5_relative_difference"]}))
