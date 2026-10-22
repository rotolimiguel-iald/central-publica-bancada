"""Register reviewed conditional R60 readout; do not accept R4 or R5."""
import datetime as dt
import json
import subprocess
import sys
import support_r60 as s

def once(label,args):
    s.new(label+'_INTENT.json',{'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp=subprocess.run(args,capture_output=True,encoding='utf8')
    receipt=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode:raise RuntimeError(str(receipt))
    print(cp.stdout[:900]);return receipt

def main():
    s.preflight('R5','DELIVERY')
    review=json.loads((s.ROOT/'FINAL_REVIEW_R60.json').read_text(encoding='utf8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for row in review['evidence']:assert s.pin(row['path'])['sha256']==row['sha256']
    files=['RELATORIO_R60.txt','PREREG_R60.json','RESULT_R60.json','verify_readout_r60.py',
           'ROOT_SOURCE_PINS_R60.json','FINAL_REVIEW_R60.json','MEMORY_APPLIED_R60.json','MEMORY_REVIEW_R60.json']
    sources=sorted(p for p in (s.ROOT/'sources').iterdir() if p.is_file())
    assert sources,'Documentary survey missing'
    delivery=s.new('DELIVERY_R60.json',{'status':'REVIEWED_CONDITIONAL_READOUT_COMPONENT','unit':'F1.FECHO_20261015',
      'claim':939,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'reference':s.pin(s.REF),'evidence':[s.pin(s.ROOT/n) for n in files]+[s.pin(p) for p in sources],
      'result':'Cross-ratio identifies generic channel b under stable separable gains; pair moments identify n and efficiencies only under pure-source/vacuum-loss assumptions.',
      'counterexamples':['Configuration-dependent gains','Mixed source with indistinguishable output moments'],
      'existing_bridge':'Ponte identifies reflection with beta; measurement access to obs/hid sectors not supplied by that identity.',
      'betaTGL_measured':False,'R4_recovery_executed':False,'R4_R5_integrally_satisfied':False,
      'provider_calls':0,'observed_data':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R60.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics',
      'dominio':'FORMAL','titulo':'R60: leitura relacional com ganhos/perdas e contramodelos de identificabilidade',
      'metodo':'Acervo existente, pré-registro de modelos condicionais, 34 verificações exatas e revisão independente.',
      'resultado':'Razão cruzada recupera b genérico; pares recuperam n/eficiências sob pureza e perda no vácuo. Sem medição beta ou poder físico.',
      'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
      'defeito':'Acesso a ambas entradas/saídas obs/hid e controle de preparo não demonstrados; ganho variável e mistura tornam a inversão ambígua.',
      'nao_refazer':'Reutilizar SMatrix/Ponte e pares R59; não identificar rho com beta/chi/ângulo passivo.',
      'proximo_passo':'Localizar o mapa físico de acesso/leitura; R4 continua aguardando recuperação administrativa autorizada.',
      'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R60.txt')],'onde':str(s.ROOT)})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],
      '--status','EM_CURSO','--evidencia',str(delivery),'--nota','R60: modelos de leitura relacionais revisados, contramodelos explícitos; memória com backup. Sem medição beta, aceite R5 ou recuperação R4.'])
    reg=s.new('REGISTRATION_R60.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINISH_GET');hs=state['p']['handles']
    for h in hs:
        if h['id']=='r60-source-survey':h.update(status='completed',result=s.pin(delivery))
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':state['revision'],'event_id':'r60-conditional-readout-custodied-20261017',
      'changes':{'records':[{'id':'r60-conditional-readout-result','kind':'fact','statute':'DERIVED',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in [delivery,reg]],
        'text':'R60 revisada: razão cruzada elimina ganhos fixos/entradas; pares separam n/eta sob fonte pura e perda em vácuo. Ganhos variáveis e fonte mista fornecem contramodelos. Ponte documental b=beta já existe; acesso físico obs/hid e preparo não demonstrados. Não mede beta, não satisfaz R5 nem recupera R4.'}],
        'flow':{'phase':'r60_conditional_readout_custodied','next_action':'Reusar contratos R60 e localizar mapa físico de acesso a setores/observáveis; recuperação R4 ainda aguarda ato específico.','handles':hs}}},'FINISH_TRANSITION')
    print(delivery)

if __name__=='__main__':main()
