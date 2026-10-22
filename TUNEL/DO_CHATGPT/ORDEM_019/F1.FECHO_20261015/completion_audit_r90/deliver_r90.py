"""Reviewed additive source custody; no scientific accept or goal completion."""
from support_r90 import ROOT, REF, ACTOR, TASK, new, pin, call, project
from pathlib import Path
import datetime, json, os, subprocess, sys

def command(label,args):
    new(label+'_INTENT.json',{'command':args})
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    p=new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode: raise RuntimeError(str(p))
    return p

def apply():
    assert not (ROOT/'DELIVERY_R90.json').exists()
    review=json.loads((ROOT/'REVIEW_R90_FINAL.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=ACTOR['id']
    for e in review['evidence']: assert pin(e['path'])==e
    for name in ['RESULTADO_R90.json','BALANCO_DA_META_R90.md','source/ACOM_V18_RECOVERY_R90.md','INDEPENDENT_COMPLETION_SCOPE_R90.txt','MEMORY_APPEND_R90.txt','MEMORY_PLAN_R90.json','deliver_r90.py']:
        assert pin(ROOT/name) in review['evidence'],name
    result=json.loads((ROOT/'RESULTADO_R90.json').read_text(encoding='utf-8'))
    for e in result['evidence']: assert pin(e['path'])==e
    assert pin(result['balance']['path'])==result['balance']
    assert result['goal_complete'] is False and result['new_builds']==0
    p=project('APPLY_SYNC'); task=next(t for t in p['projection']['active'] if t['id']==TASK)
    ready=call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_APPLY')
    assert ready.get('ready') is True
    plan=json.loads((ROOT/'MEMORY_PLAN_R90.json').read_text(encoding='utf-8'))
    extra=Path(plan['append']['path']).read_bytes(); assert pin(plan['append']['path'])==plan['append']
    for row in plan['surfaces']: assert pin(row['before']['path'])==row['before']
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); done=[]
    for i,row in enumerate(plan['surfaces'],1):
        p=Path(row['before']['path']); raw=p.read_bytes(); assert pin(p)==row['before']
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_r90_'+stamp)
        with tmp.open('xb') as f: f.write(raw+extra); f.flush(); os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra) and pin(p)==row['before']
        os.replace(tmp,p); assert p.read_bytes()==raw+extra
        assert pin(p)['sha256']==row['after_sha256']
        receipt={'before':row['before'],'backup':pin(bak),'after':pin(p),'pure_append':True}
        new(f'MEMORY_SURFACE_{i}.json',receipt); done.append(receipt)
    new('MEMORY_APPLIED_R90.json',{'claim':996,'surfaces':done})
    delivery=new('DELIVERY_R90.json',{'status':'SOURCE_RECOVERY_AND_FULL_OBJECTIVE_AUDIT_REVIEWED','unit':'F1.FECHO_20261015','claim':996,'goal_complete':False,'H3_universal_proved':False,'new_builds':0,'provider_calls':0,'physical_measurements':0,'gate_changed':False,'evidence':[pin(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    entry=new('MAP_ENTRY_R90.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R90: ACOM v18 recuperado e auditoria da meta integral','resultado':'Fontes v18 e quantizador recuperados e lidos. Primeira variacao integrada R88 preservada; estacionariedade e fonte completas seguem abertas. Regra de reconhecimento respondida; consumidor variacional ainda nao demonstrado.','estatuto':'DERIVED','status':'EM_CURSO','veredito':'SOURCE_RECOVERED_FULL_OBJECTIVE_OPEN','olhou_dados':False,'nao_refazer':'Nao repetir busca v18, builds R88/R89 ou pergunta abstrata de identidade.','defeito':'Mapa de quantizacao/reconstrucao nao fornece por si a igualdade DF(P)*E_total=0; ausencia limitada ao recorte consultado.','proximo_passo':'Consumir fonte concreta adicional ou construcao variacional justificada para o residuo ja delimitado.','refs':['formal.f1_rede.concrete_bosonic_kinematics'],'artefatos':[str(delivery),str(ROOT/'RESULTADO_R90.json'),str(ROOT/'BALANCO_DA_META_R90.md')],'onde':str(ROOT)})
    mapped=command('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',ACTOR['id']])
    boarded=command('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R90 recupera v18 e audita meta completa; zero build/rerun/provedor. Oito memorias com backup e append. H3 aberto; nenhum aceite ou gate.'])
    new('REGISTRATION_R90.json',{'delivery':pin(delivery),'map':pin(mapped),'board':pin(boarded)})
    s=call({'operation':'get','reference':REF},'GET_FINAL','session_memory.py')
    flow=dict(s['p']); flow['phase']='full_objective_audited_variational_consumer_unresolved'
    flow['next_action']='The v18 reference is recovered. Further progress requires a concrete additional source or justified same-field variational construction consuming DF(P)*E_total=0. R88 integrated variation stands; full stationarity/source and universal H3 remain open. Do not repeat identity question, completed builds or this source search.'
    flow['handles']=[dict(h,status='completed',receipt=pin(ROOT/'RESULTADO_R90.json')) if h.get('id')=='r90-source' else h for h in flow.get('handles',[])]
    call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r90-acom-source-and-full-objective-recorded','changes':{'records':[{'id':'r90-acom-source-and-full-objective-scope','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}],'text':extra.decode('utf-8')}],'flow':flow}},'FINAL_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__': {'apply':apply}[sys.argv[1]]()
