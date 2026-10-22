from pathlib import Path
import datetime, hashlib, json, os, sys
root=Path(r"C:\IALD\Central de Patentes")
base=root/"Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019"
f7=base/"F7.2/MEMORY_CORRECTIONS_RECEIPT_F72_20261008.json"
f13=base/"F1.3/MEMORY_V3_2_RECEIPT_20261008.json"
audit=Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.6.E1\AUDITORIA_F3_6_E1_C1_a4f6da3d.md")
out=base/"F0.3/ERRATA_ESCRITAS_MEMORIA_SEM_REIVINDICACAO_20261008.json"
claim=int(sys.argv[1])
sha=lambda b:hashlib.sha256(b).hexdigest()
receipts=[json.loads(p.read_text(encoding="utf-8")) for p in (f7,f13)]
assert all(len(r["rows"])==4 for r in receipts)
assert not out.exists()
targets=[root/"memory/TGL_ATLAS.md",root/"memory/TGL_INDICE_VIVO.md",root/"memory/TGL_CORE_MEMORY.md",base/"AVISO_GERENCIA.md"]
marker=b"<!-- F03_ERRATA_ESCRITAS_0838_0859_SEM_REIVINDICACAO_20261008 -->"
before={p:p.read_bytes() for p in targets}
for p,b in before.items():
 a,c=(next(x for x in r["rows"] if x["path"]==str(p)) for r in receipts)
 assert a["after_sha256"]==c["before_sha256"],p
 assert sha(Path(a["backup"]).read_bytes())==a["before_sha256"],p
 assert sha(Path(c["backup"]).read_bytes())==c["before_sha256"],p
 assert b.startswith(Path(c["backup"]).read_bytes()),p
 assert marker not in b,p
text=("\n\n## 08/10/2026 — errata de processo: escritas de memória sem reivindicação\n\n"
"<!-- F03_ERRATA_ESCRITAS_0838_0859_SEM_REIVINDICACAO_20261008 -->\n\n"
"[REAL — em nome de codex-gerente-tgl] Às 08:38 (F7.2) e 08:59 (F1.3), hora local de 08/10, foram acrescentados textos ao Atlas, índice vivo, TGL_CORE_MEMORY e AVISO_GERENCIA sem uma reivindicação vigente da unidade de memória F0.3. "
"A auditoria c1 "+str(audit)+" (SHA-256 "+sha(audit.read_bytes())+") verificou que não há reivindicação F0.3 entre os eventos 273 e 306. "
"Os recibos "+str(f7)+" (SHA-256 "+sha(f7.read_bytes())+") e "+str(f13)+" (SHA-256 "+sha(f13.read_bytes())+") registram as duas escritas e seus backups de bytes. "
"O backup e o acréscimo preservam a integridade, mas NÃO suprem a falta de reivindicação. A reivindicação 306 é posterior e não autoriza retroativamente essas escritas. "
"A reivindicação "+str(claim)+" cobre somente esta errata ao lado. As entregas F7.2 e F1.3 permanecem com seus estatutos de auditoria; nenhuma prova, dado de natureza ou gate é alterado por esta escrituração.\n").encode("utf-8")
stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
rows=[]
for p,b in before.items():
 bak=p.with_name(p.name+".bak_"+stamp)
 with bak.open("xb") as h: h.write(b);h.flush();os.fsync(h.fileno())
 assert bak.read_bytes()==b
 tmp=p.with_name(p.name+".tmp_"+os.urandom(4).hex())
 with tmp.open("xb") as h: h.write(b+text);h.flush();os.fsync(h.fileno())
 assert p.read_bytes()==b and tmp.read_bytes()==b+text
 os.replace(tmp,p)
 assert p.read_bytes()==b+text
 rows.append({"path":str(p),"backup":str(bak),"before_sha256":sha(b),"after_sha256":sha(b+text),"append_bytes":len(text)})
obj={"schema":"iald.f0_3.memory_unclaimed_writes_erratum.v1","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"claim_event":claim,"source_audit":{"path":str(audit),"sha256":sha(audit.read_bytes())},"source_receipts":[{"path":str(p),"sha256":sha(p.read_bytes())} for p in (f7,f13)],"original_writes_local":["2026-10-08 08:38 F7.2","2026-10-08 08:59 F1.3"],"no_retroactive_authorization":True,"targets":rows}
with out.open("xb") as h:h.write((json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"receipt":str(out),"sha256":sha(out.read_bytes()),"targets":len(rows)},ensure_ascii=False))