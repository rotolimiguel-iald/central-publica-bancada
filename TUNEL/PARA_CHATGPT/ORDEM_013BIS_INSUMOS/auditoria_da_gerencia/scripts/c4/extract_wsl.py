# Auditor C4 -- read-only extraction of posterior columns to scratch npz (runs in WSL /opt/lal_env, no writes to house)
import h5py, numpy as np, json, glob, os, re, hashlib
R = "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public"
OUT = os.path.dirname(os.path.abspath(__file__))
cols = ["domega220","dtau220","final_spin_non_evolved","final_mass_non_evolved","final_spin","final_mass",
        "domega440","dtau440","redshift","final_mass_source_non_evolved"]
def dump(path, tag):
    info = {"path": path, "groups": []}
    with h5py.File(path, "r") as h:
        for g in h.keys():
            if isinstance(h[g], h5py.Group) and "posterior_samples" in h[g]:
                ps = h[g]["posterior_samples"]
                names = ps.dtype.names
                info["groups"].append({"group": g, "N": int(ps.shape[0]), "has": [c for c in cols if c in names]})
                if "domega220" in names:
                    arr = ps[()]
                    d = {c: np.asarray(arr[c], float) for c in cols if c in names}
                    # prior strings
                    pri = {}
                    if "priors" in h[g] and "analytic" in h[g]["priors"]:
                        for k in ["domega220","dtau220"]:
                            if k in h[g]["priors"]["analytic"]:
                                pri[k] = h[g]["priors"]["analytic"][k][0].decode()
                    if not pri and "config_file" in h[g]:
                        try:
                            txt = h[g]["config_file/config/prior_dict"][0].decode()
                            for k in ["domega220","dtau220","domega440","dtau440"]:
                                m = re.findall(r"\b"+k+r"\s*=\s*([A-Za-z]+\([^)]*\)|[-\d.]+)", txt)
                                pri[k] = m
                        except Exception as e:
                            pri["err"] = str(e)
                    info["groups"][-1]["priors"] = pri
                    np.savez(os.path.join(OUT, "post_%s__%s.npz" % (tag, g)), **d)
    return info
res = []
res.append(dump(R + "/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5", "GW250114_17018009"))
for p in sorted(glob.glob(R + "/21454847/extracted/pSEOB/metafiles/*.h5")):
    tag = os.path.basename(p).replace("pSEOB_","").replace("_Prod0.h5","")
    try:
        res.append(dump(p, "G5_" + tag))
    except Exception as e:
        res.append({"path": p, "error": str(e)})
json.dump(res, open(os.path.join(OUT, "extract_info.json"), "w"), indent=1)
print(json.dumps(res[0], indent=1)[:3000])
print(len(res))
