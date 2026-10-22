import h5py, numpy as np, json, glob, os
R = "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin"
OUT = os.path.dirname(os.path.abspath(__file__))
info = []
for p in sorted(glob.glob(R + "/*.h5")):
    rec = {"file": os.path.basename(p), "groups": []}
    with h5py.File(p, "r") as h:
        def visit(name, obj):
            if isinstance(obj, h5py.Dataset) and name.endswith("posterior_samples") or (isinstance(obj, h5py.Group) and name.endswith("posterior_samples")):
                rec["groups"].append(name)
        h.visititems(visit)
        rec["top"] = list(h.keys())
        for g in rec["groups"]:
            obj = h[g]
            names = obj.dtype.names if isinstance(obj, h5py.Dataset) else list(obj.keys())
            rec.setdefault("names", {})[g] = [n for n in names if any(s in n for s in ["omega220","tau220","final_spin","final_mass"])]
            if isinstance(obj, h5py.Dataset) and "domega220" in names:
                a = obj[()]
                fs = "final_spin" if "final_spin" in names else ("final_spin_non_evolved" if "final_spin_non_evolved" in names else None)
                np.savez(os.path.join(OUT, "g3_%s.npz" % os.path.basename(p).replace(".h5","")), domega220=np.asarray(a["domega220"], float),
                         dtau220=np.asarray(a["dtau220"], float), chi=np.asarray(a[fs], float) if fs else np.array([]), spin_key=fs or "")
    info.append(rec)
json.dump(info, open(os.path.join(OUT, "extract_gwtc3_info.json"), "w"), indent=1)
print(json.dumps(info[:2], indent=1)[:2500])
