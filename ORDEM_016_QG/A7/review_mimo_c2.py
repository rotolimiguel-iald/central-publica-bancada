"""Reproduce a mutation-test sensitivity gap without compiling or altering Lean."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json,uuid,importlib.util
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
A6=ROOT/'A6_EQUACAO_DA_VERDADE';OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
DEST=A6/'received_reviews/mimo_c2_local';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,raw):
    if isinstance(raw,str):raw=raw.encode()
    if p.exists():
        old=p.read_bytes()
        if old==raw:return
        b=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw;t.replace(p)
def new(p,obj):
    assert not p.exists(),str(p)
    save(p,json.dumps(obj,ensure_ascii=False,indent=2))
auditpath=ROOT/'A0/auditar_axiomas.py'
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),auditor_sha256=sha(auditpath),
    target='Reproduce P1 sensitivity, isolated synthetic coverage test, and lexical P9',
    no_Lean_execution=True,no_changes_to_prior_artifacts=True))
start,cpu=perf_counter(),process_time();checks=[]
def check(name,value):assert value,name;checks.append(name)
spec=importlib.util.spec_from_file_location('audit_c2_local',auditpath)
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
m=A6/'C_controles/mutations/M7b'
receipt=json.loads((m/'mutation_M7b.json').read_bytes())
source=m/'TheEquationOfTruthM7b.lean';log=m/'mutation_M7b.log'
check('actual_M7b_custody',sha(source)==receipt['source_sha256'] and sha(log)==receipt['log_sha256'])
original=audit.audita(str(source),str(log))
line='    if sem_print: motivos.append("cobertura: theorem/lemma sem #print axioms")'
txt=auditpath.read_text('utf-8-sig');check('single_mutation_anchor',txt.count(line)==1)
mutated=txt.replace(line,'    # TEST MUTATION: coverage rejection deliberately disabled')
save(DEST/'auditor_without_coverage.py',mutated)
ns={'__name__':'audit_c2_synthetic'}
exec(compile(mutated,str(DEST/'auditor_without_coverage.py'),'exec'),ns)
changed=ns['audita'](str(source),str(log))
def old_detect(a):return receipt['rc']==0 and a['auditoria']=='FALHA' and bool(a['sem_print_axioms']) and 'axiom' in a['tokens_proibidos_na_fonte']
check('M7b_old_test_accepts_both_auditors',old_detect(original) and old_detect(changed))
check('coverage_reason_really_removed','cobertura: theorem/lemma sem #print axioms' not in changed['motivos'])
# Explicit synthetic parser fixtures, NOT compiler outputs or a purported proof.
fixture=DEST/'SYNTHETIC_INPUT_NOT_COMPILED.lean'
flog=DEST/'SYNTHETIC_LOG_NOT_COMPILER_OUTPUT.txt'
save(fixture,'theorem covered : True := True.intro\ntheorem missing : True := True.intro\n')
save(flog,"'covered' does not depend on any axioms\n")
isolated=audit.audita(str(fixture),str(flog));escape=ns['audita'](str(fixture),str(flog))
check('isolated_coverage_rule',isolated['motivos']==['cobertura: theorem/lemma sem #print axioms'])
check('isolated_fixture_kills_regression',isolated['auditoria']=='FALHA' and escape['auditoria']=='PASSA')
# P9 is a lexical counterexample, not evidence that current certified source contains it.
char_source="def quote : Char := '\"'\ntheorem hidden : True := True.intro\n"
names,private=audit.decls_da_fonte(audit.sem_comentarios(char_source))
check('Char_literal_hides_following_declaration','hidden' not in names)
base=A6/'A_reproducao';bsource=base/'TheEquationOfTruth.lean';blog=base/'equation_reproduction_01.log'
br=json.loads((base/'equation_reproduction_01.json').read_bytes())
check('actual_baseline_custody',sha(bsource)==br['source_sha256'] and sha(blog)==br['log_sha256'])
ba=audit.audita(str(bsource),str(blog))
check('baseline_is_available_and_passes',br['rc']==0 and ba['auditoria']=='PASSA')
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
res=dict(at=now.isoformat(),statute='REAL_LOCAL_AUDIT_REGRESSION_REPRODUCED_NOT_NEW_LEAN_PROOF',
    checks=checks,checks_passed=len(checks),original_M7b=original['motivos'],
    mutated_M7b=changed['motivos'],isolated_original=isolated['auditoria'],
    isolated_mutant=escape['auditoria'],baseline_declarations=ba['n_declaracoes_auditadas'],
    no_compilation=True,gate_changed=False,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',res)
report=f'''[REAL — reprodução local da lacuna de sensibilidade; DECLARADO — demais alegações ainda não verificadas]
# Revisão da auditoria MiMo C2

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.
Resposta integral recuperada/lida: job99bbefc3-504b-4c4c-a361-80efb8ba1e42,
execução53c5da1f-ae98-4bef-8443-bae946b56c43. Nenhuma nova chamada de modelo.

P1 reproduzido: removendo SOMENTE a regra que recusa theorem sem print no
auditor COPIADO, M7b continua detected=true. Ele também contém axiom, portanto
a outra recusa mascara a regressão de cobertura. O M7b real segue rejeitado;
o achado é uma lacuna do teste, não aceitação da pedra adulterada pelo auditor atual.

Acrescentamos um teste isolado do parser com fonte e log explicitamente
SINTÉTICOS, não compilados: um theorem coberto e outro sem print, sem axiom.
O auditor atual recusa somente pela cobertura; a cópia regredida aceita.
Esse controle mata a regressão que o antigo M7b não distinguia. Não substitui
nem modifica a rodada Lean de oito mutantes anteriormente custodiada.

P9 reproduzido lexicalmente: Char com aspas duplas faz o removedor de strings
esconder a declaração subsequente. Isso não prova presença desse padrão na
pedra certificada. Fica limitação nomeada do parser para fontes arbitrárias.

P4 qualificado: o baseline existe na entrega A_reproducao; seus hashes fonte/log
foram reconferidos e a auditoria atual passou{ba['n_declaracoes_auditadas']}declarações.
A ausência de baseline dentro do laço C2 não significa ausência da cadeia.
P7: o runner lido grava rc do Lean no recibo e retorna normalmente após gravar;
rc0 do wrapper não significa rc0 de Lean. Não houve repetição de compilação.
P3 permanece ressalva lógica correta: falha de um script de prova não demonstra
por si só necessidade matemática de uma hipótese em todo argumento possível.
P2/P5/P6 e alegações condicionais restantes não foram transformadas em defeitos
confirmados. O parecer trouxe11itens, não11falhas reproduzidas.

{len(checks)}checks locais, CPU{res['cpu_seconds']}s. Originais, kernel e gate
intactos. Fixtures e cópia regredida estão claramente rotulados e isolados.
'''
save(DEST/'REVISAO.md',report);save(OUT/'ENTREGA_016_A6_C2_revisao_MiMo.md',report)
files=[Path(__file__),auditpath,source,log,bsource,blog,DEST/'results.json',DEST/'REVISAO.md',
       DEST/'PRE_REGISTER.json',DEST/'auditor_without_coverage.py',fixture,flog]
new(DEST/'manifest.json',dict(opening_sha256=opening,
    artifacts=[dict(path=str(f),sha256=sha(f)) for f in files]))
ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes()
event=dict(event='A6_MIMO_C2_LOCAL_SENSITIVITY_REVIEW',at=now.isoformat(),provider='local',
    checks=len(checks),rc=0,cpu_seconds=res['cpu_seconds'],report_sha256=sha(DEST/'REVISAO.md'),
    original_gate_unchanged=True,new_external_execution=False)
save(ledger,raw+(json.dumps(event,ensure_ascii=False)+'\n').encode())
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now.isoformat(),mimo_c2_review=str(DEST/'REVISAO.md'),
    prepared_primitive_reviews_status='COORDINATOR_VERIFIED_STAGED_AFTER_MARKED_V2',
    scheduler_observed='5 pending/running jobs maximum;1 synchronous provider execution')
d['next']=[x for x in d['next'] if 'Recover and audit MiMo C2' not in x]
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps(res,ensure_ascii=False,indent=2))
