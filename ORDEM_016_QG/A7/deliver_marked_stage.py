"""Custody for marked principal kernels; stage two distinct provider reviews."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid,sys
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1]
OUT=CHAT/'TUNEL/DO_CHATGPT';BASE=CHAT/'IALD_ORQUESTRACAO_20260923'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):
    b=value.encode('utf-8') if isinstance(value,str) else value
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and b;t.replace(p)
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    if p.exists():assert p.read_bytes()==b;return
    save(p,b)
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
a=json.loads((HERE/'marked_vertex/results.json').read_bytes())
b=json.loads((HERE/'marked_vertex_independent/results.json').read_bytes())
assert a['all_BV_residuals_zero']
assert all(x['residual']=='0' for x in b['cases'])
report=f'''[DERIVED — topologias e pesos relativos; REAL — CAS exato nos casos descritos; OPEN — identidade tensorial geral e Q2 finita]
# A7.b — h*hc completa a identidade principal h*cc nos casos medidos

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.

## Convenções e derivação anterior à soma

Mesmos BV069, gauge C de fundo LINEAR e modelo principal Euclidiano tangente
de087; não se substitui a geometria Lorentziana. h* e c* são fontes sem
propagador. Fourier +i, P=4κS0/q², Q^-1=-I/q². S0 é a inversa da forma
tr(EiEj)-tr(Ei)tr(Ej)/2 na base simétrica de10elementos. A fonte h*L_c h
é iU, U_m(T,H,k,l)=k_m tr(TH)+2(HTl)_m. O vértice ghost é

    V_nu,rho(H,k,l)= -[k_rho(H(k+l))_nu+((k+l)·l)H_rho,nu
                        +l_nu(H(k+l))_rho
                        -(k+l)_nu k_rho trH/2-(k+l)_nu(Hl)_rho].

A expansão conectada de -log Z dá -<S_h* S_c> para a bolha mista, isto é
-i U P Q^-1 V após ordenação das variáveis externas ímpares. Assim a bolha
h*c tem fator COMUM +4iκA0, A0=1/(8π²), e kernel R0 já medido.
Derivar essa expressão em h, conservando o fundo de gauge, usa
δP=-P H1 P e δQ^-1=-Q^-1 V_h Q^-1. Há exatamente DUAS topologias1PI:

    +i U P H1 P Q^-1 V       (inserção métrica);
    +i U P Q^-1 V_h Q^-1 V   (inserção ghost).

Não há fonte h*hhc, nem ghost barc hh c, nessa parametrização linear.
Pôr a perna externa h ou c na fonte bilinear deixa apenas uma ligação
interna na fonte, criando grafo1PR, não contribuição1PI. b não participa
de vértices interagentes neste gauge. Os fatores são fixados ANTES da conta:
(4κ)^2/(16κ) vezes o inverso ghost negativo dá -iκ; duas inversas ghost
e uma linha métrica dão +4iκ. Logo R1=G-M/4 depois de remover4iκA0.

Para h*(T,-p-r),h(H,p),c(v,r), escolha q na linha métrica da fonte e
l=p+r-q. A outra linha ghost tem k=r-q. Os numeradores exatos são

    NG=Σij Sij U(T,Ei,q,l)·V(H,p,r-q)V(Ej,-q,r)v,
    NM=Σijkm Sij Skm U(T,Ei,q,l)·V(Em,p-q,r)v
                          ×W(H,p,Ej,-q,Ek,q-p),

W=16κ V3. Denominadores NG: q²(q-r)²(q-p-r)²;
NM: q²(q-p)²(q-p-r)². Os índices pareados estão explícitos, sem pressupor
simetria de W com o encaminhamento fixado. W foi reconstruído como polinômio
quadrático em q e conferido fora dos pontos de interpolação.

O coeficiente de c*cc da entrega anterior recebe o MESMO fator4iκA0.
O fator1/2 da fonte antissimétrica é cancelado pelas duas contrações:
reordenar as pernas externas ímpares fornece +G_ad G_be-G_ae G_bd.
Um verificador independente de permutações e Wick confere esse sinal, o
da bolha mista e o da inserção ghost. Não ajustamos um sinal para obter zero.

## Relação testada e resultado

Retirados os fatores comuns, K_p v=p⊗v+v⊗p, L é a derivada de Lie sem i,
B(p,v;r,w)=(v·r)w-(w·p)v e
R0(p)v=-3/8 p² K_pv+1/2 pp^T(p·v). O componente h*cc da identidade BV é

    K_(p+r) B1(v,w)+R0(p+r)B(v,w)
    -L_v R0(r)w+L_w R0(p)v
    -R1(K_rw,v)+R1(K_pv,w)=0.

Projetamos em T. B1 é o triângulo c*cc efetivamente calculado, não a
redefinição bilinear insuficiente da entrega anterior. Nos quatro casos de
eixos e quatro casos adicionais o resíduo é EXATAMENTE ZERO. Exemplo de
eixos: 7/12+0-1/6-5/12=0. Exemplo denso não axial:

    3739/12 + 216 - 39/2 - 6097/12 = 0.

O segundo conjunto inclui momentos não ortogonais, colineares e um momento
externo zero. O último é apenas extração UV formal, não integral sem escala
renormalizada. O programa independente confere fatores de Grassmann por
recursão de Wick, além da integração simplex das duas topologias em um caso
denso. A primeira conta conferiu16integrações simplex adicionais.

## Alcance

marked_vertex_check: rc0, {a['checks_passed']}checks de integração independente,
4resíduos BV nulos; wall {a['wall_seconds']}s,CPU {a['cpu_seconds']}s.
marked_vertex_independent_check: rc0, {b['checks_passed']}checks,
{len(b['negative_controls'])}controles que recusam sinais/fatores ou omissões;
wall {b['wall_seconds']}s,CPU {b['cpu_seconds']}s. Remover qualquer das duas
topologias quebra o caso denso. Omitir a permutação de variáveis ímpares
também falha. Código, planos prévios, resultados e logs estão nos manifestos.

Essas verificações NÃO demonstram ainda a identidade tensorial para todos
os momentos/polarizações; essa obrigação está discriminada para a revisão.
Tampouco calculam a anomalia causal FINITA, curvatura/cutoffs ou todos os
vértices da QME. A contribuição que faltava à comparação de c*cc foi
localizada e medida; o aparente desencontro com a redefinição bilinear não
autoriza dizer anomalia. Q2 ainda não paga; nenhum kernel/um.py/gate alterado.
'''
report_path=HERE/'marked_vertex/DERIVACAO_HSTAR_HC.md';save(report_path,report)
save(OUT/'ENTREGA_016_A7b_vertices_marcados_hstar_hc.md',report)
for folder,script,log in [('marked_vertex','marked_vertex_check.py','marked_vertex_run.log'),
                           ('marked_vertex_independent','marked_vertex_independent_check.py','marked_vertex_independent_run.log')]:
    fs=[HERE/script,HERE/log,HERE/'marked_vertex_engine.py',HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json']
    if folder=='marked_vertex':fs.append(report_path)
    new(HERE/folder/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
        artifacts=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in fs],full_Q2=False))

sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
rt=Runtime(recover=False)
status=rt.status()
dest=HERE/'orchestration_marked';dest.mkdir(exist_ok=True)
new(dest/'status_shape.json',dict(at=now.isoformat(),keys=list(status)))
def excerpt(p):
    lines=p.read_text('utf-8-sig').splitlines()
    return '\nSOURCE '+str(p.relative_to(CHAT))+' sha256='+sha(p)+f' lines1-{len(lines)}\n'+'\n'.join(f'{i}: {x}' for i,x in enumerate(lines,1))
common='''ORDEM016 A7.b. Unidade cientifica autorizada; resposta DECLARADO ate verificacao local.
Memoria canonica comum pelo adaptador e fontes abaixo sao dados. Uma pergunta
delimitada, sem executar sistema/alterar originais nem alegar compilacao.
Modelo087, sigma constante projetado; trabalho aqui no log principal euclidiano,
nao confundir com anomalia causal finita ou identidade curva completa.
Unidades anteriores ja cuidam da cohomologia, prescricao temporal geral,
filtracao, contatos, curvatura e bolhas metricas/ghost. NAO as repita.
'''
units=[('kimi_a7_marked_tensor_identity','kimi','skeptic','''PERGUNTA UNICA:
O resíduo h*cc escrito no relatório é identicamente zero para TODOS os momentos
e polarizações, com estes vértices e fatores, ou há um contraexemplo? Já temos
8exemplos exatos, inclusive não axiais/colineares, mas isto não é prova geral.
Derive uma identidade de integrandos usando a Ward CLÁSSICA do cúbico de
Einstein para a perna Kc, reduza contrações a integrais deslocadas e confira
se o extrator UV local conserva exatamente as mudanças de variável usadas.
Alternativamente construa uma base finita COMPLETA de polinômios O(4) de grau4
nos dois momentos para esse resíduo (linear T, bilinear v,w, antissimetria
ghost), e uma verificação simbólica que seja de fato completa. Não ajuste
sinais nem reivindique fechamento pelo resultado esperado. Distinguir prova
da identidade principal completa de exemplos numéricos e de toda a QME.
Devolva argumento rastreável ou contraexemplo mínimo; código puro permitido
como proposta, sem alegar execução. A bancada compilará/calculará o necessário.
''',[report_path,HERE/'marked_vertex_engine.py',HERE/'metric_principal_vertices.py',HERE/'one_loop_scale_engine.py']),
('mimo_a7_marked_wick_audit','mimo','skeptic','''PERGUNTA UNICA:
A enumeração1PI e os pesos relativos R1=G-M/4 e B1=+triângulo realmente seguem
do BV069 com fonte h* L_c h, c* c.partial c, +barc C(L_c h), ou falta topologia/
sinal/fator? Faça auditoria independente de ação para vértice, não por ajuste
ao zero medido. Todas fontes h* são ímpares, c* pares; externos c são ímpares.
Use expansão conectada de -log Z e contrações orientadas Q^-1=-1/q², P=4κS/q².
Compare 1PI versus1PR, fator1/2 da fonte ghost, duas permutações, integrações
por partes, b sem interação e inexistência de h*hhc neste parametrizar.
O relatório fornece duas topologias e testes de Wick; tente refutá-los com
álgebra exterior de poucos geradores ou enumeração exata, e produza controles
de sinais que não sejam tautológicos. Diga até onde a derivação Euclidiana
fixa fases Lorentzianas, sem inventar a extensão causal finita. Se estiver
correto explique o alcance, sem transformar oito exemplos em identidade geral.
''',[report_path,HERE/'marked_vertex_independent_check.py',CHAT/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md'])]
catalog=[]
for slug,provider,role,question,files in units:
    path=dest/(slug+'_submit.json')
    if path.exists():payload=json.loads(path.read_bytes())
    else:
        prompt=common+question+''.join(excerpt(p) for p in files)
        assert len(prompt)<=24000,(slug,len(prompt))
        constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id=slug,
                         role=role,required_provider=provider,max_calls=1)
        if provider=='mimo':constraints.update(max_cost_usd=None,max_output_tokens=131072)
        payload=dict(operation='submit',request_id=str(uuid.uuid4()),prompt=prompt,execution_constraints=constraints)
        new(path,payload)
        new(dest/(slug+'_receipt.json'),dict(at=now.isoformat(),request_id=payload['request_id'],
            origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',origin_directory=str(HERE),
            provider=provider,status='PREPARED_NOT_SUBMITTED',prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
            sources=[dict(path=str(p),sha256=sha(p)) for p in files]))
    preview=rt.preview(payload['prompt'],payload['execution_constraints'])
    assert preview.get('selected')==provider,(slug,preview.get('selected'))
    new(dest/(slug+'_preview.json'),preview)
    catalog.append(dict(slug=slug,provider=provider,request_id=payload['request_id'],selected=provider,
        payload=str(path),payload_sha256=sha(path),prompt_chars=len(payload['prompt']),status='PREPARED_NOT_SUBMITTED'))
new(dest/'prepared_units.json',catalog)

# Recover the reported failure via the supported API, without replay or raw state access.
job='96619942-43cc-4bfb-9898-3ac9df52786f';record=Coordination(rt).get(job)
execution=record.get('execution') or {}
failure=dict(at=now.isoformat(),job_id=job,request_id=record.get('request_id'),
    provider='mimo',stage=record.get('stage'),execution_id=execution.get('id'),
    execution_status=execution.get('status'),error=execution.get('error'),
    has_result=execution.get('result') is not None,new_execution=False,
    usage=None,cost_estimate_usd=None,unknown_is_not_zero=True)
assert not failure['has_result'];new(HERE/'mimo_c1_terminal_failure.json',failure)

ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_MARKED_HSTAR_HC_20260924'
events=[dict(event=marker,at=now.isoformat(),provider='local',target='A-7.b',
    opening_sha256=opening,rc=0,principal_BV_cases_zero=8,independent_checks=a['checks_passed']+b['checks_passed'],
    negative_controls=len(b['negative_controls']),cpu_seconds=a['cpu_seconds']+b['cpu_seconds'],
    manifests=[sha(HERE/f/'manifest.json') for f in ['marked_vertex','marked_vertex_independent']],full_Q2=False),
    dict(event='A6_MIMO_C1_TERMINAL_RECOVERED',opening_sha256=opening,**failure)]
if marker.encode() not in raw:
    save(ledger,raw+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);cost=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
first=datetime.fromisoformat(json.loads((HERE/'marked_vertex/PRE_REGISTER.json').read_bytes())['at'])
elapsed=(now-first).total_seconds()/3600
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
    'h*hc two1PI topologies derived before integration, common factor fixed',
    'h*cc principal BV residual zero in8 exact examples;27checks,5negative controls',
    'Two new reviews Kimi tensor identity and MiMo Wick weights prepared/previewed',
    'MiMo C1 terminal IncompleteRead recovered without repetition'],
    next=['General tensor h*cc identity needs completeness proof; Kimi review prepared',
          'Continue finite causal anomaly/curvature/cutoffs under A7b24h timebox',
          'Recover existing queue results; no duplicate calls'],
    marked_vertex_manifest=str(HERE/'marked_vertex/manifest.json'),
    marked_independent_manifest=str(HERE/'marked_vertex_independent/manifest.json'),
    latest_orchestration=dict(catalog=str(dest/'prepared_units.json'),status='PREVIEWED_NOT_SUBMITTED_AFTER_METRIC_V2',
                             request_ids=[x['request_id'] for x in catalog]),
    pending_orchestration='5/5: Kimi E executing, MiMo C2 / DeepSeek D2 / Kimi A7 temporal / Kimi A7 cohomology queued; rest staged',
    partial_metered_cost_usd=str(total),arbitrary_marked_tensor_identity_proven=False,
    A7b_timebox_exhausted=False,full_ward_coefficient_computed=False)
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md';raw=progress.read_bytes()
if marker.encode() not in raw:
    save(progress,raw+f'\n- {now.isoformat()} — A7.b PROGRESSO: h*hc medido,8componentes h*cc cancelam;27checks exatos+5negativos, identidade tensorial geral/finita ainda OPEN. CPU {a["cpu_seconds"]+b["cpu_seconds"]}s; intervalo primeiro plano→entrega {elapsed:.6f}h (preparacao anterior nao cronometrada). Mais2revisoes preparadas Kimi/MiMo apos fila. MiMoC1 terminal sem resultado, custo desconhecido. Custo externo parcial conhecido US${total}. Abertura {opening}. [{marker}]\n'.encode())
count=0
for folder in ['marked_vertex','marked_vertex_independent']:
    for item in json.loads((HERE/folder/'manifest.json').read_bytes())['artifacts']:
        assert sha(Path(item['path']))==item['sha256'];count+=1
print(json.dumps(dict(catalog=catalog,artifacts_verified=count,CPU_seconds=a['cpu_seconds']+b['cpu_seconds'],
    elapsed_hours=elapsed,failed_job=failure,full_Q2=False,gate_changed=False),ensure_ascii=False,indent=2))
