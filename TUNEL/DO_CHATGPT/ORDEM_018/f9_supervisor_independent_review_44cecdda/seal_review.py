"""Assemble this static-review receipt from checked source bytes; no candidate imports."""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
TARGET=BASE/'f9_supervisor_preparation'

def pin(path):
    path=Path(path).resolve(); raw=path.read_bytes()
    return {'path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def write(name,doc):
    path=HERE/name
    raw=(json.dumps(doc,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    if path.exists():
        old=path.read_bytes(); backup=path.with_name(path.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    temp=path.with_name(path.name+'.tmp')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==raw and raw
    os.replace(temp,path);assert path.read_bytes()==raw

def anchor(name,start,end):
    path=TARGET/name
    if not path.exists():path=BASE/name
    record=pin(path);lines=path.read_text(encoding='utf-8').splitlines()
    assert 1<=start<=end<=len(lines)
    return {'source':record,'first_line':start,'last_line':end,'text':'\n'.join(lines[start-1:end])}

def main():
    identity=json.loads((HERE/'IDENTIDADE_REVISAO.json').read_bytes())
    static=json.loads((HERE/'VERIFICACOES_ESTATICAS.json').read_bytes())
    assert static['request_id']==identity['request_id']
    for group in static['inventory'].values():
        for rec in group:assert pin(rec['path'])==rec
    assert pin(static['candidate_manifest']['path'])==static['candidate_manifest']
    findings=[
      ('R1',1,'DECLARED_INTEGRATION_GAP','Bootstrap e supervisor científico concretos ausentes',[
          ('process_supervisor.py',47,50),('process_supervisor.py',144,148),('supervisor_adapter.py',29,54),('supervisor_port_cooperative_proposal.py',15,42)]),
      ('R2',1,'DECLARED_INTEGRATION_GAP','Política atual recusa operações necessárias do store I02',[
          ('cooperative_policy.py',23,50),('f9_node_preflight_repair_preparation/durable_nodes.py',53,97),('f9_controller_preparation/controller.py',249,259)]),
      ('R3',1,'DECLARED_INTEGRATION_GAP','Protocolo de progresso ainda não está conectado ao pai/fornecedor',[
          ('native_progress.py',15,80),('native_progress.py',83,120),('process_supervisor.py',100,120),('f9_controller_preparation/background_supplier.py',68,91)]),
      ('R4',1,'DECLARED_INTEGRATION_GAP','Runtime/objetos/quota e verificador externo não qualificados',[
          ('cooperative_policy.py',68,80),('supervisor_port_cooperative_proposal.py',45,86),('process_supervisor.py',218,254),('f9_controller_preparation/controller.py',80,109)]),
      ('R5',2,'STATIC_BOUNDARY_CLARIFICATION','Prazo nominal começa depois do preflight; recuperação incerta continua sem retry',[
          ('process_supervisor.py',124,143),('process_supervisor.py',198,219),('process_supervisor.py',248,254),('posix_protocol.py',176,181)]),
      ('R6',3,'PROVENANCE_LIMIT_NOT_PROOF_OF_LOSS','Snapshots presentes; cronologia pré-incidente não documentada no pacote',[
          ('NOTA_BACKUPS.json',1,9),('NOTA_PREPARACAO.md',21,21)])]
    rows=[{'id':i,'priority':p,'kind':k,'title':t,'anchors':[anchor(*a) for a in refs]} for i,p,k,t,refs in findings]
    receipt={'schema':'F9_INDEPENDENT_SUPERVISOR_STATIC_REVIEW_V1',
       'request_id':identity['request_id'],'parent_request_id':identity['parent_request_id'],
       'target_preparation_request_id':identity['candidate_request_id'],
       'status':'INDEPENDENT_STATIC_REVIEW_ACCEPTED',
       'accepted_scope':'STDLIB_PROCESS_SUPERVISOR_SOURCE_AND_SCOPED_SUCCESSOR_DIFF_COHERENCE_ONLY',
       'F1_integration_status':'OPEN_R1_R4_NOT_SCIENTIFIC_EXECUTOR_READY',
       'execution_authorized':False,'runtime_qualified':False,'observed_release':False,
       'candidate_manifest':static['candidate_manifest'],'static_checks':pin(HERE/'VERIFICACOES_ESTATICAS.json'),
       'report':pin(HERE/'REVISAO_INDEPENDENTE.md'),'findings':rows,
       'finding_scope':'R1-R4 são lacunas de integração já declaradas; R5 delimita relógio/cleanup; R6 não afirma perda. Nenhum novo impedimento matemático ou alteração de prior identificados.',
       'counts':{'members_checked':25,'sources_checked':18,'backups_checked':8,'Python_AST':9,'diffs_reconstructed_in_memory':2,'candidate_executions':0,'candidate_imports':0,'provider_calls':0},
       'next_step':'Construir sucessor completo com bootstrap/adaptador scoped, store I02 revisado e pipes/watchdog no mesmo pai; só então qualificação conjunta sob decisão ROOT futura, preservando prior inteiro/modelos. Não repetir I03/755c ou abrir ensaios isolados equivalentes.',
       'preserve':['V1 escalar não substituído pela proposta conjunta90da','§6 e D8/D5b/E3/d3C6','I02_99e2 e P3 já atribuídos','originais39f88 e pacote autor read-only','fila remota inelegível sem repin ou chamada','memórias globais/decisões pertencem à ROOT'],
       'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    write('RECIBO_REVISAO_INDEPENDENTE.json',receipt)
    for name in ('inspect_static.py','seal_review.py'):ast.parse((HERE/name).read_bytes())
    names=['IDENTIDADE_REVISAO.json','inspect_static.py','VERIFICACOES_ESTATICAS.json','REVISAO_INDEPENDENTE.md','seal_review.py','RECIBO_REVISAO_INDEPENDENTE.json']
    write('MANIFESTO_REVISAO.json',{'request_id':identity['request_id'],'status':'STATIC_REVIEW_COMPLETE_NO_EXECUTION_AUTHORIZATION',
      'members':[pin(HERE/name) for name in names],'backups':[pin(p) for p in sorted(HERE.glob('*.bak_*'))],
      'excludes':['MANIFESTO_REVISAO.json','RECIBO_COORDENACAO.json']})
    print(json.dumps({'review_receipt':pin(HERE/'RECIBO_REVISAO_INDEPENDENTE.json'),'review_manifest':pin(HERE/'MANIFESTO_REVISAO.json'),'candidate_execution':False}))

if __name__=='__main__':main()
