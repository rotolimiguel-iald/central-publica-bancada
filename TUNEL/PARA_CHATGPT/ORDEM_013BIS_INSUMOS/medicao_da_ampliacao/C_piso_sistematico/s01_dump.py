"""Frente C — dump detalhado (somente leitura) das chaves relevantes."""
import json, os, sys
B = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
L = lambda fn: json.load(open(os.path.join(B, fn), encoding="utf-8"))
def pj(x, n=6000):
    s = json.dumps(x, ensure_ascii=False, indent=None, default=str)
    print(s[:n] + ("..." if len(s) > n else ""))

which = sys.argv[1]
if which == "imr":
    d = L("C5_IMR_RECOVERY.json")
    r = d["results"]
    print("KEYS:", list(r[0].keys()))
    pj(r[0]); pj(r[1])
    print("JOINT KEYS:", list(d["joint_mixture_criteria"][0].keys()))
    for j in d["joint_mixture_criteria"]:
        pj(j, 600)
    print("DRAWS:", [list(x.keys()) for x in d["draws"]])
    pj(d["scope"], 2000)
elif which == "bias":
    d = L("C5_BIAS_ABLATION.json")
    print("KEYS:", list(d["results"][0].keys()))
    for x in d["results"]:
        pj(x, 500)
    print("SCOPE:", d["scope"])
elif which == "overtone":
    d = L("C5_OVERTONE_ABLATION.json")
    print("KEYS:", list(d["results"][0].keys()))
    for x in d["results"]:
        pj(x, 700)
    print("SCOPE:", d["scope"]); print(d["shared_harmonic_rate"])
elif which == "nonlinear":
    d = L("C5_NONLINEAR_SOURCE_SUMMARY.json")
    for k, v in d.items():
        if k != "checks":
            print(k, "=", json.dumps(v, default=str)[:600])
    print("CHECK KEYS:", list(d["checks"][0].keys()))
    for x in d["checks"]:
        pj(x, 900)
elif which == "srcunc":
    d = L("C5_SOURCE_UNCERTAINTY_SUMMARY.json")
    for k, v in d.items():
        if k not in ("primary_B", "surrogate_B_examples", "runs"):
            print(k, "=", json.dumps(v, default=str)[:800])
    print("RUNS:"); [pj(x, 900) for x in d["runs"]]
    print("PRIMARY_B KEYS:", list(d["primary_B"][0].keys()))
    for x in d["primary_B"]:
        pj(x, 900)
    print("SURROGATE examples (first 6):")
    for x in d["surrogate_B_examples"][:6]:
        pj(x, 700)
elif which == "c2":
    d = L("C2_TRAJECTORY_RECOVERY.json")
    print("KEYS:", list(d["rows"][0].keys()))
    for x in d["rows"]:
        y = {k: v for k, v in x.items() if not isinstance(v, list)}
        pj(y, 1200)
        for k, v in x.items():
            if isinstance(v, list):
                print("   list", k, len(v), (v[:3] if len(v) < 60 else "..."))
    print(d["physical_scope"]); print(d["Cauchy_warning"]); print(d["not_C5"])
elif which == "c4":
    d = L("C4_CATALOG_COMBINATION.json")
    print("GR DIAG KEYS:", list(d["common_deformation_GR_diagnostics"][0].keys()))
    for x in d["common_deformation_GR_diagnostics"]:
        pj(x, 1500)
    for sel in ("release_figure_selection_31", "all_available_33"):
        print("--", sel)
        for x in d["catalog"][sel]:
            pj(x, 600)
    pj(d["physical_model_caution"]); pj(d["unresolved"])
elif which == "gwtc3":
    for fn in ("C4_GWTC3_COMBINATION.json", "C4_GWTC3_PUBLISHED_COMBINATION.json"):
        d = L(fn); print("=====", fn)
        for x in d["common_deformation_GR_diagnostics"]:
            pj(x, 1500)
        for x in d["catalog"]:
            pj(x, 500)
        pj(d["limitations"])
elif which == "c6":
    d = L("C6_RESULTS.json")
    print(d["reason"]); print(d["scope"]); print(d["do_not_combine"])
    print("CONV:"); [pj(x, 600) for x in d["convergence"]]
    print("KEYS:", list(d["results"][0].keys()))
    for x in d["results"]:
        pj(x, 700)
elif which == "psd":
    d = L("PSD_CONTROLS.json"); pj(d, 4000)
elif which == "fishemp":
    d = L("C5_FISHER_EMPIRICAL.json")
    print("REC KEYS:", list(d["records"][0].keys()))
    pj(d["records"][0], 1500)
    pj(d["same_source_R_B"], 3000)
    pj(d["mass_spin_free"], 1500)
    pj(d["not_in_this_local_fisher_approximation"])
elif which == "c1":
    d = L("C1_LEITURAS.json")
    print("ROW KEYS:", list(d["rows"][0].keys()))
    for x in d["rows"]:
        pj(x, 1200)
elif which == "c4_220":
    d = L("C4_CATALOG_220.json")
    print("TOP:", {k: (type(v).__name__, len(v) if hasattr(v, "__len__") else v) for k, v in d.items()})
    rows = d.get("rows") or d.get("results")
    print("ROW KEYS:", list(rows[0].keys()))
    pj(rows[0], 3000)
elif which == "pyring_start":
    d = L("C6_PYRING_START_COMPARISON.json"); pj(d, 8000)
elif which == "jointmodes":
    d = L("C4_JOINT_MODES.json")
    for x in d["rows"]:
        pj(x, 800)
    pj(d["GR_HPD_controls"])
