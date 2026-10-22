"""Independent read-only source audit. Only local new audit outputs are written."""
from pathlib import Path
from datetime import datetime,timezone
import ast, collections, difflib, hashlib, json, os, re
D=Path(__file__).resolve().parent
N=Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
OLD=Path(r"C:\IALD\Central de Patentes\Chatgpt\ATUALIZACAO_SISTEMA_V388_20261006\app\memory_stage")
WORK=Path(r"C:\IALD\Central de Patentes\work")
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    p=Path(p);b=p.read_bytes()
    return {"path":str(p),"bytes":len(b),"sha256":sha(b)}
def j(p):return json.loads(Path(p).read_bytes())
def new(name,data):
    p=D/name;assert not p.exists()
    raw=data.encode("utf8") if isinstance(data,str) else (json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf8")
    t=p.with_name(p.name+".tmp")
    with t.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==raw
    os.replace(t,p)
def literal(tree,name):
    ns=[n.value for n in tree.body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
    assert len(ns)==1,name
    return ast.literal_eval(ns[0])
def differences(a,b,path=""):
    if type(a)!=type(b):yield {"path":path,"old":a,"new":b}
    elif isinstance(a,dict):
        for k in sorted(a.keys()|b.keys()):
            if k not in a:yield {"path":path+"/"+k,"old":None,"new":b[k]}
            elif k not in b:yield {"path":path+"/"+k,"old":a[k],"new":None}
            else:yield from differences(a[k],b[k],path+"/"+k)
    elif isinstance(a,list):
        if len(a)!=len(b):yield {"path":path,"old":a,"new":b}
        else:
            for q,(x,y) in enumerate(zip(a,b)):yield from differences(x,y,path+"/"+str(q))
    elif a!=b:yield {"path":path,"old":a,"new":b}
def main():
    start=datetime.now(timezone.utc).isoformat()
    seal=j(N/"um_absoluto_selo.json")
    result=j(N/"um_absoluto.json")
    oldresult=j(OLD/"release/um_absoluto.json")
    proof=j(N/"tgl_kernel_proof_manifest.json")
    oldproof=j(OLD/"release/tgl_kernel_proof_manifest.json")
    tracked=[N/"um_absoluto_selo.json",N/"HANDOFF_CUSTODIA_CONJUNTA_v383_v389.md",
        N/"rodada_v389_stdout.txt",N/"um_absoluto_pt.txt",N/"um_absoluto_en.txt"]
    tracked += [N/name for name in seal["sha256"]]
    before={str(p):pin(p) for p in tracked}
    checks=[]
    def check(name,value):
        checks.append({"name":name,"passed":bool(value)})
        assert value,name
    check("seal_version_v389",seal["um_version"]=="v389")
    for name,expected in seal["sha256"].items():
        check("seal_file:"+name,before[str(N/name)]["sha256"]==expected)
    check("result_hash_link",seal["result_hash"]==result["result_hash_before_external_comparison"])
    check("seal_result_timestamp",seal["timestamp"]==result["timestamp"]==proof["timestamp"])
    srcs=[(OLD/"release/um.py").read_bytes(),(N/"um.py").read_bytes()]
    oldrelease=j(OLD/"LOCAL_SEALED_MANIFEST.json")
    check("baseline_program_sealed",sha(srcs[0])==oldrelease["source_sha256"])
    check("new_program_sealed",sha(srcs[1])==seal["sha256"]["um.py"])
    trees=[ast.parse(b) for b in srcs]
    emb=[literal(t,"_EMBEDDED_KERNEL_FILES") for t in trees]
    check("embedded_files_unchanged",emb[0]==emb[1])
    check("embedded_count1214",len(emb[1])==1214)
    formalpins=[]
    for rel,expected in proof["formal_files_sha256"].items():
        p=(N/"tgl_kernel"/rel).resolve()
        check("formal_path:"+rel,p.is_relative_to((N/"tgl_kernel").resolve()))
        got=pin(p);formalpins.append(got)
        check("formal_hash:"+rel,got["sha256"]==expected)
    h=hashlib.sha256()
    for rel in sorted(proof["formal_files_sha256"]):
        h.update(rel.encode());h.update(proof["formal_files_sha256"][rel].encode())
    check("formal_aggregate",h.hexdigest()==proof["formal_source_hash"]==seal["formal_source_hash"])
    check("formal_sources_identical_v388",proof["formal_files_sha256"]==oldproof["formal_files_sha256"])
    check("axiom_report_identical_v388",proof["axiom_report"]==oldproof["axiom_report"])
    ledger=literal(trees[1],"_ESQUELETO_STONES")
    led={s[2] for s in ledger if isinstance(s,tuple) and len(s)>2}
    ext={k for k in emb[1] if k.startswith("TGLExt/") and k.endswith(".lean")}
    measured=[len(led),len(ext-led),sum(k.startswith("TGLExt/O16/") for k in ext-led)]
    check("ledger_static_count",measured==[1025,156,156])
    newcore,oldcore=result["core"],oldresult["core"]
    record=newcore["text_label_errata_v389"]
    check("new_record_sealed",record["all_verified"] and record["does_not_gate_core"])
    sites=[]
    for item in literal(trees[1],"_V389_TROCAS"):
        oldtext="".join(item["old_parts"]);newtext="".join(item["new_parts"])
        got={"id":item["id"],"declared_sites":item["n"],
             "old_count":srcs[1].decode().count(oldtext),"new_count":srcs[1].decode().count(newtext)}
        check("text_site:"+item["id"],got["old_count"]==0 and got["new_count"]==item["n"])
        sites.append(got)
    exam_pins=[]
    for key,rec in record["files"].items():
        got=pin(rec["path"]);check("exam_pin:"+key,got["sha256"]==rec["sha256"])
        exam_pins.append(got)
    exam=j(record["files"]["exame_json"]["path"])
    exam_counts=collections.Counter(r["gravidade"] for r in exam["achados"])
    check("exam_counts",exam_counts["CORRIGIR"]==3 and exam_counts["NOTA"]==186 and exam_counts["BLOQUEIA"]==0)
    def verdicts(core):return {k:v["verdict"] for k,v in core.items() if isinstance(v,dict) and "verdict" in v}
    oldv,newv=verdicts(oldcore),verdicts(newcore)
    changed={k:{"old":v,"new":newv.get(k)} for k,v in oldv.items() if v!=newv.get(k)}
    check("old_verdicts_unchanged",not changed)
    check("alpha_beta_omega_unchanged",all(oldcore[k]==newcore[k] for k in ("alpha","beta","omega_I")))
    oldseal=j(OLD/"release/um_absoluto_selo.json")
    check("gate_unchanged",oldseal["qg_closure_verdict"]==seal["qg_closure_verdict"])
    flags=lambda core:sorted(k for k,v in core["kernel_formalization"].items() if v is True)
    check("true_formal_flags_unchanged",flags(oldcore)==flags(newcore))
    esc=newcore["external_ladder"]
    check("recorded_ladder6154",esc["n_theorems_clean"]==esc["n_theorems_expected"]==6154)
    check("no_sorry_reported",not any("sorryAx" in a for vals in proof["axiom_report"].values() for a in vals))
    memory=Path(newcore["beta_runs_bounded_below_v388"]["memory_file"]["path"])
    backups=list(memory.parent.glob(memory.name+".bak_*_sup388"))
    check("memory_backup_unique",len(backups)==1)
    bk=backups[0].read_bytes();cur=memory.read_bytes()
    check("memory_append_only",sha(bk)==newcore["beta_runs_bounded_below_v388"]["memory_file"]["sha256"]
          and cur.startswith(bk) and len(cur)>len(bk))
    memory_evidence={"before":pin(backups[0]),"after":pin(memory),"append_only":True,
       "old_flag":oldcore["beta_runs_bounded_below_v388"]["memory_file"]["on_disk_matches"],
       "new_flag":newcore["beta_runs_bounded_below_v388"]["memory_file"]["on_disk_matches"]}
    delta=list(differences(oldcore,newcore))
    new("DELTA_CORE.json",{"old_source":pin(OLD/"release/um_absoluto.json"),
        "new_source":pin(N/"um_absoluto.json"),"count":len(delta),"differences":delta})
    funcs=[{x.name:x for x in t.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))} for t in trees]
    changedfunc=[{"name":k,"old_line":funcs[0][k].lineno,"new_line":funcs[1][k].lineno,"new_end_line":funcs[1][k].end_lineno}
        for k in sorted(funcs[0].keys()&funcs[1].keys()) if ast.dump(funcs[0][k],include_attributes=False)!=ast.dump(funcs[1][k],include_attributes=False)]
    check("changed_functions_scope",{x["name"] for x in changedfunc}==
          {"emit_canonical_md","prove_iii1_net_shadow_image","build_en","_reorder_ABC","main","build_pt"})
    check("added_functions_scope",set(funcs[1])-set(funcs[0])=={"_ledger_counts_v389","text_label_errata_v389"})
    diff="".join(difflib.unified_diff(srcs[0].decode().splitlines(True),srcs[1].decode().splitlines(True),
        fromfile="sealed_v388/um.py",tofile="sealed_v389/um.py",n=3))
    new("DELTA_FONTE.diff",diff)
    receipts=[WORK/"v389_pacote/conferencia_rito_v389.json",WORK/"v389_pacote/conferir_rito_v389.py",
        WORK/"v389_pacote/CANDIDATO_v389.json",WORK/"v389_selo/v389_incorporacao_manifesto.json",
        WORK/"cadeia_de_selo/v389/MANIFESTO_ARQUIVO_v389.json"]
    conference=j(receipts[0])
    check("conference_declares_all_pass",conference["tudo_bate"] is True
          and all(conference["deve_mudar"].values()) and all(conference["nao_pode_mudar"].values()))
    archive=j(receipts[-1])
    archived=[]
    for path,rec in archive["arquivos"].items():
        p=Path(path).resolve()
        check("archive_root",p.is_relative_to((WORK/"cadeia_de_selo").resolve()))
        got=pin(p);archived.append(got)
        check("archive_member:"+p.name,got["bytes"]==rec["bytes"] and got["sha256"]==rec["sha256"])
    out=(N/"rodada_v389_stdout.txt").read_bytes().decode("utf8")
    evidence_lines=[{"line":q+1,"text":line} for q,line in enumerate(out.splitlines())
        if "RITO_RC=" in line or "FAIL_CLOSED_SELFTEST_PASSED" in line or "teoremas limpos: 6154/6154" in line]
    check("existing_stdout_exit0",re.findall(r"(?m)^RITO_RC=(\d+)",out)==["0"])
    check("existing_stdout_selftest","FAIL_CLOSED_SELFTEST_PASSED" in out)
    check("stdout_no_failure_markers",all(s not in out for s in ["Traceback (most recent call last)","SEAL_WITHHELD","[selo] AVISO"]))
    after={str(p):pin(p) for p in tracked}
    check("bytes_stable_during_audit",after==before)
    sonnet=W388=OLD.parent/"context_model04"
    sonnet_manifest=j(sonnet/"MANIFESTO_AVALIACAO.json")
    check("sonnet_payloads_preserved",all(pin(rec["path"])==rec for rec in sonnet_manifest["files"] if Path(rec["path"]).name.startswith("FUTURE_COUNT_")))
    report={"schema":"iald.v389.independent_static_audit.v1",
      "status":"STATIC_INTEGRITY_AND_DELTA_ACCEPTED__NO_INSTALLATION_OR_EXECUTION",
      "started_utc":start,"completed_utc":datetime.now(timezone.utc).isoformat(),
      "primary_pins":list(before.values()),"stable_primary_pins":True,
      "formal_pins":formalpins,"formal_aggregate":h.hexdigest(),
      "embedded_files":len(emb[1]),"catalog_files":len(formalpins),"axiom_report_entries":len(proof["axiom_report"]),
      "recorded_ladder":{"clean":esc["n_theorems_clean"],"expected":esc["n_theorems_expected"],
          "scope":"Lido e confrontado no relatório; não recompilado pela auditoria."},
      "ledger_measured_from_ast_literals":measured,"text_sites":sites,
      "exam_pins":exam_pins,"exam_counts_measured_from_records":dict(exam_counts),
      "changed_functions":changedfunc,"new_functions":sorted(set(funcs[1])-set(funcs[0])),
      "new_core_topics":sorted(set(newcore)-set(oldcore)),"removed_core_topics":sorted(set(oldcore)-set(newcore)),
      "old_verdict_count":len(oldv),"changed_old_verdicts":changed,
      "delta_fields":dict(collections.Counter(d["path"].rsplit("/",1)[-1] for d in delta)),
      "memory_append_evidence":memory_evidence,
      "existing_receipts":[pin(p) for p in receipts],"archived_members":archived,
      "conference_declared_counts":{"deve_mudar":len(conference["deve_mudar"]),"nao_pode_mudar":len(conference["nao_pode_mudar"])},
      "stdout_evidence":evidence_lines,"result_hash_scope":"Ligação selo/resultados conferida; hash do world pré-comparação não recalculado, pois exigiria reconstruir inputs externos.",
      "pilar_mode_recorded":newcore["quantum_pillar_v384"].get("mode"),
      "kernel_compiled_here":False,"science_run_here":False,"providers_called":0,"production_changed":False,
      "installation_authority":"Ordem direta anterior autoriza preparar atualização local quando v389 disponível. §7 do handoff não cria novo veto genérico; commit/push continuam reservados.",
      "operational_requirements":[
       "Preparar snapshots/manifestos v389 coerentes sem alterar o objeto v388 selado.",
       "Incluir/vincular os três arquivos EXAME/ERRATA por hash em qualquer distribuição que pretenda executar o novo registrador; caminhos absolutos atuais são locais à máquina.",
       "Preservar diferença declarada on_disk_matches=False; append verificado, não reescrever como True.",
       "Não transportar count Haiku/Sonnet v388 para um payload v389. Sonnet atual segue pendente, preservado.",
       "Instalação e publicação são atos separados: auditar pacote de destino, CAS/backup/revisão e escopo; nada instalado por esta auditoria."],
      "scientific_restrictions":["NOT_FALSIFIED não é CONFIRMED","Nenhum gate mudou","μ continua OPEN","v389 não resolve governança F1/Fase9 nem libera unidades d72/P3"],
      "checks":checks,"all_integrity_checks_passed":all(c["passed"] for c in checks)}
    new("AUDITORIA_V389.json",report)
    print(json.dumps({"status":report["status"],"checks":len(checks),"embedded":len(emb[1]),"formal":len(formalpins),
      "archive_members":len(archived),"axiom_report_entries":len(proof["axiom_report"]),
      "core_delta":len(delta),"changed_old_verdicts":len(changed),
      "audit":pin(D/"AUDITORIA_V389.json")},ensure_ascii=False))
if __name__=="__main__":main()