"""Record the consumed F9 unit and existing queue state; never run science."""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from audit_inputs import file_info, safe_write, save_json

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_F9_FFD6_IMPORT_FAILURE_20261006 -->'

def main():
    out = ROOT/'RECIBO_MEMORIA_F9_IMPORT_FAILURE.json'
    assert not out.exists()
    stamp = datetime.now(timezone.utc).isoformat()
    receipt = ROOT/'RECIBO_ROOT_F9_ENGINE_TERMINAL_FAILURE.json'
    result = json.loads(receipt.read_bytes())
    assert result['status']=='FAILED_TERMINAL_CLEANED_NOT_SCIENTIFIC_RESULT'
    assert result['solver_calls_attempted']==result['solver_calls_returned']==0
    pin = file_info(receipt)
    with sqlite3.connect((BASE/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row
        jobs=[dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks=[dict(x) for x in db.execute("SELECT id,status FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
    path=ROOT/'SLOT_SNAPSHOT.json';old=path.read_bytes();value=json.loads(old)
    value.update(checked_at=stamp,nonterminal=jobs,executions=tasks,next_state='needs_attention',next_error='Geração canônica diferente da autorizada no pedido.',metadata_status=file_info(ROOT/'ORCHESTRATOR_METADATA_F9_FAILED_ROUND.json'),dispatch='No remote dispatch, repin or duplicate service request. Local F9 terminal diagnosis and pure consumer preparation pending.')
    assert path.read_bytes()==old;save_json(path,value)
    path=BASE/'state/handoffs/slot_management.json';old=path.read_bytes();ledger=json.loads(old)
    ledger['last_checked_at']=stamp
    ledger['effective_limits_verified']={'at':stamp,'coordination':5,'executions':3,'per_parallel_provider':1,'parallel_providers':['kimi','mimo','deepseek'],'other_providers_exclusive':True,'sources':[file_info(BASE/'iald_orchestrator/coordination.py'),file_info(BASE/'iald_orchestrator/runtime.py')]}
    ledger['ordem018_F9_engine_assembly_integration_request'].update(status='PREPARATION_DELIVERED_EXECUTION_FAILED_TERMINAL_CLEANED',execution_request_id=result['request_id'],execution_consumed_once=True,retry_allowed=False,root_result=pin,math_review_sequence=553,runtime_review_sequence=555,root_authorization_sequence=556,result_sequence=557,manager_response='Official sister task acknowledged receipt/hash and terminal status; no edit/retry; await assigned read-only diagnosis.',review_dependency='Static reviews accepted; actual import failure demonstrated incomplete import closure. No scientific result accepted.')
    ledger['ordem018_F9_engine_terminal_diagnosis']={'status':'DELEGATED_READ_ONLY','agent':'/root/ordem018_proveniencia','source_result':pin,'allowed':'Read/AST/metadata only; separate diagnosis folder; no import, WSL process, solver, changed consumed package or new authorization.'}
    ledger['ordem018_discriminante_slot_request']['latest_check']={'at':stamp,'queue_state':'needs_attention','nonterminal':len(jobs),'active_executions':len(tasks),'new_provider_calls':0,'no_repeat_request':True,'useful_work':'Pure likelihood consumer a987 and read-only diagnosis of consumed ffd6 already assigned. Manager acknowledged terminal failure; no duplicate demand.'}
    assert path.read_bytes()==old;save_json(path,ledger)
    note=f'''{MARK}
## 06/10/2026 UTC — Integração F9 consumida, falha de importação antes do solver

[REAL — mapas553/555/556/557] A integração entregue f07e teve revisões matemática e operacional independentes, conferência ROOT de34membros e autorização específica para uma avaliação teórica. A unidade ffd6ccba-cd70-4747-aceb-a10003dfb7f4 foi consumida uma vez e terminou FAILED_TERMINAL_CLEANED: ferramenta externa exit{result['external_tool']['exit_code']}, wall{result['external_tool']['wall_time_seconds']}s. CASE FAILED_LATCHED durante importação CAMB→SciPy→special._ufuncs; solver tentado0/retornado0. Três eventos físicos bloquearam /usr/lib/python312.zip e charset_normalizer/__pycache__/__init__.cpython-312.pyc + charset_normalizer/__init__.py. A cadeia exata será objeto do diagnóstico dirigido; integridade do inventário não demonstrou completude dos imports. Nenhum resultado científico foi aceito; arquivos de saída preabertos vazios não são resultados.

[REAL — custódia] ROOT conferiu igualdade dos streams físicos com CASE/LINUX/CLEANUP, journal com os três eventos, identidade/autorização,24membros preservados, stderr vazio e captura sem erro/overflow com EOF/leitores encerrados. Filho recolhido exit1; cleanup exit0 sem identidades controladas vivas no instante inspecionado, STOP persistido. Recibo {pin['path']} SHA256 {pin['sha256']}. Unidade, autorização e claims permanecem terminais; nenhuma repetição ou substituição automática. As revisões553/555 ficam limitadas pelo resultado real, sem apagamento de história.

[OPEN — continuidade] Proveniência recebeu diagnóstico somente leitura/AST/metadados, sem executar/importar candidatos, alterar pacote consumido ou criar autorização. A gerente recebeu o recibo e confirmou oficialmente hash/estatuto terminal; aguarda o diagnóstico sem duplicar trabalho. O consumidor puro de likelihood a987 segue em preparação separada usando o backend existente, sem dados observados. Nenhuma revisão virou V1, certificado numérico, evidência ou confirmação física. F1/F3 abertas, F4 não pronta; §6 conserva abertura observada com o operador. D/PE, kernel, gate e originais científicos intactos.

[REAL — fila] next falhou com geração canônica distinta e foi registrado needs_attention, não idle. Há{len(jobs)}coordenação não terminal e{len(tasks)}execução queued/running. Código efetivo conserva5coordenações/3execuções/1por provedor paralelo; demais lane exclusiva. Memória comum indisponível e fonte operacional divergente, ready não é elegibilidade. Sem chamada remota/Work, repin, executor substituído ou cobrança duplicada enquanto consumidor/diagnóstico concretos estão pendentes.'''
    targets=[MEM/name for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md']]+[ROOT/'ENTREGA_018_F1_HUBBLE.md',ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']
    originals={p:p.read_bytes() for p in targets};changes=[]
    assert all(MARK.encode() not in raw for raw in originals.values())
    for p,raw in originals.items():
        assert p.read_bytes()==raw
        safe_write(p,raw+('\r\n\r\n'+note.replace('\n','\r\n')+'\r\n').encode())
        assert p.stat().st_size>len(raw)
        changes.append({'before_bytes':len(raw),'after':file_info(p)})
    path=ROOT/'CONTINUIDADE.json';old=path.read_bytes();value=json.loads(old)
    value.update(updated_at=stamp,F9_engine_assembly_status='CONSUMED_FAILED_IMPORT_NO_SOLVER_NO_RETRY',F9_engine_assembly_result=pin,F9_likelihood_consumer_status='PREPARATION_IN_PROGRESS_NO_OBSERVED_DATA')
    value['milestone_sequences']=sorted(set(value.get('milestone_sequences',[])+[553,555,556,557]))
    value['phases']['F1']='ENGINE_ASSEMBLY_FFD6_TERMINAL_IMPORT_FAILURE; ZERO_SOLVER_CALLS; PURE_LIKELIHOOD_CONSUMER_PREPARATION_PENDING; OBSERVED_COMPOSITE_CLOSED'
    value['next_steps']=['Receive directed read-only diagnosis of ffd6 import dependency omission; no automatic retry or new authorization.', 'Review concrete pure likelihood consumer a987 using existing Gaussian backend, without observed data.', 'Continue original ORDEM018 mission within existing scientific and data-opening restrictions; no duplicated provider requests.']
    assert path.read_bytes()==old;save_json(path,value);changes.append({'after':file_info(path)})
    save_json(out,{'at':stamp,'marker':MARK,'root_result':pin,'changes':changes,'slots':file_info(ROOT/'SLOT_SNAPSHOT.json'),'ledger':file_info(BASE/'state/handoffs/slot_management.json'),'backup_policy':'Exact-byte same-directory backup, verified temporary, atomic replace, compare-before-write.'})
    path=ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json';old=path.read_bytes();value=json.loads(old);previous=file_info(path)
    paths={Path(e['path']) for e in value['files']}
    paths.update([out,receipt,Path(__file__).resolve(),ROOT/'F9_ENGINE_EXECUTION_TOOL_RECEIPT.json',ROOT/'ORCHESTRATOR_METADATA_F9_FAILED_ROUND.json',ROOT/'RECIBO_ROOT_ENTREGA_INTEGRACAO_F9.json',ROOT/'F9_LIKELIHOOD_CONSUMER_PREPARATION_REQUEST.json',ROOT/'verify_f9_engine_result.py'])
    for folder in ['f9_engine_assembly_integration_preparation','derivacoes/revisao_f9_engine_assembly','proveniencia/revisao_f9_engine_assembly']:
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name and '__pycache__' not in p.parts)
    assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in paths)
    value.update(updated_at=stamp,previous_snapshot=previous,status='PARTIAL_F9_ENGINE_TERMINAL_IMPORT_FAILURE_NO_SOLVER_CONSUMER_PREPARATION_PENDING',files=[file_info(p) for p in sorted(paths,key=lambda p:str(p).casefold())])
    assert path.read_bytes()==old;save_json(path,value)
    print(json.dumps({'receipt':file_info(out),'manifest':file_info(path),'files':len(value['files']),'nonterminal':len(jobs),'executions':len(tasks)}))

if __name__=='__main__':
    main()
