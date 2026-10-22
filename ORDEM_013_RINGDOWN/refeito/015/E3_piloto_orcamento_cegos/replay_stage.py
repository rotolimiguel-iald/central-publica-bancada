"""Replay the pilot's exact prior sequence (same PriorDict, same seed 132203, same bilby draw call) beyond draw 8,
and push the draws in order through the pilot's bilby path (fmax 1024) in ONE process, as the pilot did, to find the
first crashing draw. Reads the registered config from RINGDOWN_5SIGMA_V1.json (read-only). Writes only here."""
import json, os, sys, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_repro as R
REG = "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1.json"
N = int(os.environ.get("NREPLAY", "300"))

def draws():
    import numpy as np, bilby
    cfg = json.load(open(REG, encoding="utf-8"))["pe_jobs"]["GW250114_PILOT"]
    prim = {k: getattr(bilby.core.prior, k) for k in ("Uniform", "Sine", "Cosine", "Constraint")}
    pri = {}
    for name, item in cfg["priors"].items():
        pri[name] = prim[item["kind"]](minimum=item["minimum"], maximum=item["maximum"], name=name,
                                       **({"boundary": item["boundary"]} if "boundary" in item else {}))
    def conv(p):
        out = dict(p)
        if "mass_1" in out and "mass_2" in out: out["mass_ratio"] = out["mass_2"] / out["mass_1"]
        return out  # bench's prior_conversion returns parameter_conversion(params)[0], i.e. the dict only
    priors = bilby.core.prior.PriorDict(dictionary=pri, conversion_function=conv)
    bilby.core.utils.random.seed(cfg["sampler"]["seed"]); np.random.seed(cfg["sampler"]["seed"])
    keys = [k for k, p in priors.items() if isinstance(p, bilby.core.prior.Prior) and p.is_fixed is False]
    rows = []
    for n in range(N):
        theta = priors.sample_subset_constrained_as_array(keys, size=1)[:, 0]
        rows.append(dict(zip(keys, map(float, theta))))
    return rows

rows = draws()
bench = json.load(open("/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_failure_diagnostic/PRIOR_REPLAY.json"))["draws"]
match = all(abs(rows[i]["mass_1"] - bench[i]["parameters"]["mass_1"]) < 1e-9 and abs(rows[i]["dtau440"] - bench[i]["parameters"]["dtau440"]) < 1e-9 for i in range(8))
print("first 8 draws identical to bench PRIOR_REPLAY:", match)
cases = []
for i, p in enumerate(rows):
    cases.append(dict(m1=p["mass_1"], m2=p["mass_2"], chi1=p["chi_1"], chi2=p["chi_2"], dist_Mpc=p["luminosity_distance"],
                      iota=p["theta_jn"], phase=p["phase"], dtau220=p["dtau220"], dtau440=p["dtau440"],
                      domega220=p["domega220"], domega440=p["domega440"], fmax=1024.0, fs=4096, draw_index_starting_1=i + 1))
pred = [(i + 1, (1 + c["dtau440"]) / max(1.0, 1 + c["dtau220"])) for i, c in enumerate(cases)]
print("draws with (1+d44)/max(1,1+d22) > 2.05 among first 40:", [(i, round(r, 2)) for i, r in pred[:40] if r > 2.05])
rec = R.run_group("REPLAY_SEQUENCE_pilot_path_fmax1024", "bilby", cases, timeout=900)
out = dict(group="REPLAY_SUMMARY", n_draws=N, first8_match_bench=match, returncode=rec["returncode"], completed=rec["completed"],
           crashed_case=rec["crashed_case"], statuses_first=[rec["results"].get(str(i), {}).get("status") for i in range(min(N, rec["completed"] + 1))])
with open(R.OUT, "a") as f: f.write(json.dumps(out) + "\n")
print(json.dumps(dict(rc=rec["returncode"], completed=rec["completed"], crashed=rec["crashed_case"]), indent=1))
