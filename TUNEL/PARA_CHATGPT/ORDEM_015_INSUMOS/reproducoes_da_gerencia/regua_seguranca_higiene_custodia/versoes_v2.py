import json,os,hashlib,glob,re
R=r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
est=json.load(open(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013BIS_INSUMOS\ESTADO_AUDITADO.json",encoding="utf-8"))
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()
print("== v1 intact vs ESTADO_AUDITADO ==")
full={}
for a in est["artefatos"]:
    p=os.path.join(R,a["arquivo"]); 
    if not os.path.exists(p): print("MISSING",a["arquivo"]); continue
    h=sha(p); full[a["arquivo"]]=h; ok=h[:16]==a["sha16"]; sz=os.path.getsize(p)
    print(("OK  " if ok else "DIFF"),a["arquivo"],a["sha16"],h[:16],a["bytes"],sz, "" if ok else "(vivo)" if a.get("vivo") else "<-- CHANGED")
print("\n== _vN files at top level: supersedes fields ==")
for p in sorted(glob.glob(os.path.join(R,"*_v[0-9]*.*"))):
    n=os.path.basename(p)
    if n.endswith(".json"):
        try: d=json.load(open(p,encoding="utf-8"))
        except Exception as e: print(n,"JSON ERR",e); continue
        sup=d.get("supersedes") if isinstance(d,dict) else None; sup_sha=d.get("supersedes_sha256") if isinstance(d,dict) else None
        # search nested
        if sup is None and isinstance(d,dict):
            for k,v in d.items():
                if isinstance(v,dict) and "supersedes" in v: sup=v["supersedes"]; sup_sha=v.get("supersedes_sha256"); break
        v1=None
        if sup:
            v1p=os.path.join(R,sup) if not os.path.isabs(str(sup)) else sup
            v1=sha(v1p) if os.path.exists(v1p) else "MISSING"
        print(n, "| supersedes:",sup,"| supersedes_sha256:",(sup_sha or "")[:16],"| v1 sha now:",(v1 or "")[:16], "| MATCH" if (sup_sha and v1 and sup_sha==v1) else ("NO-MATCH" if sup else "no supersedes"))
    else:
        t=open(p,encoding="utf-8",errors="replace").read()
        m=re.search(r"supersedes[^\n]{0,200}",t); h=re.findall(r"[0-9a-f]{64}",t[:600])
        print(n,"| first line:",t.splitlines()[0][:150],"| supersedes mention:",bool(m),"| sha in head:",[x[:16] for x in h][:3])
