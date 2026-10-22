from pathlib import Path
import datetime, hashlib, json, os, sys
root=Path(r"C:\IALD\Central de Patentes")
base=root/"Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019"
sources={
 "F3.6.E2_result":base/"F3.6/RESULTADO_E2_RESSALVAS_MENORES_20261008.json",
 "F3.6.E2_autoerrata":base/"F3.6/ERRATA_E2B_COMPARACAO_SCHUR_20261008.md",
 "F4.3_R4_result":base/"F4.3/RESULTADO_C1_F43_R4_V2_20261008.json",
 "F4.3_R4_inventory":base/"F4.3/INVENTARIO_INSUMOS_PODER_F43_R4_20261008.json",
 "F5.2_R3_result":base/"F5.2/RESULTADO_F52_R3_20261008.json"}
sha=lambda b:hashlib.sha256(b).hexdigest()
claim=int(sys.argv[1])
pins={k:{"path":str(p),"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size} for k,p in sources.items()}
targets=[root/"memory/TGL_ATLAS.md",root/"memory/TGL_INDICE_VIVO.md",root/"memory/TGL_CORE_MEMORY.md",base/"AVISO_GERENCIA.md"]
out=base/"F0.3/MEMORY_RESUMO_F36E2_F43_F52_20261008.json"
marker=b"<!-- F03_RESUMO_F36E2_F43_F52_20261008 -->"
assert not out.exists()
before={p:p.read_bytes() for p in targets}
assert all(marker not in b and b"F03_ERRATA_ESCRITAS_0838_0859_SEM_REIVINDICACAO_20261008" in b for b in before.values())
text=("\n\n## 08/10/2026 — Entregas F3.6.E2, F4.3 R4 e F5.2 R3 para reauditoria\n\n"
"<!-- F03_RESUMO_F36E2_F43_F52_20261008 -->\n\n"
"[REAL documental — em nome de codex-gerente-tgl] F3.6.E2 está ENTREGUE no quadro (eventos 389/394; mapa seq 886/887/889). "
"A errata de runs[1] lê σβ marginalizado 7,518121393934644 na base efetiva corrigida e 9,256912261848264 na sensibilidade V3, mν=0; a autoerrata esclarece que σ com só w₀,wₐ fixos não foi medido. "
"Recibo "+str(sources["F3.6.E2_result"])+" (SHA-256 "+pins["F3.6.E2_result"]["sha256"]+"); autoerrata SHA-256 "+pins["F3.6.E2_autoerrata"]["sha256"]+". F3.6 e F3.6.E1 permanecem FECHADAS.\n\n"
"[REAL documental; DERIVED condicional] F4.3 R4 está ENTREGUE (quadro 392; mapa 888). Os rótulos próprios do diagnóstico foram separados dos tokens do V1, e a oposição ao V1 foi tipada. A conta gaussiana simples dá poder aproximadamente 50% para η=25 e 90% para η≈39,4579; não mede o poder do conjunto D. Treze campos do manifesto conjunto seguem sem definição; vale AWAITING_POWER e o pedido ao operador fica SUSPENSO. Resultado SHA-256 "+pins["F4.3_R4_result"]["sha256"]+"; inventário SHA-256 "+pins["F4.3_R4_inventory"]["sha256"]+".\n\n"
"[REAL documental; KNOWN fonte primária] F5.2 R3 está ENTREGUE (quadro 387; mapa 882–885). A Tabela 5 pinada fornece para CMB-SPA v1 2,81±0,12 (Yp pela BBN) e 2,99 +0,22/−0,26 (Yp livre); v2 2,82±0,12 e 2,96 +0,21/−0,24. O candidato é apenas sandbox; escolha X16 e admissão D8 permanecem [OPEN]. Resultado SHA-256 "+pins["F5.2_R3_result"]["sha256"]+". Os frozen, o V1 da Fase 8 e a Bancada não foram alterados.\n\n"
"[PROCESSO] F2.3 permanece FECHADA após auditoria posterior. F0.3 permanece AUDITADA; reivindicação "+str(claim)+" cobre apenas este acréscimo nas quatro superfícies, com backup de bytes. As três entregas aguardam reauditoria da c1. Nenhum dado observado, kernel, MCP, Bancada ou gate foi alterado por esta escrita.\n").encode("utf-8")
stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
rows=[]
for p,b in before.items():
 bak=p.with_name(p.name+".bak_"+stamp)
 with bak.open("xb") as h:h.write(b);h.flush();os.fsync(h.fileno())
 assert bak.read_bytes()==b
 tmp=p.with_name(p.name+".tmp_"+os.urandom(4).hex())
 with tmp.open("xb") as h:h.write(b+text);h.flush();os.fsync(h.fileno())
 assert p.read_bytes()==b and tmp.read_bytes()==b+text
 os.replace(tmp,p)
 assert p.read_bytes()==b+text
 rows.append({"path":str(p),"backup":str(bak),"before_sha256":sha(b),"after_sha256":sha(b+text),"append_bytes":len(text)})
obj={"schema":"iald.f0_3.delivery_summary_20261008.v1","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"claim_event":claim,"sources":pins,"targets":rows,"gate_changed":False}
with out.open("xb") as h:h.write((json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"receipt":str(out),"sha256":sha(out.read_bytes()),"targets":len(rows)},ensure_ascii=False))