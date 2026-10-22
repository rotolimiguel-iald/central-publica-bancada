"""One-use integration of completed controls, documentary reviews and terminal failure."""
import sys
sys.dont_write_bytecode = True
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from audit_inputs import file_info, save_json, safe_write

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_TAIL_PASS_NUMERICAL_REVIEW_WSL_PATH_FAILURE_20261006 -->'

def check(entry, parent=None):
    p = Path(entry['path'])
    if not p.is_absolute():
        p = parent / p
    actual = file_info(p)
    assert all(actual[k] == entry[k] for k in ('bytes', 'sha256')), str(p)
    return actual

def manifest(rel):
    p = ROOT / rel
    d = json.loads(p.read_bytes())
    entries = d.get('files', d.get('artifacts'))
    return file_info(p), [check(e, p.parent) for e in entries]

def main():
    out = ROOT / 'RECIBO_MEMORIA_TAIL_NUMERICO_WSL.json'
    assert not out.exists()
    now = datetime.now(timezone.utc).isoformat()
    tail_path = ROOT / 'RECIBO_ROOT_CONTROLES_TAIL_V2_PASS.json'
    wsl_path = ROOT / 'RECIBO_ROOT_WSL_TERMINAL_FAILED_PATH.json'
    tail = json.loads(tail_path.read_bytes())
    wsl = json.loads(wsl_path.read_bytes())
    assert tail['status'] == 'EIGHT_PRIMARY_AND_NINE_NEGATIVE_SYNTHETIC_GROUPS_PASSED_ONCE'
    assert tail['parent_exit_code_observed_by_exec_tool'] == 0
    assert wsl['status'] == 'TERMINAL_FAILED_LINUX_SCRIPT_PATH_NO_CONTROL_QUALIFICATION'
    assert wsl['external_exit_code'] != 0
    evidence = [check(e) for e in tail['evidence'] + wsl['evidence']]
    pins = {'tail_result': file_info(tail_path), 'WSL_failure': file_info(wsl_path)}
    packages = {
        'tail_review': 'derivacoes/revisao_tail_implementation_v2/MANIFESTO_REVISAO_DELTA_V2.json',
        'MM_review': 'derivacoes/revisao_mm_model/MANIFESTO_REVISAO_MM.json',
        'numerical_delivery': 'f9_numerical_certification_preparation/MANIFESTO_ENTREGA.json',
        'numerical_review': 'derivacoes/revisao_certificacao_numerica_f9/MANIFESTO_REVISAO_CERTIFICACAO_NUMERICA_F9.json',
        'WSL_errata': 'preregistros/conjunto_d/errata_revisao_guard_wsl_526/MANIFESTO_ERRATA_526.json',
    }
    for key, rel in packages.items():
        pins[key], verified = manifest(rel)
        evidence.extend(verified)
    sources = json.loads((ROOT / 'f9_numerical_certification_preparation/FONTES_E_REUSO.json').read_bytes())
    evidence.extend(check(e) for e in sources['sources'])
    metadata_path = ROOT / 'ORCHESTRATOR_METADATA_20261006_0638.json'
    metadata = json.loads(metadata_path.read_bytes())
    pins['orchestrator_metadata'] = file_info(metadata_path)
    with sqlite3.connect((BASE / 'state/tasks.sqlite3').as_uri() + '?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        jobs = [dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks = [dict(x) for x in db.execute("SELECT id,status,execution_constraints FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
    path = ROOT / 'SLOT_SNAPSHOT.json'
    old = path.read_bytes(); snapshot = json.loads(old)
    snapshot.update(checked_at=now, nonterminal=jobs, executions=tasks, next_state='needs_attention', next_error='Geração canônica diferente da autorizada no pedido.', effective_limits={'nonterminal_coordination': 5, 'parallel_executions': 3, 'per_provider': 1}, metadata_status=pins['orchestrator_metadata'], dispatch='none; shared memory/source integrity failure; old pin untouched')
    assert path.read_bytes() == old; save_json(path, snapshot)
    path = BASE / 'state/handoffs/slot_management.json'
    old = path.read_bytes(); slots = json.loads(old)
    slots['last_checked_at'] = now
    slots['queue_read_error'].update(at=now, operation='next', receipt='needs_attention', dispatch='none')
    slots['ordem018_F9_MM_model_preparation_request'].update(status='RESPONDED_DOCUMENTARY_REVIEW_ACCEPTED_NOT_RATIFIED', independent_review=pins['MM_review'], review_seq=513)
    slots['ordem018_F9_numerical_certification_request'].update(status='RESPONDED_DOCUMENTARY_DELIVERY_AND_INDEPENDENT_REVIEW_ACCEPTED', response_manifest=pins['numerical_delivery'], independent_review=pins['numerical_review'], review_seq=525)
    slots['ordem018_tail_controls_result'] = {'request_id': tail['request_id'], 'status': tail['status'], 'receipt': pins['tail_result'], 'map_seq': 524, 'repeat_allowed': False}
    slots['ordem018_WSL_guard_control_result'] = {'request_id': wsl['request_id'], 'status': wsl['status'], 'receipt': pins['WSL_failure'], 'errata': pins['WSL_errata'], 'map_seq': 528, 'errata_seq': 529, 'repeat_allowed': False}
    slots['provider_eligibility_observation'] = {'at': now, 'receipt': pins['orchestrator_metadata'], 'canonical_memory': metadata['canonical_memory'], 'sources_ok': metadata['sources']['ok'], 'ready_is_not_dispatch_eligibility': True, 'manager_informed': True}
    slots['ordem018_discriminante_slot_request']['latest_check'] = {'at': now, 'queue_state': 'needs_attention', 'nonterminal': len(jobs), 'active_executions': len(tasks), 'new_provider_calls': 0, 'no_repeat_request': True, 'snapshot': file_info(ROOT / 'SLOT_SNAPSHOT.json'), 'useful_work': 'Tail synthetic controls completed; numerical documentary review accepted; WSL unit terminal failure preserved; concrete local backend-selection request pending.'}
    assert path.read_bytes() == old; save_json(path, slots)
    note = f'''{MARK}
## 06/10/2026 UTC — Envelope sintético aprovado; contrato numérico revisto; falha WSL preservada

[REAL — mapas518/524] A correção do envelope F9 recebeu revisão independente e a unidade {tail['request_id']} executou uma única vez oito grupos primários e nove negativos:17 PASS, exit0 externo,158 pins revalidados. A ferramenta mediu {tail['exec_command_wall_s']}s; o tempo até persistência foi {tail['wall_through_terminal_persistence_s']}s e o dos controles {tail['worker_controls_wall_s']}s. Recibo {pins['tail_result']['path']} SHA256 {pins['tail_result']['sha256']}. A lista inteira da família e as falhas de finalização são tratadas; recibo provisório sozinho não significa sucesso. São controles sintéticos, sem certificado físico, mínimo global ou veredito observado; captura tem teto de aceitação após coleta e prazo nominal, não garantia dura do SO.

[REAL documental; DERIVED condicional — mapas513/520/525] Aceitas as revisões documentais do modelo MM e do contrato numérico F9. Este conserva limites L_i≤g_i≤U_i sobre o prior completo, dual com Xᵀv=0 exato, quociente completo de dimensão r−63, normalização relativa κA_s e células desconhecidas com contribuição [0,w], nunca likelihood zero. Estimativas não viram certificados; concordância entre duas precisões CAMB não é erro uniforme. Backend/oráculo/certificados efetivos e adoção do experimento continuam OPEN. Dez controles NC são somente plano, não executados. Manifesto numérico SHA256 {pins['numerical_delivery']['sha256']}; revisão SHA256 {pins['numerical_review']['sha256']}. MM não foi ratificado por esta integração.

[REAL — mapas528/529; ERRATA ao aceite526] A unidade WSL {wsl['request_id']} foi consumida uma vez e falhou antes de abrir linux_control.py. common.py construiu um Path dependente do Windows e enviou barras invertidas no argv Linux; principal/helper retornaram2 e a saída externa foi {wsl['external_exit_code']}. Não houve qualificação do guard, journal ou controle WSL. O recibo original UNCERTAIN_ORPHAN_STATE permanece; uma inspeção posterior somente de leitura não encontrou processos do mesmo UID com request/nonce exatos naquele instante, sem sinal e sem repetir controle. Isso não é ausência absoluta do SO. Recibo SHA256 {pins['WSL_failure']['sha256']}; errata SHA256 {pins['WSL_errata']['sha256']}. Pacotes/claims consumidos intactos; nenhuma correção ou nova execução autorizada. Alternativas documentais são construção explícita de argv POSIX ou serialização as_posix. INIT003 continua terminal não qualificado e D fechado.

[REAL operacional] Next novamente needs_attention por geração canônica distinta; não é idle. Estado local: {len(jobs)} coordenação antiga não terminal, {len(tasks)} execuções queued/running, limites5/3/1. Metadata oficial relata memória comum indisponível e fonte operacional sem correspondência; labels ready não constituem capacidade elegível. Nenhum repin, substituição ou chamada remota/Work. Gerente informada e recebeu a unidade local documental bf2a5692-1aff-423e-9345-7bfa256d5072 para selecionar backend e propor a menor unidade útil; resposta pendente sem cobrança duplicada. Pedido enviado conserva seus bytes; estado de envio fica em recibo separado/ledger. Nenhum V1 final adotado, abertura observada, kernel, gate ou original científico alterado. A recusa automática anterior do download adicional SBF permanece sem contorno; o trabalho documental usou os pins locais admitidos.'''
    targets = [MEM / 'TGL_ATLAS.md', MEM / 'TGL_INDICE_VIVO.md', MEM / 'TGL_CORE_MEMORY.md', ROOT / 'ENTREGA_018_F1_HUBBLE.md', ROOT / 'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']
    originals = {p: p.read_bytes() for p in targets}
    assert all(MARK.encode() not in b for b in originals.values())
    changes = []
    for p, old in originals.items():
        assert p.read_bytes() == old
        safe_write(p, old + ('\r\n\r\n' + note.replace('\n', '\r\n') + '\r\n').encode())
        assert p.stat().st_size > len(old)
        changes.append({'before_bytes': len(old), 'after': file_info(p)})
    path = ROOT / 'CONTINUIDADE.json'
    old = path.read_bytes(); value = json.loads(old)
    value.update(updated_at=now, tail_envelope_status='SEVENTEEN_SYNTHETIC_GROUPS_PASS_ONCE_NO_PHYSICAL_CERTIFICATION', tail_controls_receipt=pins['tail_result'], MM_model_status='DOCUMENTARY_REVIEW_ACCEPTED_NOT_RATIFIED', numerical_certificate_status='DOCUMENTARY_INTERFACE_REVIEW_ACCEPTED_BACKEND_SELECTION_PENDING', numerical_review=pins['numerical_review'], WSL_guard_status='TERMINAL_FAILED_PATH_BEFORE_SCRIPT_NO_RETRY', WSL_guard_receipt=pins['WSL_failure'], WSL_errata=pins['WSL_errata'])
    value['milestone_sequences'] = sorted(set(value.get('milestone_sequences', []) + [513, 518, 520, 524, 525, 526, 527, 528, 529]))
    value['phases']['F1'] = 'CONSOLIDATED_DRAFT; SYNTHETIC_TAIL_PASS; MM_AND_NUMERICAL_DOCUMENTARY_REVIEWS_ACCEPTED; OBSERVED_COMPOSITE_CLOSED'
    value['phases']['F3'] = 'INIT003_TERMINAL_UNQUALIFIED; THREE_WINDOWS_STDLIB_CONTROLS_PASS; WSL_SINGLE_UNIT_TERMINAL_FAILED_PATH; D_CLOSED'
    value['next_steps'] = ['Receive pending local backend-selection unit without duplicate solicitation.', 'Keep WSL4f5d terminal; any new control requires a separate concrete decision, never replay/rename.', 'Prepare remaining F1/F3 prerequisites without observed opening; operator section6 remains in force.']
    assert path.read_bytes() == old; save_json(path, value); changes.append({'after': file_info(path)})
    save_json(out, {'at': now, 'marker': MARK, 'pins': pins, 'verified_evidence': evidence, 'changes': changes, 'policy': 'Exact-byte same-folder backup, verified temporary write, atomic replace, compare-before-write; no sealed original edited.'})
    path = ROOT / 'MANIFESTO_CONSOLIDACAO_PARCIAL.json'
    old = path.read_bytes(); value = json.loads(old); previous = file_info(path)
    paths = {Path(e['path']) for e in value['files']}
    paths.update([out, Path(__file__).resolve(), tail_path, wsl_path, ROOT / 'SLOT_SNAPSHOT.json', metadata_path, ROOT / 'authorize_tail_v2_controls.py', ROOT / 'record_tail_v2_result.py', ROOT / 'F9_BACKEND_SELECTION_REQUEST.json', ROOT / 'F9_BACKEND_SELECTION_DISPATCH_RECEIPT.json'])
    for folder in ['f9_tail_envelope_implementation_v2', 'derivacoes/revisao_tail_implementation_v2', 'derivacoes/revisao_mm_model', 'f9_numerical_certification_preparation', 'derivacoes/revisao_certificacao_numerica_f9', 'preregistros/conjunto_d/guard_wsl_integration_preparation', 'preregistros/conjunto_d/guard_wsl_integration_preparation_v2', 'preregistros/conjunto_d/revisao_guard_wsl_estatica', 'preregistros/conjunto_d/revisao_guard_wsl_v2', 'preregistros/conjunto_d/errata_revisao_guard_wsl_526']:
        paths.update(p for p in (ROOT / folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp_' not in p.name and '__pycache__' not in p.parts)
    assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in paths)
    value.update(updated_at=now, previous_snapshot=previous, status='PARTIAL_TAIL_SYNTHETIC_PASS_NUMERICAL_REVIEW_WSL_TERMINAL_FAILURE_NO_DATA_OPENING', files=[file_info(p) for p in sorted(paths, key=lambda p: str(p).casefold())])
    assert path.read_bytes() == old; save_json(path, value)
    print(json.dumps({'receipt': file_info(out), 'manifest': file_info(path), 'files': len(value['files']), 'nonterminal': len(jobs), 'active_executions': len(tasks)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
