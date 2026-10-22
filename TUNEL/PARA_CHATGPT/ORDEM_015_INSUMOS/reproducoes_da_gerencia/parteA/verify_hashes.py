import re, hashlib, os, sys, json, glob
notes = [
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013_M1_fechamento.md",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013_M2_C4_fechamento.md",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013_M3_C3_2_C2_RMOD.md",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013_M4_C5_parede_e_portao.md",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013_M5_C6pre.md",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013_M6_C7_final.md",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013BIS_MA_fechamento.md",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_013_ERRATA_contrato.md",
]
pat = re.compile(r"\]\(<([^>]+)>\)\s*(?:\|\s*)?(?:SHA256\s*)?`([0-9a-f]{64})`")
tot=ok=bad=missing=0
out=[]
for n in notes:
    txt=open(n,encoding='utf-8').read()
    for m in pat.finditer(txt):
        p=m.group(1).replace('/', os.sep); h=m.group(2); tot+=1
        if not os.path.exists(p): missing+=1; out.append(("MISSING",os.path.basename(n),p,h)); continue
        hh=hashlib.sha256(open(p,'rb').read()).hexdigest()
        if hh==h: ok+=1
        else: bad+=1; out.append(("MISMATCH",os.path.basename(n),p,h,hh))
print("total",tot,"ok",ok,"bad",bad,"missing",missing)
for o in out: print(o)
