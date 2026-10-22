from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, sys

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'TUNEL/DO_CHATGPT'
sys.path.insert(0, str(HERE.parent / 'A0'))
from auditar_axiomas import audita

now = datetime.now(timezone.utc)
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, data):
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp)
        with backup.open('xb') as f: f.write(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + '.tmp_' + stamp)
    with temp.open('xb') as f: f.write(data)
    assert data and temp.read_bytes() == data
    temp.replace(p)

opening = sha(OUT / 'ENTREGA_016_ABERTURA_operador.md')
units = [('UnitMultiplierIdentity.lean', 'unit_multiplier_01'),
         ('OrbitalMeasureSupport_v2.lean', 'orbital_support_02'),
         ('OrbitalTranslationOperators_v2.lean', 'orbital_translation_02')]
proofs = []
for name, label in units:
    source, log = HERE / name, HERE / (label + '.log')
    receipt = json.loads((HERE / (label + '.json')).read_text(encoding='utf8'))
    audit = audita(str(source), str(log))
    assert receipt['rc'] == 0 and not receipt['newer_kernel_files'] and not receipt['scan_errors']
    assert receipt['source_sha256'] == sha(source) and receipt['log_sha256'] == sha(log)
    assert audit['auditoria'] == 'PASSA', audit
    proofs.append(dict(source=str(source), source_sha256=sha(source), log_sha256=sha(log),
                       receipt_sha256=sha(HERE/(label+'.json')), receipt=receipt, audit=audit))
attempts = []
for label in ['unit_multiplier_01', 'orbital_support_01', 'orbital_support_02',
              'orbital_translation_01', 'orbital_translation_02']:
    path = HERE/(label+'.json')
    receipt = json.loads(path.read_text(encoding='utf8'))
    attempts.append(dict(label=label, sha256=sha(path), rc=receipt['rc'],
                         wall_seconds=receipt['wall_seconds'],
                         cpu_seconds=receipt['cpu_user_seconds']+receipt['cpu_kernel_seconds'],
                         utc=receipt['utc']))
dependencies = []
for name, label in [('OrbitTranslationFaithfulness_v2.lean', 'orbit_faithful_02'),
                    ('OrbitalRapidityMeasure_v4.lean', 'orbital_measure_04'),
                    ('RapidityJacobian_v2.lean', 'rapidity_jacobian_02')]:
    source = HERE/name
    receipt = json.loads((HERE/(label+'.json')).read_text(encoding='utf8'))
    assert receipt['rc'] == 0 and receipt['source_sha256'] == sha(source)
    dependencies.append(dict(path=str(source), sha256=sha(source), receipt_sha256=sha(HERE/(label+'.json'))))

# Deduplicate actual ledger estimates; do not turn unmetered failures into zero cost.
prices, unknown = {}, set()
for line in (OUT/'LEDGER_016.jsonl').read_text(encoding='utf8').splitlines():
    item = json.loads(line)
    key = item.get('job_id') or item.get('request_id')
    if not key: continue
    price = item.get('cost_estimate_usd', item.get('custo_usd'))
    if price is not None:
        try: prices[key] = Decimal(str(price)); unknown.discard(key)
        except Exception: pass
    elif item.get('desfecho') == 'failed' or 'UNMETERED' in str(item):
        prices.pop(key, None); unknown.add(key)
uncertain_job = 'bcacca23-9116-4043-8b69-ac7264009303'
prices.pop(uncertain_job, None); unknown.add(uncertain_job)
cost = dict(known_explicit_estimates_usd=str(sum(prices.values(), Decimal(0))),
            unknown_jobs=sorted(unknown), scope='NOT_INVOICE_NOT_COMPLETE_TOTAL')
n = sum(p['audit']['n_declaracoes_auditadas'] for p in proofs)
wall = sum(a['wall_seconds'] for a in attempts)
cpu = sum(a['cpu_seconds'] for a in attempts)
elapsed = (now - min(datetime.fromisoformat(a['utc']) for a in attempts)).total_seconds()
manifest = dict(status='REAL', utc=now.isoformat(), opening_sha256=opening,
    declarations=n, proofs=proofs, dependencies=dependencies, attempts=attempts,
    machine_wall_seconds=wall, machine_cpu_seconds=cpu,
    elapsed_since_first_compile_seconds=elapsed, cost=cost,
    statement='For every m>=0 and nontrivial complex normed fiber E, orbitalTranslation m is injective on R^4.',
    scope='Actual weighted mass-shell L2 translation operators; not a completed Poincare/helicity/BW representation.',
    pending=['physical helicity cocycle realization', 'positive energy analytic form',
             'boostMat covariance bridge', 'BW and Fock construction'])
