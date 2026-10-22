import os,re,glob,json
d=r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT"
fs=sorted([f for f in glob.glob(os.path.join(d,"ENTREGA_013_*.md")) if "ESPONTANEA" not in f], key=os.path.getmtime)
status_re=re.compile(r'^\s*\[(REAL|DERIVED|OPEN|KNOWN|INPUT|CONJECTURE|ONTO|DECLARADO|POSTULATE)')
rows=[]
for f in fs:
    t=open(f,encoding='utf-8',errors='replace').read()
    lines=t.splitlines()
    first=lines[0] if lines else ''
    r=dict(file=os.path.basename(f),
      L1_status=bool(status_re.match(first)),
      PAGO=bool(re.search(r'\bPAGO\b|\bPAGA\b|\bPAGOS\b',t)),
      NAO_PAGO=bool(re.search(r'N[ÃA]O PAG',t)),
      sha256=len(re.findall(r'\b[0-9a-f]{64}\b',t)),
      reproducao=bool(re.search(r'(?i)reprodu|python |wsl\.exe|comando',t)),
      nao_feito=bool(re.search(r'(?i)n[ãa]o (foi )?feito|n[ãa]o pago|ainda falta|pend[êe]nc|n[ãa]o fe[zi]|OPEN',t)),
      falhas=bool(re.search(r'(?i)falh|bak_|defeito|recusad',t)),
      axiomas=bool(re.search(r'(?i)axiom|sem Lean|Lean',t)),
      aproveitamento=bool(re.search(r'(?i)aproveitamento|REAPROVEITAMENTO',t)),
      forbidden=[m for m in re.findall(r'CONFIRMED|PROVED|CONFIRMAD[OA]|PROVAD[OA]',t)],
      M1_mention=bool(re.search(r'\bM1\b',t)))
    rows.append(r)
keys=['L1_status','PAGO','NAO_PAGO','sha256','reproducao','nao_feito','falhas','axiomas','aproveitamento']
print("file".ljust(62)," ".join(k[:6] for k in keys),"forbidden")
for r in rows:
    print(r['file'][:62].ljust(62)," ".join(str(r[k])[:6].ljust(6) for k in keys), r['forbidden'])
print("totals:",{k:sum(1 for r in rows if (r[k] if not isinstance(r[k],int) or isinstance(r[k],bool) else r[k]>0)) for k in keys}, "of",len(rows))
json.dump(rows,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'contract.json'),'w'),indent=1)
# REAPROVEITAMENTO files
import glob as g
print("REAPROVEITAMENTO files:", g.glob(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\**\REAPROVEITAMENTO*",recursive=False), g.glob(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\REAPROVEITAMENTO*"))
