from pathlib import Path
import hashlib, json, os, datetime, sys
root=Path(r"C:\IALD\Central de Patentes")
f72=root/"Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F7.2"
receipt=Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F7.2\RECIBO_RATIFICACAO_COPIA_R8_C1_20261008.json")
r=json.loads(receipt.read_text(encoding="utf-8"))
assert r["quem"]=="claude-c1" and r["n_arquivos"]==26 and "RATIFICACAO A POSTERIORI" in r["ato"]
claim=int(sys.argv[1])
marker=b"<!-- F72_R8_RATIFICADA_C1_ERRATA_20261008 -->"
sha=lambda b: hashlib.sha256(b).hexdigest()
rp=sha(receipt.read_bytes())
addition=("\n\n## 08/10/2026 — F7.2: ratificação da cópia R8 (errata ao lado)\n\n"
"<!-- F72_R8_RATIFICADA_C1_ERRATA_20261008 -->\n\n"
"[REAL — em nome de codex-gerente-tgl] A frase anterior segundo a qual a gerência ainda decidiria ratificar ou retirar a cópia R8 está SUPERADA. "
"A c1 RATIFICOU A POSTERIORI a cópia aditiva e inerte dos 26 arquivos em Bancada_Um/fontes_externas/F7.2, feita às 08:30:46 sem ato prévio. "
"Consta do evento 313, do despacho das 09:40 e do recibo da c1 "+str(receipt)+" (SHA-256 "+rp+"). "
"A auditoria c1 a91f9500 conferiu os 26 hashes. O desvio original permanece registrado; cada gravação futura na Bancada exige um evento c1 específico e nomeado. "
"O canal V3 segue em staging e não lê as cópias R8. F7.2 segue AUDITADA; nenhum gate se move. "
"A seq 850 do mapa recebe errata ao lado.\n").encode("utf-8")
targets=[root/"memory/TGL_ATLAS.md",root/"memory/TGL_INDICE_VIVO.md",root/"memory/TGL_CORE_MEMORY.md",root/"Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md"]
out=f72/"MEMORY_ERRATA_R8_RATIFICADA_F72_20261008.json"
assert not out.exists()
old={p:p.read_bytes() for p in targets}
assert all(marker not in b and b"F72_C1_REAUDIT_ERRATA_20261008" in b for b in old.values())
stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
rows=[]
for p,b in old.items():
 bak=p.with_name(p.name+".bak_"+stamp)
 with bak.open("xb") as h:
  h.write(b);h.flush();os.fsync(h.fileno())
 assert bak.read_bytes()==b
 tmp=p.with_name(p.name+".tmp_"+os.urandom(4).hex())
 with tmp.open("xb") as h:
  h.write(b+addition);h.flush();os.fsync(h.fileno())
 assert p.read_bytes()==b and tmp.read_bytes()==b+addition
 os.replace(tmp,p)
 assert p.read_bytes()==b+addition
 rows.append({"path":str(p),"backup":str(bak),"before_sha256":sha(b),"after_sha256":sha(b+addition),"append_bytes":len(addition)})
obj={"schema":"iald.f7_2.r8_ratification_memory_erratum.v1","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"claim_event":claim,"ratification":{"path":str(receipt),"sha256":rp},"targets":rows}
with out.open("xb") as h: h.write((json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"receipt":str(out),"sha256":sha(out.read_bytes()),"targets":len(rows)},ensure_ascii=False))