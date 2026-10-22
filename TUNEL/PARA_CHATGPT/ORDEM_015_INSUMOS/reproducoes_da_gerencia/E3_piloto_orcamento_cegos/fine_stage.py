"""Fine threshold in dtau440 (dtau220 = 0) on four sources, direct LAL path fs 4096, one process per point."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_repro as R
SRC = dict(REF=R.REF, DRAW8=R.DRAW8,
           HIGHMASS=dict(m1=90.0, m2=80.0, chi1=0.3, chi2=0.3, dist_Mpc=800.0, iota=0.6, phase=0.37),
           LOWMASS=dict(m1=20.0, m2=12.0, chi1=-0.14, chi2=-0.058, dist_Mpc=1000.0, iota=0.8, phase=0.3),
           HIGHSPIN=dict(m1=45.0, m2=35.0, chi1=0.95, chi2=0.9, dist_Mpc=500.0, iota=0.6, phase=0.37),
           NEGSPIN=dict(m1=45.0, m2=35.0, chi1=-0.9, chi2=-0.9, dist_Mpc=500.0, iota=0.6, phase=0.37))
rows = []
for name, src in SRC.items():
    for d44 in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6):
        c = dict(src, dtau220=0.0, dtau440=d44, domega220=0.0, domega440=0.0, fs=4096)
        rec = R.run_group(f"FINE_{name}_d44_{d44}", "direct", [c], timeout=300)
        st = list(rec["results"].values())[0]["status"] if rec["results"] else f"CRASH_rc{rec['returncode']}"
        rows.append(dict(source=name, dtau440=d44, status=st))
    # also the negative side of dtau220 with d44 fixed 1.0 and 1.2 to check independence from dtau220<=0
    for d22 in (-0.8, -0.4):
        for d44 in (1.0, 1.2):
            c = dict(src, dtau220=d22, dtau440=d44, fs=4096)
            rec = R.run_group(f"FINE_{name}_d22_{d22}_d44_{d44}", "direct", [c], timeout=300)
            st = list(rec["results"].values())[0]["status"] if rec["results"] else f"CRASH_rc{rec['returncode']}"
            rows.append(dict(source=name, dtau220=d22, dtau440=d44, status=st))
with open(R.OUT, "a") as f: f.write(json.dumps(dict(group="FINE_SUMMARY", rows=rows)) + "\n")
for r in rows: print(r)
