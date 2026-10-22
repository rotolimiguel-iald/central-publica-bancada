"""Custody and register reviewed R59 components; preserve the R4 approval block."""
from pathlib import Path
import datetime as dt
import json
import subprocess
import sys
import support_r59 as s

def once(label,args):
    s.new(label+'_INTENT.json',{'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp=subprocess.run(args,capture_output=True,encoding='utf-8')
    p=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode:raise RuntimeError(str(p))
    print(cp.stdout[:900]);return p

def main():
    s.preflight('R5','DELIVERY')
    review=json.loads((s.ROOT/'independent_review/FINAL_COMPONENT_REVIEW_R59.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for x in review['evidence']:
        assert s.pin(x['path'])['sha256']==x['sha256'],x['path']
    files=['RELATORIO_R59.txt','CUTOFF_DERIVATION_R59.txt','CUTOFF_RESULT_R59.json','derive_cutoff_r59.py',
        'squeezing/DELIVERY_R1.json','squeezing/DERIVATION_R1.txt','squeezing/SYMBOLIC_RESULTS_R1.json',
        'independent_review/FINAL_COMPONENT_REVIEW_R59.json','independent_review/CUTOFF_INDEPENDENT_CHECKS_R59.json',
        'MEMORY_APPLIED_R59.json','MEMORY_REVIEW_R59.json','MEMORY_PATH_VALIDATION_R59.json',
        'NOVA_PENDENCIA_R4_LEASE_R59.json','oh_correlation/EXPLORATION_R59.json','oh_correlation/SOURCE_PINS_R59.json']
    delivery=s.new('DELIVERY_R59.json',{'status':'REVIEWED_FINITE_COMPONENTS_R4_ADMIN_PENDING',
        'unit':'F1.FECHO_20261015','claim':939,'author':s.ACTOR['id'],'reference':s.pin(s.REF),
        'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'evidence':[s.pin(s.ROOT/n) for n in files],
        'conclusion':'Pair phase recovered for rho>0; Gram/symplectic covariance; occupation cutoff converges in the same two-mode Fock with exact errors.',
        'scope':'Written derivation plus exact symbolic and independent checks; not new Lean build or physical network realization.',
        'R4_recovery_executed':False,'R4_integrally_satisfied':False,'R5_integrally_satisfied':False,
        'R4_exploration':'Produced before suspension notice; preserved, not used as reviewed result or accepted as R4.',
        'pending_operator_unit':'F1.FECHO.R4_LEASE_R59','provider_calls':0,'observed_data':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R59.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics',
        'dominio':'FORMAL','titulo':'R59: covariância de pares, leitura de fase e limite de ocupação no mesmo Fock',
        'metodo':'Derivação escrita, álgebra simbólica exata, controles negativos e reprodução independente.',
        'resultado':'m=exp(i phi)sinh(rho)cosh(rho), covariânciaGram/CCR e cortes com fidelidade1-q^(N+1). R4recuperaçãoadministrativaaguardaoperador.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Não identifica modos/preparo físico nem demonstra dinâmicaOH ou refinamentoespacial; rho=0 não determina fase.',
        'nao_refazer':'Reutilizar covariância e caudasR59 e consumidoresR6/R7/R8. Não repetir exploraçãoOH nem recuperarR4semato.',
        'proximo_passo':'Contrato físico de modos/quadraturas e dinâmica, após recuperação administrativaR4autorizada; conservar distinção cortesdeocupação/redeespacial.',
        'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R59.txt')],'onde':str(s.ROOT)})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015',
        '--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota',
        'R59 componentes de pares/covariância e corte revisados; oito memórias com backup. R4recuperaçãopendenteoperador, sem reset; R5nãoaceitointegralmente.'])
    reg=s.new('REGISTRATION_R59.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINISH_GET');handles=state['p']['handles']
    for h in handles:
        if h['id']=='r59-squeezing':h.update(status='completed',result=s.pin(s.ROOT/'squeezing/DELIVERY_R1.json'))
        elif h['id']=='r59-oh-correlation':h.update(status='completed',result=s.pin(s.ROOT/'oh_correlation/SOURCE_PINS_R59.json'),note='Agent returned; no execution pending. AdministrativeR4approval remains pending in board945 and q.')
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
        'expected_revision':state['revision'],'event_id':'r59-components-custodied-r4-pending-20261017',
        'changes':{'records':[{'id':'r59-reviewed-pair-covariance','kind':'fact','statute':'DERIVED',
            'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in [delivery,reg]],
            'text':'R59: fase em pares com médiaunilateralzero, formaGram/CCR e convergência de ocupação do mesmo par, erros explícitos; revisão independente. Não é limiteespacial/dinâmicaOH nem aceiteR4/R5. R4recuperaçãoadministrativaaguarda resposta; nenhum resetexecutado, exploração anteriorpreservadasemintegrar.'}],
            'flow':{'phase':'r59_components_custodied_r4_approval_pending','next_action':'Após resposta sobre leaseR4, recuperar administrativamente conforme autorização e retomar ligação ao geradorOH; reutilizar covariância/caudasR59. R5físico ainda aberto.','handles':handles}}},'FINISH_TRANSITION')
    print(delivery)

if __name__=='__main__':main()
