"""Integrate reviewed finite R61 component; no full R4/R5 acceptance."""
import datetime as dt
import json
import subprocess
import sys
import support_r61 as s

def once(label,args):
    s.new(label+'_INTENT.json',{'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp=subprocess.run(args,capture_output=True,encoding='utf8')
    receipt=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode:raise RuntimeError(str(receipt))
    print(cp.stdout[:900]);return receipt

def main():
    s.preflight('R4','DELIVERY')
    review=json.loads((s.ROOT/'FINAL_REVIEW_R61.json').read_text(encoding='utf8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for row in review['evidence']:assert s.pin(row['path'])['sha256']==row['sha256']
    files=['RELATORIO_R61.txt','RELATORIO_CANDIDATO_R61.md','SCOPE_R61.json','DELIVERY_R61.json',
      'CUSTODY_R61.json','FINAL_REVIEW_R61.json','FINAL_REVIEW_R61_ADDENDUM_R1.json','MEMORY_APPLIED_R61.json','MEMORY_REVIEW_R61.json',
      'independent_review/INDEPENDENT_RESULT_R61.json','independent_review/verify_independent_r61.py']
    recovery=s.ROOT.parent/'r4_recovery_authorized_20261017/RECOVERY_RESULT.json'
    delivery=s.new('DELIVERY_INTEGRATED_R61.json',{'status':'REVIEWED_FINITE_COMPONENT_R4_RECOVERED','unit':'F1.FECHO_20261015',
      'claim':939,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'reference':s.pin(s.REF),'evidence':[s.pin(s.ROOT/n) for n in files]+[s.pin(recovery)],
      'result':'Finite optical pair dynamics require joint optical-OH correlations; equal optical marginals can have unequal derivatives.',
      'R4_recovery_executed':True,'criteria_and_previous_results_preserved':True,
      'R4_R5_integrally_satisfied':False,'original_scientific_execution_repeated':False,
      'independent_identity_verification':True,'betaTGL_measured':False,
      'provider_calls':0,'observed_data':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R61.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics',
      'dominio':'FORMAL','titulo':'R61: R4 recuperada; pares dependem de correlacoes conjuntas optica-OH no corte finito',
      'metodo':'Custodia da exploracao R59 e verificacao independente das identidades e do contramodelo, sem repetir o script original.',
      'resultado':'C/B exigem correlacoes auxiliares; marginais iguais com derivadas diferentes. Autorizacao administrativa executada e provas preservadas.',
      'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
      'defeito':'Fecho reduzido C/B nao autonomo; preparo conjunto/receptor e limite bosonico nao demonstrados.',
      'nao_refazer':'Exploracao R59, leitura R60 e recuperacao administrativa R4 concluidas; nao repetir execucoes.',
      'proximo_passo':'Especificar preparo conjunto e observavel do receptor; transportar correlacoes auxiliares ou justificar reducao.',
      'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R61.txt')],'onde':str(s.ROOT)})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],
      '--status','EM_CURSO','--evidencia',str(delivery),'--nota','R61: recuperacao R4 autorizada concluida; pares no corte finito revisados, nao fechamento reduzido localizado. Sem repetir execucao anterior ou satisfazer integralmente R4/R5.'])
    reg=s.new('REGISTRATION_R61.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINISH_GET');hs=state['p']['handles']
    for h in hs:
        if h['id']=='r61-oh-custody':h.update(status='completed',result=s.pin(delivery))
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':state['revision'],'event_id':'r61-reviewed-oh-component-custodied-20261017',
      'changes':{'records':[{'id':'r61-finite-oh-component-result','kind':'fact','statute':'DERIVED',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in [delivery,reg]],
        'text':'R61: a recuperacao administrativa R4 foi autorizada e executada. A exploracao R59 foi custodiada/revisada sem repetir script; no corte 2x2x2 os pares C/B pedem correlacoes optica-OH. Estados com marginais iguais tem derivadas diferentes; fecho reduzido nao autonomo. Nao mede beta nem transfere lambda/2 ao dominio bosonico. R4/R5 seguem abertos; R3/R10 em revalidacao.'}],
        'flow':{'phase':'r61_reviewed_finite_oh_component_custodied','next_action':'Reusar R59/R60/R61; especificar preparo conjunto e receptor e justificar fecho de correlacoes. Autorizacao administrativa R4 resolvida.','handles':hs}}},'FINISH_TRANSITION')
    print(delivery)

if __name__=='__main__':main()
