"""Register the independently reviewed documentary OH mirror component."""
import json,subprocess,sys,datetime as dt
import support_r79 as s
def once(label,args):
    s.new(label+'_INTENT.json',{'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    r=subprocess.run(args,capture_output=True,encoding='utf-8')
    p=s.new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(str(p))
    return p
def main():
    assert sys.argv[1:]==['--apply']
    assert not (s.ROOT/'DELIVERY_R79.json').exists()
    rv=json.loads((s.ROOT/'REVIEW_R79.json').read_text(encoding='utf-8'))
    assert rv['status'].startswith('PASS') and rv['reviewer']!=s.ACTOR['id']
    for e in rv['evidence']:assert s.pin(e['path'])==e
    for n in ['RELATORIO_R79.md','SOURCE_PINS_DRIVE_R79.json','OPTICAL_DRIVE_BRIDGE_R79.md','CUT_RESPONSE_BOUND_R79.md','MATERIAL_IDENTIFICATION_R79.md','SHEET_SCATTERING_R79.md','RESULT_R79.json','FREEZE_R79.json','ORIGEM_R79.txt','MEMORY_PLAN_R79.json','MEMORY_APPEND_R79.txt','memory_r79.py','finish_r79.py','support_r79.py']:
        assert s.pin(s.ROOT/n) in rv['evidence'],n
    for manifest in ['SOURCE_PINS_DRIVE_R79.json','CUT_RESPONSE_SOURCES_R79.json','SOURCE_PINS_MATERIAL_R79.json']:
        for e in json.loads((s.ROOT/manifest).read_text(encoding='utf-8'))['sources']:
            assert s.pin(e['path'])['sha256']==e['sha256']
    s.check('FINISH_CHECK')
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r79.py'),'apply'])
    delivery=s.new('DELIVERY_R79.json',{'status':'REVIEWED_SYNTHETIC_CONDITIONAL_COMPONENT','unit':'F1.FECHO_20261015','claim':967,'scope_event':983,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'evidence':[s.pin(p) for p in sorted(s.ROOT.iterdir()) if p.is_file()],
        'scope':'Coherent port-drive bridge, analytic uniform continuum tail of first variation, and material sheet/bright-mode contract; one preregistered cut refinement. Device calibration remains OPEN.',
        'R4_R5_integrally_satisfied':False,'scientific_executions':1,'physical_measurements':0,'new_lean_builds':0,'canonical_changed':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R79.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R79: drive optico, limite continuo da resposta e contorno material',
        'metodo':'Reuso R66/R74/R75/R78; derivacao da entrada coerente, cauda ponderada uniforme e contrato dipolar/folha. Plano/corte por cota antes da execucao unica; revisao distinta; backups.',
        'resultado':(s.ROOT/'MAP_SUMMARY_R79.txt').read_text(encoding='utf-8'),
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Calibracao do MESMO aparelho e textura de correlacao do banho J abertas. Ponte do drive demonstrada para H_COHERENT_PORT1; cauda continua distinta de erro numerico sem enclosure. Nao inferir 5sigma ou equivalencia S_sheet=S_beta.',
        'nao_refazer':'Reusar R57/R66/R73/R74/R78/R79. Nao repetir refinamento8. Contrato de porta e cota de derivada agora existentes; nao voltar a perguntar mecanismo de reconhecimento.',
        'proximo_passo':'Identificar perfis/populacoes/regime do MESMO dispositivo, projetar bomba no modo brilhante e conferir banho comum que realiza J; preservar resultado refinado e suas cotas.',
        'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R79.md'),str(s.ROOT/'ORIGEM_R79.txt')],'onde':str(s.ROOT),'refs':['formal.anchored_name_contour']})
    mapped=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    boarded=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R79 revisada: ponte coerente de entrada, limite uniforme/cota da derivada e contrato material/folha; refinamento unico registrado. R4/R5 integrais abertos; memoria com backups, sem producao/gate.'])
    reg=s.new('REGISTRATION_R79.json',{'delivery':s.pin(delivery),'map':s.pin(mapped),'board':s.pin(boarded)})
    s.mutate('release','RELEASE_R4',task_id='R4',reason='R79 componentes de drive/cota/folha revisados e refinamento unico custodiado. Calibracao material, banho comum e realizacao global continuam abertos; limite da primeira variacao demonstrado no dominio nomeado.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r79-optical-drive-continuum-recorded','changes':{
        'records':[{'id':'r79-optical-drive-continuum','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg,s.ROOT/'ORIGEM_R79.txt')],'text':(s.ROOT/'MEMORY_APPEND_R79.txt').read_text(encoding='utf-8')}],
        'flow':{'phase':'r79_optical_drive_continuum_reviewed','next_action':'R79 ja entrega drive coerente do porto, limite uniforme/cota da primeira variacao e folha material com r/t/absorcao condicionais. Refinamento8 executado uma vez, nao repetir. Proximo: identificar perfis/populacoes, erro de reducao OH e textura do banho comum no MESMO dispositivo; Gamma e realizacao global abertas. Consultar fontes; claim/check antes de avancar. R3/R10 exigem revalidacao final.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    post=s.project('POST_DELIVERY_PROJECT')
    s.new('POST_DELIVERY_VERIFIED_R79.json',{'delivery':s.pin(delivery),'registration':s.pin(reg),'revision':post['receipt']['revision'],'projection_sha256':post['projection_sha256'],'active':[{k:x.get(k) for k in ['id','status','lease']} for x in post['projection']['active']]})
    print(delivery)
if __name__=='__main__':main()
