"""Reviewed progress only: keep R16 working; no goal completion or semantic accept."""
from support_r84 import ROOT, REF, ACTOR, TASK, new, pin, call, project, mutate
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

def command(label, args):
    new(label+'_INTENT.json',{'command':args})
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    p=new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode: raise RuntimeError(str(p))
    return p

def apply():
    assert not (ROOT/'DELIVERY_R85.json').exists()
    review=json.loads((ROOT/'REVIEW_R85_FINAL.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=ACTOR['id']
    for e in review['evidence']: assert pin(e['path'])==e
    for name in ['RESULTADO_R85.json','SOURCE_COMPLETENESS_R85.txt','SOURCE_OFFSHELL_RESULT.json','MEMORY_APPEND_R85.txt','MEMORY_PLAN_R85.json','deliver_r85.py']:
        assert pin(ROOT/name) in review['evidence'],name
    result=json.loads((ROOT/'RESULTADO_R85.json').read_text(encoding='utf-8'))
    for e in result['evidence']: assert pin(e['path'])==e
    assert result['goal_complete'] is False
    assert result['build_exit_code']==0 and result['axioms_only_trio'] is True
    p=project('APPLY_SYNC'); task=next(t for t in p['projection']['active'] if t['id']==TASK)
    preflight=call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_APPLY')
    if preflight.get('ready') is not True:
        raise RuntimeError('Mission preflight refused: '+repr(preflight))
    plan=json.loads((ROOT/'MEMORY_PLAN_R85.json').read_text(encoding='utf-8')); extra=Path(plan['append']['path']).read_bytes()
    assert pin(plan['append']['path'])==plan['append']
    for row in plan['surfaces']: assert pin(row['before']['path'])==row['before']
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); done=[]
    for i,row in enumerate(plan['surfaces'],1):
        p=Path(row['before']['path']);raw=p.read_bytes();assert pin(p)==row['before']
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_r85_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra) and pin(p)==row['before']
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        assert pin(p)['sha256']==row['after_sha256']
        receipt={'before':row['before'],'backup':pin(bak),'after':pin(p),'pure_append':True}
        new(f'MEMORY_SURFACE_{i}.json',receipt);done.append(receipt)
    new('MEMORY_APPLIED_R85.json',{'claim':996,'surfaces':done})
    delivery=new('DELIVERY_R85.json',{'status':'INTEGRATED_VARIATION_PROGRESS_REVIEWED_GOAL_OPEN','unit':'F1.FECHO_20261015','claim':996,'H3_universal_proved':False,'lean_builds':result['build_attempt_count'],'provider_calls':0,'physical_measurements':0,'gate_changed':False,'evidence':[pin(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    entry=new('MAP_ENTRY_R85.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R85: Palatini, levantamento metrico P16 e fonte fora do fundo','resultado':'Ligacao de deltaRic a corrente covariante; P16 com levantamento local de campos metricos compactos; material varia junto. Fonte modular requer extensao fora do fundo. Objetivo integral aberto.','estatuto':'DERIVED','status':'EM_CURSO','veredito':'PASS_COMPONENT_WITH_SCOPE','olhou_dados':False,'nao_refazer':'Reuso R83/R84, CurvatureNonlinearVariation, MetricRicciVariation, VariationalInhabitant, SelectedFisherGibbs e SelectedProbabilitySigma.','defeito':'Selecao dinamica P, equacao material e fonte integral abertas; corrente ponderada e volume ainda requerem ligacao.','proximo_passo':'Buscar e construir selecao dinamica P e levantamento de testes nulos compactos com campos materiais controlados; nao assumir H3.','artefatos':[str(delivery),str(ROOT/'RESULTADO_R85.json')],'onde':str(ROOT),'refs':['formal.f1_rede.concrete_bosonic_kinematics']})
    mapped=command('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',ACTOR['id']])
    boarded=command('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R85 corrente Palatini, alcance P16 e limites de fonte/estacionariedade revisados. Oito memorias append/backup. Objetivo R16 permanece working; H3 universal aberto; sem dados/gate.'])
    new('REGISTRATION_R85.json',{'delivery':pin(delivery),'map':pin(mapped),'board':pin(boarded)})
    s=call({'operation':'get','reference':REF},'GET_FINAL','session_memory.py')
    flow=dict(s['p']);flow['phase']='P16_lift_material_stationarity_open';flow['next_action']='R85 Palatini current and local P16 metric lift established with scope. Continue weighted boundary identity, material equations and independent P dynamics; full modular source off background remains open. R16 working; no universal H3 or physical significance.'
    finished={'r85-boundary-builder':ROOT/'RESULTADO_R85.json','r85-P-selection':ROOT/'RESULTADO_R85.json'}
    flow['handles']=[dict(h,status='completed',receipt=pin(finished[h['id']])) if h.get('id') in finished else h for h in flow.get('handles',[])]
    call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r85-integrated-action-P-recorded','changes':{'records':[{'id':'r85-integrated-action-P-scope','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}],'text':extra.decode('utf-8')}],'flow':flow}},'FINAL_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':
    {'apply':apply}[sys.argv[1]]()
