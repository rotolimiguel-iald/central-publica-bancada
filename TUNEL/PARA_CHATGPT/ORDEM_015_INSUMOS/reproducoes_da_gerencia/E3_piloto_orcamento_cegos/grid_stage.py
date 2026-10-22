"""2-D map of the native abort on the reference source: dtau220 x dtau440 (direct LAL path, fs 4096).
Also the same map with the 440 damping-time ratio r = (1+dtau440)/(1+dtau220) printed, to locate the wall."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_repro as R
D22 = [-0.8, -0.5, 0.0, 0.5, 1.0, 2.0]
D44 = [-0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
rows = []
for d22 in D22:
    for d44 in D44:
        rec = R.run_group(f"GRID_REF_direct4096_d22_{d22}_d44_{d44}", "direct", [dict(R.REF, dtau220=d22, dtau440=d44, fs=4096)], timeout=300)
        st = list(rec["results"].values())[0]["status"] if rec["results"] else f"CRASH_rc{rec['returncode']}"
        rows.append(dict(dtau220=d22, dtau440=d44, ratio_440_over_220=(1 + d44) / (1 + d22), status=st))
# second family: DRAW8-like high-spin source at same grid but only the diagonal ratio 1.0..3.0 to test source dependence
for d22, d44 in ((0.0, 1.0), (0.0, 1.5), (0.0, 2.0), (0.0, 3.0), (0.5, 2.0), (0.5, 3.0), (1.0, 3.0), (1.0, 4.0)):
    rec = R.run_group(f"GRID_DRAW8_direct4096_d22_{d22}_d44_{d44}", "direct", [dict(R.DRAW8, dtau220=d22, dtau440=d44, fs=4096)], timeout=300)
    st = list(rec["results"].values())[0]["status"] if rec["results"] else f"CRASH_rc{rec['returncode']}"
    rows.append(dict(source="DRAW8", dtau220=d22, dtau440=d44, ratio_440_over_220=(1 + d44) / (1 + d22), status=st))
with open(R.OUT, "a") as f: f.write(json.dumps(dict(group="GRID_SUMMARY", rows=rows)) + "\n")
print("=== GRID (REF source unless marked) status by (dtau220, dtau440) ratio=(1+d44)/(1+d22)")
for r in rows: print(r.get("source", "REF"), r["dtau220"], r["dtau440"], round(r["ratio_440_over_220"], 3), r["status"])
