"""Additive reviewed delivery; local density proof, not H3 or stationarity."""
from support_r83 import ROOT, REF, ACTOR, TASK, new, pin, call, project, mutate
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

def command(label, args):
    new(label+'_INTENT.json',{'command':args})
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    p=new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode: raise RuntimeError(str(p))
    return p

def apply():
    assert not (ROOT/'DELIVERY_R83.json').exists()
    review=json.loads((ROOT/'REVIEW_R83_FINAL.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=ACTOR['id']
    for e in review['evidence']: assert pin(e['path'])==e
    for name in ['RELATORIO_R83.txt','FINAL_BUILD_R83.json','SOURCE_PINS_R83.json','MEMORY_APPEND_R83.txt','MEMORY_PLAN_R83.json','deliver_r83.py']:
        assert pin(ROOT/name) in review['evidence'],name
    for e in json.loads((ROOT/'SOURCE_PINS_R83.json').read_text(encoding='utf-8'))['sources']: assert pin(e['path'])==e
    final=json.loads((ROOT/'FINAL_BUILD_R83.json').read_text(encoding='utf-8'))
    for e in final['evidence']: assert pin(e['path'])==e
    assert final['exit_code']==0 and final['axioms_only_trio'] is True and final['sorry_count']==0
    p=project('APPLY_SYNC'); task=next(t for t in p['projection']['active'] if t['id']==TASK)
    preflight=call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_APPLY')
    if preflight.get('ready') is not True:
        raise RuntimeError('Mission preflight refused: '+repr(preflight))
    plan=json.loads((ROOT/'MEMORY_PLAN_R83.json').read_text(encoding='utf-8')); extra=Path(plan['append']['path']).read_bytes()
    assert pin(plan['append']['path'])==plan['append']
    for row in plan['surfaces']: assert pin(row['before']['path'])==row['before']
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); done=[]
    for i,row in enumerate(plan['surfaces'],1):
        p=Path(row['before']['path']);raw=p.read_bytes();assert pin(p)==row['before']
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_r83_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra) and pin(p)==row['before']
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        assert pin(p)['sha256']==row['after_sha256']
        receipt={'before':row['before'],'backup':pin(bak),'after':pin(p),'pure_append':True}
        new(f'MEMORY_SURFACE_{i}.json',receipt);done.append(receipt)
    new('MEMORY_APPLIED_R83.json',{'claim':991,'surfaces':done})
    delivery=new('DELIVERY_R83.json',{'status':'LOCAL_DENSITY_KERNEL_COMPONENT_REVIEWED','unit':'F1.FECHO_20261015','claim':991,'H3_universal_proved':False,'lean_builds':final['attempt_count'],'provider_calls':0,'physical_measurements':0,'gate_changed':False,'evidence':[pin(p) for p in sorted(ROOT.iterdir()) if p.is_file()]})
    entry=new('MAP_ENTRY_R83.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R83: derivada local da densidade gravitacional e reuso do mesmo P','resultado':'Derivada local compilada em sandbox, so trio; casos escalar, norma de covetor e soma com materia. Origem comum P ja existe.','estatuto':'DERIVED','status':'EM_CURSO','veredito':'PASS_COMPONENT_WITH_SCOPE','olhou_dados':False,'nao_refazer':'Reuso R58/R82, ScalarMatterDensityVariation, MetricEinsteinVariation, SelectedFisherGibbs e SelectedProbabilitySigma.','defeito':'Acao integrada, estacionariedade e fonte nao minimal do mesmo registro continuam abertas.','proximo_passo':'Partir de selectedSigmaRecord, resolver representacao Psi e alcance das variacoes induzidas de g(P).','artefatos':[str(delivery),str(ROOT/'RELATORIO_R83.txt')],'onde':str(ROOT),'refs':['formal.f1_rede.concrete_bosonic_kinematics']})
    mapped=command('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',ACTOR['id']])
    boarded=command('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R83 derivada local formal revisada, so trio; origem comum P recuperada. Oito memorias append/backup. H3 universal aberto; sem dados/gate.'])
    new('REGISTRATION_R83.json',{'delivery':pin(delivery),'map':pin(mapped),'board':pin(boarded)})
    current=project('BEFORE_SUBMIT');task=next(t for t in current['projection']['active'] if t['id']==TASK)
    mutate('submit','SUBMIT',task_id=TASK,lease_id=task['lease']['id'],evidence=[pin(delivery),pin(ROOT/'REVIEW_R83_FINAL.json')])
    s=call({'operation':'get','reference':REF},'GET_FINAL','session_memory.py')
    flow=dict(s['p']);flow['phase']='h3_density_variation_reviewed';flow['next_action']='R83: derivada local formalizada; same-P ja existe em SelectedFisherGibbs/SelectedProbabilitySigma. Prosseguir na identificacao nao minimal e alcance das variacoes em P; acao integrada/estacionariedade/H3 universal OPEN. OH adiado; aceites administrativos anteriores separados.'
    flow['handles']=[dict(h,status='completed',receipt=str(ROOT/'FINAL_BUILD_R83.json')) if h.get('id')=='r83-density-construction' else h for h in flow.get('handles',[])]
    call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r83-local-density-recorded','changes':{'records':[{'id':'r83-density-variation','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}],'text':extra.decode('utf-8')}],'flow':flow}},'FINAL_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':
    {'apply':apply}[sys.argv[1]]()
