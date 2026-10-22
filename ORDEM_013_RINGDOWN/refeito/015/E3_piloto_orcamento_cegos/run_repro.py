"""Driver: spawns wf_case.py per group of cases, records rc/signal, and identifies the crashing case.

Runs in WSL /opt/lal_env. Writes only inside this folder. Never touches /opt or the bench's folders.
Usage: python run_repro.py <stage>   stages: versions | targeted | scan_registered | scan_narrow | all
"""
import json, os, subprocess, sys, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
PY = "/opt/lal_env/bin/python"
WORKER = os.path.join(HERE, "wf_case.py")
OUT = os.environ.get("REPRO_OUT", os.path.join(HERE, "REPRO_RESULTS.jsonl"))

REF = dict(m1=39.0, m2=33.0, chi1=0.05, chi2=-0.03, dist_Mpc=403.0, iota=0.6, phase=0.37)  # C5_IMR_CONTROLS.json
DRAW8 = dict(m1=40.70912464765123, m2=20.237781889510657, chi1=0.9196233876975504, chi2=0.2055129322455731,
             dist_Mpc=103.3345570969183, iota=1.560261620994438, phase=4.252515165901328,
             dtau220=-0.6157519631492032, dtau440=1.7780455359890353,
             domega220=-0.42647193412015016, domega440=0.7808349673597068)  # bench DRAW8 exact
DRAW2 = dict(m1=20.860586263061307, m2=12.965093961217725, chi1=-0.13877212574117448, chi2=-0.05752201871382956,
             dist_Mpc=1473.8057561837784, iota=0.2732633972102579, phase=5.133423253519265,
             dtau220=1.9914659412667162, dtau440=-0.1969196314413365,
             domega220=1.3570260139143946, domega440=-0.6195938635097105)

def run_group(name, mode, cases, timeout=600):
    tag = name + "_" + hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest()[:8]
    spec = os.path.join(HERE, "spec_" + tag + ".json"); prog = os.path.join(HERE, "prog_" + tag + ".jsonl")
    if os.path.exists(prog): os.remove(prog)
    json.dump(dict(mode=mode, cases=cases, progress=prog), open(spec, "w"))
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    t0 = time.perf_counter()
    try:
        p = subprocess.run([PY, "-B", WORKER, spec], capture_output=True, text=True, timeout=timeout, env=env)
        rc, err = p.returncode, p.stderr[-3000:]
    except subprocess.TimeoutExpired:
        rc, err = "TIMEOUT", ""
    wall = time.perf_counter() - t0
    lines = [json.loads(l) for l in open(prog)] if os.path.exists(prog) else []
    results = {}; last_begin = None; done = False
    for l in lines:
        if "begin" in l: last_begin = l["begin"]
        elif "end" in l: results[l["end"]] = l["result"]
        elif "done" in l: done = True
    crashed_case = None
    if not done and last_begin is not None and last_begin not in results:
        crashed_case = dict(index=last_begin, case=cases[last_begin])
    rec = dict(group=name, mode=mode, n_cases=len(cases), returncode=rc, wall_s=round(wall, 3), completed=len(results),
               done=done, crashed_case=crashed_case, results={str(k): v for k, v in results.items()},
               stderr_tail=err.strip().splitlines()[-6:] if err else [])
    with open(OUT, "a") as f: f.write(json.dumps(rec) + "\n")
    print(json.dumps(dict(group=name, rc=rc, completed=len(results), of=len(cases), crashed=crashed_case is not None,
                          statuses=[v.get("status") for v in results.values()]), ensure_ascii=False))
    return rec

def stage_versions():
    code = ("import sys,lal,lalsimulation as ls,numpy,bilby,dynesty,platform;"
            "print(__import__('json').dumps(dict(python=sys.version.split()[0],lal=lal.__version__,lalsimulation=ls.__version__,"
            "numpy=numpy.__version__,bilby=bilby.__version__,dynesty=dynesty.__version__,kernel=platform.release(),"
            "approx_pSEOBNRv4HM_PA=ls.GetApproximantFromString('pSEOBNRv4HM_PA'))))")
    p = subprocess.run([PY, "-c", code], capture_output=True, text=True)
    rec = dict(group="versions", out=p.stdout.strip(), err=p.stderr.strip()[-500:])
    with open(OUT, "a") as f: f.write(json.dumps(rec) + "\n")
    print(rec["out"])

