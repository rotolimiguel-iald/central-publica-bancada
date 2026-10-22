"""One-use local memory integration of existing results, without scientific execution."""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from audit_inputs import file_info, safe_write, save_json

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_WSL_PASS_FIVE_MODEL_STATIC_ACCEPTANCE_20261006 -->'

def main():
    output = ROOT / 'RECIBO_MEMORIA_WSL_E_MONTAGEM.json'
    assert not output.exists()
    now = datetime.now(timezone.utc).isoformat()
    names = {'wsl': 'RECIBO_ROOT_WSL_CORRIGIDO_PASS.json', 'assembly': 'RECIBO_ROOT_REVISAO_FIVE_MODEL_ASSEMBLY.json',
             'integration': 'F9_ENGINE_ASSEMBLY_INTEGRATION_REQUEST.json',
             'delivery': 'WSL_AND_ASSEMBLY_MANAGER_DELIVERY_RECEIPT.json',
             'metadata': 'ORCHESTRATOR_METADATA_WSL_PASS_ROUND.json'}
    pins = {k: file_info(ROOT / n) for k, n in names.items()}
    wsl = json.loads((ROOT / names['wsl']).read_bytes())
    assembly = json.loads((ROOT / names['assembly']).read_bytes())
    assert wsl['status'] == 'PASS_WSL_STDLIB_INTEGRATION_ONCE_VERIFIED_BY_ROOT'
    assert wsl['repeat_allowed'] is False and assembly['status'] == 'LIMITED_STATIC_ACCEPTANCE_NOT_EXECUTION'
    for e in wsl['evidence'] + assembly['review_pins'] + assembly['assembly_pins']:
        actual = file_info(e['path'])
        assert all(actual[k] == e[k] for k in ('bytes','sha256')), e['path']
    with sqlite3.connect((BASE / 'state/tasks.sqlite3').as_uri() + '?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        jobs = [dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks = [dict(x) for x in db.execute("SELECT id,status FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
    path = ROOT / 'SLOT_SNAPSHOT.json'; old = path.read_bytes(); value = json.loads(old)
    value.update(checked_at=now, nonterminal=jobs, executions=tasks, next_state='needs_attention',
                 next_error='Geração canônica diferente da autorizada no pedido.', metadata_status=pins['metadata'],
                 effective_limits={'nonterminal_coordination':5,'parallel_executions':3,'per_provider':1,'other_providers_exclusive_lane':True},
                 dispatch='No remote dispatch; blocked canonical memory/source; existing concrete local preparation f07e pending.')
    assert path.read_bytes() == old; save_json(path, value)
    path = BASE / 'state/handoffs/slot_management.json'; old = path.read_bytes(); ledger = json.loads(old)
    ledger['last_checked_at'] = now
    ledger['effective_limits_verified'] = {'at':now,'coordination':5,'executions':3,'per_parallel_provider':1,'parallel_providers':['kimi','mimo','deepseek'],'other_providers_exclusive':True,
        'sources':[file_info(BASE/'iald_orchestrator/coordination.py'),file_info(BASE/'iald_orchestrator/runtime.py')]}
    ledger['ordem018_WSL_corrected_transport_decision'].update(status=wsl['status'], execution_consumed_once=True, retry_allowed=False, root_result=pins['wsl'], map_sequence=550)
    ledger['ordem018_F9_five_model_assembly_request'].update(status=assembly['status'], root_review=pins['assembly'], independent_review_map=548)
    ledger['ordem018_F9_engine_assembly_integration_request'].update(review_dependency='Assembly548 accepted statically; transport550 qualified only stdlib. Concrete integration/runtime still needs its own review before execution.', upstream_delivery=pins['delivery'])
    ledger['ordem018_discriminante_slot_request']['latest_check'] = {'at':now,'queue_state':'needs_attention','nonterminal':len(jobs),'active_executions':len(tasks),
        'new_provider_calls':0,'no_repeat_request':True,'useful_work':'Existing F9 engine-to-assembly preparation f07e pending; completed WSL550 and static review548 delivered to manager.'}
    assert path.read_bytes() == old; save_json(path, ledger)
    result = wsl['observed_result']
    note = f'''{MARK}
## 06/10/2026 UTC — WSL corrigido concluído e montagem F9 revisada

[REAL — mapas547/549/550] A nova unidade WSL {wsl['request_id']} foi consumida uma vez após revisão independente e autorização específica ROOT. Resultado PASS_WSL_STDLIB_INTEGRATION_ONCE, exit externo0, wall externo{wsl['external_execution']['wall_time_seconds']}s. ROOT conferiu identidade/pins/autorização, argv real de supervisor/filho/cleanup, igualdade entre stdout físico e recibos, EOF e leitores encerrados. O importador absorveu a exceção esperada de cache; o latch permaneceu ativo, callback0 e checkpoints bloqueados. Journal físico e retornos os.write/fsync conferidos. Filho recolhido com exit0; cleanup exit0 sem identidades controladas vivas no instante inspecionado sob gate, STOP persistente. Recibo {pins['wsl']['path']} SHA256 {pins['wsl']['sha256']}. A exibição da ferramenta externa foi truncada; não foi apresentada como captura integral do stdout externo. Os streams internos físicos foram conferidos integralmente.

[LIMITE] Esse PASS rápido qualifica apenas a integração stdlib descrita, não imports científicos, LAL/PE/CAMB, timeout-path, convergência, deadline absoluto do SO ou ausência universal de órfãos. Nenhum dado D ou centro observado foi aberto. Unidade5b67 consumida sem repetição; INIT003,4f5d e NC02c890 continuam terminais em seus estatutos anteriores. A errata543 da NC02 permanece: fechamento de dependências deve ser conferido; módulo dinâmico causador exato continua OPEN.

[REAL documental — entrega545/revisão548] A montagem pura F9 H1–H5 recebeu aceite independente limitado, sem bloqueador novo. ROOT conferiu6membros da entrega e3da revisão, além de ler integralmente o parecer. São283linhas de médias e63colunas nuisance separadas, com7linhas transformadas por fator5 e119respostas Cefeidas. A integração conserva z=0+sete redshifts BAO. O consumidor futuro deve aplicar Ty e TCTᵀ e conferir suporte/normalização; o candidato MM continua condicional e não ratificado. Nada disso é uma execução científica, evidência observada ou certificação numérica. Recibo {pins['assembly']['path']} SHA256 {pins['assembly']['sha256']}.

[REAL operacional; OPEN implementação] Os dois resultados foram enviados à gerente pela ferramenta oficial. O pedido concreto f07e4aba-e976-4d78-be1c-449968d4a305 prepara a integração do motor existente com as cinco médias, em uma futura configuração independente de dados. Está pendente de entrega/revisão; nenhuma execução é autorizada só pela revisão da montagem. A indisponibilidade da cota uniforme limita certificação, sem impedir estimativas ENGINEERING_ONLY. F1/F3 permanecem abertas, F4 não pronta; §6 mantém abertura do composto observado com o operador. Nenhum kernel, gate ou original científico alterado.

[REAL fila] Próximo item retornou erro de geração canônica, registrado needs_attention em2026-10-06T08:10:59.380397+00:00, não idle. Snapshotlocal: {len(jobs)} coordenação não terminal e{len(tasks)} execução queued/running; limites5coordenações/3execuções/1por provedor paralelo, demais em lane exclusiva. Memória comum indisponível e fonte operacional divergente; ready não é capacidade utilizável. Zero chamadas novas a provedores/Work, sem repin, substituição ou cobrança duplicada enquanto f07e está em andamento.'''
    targets = [MEM/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]
    targets += [ROOT/'ENTREGA_018_F1_HUBBLE.md', ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']
    originals = {p:p.read_bytes() for p in targets}
    assert all(MARK.encode() not in raw for raw in originals.values())
    changes=[]
    for p, raw in originals.items():
        assert p.read_bytes() == raw
        safe_write(p, raw + ('\r\n\r\n' + note.replace('\n','\r\n') + '\r\n').encode('utf-8'))
        assert p.stat().st_size > len(raw)
        changes.append({'before_bytes':len(raw),'after':file_info(p)})
    path=ROOT/'CONTINUIDADE.json'; old=path.read_bytes(); value=json.loads(old)
    value.update(updated_at=now, five_model_assembly_status=assembly['status'], five_model_assembly_review=pins['assembly'],
                 WSL_new_unit_status=wsl['status'], WSL_new_unit_receipt=pins['wsl'], F9_engine_assembly_request=pins['integration'], F9_engine_assembly_status='PREPARATION_PENDING_NO_EXECUTION', manager_delivery=pins['delivery'])
    value['milestone_sequences']=sorted(set(value.get('milestone_sequences',[])+[545,547,548,549,550]))
    value['phases']['F1']='FIVE_MODEL_STATIC_ACCEPTANCE; ENGINE_ASSEMBLY_INTEGRATION_PREPARATION_PENDING; NC02_TERMINAL_UNQUALIFIED; OBSERVED_COMPOSITE_CLOSED'
    value['phases']['F3']='WSL_NEW_UNIT_STDLIB_PASS_ONLY; INIT003_AND_4f5d_TERMINAL_UNQUALIFIED; D_CLOSED'
    value['next_steps']=['Receive and independently review concrete engine-to-five-model integration f07e; keep scientific runtime qualification separate from stdlib transport PASS.', 'Continue actual F9 implementation without opening observed composite or replaying consumed controls.', 'Retain NC02 terminal failure and errata543; any future relevant runtime inventory must include transitive origins and failure diagnostics.']
    assert path.read_bytes()==old;save_json(path,value);changes.append({'after':file_info(path)})
    save_json(output,{'at':now,'marker':MARK,'pins':pins,'changes':changes,'slots':file_info(ROOT/'SLOT_SNAPSHOT.json'), 'ledger':file_info(BASE/'state/handoffs/slot_management.json'), 'policy':'Exact-byte backup, verified temporary, atomic replace, compare before write.'})
    path=ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json';old=path.read_bytes();value=json.loads(old);previous=file_info(path)
    paths={Path(e['path']) for e in value['files']}
    paths.update(ROOT/n for n in names.values())
    paths.update([output,Path(__file__).resolve(),ROOT/'verify_wsl_and_assembly_receipts.py',ROOT/'RECIBO_ROOT_PREPARACAO_WSL_CORRIGIDA.json',ROOT/'F9_ENGINE_ASSEMBLY_INTEGRATION_DISPATCH_RECEIPT.json'])
    for folder in ['f9_five_model_assembly_preparation','proveniencia/revisao_five_model_assembly','derivacoes/revisao_wsl_corrected_transport','preregistros/conjunto_d/guard_wsl_corrected_transport_preparation']:
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name and '__pycache__' not in p.parts)
    assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in paths)
    value.update(updated_at=now, previous_snapshot=previous, status='PARTIAL_WSL_STDLIB_PASS_F9_ASSEMBLY_STATIC_ACCEPTANCE_INTEGRATION_PENDING', files=[file_info(p) for p in sorted(paths,key=lambda p:str(p).casefold())])
    assert path.read_bytes()==old;save_json(path,value)
    print(json.dumps({'receipt':file_info(output),'manifest':file_info(path),'files':len(value['files']),'nonterminal':len(jobs),'active_executions':len(tasks)},ensure_ascii=False))

if __name__ == '__main__':
    main()
