"""Persist the ongoing owned execution without claiming its result."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;R=ROOT/'ORDEM_016_QG';OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import write,save,sha
at=datetime.now(timezone.utc).isoformat()
clock=B/'bis/PART_015_BUDGET_START.json';run=D/'nulls_campaign_001'
started=[json.loads(p.read_bytes()) for p in run.glob('*_PROCESS.json')]
finished=[json.loads(p.read_bytes()) for p in run.glob('*_FINISH.json')]
record=dict(at=at,status='RUNNING' if not (run/'RESULT.json').exists() else 'FINISHED_REQUIRES_REVIEW',
    exec_session_id=64813,script_sha256=sha(D/'run_nulls_registered_v1.py'),clock_sha256=sha(clock),
    started_cells=len(started),finished_cells=len(finished),result=str(run/'RESULT.json'),
    maximum_machine_hours=1,do_not_restart=True,gate_changed=False,
    next_action='Review existing T03 result; record actual union hours and tails, then T04 qualification400 and pilot',
    T04_prepared=str(D/'t04/supervise_t04.py'),T04_script_sha256=sha(D/'t04/supervise_t04.py'),
    coordination_review='REQUESTED_LOCAL_NOT_RECEIVED;coordinator currently occupied by another operator request',
    operational_errata='One inline read-only process inspection failed shell quoting/SyntaxError; replaced by inspect_null_processes.py, six owned processes verified1thread each; no scientific rerun')
save(D/'NULLS_ACTIVE_CHECKPOINT.json',record)
cp=R/'A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
state.update(at=at,next='PART_B_T03_POLL_64813_NO_RESTART_THEN_T04',next_action='PART_B_T03_POLL_64813_NO_RESTART_THEN_T04',
    active_process=record,continuation_rule='Do not duplicate existing run; its external supervisor enforces1h and cleans own children. Keep partial package immutable. Check management receipts first.')
save(cp,state,True)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n{at} | B/R7 e T03 | EM EXECUÇÃO: {len(started)} células iniciadas, {len(finished)} concluídas; sessão64813 | teto1h, custo final ainda não medido | relógio SHA256 {sha(clock)}; T04 preparado, não executado\n'.encode(),True)
print(json.dumps(record))
