"""Register the independently reviewed documentary OH mirror component."""
import json,subprocess,sys,datetime as dt
import support_r78 as s
def once(label,args):
    s.new(label+'_INTENT.json',{'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    r=subprocess.run(args,capture_output=True,encoding='utf-8')
    p=s.new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(str(p))
    return p
def main():
    assert sys.argv[1:]==['--apply']
    assert not (s.ROOT/'DELIVERY_R78.json').exists()
    rv=json.loads((s.ROOT/'REVIEW_R78.json').read_text(encoding='utf-8'))
    assert rv['status'].startswith('PASS') and rv['reviewer']!=s.ACTOR['id']
    for e in rv['evidence']:assert s.pin(e['path'])==e
    for n in ['RELATORIO_R78.md','SOURCE_PINS_NORMALIZACOES_R78.json','NORMALIZACOES_R78.md','RESULT_R78.json','FREEZE_R78.json','ORIGEM_R78.txt','MEMORY_PLAN_R78.json','MEMORY_APPEND_R78.txt','memory_r78.py','finish_r78.py','support_r78.py']:
        assert s.pin(s.ROOT/n) in rv['evidence'],n
    for e in json.loads((s.ROOT/'SOURCE_PINS_NORMALIZACOES_R78.json').read_text(encoding='utf-8'))['sources']:
        assert s.pin(e['path'])['sha256']==e['sha256']
    s.check('FINISH_CHECK')
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r78.py'),'apply'])
    delivery=s.new('DELIVERY_R78.json',{'status':'REVIEWED_SYNTHETIC_CONDITIONAL_COMPONENT','unit':'F1.FECHO_20261015','claim':967,'scope_event':981,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'evidence':[s.pin(p) for p in sorted(s.ROOT.iterdir()) if p.is_file()],
        'scope':'R66 generator and R74 instrument reused in one finite-cut transient response calculation; dimensional normalizations located; physical mapping remains OPEN.',
        'R4_R5_integrally_satisfied':False,'scientific_executions':1,'physical_measurements':0,'new_lean_builds':0,'canonical_changed':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R78.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R78: resposta complexa OH-luz em corte finito e normalizacoes recuperadas',
        'metodo':'Fontes por SHA/linhas; plano e codigo revisados/fixados antes de uma execucao sintetica. Duhamel versus diferencas centrais; revisao distinta e backups de memoria.',
        'resultado':'93 checks/exit0. Respostas maximas a probes adimensionais: com semente3.2665e-7; sem semente2.5429e-9; bloqueada5.421e-20. Escalas F0/rho0/OH/geometria localizadas; prefator material nao determinado.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Mapa material/drive fisico e Gamma independente abertos; sem cota continua para os novos probes. h- em coordenadas de controle nao identifica canal optico. Consistencia numerica nao e sigma fisico.',
        'nao_refazer':'Reusar R57/R73/R74/R66. R78 ja executada uma vez; nao repetir. Nao exigir vacuo OH para transmissao de fase.',
        'proximo_passo':'Recuperar/derivar conversao drive optico-controles XP e identificacao da superficie OH com o gerador; estabelecer alcance de corte antes de nova execucao.',
        'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R78.md'),str(s.ROOT/'ORIGEM_R78.txt')],'onde':str(s.ROOT),'refs':['formal.anchored_name_contour']})
    mapped=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    boarded=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R78 revisada: uma execucao sintetica, 93 checks/exit0; resposta complexa finita e normalizacoes localizadas. Memoria com backup; R4/R5 integrais abertos, sem producao/gate.'])
    reg=s.new('REGISTRATION_R78.json',{'delivery':s.pin(delivery),'map':s.pin(mapped),'board':s.pin(boarded)})
    s.mutate('release','RELEASE_R4',task_id='R4',reason='R78 componente sintetico/documental revisado, executado uma vez e custodiado. Mapa material, calibracao e limite continuo dos novos probes permanecem abertos.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r78-oh-complex-response-recorded','changes':{
        'records':[{'id':'r78-oh-complex-response','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg,s.ROOT/'ORIGEM_R78.txt')],'text':(s.ROOT/'MEMORY_APPEND_R78.txt').read_text(encoding='utf-8')}],
        'flow':{'phase':'r78_oh_response_reviewed','next_action':'R78 executada uma vez: resposta transitoria complexa do corte3 e normalizacoes recuperadas. Nao repetir. Proximo: conversao drive optico-probes XP e identificacao face OH-gerador; controlar limite continuo dos novos probes. Gamma/calibracao e realizacao global abertas. Reusar R57/R73/R74, nao tratar vacuoOH como alvo de fase. Consultar acervo; claim/check antes de avancar.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    post=s.project('POST_DELIVERY_PROJECT')
    s.new('POST_DELIVERY_VERIFIED_R78.json',{'delivery':s.pin(delivery),'registration':s.pin(reg),'revision':post['receipt']['revision'],'projection_sha256':post['projection_sha256'],'active':[{k:x.get(k) for k in ['id','status','lease']} for x in post['projection']['active']]})
    print(delivery)
if __name__=='__main__':main()
