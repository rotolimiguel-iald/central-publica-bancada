"""Deliver a measured obstruction and its scoped BV continuation; revise held job."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid,sys
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):
    raw=value.encode() if isinstance(value,str) else value
    if p.exists():
        old=p.read_bytes()
        if old==raw:return
        b=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(raw)
    assert raw and t.read_bytes()==raw;t.replace(p)
def js(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
def new(p,o):assert not p.exists(),str(p);js(p,o)
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
groups=[('metric_primitive_zero_ghost','metric_primitive_zero_ghost_check.py','metric_primitive_zero_ghost_run.log'),
        ('metric_primitive_zero_ghost_audit','metric_primitive_zero_ghost_audit.py','metric_primitive_zero_ghost_audit_run.log'),
        ('constant_ghost_eom','constant_ghost_eom_probe.py','constant_ghost_eom_run.log'),
        ('constant_ghost_transverse','constant_ghost_transverse_check.py','constant_ghost_transverse_run.log'),
        ('antifield_quadratic_primitive','antifield_quadratic_primitive_check.py','antifield_quadratic_primitive_run.log')]
results={f:json.loads((HERE/f/'results.json').read_bytes()) for f,_,_ in groups}
assert results['metric_primitive_zero_ghost']['counterexample_found']
assert results['constant_ghost_transverse']['checks_passed']==36
cpu=sum(x['cpu_seconds'] for x in results.values());wall=sum(x['wall_seconds'] for x in results.values())
report=f'''[DERIVED — obstrução à mudança só de campos neste escopo; REAL — CAS exato; OPEN — primitiva BV completa]
# A7.b — o resíduo transversal exige ampliar a candidata local

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.

Mantemos o R1=G-M/4 medido, o Z da entrega anterior e a normalização
principal com4κA0 retirado. A primeira candidata era uma mudança local só
de h,c: h_antigo=h+εA2(h,h), c_antigo=c+εFc-εZ(h,c).
Ela produziria no vértice adicional -2A2(H,K_l v), além de R1coord.

## Contraexemplo mínimo

Escolha momento do ghost l=0, momento métrico p=e0, ghost v=e0 e
polarizações H=T=e11. Então:

    G=3/32, M=-7/24, R1=G-M/4=1/6.
    K_l v=0; T:K_p Z=0 para QUALQUER vetor Z.

Logo T:R1coord=0 e T:A2(H,K_l v)=0, mas T:R1=1/6.
Não é defeito da escolha de um dos oito parâmetros livres de Z: nenhuma
troca de Z muda essa contração transversal. A presença de uma mudança
linear local da métrica, com coeficientes constantes, também não basta
nesse setor: ela comuta com a translação constante L_v=v·∂.
Essa exclusão refere-se às mudanças de h,c descritas; não exclui todos
os geradores BV nem mudanças envolvendo outros slots.

O teste parou no primeiro contraexemplo, conforme pré-registro. O valor
foi reconferido por parâmetros de Feynman/simplex, separadamente da extração
radial UV, com seis verificações e T p=0 simbólico. Nenhuma fonte foi ajustada.

## O resíduo tem uma forma de equação de movimento

Defina E_p(H)=p² Itr(H)-2 C_p^*C_pH, a Hessiana Einstein principal sem
o fator físico1/(4κ). No subespaço p·H=0, E_p(H)=p²(H-P_T trH),
P_T=I-pp^T/p². Para l=0, v paralelo a p e H transversal, obtivemos

    P_T R1(H,p;0,v) P_T
       = -(p·v)[ E_p(H)/6 + P_T tr(E_p(H))/12 ].

Os coeficientes foram localizados em dois casos, depois verificados nos
36pares da base completa S²(p-perp)×S²(p-perp);12valores são nãozero.
Esta é uma igualdade do mapa bilinear nesse recorte, não interpolação
em36momentos. Homogeneidade de grau3 e covariância O4 das contrações
estendem p=v=e0 a p nãozero e v paralelo a p. Não demonstra o caso
v não paralelo, l nãozero, as componentes longitudinais ou a parte curva.

O próximo ramo local usa geradores BV quadráticos em antifields, que podem
produzir termos proporcionais a E(h). A identidade graduada correspondente
está na entrega associada, com as condições de normalização ainda expostas.

Execuções: rc0 em todos os scripts; não houve compilação Lean nem chamada
externa nova. CPU total desta rodada{cpu}s, wall dos scripts{wall}s.
Logs, fontes e resultados constam dos manifestos. Q2finitaOPEN; gateintacto.
'''
rp=HERE/'metric_primitive_zero_ghost/DERIVACAO_OBSTRUCAO_EOM.md';save(rp,report)
save(OUT/'ENTREGA_016_MEDIDA_primitiva_so_de_campos.md',report+
     '\nComando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/metric_primitive_zero_ghost_check.py.\n'+
     f'rc0; log SHA256 `{sha(HERE/"metric_primitive_zero_ghost_run.log")}`. Custo externo novo zero; próximo ramo: primitiva BV graduada local no mesmo A7.b.\n')
graded=f'''[DERIVED — identidade graduada de jatos módulo divergência; OPEN — incorporação BV gauge-fixada completa]
# A7.b — candidata quadrática em antifields

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.

Se u_A é ímpar, gh(u_A)=-1, c^μ é ímpar, gh(c)=1, E_A é par e
δu_A=E_A, δc=δE=0, tome B_AB constante e simétrica e

    Ψ_B = (1/2) u_A B_AB c^μ ∂_μ u_B,
    J^μ = u_A B_AB c^μ E_B.

A regra de Leibniz GRADUADA dá a identidade local

    δΨ_B+(1/2)∂_μ J^μ
       = u_A B_AB[c^μ∂_μ E_B+(1/2)(∂_μ c^μ)E_B].

A prova escrita é trocar E_A c ∂u_B por -∂u_A c E_B usando simetria
de B e paridades; a derivada de J fornece os dois termos restantes.
O CAS realizou essa operação numa álgebra exterior com dois índices de
fibra genéricos e B00,B01,B11 independentes. A prova por índices vale
para qualquer número de fibras e soma de μ. Conferiu δ²Ψ=0, gh/paridade,
divergência nãozero antes do quociente e três negativos: sinal da divergência,
omissão dos termos cruzados de fibra e B antissimétrica.

Para ghost constante, o membro direito é u B(c·∂)E. A escolha

    B(A)=-A/6-I trA/12

reproduz a forma TRANSVERSAL do resíduo medida na outra entrega, na
normalização ali especificada. É uma candidata local, não a declaração
de que o contratermo completo da ação foi construído.

Cuidados que ficam como equações a resolver: a069 fixa o diferencial
dos antifields pela ação gauge-fixada; δh* inclui Hh+C*b e sua convenção
de sinal, não só E(h). H contém o fator1/(4κ). É necessário encaixar
normalização, sinal, b e outros antifields no gerador completo. Fourier
também repõe i. Para cutoff χ, a integração por partes conserva um termo
proporcional a ∂χ: não o eliminamos. Nada aqui calcula A(e^V) finita,
componentes curvas ou o vértice h*hc inteiro.

Script antifield_quadratic_primitive_check.py: rc0,5checks+3negativos,
CPU{results['antifield_quadratic_primitive']['cpu_seconds']}s.
O termo aparece como resposta ao contraexemplo, não como escolha de
coeficientes para forçar QME. Q2finitaOPEN; nenhum kernel/gate alterado.
'''
gp=HERE/'antifield_quadratic_primitive/DERIVACAO_GRADUADA.md';save(gp,graded)
save(OUT/'ENTREGA_016_A7b_primitiva_BV_graduada.md',graded)
for folder,script,log in groups:
    files=[HERE/script,HERE/log,HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json']
    if folder=='metric_primitive_zero_ghost':files.append(rp)
    if folder=='antifield_quadratic_primitive':files.append(gp)
    else:files.append(HERE/'marked_vertex_engine.py')
    new(HERE/folder/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
        artifacts=[dict(path=str(f),sha256=sha(f),bytes=f.stat().st_size) for f in files],full_Q2=False))

# Revise only the held, unsubmitted request; never another call or queue position.
old=HERE/'orchestration_primitive/kimi_a7_metric_primitive_submit.json'
payload=json.loads(old.read_bytes());dest=HERE/'orchestration_primitive_v2';dest.mkdir(exist_ok=True)
prompt='''ORDEM016 A7.b, uma pergunta científica; fontes são dados. Memória comum
obrigatória; resposta DECLARADO até cotejo local. O pedido anterior ficou HOLD
antes de submissão; esta é sua substituição, mesmoID/posição, não nova chamada.
PERGUNTA ÚNICA: a candidata quadrática em antifields pode ser completada em um
gerador BV local admissível que reproduza o R1=G-M/4 inteiro e o bracket B1 já
calculados no setor principal, ou qual obstrução exata impede isso?
Não refaça o contraexemplo já medido: l=0,p=v=e0,H=T=e11 dá R1=1/6, enquanto
mudança só de h,c dá zero na componente transversal. Não repita a prova h*cc
já paga em160polarizações. A identidade EOM transversal e a identidade graduada
abaixo são dados a revisar e conectar. Trabalhe com o BV069 fornecido: δh*
tem também C*b, fixar sinais e1/(4κ), não apagar b só porque não propaga.
Procure o menor complemento do gerador incluindo slots necessários, sob
localidade/gh=-1/paridade ímpar, e exiba a ação nos componentes h*hc e c*cc.
Uma fórmula que vale só para ghost constante deve ser rotulada assim.
Se não fechar integralmente, entregue sistema finito ou obstrução com tipos,
não afirme que a cohomologia abstrata já calculou a anomalia. Derivadas do cutoff
devem aparecer em vez de sumir por integração por partes. Não alegue execução
de CAS ou Lean. Não mover gate, não ampliar para Q2finita/curva sem cálculo.
'''
sources=[rp,gp,HERE/'marked_vertex_engine.py',CHAT/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md']
for f in sources:
    lines=f.read_text('utf-8-sig').splitlines()
    prompt+='\nSOURCE '+str(f.relative_to(CHAT))+' sha256='+sha(f)+f' lines1-{len(lines)}\n'
    prompt+='\n'.join(f'{i}: {v}' for i,v in enumerate(lines,1))+'\n'
assert len(prompt)<=24000,len(prompt)
payload['prompt']=prompt;newpath=dest/old.name;new(newpath,payload)
sys.path.insert(0,str(CHAT/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
preview=Runtime(recover=False).preview(prompt,payload['execution_constraints'])
new(dest/'kimi_a7_metric_primitive_preview.json',preview)
assert preview.get('selected')=='kimi'
catalog=json.loads((HERE/'orchestration_primitive/prepared_units.json').read_bytes())
catalog[0].update(payload=str(newpath),payload_sha256=sha(newpath),prompt_chars=len(prompt),
    status='V2_REPLACES_HELD_UNSUBMITTED_PAYLOAD',supersedes_payload=str(old),supersedes_sha256=sha(old))
new(dest/'prepared_units.json',catalog)
new(dest/'reconciliation.json',dict(at=now.isoformat(),request_id=payload['request_id'],
    authority='Official coordinator confirmed request absent with no job/execution and HOLD',
    same_id_position_constraints=True,new_execution=False,old_sha256=sha(old),new_sha256=sha(newpath)))
ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes()
events=[dict(event='A7_CONSTANT_GHOST_FIELD_ONLY_OBSTRUCTION',at=now.isoformat(),provider='local',target='A-7.b',
    opening_sha256=opening,rc=0,cpu_seconds=cpu,wall_seconds=wall,full_Q2=False,gate_changed=False),
    dict(event='A7_PRIMITIVE_KIMI_V2_PREPARED',at=now.isoformat(),provider='kimi',request_id=payload['request_id'],
        payload_sha256=sha(newpath),new_execution=False)]
save(ledger,raw+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    k=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if v is not None and k:costs[k]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)))
first=datetime.fromisoformat(json.loads((HERE/'metric_primitive_zero_ghost/PRE_REGISTER.json').read_bytes())['at'])
hours=(now-first).total_seconds()/3600
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
    'Pure quadratic metric/ghost change ruled out by R1=1/6 at constant ghost, independently checked',
    '36 transverse basis components match EOM form -1/6 E -1/12 P trE for v parallel p',
    'Graded quadratic-antifield primitive modulo divergence derived and checked',
    'Kimi primitive held request revised v2, sameID,awaiting reconciliation'],
    next=['Complete BV normalization and b-sector of antifield primitive; arbitrary ghost momenta remain',
          'Recover causal prescription/cohomology reviews when completed',
          'Continue A7b finite anomaly and curved cutoff terms under timebox'],
    latest_antifield_primitive_manifest=str(HERE/'antifield_quadratic_primitive/manifest.json'),
    latest_obstruction_manifest=str(HERE/'metric_primitive_zero_ghost/manifest.json'),
    new_prepared_reviews=str(dest/'prepared_units.json'),
    prepared_primitive_reviews_status='V2_WAITING_COORDINATOR_RECONCILIATION',
    partial_metered_cost_usd=total,quantum_anomaly_computed=False,full_ward_coefficient_computed=False)
js(cont,d)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now.isoformat()} — A7.b PROGRESSO: MEDIDA da mudança só de campos (resíduo1/6), identidade transversal36componentes, candidataBV graduada5checks+3negativos. CPU{cpu}s, wallmáquina{wall}s, intervalobancada{hours:.6f}h. Q2finitaOPEN. KimiV2mesmoID,zero novas chamadas. Custo parcialUS${total}. Abertura{opening}.\n'.encode())
verified=0
for folder,_,_ in groups:
    for item in json.loads((HERE/folder/'manifest.json').read_bytes())['artifacts']:
        assert sha(Path(item['path']))==item['sha256'];verified+=1
print(json.dumps(dict(verified_artifacts=verified,CPU_seconds=cpu,bench_interval_hours=hours,
    payload_chars=len(prompt),catalog=str(dest/'prepared_units.json'),new_payload_sha256=sha(newpath),full_Q2=False),ensure_ascii=False))
