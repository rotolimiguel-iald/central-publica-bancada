from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
B = HERE/'B_fechamentos'
OUT = ROOT.parent/'TUNEL/DO_CHATGPT'
spec = importlib.util.spec_from_file_location('audit', ROOT/'A0/auditar_axiomas.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, value):
    raw = value if isinstance(value, bytes) else (value.encode('utf-8') if isinstance(value, str)
        else json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(raw)
    assert tmp.read_bytes()==raw and raw
    tmp.replace(p)

finals = [
    ('B3a', 'QubitScalarEntropy.lean', 'qubit_scalar_01'),
    ('B3b', 'QubitEntropyDerivative_v3.lean', 'qubit_derivative_03'),
    ('B3d', 'IdempotentDephasing_v2.lean', 'idempotent_exp_02'),
    ('B1b', 'FiniteGapRate_v2.lean', 'finite_gap_02')]
attempt_labels = ['qubit_scalar_01', 'qubit_derivative_01','qubit_derivative_02','qubit_derivative_03',
                  'idempotent_exp_01','idempotent_exp_02','finite_gap_01','finite_gap_02']
results=[]
for branch, file, label in finals:
    source=B/file;log=B/(label+'.log');receipt=json.loads((B/(label+'.json')).read_bytes())
    assert receipt['rc']==0 and receipt['source_sha256']==sha(source) and receipt['log_sha256']==sha(log)
    assert not receipt['newer_kernel_files'] and not receipt['scan_errors']
    result=audit.audita(str(source),str(log));assert result['auditoria']=='PASSA', result
    save(B/(label+'_audit.json'),result)
    results.append(dict(branch=branch,source=str(source),source_sha256=sha(source),
        log_sha256=sha(log),receipt=receipt,audit=result))
attempts=[]
for label in attempt_labels:
    p=B/(label+'.json');r=json.loads(p.read_bytes())
    assert sha(B/(label+'.log'))==r['log_sha256']
    attempts.append(dict(label=label,receipt_sha256=sha(p),**r))
opening=OUT/'ENTREGA_016_ABERTURA_operador.md'
now=datetime.now(timezone.utc)
wall=sum(r['wall_seconds'] for r in attempts)
cpu=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in attempts)
first=min(datetime.fromisoformat(r['utc']) for r in attempts)
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes()
events=[json.loads(line) for line in old.decode('utf-8-sig').splitlines() if line.strip()]
costs={}
for e in events:
    c=e.get('cost_estimate_usd', e.get('cost_usd', e.get('custo_usd')))
    if c is not None:
        key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
        if key: costs[key]=Decimal(str(c))
cost=sum(costs.values(),Decimal(0))
manifest=dict(status='REAL_SCOPED_COMPILED_AND_AUDITED',at=now.isoformat(),
    opening_sha256=sha(opening),finals=results,attempts=attempts,
    wall_seconds=wall,cpu_seconds=cpu,
    recorded_bench_window_seconds=(now-first).total_seconds(),
    recorded_bench_window_scope='First compile through audit; excludes preparation before first compile and is not exclusive work time',
    source_count=len(finals),new_theorem_count=sum(r['audit']['n_theorem_lemma_na_fonte'] for r in results),
    reported_external_estimates_usd=str(cost),external_accounting_complete=False,
    gate_changed=False,kernel_written=False,
    packaging='Companion modules; original V3 prefix unchanged in the previously audited base. Monolithic integration pending.')
save(B/'entropy_and_gap_manifest_v2.json',manifest)
lines=['[REAL — provas Lean compiladas e auditadas no escopo dos enunciados]', '',
    '# A6 — entropia escalar, exponencial idempotente e taxa espectral', '',
    'Abertura do operador, SHA256: `'+sha(opening)+'`.', '', 'Correção ao lado: substitui a entrega anterior apenas no somatório de custos. O agregador anterior omitia o campo legado cost_usd; as provas e seus recibos permanecem idênticos. Predecessor SHA256: `'+sha(OUT/'ENTREGA_016_A6_B_entropia_e_taxa.md')+'`.', '',
    '| Alvo | Estado | Resultado | Teoremas novos |', '|---|---|---|---:|',
    '| B3a | PAGO | Raio em [0,1), antitonia; entropia crescente; déficit não negativo e decrescente | 14 |',
    '| B3b | PAGO sob r>0 | Derivada exata da entropia escalar | 4 |',
    '| B3d | PAGO | Exponencial de idempotente em álgebra de Banach completa | 2 |',
    '| B1b | PAGO sob gap | Decaimento em norma com constante 1 por Parseval | 3 |', '',
    'B3a usa p∈(0,1), k=|c|²≥0, k<p(1−p), s≥0. Foram provados '
    'r(s)=√((2p−1)²+4ke^(−2s)), S(s)=binEntropy((1+r(s))/2) e '
    'D(s)=binEntropy(p)−S(s)≥0. S é estritamente crescente quando k>0. '
    'A igualdade desse escalar com −Tr(ρ log ρ) pertence ao harness matricial D, ainda pendente.', '',
    'B3b: S′(s)=(2ke^(−2s)/r(s)) log((1+r(s))/(1−r(s))). '
    'O caso r=0 não foi incluído nessa fórmula dividida por r; a monotonicidade B3a o inclui.', '',
    'B3d: para e²=e, exp(−s(1−e))=e+exp(−s)(1−e). '
    'É identidade algébrica para s real; idempotência sozinha não garante que e seja canal '
    'completamente positivo, não fixa taxa física nem seleciona um vácuo único.', '',
    'B1b: ||T_s x−Px||≤exp(−sγ)||x−Px||, s≥0, γ>0, em dimensão finita. '
    'A hipótese do gap se refere exatamente aos autovalores de H: cada um é zero ou ≥γ. '
    'Ela já implica não negatividade espectral; não foi acrescentada uma segunda hipótese redundante '
    'de positividade. Não se afirma igualdade de norma de operador nem existência de modo que atinja γ. '
    'Núcleo total e dimensão zero permanecem admitidos.', '',
    f'Auditoria: {manifest["new_theorem_count"]} teoremas novos, quatro fontes finais, cobertura integral; '
    'todos os axiomas contidos no trio. Nenhum sorry/axiom novo nas fontes finais. '
    'Oito tentativas no total: B3a 1; B3b 3; B3d 2; B1b 2. Falhas preservadas.', '',
    f'Custo de máquina: {wall:.6f}s parede somados, {cpu:.6f}s CPU; '
    f'janela registrada de bancada {manifest["recorded_bench_window_seconds"]/3600:.6f}h '
    '(não exclusiva; começa na primeira compilação). Estimativas externas explícitas deduplicadas: '
    f'US${cost}; incompletas, não equivalem à fatura. Nenhuma chamada externa nova nesta implementação.', '',
    'Não move o gate. Permanece a MEDIDA de empacotamento: provas em módulos companheiros, '
    'prefixo V3 da base preservado, monólito final ainda não integrado. A etapa seguinte é B1d '
    '(limite forte em dimensão infinita), seguida dos controles C e do harness D.', '',
    'Manifesto de fontes, logs, comandos, hashes e tempos: '+str(B/'entropy_and_gap_manifest_v2.json'), '']
save(OUT/'ENTREGA_016_A6_B_entropia_e_taxa_v2.md','\n'.join(lines))
marker='A6_ENTROPY_AND_GAP_ACCOUNTING_CORRECTED_20260924'
if marker.encode() not in old:
    e=dict(event=marker,at=now.isoformat(),opening_sha256=sha(opening),
        manifest=str(B/'entropy_and_gap_manifest_v2.json'),manifest_sha256=sha(B/'entropy_and_gap_manifest_v2.json'),
        wall_seconds=wall,cpu_seconds=cpu,external_execution=False,gate_changed=False)
    save(ledger,old+(b'' if old.endswith(b'\n') else b'\n')+json.dumps(e,ensure_ascii=False).encode()+b'\n')
progress=OUT/'ENTREGA_016_PROGRESSO.md';raw=progress.read_bytes()
if marker.encode() not in raw:
    line=(f'\n- {now.isoformat()} — A6.B3a/B3b/B3d/B1b PAGO no escopo: 23 teoremas novos auditados, '
        f'8 tentativas; máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU. Janela registrada '
        f'de bancada {manifest["recorded_bench_window_seconds"]/3600:.6f}h, não exclusiva. '
        f'Estimativas US${cost}, incompletas. Abertura {sha(opening)}. '
        f'Não move gate; monólito pendente; próximo B1d. [{marker}]\n')
    save(progress,raw+line.encode('utf-8'))
print(json.dumps(dict(theorems=manifest['new_theorem_count'],wall_seconds=wall,cpu_seconds=cpu,
                     estimated_costs=str(cost),audit='PASSA'),ensure_ascii=False))
