import os,re,hashlib,json,sys
D=r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT"
notes=sorted(f for f in os.listdir(D) if f.startswith("ENTREGA_013BIS_") and f.endswith(".md"))
abertura_sha=hashlib.sha256(open(os.path.join(D,"ENTREGA_013BIS_ABERTURA_operador.md"),"rb").read()).hexdigest()
print("ABERTURA sha256",abertura_sha)
rows=[]
for f in notes:
    b=open(os.path.join(D,f),"rb").read(); t=b.decode("utf-8","replace")
    first=t.splitlines()[0] if t else ""
    r={"nota":f,"bytes":len(b),"sha16":hashlib.sha256(b).hexdigest()[:16],
       "estatuto_1a_linha":bool(re.match(r"^\s*\[(REAL|OPEN|DERIVED|KNOWN|INPUT|CONJECTURE|DECLARADO|ONTO|POSTULATE)",first)),
       "PAGO":len(re.findall(r"\bPAGO\b",t)),"NAO_PAGO":len(re.findall(r"N[ÃA]O PAGO",t)),
       "sha256_hex":len(re.findall(r"\b[0-9a-f]{64}\b",t)),
       "reproducao":bool(re.search(r"(?i)reprodu",t)),
       "nao_feito":bool(re.search(r"(?i)n[ãa]o (foi )?(feito|feita|realizad|executad|pago)|não se (fez|executou)|NÃO FEITO|not done|não realizou|não realizad",t)),
       "falhas_preservadas":bool(re.search(r"(?i)falh|abort|preservad|SIGSEGV|recusad",t)),
       "axiomas_NA":bool(re.search(r"(?i)axiomas?:?\s*N/A|N/A\s*[—-]\s*sem Lean|sem Lean",t)),
       "ficha_REAPROVEITAMENTO":bool(re.search(r"REAPROVEITAMENTO_",t)),
       "cita_sha_abertura":abertura_sha in t,
       "CONFIRMED":len(re.findall(r"\bCONFIRMED\b",t)),"PROVED":len(re.findall(r"\bPROVED\b",t)),
       "NAO_CEGO":len(re.findall(r"N[ÃA]O[- ]CEG",t)),
       "anos":[m.group(0) for m in re.finditer(r"[^\n]{0,60}\banos\b[^\n]{0,40}",t)][:6],
       "offset0":[m.group(0) for m in re.finditer(r"[^\n]{0,60}(offset|deslocamento)[^\n]{0,20}(fixo|fixed)[^\n]{0,30}",t)][:4],
       "beta_lit":len(re.findall(r"0\.0120|0\.01203|1\.2031",t)),
       "escolh":[m.group(0) for m in re.finditer(r"[^\n]{0,50}(escolh|prefer)[^\n]{0,60}",t)][:8],
       "first_line":first[:160]}
    rows.append(r)
json.dump(rows,open(sys.argv[1],"w",encoding="utf-8"),ensure_ascii=False,indent=1)
hdr=["nota","bytes","sha16","estatuto_1a_linha","PAGO","NAO_PAGO","sha256_hex","reproducao","nao_feito","falhas_preservadas","axiomas_NA","ficha_REAPROVEITAMENTO","cita_sha_abertura","CONFIRMED","PROVED","NAO_CEGO","beta_lit"]
print("\t".join(hdr))
for r in rows: print("\t".join(str(r[k]) for k in hdr))
print()
for r in rows:
    print("--",r["nota"]); print("  1a:",r["first_line"]); 
    if r["anos"]: print("  anos:",r["anos"])
    if r["offset0"]: print("  offset:",r["offset0"])
