"""Record the partial prescription and actual EH variational contact, with custody."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json

HERE=Path(__file__).resolve().parent
CHAT=HERE.parents[1]
DEST=HERE/'linear_normalization_v2'
OUT=CHAT/'TUNEL/DO_CHATGPT'
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
result=json.loads((DEST/'results.json').read_bytes())
assert result['source_sha256']==sha(HERE/'linear_contact_check_v2.py')
assert result['plan_sha256']==sha(DEST/'PRE_REGISTER.json')
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — contato da ação métrica; REAL — CAS; KNOWN — normalização linear; OPEN — anomalia]
# A7.b — normalização linear e contato com cutoff na ação Einstein–Hilbert

Abertura sha256 `{opening}`.

## 1. Parte da prescrição fixada antes da conta

Adota-se a condição de normalização para inserções lineares da equação158 de
Fröb, arXiv1803.10235v3. O Teorema9, pp40–43, prova que a liberdade finita pode
implementá-la. A indução envolve número total de campos e aridade; não basta
zerar um coeficiente isolado. O Teorema8 usa essa condição para uma inserção
inteiramente dependente de antifields. Ele não elimina vértices mistos.
Os Teoremas3/6/7 e a prova9 foram conferidos no PDF; isso corrige ao lado a
limitação do HTML registrada em model_inputs/DERIVACAO_OPERADORES.md.
Fonte: https://arxiv.org/pdf/1803.10235v3 .

Essa escolha é parcial: fixa inserções lineares relativamente aos produtos
inferiores. Ainda não fixa todas as extensões não lineares, os termos finitos
compatíveis com o contrato072, nem calcula a quebra Ward.

No setor bosônico métrico, chamando H a Hessiana e t um teste tensorial compacto,
a identidade de Green converte essa normalização no contato

    T_(n+1)(F^n,h(Ht)) − T_n(F^n) ⋆ h(Ht)
      = i ħ n T_n(F^(n−1), δ_t F).

Mantém-se o primeiro termo off-shell: não aplicar a equação de campo dentro de T
e apagar o lado direito. A verificação abaixo calcula δ_t F numa família métrica
concreta; não calcula coeficientes quânticos das extensões.

## 2. Família que preserva a variável de perturbação

Tome h=u gbar, gnew=(1+u)gbar, e cutoff χ; Rbar=12K, Λ=3K.
Esta é uma restrição da ação Einstein–Hilbert a métricas, não um modelo quântico
escalar nem uma substituição do propagador tensorial. A variável é linear em h.

Derivação geométrica: para gnew=e^(2φ)gbar, a diferença de conexões é
C^a_bc=δ^a_b φ_c+δ^a_c φ_b−gbar_bc φ^a. Contraindo a diferença de Ricci,
o termo derivativo é −6□φ e o quadrático é −6(∇φ)^2. O CAS confere ambos
com índices Lorentzianos. Substituindo φ=log(1+u)/2 e a densidade (1+u)^2,
a lagrangiana puxada para essa família, por volume de fundo, fica

    Lχ = −χ/(2κ) [(1+u)Rbar −3□u
                  +3(∇u)^2/(2(1+u)) −2Λ(1+u)^2].

O Euler–Lagrange exato, sem descartar derivadas de χ, é

    Eχ = 1/(2κ) [−χ Rbar +4Λχ(1+u)
          +3χ□u/(1+u) −3χ(∇u)^2/(2(1+u)^2)
          +3∇χ·∇u/(1+u) +3□χ].

Em u=0 on-shell: Eχ=3□χ/(2κ); o cutoff impede confundir a equação localizada
com a equação de fundo sem cutoff. A contribuição tem suporte onde χ varia.

Subtraindo graus0,1,2 na MESMA variável linear u, a interação restrita é

    Vχ = 3χ/(4κ) [u/(1+u)] (∇u)^2,
    δVχ/δu = −3/(4κ) [χ(∇u)^2/(1+u)^2
                         +2χu□u/(1+u) +2u∇χ·∇u/(1+u)].

Logo há contato de gradiente do cutoff na interação, enquanto □χ pertence
à parte linear removida. Para o teste t gbar, δ_t V=∫t(δVχ/δu) μbar.
O setor cosmológico nessa família tem apenas graus até2, pois o determinante
é (1+u)^4. Isso não anula vértices cosmológicos de grau7/8 noutras direções;
a família de posto1 da conta de filtração é diferente da família de traço.

## 3. Resultado, correção de escopo e próximo elo

Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/linear_contact_check_v2.py`.
rc0 observado; {result['checks_passed']} identidades e {result['negative_controls_detected']} controles negativos passam;
wall {result['wall_seconds']}s, CPU {result['cpu_seconds']}s, Sympy {result['sympy_version']}.
Os vértices3–8 dão exatamente os contatos2–7. O teste recusa perda do cutoff,
troca de sinal cinético e confusão entre contato livre e interagente.
Resultado estruturado direto; não houve captura independente de stdout.

A conta anterior linear_contact_check.py também passou (13/5), mas usa
gnew=e^(2φ)gbar e subtrai o Taylor quadrático em φ. Isso muda a separação
livre/interação. É verificação auxiliar preservada, não a interação original
em h. A versão v2 é a referência para essa separação na família h=u gbar.

Não foram incluídas as polarizações métricas restantes, gauge, ghosts e
antifields nos contatos calculados. Nenhuma alteração de medida funcional
foi deduzida da mudança de coordenada, nenhum laço foi avaliado.
Falta completar a prescrição não linear e extrair a primeira quebra quântica
de ghost1/forma4. A normalização parcial não é uma prova de QME.
Sem novo Lean, mudança de original, gate ou confirmação física.
'''
new(DEST/'DERIVACAO_CONTATO.md',report)
manifest=dict(statute='REAL_LOCAL_CONTACT_PARTIAL_NORMALIZATION',
    opening_sha256=opening,observed_rc=0,rc_source='exec_command',
    independent_stdout_captured=False,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in [
        HERE/'linear_contact_check.py',HERE/'linear_normalization/PRE_REGISTER.json',
        HERE/'linear_normalization/results.json',HERE/'linear_contact_check_v2.py',
        DEST/'PRE_REGISTER.json',DEST/'results.json',DEST/'DERIVACAO_CONTATO.md']],
    complete_temporal_prescription=False,quantum_anomaly_computed=False,gate_changed=False)
new(DEST/'manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
new(OUT/'ENTREGA_016_A7b_normalizacao_linear_e_contato.md',report)
ledger=OUT/'LEDGER_016.jsonl'
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
event=dict(event='A7B_LINEAR_NORMALIZATION_METRIC_CONTACT_20260924',
    at=datetime.now(timezone.utc).isoformat(),target='A7.b',provider='local_CAS',
    external_calls=0,result_sha256=sha(DEST/'results.json'),rc=0,
    wall_seconds=result['wall_seconds'],cpu_seconds=result['cpu_seconds'],
    quantum_anomaly_computed=False,complete_temporal_prescription=False)
assert not any(r.get('event')==event['event'] for r in rows)
replace(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode('utf-8'))
costs={}
for r in rows:
    cost=r.get('cost_estimate_usd',r.get('cost_usd',r.get('custo_usd')))
    key=r.get('execution_id') or r.get('job_id') or r.get('request_id') or r.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
replace(progress,progress.read_bytes()+f'\n- {event["at"]} — A7.b NORMALIZACAO_LINEAR_CONTATO: parcial, quebra NÃO PAGA; v2 rc0, 15 checks/4 negativos. Máquina v2 {result["wall_seconds"]/3600:.9f}h; primeira conta auxiliar 2.1089064s. Bancada total da etapa não instrumentada. Zero novas chamadas. Custo acumulado medido/deduplicado parcial US${total}, não fatura; assinatura não equivale a zero.\n'.encode())
cp=HERE/'CONTINUIDADE.json'
c=json.loads(cp.read_bytes())
c.update(at=event['at'],previous_goal_turn='PROGRESS',
    completed_this_turn=['Frob Theorem9 proof read in primary PDF',
        'Partial linear-insertion normalization fixed',
        'Original linear metric split EH contact computed: 15 identities/4 negative controls'],
    next=['Complete nonlinear EG prescription before anomaly coefficient',
        'Retain cutoff contacts and original h-free split',
        'Consume staged A7 model results without duplicate calls'])
replace(cp,json.dumps(c,ensure_ascii=False,indent=2))
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7b_normalizacao_linear_e_contato.md'),
    manifest_sha256=sha(DEST/'manifest.json'),partial_metered_cost_usd=str(total)),ensure_ascii=False))
