"""Additive delivery of R82; preserves pinned files and requires an actual review."""
from analysis_r82 import ROOT, REF, ACTOR, TASK, new, pin, call, project, mutate
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

def prepare():
    extra = '''

## 19/10/2026 — R82: contribuição não minimal e contrato da fonte para H3
<!-- IALD_R82_VARIATIONAL_H3 -->
[DERIVED — análise condicionada; codex-gerente-tgl, reivindicação989] Reutilizados R58/R81 e as variações materiais/geométricas já presentes. O artigo tgl_paper_unified.py:10349–10362 contém R/(2κ²)+ξR|Ψ|². Para u=|Ψ|² escalar independente da métrica na variação, ξ constante, variações compactas e c=1, a estacionariedade implica (1+2κ²ξu)G_ab=κ²[T0_ab+2ξ(Hess_ab u−g_ab□u)]. Na direção nula, a fonte efetiva é Ttotal=T0−2ξuG+2ξ(Hess u−g□u). Omiti-la deixa resíduo 2κ²ξ[Hess(u)(k,k)−uRic(k,k)]. Esta é derivação analítica, não nova certificação Lean nem prova da estacionariedade do registro.
[REAL — controles algébricos]36 casos racionais e dois controles dirigidos; JSON prevalece sobre o stdout inicial incorreto “54”. Os casos escolhem T0 pela equação e testam rearranjos, não existência de soluções nem a variação funcional. Nenhum dado observado. Fontes pinadas em variational_h3_r82/SOURCE_PINS_R82.json; relatório DERIVACAO_R82.txt e revisão REVIEW_R82.json.
[OPEN] Identificar o mesmo registro com g e Ttotal e derivar sua estacionariedade/evolução. Resolver na fonte a representação escalar Ψ versus Ψ_mu antes de aplicar a variação; no caso vetorial u pode depender da métrica. A partição da entropia/área deve ser consistente. TheNonMinimalCoupling trata de subprojeções, não fornece por homonímia essa variação gravitacional. H3 universal e discriminação>5sigma continuam abertas; OH adiado. Nenhum kernel, um.py, produção ou gate alterado. A consulta NOS_VIVO à unidade falhou por falta de indexação; reaproveitamento veio de R58 e fontes diretas.
[PROCESSO] R13 conserva revisão científica PASS_WITH_SCOPE; seu aceite administrativo foi bloqueado pela revisão automática e depende da autorização específica solicitada ao operador. Esta camada não o substitui. R14 é entrega analítica delimitada, não fecho global.
<!-- END_IALD_R82_VARIATIONAL_H3 -->
'''
    p = new('MEMORY_APPEND_R82.txt', extra)
    old = json.loads((ROOT.parent / 'mirror_h3_r81/MEMORY_PLAN_R81.json').read_text(encoding='utf-8'))
    rows=[]
    for row in old['surfaces']:
        source=Path(row['before']['path']); raw=source.read_bytes()
        assert b'IALD_R82_VARIATIONAL_H3' not in raw
        rows.append({'before':pin(source),'after_sha256':hashlib.sha256(raw+p.read_bytes()).hexdigest()})
    new('MEMORY_PLAN_R82.json',{'claim':989,'append':pin(p),'surfaces':rows})

