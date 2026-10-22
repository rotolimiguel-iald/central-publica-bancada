"""Register reviewed R69 components, preserving the full R4/R5 criteria."""
import datetime as dt,json,subprocess,sys
from pathlib import Path
import support_r69 as s

def once(label,cmd):
    s.new(label+'_INTENT.json',{'command':cmd,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    p=subprocess.run(cmd,capture_output=True,encoding='utf-8')
    out=s.new(label+'_RESULT.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:raise RuntimeError(str(out))
    print(p.stdout[:700]);return out

def preflight(task,label):
    m=s.project(label+'_PROJECT');t=next(x for x in m['projection']['active'] if x['id']==task)
    return s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':task,'lease_id':t['lease']['id']},label+'_CHECK')

def main():
    assert not (s.ROOT/'DELIVERY_R69.json').exists()
    preflight('R4','DELIVERY_R4');preflight('R5','DELIVERY_R5')
    review=json.loads((s.ROOT/'REVIEW_R69.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for row in review['evidence']:assert s.pin(row['path'])['sha256']==row['sha256']
    for row in json.loads((s.ROOT/'REUSE_PINS_R69.json').read_text(encoding='utf-8'))['sources']:
        assert s.pin(row['path'])==row
    calibration=json.loads((s.ROOT/'CALIBRATION_RESULT_POINTER_R69.json').read_text(encoding='utf-8'))
    assert calibration['passed'] and calibration['exit_code']==0
    for p in calibration['evidence']:assert s.pin(p['path'])['sha256']==p['sha256']
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r69_r2.py'),'apply'])
    evidence=[s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix!='.pyc']
    delivery=s.new('DELIVERY_R69.json',{'status':'REVIEWED_CORRESPONDENCE_CALIBRATION_LOCALITY_COMPONENT','unit':'F1.FECHO_20261015','claim':960,'scope_event':962,
        'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'evidence':evidence,'calibration':calibration,
        'mathematics':'Isometric transport of the anchored projection and orthogonal internal/external residuals; calibrated metric and observational scope; bounded local GKLS commutant criterion and explicit limits for the bosonic device.',
        'new_lean_builds':0,'physical_measurements':0,'R4_R5_integrally_satisfied':False,'canonical_changed':False,'gate_changed':False})
    entry=s.new('MAP_ENTRY_R69.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
        'titulo':'R69: correspondencia concreta ligada ao instrumento e ao criterio causal',
        'metodo':'Reuso R62/R64/R65/R66/R68; prova analitica de transporte/residuos; contrato executavel e controles sinteticos preregistrados; fontes concretas da rede e revisao independente.',
        'resultado':'VPV* transporta posto e distingue residuo interno/externo. Decoder quatro correlacoes conserva escopo observacional; Gamma independente e normalizacao/tempo exigidos. Rede local existente localizada; isometria de modos nao prova localidade dos coeficientes.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Sem calibracao medida, novoLean ou afiliação local do gerador ilimitadoR66. Correspondencia de observaveis nao equivale estado inteiro; R4/R5 integrais abertos.',
        'nao_refazer':'Reusar decoderR62/instrumentoR64/calibracaoR65/reservatorioR66/contornoR68. RedeMaxwell/Weyl e localidade ja existem; nao confundir Fock temporal com espacial.',
        'proximo_passo':'Fornecer calibracao independente do mesmo canal e ligar acoplamentos localizados da rede ao gerador efetivo do dispositivo com dominio/erro controlados; preservar obstrucoes tipadas.',
        'artefatos':[str(delivery),str(s.ROOT/'PONTE_CORRESPONDENCIA_R69.md'),str(s.ROOT/'LOCALITY_BRIDGE_R69.md'),str(s.ROOT/'REVIEW_R69.json')],
        'onde':str(s.ROOT),'refs':['formal.anchored_name_contour']})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R69: correspondencia/metricas/residuos ligados; contrato calibracao e controles sinteticos; localidade existente reutilizada com limite tipado do dispositivo. Revisao distinta; R4/R5 abertos, sem producao/dado/gate.'])
    reg=s.new('REGISTRATION_R69.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    for task in ['R4','R5']:
        s.mutate('release','RELEASE_'+task,task_id=task,reason='Componente R69 custodiado e revisado; liberar posse temporaria sem reduzir criterio integral nem repetir execucoes. Calibracao fisica e localidade do dispositivo ainda abertas.',sources=[s.pin(delivery)])
    state=s.call({'operation':'get','reference':s.REF},'FINISH_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r69-correspondence-calibration-locality-recorded',
        'changes':{'records':[{'id':'r69-correspondence-calibration-locality','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg)],
        'text':'R69: V/VPV* transportam correspondenciaR68; residuo total inclui componente fora dos modos. Calibracao C exige metrica transportada, decoderR62/64 quatrocorrelacoes nao determina estado inteiro. Gamma independente, convencaoJ0 e relogio exigidos. RedeMaxwell/Weyl e localidade concretas reaproveitadas; coeficientesR66 nao localizados apenas por ortonormalidade. CriterioGKLSbounded fixa comutante; ilimitados/cortes globais exigem ponte propria. Provaanalitica e controles sinteticos revisados,semnovoLean/dado/calibracaomedida. R4/R5 permanecemabertos; leasesliberados. AceiteR11administrativo continua bloqueado apesarautorizacaohumana.'},{'id':'r69-operator-state-space-identity','kind':'decision','statute':'INPUT','sources':[{'kind':'artifact','ref':str(s.ROOT/'OPERADOR_IDENTIDADE_ESTADOS_R69.txt'),'sha256':s.pin(s.ROOT/'OPERADOR_IDENTIDADE_ESTADOS_R69.txt')['sha256']}],'text':(s.ROOT/'OPERADOR_IDENTIDADE_ESTADOS_R69.txt').read_text(encoding='utf-8')+' Definicao conceitual do autor, com alcance em CUNHAGEM_IDENTIDADE_ESTADOS_R69.md; nao prova numerica, nem reducao da teoria fisica a um indice documental.'}],
        'flow':{'phase':'r69_correspondence_bridge_reviewed','next_action':'Reusar R69; R4 exige referencia independente do mesmo canal/relogio. R5 exige acoplamento localizado com dominios e reducao controlada ao geradorR66; nao promover isometria/decoder a causalidade/tomografia. Retomada exige claim/check, nao repetir execucoes.','handles':state['p']['handles']}}},'FINISH_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':main()
