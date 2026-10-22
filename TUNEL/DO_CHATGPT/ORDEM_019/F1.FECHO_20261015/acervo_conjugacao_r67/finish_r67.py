"""Register the reviewed documentary supplement without closing physics requirements."""
from pathlib import Path
import json, subprocess, sys, datetime as dt
import start_r67 as s

def once(label,args):
    s.new(label+'_INTENT.json',{'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'command':args})
    p=subprocess.run(args,capture_output=True,encoding='utf-8')
    receipt=s.new(label+'_RESULT.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:raise RuntimeError(str(receipt))
    print(p.stdout[:700]);return receipt

def main():
    m=s.project('FINISH_SYNC');t=next(x for x in m['projection']['active'] if x['id']=='R11_ACERVO')
    s.call({'operation':'check','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':t['id'],'lease_id':t['lease']['id']},'FINISH_CHECK')
    review=json.loads((s.ROOT/'REVIEW_R67.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!='codex-gerente-tgl'
    for p in review['evidence']:assert s.pin(p['path'])==p
    once('MEMORY_APPLY',[sys.executable,'-B','-X','utf8',str(s.ROOT/'memory_r67_r2.py'),'apply'])
    supplement=json.loads((s.ROOT/'SUPPLEMENT_R67.json').read_text(encoding='utf-8'))
    evidence=[s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix not in ['.pyc']]
    delivery=s.new('DELIVERY_R67.json',{'status':'REVIEWED_DOCUMENTARY_SUPPLEMENT','unit':'F1.FECHO_20261015','claim':958,
        'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'summary':supplement['summary'],'evidence':evidence,
        'review':s.pin(s.ROOT/'REVIEW_R67.json'),'memory':s.pin(s.ROOT/'MEMORY_APPLIED_R67.json'),
        'scope':'Document recovery and source-to-contract mapping. No new Lean build or theological uniqueness theorem; R4/R5 remain open. Canonical corpus_index unchanged.'})
    entry=s.new('MAP_ENTRY_R67.json',{'tipo':'ROTA','rota_id':'memoria.acervo.provas_conjugacao','dominio':'MEMORIA_DOCUMENTAL',
        'titulo':'R67: Provas recuperadas e cadeia observador-conjugacao-identidade',
        'pergunta':'Quais correspondencias o autor ja escreveu e como se ligam aos contratos existentes?',
        'metodo':'Censo de caminhos, reconhecimento DOCX por conteudo, hashes de bytes, extracao de paragrafos e revisao documental independente.',
        'resultado':'2299 arquivos;410 caminhos ausentes.116 DOCX recuperados,58 hashes,56 textos normalizados adicionais. Estratigrafia05out reaproveitada; fontes e assinaturas ligadas.',
        'veredito':'PASS_DOCUMENTARY_SCOPE','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,
        'defeito':'Sem OCR/imagens/ZIP, sem compilacao Lean nova. NamedIdentity nao seleciona nome historico unico; leitura teologica ONTO. Memoria usa verificacao otimista, nao lock global.',
        'nao_refazer':'Reusar suplemento e search_r67; nao tratar TheUnconjugatedObserver agosto como ultima leitura nem confundir invariancia total com TomitaJ.',
        'proximo_passo':'Usar fontes recuperadas nas consultas. R4/R5 prosseguem separadamente com calibracao e localizacao causal do sistemaR66.',
        'artefatos':[str(delivery),str(s.ROOT/'LEITURA_E_LIGACOES_R67.md'),str(s.ROOT/'SUPPLEMENT_R67.json')],
        'onde':str(s.ROOT),'refs':['formal.f1_rede.concrete_bosonic_kinematics']})
    mr=once('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R67 documental revisada:116DOCX recuperados,58hashes,56textos adicionais;correspondencias e estratigrafia05out. R4/R5 abertos;sem novoLean/gate.'])
    reg=s.new('REGISTRATION_R67.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    m=s.project('SUBMIT_SYNC');t=next(x for x in m['projection']['active'] if x['id']=='R11_ACERVO')
    s.call({'operation':'submit','reference':s.REF,'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'event_id':'r67-submit-documentary-supplement','task_id':t['id'],'lease_id':t['lease']['id'],'evidence':[s.pin(delivery),s.pin(reg)],'note':'Recuperacao documental revisada; aceite independente do requisito ainda separado.'},'SUBMIT')
    state=s.call({'operation':'get','reference':s.REF},'TRANSITION_GET','session_memory.py')
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r67-documentary-recovery-registered','changes':{'records':[{'id':'r67-acervo-conjugacao','kind':'fact','statute':'REAL','sources':[{'kind':'artifact','ref':str(delivery),'sha256':s.pin(delivery)['sha256']}],'text':'R67:116DOCX recuperados em58hashes e56textos normalizados adicionais; suplemento e busca local,135checks independentes. Correspondencias antigas localizadas; correcao05out prevalece. TomitaJ nao e invariancia sob todos operadores. Identificacao teologica ONTO; NamedIdentity nao fixa nome historico. R4/R5 nao satisfeitos por este levantamento.'}],'flow':{'phase':'r67_documentary_recovery_reviewed','next_action':'Integrar aceite documental real de R11_ACERVO; reusar fontes e suplemento. Retomar R5 com claim/check para localizacao causal de modos e acoplamentos R66; R4 calibracao e relogio continuam abertos.','handles':state['p']['handles']}}},'TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':main()
