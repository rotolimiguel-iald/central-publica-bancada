"""Register reviewed R80; originals and production stay untouched."""
import datetime as dt
import json
import subprocess
import sys
import support_r80 as s

def once(label, args):
    s.new(label+'_INTENT.json', {'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    p=subprocess.run(args,capture_output=True,encoding='utf-8')
    receipt=s.new(label+'_RESULT.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:raise RuntimeError(str(receipt))
    return receipt

def main():
    assert sys.argv[1:]==['--apply']
    assert not (s.ROOT/'DELIVERY_R80.json').exists()
    review=json.loads((s.ROOT/'REVIEW_R80.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for e in review['evidence']:assert s.pin(e['path'])==e
    required=['RESUMO_VIGENTE_R80.md','RELATORIO_R80.md','MATERIAL_AUDIT_R80.md','BATH_IDENTIFICATION_R80.md','SOURCE_PINS_R80.json','MATERIAL_DATA_STATUS_R80.json','material_contract_r80_r2.py','RESULT_TESTS_R80_R2.json','PREREG_TESTS_R80_R2.json','ERRATA_VALIDATOR_R80.md','ORIGEM_R80.txt','MEMORY_PLAN_R80.json','MEMORY_APPEND_R80_R2.txt','memory_r80_r2.py','finish_r80.py','support_r80.py']
    for n in required:assert s.pin(s.ROOT/n) in review['evidence'],n
    for e in json.loads((s.ROOT/'SOURCE_PINS_R80.json').read_text(encoding='utf-8'))['sources']:
        assert s.pin(e['path'])['sha256']==e['sha256']
    s.check('FINISH_CHECK')
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r80_r2.py'),'apply'])
    delivery=s.new('DELIVERY_R80.json',{'status':'REVIEWED_CONDITIONAL_MATERIAL_COMPONENT','unit':'F1.FECHO_20261015','claim':985,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'evidence':[s.pin(p) for p in sorted(s.ROOT.iterdir()) if p.is_file()],
        'R4_R5_integrally_satisfied':False,'trajectories':0,'physical_measurements':0,'new_lean_builds':0,'canonical_changed':False,'gate_changed':False,
        'current_validator':'material_contract_r80_r2.py','historical_validator':'material_contract_r80.py SUPERSEDED_PSD_FINDING'})
    entry=s.new('MAP_ENTRY_R80.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R80: identificacao OH/optica e criterios de banho comum',
        'metodo':'Reuso R65/R66/R74/R79; cinco textos de projeto/artigo; Gram/fase/bright; validador sintetico com correcao PSD independente.',
        'resultado':(s.ROOT/'RESUMO_VIGENTE_R80.md').read_text(encoding='utf-8'),
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Identidade RF/optico/envelope e conversor/banho material nao identificados nesta cobertura. R1 do validador superada; R2 vigente.',
        'nao_refazer':'Reusar R65/R66/R74/R78/R79. Niveis OH existem; nao confundir Lambda doubling com conversor Raman. Nenhuma nova trajetoria.',
        'proximo_passo':'Identificar ou derivar conversor e correlacoes do mesmo dispositivo a partir dos componentes documentados, sem preencher calibracao por exemplos sinteticos.',
        'artefatos':[str(delivery),str(s.ROOT/'RESUMO_VIGENTE_R80.md'),str(s.ROOT/'MATERIAL_AUDIT_R80.md')],'onde':str(s.ROOT),'refs':['formal.f1_rede.concrete_bosonic_kinematics']})
    mapped=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    boarded=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R80 revisada: inventario material, contrato de banho/fase/bright e validador R2 31checks. R1 superada por achado PSD preservado. R4/R5 abertos; memoria com backups; zero trajetorias/producao/gate.'])
    reg=s.new('REGISTRATION_R80.json',{'delivery':s.pin(delivery),'map':s.pin(mapped),'board':s.pin(boarded)})
    s.mutate('release','RELEASE_R4',task_id='R4',reason='R80 revisada: criterios e inventario entregues, conversor/material e rede global abertos; nao usar fixtures como calibracao.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r80-material-bath-recorded','changes':{
        'records':[{'id':'r80-material-bath','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg,s.ROOT/'ORIGEM_R80.txt')],'text':(s.ROOT/'MEMORY_APPEND_R80_R2.txt').read_text(encoding='utf-8')}],
        'flow':{'phase':'r80_material_bath_reviewed','next_action':'R80 entrega inventario OH/optica e contrato executavel R2 de banho/fase/bright. Niveis OH e EOM existem; falta identificar o mapa fisico RF/optico/envelopes e reservatorio comum do mesmo aparelho. Nao repetir trajetorias R78/R79 nem atribuir calibracao aos fixtures. R4/R5 abertos; R3/R10 revalidacao final. Claim/check antes de continuar.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    post=s.project('POST_DELIVERY_PROJECT')
    s.new('POST_DELIVERY_VERIFIED_R80.json',{'delivery':s.pin(delivery),'registration':s.pin(reg),'revision':post['receipt']['revision'],'active':[{k:x.get(k) for k in ['id','status','lease']} for x in post['projection']['active']]})
    print(delivery)

if __name__=='__main__':main()
