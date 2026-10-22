"""Record a fixed primitive extension and the reviewed, uncompiled Kimi result."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json

HERE=Path(__file__).resolve().parent
CHAT=HERE.parents[1]
OUT=CHAT/'TUNEL/DO_CHATGPT'
DEST=HERE/'primitive_extension'
REV=HERE.parent/'A6_EQUACAO_DA_VERDADE/received_reviews'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    if isinstance(raw,str):raw=raw.encode('utf-8')
    assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)
def replace(p,raw):
    if isinstance(raw,str):raw=raw.encode('utf-8')
    old=p.read_bytes()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(p.with_name(p.name+'.bak_'+stamp),old)
    t=p.with_name(p.name+'.replacement_'+stamp)
    new(t,raw)
    t.replace(p)
    assert p.read_bytes()==raw
r=json.loads((DEST/'results.json').read_bytes())
assert r['source_sha256']==sha(HERE/'primitive_extension_check.py')
assert r['plan_sha256']==sha(DEST/'PRE_REGISTER.json')
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — extensão primitiva; REAL — CAS algébrico; OPEN — produtos completos e anomalia]
# A7.b — primeira extensão não linear com normalização explícita

Abertura sha256 `{opening}`.

## Convenção fixada antes do cálculo

Assinatura +---, z=x²−i0, □=∂t²−∑∂i². μ_R>0 é uma escala de referência fixa,
mantida simbólica; não é ajustada após observar Ward. Para a distribuição z^−2
fora da origem, escolhe-se

    R2 = −(1/4) □ [log(μ_R² z)/z],

sem adicionar termo delta finito. O kernel log(z)/z tem grau de escala2,
portanto sua extensão à origem é única; a derivada é distribucional. A
escolha é Lorentz-covariante. O CAS verifica a identidade radial longe da
origem: □F(z)=4z F''(z)+8F'(z). Não verifica frente de onda nem existência
distribucional por amostragem numérica.

[KNOWN] Hollands, §3.4, eq223–227, constrói a extensão pelo termo finito de
uma família meromorfa. O texto omite fatores numéricos no exemplo; os nossos
coeficientes são calculados na convenção acima. No fim de §3.3, T10/T11 ainda
exigem ajustes da extensão. Portanto essa conta não certifica todos os produtos.
https://arxiv.org/html/0705.3340v4

## Derivação dos coeficientes e do contato de escala

A identidade radial fornece, antes de tomar a parte finita,

    U_a = (μ_R²)^a z^(−2+a)
        = □[(μ_R²)^a z^(−1+a)]/[4a(a−1)].

O kernel dentro de □ tem expansão

    −1/(4a z) − [1+log(μ_R²z)]/(4z) + O(a).

Logo a parte finita analítica e a escolha diferencial são diferentes:

    FP U_a = R2 − (1/4)□(1/z).

O contato pode ser normalizado sem importar o prefator suprimido da fonte.
Fixe a transformada inversa com exp(−ipx)/(2π)^4. O inverso de □ tem
transformada −1/(p²+i0), de modo que □G0=δ0. O contorno em p0 no ponto
t=0 dá i/(2|p|); a transformada espacial de 1/(2|p|) é 1/(4π²r²).
A expressão Lorentz-invariante correspondente é G0=−i/(4π²z). Assim

    □(1/z) = 4iπ² δ0,
    Res_(a=0) U_a = −iπ² δ0,
    FP U_a = R2 − iπ² δ0,
    μ_R dR2/dμ_R = −2iπ² δ0.

A identidade de contorno/boundary value é uma derivação escrita; o CAS usa
esse contato como entrada analítica e verifica os coeficientes resultantes.
Para o quadrado do inverso principal G0, sem os fatores Wick iħ nem pesos
dos vértices, isso dá

    μ_R d[R(G0²)]/dμ_R = i/(8π²) δ0.

É um contato de ESCALA do kernel primitivo, não uma anomalia Ward/BRST.
Curvatura, tensor B^−1, ghosts e todos os vértices ainda entram na contração
real da teoria. Este G0 é o inverso principal plano usado na expansão local;
não substitui o Green exato do fundo curvo.

Para n>=3, a mesma escolha se prolonga por

    Rn = □R_(n−1)/[4(n−1)(n−2)]
       = −□^(n−1)[log(μ_R²z)/z]/[4^(n−1)(n−1)!(n−2)!].

O CAS verifica n=2,...,5. Isso é uma família radial, não autorização para
renormalizar todo produto tensorial escolhendo decomposições arbitrárias:
as identidades entre decomposições, diagonais parciais e T10/T11 ainda precisam
ser conciliadas. A condição linear de Fröb já fixada permanece exigida.

## Verificação e alcance

Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/primitive_extension_check.py`.
rc0 observado; {r['checks_passed']} checks e {r['negative_controls_detected']} negativos passam, Sympy {r['sympy_version']}.
wall {r['wall_seconds']}s; CPU {r['cpu_seconds']}s. Resultado estruturado direto;
sem arquivo stdout independente. Plano anterior à execução; manifesto com hashes.
Não houve CAS de distribuições, renormalização de todos os grafos, coeficiente
Ward completo, novo Lean ou alteração do gate. Próximo trabalho: extensão
tensorial compatível com os contatos e a hierarquia, antes da soma da quebra.
'''
new(DEST/'DERIVACAO_EXTENSAO.md',report)
manifest=dict(statute='REAL_ALGEBRA_AND_DERIVED_PRIMITIVE_DISTRIBUTION',
    opening_sha256=opening,observed_rc=0,rc_source='exec_command',independent_stdout_captured=False,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in [HERE/'primitive_extension_check.py',
        DEST/'PRE_REGISTER.json',DEST/'results.json',DEST/'DERIVACAO_EXTENSAO.md']],
    all_graphs_renormalized=False,quantum_anomaly_computed=False)
new(DEST/'manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
new(OUT/'ENTREGA_016_A7b_extensao_primitiva.md',report)

job='93c0358f-04f8-4bea-a4d6-6977171d6fed'
receipt=json.loads((REV/(job+'.json')).read_bytes())
response=REV/(job+'.md')
assert sha(response)==receipt['response_sha256']
source=HERE.parent/'A6_EQUACAO_DA_VERDADE/B_fechamentos/TheEquationOfTruth_T20_v3.lean'
review=f'''[DERIVED — revisão escrita; DECLARADO — candidatos Lean; OPEN — compilação do limite forte]
# Revisão Kimi A6.B1d

Abertura sha256 `{opening}`.
Resposta lida inteira: `{response.name}`, sha256 `{sha(response)}`.
Fonte de definições lida: `{source.name}`, sha256 `{sha(source)}`.
T/flow nas linhas174–177 não pressupõem dimensão finita; reading nas linhas182–183
é a projeção ortogonal do kernel; FlowTendsToFamily nas linhas299–300 é convergência
para cada vetor. Isso confirma a tipagem que o executor inferiu.

A rota por densidade é coerente para H limitado, positivo e auto-adjunto em
Hilbert completo: ran(H)^perp=ker(H), logo closure(ran(H))=ker(H)^perp.
Das cotas ||exp(−sH)||<=1 e ||exp(−sH)H||<=1/(e s), para z nesse fecho,
escolhe-se Hy a distância <epsilon/2 de z e s>2||y||/(e epsilon).
Então ||exp(−sH)z||<epsilon. A parcela na projeção permanece fixa.
As cotas espectrais precisam ser demonstradas no formalismo Lean, não assumidas
como nomes de API. O texto recebido não contém corpos Lean nem compilação.

Correções: a afirmação de que CFC não produz o candidato é excessiva. No próprio
diag(1/n), a projeção é 0, que é CFC da função zero; o que falha é a convergência
uniforme das exponenciais. Sem gap significa ausência de taxa uniforme em norma,
não ausência de toda taxa para um vetor. H=0 deve ser tratado separadamente quando
se escreve mínimo do espectro positivo vazio. A rota de Vigier exige cotas para
s,t>=0; não se deve aplicar 0<=T_s−T_t<=I para tempos negativos.

A auditoria local anterior já havia localizado a passagem por densidade como
pendência. A resposta desenvolve sua prova escrita, sem substituir a compilação
nem pagar B1d. Nenhum novo ciclo Lean foi gasto nesta revisão, nenhum gate alterado.
Execução única {receipt['execution_id']}; metadados preservados no recibo JSON.
Nenhuma nova chamada: o resultado foi recuperado pela API existente.
'''
new(REV/'REVISAO_KIMI_A6_B1d.md',review)
new(REV/'REVISAO_KIMI_A6_B1d.json',json.dumps(dict(
    job_id=job,execution_id=receipt['execution_id'],response_sha256=sha(response),
    source_sha256=sha(source),review_sha256=sha(REV/'REVISAO_KIMI_A6_B1d.md'),
    response_read_full=True,lean_compiled_this_review=False,strong_limit_formalized=False,
    gate_changed=False),ensure_ascii=False,indent=2))

ledger=OUT/'LEDGER_016.jsonl'
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
event=dict(event='A7B_PRIMITIVE_EXTENSION_AND_KIMI_B1D_REVIEW_20260924',
    at=datetime.now(timezone.utc).isoformat(),target='A7.b',provider='local_CAS_and_review',
    external_calls=0,result_sha256=sha(DEST/'results.json'),
    review_sha256=sha(REV/'REVISAO_KIMI_A6_B1d.md'),
    wall_seconds=r['wall_seconds'],cpu_seconds=r['cpu_seconds'],rc=0,
    quantum_anomaly_computed=False)
assert not any(a.get('event')==event['event'] for a in rows)
replace(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
costs={}
for a in rows:
    cost=a.get('cost_estimate_usd',a.get('cost_usd',a.get('custo_usd')))
    key=a.get('execution_id') or a.get('job_id') or a.get('request_id') or a.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
replace(progress,progress.read_bytes()+f'\n- {event["at"]} — A7.b EXTENSAO_PRIMITIVA: parcial; quebra NÃO PAGA; 11 checks/3 negativos rc0, máquina {r["wall_seconds"]/3600:.9f}h. B1d Kimi recebido/revisado, sem compilação nova; tempo de bancada não instrumentado. Zero novas chamadas, custo deduplicado parcial US${total}; não fatura.\n'.encode())
cp=HERE/'CONTINUIDADE.json'
c=json.loads(cp.read_bytes())
c.update(at=event['at'],previous_goal_turn='PROGRESS',
    completed_this_turn=['Fixed primitive nonlinear Lorentzian differential extension',
        '11 exact algebra checks and 3 negative controls',
        'Kimi B1d recovered and reviewed with CFC overstatement corrected'],
    next=['Complete tensor and multilocal extensions compatible with T10/T11',
        'Calculate full Ward coefficient only after prescription completion',
        'Consume A7 queued results; no duplicate requests'],
    primitive_extension_manifest=str(DEST/'manifest.json'),
    strong_limit_review=str(REV/'REVISAO_KIMI_A6_B1d.md'))
replace(cp,json.dumps(c,ensure_ascii=False,indent=2))
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7b_extensao_primitiva.md'),
    manifest_sha256=sha(DEST/'manifest.json'),partial_metered_cost_usd=str(total)),ensure_ascii=False))
