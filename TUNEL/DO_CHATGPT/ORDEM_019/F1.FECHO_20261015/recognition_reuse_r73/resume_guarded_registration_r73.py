"""Apply and register one reviewed documentary correction; release only R4."""
import datetime as dt
import json, subprocess, sys
import support_r73 as s

def once(label, command):
    s.new(label+'_INTENT.json', {'command':command,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    p=subprocess.run(command,capture_output=True,encoding='utf-8')
    out=s.new(label+'_RESULT.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode: raise RuntimeError(str(out))
    return out

def main():
    # Fail before any mutation if any downstream operation was attempted.
    for name in ['BOARD_REGISTER_INTENT.json','BOARD_REGISTER_RESULT.json','REGISTRATION_R73.json','RELEASE_R4_REQUEST.json','RELEASE_R4_RESULT.json','FINISH_TRANSITION_REQUEST.json','FINISH_TRANSITION_RESULT.json','MAP_REGISTER_WITH_TARGET_INTENT.json']:
        assert not (s.ROOT/name).exists(), 'Recovery must not repeat '+name
    snapshot=s.project('RECOVERY_GUARDED_PROJECT')
    assert snapshot['receipt']['revision']==510
    task=next(t for t in snapshot['projection']['active'] if t['id']=='R4')
    assert task['lease']['id']=='9a70d83d-589a-4816-b9a1-b6fac4f970e8'
    failed=json.loads((s.ROOT/'MAP_REGISTER_RESULT.json').read_text(encoding='utf-8'))
    assert failed['exit_code']==2 and json.loads(failed['stdout'])['ok'] is False
    delivery=s.ROOT/'DELIVERY_R73.json'
    assert delivery.exists()
    applied=json.loads((s.ROOT/'MEMORY_APPLIED_R73.json').read_text(encoding='utf-8'))
    for row in applied['surfaces']:
        assert s.pin(row['after']['path'])==row['after']
        assert s.pin(row['backup']['path'])==row['backup']
    entry=json.loads((s.ROOT/'MAP_ENTRY_R73.json').read_text(encoding='utf-8'))
    prior=json.loads(json.loads((s.ROOT.parent/'device_profiles_r72/MAP_REGISTER_RESULT.json').read_text(encoding='utf-8'))['stdout'])
    entry['corrige']=prior['gravados'][0]['seq']
    corrected=s.new('MAP_ENTRY_R73_WITH_TARGET.json',entry)
    mr=once('MAP_REGISTER_WITH_TARGET',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(corrected),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R73 documental: retirada da redefinicao redundante ao operador; reuso R57/M2v394/R64. Claim967scope971, oito memorias combackup; semexecucao cientifica. R4/R5 integrais abertos.'])
    registration=s.new('REGISTRATION_R73.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    s.mutate('release','RELEASE_R4',task_id='R4',reason='R73 corrige pedido redundante: reconhecimento/travessia/releitura existentes. Equipe deve ligar canais instrumentais; Gamma/calibracao e R4/R5 integrais continuam abertos.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r73-recognition-reuse-correction-recorded','changes':{'records':[{'id':'r73-recognition-reuse-correction','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,registration)],'text':'R73: QUESTION_MODAL_IDENTITY_R72 WITHDRAWN_AS_OPERATOR_REDEFINITION_REQUEST. R57 leitor/decoder recuperam fronteira escalar; releitura idempotente separada. M2/v394 ja construiu travessia continua com escopo; R64 ja discutia RF/optica. Equipe audita e liga canais aos objetos existentes sem nova cunhagem ao operador. Gamma e R4/R5 integrais abertos. Camada documental revisada, sem nova ciencia, producao ou gate.'}],'flow':{'phase':'r73_recognition_reuse_corrected','next_action':'Reusar reconhecimento R57 e continuidade M2/v394; auditar e ligar canais instrumentais aos objetos ja construidos, com referencia, ganhos, unidades e estado. Nao reabrir definicao ao operador. Preservar Gamma/R4/R5 abertos; claim/check antes de avancar.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':main()
