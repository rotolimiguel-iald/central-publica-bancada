import hashlib, json, os, sys
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for ch in iter(lambda:f.read(1<<20),b''): h.update(ch)
    return h.hexdigest()
base=r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013_INSUMOS"
man=json.load(open(os.path.join(base,"MANIFESTO_INSUMOS.json"),encoding="utf-8"))
out={"manifesto":{},"fontes":{},"extras_na_pasta":[]}
ok=0;bad=0
for rel,v in man["arquivos"].items():
    p=os.path.normpath(os.path.join(base,rel))
    if not os.path.exists(p):
        out["manifesto"][rel]="MISSING";bad+=1;continue
    s=sha(p)[:16]; b=os.path.getsize(p)
    st="OK" if (s==v["sha16"] and b==v["bytes"]) else f"DIFF sha16={s} bytes={b} esperado={v}"
    if st=="OK": ok+=1
    else: bad+=1
    out["manifesto"][rel]=st
print("MANIFESTO: ok",ok,"bad",bad)
for k,v in out["manifesto"].items():
    if v!="OK": print("  ",k,v)
# extras
listed=set(os.path.normpath(os.path.join(base,r)) for r in man["arquivos"])
for root,ds,fs in os.walk(base):
    for f in fs:
        p=os.path.normpath(os.path.join(root,f))
        if p not in listed and not p.endswith("MANIFESTO_INSUMOS.json"):
            st=os.stat(p)
            out["extras_na_pasta"].append((p,st.st_size,st.st_mtime))
print("EXTRAS in insumos folder:",out["extras_na_pasta"])
# also check whole PARA_CHATGPT tree mtimes after 2026-09-21 19:41
import time
pc=r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT"
cut=time.mktime(time.strptime("2026-09-21 19:41:00","%Y-%m-%d %H:%M:%S"))
late=[]
for root,ds,fs in os.walk(pc):
    for f in fs:
        p=os.path.join(root,f)
        if os.stat(p).st_mtime>cut: late.append((p,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(p).st_mtime))))
    for d in ds:
        p=os.path.join(root,d)
        if os.stat(p).st_mtime>cut: late.append(("DIR "+p,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(p).st_mtime))))
print("PARA_CHATGPT entries modified after order:",len(late))
for x in late[:50]: print("  ",x)
# fontes da casa
fc=json.load(open(os.path.join(base,"FONTES_DA_CASA.json"),encoding="utf-8"))
for f in fc["fontes"]:
    p=f["caminho"]
    if not os.path.exists(p): print("FONTE MISSING",p); continue
    s=sha(p)[:16]; b=os.path.getsize(p)
    st="OK" if (s==f["sha16"] and b==f["bytes"]) else f"DIFF now sha16={s} bytes={b} (esperado {f['sha16']} {f['bytes']})"
    print("FONTE",st, p, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(p).st_mtime)))
