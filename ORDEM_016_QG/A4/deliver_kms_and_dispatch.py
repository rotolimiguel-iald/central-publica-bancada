from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT.parent / 'TUNEL/DO_CHATGPT'
BASE = ROOT.parent / 'IALD_ORQUESTRACAO_20260923'
DEST = HERE / 'orchestration_reviews_20260924'
sys.path.insert(0, str(ROOT/'A0'))
from auditar_axiomas import audita
sys.path.insert(0, str(BASE))
from iald_orchestrator.coordination import Coordination

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, data):
    raw = data if isinstance(data, bytes) else data.encode('utf-8')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        old = path.read_bytes()
        bak = path.with_name(path.name+'.bak_'+stamp)
        with bak.open('xb') as stream:
            stream.write(old)
        assert bak.read_bytes() == old
    tmp = path.with_name(path.name+'.tmp_'+stamp)
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert raw and tmp.read_bytes() == raw
    tmp.replace(path)

def dump(path, value):
    save(path, json.dumps(value, ensure_ascii=False, indent=2))

opening = OUT/'ENTREGA_016_ABERTURA_operador.md'
source, log = HERE/'KMSStripConditional.lean', HERE/'kms_strip_01.log'
audit = audita(str(source), str(log))
receipt_path = HERE/'kms_strip_01.json'
receipt = json.loads(receipt_path.read_bytes())
assert audit['auditoria'] == 'PASSA'
assert receipt['rc'] == 0 and receipt['newer_kernel_files'] == [] and receipt['scan_errors'] == []
assert receipt['source_sha256'] == sha(source) and receipt['log_sha256'] == sha(log)
assert receipt['opening_sha256'] == sha(opening)
reuse = json.loads((HERE/'kms_rescale_reuse.json').read_bytes())
assert sha(Path(reuse['source'])) == reuse['source_sha256']
original_lines = Path(reuse['source']).read_text(encoding='utf-8-sig').splitlines()
original = '\n'.join(original_lines[reuse['start_line']-1:reuse['end_line']])
current = source.read_text(encoding='utf-8').split('theorem kms_rescale_existing', 1)[1]
current = current.split('/-- Conditional bridge:', 1)[0]
old_body = original.split(':= by', 1)[1].strip()
new_body = current.split(':= by', 1)[1].strip()
assert old_body == new_body, 'Reuse body differs; inspect, do not claim unchanged'
at = datetime.now(timezone.utc).isoformat()
dump(HERE/'kms_strip_manifest.json', dict(at=at, status='REAL_COMPILED_CONDITIONAL',
    source=str(source), source_sha256=sha(source), log=str(log), log_sha256=sha(log),
    receipt=receipt, receipt_sha256=sha(receipt_path), audit=audit,
    reused_body_exact=True, reuse= reuse, opening_sha256=sha(opening),
    remaining_named_hypotheses=['H_regional_modular_strip','H_modular_equals_geometric']))

coordination = Coordination()
jobs = []
ids = ['6cdeb9a0-20f7-45af-8b96-4bf5bb35c8f2',
       'f8ec22e7-21c2-4bf4-b3bc-29655e681481',
       'cc64f514-586e-48c9-b6bb-e3b963d16bff',
       '63b4e640-2b1a-4f7e-8213-76b2eb94d3e5',
       'a947924d-70c2-4191-97f2-d845f56420ee']
first_receipt = json.loads((DEST/'kimi_kms_strip_scope_receipt.json').read_bytes())
ids.append(first_receipt['job_id'])
for job_id in ids:
    job = coordination.get(job_id)
    execution = job.get('execution') or {}
    constraints = job.get('execution_constraints') or {}
    jobs.append(dict(job_id=job_id, request_id=job['request_id'], stage=job['stage'],
        provider=constraints.get('required_provider'), lemma_id=constraints.get('lemma_id'),
        execution_id=job.get('execution_task_id'), execution_status=execution.get('status'),
        has_persisted_result=bool(execution.get('result'))))
prepared = json.loads((DEST/'prepared_units.json').read_bytes())
dump(DEST/'dispatch_snapshot.json', dict(at=at,jobs=jobs,prepared=prepared,
    local_queue_capacity=5, delegated_registration_to='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    note='Polar registration rejected locally at capacity; MiMo A4 not submitted here. '
         'Coordinator instructed to use same UUIDs when slots become available; this is a dated snapshot.'))

