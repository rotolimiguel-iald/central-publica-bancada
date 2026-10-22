"""One-use memory integration; no scientific execution or transport."""
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
MARK = '<!-- ORDEM018_NC02_TERMINAL_LAYOUT_WSL_DECISION_20261006 -->'

def main():
    output = ROOT / 'RECIBO_MEMORIA_NC02_LAYOUT.json'
    assert not output.exists()
    now = datetime.now(timezone.utc).isoformat()
    names = {
        'nc02': 'RECIBO_ROOT_NC02_TERMINAL_FAILURE.json',
        'backend': 'RECIBO_ROOT_BACKEND_E_PREPARACAO_NC02.json',
        'layout': 'f9_structural_layout_preparation/MANIFESTO_LAYOUT_ESTRUTURAL.json',
        'layout_root': 'RECIBO_ROOT_LAYOUT_ESTRUTURAL.json',
        'wsl_decision': 'WSL_CORRECTED_TRANSPORT_MANAGER_DECISION.json',
        'assembly_request': 'F9_FIVE_MODEL_ASSEMBLY_REQUEST.json',
        'metadata': 'ORCHESTRATOR_METADATA_NC02_ROUND.json',
    }
    pins = {k: file_info(ROOT / name) for k, name in names.items()}
    nc = json.loads((ROOT / names['nc02']).read_bytes())
    assert nc['external_exit_code'] == 1 and nc['repeat_allowed'] is False
    verified = []
    for e in nc['evidence']:
        a = file_info(e['path'])
        assert all(a[k] == e[k] for k in ('bytes', 'sha256'))
        verified.append(a)
    with sqlite3.connect((BASE / 'state/tasks.sqlite3').as_uri() + '?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        jobs = [dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks = [dict(x) for x in db.execute("SELECT id,status FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
    path = ROOT / 'SLOT_SNAPSHOT.json'
    old = path.read_bytes(); snapshot = json.loads(old)
    snapshot.update(checked_at=now, nonterminal=jobs, executions=tasks, next_state='needs_attention', next_error='Geração canônica diferente da autorizada no pedido.', effective_limits={'nonterminal_coordination': 5, 'parallel_executions': 3, 'per_provider': 1, 'other_providers_exclusive_lane': True}, metadata_status=pins['metadata'], dispatch='none; source/common memory failure, no repin or fallback')
    assert path.read_bytes() == old; save_json(path, snapshot)
    path = BASE / 'state/handoffs/slot_management.json'
    old = path.read_bytes(); ledger = json.loads(old)
    ledger['last_checked_at'] = now
    ledger['effective_limits_verified'] = {'at': now, 'coordination': 5, 'executions': 3, 'per_parallel_provider': 1, 'parallel_providers': ['kimi','mimo','deepseek'], 'other_providers_exclusive': True, 'sources': [file_info(BASE / 'iald_orchestrator/coordination.py'), file_info(BASE / 'iald_orchestrator/runtime.py')]}
    ledger['ordem018_NC02_preparation'].update(status=nc['status'], root_receipt=pins['nc02'], execution_consumed_once=True, retry_allowed=False)
    ledger['ordem018_F9_five_model_assembly_request'].update(structural_layout_delivered=pins['layout'], structural_delivery_channel='official send_message_to_thread', status='IMPLEMENTATION_IN_PROGRESS_STRUCTURAL_LAYOUT_DELIVERED')
    ledger['ordem018_WSL_corrected_transport_decision'].update(status='MANAGER_AUTHORIZED_PREPARATION_IN_PROGRESS_REVIEW_BEFORE_SINGLE_LAUNCH', decision_receipt=pins['wsl_decision'])
    ledger['ordem018_discriminante_slot_request']['latest_check'] = {'at': now, 'queue_state': 'needs_attention', 'nonterminal': len(jobs), 'active_executions': len(tasks), 'new_provider_calls': 0, 'no_repeat_request': True, 'useful_work': 'Five-model F9 assembly active with structural layout delivered; new WSL preparation specifically authorized; NC02 terminal failure under static diagnosis.'}
    assert path.read_bytes() == old; save_json(path, ledger)
    note = f'''{MARK}
## 06/10/2026 UTC — Preparação F9, layout estrutural e NC02 terminal

[REAL documental — mapas531/534/535/537] A escolha local de backend recebida da gerente foi conferida: Fraction/inteiros para a pequena unidade racional NC02; bibliotecas alternativas ficaram em avaliação documental. A unidade preparada recebeu revisão independente e conferência ROOT de536 pins e14+11 membros. A autorização539 limitou o consumo aos dois casos sintéticos fixos. Não houve abertura de composto observado, cálculo CAMB ou envio remoto.

[REAL — mapa540] NC02 {nc['request_id']} foi consumida uma vez e terminou FAILED_WORKER_OR_RECEIPT, worker/supervisor exit1, erro UNPINNED_IMPORTED_MODULE e audit_denied vazio. Tempo externo {nc['exec_command_wall_s']}s; observação até persistência {nc['wall_through_persistence_s']}s. Nenhum resultado aritmético foi aceito, nenhum PASS foi promovido. O recibo não registra qual módulo faltou: identidade não inferida. Diagnóstico por leitura está em curso; pacote/CLAIM permanecem intactos, sem repetição. Recibo {pins['nc02']['path']} SHA256 {pins['nc02']['sha256']}.

[REAL documental — mapa542] Foi entregue à gerente o layout ordenado3CMB+13BAO, unidades/redshifts e origem de ALPHA_FINE_CODATA_2018 no código já pinado. O último par BAO em2.33 é DH depois DM; *_over_rs histórico usa rdrag, enquanto CMB usa rstar. z_lei fixo permanece separado de zstar/zdrag térmicos dependentes dos parâmetros. β só em runtime. Bytes completos do catálogo DESI foram lidos para hash, com projeção restrita a rótulos/redshifts, sem capturar/decodificar/converter coluna central. Manifesto SHA256 {pins['layout']['sha256']}. A montagem pura das cinco hipóteses segue no pedido8e017d91-f3bb-4ec6-9236-5b2c327d1b98, sem cobrança duplicada. O contrato numérico admite estimativas ENGINEERING_ONLY com limitações explícitas: ausência de cota uniforme CAMB limita certificação, não impede implementar análise.

[INPUT — decisão oficial2ea, mapa541; REAL pins] A gerente autorizou preparação de pacote NOVO WSL stdlib corrigido, com nova raiz/identidade, representação PurePosixPath e comparação argv; execução única somente depois de pins, revisão independente de integração/delta e autorização ROOT específica. Até este registro há preparação, não execução. Limite nominal60s, um primário, no máximo um cleanup e um filho; preservar STOP/gate/pidfd/journal. Unidade4f5d terminal/intacta, sem rerun. Falha/incerteza da nova unidade também impede repetição. Decisão SHA256 {pins['wsl_decision']['sha256']}. Nenhum D/PE/LAL/solver/controle científico autorizado por essa decisão técnica.

[REAL operacional] Fila needs_attention, não idle: geração canônica difere do pedido antigo. Consulta local: {len(jobs)} coordenação não terminal, {len(tasks)} execução queued/running. Limites efetivos5coordenações/3execuções/1por provedor paralelo; demais provedores usam lane exclusiva. Memória comum indisponível/fonte operacional divergente, sem repin/substituição/chamada remota/Work. Gerente informada; tarefas locais concretas continuam. F1/F3 abertas e F4 não pronta; §6 da ORDEM018 conserva a decisão de abertura observada com o operador. Nenhum kernel, gate ou original científico alterado.'''
    targets = [MEM / n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]
    targets += [ROOT / 'ENTREGA_018_F1_HUBBLE.md', ROOT / 'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']
    originals = {p:p.read_bytes() for p in targets}
    assert all(MARK.encode() not in raw for raw in originals.values())
    changes=[]
    for p, raw in originals.items():
        assert p.read_bytes() == raw
        safe_write(p, raw + ('\r\n\r\n' + note.replace('\n','\r\n') + '\r\n').encode())
        assert p.stat().st_size > len(raw)
        changes.append({'before_bytes':len(raw),'after':file_info(p)})
    path = ROOT / 'CONTINUIDADE.json'
    old=path.read_bytes(); value=json.loads(old)
    value.update(updated_at=now, NC02_status=nc['status'], NC02_receipt=pins['nc02'], structural_layout=pins['layout'], five_model_assembly_status='IN_PROGRESS_WITH_LAYOUT_SUPPLIED', WSL_new_unit_status='PREPARATION_AUTHORIZED_PENDING_INDEPENDENT_REVIEW', WSL_manager_decision=pins['wsl_decision'])
    value['milestone_sequences']=sorted(set(value.get('milestone_sequences',[])+[531,533,534,535,536,537,538,539,540,541,542]))
    value['phases']['F1']='FIVE_MODEL_IMPLEMENTATION_IN_PROGRESS; LAYOUT_DELIVERED; NC02_TERMINAL_UNQUALIFIED; OBSERVED_COMPOSITE_CLOSED'
    value['phases']['F3']='INIT003_AND_4f5d_TERMINAL_UNQUALIFIED; NEW_STDLIB_WSL_PREPARATION_AUTHORIZED; D_CLOSED'
    value['next_steps']=['Review concrete five-model assembly after delivery; do not replace implementation with toy-control campaigns.', 'Review new WSL corrected package and authorize only its concrete scoped unit; preserve old terminal units.', 'Complete NC02 static diagnosis without retry or observed-data opening.']
    assert path.read_bytes()==old;save_json(path,value);changes.append({'after':file_info(path)})
    save_json(output,{'at':now,'marker':MARK,'pins':pins,'verified_execution_evidence':verified,'changes':changes,'policy':'Exact-byte backup, verified temporary, atomic replace, compare before write.'})
    path=ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json';old=path.read_bytes();value=json.loads(old);previous=file_info(path)
    paths={Path(e['path']) for e in value['files']}
    paths.update(ROOT/n for n in names.values());paths.update([output,Path(__file__).resolve(),ROOT/'RECIBO_ROOT_NC02_PRE_EXECUCAO.json',ROOT/'F9_FIVE_MODEL_ASSEMBLY_DISPATCH_RECEIPT.json',ROOT/'WSL_CORRECTED_TRANSPORT_DECISION_REQUEST.json',ROOT/'WSL_CORRECTED_TRANSPORT_DECISION_DISPATCH_RECEIPT.json'])
    for folder in ['f9_backend_selection_preparation','f9_nc02_rational_preparation','proveniencia/revisao_nc02_rational','f9_structural_layout_preparation','preregistros/conjunto_d/guard_wsl_path_repair_preparation','preregistros/conjunto_d/revisao_guard_wsl_path_candidate']:
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp_' not in p.name and '__pycache__' not in p.parts)
    assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in paths)
    value.update(updated_at=now,previous_snapshot=previous,status='PARTIAL_FIVE_MODEL_IMPLEMENTATION_NC02_TERMINAL_LAYOUT_READY_WSL_PREPARATION',files=[file_info(p) for p in sorted(paths,key=lambda p:str(p).casefold())])
    assert path.read_bytes()==old;save_json(path,value)
    print(json.dumps({'receipt':file_info(output),'manifest':file_info(path),'files':len(value['files'])},ensure_ascii=False))

if __name__ == '__main__':
    main()