def stage_targeted():
    # (1) the waveform the task asked for: dtau220=-0.02 at 4096 and 8192 Hz, direct LAL path
    for fs in (4096, 8192):
        run_group(f"REF_dtau220_-0.02_direct_{fs}", "direct", [dict(REF, dtau220=-0.02, fs=fs)])
        run_group(f"REF_dtau0_direct_{fs}", "direct", [dict(REF, dtau220=0.0, fs=fs)])
        run_group(f"REF_SEOBNRv4HM_PA_direct_{fs}", "direct", [dict(REF, approximant="SEOBNRv4HM_PA", fs=fs)])
        run_group(f"REF_dtau220_-0.02_dtau440_-0.08_direct_{fs}", "direct", [dict(REF, dtau220=-0.02, dtau440=-0.082, fs=fs)])
    # (2) the same through the pilot's bilby path at the pilot fmax (1024 -> internal 2048 Hz) and higher
    for fmax in (1024, 2048, 4096):
        run_group(f"REF_dtau220_-0.02_bilby_fmax{fmax}", "bilby", [dict(REF, dtau220=-0.02, fmax=fmax)])
    # (3) the bench's DRAW8 exact tuple: direct path at three rates, bilby path at three fmax
    for fs in (2048, 4096, 8192):
        run_group(f"DRAW8_direct_{fs}", "direct", [dict(DRAW8, fs=fs)])
    for fmax in (1024, 2048, 4096):
        run_group(f"DRAW8_bilby_fmax{fmax}", "bilby", [dict(DRAW8, fmax=fmax)])
    # (4) isolate the mechanism on DRAW8 at fs 4096 (direct): zero each deformation family in turn
    run_group("DRAW8_direct_4096_dtau440_0", "direct", [dict(DRAW8, dtau440=0.0, fs=4096)])
    run_group("DRAW8_direct_4096_dtau220_0", "direct", [dict(DRAW8, dtau220=0.0, fs=4096)])
    run_group("DRAW8_direct_4096_domega_0", "direct", [dict(DRAW8, domega220=0.0, domega440=0.0, fs=4096)])
    run_group("DRAW8_direct_4096_alldef_0", "direct", [dict(DRAW8, dtau220=0.0, dtau440=0.0, domega220=0.0, domega440=0.0, fs=4096)])
    run_group("DRAW8_direct_4096_GR_SEOBNRv4HM_PA", "direct", [dict(DRAW8, approximant="SEOBNRv4HM_PA", fs=4096)])
    # (5) dtau440 threshold scan on DRAW8 (direct, 4096): each in own process
    for d44 in (0.0, 0.5, 1.0, 1.5, 1.7780455359890353, 2.5, 4.0):
        run_group(f"DRAW8_direct_4096_dtau440_{d44}", "direct", [dict(DRAW8, dtau440=d44, fs=4096)])
    # (6) REF source with extreme registered corners of the deformation box
    for d22, d44 in ((-0.8, 4.0), (2.0, -0.8), (-0.8, -0.8), (2.0, 4.0), (-0.5, 4.0)):
        run_group(f"REF_direct_4096_corner_d22_{d22}_d44_{d44}", "direct", [dict(REF, dtau220=d22, dtau440=d44, fs=4096)])
    # (7) DRAW2 (the other logged EDOM draw) at 4096 direct
    run_group("DRAW2_direct_4096", "direct", [dict(DRAW2, fs=4096)])

def draw_prior(rng, box):
    while True:
        m1 = rng.uniform(15, 100); m2 = rng.uniform(10, 100)
        if m2 <= m1 and m2 / m1 >= 0.125: break
    return dict(m1=m1, m2=m2, chi1=rng.uniform(-0.99, 0.99), chi2=rng.uniform(-0.99, 0.99),
                dist_Mpc=rng.uniform(100, 2000), iota=float(__import__("numpy").arccos(rng.uniform(-1, 1))),
                phase=rng.uniform(0, 6.283185307179586),
                dtau220=rng.uniform(*box["dtau220"]), dtau440=rng.uniform(*box["dtau440"]),
                domega220=rng.uniform(*box["domega220"]), domega440=rng.uniform(*box["domega440"]))

def stage_scan(name, box, n=120, seed=132203, per_proc=1, mode="bilby", fmax=1024, fs=4096):
    import numpy as np
    rng = np.random.default_rng(seed)
    draws = [draw_prior(rng, box) for _ in range(n)]
    summary = dict(FINITE=0, DOMAIN_RETURNED_NONE=0, CRASH=0, OTHER=0); crashes = []
    for i in range(0, n, per_proc):
        chunk = draws[i:i + per_proc]
        cases = [dict(c, fmax=fmax, fs=fs) for c in chunk]
        rec = run_group(f"{name}_{i:04d}", mode, cases, timeout=300)
        for k, v in rec["results"].items():
            s = v.get("status"); summary[s if s in summary else "OTHER"] = summary.get(s if s in summary else "OTHER", 0) + 1
        if rec["crashed_case"] is not None:
            summary["CRASH"] += 1; crashes.append(dict(rc=rec["returncode"], case=rec["crashed_case"]["case"]))
    out = dict(group=f"SCAN_SUMMARY_{name}", box=box, n=n, seed=seed, mode=mode, fmax=fmax, summary=summary, crashes=crashes)
    with open(OUT, "a") as f: f.write(json.dumps(out) + "\n")
    print(json.dumps(dict(scan=name, summary=summary, n_crash_listed=len(crashes))))

REGISTERED = dict(dtau220=(-0.8, 2.0), dtau440=(-0.8, 4.0), domega220=(-0.8, 2.0), domega440=(-0.8, 2.0))
NARROW = dict(dtau220=(-0.5, 0.5), dtau440=(-0.5, 0.5), domega220=(-0.5, 0.5), domega440=(-0.5, 0.5))
GR_ONLY = dict(dtau220=(0.0, 0.0), dtau440=(0.0, 0.0), domega220=(0.0, 0.0), domega440=(0.0, 0.0))

if __name__ == "__main__":
    st = sys.argv[1] if len(sys.argv) > 1 else "all"
    if st in ("versions", "all"): stage_versions()
    if st in ("targeted", "all"): stage_targeted()
    if st in ("scan_registered", "all"): stage_scan("REGISTERED_bilby_fmax1024", REGISTERED, n=int(os.environ.get("NSCAN", "120")))
    if st in ("scan_narrow", "all"): stage_scan("NARROW_bilby_fmax1024", NARROW, n=int(os.environ.get("NSCAN", "120")))
    if st in ("scan_gr", "all"): stage_scan("GR_ONLY_bilby_fmax1024", GR_ONLY, n=int(os.environ.get("NSCAN", "60")))
    if st == "scan_registered_direct4096": stage_scan("REGISTERED_direct_fs4096", REGISTERED, n=int(os.environ.get("NSCAN", "120")), mode="direct", fs=4096)
