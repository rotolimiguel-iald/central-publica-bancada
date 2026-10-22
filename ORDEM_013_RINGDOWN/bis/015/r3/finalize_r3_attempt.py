import json, hashlib, copy
from pathlib import Path
from datetime import datetime, timezone

b=Path(r"C:\IALD\Central de Patentes\Chatgpt")
root=b/"ORDEM_013_RINGDOWN"; d=root/"bis/015/r3"; out=b/"TUNEL/DO_CHATGPT"
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def put(p, obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode() if isinstance(obj,dict) else obj.encode()
    with p.open("xb") as f:f.write(data)
    assert p.stat().st_size==len(data)
start=json.loads((d/"R3_START.json").read_text(encoding="utf-8"))
oldp=root/"ORCAMENTO_015_v7.json"; old=json.loads(oldp.read_text(encoding="utf-8"))
assert sha(oldp)=="c05fc514e6183ced70a30c43599d3b51ca5d25791f5a97befcfc9012631b0d4b"
src=root/"cache/R3_LAL_SOURCE_015/lalsimulation/lib/LALSimIMRSpinAlignedEOB.c"
assert sha(src)==start["local_source_sha256"]
now=datetime.now(timezone.utc); spent=(now-datetime.fromisoformat(start["started_utc"])).total_seconds()/3600
assert 0<spent<2
r={"status":"R3_MEDIDA_NOT_QUALIFIED_MISSING_LOCAL_BUILD_PREREQUISITES","started_utc":start["started_utc"],"closed_utc":now.isoformat(),"charged_machine_hours_conservative_upper_bound":spent,"accounting_note":"Charges whole start-to-close wall including local analysis, conservatively.","source_commit_verified":start["source_commit"],"source_file_sha256_verified":sha(src),"clone_returncode":0,"bootstrap_command":"./00boot in pinned source copy","bootstrap_returncode":1,"bootstrap_output":"00boot: running autoreconf\n./00boot: 28: autoreconf: not found\n!!! ./00boot: autoreconf failed","missing_local_tools":["autoreconf","autoconf","automake","pkg-config","swig","gsl-config"],"patch_applied":False,"build_performed":False,"points_finite_checked":0,"points_required":122,"old_new_waveform_compared":False,"scientific_use_authorized":False,"gate_changed":False,"next_prescribed_target":"T07"}
rp=d/"R3_RESULT.json";put(rp,r)
opening=sha(out/"ENTREGA_016_ABERTURA_operador.md")
note=f"""[REAL — fonte pinada; MEDIDA — R3 não qualificado]

Abertura016SHA256: {opening}; ORDEM015 SHA256: {start['order_015_sha256']}; R3_START SHA256: {sha(d/'R3_START.json')}; R3_RESULT SHA256: {sha(rp)}.

A tag oficial lalsuite-v7.26.15 foi clonada em cópia própria; git rev-parse HEAD = {start['source_commit']}. O arquivo C copiado tem SHA256 {sha(src)}, idêntico ao pin instalado. Bootstrap `./00boot` terminou rc=1: `autoreconf: not found`. GCC/Make existem; autoreconf, autoconf, automake, pkg-config, swig e gsl-config não foram encontrados. Nenhum original da Física foi alterado.

Rascunho MiMo só com max_lm(dtau) foi rejeitado pelo contrato R3: a duração requer (1+dtau_lm)/Im omega_lm^GR e guardas de índice/overflow. Sem patch, build, 122 pontos ou comparação de ondas antiga/nova. Custo conservador início→fecho {spent:.6f} h de 2 h reservadas, incluindo análise local. R3 NÃO PAGO; nenhum uso científico, sigma ou gate. Próximo ramo T07.
"""
put(out/"ENTREGA_015_MEDIDA_patch_lal.md",note)
new=copy.deepcopy(old);new["registered_utc"]=now.isoformat();new["supersedes_sha256"]=sha(oldp);new["witness_relative_to_Chatgpt"]="TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v8.md"
for item in new["items"]:
    if item["item"]=="R3_LAL_patch":
        item.update(allocated_machine_hours=spent,actual_machine_hours=spent,status=r["status"],final_receipt_sha256=sha(rp))
    if item["item"]=="T10_calibration":item["allocated_machine_hours"]+=2-spent
new["allocated_machine_hours"]=sum(i["allocated_machine_hours"] for i in new["items"])
new["unallocated_machine_hours"]=new["authorized_machine_hours"]-new["allocated_machine_hours"]
assert abs(new["unallocated_machine_hours"])<1e-8
new["accounting"]["intervals"].append({"target":"R3_LAL_source_build_attempt","receipt_relative_to_Chatgpt":"ORDEM_013_RINGDOWN/bis/015/r3/R3_RESULT.json","sha256":sha(rp),"union_machine_hours":spent,"accounting_statute":"CONSERVATIVE_WALL_UPPER_BOUND"})
new["accounting"]["machine_hours_spent"]+=spent
new["reallocation_reason"]="R3 source pinned; bootstrap failed missing autoreconf; unused R3 allocation transferred to T10"
new["reallocation_changes"]={"R3_LAL_patch":{"old":2.0,"new":spent},"T10_calibration":{"old":next(i["allocated_machine_hours"] for i in old["items"] if i["item"]=="T10_calibration"),"new":next(i["allocated_machine_hours"] for i in new["items"] if i["item"]=="T10_calibration")}}
new["R3_attempt"].update(qualification_status=r["status"],result_sha256=sha(rp))
bp=root/"ORCAMENTO_015_v8.json";put(bp,new)
w=f"""[REAL] R3 fonte pinada; bootstrap rc=1; qualificação NÃO PAGA.

Abertura016SHA256: {opening}; pai v7 SHA256: {sha(oldp)}; R3_RESULT SHA256: {sha(rp)}; orçamento v8 SHA256: {sha(bp)}.

R3 cobrado conservadoramente {spent:.6f} h. Saldo {2-spent:.6f} h transferido a T10 antes de qualquer calibração. Total autorizado {new['authorized_machine_hours']:.9f} h; alocado {new['allocated_machine_hours']:.9f} h; gasto registrado {new['accounting']['machine_hours_spent']:.9f} h. Sem patch, build, 122 pontos, sigma ou gate. Próximo T07.
"""
put(out/"ENTREGA_015_ORCAMENTO_015_v8.md",w)
print(json.dumps({"result_sha256":sha(rp),"budget_sha256":sha(bp),"witness_sha256":sha(out/"ENTREGA_015_ORCAMENTO_015_v8.md"),"charged_hours":spent,"spent_total":new["accounting"]["machine_hours_spent"]}))

