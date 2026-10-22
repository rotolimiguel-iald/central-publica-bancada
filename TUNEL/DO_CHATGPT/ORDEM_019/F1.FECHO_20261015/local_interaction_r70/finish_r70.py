"""Custody and register reviewed R70 components, never close integral R4/R5."""
import datetime as dt
import json
import subprocess
import sys
import support_r70 as s

def once(label,cmd):
    s.new(label+'_INTENT.json',{'command':cmd,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    p=subprocess.run(cmd,capture_output=True,encoding='utf-8')
    result=s.new(label+'_RESULT.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:raise RuntimeError(str(result))
    print(p.stdout[:500],flush=True)
    return result

def main():
    assert not (s.ROOT/'DELIVERY_R70.json').exists()
    for task in ['R4','R5']:
        m=s.project('FINISH_'+task+'_PROJECT')
        t=next(t for t in m['projection']['active'] if t['id']==task)
        s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':task,'lease_id':t['lease']['id']},'FINISH_'+task+'_CHECK')
    review=json.loads((s.ROOT/'REVIEW_R70.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for p in review['evidence']:assert s.pin(p['path'])['sha256']==p['sha256']
    for p in json.loads((s.ROOT/'REUSE_PINS_R70.json').read_text(encoding='utf-8'))['sources']:
        assert s.pin(p['path'])==p
    result=json.loads((s.ROOT/'RESULT_CAUSAL_R70.json').read_text(encoding='utf-8'))
    command=json.loads((s.ROOT/'COMMAND_CAUSAL_R70.json').read_text(encoding='utf-8'))
    assert result['passed'] and command['exit_code']==0
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r70.py'),'apply'])
    evidence=[s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix!='.pyc']
    delivery=s.new('DELIVERY_R70.json',{'status':'REVIEWED_LOCAL_INTERACTION_AND_IDENTIFIABILITY_COMPONENT',
        'unit':'F1.FECHO_20261015','claim':960,'scope_event':964,'author':s.ACTOR['id'],
        'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'evidence':evidence,
        'mathematics':'Analytic local-vacuum rigidity, OH block version and purity-tangent obstruction for bounded local GKLS; local bounded Weyl candidate with common jump and controlled collision limit at fixed epsilon; explicit creation component; rate-product nonidentifiability for controlled protocols; causal-error bounds.',
        'synthetic_checks':len(result['checks']),'synthetic_passes':sum(x['passed'] for x in result['checks']),
        'new_lean_builds':0,'physical_measurements':0,'calibration_python_drafts':'NOT_EXECUTED_NOT_VALIDATED_NOT_A_CONSUMER',
        'R4_R5_integrally_satisfied':False,'canonical_changed':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R70.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
        'titulo':'R70: interacao local construida e diferenca concreta frente ao gerador de perdas',
        'metodo':'Reuso rede/Weyl/vacuo separante, R65/R66/R69; provas analiticas e tres controles sinteticos preregistrados; revisao distinta.',
        'resultado':'Candidato GKLS local limitado por Weyl, um J e reservatorio com limite colisional em epsilon fixo. Rigidez do vacuo e pureza impedem igualdade exata limitada com R66 em duas entradas; modo local tem criacao g nao nula. Colisoes identificam lambda, nao beta e Gamma separados. Cotas causais e de aproximacao explicitadas.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Nao ha novo Lean, calibracao medida, limite epsilon zero de semigrupos ou igualdade do candidato local com R66. Python de calibracao e rascunho nao executado.',
        'nao_refazer':'Nao reconstruir rede/Fock nem repetir controles R69; nao tentar igualdade estrita bounded/local que a tangente de pureza exclui sob as hipoteses declaradas.',
        'proximo_passo':'Calcular componente criadora e erro de reducao no acoplamento fisico especifico; identificar referencia independente para Gamma no mesmo J0/relogio.',
        'artefatos':[str(delivery),str(s.ROOT/'locality/LOCAL_INTERACTION_R70.md'),str(s.ROOT/'calibration/RESERVOIR_CALIBRATION_R70.md'),str(s.ROOT/'CAUSAL_ERROR_BUDGET_R70.md'),str(s.ROOT/'ADENDO_NORMA_CAUSAL_R70.md')],
        'onde':str(s.ROOT),'refs':['formal.anchored_name_contour']})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R70 revisada: candidato local limitado construido com J unico; obstrucao precisa a igualdade estritaR66, erro e calibracao independente delimitados. 3/3controles sinteticos, zero medida/novoLean/producao/gate; R4/R5 abertos.'])
    registration=s.new('REGISTRATION_R70.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    for task in ['R4','R5']:
        s.mutate('release','RELEASE_'+task,task_id=task,reason='Componente R70 revisado custodiado; liberar posse sem reduzir criterio. Interacao fisica/erro de reducao e referencia independente permanecem abertos.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r70-local-interaction-identifiability-recorded',
      'changes':{'records':[{'id':'r70-local-interaction-identifiability','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,registration)],
       'text':'R70: candidato local limitado construido por Weyl, com cinco saltos, J unico e limite de colisoes em epsilon fixo. Separacao do vacuo e prova por blocos OH dao obstrucao bounded-local a igualdade exataR66 pelas tangentes de pureza. Modo local contem criacao g nao nula; nao foi removida. Cotas causais/erro com fator de norma explicitado;3controles sinteticosPASS. Colisoes calibram produto lambda; controles/adaptacao do mesmo instrumento nao separam betaGamma. R4/R5 abertos, referencia independente e erro fisico faltam; semnovoLean/medida/producao/gate. Scriptscalibracao rascunhos nao validados.'}],
       'flow':{'phase':'r70_local_interaction_reviewed','next_action':'Reusar candidato localR70 e calcular sua componente criadora/erro no acoplamento fisico concreto; procurar referencia independente Gamma com mesmoJ0/relogio. Nao perseguir igualdade bounded-local excluida, nem promover aproximacao sem cota. Claim/check antes de retomar.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    print(delivery,flush=True)

if __name__=='__main__':main()
