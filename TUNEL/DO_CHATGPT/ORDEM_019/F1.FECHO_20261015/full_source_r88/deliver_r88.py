"""Reviewed progress only: keep R16 working; no goal completion or semantic accept."""
from support_r88 import ROOT, REF, ACTOR, TASK, new, pin, call, project, mutate
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

def command(label, args):
    new(label+'_INTENT.json',{'command':args})
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    p=new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode: raise RuntimeError(str(p))
    return p

def apply():
    assert not (ROOT/'DELIVERY_R88.json').exists()
    review=json.loads((ROOT/'REVIEW_R88_FINAL.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=ACTOR['id']
    for e in review['evidence']: assert pin(e['path'])==e
    for name in ['RESULTADO_R88.json','P5_COVARIANT_STATIONARITY_R88.txt','P5_DOMAIN_QUALIFIER_R88.txt','source/ONE_FORM_FULL_SOURCE_R88.md','source/SOURCE_PINS_R88.json','spectral_reuse/SPECTRAL_RULE_REUSE_R88.md','spectral_reuse/SOURCE_PINS_SPECTRAL_R88.json','OPERATOR_SPECTRAL_RULE_REPLY_R88.json','OPERATOR_STEERING_R88.txt','MEMORY_APPEND_R88.txt','MEMORY_PLAN_R88.json','deliver_r88.py']:
        assert pin(ROOT/name) in review['evidence'],name
    result=json.loads((ROOT/'RESULTADO_R88.json').read_text(encoding='utf-8'))
    for e in result['evidence']: assert pin(e['path'])==e
    assert result['goal_complete'] is False
    assert result['build_exit_code']==0 and result['axioms_only_trio'] is True
    p=project('APPLY_SYNC'); task=next(t for t in p['projection']['active'] if t['id']==TASK)
    preflight=call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_APPLY')
    if preflight.get('ready') is not True:
        raise RuntimeError('Mission preflight refused: '+repr(preflight))
    plan=json.loads((ROOT/'MEMORY_PLAN_R88.json').read_text(encoding='utf-8')); extra=Path(plan['append']['path']).read_bytes()
    assert pin(plan['append']['path'])==plan['append']
    for row in plan['surfaces']: assert pin(row['before']['path'])==row['before']
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); done=[]
    for i,row in enumerate(plan['surfaces'],1):
        p=Path(row['before']['path']);raw=p.read_bytes();assert pin(p)==row['before']
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_r88_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra) and pin(p)==row['before']
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        assert pin(p)['sha256']==row['after_sha256']
        receipt={'before':row['before'],'backup':pin(bak),'after':pin(p),'pure_append':True}
        new(f'MEMORY_SURFACE_{i}.json',receipt);done.append(receipt)
    new('MEMORY_APPLIED_R88.json',{'claim':996,'surfaces':done})
    delivery=new('DELIVERY_R88.json',{'status':'INTEGRATED_VARIATION_PROGRESS_REVIEWED_GOAL_OPEN','unit':'F1.FECHO_20261015','claim':996,'H3_universal_proved':False,'lean_components':result['build_components'],'provider_calls':0,'physical_measurements':0,'gate_changed':False,'evidence':[pin(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    entry=new('MAP_ENTRY_R88.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R88: regra espectral reaproveitada, Hessiana e variacao da densidade','resultado':'Derivadas reais do campo levantado, corrente Hessiana e composicao local da densidade compiladas. Regra recuperada: dissipador do salto existente e gradiente do contraste, leitura espectral compara alvo. Ramo P5 transportado por covariancia; fonte de 1-forma nomeada derivada. H3 universal aberto.','estatuto':'DERIVED','status':'EM_CURSO','veredito':'PASS_COMPONENT_WITH_SCOPE','olhou_dados':False,'nao_refazer':'Reuso R83 a R87, ramo Einstein-sigma de09set, DecisionCommutation e regra no motor continuo. Nao repetir pergunta abstrata de identidade. Busca espectral com cobertura e pinos; nenhum rebuild verde.','defeito':'Fonte e estacionariedade da ACAO COMPLETA abertas; ramo ambiente tem habitante. Campos S3/S14 e representacoes espectrais distintos. Hipoteses integrais e contorno fisico preservados.','proximo_passo':'Consumir representacao espectral efetiva no campo e na fonte da mesma acao; usar a primeira variacao integrada agora composta, sem pedir recunhagem ao operador.','artefatos':[str(delivery),str(ROOT/'RESULTADO_R88.json')],'onde':str(ROOT),'refs':['formal.f1_rede.concrete_bosonic_kinematics']})
    mapped=command('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',ACTOR['id']])
    boarded=command('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R88 regra espectral existente recuperada, derivadas/Hessiana/densidade compiladas e fonte de 1-forma nomeada revisadas. Oito memorias append/backup. R16 working, H3 universal aberto; sem dados/gate.'])
    new('REGISTRATION_R88.json',{'delivery':pin(delivery),'map':pin(mapped),'board':pin(boarded)})
    s=call({'operation':'get','reference':REF},'GET_FINAL','session_memory.py')
    flow=dict(s['p']);flow['phase']='spectral_satisfaction_reused_density_composed_full_source_open';flow['next_action']='R88: use recovered spectral commutator, dissipation and fixed reading to consume the concrete representation in the same-P full action; do not repeat the answered abstract identity question. P5 stationary ambient branch transported with named constants. Full-density and integrated variation compiled under explicit support/domination, boundary divergence retained. R16 working, universal H3 open.'
    finished={'r88-boundary':ROOT/'RESULTADO_R88.json','r88-source':ROOT/'RESULTADO_R88.json','r88-spectral-reuse':ROOT/'RESULTADO_R88.json'}
    flow['handles']=[dict(h,status='completed',receipt=pin(finished[h['id']])) if h.get('id') in finished else h for h in flow.get('handles',[])]
    call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r88-integrated-action-P-recorded','changes':{'records':[{'id':'r88-integrated-action-P-scope','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}],'text':extra.decode('utf-8')}],'flow':flow}},'FINAL_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':
    {'apply':apply}[sys.argv[1]]()
