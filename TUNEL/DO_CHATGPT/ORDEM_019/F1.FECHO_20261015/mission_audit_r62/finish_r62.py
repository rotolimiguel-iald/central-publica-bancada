"""Deliver reviewed R62 audit and finite readout component without full acceptance."""
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
import support_r62 as s

def once(label,args):
    s.new(label+'_INTENT.json',{'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp=subprocess.run(args,capture_output=True,encoding='utf8')
    receipt=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode:raise RuntimeError(str(receipt))
    print(cp.stdout[:1000]);return receipt

def main():
    s.preflight('R4','DELIVERY')
    review=json.loads((s.ROOT/'FINAL_REVIEW_R62.json').read_text(encoding='utf8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for row in review['evidence']:assert s.pin(row['path'])['sha256']==row['sha256']
    result=json.loads((s.ROOT/'run_r62/RESULT_R62.json').read_text(encoding='utf8'))
    assert result['status']=='PASS_FINITE_SYNTHETIC_READOUT'
    names=['RELATORIO_R62.txt','AUDIT_MISSION_R62.json','PREPARED_READOUT_PLAN_R62.json',
      'PREEXEC_REVIEW_R62.json','ROOT_PREEXEC_REVIEW_R62.json','run_prepared_readout_r62_r2.py',
      'FREEZE_READOUT_R62.json','DELIVERY_READOUT_R62.json',
      'finite_device_functions_r62.py','AST_EXTRACTION_R62.json','run_r62/RESULT_R62.json',
      'FINAL_REVIEW_R62.json','MEMORY_APPLIED_R62.json','MEMORY_REVIEW_R62.json','MEMORY_REVIEW_R62_R1.json',
      'sources/DELIVERY_R1.json','REQUIREMENT_PINS_R62.json','VERSION_PINS_R62.json']
    delivery=s.new('DELIVERY_INTEGRATED_R62.json',{'status':'REVIEWED_AUDIT_AND_FINITE_READOUT','unit':'F1.FECHO_20261015',
      'claim':939,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'reference':s.pin(s.REF),'evidence':[s.pin(s.ROOT/n) for n in names],
      'result':'Reused full joint generator; four cross-quadrature expectations reconstruct C and B including OH correlations and losses in the finite model.',
      'R4_R5_integrally_satisfied':False,'canonical_changed':False,'betaTGL_measured':False,
      'provider_calls':0,'observed_data':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R62.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics',
      'dominio':'FORMAL','titulo':'R62: apanhado da missao e leitor quadratico sobre gerador conjunto reaproveitado',
      'metodo':'Conferencia dos aceites e pinos, levantamento dirigido, plano pinado e teste sintetico com gerador existente; revisao independente.',
      'resultado':'Quatro expectativas cruzadas recuperam C/B e covariancias no corte, sem eliminar OH. R4/R5 e rito/revisao final permanecem abertos.',
      'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
      'defeito':'Acesso e calibracao fisica dos dois modos, estado do dispositivo e limite/entrelacamento com a rede permanecem por demonstrar.',
      'nao_refazer':'Nao reconstruir Fock/Takesaki/Maxwell aceitos nem Liouvilliano64 existente. Reusar decoder R62 no proximo contrato.',
      'proximo_passo':'Confrontar preparo/receptor fisicos com o contrato tipado e ligar forma de duas pontas, estados e dinamica aos pacotes de rede existentes.',
      'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R62.txt')],'onde':str(s.ROOT)})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],
      '--status','EM_CURSO','--evidencia',str(delivery),'--nota','R62: revisao dos aceites e versoes; leitura quadratica C/B testada no gerador conjunto existente. Sem beta medida ou aceite integral R4/R5.'])
    reg=s.new('REGISTRATION_R62.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINISH_GET');hs=state['p']['handles']
    for h in hs:
        if h['id'] in ('r62-audit','r62-sources','r62-readout'):h.update(status='completed',result=s.pin(delivery))
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':state['revision'],'event_id':'r62-reviewed-audit-readout-custodied',
      'changes':{'records':[{'id':'r62-audit-and-readout-result','kind':'fact','statute':'DERIVED',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in [delivery,reg]],
        'text':'R62: aceites conferidos no proprio escopo; canonico v393 distinto do app v392 e candidatos. Gerador conjunto finito existente reutilizado; quatro quadraturas recuperam C/B e covariancias sem descartar OH, com controles negativos. Nao mede beta nem implementa POVM fisica. R4/R5 seguem abertos; R3/R10 dependem deles.'}],
        'flow':{'phase':'r62_reviewed_audit_and_readout_custodied','next_action':'Reusar decoder quadratico e gerador conjunto; completar mapa fisico do preparo/receptor e compatibilidade dos estados/dinamica com a rede. Preservar aceites existentes e limites H3.','handles':hs}}},'FINISH_TRANSITION')
    print(delivery)

if __name__=='__main__':main()