report = ['[REAL — distribuição e compilação local; respostas de provedores ainda não são prova]',
    '', '# ORDEM 016 — reforço A4 para Kimi/MiMo', '', f'Data UTC: {at}.',
    f'Abertura sha256: `{sha(opening)}`.', '',
    'Foram preparadas três unidades novas, distintas das A3: Kimi cético da faixa KMS; '
    'Kimi cético do alcance geométrico do quociente polar; MiMo da álgebra das dez leituras. '
    'As três prévias selecionaram o executor exigido. Memória comum pelo transporte; '
    'uma chamada por unidade, sem substituição automática.', '',
    f'Kimi KMS registrado: `{first_receipt["job_id"]}`. A segunda submissão foi recusada '
    'antes de chamada remota porque havia cinco coordenações pendentes. A terceira '
    'não foi submetida nesta rodada. A coordenação oficial recebeu os payloads e a ordem '
    'de registrá-los com os mesmos UUIDs quando abrir vaga; não se ampliou nem se contornou a fila.', '',
    '| Provedor | Unidade | request_id |', '|---|---|---|']
for unit in prepared:
    report.append(f'| {unit["provider"]} | {unit["slug"]} | {unit["request_id"]} |')
report += ['', '## Estado observado da fila', '', '| job_id | Estado | Execução |', '|---|---|---|']
for job in jobs:
    report.append(f'| {job["job_id"]} | {job["stage"]} | {job["execution_status"]} |')
report += ['', 'A falha MiMo anterior IncompleteRead foi preservada sem repetição. '
    'Não há recibo de consumo final para essa tentativa; custo não confirmado, nunca zero presumido.', '',
    '## Prova local que acompanha a revisão', '',
    'KMSStripConditional.lean: 3 declarações auditadas, rc0, somente '
    'propext/Classical.choice/Quot.sound. O corpo de kms_rescale_existing foi comparado '
    'textualmente ao insumo: reutilizado sem alteração. As duas composições novas provam '
    'a reescala de uma faixa KMS modular já assumida para rapidez 2π e tempo de Killing 2π/κ.', '',
    '**Não se produziu o estado/rede regional.** H_regional_modular_strip e '
    'H_modular_equals_geometric permanecem hipóteses explícitas. Nenhum gate alterado.', '',
    f'Fonte SHA256: `{sha(source)}`.', f'Log SHA256: `{sha(log)}`.',
    f'Tempo de máquina: {receipt["wall_seconds"]:.3f}s parede; '
    f'{receipt["cpu_user_seconds"]+receipt["cpu_kernel_seconds"]:.3f}s CPU.', '',
    f'Manifesto: `{HERE / "kms_strip_manifest.json"}`.',
    f'Custódia da distribuição: `{DEST / "dispatch_snapshot.json"}`.', '']
save(OUT/'ENTREGA_016_ORQUESTRACAO_reforco_A4_Kimi_MiMo.md', '\n'.join(report))
progress = OUT/'ENTREGA_016_PROGRESSO.md'
old = progress.read_bytes()
marker = 'A4_KMS_CONDITIONAL_AND_REVIEW_DISPATCH_20260924'
if marker.encode() not in old:
    line = (f'\n- {at} — A-4k.4 MEDIDA parcial: ponte condicional KMS compilada '
            f'(3 declarações, rc0/trio, {receipt["wall_seconds"]/3600:.6f} h máquina). '
            'Faixa modular regional e BW ainda hipóteses; bancada desta subentrega não '
            'cronometrada integralmente. Duas revisões Kimi e uma MiMo preparadas: uma '
            'registrada, duas entregues à coordenação para vaga. Não move gate. '
            f'[{marker}]\n')
    save(progress, old+line.encode('utf-8'))
print(json.dumps(dict(audit=audit['auditoria'], declarations=audit['n_declaracoes_auditadas'],
    reused_body_exact=True, jobs=jobs,report=str(OUT/'ENTREGA_016_ORQUESTRACAO_reforco_A4_Kimi_MiMo.md')),
    ensure_ascii=False))