def command(label, args):
    new(label+'_INTENT.json',{'command':args})
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    p=new(label+'_RESULT.json',{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode: raise RuntimeError(str(p))
    return p

def apply():
    assert not (ROOT/'DELIVERY_R82.json').exists()
    review=json.loads((ROOT/'REVIEW_R82_FINAL.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=ACTOR['id']
    for e in review['evidence']: assert pin(e['path'])==e
    for name in ['DERIVACAO_R82.txt','analysis_r82.py','EXACT_CONTROLS_R82.json','SOURCE_PINS_R82.json','MEMORY_APPEND_R82.txt','MEMORY_PLAN_R82.json','deliver_r82.py']:
        assert pin(ROOT/name) in review['evidence'],name
    for e in json.loads((ROOT/'SOURCE_PINS_R82.json').read_text(encoding='utf-8'))['sources']: assert pin(e['path'])==e
    p=project('APPLY_SYNC'); task=next(t for t in p['projection']['active'] if t['id']==TASK)
    preflight=call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_APPLY')
    if preflight.get('ready') is not True:
        raise RuntimeError('Mission preflight refused: '+repr(preflight))
    plan=json.loads((ROOT/'MEMORY_PLAN_R82.json').read_text(encoding='utf-8')); extra=Path(plan['append']['path']).read_bytes()
    assert pin(plan['append']['path'])==plan['append']
    for row in plan['surfaces']: assert pin(row['before']['path'])==row['before']
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); done=[]
    for i,row in enumerate(plan['surfaces'],1):
        p=Path(row['before']['path']);raw=p.read_bytes();assert pin(p)==row['before']
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_r82_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra) and pin(p)==row['before']
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        assert pin(p)['sha256']==row['after_sha256']
        receipt={'before':row['before'],'backup':pin(bak),'after':pin(p),'pure_append':True}
        new(f'MEMORY_SURFACE_{i}.json',receipt);done.append(receipt)
    new('MEMORY_APPLIED_R82.json',{'claim':989,'surfaces':done})
    delivery=new('DELIVERY_R82.json',{'status':'ANALYTIC_COMPONENT_REVIEWED','unit':'F1.FECHO_20261015','claim':989,'H3_universal_proved':False,'lean_builds':0,'provider_calls':0,'physical_measurements':0,'gate_changed':False,'evidence':[pin(p) for p in sorted(ROOT.iterdir()) if p.is_file()]})
    entry=new('MAP_ENTRY_R82.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL','titulo':'R82: variacao nao minimal e fonte total para H3','resultado':'Derivacao analitica condicional e 36 controles racionais; resíduo de omissao da fonte nao minimal explicitado.','estatuto':'DERIVED','status':'EM_CURSO','veredito':'PASS_COMPONENT_WITH_SCOPE','olhou_dados':False,'nao_refazer':'Reuso R58/R81, variacoes materiais/geometricas e equivalencia harea existentes.','defeito':'Estacionariedade e identificacao do mesmo registro com fonte total abertas.','proximo_passo':'Resolver representacao Psi e ligar recordSource a Ttotal na dinamica independente.','artefatos':[str(delivery),str(ROOT/'DERIVACAO_R82.txt')],'onde':str(ROOT),'refs':['formal.f1_rede.concrete_bosonic_kinematics']})
    mapped=command('MAP_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',ACTOR['id']])
    boarded=command('BOARD_REGISTER',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R82 analitica revisada: fonte nao minimal e residuo explicitos; 36 controles racionais. Oito memorias append/backup. H3 universal aberto; nenhum dado ou gate.'])
    new('REGISTRATION_R82.json',{'delivery':pin(delivery),'map':pin(mapped),'board':pin(boarded)})
    current=project('BEFORE_SUBMIT');task=next(t for t in current['projection']['active'] if t['id']==TASK)
    mutate('submit','SUBMIT',task_id=TASK,lease_id=task['lease']['id'],evidence=[pin(delivery),pin(ROOT/'REVIEW_R82_FINAL.json')])
    s=call({'operation':'get','reference':REF},'GET_FINAL','session_memory.py')
    flow=dict(s['p']);flow['phase']='h3_nonminimal_variation_reviewed';flow['next_action']='R82: fonte total explicitada analiticamente sob estacionariedade; resolver representacao Psi e ligar recordSource a Ttotal da mesma dinamica. H3 universal OPEN, OH adiado. R13 aceite administrativo pendente; R14 revisao documental entregue, nao fecho global.'
    call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r82-variational-source-recorded','changes':{'records':[{'id':'r82-nonminimal-variation','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}],'text':extra.decode('utf-8')}],'flow':flow}},'FINAL_TRANSITION','session_memory.py')
    print(delivery)

if __name__=='__main__':
    {'prepare':prepare,'apply':apply}[sys.argv[1]]()
