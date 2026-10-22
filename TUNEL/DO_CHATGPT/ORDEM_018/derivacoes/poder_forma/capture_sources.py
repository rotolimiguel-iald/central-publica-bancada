"""Capture scientific covariance and redshift metadata; never parse observed means."""
from pathlib import Path
import datetime, hashlib, json, os, re, urllib.request
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,b):
 p=ROOT/name
 if isinstance(b,str): b=b.encode("utf-8")
 assert not p.exists(),str(p)
 t=p.with_name(p.name+".tmp");t.write_bytes(b)
 assert t.stat().st_size==len(b)
 os.replace(t,p);assert p.read_bytes()==b
def dump(name,obj):write(name,json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
records=[]
def capture(p):
 p=Path(p);b=p.read_bytes();r={"path":str(p),"bytes":len(b),"sha256":sha(b)}
 records.append(r);return b,r
receipt,rec=capture(BASE/"FONTES_PUBLICAS_ADICIONAIS.json")
data=json.loads(receipt)
for name,remote_name in [("Pantheon+SH0ES.dat","pantheon_table.txt"),("pantheon_covariance.dat","pantheon_cov.txt")]:
 b,r=capture(BASE/"reproducao_fase5"/name)
 primary=next(x for x in data if Path(x["path"]).name==remote_name)
 assert r["sha256"]==primary["sha256"]==primary["local_copy"]["sha256"]
 r["public_url"]=primary["url"];r["public_receipt_matches"]=True
 if name.endswith(".dat") and name.startswith("Pantheon"):
  rows=b.decode("utf-8").splitlines();header=rows[0].split()
  cols={k:header.index(k) for k in ["zHD","zHEL","IS_CALIBRATOR"]}
  metadata=[{k:float(v.split()[idx]) for k,idx in cols.items()} for v in rows[1:] if v.strip()]
  dump("pantheon_metadata_only.json",metadata)
 else:write("pantheon_STAT_SYS.cov",b)
desi=Path("C:/IALD/Artigo/teste_acustico_beta_tgl_v1/_originais")
b,r=capture(desi/"desi_gaussian_bao_ALL_GCcomb_mean.txt")
metadata=[]
for line in b.decode("utf-8").splitlines():
 if not line.strip() or line.lstrip().startswith("#"):continue
 parts=line.split();assert len(parts)==3
 metadata.append({"z":float(parts[0]),"type":parts[2]})
dump("desi_metadata_only.json",metadata)
b,r=capture(desi/"desi_gaussian_bao_ALL_GCcomb_cov.txt")
url="https://raw.githubusercontent.com/CobayaSampler/bao_data/refs/heads/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"
with urllib.request.urlopen(url,timeout=45) as response:
 public=response.read();final_url=response.url
r["public_url"]=url;r["public_final_url"]=final_url;r["public_sha256"]=sha(public)
r["public_bytes"]=len(public);r["public_bytes_match"]=public==b
assert public==b,"DESI covariance differs from current public release; no switch allowed"
write("desi_DR2.cov",b)
canonical=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py")
b,r=capture(canonical)
m=re.search(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)",b.decode("utf-8"),re.M)
assert m
dump("alpha_source.json",{"source":r,"line_number":b.decode("utf-8")[:m.start()].count("\n")+1,
 "declaration":m.group(0),"alpha":float(m.group(1)),"action":"read only, no import"})
dump("FONTES_COVARIANCIAS_METADATA.json",{
 "at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "status":"REAL_BYTES_VERIFIED__ONLY_METADATA_PARSED",
 "sources":records,"sn_parsed_columns":["zHD","zHEL","IS_CALIBRATOR"],
 "bao_parsed_columns":[0,2],"observed_central_values_parsed":False,
 "plan_sha256":sha((ROOT/"PLANO_ANTES_DO_PODER.md").read_bytes()),
 "runtime":"Python314 normal user; sandbox package discovery unavailable, no installs"})
print(json.dumps({"pantheon_rows":len(json.loads((ROOT/"pantheon_metadata_only.json").read_text())),"desi_rows":len(metadata),
 "covariance_identity":"Both official byte matches verified","alpha_decl":m.group(0)},ensure_ascii=False))
