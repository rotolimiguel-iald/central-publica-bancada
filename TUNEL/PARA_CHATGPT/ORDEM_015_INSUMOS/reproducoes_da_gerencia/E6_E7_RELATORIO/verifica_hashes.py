import re, hashlib, os, sys, json
BASE = r"C:\IALD\Central de Patentes\Chatgpt"
docs = {
 "RELATORIO_FINAL": r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013BIS_RELATORIO_FINAL.md",
 "B5": r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013BIS_B5_quadro_e_modulo.md",
}
pat = re.compile(r"\[([^\]]+)\]\(<[^>]+>\)\s+—\s+`([0-9a-f]{64})`\s+\((\d+) B\)")
out = {}
for k, p in docs.items():
    txt = open(p, encoding="utf-8").read()
    rows = pat.findall(txt)
    res = []
    for rel, h, nb in rows:
        fp = os.path.join(BASE, rel.replace("/", os.sep))
        if not os.path.exists(fp):
            res.append((rel, "MISSING", h, nb, None)); continue
        sz = os.path.getsize(fp)
        hh = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        res.append((rel, "OK" if (hh == h and sz == int(nb)) else "MISMATCH", h, nb, (hh, sz)))
    out[k] = res
    n_ok = sum(1 for r in res if r[1] == "OK")
    print(f"{k}: {n_ok}/{len(res)} OK")
    for r in res:
        if r[1] != "OK":
            print("  ", r)
json.dump(out, open("hashes_verificados.json", "w"), indent=1)
