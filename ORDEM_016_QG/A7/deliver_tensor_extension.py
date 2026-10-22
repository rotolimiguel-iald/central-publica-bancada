"""Preserve the measured one-pair calculation and its exact scope."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'TUNEL/DO_CHATGPT'
DEST = HERE / 'tensor_extension'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p, data):
    if isinstance(data, str): data = data.encode('utf-8')
    assert data and not p.exists(), str(p)
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f: f.write(data)
    assert tmp.read_bytes() == data
    tmp.replace(p)
def append(p, data):
    old = p.read_bytes()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(p.with_name(p.name + '.bak_' + stamp), old)
    tmp = p.with_name(p.name + '.replacement_' + stamp)
    new(tmp, old + data.encode('utf-8'))
    tmp.replace(p)
    assert p.read_bytes() == old + data.encode('utf-8')

r = json.loads((DEST/'results.json').read_bytes())
assert r['source_sha256'] == sha(HERE/'tensor_extension_check.py')
assert r['plan_sha256'] == sha(DEST/'PRE_REGISTER.json')
opening = sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report = f'''[DERIVED — extensão de um par; REAL — álgebra exata; OPEN — prescrição completa e quebra Ward]
# A7.b — extensão tensorial e contatos entre normalizações

Abertura sha256 `{opening}`.

## Prescrição anterior ao CAS e correção ao lado

Na convenção +---, z=x²−i0 e C=4iπ², usa-se □(1/z)=Cδ da derivação
primitiva. Para kernels de UM PAR de pontos, fixou-se antes desta conta:

    R(u) = FP_(a=0) [(1−a) μ_R^(2a) z^a u].

O mesmo regulador a é usado para todos os kernels relacionados por multiplicação
polinomial. μ_R>0 permanece escala de referência simbólica, não ajustada após
Ward. A continuação meromorfa é o insumo distribucional: o CAS não a constrói.
Assim R(pu)=pR(u) para polinômios p, por linearidade da extração de Laurent.
Isso conserva contrações, mas NÃO implica R(∂u)=∂R(u).

A família diferencial anterior D_n era uma extensão válida de cada potência
separadamente. Ainda não era uma prescrição conjunta multiplicativa, como já
advertia seu relatório. Agora R_2=D_2 conserva exatamente a normalização
primitiva, mas potências superiores recebem contatos finitos determinados.

Se U_n(a)=μ_R^(2a)z^(−n+a), r_n=−1/[4^(n−1)(n−1)!(n−2)!], então

    Res U_n = C r_n □^(n−2)δ,
    D_n = r_n □^(n−1)[log(μ_R²z)/z],
    FP U_n = D_n + (H_(n−1)+H_(n−2)) Res U_n,
    R_n = D_n + (H_(n−1)+H_(n−2)−1) Res U_n.

Aqui H_j é número harmônico; não é Hamiltoniano. Os coeficientes vêm da expansão
de 1/∏_(j=2)^n [4(j−1−a)(j−2−a)]. Exemplo concreto:

    R_3 = D_3 − (3C/64)□δ,
    z D_3 = D_2 + (3C/8)δ,     z R_3 = R_2.

Usou-se z□^mδ=4m(m+1)□^(m−1)δ em quatro dimensões. Para n>=3,

    □R_(n−1) = 4(n−1)(n−2)R_n − 4(2n−3)Res U_n.

Isso exibe o contato que seria perdido ao exigir simultaneamente a recorrência
diferencial sem contatos e multiplicação polinomial sem contatos.

## Tensor de posto dois: o traço verifica a normalização

Para x_μ x_ν/z³, diferenciar z^(−1+a) ANTES de tomar a parte finita fornece

    T_μν(a) = ∂_μ∂_ν[μ_R^(2a)z^(−1+a)]/[4(a−1)(a−2)]
              − η_μν U_2(a)/[2(a−2)].

Aplicando o mesmo fator (1−a), resulta

    R_μν = (1/8)∂_μ∂_ν(1/z) + (1/4)η_μν R_2 − (C/32)η_μν δ.

A contração dá η^μν R_μν=R_2. Sem o último termo, o traço teria o erro
Cδ/8. Equivalentemente,

    ∂_μ∂_ν(1/z) = 8R_μν − 2η_μν R_2 + (C/4)η_μνδ.

Esse contato é de normalização distribucional. NÃO é, sozinho, a anomalia
BRST. Para derivadas, a identidade geral é

    ∂_μ R(u) − R(∂_μu)
      = 2 FP [a(1−a) μ_R^(2a)z^a (x_μ/z)u].

Se a família entre colchetes sem a(1−a) tem coeficientes c_−2/a²+c_−1/a+…,
o resultado é 2(c_−1−c_−2). Usar só 2Res omite o polo duplo dos termos
logarítmicos. Não se presume derivação sem anomalia de normalização.

## Evidência e próximo uso

Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/tensor_extension_check.py`.
rc0 observado na sessão de execução33481; {r['checks_passed']} identidades e
{r['negative_controls_detected']} controles negativos, Sympy {r['sympy_version']}.
wall {r['wall_seconds']}s; CPU {r['cpu_seconds']}s. Saída estruturada preservada;
nenhum stdout independente. Verificados n=2,…,7 e o tensor acima. Alguns checks
avaliam consequências algébricas de identidades distribucionais assumidas;
não substituem uma prova dessas identidades. Revisão adversarial será externa.

Escopo: kernels homogêneos principais, um par, espaço tangente plano.
Não há extensão de todas as diagonais de grafos, curvatura completa, ajuste de
T10/T11, soma métrica+ghosts+antifields, nem coeficiente de quebra Ward calculado.
O dado permite construir uma tabela de contatos coerente para essa soma.
Não move o item interagente da QG, não altera kernel, um.py ou gate.
'''
new(DEST/'DERIVACAO_TENSORIAL.md', report)
artifacts = [HERE/'tensor_extension_check.py', DEST/'PRE_REGISTER.json',
             DEST/'results.json', DEST/'DERIVACAO_TENSORIAL.md']
manifest = dict(opening_sha256=opening, observed_rc=0, rc_source='write_stdin_session_33481',
    artifacts=[dict(path=str(p), sha256=sha(p)) for p in artifacts],
    quantum_anomaly_computed=False, all_graphs_renormalized=False, gate_changed=False)
new(DEST/'manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
new(OUT/'ENTREGA_016_A7b_extensao_tensorial.md', report)
event = dict(event='A7B_TENSOR_EXTENSION_20260924', at=datetime.now(timezone.utc).isoformat(),
    target='A7.b', provider='local_CAS', external_calls=0,
    manifest_sha256=sha(DEST/'manifest.json'), result_sha256=sha(DEST/'results.json'),
    wall_seconds=r['wall_seconds'], cpu_seconds=r['cpu_seconds'], rc=0,
    checks=r['checks_passed'], negative_controls=r['negative_controls_detected'],
    quantum_anomaly_computed=False)
ledger = OUT/'LEDGER_016.jsonl'
assert event['event'] not in ledger.read_text('utf-8-sig')
append(ledger, json.dumps(event, ensure_ascii=False)+'\n')
append(OUT/'ENTREGA_016_PROGRESSO.md',
    f'\n- {event["at"]} — A7.b EXTENSAO_TENSORIAL: parcial, quebra NÃO PAGA; 41 checks/8 negativos rc0; máquina {r["wall_seconds"]/3600:.9f}h; CPU {r["cpu_seconds"]}s. Bancada não instrumentada. Zero chamada externa nova; sem novo custo de provedor.\n')
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7b_extensao_tensorial.md'),
    manifest_sha256=sha(DEST/'manifest.json')), ensure_ascii=False))
