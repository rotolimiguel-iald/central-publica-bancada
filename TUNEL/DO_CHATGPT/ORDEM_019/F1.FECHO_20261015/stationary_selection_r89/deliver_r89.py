"""Reviewed progress only: keep R16 working; no goal completion or semantic accept."""
from support_r89 import ROOT, REF, ACTOR, TASK, new, pin, call, project, mutate
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

def command(label, args):
    new(label+'_INTENT.json',{'command':args})
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    p=new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode: raise RuntimeError(str(p))
    return p

def apply():
    assert not (ROOT/'DELIVERY_R89.json').exists()
    review=json.loads((ROOT/'REVIEW_R89_FINAL.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=ACTOR['id']
    for e in review['evidence']: assert pin(e['path'])==e
    for name in ['RESULTADO_R89.json','formal/BUILDER_DELIVERY_R89.json','source/SPECTRAL_STATIONARITY_DIAGNOSTIC_R89.md','source/ACTION_EOM_RESIDUAL_R89.md','source/SOURCE_FINAL_R89.json','MEMORY_APPEND_R89.txt','MEMORY_PLAN_R89.json','deliver_r89.py']:
        assert pin(ROOT/name) in review['evidence'],name
    result=json.loads((ROOT/'RESULTADO_R89.json').read_text(encoding='utf-8'))
    for e in result['evidence']: assert pin(e['path'])==e
    assert result['goal_complete'] is False
    assert result['build_exit_code']==0 and result['axioms_only_trio'] is True
    p=project('APPLY_SYNC'); task=next(t for t in p['projection']['active'] if t['id']==TASK)
    preflight=call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_APPLY')
    if preflight.get('ready') is not True:
        raise RuntimeError('Mission preflight refused: '+repr(preflight))
    plan=json.loads((ROOT/'MEMORY_PLAN_R89.json').read_text(encoding='utf-8')); extra=Path(plan['append']['path']).read_bytes()
    assert pin(plan['append']['path'])==plan['append']
    for row in plan['surfaces']: assert pin(row['before']['path'])==row['before']
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); done=[]
    for i,row in enumerate(plan['surfaces'],1):
        p=Path(row['before']['path']);raw=p.read_bytes();assert pin(p)==row['before']
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_r89_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra) and pin(p)==row['before']
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        assert pin(p)['sha256']==row['after_sha256']
        receipt={'before':row['before'],'backup':pin(bak),'after':pin(p),'pure_append':True}
        new(f'MEMORY_SURFACE_{i}.json',receipt);done.append(receipt)
    new('MEMORY_APPLIED_R89.json',{'claim':996,'surfaces':done})
    delivery=new('DELIVERY_R89.json',{'status':'INTEGRATED_VARIATION_PROGRESS_REVIEWED_GOAL_OPEN','unit':'F1.FECHO_20261015','claim':996,'H3_universal_proved':False,'lean_components':result['build_components'],'provider_calls':0,'physical_measurements':0,'gate_changed':False,'evidence':[pin(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    entry_data={'tipo': 'RESULTADO', 'rota_id': 'formal.f1_rede.concrete_bosonic_kinematics', 'dominio': 'FORMAL', 'titulo': 'R89: selecao espectral do mesmo estado e residuo funcional da acao', 'resultado': 'Tres consumidores Lean compilados: residuo do gerador, alvo movel e alvo fixo. Confronto literal entre acao e EOM explicita termos a corresponder; modulo abs exige regularidade da classe variacional. R88 primeira variacao integrada preservada.', 'estatuto': 'DERIVED', 'status': 'EM_CURSO', 'veredito': 'PASS_COMPONENT_WITH_SCOPE', 'olhou_dados': False, 'nao_refazer': 'R85 controles Gibbs/GKLS e P16 citados; P5 estacionario e R88 integral mantidos. Nao repetir pergunta de identidade nem execucoes anteriores.', 'defeito': 'Identidade do gerador do proprio estado nao seleciona deltaS_total=0; falta consumir campo e setor modular numa unica fonte funcional. Nao demonstrada ausencia global no acervo.', 'proximo_passo': 'Conferir representacoes e termos restantes contra o residuo Euler explicito, sem ajustar acao para fabricar equivalencia.', 'refs': ['formal.f1_rede.concrete_bosonic_kinematics']}
    entry_data.update({'artefatos':[str(delivery),str(ROOT/'RESULTADO_R89.json')],'onde':str(ROOT)})
    entry=new('MAP_ENTRY_R89.json',entry_data)
    mapped=command('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',ACTOR['id']])
    boarded=command('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R89 selecao do mesmo estado e residuo funcional revisados; tres consumidores Lean, sem repetir controles. Oito memorias append/backup. R16 aberto, sem dado/gate.'])
    new('REGISTRATION_R89.json',{'delivery':pin(delivery),'map':pin(mapped),'board':pin(boarded)})
    s=call({'operation':'get','reference':REF},'GET_FINAL','session_memory.py')
    flow=dict(s['p']);flow['phase']='same_state_selection_and_action_residual_verified';flow['next_action']='R89 distinguishes same-state fixed-space identity from stationarity of the complete action. Use explicit Euler residual and admissible-variation regularity to verify candidate source representations in existing archive. R88 integrated variation proved with explicit hypotheses; full same-P source and stationarity remain open. No repeated abstract identity question.'
    finished={'r89-formal':ROOT/'RESULTADO_R89.json','r89-source':ROOT/'RESULTADO_R89.json'}
    flow['handles']=[dict(h,status='completed',receipt=pin(finished[h['id']])) if h.get('id') in finished else h for h in flow.get('handles',[])]
    call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r89-integrated-action-P-recorded','changes':{'records':[{'id':'r89-integrated-action-P-scope','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}],'text':extra.decode('utf-8')}],'flow':flow}},'FINAL_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':
    {'apply':apply}[sys.argv[1]]()
