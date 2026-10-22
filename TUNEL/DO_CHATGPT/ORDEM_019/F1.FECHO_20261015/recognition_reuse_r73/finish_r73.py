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
    if sys.argv[1:]!=['--apply']:raise RuntimeError('Explicit --apply after independent review required')
    assert not (s.ROOT/'DELIVERY_R73.json').exists()
    review=json.loads((s.ROOT/'REVIEW_R73.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for e in review['evidence']:assert s.pin(e['path'])['sha256']==e['sha256']
    for name in ['CORRECAO_REAPROVEITAMENTO_R73.md','SOURCE_PINS_R73.json','WITHDRAWAL_MODAL_REQUEST_R73.json','MEMORY_PLAN_R73.json','MEMORY_APPEND_R73.txt','memory_r73.py','support_r73.py','finish_r73.py']:
        assert s.pin(s.ROOT/name) in review['evidence']
    for e in json.loads((s.ROOT/'SOURCE_PINS_R73.json').read_text(encoding='utf-8'))['sources']:
        assert s.pin(e['path'])==e
    m=s.project('FINISH_R4_PROJECT')
    lease=json.loads((s.ROOT/'CLAIM_R4_RESULT.json').read_text(encoding='utf-8'))['response']['result']['task']['lease']['id']
    s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':'R4','lease_id':lease},'FINISH_R4_CHECK')
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r73.py'),'apply'])
    evidence=[s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix!='.pyc']
    delivery=s.new('DELIVERY_R73.json',{'status':'REVIEWED_DOCUMENTARY_CORRECTION','unit':'F1.FECHO_20261015','claim':967,'scope_event':971,'author':s.ACTOR['id'],'evidence':evidence,'question_disposition':'WITHDRAWN_AS_OPERATOR_REDEFINITION_REQUEST','R4_R5_integrally_satisfied':False,'new_scientific_executions':0,'providers':0,'canonical_changed':False,'gate_changed':False,'process':'First invalid board scope attempt preserved; corrected scope971 governs this append.'})
    entry=s.new('MAP_ENTRY_R73.json',{'tipo':'ERRATA','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R73: retirar redefinicao redundante e reutilizar reconhecimento existente','metodo':'Leitura focal R57, v394 e R64; pins e recibo historico conferidos; revisao distinta; sem nova ciencia.','resultado':'QUESTION_MODAL_IDENTITY_R72 retirada como pedido de redefinicao ao operador. R57 ja contem leitor, decoder e releitura; M2/v394 contem travessia continua; R64 ja distingue RF/optica. A equipe ligara os canais instrumentais aos objetos existentes.','veredito':'WITHDRAWN_AS_OPERATOR_REDEFINITION_REQUEST','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,'defeito':'Calibracao independente Gamma e criterios integrais R4/R5 continuam abertos; idempotencia isolada nao recupera fase.','nao_refazer':'Nao reabrir a definicao do mecanismo nem pedir nova cunhagem; nao repetir R57/M2/R64.','proximo_passo':'Auditar e ligar canais instrumentais a objetos e referencias existentes, com estado, ganhos, unidades e dominios.','artefatos':[str(delivery),str(s.ROOT/'WITHDRAWAL_MODAL_REQUEST_R73.json'),str(s.ROOT/'CORRECAO_REAPROVEITAMENTO_R73.md')],'onde':str(s.ROOT),'refs':['formal.anchored_name_contour']})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R73 documental: retirada da redefinicao redundante ao operador; reuso R57/M2v394/R64. Claim967scope971, oito memorias combackup; semexecucao cientifica. R4/R5 integrais abertos.'])
    registration=s.new('REGISTRATION_R73.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    s.mutate('release','RELEASE_R4',task_id='R4',reason='R73 corrige pedido redundante: reconhecimento/travessia/releitura existentes. Equipe deve ligar canais instrumentais; Gamma/calibracao e R4/R5 integrais continuam abertos.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r73-recognition-reuse-correction-recorded','changes':{'records':[{'id':'r73-recognition-reuse-correction','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,registration)],'text':'R73: QUESTION_MODAL_IDENTITY_R72 WITHDRAWN_AS_OPERATOR_REDEFINITION_REQUEST. R57 leitor/decoder recuperam fronteira escalar; releitura idempotente separada. M2/v394 ja construiu travessia continua com escopo; R64 ja discutia RF/optica. Equipe audita e liga canais aos objetos existentes sem nova cunhagem ao operador. Gamma e R4/R5 integrais abertos. Camada documental revisada, sem nova ciencia, producao ou gate.'}],'flow':{'phase':'r73_recognition_reuse_corrected','next_action':'Reusar reconhecimento R57 e continuidade M2/v394; auditar e ligar canais instrumentais aos objetos ja construidos, com referencia, ganhos, unidades e estado. Nao reabrir definicao ao operador. Preservar Gamma/R4/R5 abertos; claim/check antes de avancar.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':main()
