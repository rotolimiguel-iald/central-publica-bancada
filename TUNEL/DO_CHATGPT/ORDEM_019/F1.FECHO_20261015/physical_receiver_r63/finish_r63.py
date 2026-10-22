"""Custody of reviewed receiver mathematics; no acceptance of full R4/R5."""
import datetime as dt
import json
import subprocess
import sys
import support_r63 as s


def once(label, command):
    s.new(label+'_INTENT.json', {'command':command,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp=subprocess.run(command,capture_output=True,encoding='utf-8')
    out=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode: raise RuntimeError(str(out))
    print(cp.stdout[:1000])
    return out


def main():
    s.preflight('R4','DELIVERY_R63')
    review=json.loads((s.ROOT/'FINAL_REVIEW_R63.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for p in review['evidence']:
        assert s.pin(p['path'])['sha256']==p['sha256']
    result=json.loads((s.ROOT/'receiver/RESULT_R63.json').read_text(encoding='utf-8'))
    assert result['status']=='PASS_EXACT_COMPRESSED_HOMODYNE'
    assert len(result['checks'])==18 and all(c['passed'] for c in result['checks'])
    names=['RELATORIO_R63.txt','receiver/DELIVERY_RECEIVER_R63.json','receiver/DERIVACAO_RECEPTOR_R63.md',
           'receiver/PLAN_R63.json','receiver/START_R63.json','receiver/RESULT_R63.json',
           'receiver/verify_compressed_homodyne_r63.py','sources/DELIVERY_R1.json',
           'sources/PHYSICAL_RECEIVER_MAP_R1.json','sources/PHYSICAL_RECEIVER_MAP_R1.txt',
           'sources/SOURCE_PINS_AND_ANCHORS_R1.json','CANONICAL_PINS_R63.json',
           'FINAL_REVIEW_R63.json','MEMORY_REVIEW_R63.json','MEMORY_APPLIED_R63.json',
           'BOARD_RENEW_R63.json','R5_RELEASE_RESULT.json']
    delivery=s.new('DELIVERY_INTEGRATED_R63.json',{
        'status':'REVIEWED_COMPRESSED_HOMODYNE_COMPONENT','unit':'F1.FECHO_20261015',
        'claim':952,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'reference':s.pin(s.REF),'evidence':[s.pin(s.ROOT/n) for n in names],
        'result':'Bosonic homodyne POVM compression: second moment defect cancels in cross-quadrature decoder. Kinematic state inclusion reuses Fock; physical dynamics and receiver calibration remain explicit.',
        'exact_algebra_checks':18,'R4_R5_integrally_satisfied':False,
        'canonical_changed':False,'betaTGL_measured':False,'provider_calls':0,'observed_data':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R63.json',{
        'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
        'titulo':'R63: POVM homodina comprimida preserva o decoder cruzado; mapa fisico de receptor e escalas',
        'metodo':'Reuso dirigido de14fontes, derivacao e18identidades simbolicas exatas; revisao independente; sem nova trajetoria.',
        'resultado':'PX2P=(PXP)^2+n; excesso ni+no cancela em Qmais-Qmenos. Contagem R7 reutilizada; amplitude coerente e intensidade total distinguidas; parametros sinteticos nao sao calibracao.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Preparo material, pacotes/portas/filtros calibrados e entrelacamento dinamico/localizacao com rede ainda abertos.',
        'nao_refazer':'Nao repetir18identidades, decoderR62, gerador64 ou Fock/Takesaki aceitos. Reusar quadro giranteR57 com suas hipoteses.',
        'proximo_passo':'Construir vinculo do campo temporal coletado aos modos da cavidade no quadro girante, com preparo e calibracoes explicitos.',
        'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R63.txt')],'onde':str(s.ROOT)})
    mr=once('MAP_REGISTER_R63',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER_R63',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R63: POVM bosonica comprimida,18identidades e decoder preservado; fontes/calibracoes separadas. Sem aceite integralR4/R5 ou beta medido.'])
    reg=s.new('REGISTRATION_R63.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINISH_GET_R63')
    handles=state['p']['handles']
    for h in handles:
        if h['id'] in ('r63-sources','r63-receiver','r63-review'):
            h.update(status='completed',result=s.pin(delivery))
    s.call('session_memory.py',{
        'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
        'expected_revision':state['revision'],'event_id':'r63-reviewed-receiver-custodied',
        'changes':{'records':[{
            'id':'r63-bosonic-compressed-receiver','kind':'fact','statute':'DERIVED',
            'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg)],
            'text':'R63: POVM homodina bosonica comprimida tem segundo momento M1^2+n; excesso local cancela no decoderC/B.18identidades exatas, revisao independente. Inclusao cinematica de estados na Fock, sem entrelacamento dinamico. R7contagem e quadro giranteR57 reutilizados; |<a>|^2 nao e contagem total em|1>, razao de frequencias sinteticas1.2 nao calibra projetoOH/780nm. R4/R5 abertos; R5 liberado explicitamente ocioso, provas/criterios preservados; R3/R10 dependem dessas pontes. Sem medicao de beta ou mudanca de gate.'}],
            'flow':{'phase':'r63_reviewed_receiver_custodied','next_action':'Vincular campo temporal coletado aos modos de cavidade no quadro girante ja existente, com preparo/portas/filtros/calibracao explicitos; depois compatibilidade dinamica/localizacao com rede. Reusar POVM R63 e decoder R62.','handles':handles}}},'FINISH_TRANSITION_R63')
    print(delivery)


if __name__=='__main__':main()
