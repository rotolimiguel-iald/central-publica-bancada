"""Power-only design calculation. No observed means, likelihood, verdict, or original execution."""
from pathlib import Path
import hashlib, json, math, os, datetime

BASE = Path(__file__).resolve().parent
INPUTS = BASE.parents[3] / "PARA_CHATGPT" / "ORDEM_018_INSUMOS"

def atomic_json(path, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data
    os.replace(tmp, path)
    assert path.read_bytes() == data

def calculate():
    # Deliberately use the audited snapshot; no import/execution of um.py.
    input_file = INPUTS / "FASE8__PODER_FASE8_UNIVERSO_PRIMORDIAL.json"
    raw = input_file.read_bytes()
    audit = json.loads((BASE.parent / "AUDITORIA_PREREGISTROS_F3.json").read_bytes())
    expected = next(x["sha256"] for x in audit["manifest_checks"] if x["name"] == input_file.name)
    assert hashlib.sha256(raw).hexdigest() == expected
    legacy = json.loads(raw)
    alpha = legacy["beta"]["alpha_regex"]
    ALPHA_FINE_CODATA_2018 = alpha
    beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
    p = json.loads((BASE / "PARAMETROS_PRIMARIOS.json").read_bytes())
    checks = []
    for source in json.loads((BASE / "FONTES_PRIMARIAS.json").read_bytes()):
        source_raw = (BASE/source["file"]).read_bytes()
        ok = len(source_raw) == source["bytes"] and hashlib.sha256(source_raw).hexdigest() == source["sha256"]
        assert ok, source["file"]
        checks.append({"file":source["file"],"sha256":source["sha256"],"match":ok})
    delta_rad = 4*beta/3
    speedup = math.sqrt(1+delta_rad)
    f_nu = (7/8)*(4/11)**(4/3)
    n_sm = 3.044 # [INPUT] benchmark convention from Fase8, distinct from N_nu=3.
    delta_neff_late = delta_rad*(1+f_nu*n_sm)/f_nu
    delta_nu_early = delta_rad*43/7 # ideal relativistic e+- plasma, N_nu=3
    fields = p["fields2020"]
    nu_y = fields["log_derivatives"]["G_N"]["Yp"]
    nu_d = fields["log_derivatives"]["G_N"]["DH"]
    delta_y = fields["fiducial_Yp_theory"]*math.expm1(nu_y*math.log1p(delta_rad))
    delta_log_d = nu_d*math.log1p(delta_rad)
    delta_log10_d = delta_log_d/math.log(10)
    sigma_ln_d = math.log(10)*next(x["sigma"] for x in p["observational_sigmas"] if x["id"]=="Cooke2018")
    helium=[]
    for row in p["observational_sigmas"]:
        if row["observable"]=="Yp":
            helium.append({"sigma_source":row["id"],"sigma_observed":row["sigma"],"design_separation_sigma":abs(delta_y)/row["sigma"]})
    pitrou_cases=[]
    for label,dn in [("early_epoch_equivalent",delta_nu_early),("late_epoch_equivalent",delta_neff_late)]:
        u=dn/p["pitrou2018"]["N_nu"]
        responses={k:sum(c*u**(i+1) for i,c in enumerate(v)) for k,v in p["pitrou2018"]["fractional_series_coefficients_N_nu"].items()}
        dy=p["pitrou2018"]["fiducial_Yp_theory"]*responses["Yp"]
        pitrou_cases.append({"label":label,"Delta_Nnu_input":dn,"fractional_response":responses,"delta_Yp_theory":dy,"delta_ln_DH_theory":math.log1p(responses["DH"]),"role":"TWO_DISTINCT_EXTRA_SPECIES_DESIGN_CASES_NOT_PROVEN_BRACKET_OF_UNIFORM_S"})
    deriv=fields["log_derivatives"]
    nuisance_det=deriv["eta"]["Yp"]*deriv["tau_n"]["DH"]-deriv["tau_n"]["Yp"]*deriv["eta"]["DH"]
    # Independent algebraic limiting checks, without experimental centers.
    assert math.expm1(nu_d*math.log1p(0)) == 0
    assert abs(speedup**2-(1+delta_rad)) < 1e-14
    assert abs(2*math.log(speedup)-math.log1p(delta_rad)) < 1e-14
    assert nuisance_det != 0
    return {
      "status":"DERIVED_CONDITIONAL_DESIGN_ONLY_NO_VERDICT",
      "generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "input_snapshot":{"path":str(input_file),"sha256":expected},
      "source_integrity":checks,
      "beta":{"alpha_snapshot":alpha,"formula":"ALPHA_FINE_CODATA_2018*sqrt(e)","runtime":beta},
      "map_A":{"delta_radiation":delta_rad,"S_radiation_dominated":speedup,"DeltaNeff_post_annihilation":delta_neff_late,"DeltaNnu_ideal_pre_annihilation":delta_nu_early,"N_SM_benchmark_input":n_sm,"comment":"No single DeltaNnu exactly represents uniform dressing through annihilation."},
      "fields_uniform_speedup_proxy":{"dlnY_dlnS":2*nu_y,"dlnDH_dlnS":2*nu_d,"delta_Yp_theory":delta_y,"delta_ln_DH_theory":delta_log_d,"delta_log10_DH_theory":delta_log10_d,"fractional_DH_theory":math.expm1(delta_log_d),"helium_obs_only_design":helium,"Cooke_sigma_ln_DH":sigma_ln_d,"Cooke_obs_only_design_separation_sigma":abs(delta_log_d)/sigma_ln_d,"required_sigma_Yp_for_5sigma":abs(delta_y)/5,"required_sigma_log10_DH_for_5sigma":abs(delta_log10_d)/5,"scope":"Approximate frozen logarithmic derivative at Fields fiducial; no nuisance marginalization, network rerun, or experimental likelihood."},
      "pitrou_additional_neutrino_cases":pitrou_cases,
      "nuisance_identifiability":{"observables":["lnYp","lnDH"],"columns":["lneta","lntau_n"],"X":[[deriv["eta"]["Yp"],deriv["tau_n"]["Yp"]],[deriv["eta"]["DH"],deriv["tau_n"]["DH"]]],"determinant":nuisance_det,"rank":2,"unconstrained_nuisance_projected_signal":"zero for any two-component signal if both nuisance columns are unrestricted","priors_required":True,"joint_power_computed":False},
      "cmb_sigma_only_scenarios":[{"id":x["id"],"sigma_Neff":x["sigma_Neff"],"design_separation_sigma":delta_neff_late/x["sigma_Neff"],"scope":x["status"],"calendar":None} for x in p["cmb_design_scenarios"]],
      "sigma_Neff_needed_5sigma":delta_neff_late/5,
      "pitrou2018_theory_error_scale":{"fractional_sigma_DH":p["pitrou2018"]["theory_fractional_sigma_fixed_omega_b"]["DH"],"scale_over_Fields_signal_fraction":p["pitrou2018"]["theory_fractional_sigma_fixed_omega_b"]["DH"]/abs(math.expm1(delta_log_d)),"scope":"Scale comparison across models only; not a legitimate mixed-model likelihood or universal systematic floor."},
      "bounds":{"observed_centers_used":False,"posteriors_opened":False,"strain_opened":False,"PE_run":False,"original_programs_imported_or_run":False,"BBN_network_run":False,"new_composite_or_verdict":False}
    }
if __name__ == "__main__":
    result=calculate()
    atomic_json(BASE/"CALCULO_SENSIBILIDADES_SIGMAS.json",result)
    print(json.dumps({"status":result["status"],"uniform_speedup":result["fields_uniform_speedup_proxy"],"nuisance":result["nuisance_identifiability"]},ensure_ascii=False,indent=2))