save(HERE/'translation_operator_faithfulness_manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode())
report = f'''[REAL — fidelidade das translações como operadores L², compilada e auditada]

# ORDEM 016 — A3.1: do caráter pontual ao operador

UTC {now.isoformat()}; ABERTURA sha256 `{opening}`.

**PAGO no escopo de A3.1:** para todo m≥0 e toda fibra complexa normada
não trivial E, `orbitalTranslation m` é injetiva em ℝ⁴. Em particular,
U(a)=I implica a=0. A construção cobre m=0, m>0 e a fibra ℂ×ℂ
com o mesmo caráter de translação nas duas componentes.

**Cadeia efetivamente ligada:**

1. `unitMultiplier` constrói o operador pela multiplicação de Hölder L∞×L²,
reutilizando o padrão de `ContinuousModularMultipliers`. Preserva a norma.
2. Indicadores de uma cobertura enumerável por conjuntos de medida finita
provam que agir como identidade sobre todo L² força o multiplicador a ser
1 quase em toda parte. O argumento vale para qualquer fibra não trivial.
3. A densidade orbital é positiva quase em toda parte. A medida ponderada
tem suporte pleno e é sigma-finita, inclusive para m=0. Continuidade leva
a igualdade a.e. à igualdade pontual; não se extrai valor de um eixo nulo.
4. `shellMomentum_covers_shell` cobre a órbita de energia positiva.
Os sete lemas pontuais já compilados são reutilizados, sem nova prova
paralela. `orbitalTranslation_faithful` e `orbitalTranslation_injective`
fecham a passagem. Soma, identidade, inversa e equivalência isométrica
complexa foram construídas para os operadores reais em L²(d³p/p₀;E).

**Verificação:** {n} declarações auditadas em três arquivos finais;
rc0, cobertura completa de `#print axioms`, somente o trio permitido,
nenhuma admissão e nenhum arquivo novo/modificado no kernel durante as
compilações. {len(attempts)} tentativas preservadas, no máximo duas por módulo.
As duas correções foram de elaboração Lean: igualdade de conjuntos no
lema de medida nula e coerções na composição da equivalência isométrica.
Máquina: {wall:.6f}s parede, {cpu:.6f}s CPU. Intervalo desde a primeira
compilação desta entrega: {elapsed/3600:.6f}h (não é o total histórico do ramo).

**Custódia:** fontes, logs, comandos, dependências e hashes calculados em
`A3/translation_operator_faithfulness_manifest.json`. A entrega anterior
de espectro permanece intacta; esta nota resolve sua pendência de
fidelidade L². Original `um.py`, kernel e gate não foram alterados.

**Limite:** o resultado da fibra dupla fecha as translações desse setor.
Não identifica automaticamente o boost componente a componente com a
representação física do fóton. Construção das helicidades, forma analítica
de energia positiva, ligação com `boostMat`, BW e Fock continuam separadas.
Próximo ramo: completar a medição condicionada das helicidades e avançar
nos subalvos 2–3 do ramo principal, preservando a árvore da ordem.

Sem nova chamada externa nesta rodada. Estimativas explícitas deduplicadas:
US$ {cost['known_explicit_estimates_usd']}; {len(unknown)} jobs sem custo
informado. Não é total faturado. Kimi/MiMo já registrados continuam sob
a autorização específica de envio solicitada pela coordenadora; não
houve repetição nem alteração do payload para contornar a revisão.
'''
save(OUT/'ENTREGA_016_A3_1_fidelidade_operadores_L2.md', report.encode())
p = OUT/'ENTREGA_016_PROGRESSO.md'
save(p, p.read_bytes()+f'\n{now.isoformat()} | A3.1 PAGO no escopo de translações L²: +{n} declarações; m=0/m>0/fibra dupla. U(a)=I implica a=0 por indicadores, suporte pleno e lemas pontuais existentes. Máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU; intervalo desde primeira compilação {elapsed/3600:.6f}h. Custo conhecido {cost["known_explicit_estimates_usd"]} USD, desconhecidos preservados. Sem chamadas novas; H2/Poincaré/helicidades completas ainda não pagos.\n'.encode())
print(json.dumps(dict(status='PASSA', declarations=n, wall_seconds=wall, cpu_seconds=cpu, cost=cost), ensure_ascii=False))
