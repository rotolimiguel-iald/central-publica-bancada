"""Apply reviewed append-only memory and register this bounded H3 analysis."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
from support_r81 import ROOT,new,pin,check,mutate,call,REF,ACTOR,TASK,project

def command(label,args):
    new(label+'_INTENT.json',{'command':args})
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    p=new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(str(p))
    return p

def main():
    assert sys.argv[1:]==['--apply']
    if (ROOT/'DELIVERY_R81.json').exists():raise FileExistsError('DELIVERY_R81.json')
    review=json.loads((ROOT/'REVIEW_R81.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=ACTOR['id']
    for e in review['evidence']:assert pin(e['path'])==e
    for name in ['ANALISE_R81.txt','RecoveryAreaCoefficient.lean','SOURCE_PINS_R81.json','MEMORY_PLAN_R81.json','MEMORY_APPEND_R81.txt','finish_r81.py']:
        assert pin(ROOT/name) in review['evidence'],name
    for e in json.loads((ROOT/'SOURCE_PINS_R81.json').read_text(encoding='utf-8'))['sources']:
        assert pin(e['path'])==e
    check('FINISH')
    plan=json.loads((ROOT/'MEMORY_PLAN_R81.json').read_text(encoding='utf-8'))
    assert pin(plan['append']['path'])==plan['append']
    extra=Path(plan['append']['path']).read_bytes()
    for row in plan['surfaces']:assert pin(row['before']['path'])==row['before']
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');done=[]
    for row in plan['surfaces']:
        p=Path(row['before']['path']);raw=p.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==row['before']['sha256']
        backup=p.with_name(p.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert backup.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_r81_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra)
        assert pin(p)==row['before']
        os.replace(tmp,p)
        assert p.read_bytes()==raw+extra
        assert pin(p)['sha256']==row['after_sha256']
        done.append({'before':row['before'],'backup':pin(backup),'after':pin(p),'pure_append':True})
        new('MEMORY_SURFACE_'+str(len(done))+'.json',done[-1])
    new('MEMORY_APPLIED_R81.json',{'claim':987,'surfaces':done})
    delivery=new('DELIVERY_R81.json',{'status':'REVIEWED_SCOPE_COMPONENT','unit':'F1.FECHO_20261015','claim':987,'author':ACTOR['id'],'H3_universal_proved':False,'physical_measurements':0,'provider_calls':0,'gate_changed':False,'evidence':[pin(p) for p in sorted(ROOT.iterdir()) if p.is_file()]})
    entry=new('MAP_ENTRY_R81.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R81: recuperacao Mirror e coeficiente geometrico de H3','resultado':'Reuso SelectorRecordReconstruction: metrica/fonte recuperadas, harea ainda nomeada. Ponte de coeficientes em sandbox; recuperacao conjunta nao fixa area nem entropia marginal. OH adiado.','estatuto':'DERIVED','status':'EM_CURSO','veredito':'PASS_COMPONENT_WITH_SCOPE','olhou_dados':False,'nao_refazer':'Rede/Fock/Takesaki e H3 nulo fixo preservados. A reconstrucao do registro ja existe.','defeito':'H3 universal e derivacao independente da area continuam abertas.','proximo_passo':'Derivar o coeficiente inducedArea da mesma dinamica/fonte em cada ponto e direcao; nao definir area por entropia.','artefatos':[str(delivery),str(ROOT/'ANALISE_R81.txt'),str(ROOT/'RecoveryAreaCoefficient.lean')],'onde':str(ROOT),'refs':['formal.f1_rede.concrete_bosonic_kinematics']})
    mapped=command('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',ACTOR['id']])
    boarded=command('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R81: recuperacao e coeficiente H3 revisados; alcance condicional. OH adiado. Oito memorias append/backup; sem dado/produção/gate.'])
    new('REGISTRATION_R81.json',{'delivery':pin(delivery),'map':pin(mapped),'board':pin(boarded)})
    p=project('SUBMIT_SYNC');task=next(x for x in p['projection']['active'] if x['id']==TASK)
    mutate('submit','SUBMIT',task_id=TASK,lease_id=task['lease']['id'],evidence=[pin(delivery),pin(ROOT/'REVIEW_R81.json')])
    s=call({'operation':'get','reference':REF},'GET_FINAL','session_memory.py')
    flow=dict(s['p']);flow['phase']='h3_recovery_coefficient_reviewed';flow['next_action']='R81 revisada: recuperacao do registro ja existe; ponte B=eta*A2 condicional explicita. Buscar derivacao geometrica do coeficiente da mesma fonte, sem reabrir OH; H3 universal OPEN. Revisao/aceite R13 distintos do fecho global. Nenhum 5sigma calculado.'
    call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r81-recovery-h3-recorded','changes':{'records':[{'id':'r81-recovery-h3','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']},{'kind':'artifact','ref':str(ROOT/'ORIGEM.txt'),'sha256':pin(ROOT/'ORIGEM.txt')['sha256']}],'text':extra.decode('utf-8')}],'flow':flow}},'FINAL_TRANSITION','session_memory.py')
    print(delivery)
if __name__=='__main__':main()
