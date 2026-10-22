"""Reserve one independent review of the newly executed C3 package, not its old plan."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,uuid,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C4';Q=D/'orchestration'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,write,put,append
plan=json.loads((ROOT/'C3/PLAN.json').read_bytes());result=json.loads((ROOT/'C3/RESULTS.json').read_bytes());audits=json.loads((ROOT/'C3/AXIOM_AUDIT.json').read_bytes())
table=[]
for i,x in enumerate(plan['groups']):
    table.append(dict(source=x['source'],source_sha256=x['source_sha256'],copy=x['copy'],copy_sha256=x['copy_sha256'],
        body_sha256=x['body_sha256'],body_bytes_equal=x['body_bytes_equal'],changes=x['changes'],imports=x['imports'],
        rc=result['receipts'][i]['rc'],theorems=audits[i]['n_theorem_lemma_na_fonte'],audit=audits[i]['auditoria']))
summary=Q/'C3_VERIFIED_PROJECTION.json';put(summary,dict(groups=table,aggregate=dict(path=str(ROOT/'C3/package/IntegrationAudit.lean'),
    sha256=sha(ROOT/'C3/package/IntegrationAudit.lean'),rc=result['receipts'][-1]['rc'],unique_printed=130,audit=audits[-1]['auditoria']),
    theorem_count=127,body_changes=0,kernel_installed=False,gate_changed=False,origin_result_sha256=sha(ROOT/'C3/RESULTS.json')))
prompt='''ORDEM016,C3 entrega executada: crítica independente nova após o planoC25. Texto somente; memória científica comum, sem ferramentas, compilação ou alteração de gate. Pergunta única: a evidência abaixo sustenta exatamente "doze fontes coexistem, com só dois imports trocados e corpos preservados", e quais conclusões mais fortes NÃO seguem? Confira aliasT20/T20_v3, alcance do consumidor com prints, diferença 127teoremas/130declarações, e se FlowTendsToFamily ou outra condição foi disfarçada de provada. O pacote compilou em13processos seriais rc0/trio; não pedir lakebuild nem mudarcanônico. Proponha somente correção concreta se houver erro, não nova camada sem necessidade. Separar leitura preservada de leitor discriminante (injOn) e do vínculo físico Ward/BW. C25 era plano com projeções parciais; este pedido audita o RESULTADO compilado/relatório atual. Não afirmar leitura remota de arquivo local; hashes são os recebidos, não medidos por você.\n'''
sources=[(summary,None),(ROOT/'C3/RELATORIO.md',None),(ROOT/'C3/package/TheEquationOfTruth_T20_v3.lean',(290,330)),
    (ROOT/'C3/package/TheEquationOfTruth_T20_v3.lean',(641,667)),(ROOT/'C3/package/InscriptionBridge.lean',(1,40)),
    (ROOT/'C3/package/IntegrationAudit.lean',(1,16))]
refs=[]
for p,span in sources:
    lines=p.read_text('utf-8-sig').splitlines();inds=list(range(span[0]-1,min(span[1],len(lines)))) if span else list(range(len(lines)))
    ref=dict(path=str(p),sha256=sha(p),included_lines=[i+1 for i in inds]);refs.append(ref)
    prompt+='\nSOURCE '+json.dumps(ref,ensure_ascii=False)+'\n'+'\n'.join(f'{i+1}: {lines[i]}' for i in inds)+'\n'
assert len(prompt)<=20000,len(prompt)
rid=str(uuid.uuid4());ec=dict(mission_id='ORDEM_016',branch_id='C3-final-critique',lemma_id='executed_twelve_source_integration_scope',role='skeptic',required_provider='kimi',max_calls=1)
p=Q/'kimi_c3_final_submit.json';put(p,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=ec))
put(Q/(rid+'_origin.json'),dict(at=datetime.now(timezone.utc).isoformat(),thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,house='Central de Patentes',payload=str(p),payload_sha256=sha(p),sources=refs,status='PREPARED_NOT_SUBMITTED'))
v=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=ec)),text=True,encoding='utf-8',capture_output=True,cwd=BASE)
resp=json.loads(v.stdout);put(Q/(rid+'_preview.json'),dict(returncode=v.returncode,response=resp));assert v.returncode==0 and resp.get('selected')=='kimi'
row=dict(provider='kimi',request_id=rid,payload=str(p),payload_sha256=sha(p),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),preview=str(Q/(rid+'_preview.json')),sources=refs,status='PREPARED_NOT_SUBMITTED_COORDINATOR_OWNS_TRANSITIONS')
put(Q/'c3_final_unit.json',row)
append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),event='C3_FINAL_SKEPTIC_PREPARED',remote_call=False,**row))+'\n')
print(json.dumps(dict(request_id=rid,prompt_chars=len(prompt),catalog=str(Q/'c3_final_unit.json'))))
