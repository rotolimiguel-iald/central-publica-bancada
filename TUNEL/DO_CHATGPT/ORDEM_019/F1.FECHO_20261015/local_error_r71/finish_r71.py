"""Custody and register reviewed R71 components, never close integral R4/R5."""
import datetime as dt
import json
import subprocess
import sys
import support_r71 as s

def once(label,cmd):
    s.new(label+'_INTENT.json',{'command':cmd,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    p=subprocess.run(cmd,capture_output=True,encoding='utf-8')
    result=s.new(label+'_RESULT.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:raise RuntimeError(str(result))
    print(p.stdout[:500],flush=True)
    return result

def main():
    assert not (s.ROOT/'DELIVERY_R71.json').exists()
    for task in ['R4','R5']:
        m=s.project('FINISH_'+task+'_PROJECT')
        t=next(t for t in m['projection']['active'] if t['id']==task)
        s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':task,'lease_id':t['lease']['id']},'FINISH_'+task+'_CHECK')
    review=json.loads((s.ROOT/'REVIEW_R71.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for p in review['evidence']:assert s.pin(p['path'])['sha256']==p['sha256']
    result=json.loads((s.ROOT/'RESULT_VACUUM_R71.json').read_text(encoding='utf-8'))
    command=json.loads((s.ROOT/'COMMAND_VACUUM_R71.json').read_text(encoding='utf-8'))
    assert result['passed'] and command['exit_code']==0
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r71.py'),'apply'])
    evidence=[s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix!='.pyc']
    delivery=s.new('DELIVERY_R71.json',{'status':'REVIEWED_LOCAL_CAVITY_TRANSPORT_AND_ENERGY_ERROR_COMPONENT',
        'unit':'F1.FECHO_20261015','claim':967,'scope_event':966,'author':s.ACTOR['id'],
        'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'evidence':evidence,
        'mathematics':'Analytic finite Bogoliubov transport of the full R66 generator, domains, spectator and reservoir to a local oscillator subfactor with changed cavity reference. Local number cuts and trace-norm limit preserve the commutant. Energy-cut generator-error and global-vacuum creation-cost bounds. NOT_LEAN; actual patent modes and independent Gamma remain open.',
        'synthetic_checks':len(result['checks']),'synthetic_passes':sum(x['passed'] for x in result['checks']),
        'new_lean_builds':0,'physical_measurements':0,'process_scope':'Documentary/synthetic work after board claim960 expiry; renewed967 before memory; no inferred ratification',
        'R4_R5_integrally_satisfied':False,'canonical_changed':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R71.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
        'titulo':'R71: transporte local do gerador completo por referencia de cavidade e cotas de erro',
        'metodo':'Reuso R66/R69/R70, fontes primarias de squeezing/cavidade, aproximacao compacta e implementacao simpletica finita; revisao independente.',
        'resultado':'Realizacao analitica local exata de R66 em subfator de dois osciladores com vacuo Omega_b distinto do global, preservando reservatorio, bomba, J unico, dominios e espectador. Cotas de erro/energia e cinco controles sinteticos PASS. Geometria da patente recuperada; modos materiais e Gamma independente ainda abertos.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'NOT_LEAN. Nao identifica modos da camara real, preparo fisico, energia/clock ou calibracao. Claim960 venceu durante trabalho; renovado967 antes da memoria, desvio explicito.',
        'nao_refazer':'Nao reconstruir squeezing ja escrito ou gerador R66; nao confundir vacuo de cavidade com global separante; nao repetir controles R71.',
        'proximo_passo':'Perfis da cavidade mista, preparo e energia da referencia transportada; normalizacao/relogio e referencia independente Gamma.',
        'artefatos':[str(delivery),str(s.ROOT/'locality/BOGOLIUBOV_CAVITY_R71.md'),str(s.ROOT/'locality/ENERGY_ERROR_R71.md'),str(s.ROOT/'sources/FOCAL_DEVICE_MODE_SOURCES_R71.md'),str(s.ROOT/'sources/ADENDO_SQUEEZING_VACUO_R71.md')],
        'onde':str(s.ROOT),'refs':['formal.anchored_name_contour']})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R71 revisada: transporte analitico local de R66 com referencia de cavidade; 5/5controles sinteticos, fontes recuperadas. R4/R5 integrais abertos. Claim967 antes da memoria; desvio de vencimento960 documentado. SemnovoLean/medida/producao/gate.'])
    registration=s.new('REGISTRATION_R71.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    for task in ['R4','R5']:
        s.mutate('release','RELEASE_'+task,task_id=task,reason='Componente R71 revisado: transporte local analitico concluido no modelo; perfis materiais, preparo/energia/clock e Gamma independente continuam abertos. Criterios integrais preservados.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r71-local-interaction-identifiability-recorded',
      'changes':{'records':[{'id':'r71-local-interaction-identifiability','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,registration)],
       'text':'R71: referencia de cavidade Omega_b e pares locais construidos analiticamente permitem transporte integral R66, cortes locais e causalidade por limite. NOT_LEAN; cinco controles sinteticos PASS de custo relativo ao vacuo global e erro em energia. Artigos ja continham squeezing e vacuo da cavidade; geometria recuperada, perfis materiais/preparo/energia/clock e Gamma independente ainda abertos. R4/R5 nao reduzidos. Claim960 expirou durante trabalho, renovado967 antes da memoria; desvio documentado. Semmedida/producao/gate.'}],
       'flow':{'phase':'r71_local_cavity_transport_reviewed','next_action':'Reusar transporte local R71; identificar perfis e preparo da cavidade material, energia e relogio, depois referencia independente Gamma. Nao repetir controles. Claim/check antes da proxima etapa.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    print(delivery,flush=True)

if __name__=='__main__':main()
