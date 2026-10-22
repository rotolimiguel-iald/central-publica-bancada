import json, hashlib, os
root=r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
d=json.load(open(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013BIS_INSUMOS\ESTADO_AUDITADO.json",encoding='utf-8'))
for a in d['artefatos']:
    p=os.path.join(root,a['arquivo'])
    if not os.path.exists(p): print("MISSING",a['arquivo']); continue
    b=open(p,'rb').read(); h=hashlib.sha256(b).hexdigest()[:16]
    print(("OK   " if h==a['sha16'] and len(b)==a['bytes'] else "DIFF ")+a['arquivo'], a['sha16'], h, a['bytes'], len(b))
