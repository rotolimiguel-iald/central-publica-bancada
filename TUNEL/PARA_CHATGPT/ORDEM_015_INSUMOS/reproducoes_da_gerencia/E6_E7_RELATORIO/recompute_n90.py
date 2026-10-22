import json, math, hashlib, os, sys
import numpy as np
B = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
post = json.load(open(os.path.join(B, r"cache\POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json"), encoding="utf-8"))
print("schema", post['schema'], "catalogue", post['catalogue'], "runtime", post['runtime'])
print("n events", len(post['events']), "sum N", sum(e['N'] for e in post['events']))
ds = json.load(open(os.path.join(B, r"bis\e0_core\DATASET.json"), encoding="utf-8"))
core = json.load(open(os.path.join(B, r"bis\e0_core\E0_CORE.json"), encoding="utf-8"))
sets = ds['sets']
print("sets:", {k: (len(v) if isinstance(v, list) else type(v).__name__) for k, v in sets.items()})
s31 = sets['GWTC5_31']; print("GWTC5_31 sample:", json.dumps(s31)[:600])
# map product ids
rows = {r['product_id']: r for r in ds['rows']}
# --- prediction at medians (R-B, R-MOD?, R-RAIZ-0, R-LIN), BCW 220
ALPHA = 7.2973525693e-3; b = ALPHA*math.sqrt(math.e)
c=299792458.0; G=6.67430e-11; gm_sun=1.3271244e20; hbar=6.62607015e-34/(2*math.pi); tp=math.sqrt(hbar*G/c**5)
def pred(reading, m, a, z):
    tm=m*gm_sun/c**3; z1=1+z
    wr=1.5251-1.1568*(1-a)**0.1292; Q=.7000+1.4187*(1-a)**(-.4990); damping=wr/(2*Q)
    omega=wr/tm; tau=tm/damping
    if reading=='R-B': g=b*tm*omega**2/2
    elif reading=='R-RAIZ-0': g=b*omega/2
    elif reading=='R-LIN': g=b*omega
    elif reading=='R-A': g=b*z1*tp*omega**2/2
    else: return None
    x=g*tau; return -x/(1+x)
ev = {e['event_id']: e for e in post['events']}
print("E7 event ids:", sorted(ev)[:40])
# figure which product ids / events are in GWTC5_31
ids31 = s31 if isinstance(s31, list) else s31.get('product_ids') or s31.get('events')
out = {}
z90 = 5 + 1.2815515655446004
for reading in ('R-B','R-RAIZ-0','R-LIN','R-A'):
    d=[]; s=[]; d_e0=[]; s_e0=[]; missing=[]
    for pid in ids31:
        r = rows.get(pid) if isinstance(pid,str) else None
        if r is None:
            missing.append(pid); continue
        evid = r['event']
        e = ev.get(evid)
        if e is None:
            # try match by source sha
            cand=[x for x in post['events'] if x['source_sha256']==r['source_sha256']]
            e = cand[0] if cand else None
        if e is None: missing.append((pid, evid)); continue
        S = e['samples']
        tau = np.asarray(S['dtau220'], float)
        sig = float(np.std(tau, ddof=1))
        m = float(np.median(S['Mfdet'])); a=float(np.median(S['af'])); zz=float(np.median(S['z']))
        dd = pred(reading, m, a, zz)
        d.append(dd); s.append(sig)
        s_e0.append(r['stdtau'])
        pr = r['predictions']
        d_e0.append(pr.get(reading) if isinstance(pr, dict) else None)
    d=np.array(d); s=np.array(s)
    zsig = math.sqrt(np.sum((d/s)**2))
    mean_d2s2 = np.mean((d/s)**2)
    N90 = z90**2/mean_d2s2; N50 = 25/mean_d2s2
    I90 = N90*np.mean(1/s**2)
    cw = abs(np.sum(d/s**2))/math.sqrt(np.sum(1/s**2))   # common weighted correction / sigma_comb
    wmean = np.sum(d/s**2)/np.sum(1/s**2)
    out[reading] = dict(n=len(d), missing=missing, z_signal=zsig, N90=N90, N50=N50, I90=I90, I90_over_unit0058=I90*0.058**2,
                        common_weighted_corr_over_sigma=cw, weighted_mean_delta=wmean, N90_over_N50=N90/N50,
                        max_abs_diff_sigma_vs_E0=float(np.max(np.abs(s-np.array(s_e0)))) if len(s_e0)==len(s) else None,
                        e0_pred_sample=str(d_e0[:2])[:300])
    print(reading, json.dumps({k:v for k,v in out[reading].items() if k!='missing'}, default=str))
    print("   missing:", missing[:5])
print("=== E0_CORE combinations GWTC5_31 (R-B etc)")
comb = core['combinations']['GWTC5_31']
print(type(comb), (list(comb.keys())[:20] if isinstance(comb, dict) else len(comb)))
cc = comb if isinstance(comb, list) else comb.get('readings') or comb.get('rows') or list(comb.values())
for row in (cc if isinstance(cc, list) else []):
    if isinstance(row, dict) and row.get('reading') in ('R-B','R-RAIZ-0','R-LIN','R-A'):
        print(json.dumps({k:v for k,v in row.items() if not isinstance(v,(list,dict))}, ensure_ascii=False)[:1500])
json.dump(out, open("recompute_n90.json","w"), indent=1, default=str)
