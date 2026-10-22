"""Perform the specifically approved R4 lease recovery, with immutable receipts."""
import json
import subprocess
import sys
import support_recovery as s

def board(label,args):
    s.new(label+'_INTENT.json',{'args':args})
    cp=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py']+args,capture_output=True,encoding='utf8')
    p=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode:raise RuntimeError(str(p))
    print(cp.stdout);return p

def tasks(m):return {t['id']:t for t in m['projection']['active']+m['projection']['settled']}

def main():
    auth=s.new('AUTORIZACAO_OPERADOR.json',{
      'origin':'Direct human answer in this conversation, send_user_message_question_reply',
      'questionItemId':'["request_user_input_async","call_bd7b5d12043447818a8e1fc023836e76",0]',
      'question':'A revisão automática bloqueou a recuperação de R4: o lease antigo venceu, mas o protocolo exige invalidá-lo explicitamente antes de reivindicar novamente; isso também revalida R3/R10, que já estavam pendentes. Autoriza essa recuperação administrativa, preservando critérios, provas e resultados anteriores, sem repetir execuções?',
      'answer':'Autorizar a recuperação de R4',
      'scope':'Administrative recovery only; no scientific proof or run repeated by this script.'})
    board('BOARD_CLAIM',['reivindicar','F1.FECHO.R4_LEASE_R59','--quem',s.ACTOR['id']])
    before=s.project('BEFORE');bt=tasks(before)
    assert bt['R4']['lease']['id']=='1e29d211-3523-4b98-a64d-5264c0c9bdea'
    assert bt['R3']['status']==bt['R10']['status']=='needs_revalidation'
    reason='Recuperação administrativa autorizada expressamente pelo operador em resposta call_bd7b5d12043447818a8e1fc023836e76. Lease R4 expirado revogado; critérios e evidências preservados. R3/R10 já pendentes permanecem em revalidação. Não repetir execuções.'
    s.call('mission_cli.py',{'operation':'invalidate','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':before['receipt']['revision'],'state_sha256':before['receipt']['state_sha256'],
      'event_id':'r4-expired-lease-recovery-human-approved-20261017','task_id':'R4','reason':reason,
      'sources':[s.pin(auth)]},'INVALIDATE')
    mid=s.project('AFTER_INVALIDATE');mt=tasks(mid)
    changed={k for k in bt if bt[k]!=mt[k]}
    assert changed=={'R4','R3','R10'},changed
    for k in bt:
        for field in ['criterion','depends_on','evidence','review_evidence']:
            assert bt[k].get(field)==mt[k].get(field),(k,field)
    s.call('mission_cli.py',{'operation':'claim','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':mid['receipt']['revision'],'projection_sha256':mid['projection_sha256'],
      'event_id':'r4-new-root-lease-after-approved-recovery-20261017','task_id':'R4','lease_seconds':14400},'CLAIM')
    s.preflight('R4','RECOVERED')
    after=s.project('AFTER');at=tasks(after)
    assert at['R4']['lease']['owner']==s.ACTOR['id']
    assert at['R4']['lease']['id']!=bt['R4']['lease']['id']
    assert at['R5']==bt['R5']
    for k in bt:
        for field in ['criterion','depends_on','evidence','review_evidence']:
            assert bt[k].get(field)==at[k].get(field),(k,field)
    receipt=s.new('RECOVERY_RESULT.json',{'status':'RECOVERED_PREFLIGHT_PASS','authorization':s.pin(auth),
      'before_receipt':before['receipt'],'after_receipt':after['receipt'],'affected':['R4','R3','R10'],
      'criteria_dependencies_evidence_preserved':True,'R5_unchanged':True,
      'settled_unchanged':before['projection']['settled']==after['projection']['settled'],
      'R4_new_lease':at['R4']['lease'],'scientific_runs':0,'provider_calls':0,'gate_changed':False})
    board('BOARD_DELIVERY',['avancar','F1.FECHO.R4_LEASE_R59','--quem',s.ACTOR['id'],'--status','ENTREGUE',
      '--evidencia',str(receipt),'--nota','Resposta humana registrada; recuperação R4 concluída com novo lease/preflight. Critérios, provas e estados aceitos preservados; nenhuma execução repetida. Fechamento administrativo pela gerência.'])
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'STATE_GET')
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':state['revision'],'event_id':'r4-authorized-recovery-recorded-20261017',
      'changes':{'records':[{'id':'r4-recovery-human-approved-completed','kind':'decision','statute':'INPUT',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in [auth,receipt]],
        'text':'Operador autorizou recuperação R4. Lease antigo invalidado explicitamente e novo lease root obtido; preflight passou. R3/R10 permanecem pendentes, critérios/evidências e R5/aceitos preservados. Pendência administrativa anterior atendida; não repetir execuções.'}],
        'flow':{'phase':'r4_recovered_ready_for_continuation','next_action':'Recuperar exploração OH já existente e revisar a ligação de observáveis/dinâmica sem repetir execução; manter R59/R60 como componentes condicionais.','handles':state['p']['handles']}}},'STATE_TRANSITION')
    print(receipt)

if __name__=='__main__':main()
