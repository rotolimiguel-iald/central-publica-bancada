"""Isolated review guards and receipt expression only. Never run the launcher."""
import ast,copy,hashlib,json,sys,time
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;B=HERE.parents[1]
PRODUCER=B/'refeito/activate_kerr_013bis.py'
MANIFEST=B/'bis/e3_pyring_preparation/MANIFEST_v3.json'
REVIEW=HERE/'MANIFEST_V3_INDEPENDENT_RECEIPT.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,value):
    with p.open('x',encoding='utf-8',newline='\n') as f:
        f.write(value if isinstance(value,str) else json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    started=time.perf_counter();checks=[];negative_count=0
    out=HERE/'orchestrator_closing_001';out.mkdir()
    raw=PRODUCER.read_bytes();source_hash=sha(PRODUCER);review_hash=sha(REVIEW);manifest_hash=sha(MANIFEST)
    with (out/'activate_kerr_snapshot.py').open('xb') as f:f.write(raw)
    def check(name,condition,detail=None):
        if not condition:raise RuntimeError('FAILED '+name)
        checks.append(dict(name=name,passed=True,detail=detail))
    def reject(name,fn):
        nonlocal negative_count
        try:fn()
        except (ValueError,KeyError,TypeError,FileNotFoundError) as e:
            checks.append(dict(name=name,passed=True,refusal=type(e).__name__));negative_count+=1
        else:raise RuntimeError('NEGATIVE ACCEPTED '+name)
    tree=ast.parse(raw.decode('utf-8'))
    selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('strict_load','check_review')]
    check('only_two_pure_review_helpers_extracted',len(selected)==2)
    ns=dict(json=json,sha=sha)
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(out/'activate_kerr_snapshot.py'),'exec',optimize=1),ns)
    actual=ns['check_review'](REVIEW,MANIFEST,MANIFEST.name)
    check('immutable_real_V3_receipt_accepted',actual['manifest_sha256']==manifest_hash and actual['blocking_findings']==[])
    wrong_manifest=out/'different_manifest.json';save(wrong_manifest,dict(status='SYNTHETIC_OTHER_MANIFEST'))
    reject('valid_review_different_manifest_bytes',lambda:ns['check_review'](REVIEW,wrong_manifest,MANIFEST.name))
    reject('valid_review_wrong_manifest_name',lambda:ns['check_review'](REVIEW,MANIFEST,'MANIFEST_v2.json'))
    changes=[('nonclosing_status',{'status':'STATIC_REVIEW_ONLY'}),('old_status',{'status':'MANIFEST_V2_DOCUMENTARY_CHECKED_NOT_EXECUTION_AUTHORIZATION'}),
        ('open_blocker',{'blocking_findings':[{'id':'OPEN'}]}),('null_blockers',{'blocking_findings':None}),('object_blockers',{'blocking_findings':{}}),
        ('wrong_manifest_hash',{'manifest_sha256':'0'*64}),('wrong_manifest_filename',{'manifest_filename':'MANIFEST_v2.json'}),
        ('empty_checks',{'checks':[]}),('false_check',{'checks':[{'passed':False}]}),('one_bad_among_good',{'checks':[{'passed':True},{'passed':False}]}),
        ('truthy_integer_not_bool',{'checks':[{'passed':1}]}),('truthy_string_not_bool',{'checks':[{'passed':'true'}]}),
        ('missing_passed',{'checks':[{}]}),('null_checks',{'checks':None}),('checks_object',{'checks':{'passed':True}})]
    for name,patch in changes:
        p=out/(name+'.json');obj=copy.deepcopy(actual);obj.update(patch);save(p,obj)
        reject(name,lambda p=p:ns['check_review'](p,MANIFEST,MANIFEST.name))
    for name in ('status','blocking_findings','manifest_filename','manifest_sha256','checks'):
        obj=copy.deepcopy(actual);del obj[name];p=out/('missing_'+name+'.json');save(p,obj)
        reject('missing_'+name,lambda p=p:ns['check_review'](p,MANIFEST,MANIFEST.name))
    for name,text in [('duplicate_status','{"status":1,"status":2}'),('nested_duplicate','{"checks":[{"passed":true,"passed":false}]}'),
        ('nan','{"extra":NaN}'),('infinity','{"extra":Infinity}'),('negative_infinity','{"extra":-Infinity}'),('malformed','{')]:
        p=out/(name+'.json');save(p,text)
        reject(name,lambda p=p:ns['strict_load'](p))
    reject('missing_review_file',lambda:ns['check_review'](out/'absent.json',MANIFEST,MANIFEST.name))
    # Inspect the main AST; do not compile or call it.
    mainnode=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    calls=[n for n in ast.walk(mainnode) if isinstance(n,ast.Call)]
    review_call=next(n for n in calls if isinstance(n.func,ast.Name) and n.func.id=='check_review')
    publishes=[n for n in calls if isinstance(n.func,ast.Name) and n.func.id=='publish_new']
    registration=next(n for n in calls if isinstance(n.func,ast.Name) and n.func.id=='checked_registration')
    launches=[n for n in calls if isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='subprocess' and n.func.attr=='run']
    check('review_gate_before_authorization_and_launch',registration.lineno<review_call.lineno<min(n.lineno for n in publishes)<launches[0].lineno)
    check('one_controller_launch_no_outer_timeout',len(launches)==1 and not any(k.arg=='timeout' for k in launches[0].keywords))
    # Evaluate only the output-dictionary expression with synthetic log and hashes.
    assignment=next(n for n in mainnode.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='value' for t in n.targets))
    expr=compile(ast.Expression(assignment.value),'<outer_receipt_expression>','eval',optimize=1)
    class Log:
        def __init__(self,exists):self.present=exists
        def exists(self):return self.present
    class Clock:
        @staticmethod
        def perf_counter():return 12.
    for name,present,error,rc in [('missing_log',False,{'type':'PermissionError'},None),('child_failed',True,{'type':'ChildFailure'},3),('zero_exit',True,None,0)]:
        log=Log(present);hash_calls=[]
        def fake_sha(value):
            if value is log and not present:raise RuntimeError('Attempted to hash absent log')
            hash_calls.append('log' if value is log else 'authorization');return 'SYNTHETIC_HASH'
        fields=eval(expr,dict(error=error,rc=rc,command=['SYNTHETIC_NO_LAUNCH'],digest='MOCK',authpath='MOCK_AUTH',
            sha=fake_sha,log=log,time=Clock,start=10.,datetime=datetime,timezone=timezone))
        check(name+'_log_hash',fields['log_sha256']==('SYNTHETIC_HASH' if present else None))
        check(name+'_status',fields['status']==('EXECUTION_COMPLETED_REVIEW_PENDING' if error is None else 'EXECUTION_FAILED_OR_PARTIAL'))
        check(name+'_error_preserved',fields['error']==error)
        check(name+'_log_not_hashed_when_absent',hash_calls==(['authorization','log'] if present else ['authorization']))
    check('no_source_drift',sha(PRODUCER)==source_hash)
    check('V3_receipt_preserved',sha(REVIEW)==review_hash)
    check('manifest_preserved',sha(MANIFEST)==manifest_hash)
    r=dict(status='ORCHESTRATOR_R1_N1_CLOSED_STATIC_FINITE_NO_EXECUTION',created_utc=datetime.now(timezone.utc).isoformat(),
        orchestrator_relative_to_Chatgpt=PRODUCER.relative_to(B.parent).as_posix(),orchestrator_sha256=source_hash,
        manifest_filename=MANIFEST.name,manifest_sha256=manifest_hash,independent_V3_receipt_filename=REVIEW.name,independent_V3_receipt_sha256=review_hash,
        closed_findings=['ORCH-R1','ORCH-N1'],blocking_findings=[],checks=checks,checks_count=len(checks),negative_count=negative_count,
        python_optimize=sys.flags.optimize,script_sha256=sha(__file__),wall_seconds=time.perf_counter()-started,
        scope='Only strict_load/check_review and synthetic receipt dictionary evaluated; main not compiled or run',
        launched_processes=0,authorization_created=False,activation_created=False,physical_waveforms=0,strain_values_read=0,PE_runs=0,
        boundaries=['Not native ACL/sealer or candidate003 chronology review','Not B2/F0-stop certification','No outer timeout added; controller retains two-hour deadline/cleanup','Zero controller exit still requires every variant/convergence review','E3.1 remains unpaid; exact source/PSD/strain identity OPEN','No judgment on E4 execution or W review'])
    target=HERE/'ORCHESTRATOR_R1_N1_CLOSING_RECEIPT.json';save(target,r)
    report=f'''# Fechamento independente ORCH-R1 / ORCH-N1

[REAL — delta estático e fixtures finitos; nenhuma execução do launcher]

{r['created_utc']}

**ORCH-R1 e ORCH-N1 fechados no escopo exercitado; sem bloqueante residual desses achados.** {len(checks)} verificações sob `-O`, incluindo {negative_count} recusas esperadas.

Orquestrador `refeito/activate_kerr_013bis.py`: `{source_hash}`. Manifesto vinculado: MANIFEST_v3.json, `{manifest_hash}`. Recibo independente imutável aceito semanticamente: MANIFEST_V3_INDEPENDENT_RECEIPT.json, `{review_hash}`. Os três hashes foram conferidos novamente ao terminar. O recibo V3 permanece byte-idêntico; seu achado histórico sobre o orquestrador anterior é encerrado por este documento ao lado.

**R1:** check_review carrega JSON, exige o status exato V3_DOCUMENTARY_DELTA_CLOSED_NO_EXECUTION_AUTHORIZATION, blocking_findings vazio, nome/hash do manifesto iguais ao selecionado, checks não vazios e cada passed exatamente True. A validação ocorre antes de publicar autorização ou lançar processo. O recibo V3 real passa. Pareamento com manifesto diferente, status antigo/não conclusivo, bloqueantes, campos ausentes, checks vazios/falsos/truthy não booleanos e arquivo ausente recusam. strict_load recusa chaves duplicadas, inclusive aninhadas, NaN, Infinity, -Infinity e JSON malformado. Não se testou um esquema genérico adicional: o fechamento refere-se aos campos operacionais usados.

**N1:** a expressão do recibo externo foi avaliada isoladamente com log ausente e erro artificial: log_sha256=null, erro preservado e EXECUTION_FAILED_OR_PARTIAL; não chama sha no log ausente. Também conferidos log presente com retorno3 e retorno0; este último permanece EXECUTION_COMPLETED_REVIEW_PENDING. Não se abriu log real, não se chamou Popen/run nem se executou main.

Há uma única chamada estática ao controller, sem timeout externo concorrente. O controller revisado conserva prazo/cleanup. E2/B2/F0 permanecem requisitos de execução do principal; a presença dos guards não certifica que esses atos já ocorreram. Este recibo não autoriza executar nem aprova ACL nativa/selagem/cronologia candidate003.

Nenhuma fonte produtora/congelada ou manifesto foi alterado. As fixtures novas estão em orchestrator_closing_001; script reprodutível close_orchestrator_r1_n1.py, que recusa sobrescrever o diretório existente. Parede dos controles {r['wall_seconds']:.6f}s. E4 e a revisão W ficam fora deste parecer.

**PAGO:** correções de vinculação do parecer e registro de falha do orquestrador, no alcance estático/finito. **NÃO PAGO:** execução/aceitação E3.1 e equivalência exata de GWOSC/C00_AR, PSDs e versão executável. Um retorno0 não aceita PE: continuam obrigatórios os resultados de cada variante e a convergência. Identidade não demonstrada permanece OPEN.

Recibo de fechamento: ORCHESTRATOR_R1_N1_CLOSING_RECEIPT.json, SHA256 `{sha(target)}`.
'''
    save(HERE/'ORCHESTRATOR_R1_N1_CLOSING_REVIEW.md',report)
    print(json.dumps(dict(status=r['status'],checks=len(checks),negative_count=negative_count,orchestrator_sha256=source_hash,receipt_sha256=sha(target))))

if __name__=='__main__':main()
