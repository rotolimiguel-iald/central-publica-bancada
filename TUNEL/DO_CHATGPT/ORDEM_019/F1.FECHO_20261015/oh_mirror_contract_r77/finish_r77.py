"""Register the independently reviewed documentary OH mirror component."""
import json,subprocess,sys,datetime as dt
import support_r77 as s
def once(label,args):
    s.new(label+'_INTENT.json',{'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    r=subprocess.run(args,capture_output=True,encoding='utf-8')
    p=s.new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(str(p))
    return p
def main():
    assert sys.argv[1:]==['--apply']
    assert not (s.ROOT/'DELIVERY_R77.json').exists()
    rv=json.loads((s.ROOT/'REVIEW_R77.json').read_text(encoding='utf-8'))
    assert rv['status'].startswith('PASS') and rv['reviewer']!=s.ACTOR['id']
    for e in rv['evidence']:assert s.pin(e['path'])==e
    for n in ['RELATORIO_R77.md','SOURCE_PINS_R77.json','SOURCE_EXCERPTS_R77.txt','ORIGEM_R77.txt','MEMORY_PLAN_R77.json','MEMORY_APPEND_R77.txt','memory_r77.py','finish_r77.py','support_r77.py']:
        assert s.pin(s.ROOT/n) in rv['evidence'],n
    for e in json.loads((s.ROOT/'SOURCE_PINS_R77.json').read_text(encoding='utf-8'))['sources']:
        assert s.pin(e['path'])['sha256']==e['sha256']
    s.check('FINISH_CHECK')
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r77.py'),'apply'])
    delivery=s.new('DELIVERY_R77.json',{'status':'REVIEWED_DOCUMENTARY_CONDITIONAL_COMPONENT','unit':'F1.FECHO_20261015','claim':967,'scope_event':979,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'evidence':[s.pin(p) for p in sorted(s.ROOT.iterdir()) if p.is_file()],
        'scope':'OH face and mirror interpretation preserved; R57/R74 re-used; passive conditional dilation; R76 vacuum target separated from phase transmission; local dimensional issue documented.',
        'R4_R5_integrally_satisfied':False,'scientific_executions':0,'physical_measurements':0,'new_lean_builds':0,'canonical_changed':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R77.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R77: face hidroxila, espelhamento e alvo de fase corrigido',
        'metodo':'Fontes por SHA/linhas, fala do operador em custodia, reuso R57/R66/R74 e revisao distinta. Derivacao condicional sem nova campanha.',
        'resultado':'M=g_OH S_beta conserva abertura e admite dilatacao passiva se |g_OH|<=1. Vazio OH da R76 nao e requisito geral da transmissao de fase. Face OH e parede requerem identificacao material; mapa de radicalizacao precisa reter fase.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Resposta material, Gamma independente, codificador de campos/superficie e realizacao global continuam abertos. luz.tex:208-218 contem discrepancia dimensional e marcador de prova, sem conclusao de ausencia universal.',
        'nao_refazer':'Reusar leitor/decoder R57, fase/instrumento R74 e gerador R66. Nao repetir R76 nem pedir novamente mecanismo de reconhecimento.',
        'proximo_passo':'Recuperar/derivar mapa material da face OH e resposta do gerador para comparacao de transferencia complexa; preregistro antes de nova execucao.',
        'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R77.md'),str(s.ROOT/'ORIGEM_R77.txt')],'onde':str(s.ROOT),'refs':['formal.anchored_name_contour']})
    mapped=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    boarded=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R77 revisada: OH face, espelhamento canal; reuso R57/R74, alvo R76 delimitado; memoria com backup. R4/R5 integrais abertos, sem campanha/producao/gate.'])
    reg=s.new('REGISTRATION_R77.json',{'delivery':s.pin(delivery),'map':s.pin(mapped),'board':s.pin(boarded)})
    s.mutate('release','RELEASE_R4',task_id='R4',reason='R77 documental revisada; alvo de fase corrigido por esclarecimento do operador. Resposta material e calibracao permanecem abertas.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r77-oh-mirror-correction-recorded','changes':{
        'records':[{'id':'r77-oh-mirror-contract','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg,s.ROOT/'ORIGEM_R77.txt')],'text':(s.ROOT/'MEMORY_APPEND_R77.txt').read_text(encoding='utf-8')}],
        'flow':{'phase':'r77_oh_mirror_contract_reviewed','next_action':'OH fornece a face; espelhamento e o canal segundo esclarecimento do operador. Reusar R57/R64/R66/R74 para derivar resposta complexa material e mapa entre face OH e fronteira; nao tratar vazio OH da R76 como alvo necessario. Calibracao Gamma e realizacao global abertas. Preservar fase no radical; consultar acervo antes de construir. Nenhuma campanha repetida; claim/check antes de avancar.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    post=s.project('POST_DELIVERY_PROJECT')
    s.new('POST_DELIVERY_VERIFIED_R77.json',{'delivery':s.pin(delivery),'registration':s.pin(reg),'revision':post['receipt']['revision'],'projection_sha256':post['projection_sha256'],'active':[{k:x.get(k) for k in ['id','status','lease']} for x in post['projection']['active']]})
    print(delivery)
if __name__=='__main__':main()
