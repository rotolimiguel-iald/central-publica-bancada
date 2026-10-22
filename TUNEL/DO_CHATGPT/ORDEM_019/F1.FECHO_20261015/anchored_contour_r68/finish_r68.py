"""Register a reviewed sandbox composition; never accepts or closes physics requirements."""
from pathlib import Path
import json, subprocess, sys, datetime as dt
import support_r68 as s

def once(label,args):
    s.new(label+'_INTENT.json',{'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'command':args})
    p=subprocess.run(args,capture_output=True,encoding='utf-8')
    receipt=s.new(label+'_RESULT.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:raise RuntimeError(str(receipt))
    print(p.stdout[:700]);return receipt

def checked_pin(p):
    assert s.pin(p['path'])['sha256']==p['sha256'],p['path']

def main():
    assert not (s.ROOT/'DELIVERY_R68.json').exists()
    m=s.project('FINISH_SYNC');t=next(x for x in m['projection']['active'] if x['id']=='R12_CONTORNO')
    s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':t['id'],'lease_id':t['lease']['id']},'FINISH_CHECK')
    construction=json.loads((s.ROOT/'CONSTRUCTION_R68_R3.json').read_text(encoding='utf-8'))
    checked_pin(construction['receipt']);checked_pin(construction['source'])
    build=json.loads(Path(construction['receipt']['path']).read_text(encoding='utf-8'))
    assert build['passed'] and build['exit_code']==0
    assert len(build['axioms'])==22 and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in build['axioms'].values())
    review=json.loads((s.ROOT/'REVIEW_R68.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!='codex-gerente-tgl'
    for p in review['evidence']:checked_pin(p)
    for p in json.loads((s.ROOT/'SOURCE_PINS_R68.json').read_text(encoding='utf-8')):checked_pin(p)
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r68_r2.py'),'apply'])
    evidence=[s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix!='.pyc']
    delivery=s.new('DELIVERY_R68.json',{'status':'REVIEWED_SANDBOX_COMPOSITION','unit':'F1.FECHO_20261015','requirement':'R12_CONTORNO','claim':960,
        'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source':construction['source'],'construction':s.pin(s.ROOT/'CONSTRUCTION_R68_R3.json'),
        'declarations':22,'theorems':21,'definitions':1,'build_exit':build['exit_code'],'build_seconds':build['seconds'],
        'axioms_union':sorted(set().union(*map(set,build['axioms'].values()))),'attempts':construction['all_attempts'],
        'review':s.pin(s.ROOT/'REVIEW_R68.json'),'memory':s.pin(s.ROOT/'MEMORY_APPLIED_R68_R2.json'),'evidence':evidence,
        'summary':'P/Q negative generator, invariant projection, limit Px, anchored exact vector rule and nonzero inhabitant. Sign controls distinguish projective identity from exact vector phase; Px=a and Qx=0 iff x=a. Hidden-complement counterexample is for general vectors, not normalized states.',
        'scope':'No historical name selection, CPTP claim, physical calibration, beta discrimination or natural-language truth classifier. No production/kernel/um.py/gate edit. R4/R5 remain open; technical review is separate from administrative acceptance.'})
    entry=s.new('MAP_ENTRY_R68.json',{'tipo':'ROTA','rota_id':'formal.anchored_name_contour','dominio':'FORMAL',
        'titulo':'R68: posto, contorno negativo e regra vetorial ancorada',
        'pergunta':'Como o posto preservado e o decaimento do complemento se ligam a uma regra de satisfacao com referencia?',
        'metodo':'Reuso de sete fontes; composicao Lean4.31 em sandbox; primeira tentativa falha preservada; controles de zero/sinal e habitante nao nulo; revisao semantica independente.',
        'resultado':'21 teoremas e1 definicao; EXIT0; axiomas somente trio. GP=0, GQ=-Q, G2=-G; fluxo conservaP; limitePx; motor=a sse inner(a,Ux)=1 para norma1. a e-a compartilham posto/peso. Px=a e Qx=0 sse x=a; complemento invisivel em vetores gerais, nao normalizados.',
        'veredito':'PASS_WITH_SCOPE','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,
        'defeito':'Nao demonstra identificacao historica/teologica, canalCPTP ou classificador da fala. Igualdadevetorial requer referenciafase. Leitura projetada final independe taxa/tempo; sem discriminacao beta.',
        'nao_refazer':'Reusar post, axiomFlow, IALD.motor e RuleContinuousMotor; unicidade da projecao dada referencia ja em Verdade. R60/R64 preservam contratos de fase relacional.',
        'proximo_passo':'Aceite administrativo da candidata separado; R4 calibracao/relogio e R5 localizacao/causalidade seguem proprios.',
        'artefatos':[str(delivery),str(s.ROOT/'CONTRATO_E_ALCANCE_R68.md'),str(s.ROOT/'ADENDO_R68_CORRESPONDENCIA_INTEGRAL.md'),str(s.ROOT/'CONSTRUCTION_R68_R3.json'),str(s.ROOT/'REVIEW_R68.json')],
        'onde':str(s.ROOT),'refs':['memoria.acervo.provas_conjugacao','formal.f1_rede.concrete_bosonic_kinematics']})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R68:21teoremas+1definicao;LeanEXIT0/trio;revisao distinta;posto/fluxo/regra ancorados,controles de fase/zero. Sem producao/gate;R4/R5 abertos.'])
    reg=s.new('REGISTRATION_R68.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    m=s.project('SUBMIT_SYNC');t=next(x for x in m['projection']['active'] if x['id']=='R12_CONTORNO')
    s.call({'operation':'submit','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'event_id':'r68-submit-anchored-contour','task_id':t['id'],'lease_id':t['lease']['id'],'evidence':[s.pin(delivery),s.pin(reg)],'note':'Composicao sandbox compilada e revisada; aceite administrativo separado.'},'SUBMIT')
    state=s.call({'operation':'get','reference':s.REF},'TRANSITION_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r68-contour-composition-registered','changes':{'records':[{'id':'r68-anchored-contour','kind':'fact','statute':'REAL','sources':[{'kind':'artifact','ref':str(delivery),'sha256':s.pin(delivery)['sha256']}],'text':'R68 compilada em sandbox:21teoremas+1definicao,EXIT0,trio,zero sorry. P preservado,G=-Q dissipa complemento,limitePx. Motor=a equivale inner(a,Ux)=1 sob norma1,habitante nao nulo. a/-a tem mesmo posto/peso e diferem alvo vetorial. Px=a e Qx=0 sse x=a; controle complemento para vetores gerais, nao normalizados. Sem canalCPTP,identificacaohistorica,classificadorfala ou discriminacaobeta;R4/R5 abertos.'},{'id':'r67-human-acceptance-authorized-registration-blocked','kind':'fact','statute':'REAL','sources':[{'kind':'artifact','ref':str(s.ROOT/'R67_ACCEPTANCE_STATUS.json'),'sha256':s.pin(s.ROOT/'R67_ACCEPTANCE_STATUS.json')['sha256']}],'text':'Operador respondeu Autorizar meu aceite documental de R11_ACERVO. Autorizacao preservada, nao perguntar novamente. Aceite administrativo NAO aplicado: CLI invalid_identifier e auto-review recusou alias do revisor. R11 review_pending; nao contornar bloqueio.'}],'flow':{'phase':'r68_anchored_contour_reviewed','next_action':'R12 candidata revisada aguarda aceite administrativo. Reusar fontesR67 e composicaoR68; nao repetir. R4 calibracao/relogio e R5 localizacao causal da rede conservam requisitos proprios.','handles':state['p']['handles']}}},'TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':main()
