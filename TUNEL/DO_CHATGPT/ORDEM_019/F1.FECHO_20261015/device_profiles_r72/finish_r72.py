"""Custody and register reviewed R72 components, never close integral R4/R5."""
import datetime as dt
import json
import subprocess
import sys
import support_r72 as s

def once(label,cmd):
    s.new(label+'_INTENT.json',{'command':cmd,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    p=subprocess.run(cmd,capture_output=True,encoding='utf-8')
    result=s.new(label+'_RESULT.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:raise RuntimeError(str(result))
    print(p.stdout[:500],flush=True)
    return result

def main():
    assert not (s.ROOT/'DELIVERY_R72.json').exists()
    for task in ['R4','R5']:
        m=s.project('FINISH_'+task+'_PROJECT')
        t=next(t for t in m['projection']['active'] if t['id']==task)
        s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':task,'lease_id':t['lease']['id']},'FINISH_'+task+'_CHECK')
    review=json.loads((s.ROOT/'REVIEW_R72.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for p in review['evidence']:assert s.pin(p['path'])['sha256']==p['sha256']
    result=json.loads((s.ROOT/'RESULT_PREPARATION_R72.json').read_text(encoding='utf-8'))
    command=json.loads((s.ROOT/'COMMAND_PREPARATION_R72.json').read_text(encoding='utf-8'))
    assert result['passed'] and command['exit_code']==0
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r72.py'),'apply'])
    evidence=[s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix!='.pyc']
    delivery=s.new('DELIVERY_R72.json',{'status':'REVIEWED_PROFILE_ENERGY_AND_PREPARATION_COMPONENT',
        'unit':'F1.FECHO_20261015','claim':967,'scope_event':969,'author':s.ACTOR['id'],
        'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'evidence':evidence,
        'mathematics':'Physical response kernels to normalized compact smears, symplectic Gram and channel-aware canonical pairs; perturbation bounds. Existing regular Maxwell moments imply finite mean energy of the constructed cavity vacuum via passive then finite active implementation. Gaussian-assumption-free local vacuum witness from second moments with spectral-gap trace-distance bound. NOT_LEAN.',
        'synthetic_checks':len(result['checks']),'synthetic_passes':sum(x['passed'] for x in result['checks']),
        'new_lean_builds':0,'physical_measurements':0,'process_scope':'Claim967, scope969; first scope registration parsed wrong argument and failed before write, corrected receipt preserved',
        'R4_R5_integrally_satisfied':False,'canonical_changed':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R72.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
        'titulo':'R72: resposta material aos modos locais, energia finita e testemunha de preparo',
        'metodo':'Reuso R63/R64/R66/R71 e energia Maxwell existente; derivacoes analiticas, auditoria documental focal e oito controles sinteticos preregistrados; revisao distinta.',
        'resultado':'Ponte kernels-smearing-Gram-pares com transporte dos canais e cotas de erro. Energia media finita de Omega_b demonstrada por momentos regulares e fatoracao passiva/ativa. Testemunha sem hipotese gaussiana por gapN e quadraturas, 8/8checks. Fontes distinguem RF, laser, contorno e estadoOH; calibracao independente continua aberta.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'NOT_LEAN. Nao entrega perfis medidos, resposta material, preparo observado ou Gamma. Testemunha local nao certifica espectador nem se transfere automaticamente da saida temporal a cavidade. Aritmetica nominal nao resolve EM.',
        'nao_refazer':'Reusar energia regular e transporte local existentes; nao repetirR71/R72 nem confundir modosRF/opticos pelo nome.',
        'proximo_passo':'Obter/reconhecer resposta material e kernels dos canais; ligar conversaoRF/laser ao mesmoJ0 e textura de banho; conferir preparo e referencia independenteGamma.',
        'artefatos':[str(delivery),str(s.ROOT/'mathematics/DEVICE_PROFILE_BRIDGE_R72.md'),str(s.ROOT/'PREPARATION_WITNESS_R72.md'),str(s.ROOT/'sources/BOUNDARY_DATA_TABLE_R72.md'),str(s.ROOT/'DIMENSIONAL_RESULT_R72.json')],
        'onde':str(s.ROOT),'refs':['formal.anchored_name_contour']})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R72 revisada: perfis-smearing-Gram, energia finita por reuso, testemunha de preparo semGaussianidade e8/8controles. RF/optica e dados materiais distinguidos. R4/R5 integrais abertos; claim967scope969; semnovoLean/medida/producao/gate.'])
    registration=s.new('REGISTRATION_R72.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    for task in ['R4','R5']:
        s.mutate('release','RELEASE_'+task,task_id=task,reason='Componente R72 revisado: energia finita e testemunha de preparo construidas; resposta material, kernels, conversaoRF/laser, preparo observado e Gamma continuam abertos. Criterios integrais preservados.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r72-local-interaction-identifiability-recorded',
      'changes':{'records':[{'id':'r72-local-interaction-identifiability','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,registration)],
       'text':'R72: ponte resposta-kernels-smearing-Gram-pares com erroCCR e canais transportados. Energia media finita de Omega_b por energia Maxwell existente e unitario passivo/ativo. Testemunha local por gapN, segundosmomentos e medias, semGaussianidade; distancia ao vacuo e produto com espectador condicionado, naoOmega_spec.8/8controles sinteticosPASS. Fontes distinguem geometriaRF/laser; resposta material/kernels/conversaoJ0/preparo/calibracaoGamma abertos. NOT_LEAN, semmedida/producao/gate. Claim967scope969 e memorias combackup.'}],
       'flow':{'phase':'r72_profile_energy_preparation_reviewed','next_action':'Reconhecer resposta material e kernels de leitura/atuacao, preservar bandasRF/optica e derivar sua conversao no mesmoJ0/banho. Usar testemunha de preparo apenas nos modos calibrados, obterGamma independente. Nao refazer energia regular/transporte/testes. Claim/check antes de avancar.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    print(delivery,flush=True)

if __name__=='__main__':main()
