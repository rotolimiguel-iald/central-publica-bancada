"""Record the exact truncation audit and next obligation without promoting it to QME."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import json
import hashlib

HERE=Path(__file__).resolve().parent
CHAT=HERE.parents[1]
DEST=HERE/'quantum_filtration'
OUT=CHAT/'TUNEL/DO_CHATGPT'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def new(p,raw):
    if isinstance(raw,str):raw=raw.encode('utf-8')
    if p.exists():
        assert p.read_bytes()==raw,str(p)
        return
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)

def append(p,raw):
    if isinstance(raw,str):raw=raw.encode('utf-8')
    old=p.read_bytes()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(p.with_name(p.name+'.bak_'+stamp),old)
    t=p.with_name(p.name+'.tmp_'+stamp)
    new(t,old+raw)
    t.replace(p)
    assert p.read_bytes()==old+raw

result=json.loads((DEST/'results.json').read_text('utf-8'))
assert result['source_sha256']==sha(HERE/'quantum_filtration_check.py')
assert result['plan_sha256']==sha(DEST/'PRE_REGISTER.json')
assert all(c['passed'] for c in result['checks'])
assert all(c['detected'] for c in result['negative_controls'])
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
text=f'''[DERIVED — filtração perturbativa; REAL — CAS exato; OPEN — quebra quântica]
# A7.b — contrair antes de truncar a valência externa

Abertura da ORDEM016: sha256 `{opening}`.

## O cálculo que muda a preparação

A087 define C_N pela valência clássica e prova que s não a reduz (linhas11–13).
Essa afirmação não diz que a mesma projeção comuta com contrações quânticas.
Num par bosônico com contração formal ħ C, para monômios não normalizados,

    q^(N+1) ⋆ q = q^(N+2) + (N+1) ħ C q^N.

O primeiro fator é zero em C_N, mas o segundo termo do produto não é. A idealidade
clássica não se transfere ao produto deformado. A identidade é algébrica para todo
N>=0; o CAS verifica N=2,...,8. C denota um pareamento de contração, não um número
de amplitude física. Não é necessário tomar um valor singular de propagador em x=x.

Para duas inserções distintas a conta de Wick dá

    [(ħ C)^2/2!] (d_x^2 x^7)(d_y^2 y^3) = 126 ħ² C² x^5 y.

São seis pernas externas, duas linhas internas e dois vértices: L=I−V+1=1.
O poder ħ² do produto temporal NÃO é o número de laços; os fatores de vértice e a
normalização da ação efetiva precisam ser incluídos. Nenhuma distribuição foi
estendida, nenhum índice métrico/ghost foi contraído e nenhum coeficiente Ward foi obtido.

## Corte compatível

Uma contração de ordem r leva ħ^p A_m e ħ^q A_n a
ħ^(p+q+r) A_(m+n−2r). O peso E+2p é aditivo: a perda de dois campos é compensada
pelo peso dois de ħ. Portanto a filtração conjunta, com potências não negativas de
ħ, é compatível com esse produto formal. A expansão de S contém ħ inversos;
para a ação efetiva conectada usa-se separadamente a identidade da fonte069:

    Σ_v (v−2) = E+2L−2.

Com vértices de interação v>=3 e L=1, V<=E e cada v<=E+3−V.
Para E<=6, isso requer considerar vértices até8; em grafos com V>=2, até7.
O exemplo (7,3) mostra por que C6 aplicado ANTES dos produtos não basta.
Se uma ordenação elimina tadpoles de um único vértice, isso não elimina por si a
família (7,3). A identidade vale para a contagem topológica; contatos, antifields
externos, graduação e inserções marcadas exigem a análise própria da Ward.

O CAS enumera29 PARTIÇÕES DE VALÊNCIAS para E=1,...,6 e L=1, das quais11 têm E=6.
Três famílias contêm vértice>6. Não são29 grafos nem29 amplitudes não nulas.
O termo cosmológico admite coeficientes de grau7/8: na direção local de posto1,
sqrt(det(1+q e_00))=sqrt(1+q), com coeficientes33/2048 e−429/32768.
Isso verifica disponibilidade de vértices, sem excluir cancelamentos da ação completa.

## Consequência e verificação

Registrar a projeção EXTERNA após as contrações e a graduação por ħ/pernas antes
de fixar a prescrição temporal. O C6 clássico continua válido em seu domínio.
Esta é uma obrigação de implementação, não obstrução à existência da teoria.
A prescrição completa e o coeficiente a_1 em H^(1,4)(s|d_H) continuam pendentes.
Não se escolhe a_1=0 por definição nem se transporta H4 clássico para esse grupo.

Comando executado: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/quantum_filtration_check.py`.
rc0 observado pela ferramenta exec_command; {result['checks_passed']} checks e
{result['negative_controls_detected']} negativos; {result['wall_seconds']}s de cálculo,
{result['cpu_seconds']}s CPU. A saída estruturada foi gravada diretamente pelo script;
não foi capturado um arquivo stdout independente. Reprodução não sobrescreve o plano.
Plano, fonte e resultado têm hashes no manifesto associado. Sem Lean novo/original/gate.

Fontes locais: A087 linhas11–13,69–71; Q2_069 §§4–6; contrato072 §5 (hashes no plano).
Leitura primária delimitada: BFR, §3.4, equações52–54, distingue o produto fora da
diagonal e as extensões com liberdade local. Não fornece o coeficiente deste cálculo.
https://arxiv.org/html/1306.1058v4
'''
new(DEST/'DERIVACAO_FILTRACAO.md',text)
manifest=dict(status='REAL_EXACT_TRUNCATION_AUDIT',
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in [HERE/'quantum_filtration_check.py',
        DEST/'PRE_REGISTER.json',DEST/'results.json',DEST/'DERIVACAO_FILTRACAO.md']],
    observed_command_rc=0,rc_source='exec_command tool result',
    independent_stdout_log_captured=False, quantum_anomaly_computed=False,
    products_prescription_fixed=False,gate_changed=False)
new(DEST/'manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
new(OUT/'ENTREGA_016_A7b_filtracao_quantica.md',text)
ledger=OUT/'LEDGER_016.jsonl'
rows=[json.loads(s) for s in ledger.read_text('utf-8-sig').splitlines() if s.strip()]
event='A7B_QUANTUM_FILTRATION_EXACT_20260924'
if not any(r.get('event')==event for r in rows):
    append(ledger,json.dumps(dict(event=event,at=datetime.now(timezone.utc).isoformat(),
        target='A7.b',provider='local_CAS',external_calls=0,
        result_sha256=sha(DEST/'results.json'),wall_seconds=result['wall_seconds'],
        cpu_seconds=result['cpu_seconds'],rc=0,quantum_anomaly_computed=False),ensure_ascii=False)+'\n')
costs={}
for row in rows:
    cost=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    key=row.get('execution_id') or row.get('job_id') or row.get('request_id') or row.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
marker='A7.b FILTRACAO_QUANTICA_EXATA'
if marker not in progress.read_text('utf-8-sig'):
    append(progress,f'\n- {datetime.now(timezone.utc).isoformat()} — {marker}: parcial; quebra NÃO PAGA. '
        f'{result["checks_passed"]} checks/{result["negative_controls_detected"]} negativos, '
        f'cálculo {result["wall_seconds"]/3600:.9f}h; tempo humano/bancada desta etapa não instrumentado. '
        f'Zero novas chamadas; custos explicitamente registrados e deduplicados US${total} '
        '(parcial, estimativa; não fatura; assinatura não equivale a zero).\n')
continuity=HERE/'CONTINUIDADE.json'
old=continuity.read_bytes()
value=json.loads(old)
value.update(at=datetime.now(timezone.utc).isoformat(),previous_goal_turn='PROGRESS',
    completed_this_turn=['Kimi single-time review reused existing compiled lemma',
        'Quantum valence filtration audit: 27 exact checks and 11 negative controls'],
    next=['Complete explicit temporal prescription, with external truncation AFTER contractions',
        'Keep vertices up to eight for one-loop external valence six before graph-specific exclusions',
        'Consume A7 executor responses without changing existing requests'],
    quantum_anomaly_computed=False)
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
new(continuity.with_name(continuity.name+'.bak_'+stamp),old)
tmp=continuity.with_name(continuity.name+'.tmp_'+stamp)
new(tmp,json.dumps(value,ensure_ascii=False,indent=2))
tmp.replace(continuity)
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7b_filtracao_quantica.md'),
    manifest_sha256=sha(DEST/'manifest.json'),partial_metered_cost_usd=str(total)),ensure_ascii=False))
