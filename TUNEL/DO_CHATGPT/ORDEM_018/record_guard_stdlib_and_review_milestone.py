"""Record consumed guard controls and static findings, without executing either."""
from pathlib import Path
from datetime import datetime, timezone
import json
import sqlite3
from audit_inputs import file_info, save_json, safe_write

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_GUARD_STDLIB_PASS_TAIL_STATIC_FINDINGS_20261006 -->'


def checked(pin, parent=None):
    path = Path(pin['path'])
    if not path.is_absolute():
        assert parent is not None
        path = parent / path
    got = file_info(path)
    assert all(got[key] == pin[key] for key in ('bytes', 'sha256')), str(path)
    return got


def main():
    out = ROOT / 'RECIBO_MEMORIA_GUARD_STDLIB_E_REVISAO_TAIL.json'
    assert not out.exists()
    now = datetime.now(timezone.utc).isoformat()
    guard_path = ROOT / 'RECIBO_ROOT_INTEGRACAO_STDLIB_GUARD_PASS.json'
    guard = json.loads(guard_path.read_bytes())
    assert guard['status'] == 'THREE_REAL_STDLIB_GUARD_CONTROLS_PASSED_ONCE'
    assert guard['parent_exit_code_observed_by_exec_tool'] == 0
    evidence = [checked(pin) for pin in guard['evidence']]
    review_path = ROOT / 'derivacoes/revisao_tail_implementation/MANIFESTO_REVISAO_ESTATICA.json'
    review = json.loads(review_path.read_bytes())
    entries = review.get('artifacts', review.get('files'))
    assert isinstance(entries, list) and entries
    review_evidence = [checked(pin, review_path.parent) for pin in entries]
    pins = {'guard_receipt': file_info(guard_path), 'tail_review': file_info(review_path)}
    mm_folder = ROOT / 'f9_mm_model_preparation'
    mm_path = mm_folder / 'MANIFESTO_ENTREGA.json'
    mm = json.loads(mm_path.read_bytes())
    assert mm['request_id'] == '98a42877-3879-43a7-841c-8bb662be3d06'
    assert mm['science_executed'] is False and mm['remote_model_calls'] == 0
    mm_evidence = [checked(pin, mm_folder) for pin in mm['files']]
    mm_sources = json.loads((mm_folder / 'FONTES_E_FORMULAS.json').read_bytes())
    mm_source_pins = [checked(pin) for pin in mm_sources['sources']]
    pins['MM_manifest'] = file_info(mm_path)
    with sqlite3.connect((BASE / 'state/tasks.sqlite3').as_uri() + '?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        jobs = [dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks = [dict(x) for x in db.execute("SELECT id,status,execution_constraints FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
    snapshot_path = ROOT / 'SLOT_SNAPSHOT.json'
    old = snapshot_path.read_bytes()
    snapshot = json.loads(old)
    snapshot.update(checked_at=now, nonterminal=jobs, executions=tasks, next_state='needs_attention',
                    next_error='Geração canônica diferente da autorizada no pedido.',
                    dispatch='none; old memory pin and failed/uncertain units preserved',
                    effective_limits={'nonterminal_coordination': 5, 'parallel_executions': 3, 'per_provider': 1})
    assert snapshot_path.read_bytes() == old
    save_json(snapshot_path, snapshot)
    slots_path = BASE / 'state/handoffs/slot_management.json'
    old = slots_path.read_bytes()
    slots = json.loads(old)
    slots['last_checked_at'] = now
    slots['queue_read_error'].update(at=now, operation='next', receipt='needs_attention_without_job_id_due_get_validation', dispatch='none')
    slots['ordem018_F9_MM_model_preparation_request'].update(
        status='RESPONDED_DOCUMENTARY_DELIVERY_VERIFIED_INDEPENDENT_REVIEW_PENDING',
        response_received_at=now, response_manifest=pins['MM_manifest'], response_map_seq=511,
        original_request_file_preserved_for_source_pin=True)
    slots['ordem018_discriminante_slot_request']['latest_check'] = {
        'at': now, 'queue_state': 'needs_attention', 'nonterminal': len(jobs), 'active_executions': len(tasks),
        'new_provider_calls': 0, 'no_repeat_request': True, 'snapshot': file_info(snapshot_path),
        'useful_work': 'Windows stdlib controls consumed successfully; WSL preparation and tail correction in progress; MM manager delivery verified, independent review pending.'}
    assert slots_path.read_bytes() == old
    save_json(slots_path, slots)
    note = f'''{MARK}
## 06/10/2026 UTC — Três controles reais do guard no Windows e revisão do envelope

[REAL — mapa509] A unidade {guard['request_id']} executou uma única vez três controles stdlib no Python Windows. Os três passaram, com exit0 observado pela ferramenta e duração externa {guard['exec_command_wall_s']}s. A duração interna {guard['supervisor_wall_before_final_receipt_io_s']}s é anterior ao I/O do recibo final, não o tempo total. Foram conferidos claims, nonces, PIDs, pins, streams e journal físico. I01 registrou duas negativas; I02 confirmou que SourceFileLoader absorve a negativa do cache pyc, mas o latch bloqueia o próximo callback; I03 confirmou latch persistente após EBADF no journal. Nenhum callback posterior à negativa foi executado. Recibo SHA256 {pins['guard_receipt']['sha256']}.

[ESCOPO] São controles operacionais locais com hook real e biblioteca padrão, sem PE, bibliotecas científicas, likelihood, waveform, dados D ou chamadas de modelo. Não qualificam a integração no Python WSL3.12, driver científico ou cobertura nativa; não demonstram contenção de código hostil nem durabilidade sob perda de energia. A preparação de um único controle no importador WSL foi delegada separadamente e ainda não autoriza executá-lo. INIT003 continua terminal não qualificado e nenhuma unidade consumida será repetida.

[REAL estático — mapa510] A revisão independente da implementação candidata do envelope conferiu316 comparações de pins, sem importar/executar o candidato. TI-01: domínio encurtado pode ser aceito sem vínculo com a família completa congelada. TI-02: falta checagem de prazo após I/O terminal. TI-03: communicate limita aceitação de tamanho após coleta, não retenção durante captura. Os dois primeiros bloqueiam consumo da unidade sintética. Correção estática em V2 foi solicitada ao autor, mantendo a mesma identidade não consumida e o snapshot anterior. Manifesto da revisão SHA256 {pins['tail_review']['sha256']}. O cálculo aritmético permanece uma proposta condicional, sem certificado físico, V1 adotado ou veredito observado.

[REAL documental — mapa511] A gerente entregou os cinco termos MM/maser: seis arquivos e doze fontes conferidos contra os pins, sem reabrir catálogos ou interpretar valores centrais. A transformação contém F(v/c), enquanto a receita de propagação upstream usa1/v; a diferença foi registrada simbolicamente, sem troca silenciosa ou impacto numérico alegado. Recomendação A é um experimento gaussiano de trabalho fiel ao upstream, com matriz comum congelada e independência MM proposta como INPUT. Congelamento não demonstra a verdadeira lei condicional. Alternativa B exige primitivas conjuntas, assimetrias e transporte exato; planos MM-P01–P12 não executados. Contrato não ratificado; revisão independente solicitada. Manifesto SHA256 {pins['MM_manifest']['sha256']}.

[REAL operacional] Next voltou a falhar por geração canônica distinta no pedido antigo; registrado needs_attention e não idle. Consulta SQLite somente leitura: {len(jobs)} coordenação não terminal e {len(tasks)} execuções queued/running. Limites5/3/1 conferidos na implementação; nenhum envio, repin, substituição de executor ou nova cobrança à gerente. A entrega MM foi resolvida no ledger como recebida e conferida, com revisão independente pendente. Nenhum kernel, gate, original científico ou automação alterado.'''
    changes = []
    for path in (MEM / 'TGL_ATLAS.md', MEM / 'TGL_INDICE_VIVO.md', MEM / 'TGL_CORE_MEMORY.md',
                 ROOT / 'ENTREGA_018_F1_HUBBLE.md', ROOT / 'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md'):
        old = path.read_bytes()
        assert MARK.encode() not in old
        new = old + ('\r\n\r\n' + note.replace('\n', '\r\n') + '\r\n').encode()
        assert path.read_bytes() == old
        safe_write(path, new)
        assert path.stat().st_size > len(old)
        changes.append({'before_bytes': len(old), 'after': file_info(path)})
    path = ROOT / 'CONTINUIDADE.json'
    old = path.read_bytes()
    value = json.loads(old)
    value.update(updated_at=now, guard_stdlib_controls_status='THREE_PASS_WINDOWS_ONCE_WSL_INTEGRATION_UNQUALIFIED',
                 guard_stdlib_receipt=pins['guard_receipt'], tail_implementation_review=pins['tail_review'],
                 tail_envelope_status='STATIC_REVIEW_TI01_TI02_BLOCK_CONSUMPTION_V2_REPAIR_IN_PROGRESS',
                 MM_model_status='DOCUMENTARY_DELIVERY_VERIFIED_INDEPENDENT_REVIEW_PENDING', MM_manifest=pins['MM_manifest'])
    value['milestone_sequences'] = sorted(set(value.get('milestone_sequences', []) + [509, 510, 511]))
    value['phases']['F1'] = 'CONSOLIDATED_DRAFT; TAIL_V2_REPAIR; MM_SYMBOLIC_CONTRACT_REVIEW_PENDING; OBSERVED_COMPOSITE_CLOSED'
    value['phases']['F3'] = 'INIT003_TERMINAL_UNQUALIFIED; THREE_WINDOWS_STDLIB_CONTROLS_PASS; WSL_SINGLE_CONTROL_PREPARATION; D_CLOSED'
    assert path.read_bytes() == old
    save_json(path, value)
    changes.append({'after': file_info(path)})
    save_json(out, {'at': now, 'marker': MARK, 'pins': pins, 'guard_evidence': evidence,
                    'review_evidence': review_evidence, 'MM_files': mm_evidence, 'MM_sources': mm_source_pins, 'changes': changes,
                    'policy': 'Exact-byte same-folder backups; verified temporary bytes; atomic replace and compare-before-write.'})
    path = ROOT / 'MANIFESTO_CONSOLIDACAO_PARCIAL.json'
    old = path.read_bytes()
    value = json.loads(old)
    previous = file_info(path)
    paths = {Path(x['path']) for x in value['files']}
    paths.update((out, guard_path, snapshot_path, Path(__file__).resolve()))
    for folder in ('preregistros/conjunto_d/guard_stdlib_integration_preparation', 'f9_tail_envelope_implementation', 'derivacoes/revisao_tail_implementation', 'f9_mm_model_preparation'):
        paths.update(p for p in (ROOT / folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '__pycache__' not in p.parts)
    assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in paths)
    value.update(updated_at=now, previous_snapshot=previous,
                 status='PARTIAL_WINDOWS_GUARD_CONTROLS_PASS_TAIL_STATIC_REPAIR_NO_DATA_OPENING',
                 files=[file_info(p) for p in sorted(paths, key=lambda x: str(x).casefold())])
    assert path.read_bytes() == old
    save_json(path, value)
    print(json.dumps({'receipt': file_info(out), 'manifest': file_info(path), 'files': len(value['files']),
                      'nonterminal': len(jobs), 'active_executions': len(tasks)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
