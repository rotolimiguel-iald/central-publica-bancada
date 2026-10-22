"""Frente C — inspecao de estrutura (somente leitura) dos JSONs da bancada."""
import json, hashlib, os, sys
B = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
FILES = sys.argv[1:] or [
    "C5_IMR_RECOVERY.json", "C5_IMR_RECOVERY_VALIDATION.json", "C5_BIAS_ABLATION.json",
    "C5_OVERTONE_ABLATION.json", "C5_NONLINEAR_SOURCE_SUMMARY.json",
    "C5_SOURCE_UNCERTAINTY_SUMMARY.json", "C2_TRAJECTORY_RECOVERY.json",
    "C4_CATALOG_COMBINATION.json", "C4_GWTC3_COMBINATION.json",
    "C4_GWTC3_PUBLISHED_COMBINATION.json", "C6_RESULTS.json", "PSD_CONTROLS.json",
    "C5_FISHER_EMPIRICAL.json", "C1_LEITURAS.json", "C4_JOINT_MODES.json",
    "C6_PYRING_START_COMPARISON.json", "C5_EXTRA_QNMS.json",
]
def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()[:16]
def shape(v, depth=0, maxd=2):
    if isinstance(v, dict):
        if depth >= maxd:
            return "{%d keys}" % len(v)
        return "{" + ", ".join("%s: %s" % (k, shape(x, depth + 1, maxd)) for k, x in list(v.items())[:40]) + ("..." if len(v) > 40 else "") + "}"
    if isinstance(v, list):
        if not v:
            return "[]"
        return "[%d x %s]" % (len(v), shape(v[0], depth + 1, maxd))
    if isinstance(v, str):
        return repr(v[:60])
    return repr(v)
for fn in FILES:
    p = os.path.join(B, fn)
    if not os.path.exists(p):
        print("=== %s NAO ENCONTRADO" % fn); continue
    d = json.load(open(p, encoding="utf-8"))
    print("=== %s  bytes=%d sha16=%s" % (fn, os.path.getsize(p), sha16(p)))
    print(shape(d, 0, 2)[:4000])
    print()
