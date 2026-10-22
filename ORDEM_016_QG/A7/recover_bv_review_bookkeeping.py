"""Resume only bookkeeping after a same-timestamp backup collision; no provider retry."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

def main():
    now=datetime.now(timezone.utc);D=H/'bv_review_and_volume_delivery'
    old_manifest=D/'manifest.json'
    for a in json.loads(old_manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
    ledger=OUT/'LEDGER_016.jsonl';events=[json.loads(v) for v in ledger.read_text('utf-8').splitlines()]
    exid='b6d6658a-0dfe-41e3-aa05-1d413874b348'
    charged=[e for e in events if e.get('execution_task_id')==exid and e.get('cost_estimate_usd') is not None]
    assert len(charged)==1,charged
    ds=dict(at=now.isoformat(),event='BILOCAL_WICK_REVIEW_DISPATCH_CONFIRMED',target='A7.b',provider='deepseek',
        request_id='cd6a1a0d-d671-4e6a-888a-e9c1ba6ea703',job_id='e3aa9cba-3f1f-4c0c-b7df-1a0838ac30f3',
        execution_task_id='18b266db-d2f1-4ef8-a253-73f9b8f2c896',worker_session=93618,
        payload_sha256=sha(H/'orchestration_bilocal_wick_transport/deepseek_bilocal_wick_transport_submit.json'),
        status='RUNNING_CONFIRMED_BY_COORDINATOR',observed_at='2026-09-25T17:56:39Z',cost_estimate_usd=None)
    assert not any(e.get('event')==ds['event'] and e.get('execution_task_id')==ds['execution_task_id'] for e in events)
    # Single append avoids the helper's per-process timestamp collision.
    recovery=dict(at=now.isoformat(),event='BOOKKEEPING_RECOVERY_AFTER_BACKUP_COLLISION',target='A7.b',
        failed_command='python deliver_mimo_bv_review_and_volume.py',returncode=1,
        reason='Second ledger append reused the same backup timestamp; assertion stopped before mutation',
        mathematical_checks_failed=False,duplicate_provider_call=False,mimo_cost_already_recorded_once=True)
    append(ledger,json.dumps(ds,ensure_ascii=False)+'\n'+json.dumps(recovery,ensure_ascii=False)+'\n')
    cost=Decimal(0);seen=set()
    for e in events:
        val=e.get('cost_estimate_usd',e.get('cost_usd'))
        if val is None:continue
        key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
        if key and key in seen:continue
        if key:seen.add(key)
        cost+=Decimal(str(val))
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    put(D/'BOOKKEEPING_RECOVERY.json',dict(**recovery,known_partial_cost_usd=str(cost),predecessor_sha256=sha(old_manifest)))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: MiMo57e auditado4controles novos; primitiva quadrática20controles registrada separadamente. DeepSeekcd6 RUNNING confirmado. Recuperação do registro após colisão de nome de backup, sem repetir auditoria ou provedor. Custo conhecido parcialUSD{cost}; Q2 completa OPEN. AberturaSHA256={opening}.\n')
    p=H/'CONTINUIDADE.json';st=json.loads(p.read_bytes())
    st.setdefault('head_history',[]).append({k:st.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    st.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'MiMo57e reviewed; coordinate bridge accepted, explanatory Lie-square error corrected',
        'Explicit quadratic volume primitive and inhomogeneous WZ checked,20controls',
        'DeepSeekcd6 distinct bilocal transport/extension review dispatched by coordinator',
        'Bookkeeping backup collision recovered without repeated provider cost or call'],
        next=['Derive extension commutator plus composite Euler contact in the actual T2 prescription',
              'Receive DeepSeekcd6 and authorized Kimi reviews without retries',
              'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
        pending_orchestration='MiMo57e complete/audited; DeepSeekcd6 running worker93618; Kimi3 awaiting actual quota',
        partial_metered_cost_usd=str(cost))
    st['bv_review_volume_update']=dict(manifest=str(D/'manifest_v2.json'),full_Q2=False)
    st['latest_verified_orchestration']['mimo_new']['status']='COMPLETED_RECEIVED_AUDITED'
    st['bilocal_review_execution']=ds
    put(p,st,True)
    put(D/'manifest_v2.json',dict(at=now.isoformat(),supersedes=str(old_manifest),predecessor_sha256=sha(old_manifest),
        artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),old_manifest,D/'BOOKKEEPING_RECOVERY.json']],
        bookkeeping_complete=True,new_provider_call=False,full_Q2=False,gate_changed=False))
    write(OUT/'ENTREGA_016_MEDIDA_MiMo_BV_e_primitiva_quadratica_RECIBO.md',
        f'[REAL — recuperação do registro, sem repetir cálculo ou chamada]\n\nA entrega científica e seu manifesto já estavam íntegros. O segundo append no ledger recusou reutilizar o nome do backup e parou antes da escrita. O recibo MiMo ficou contabilizado exatamente uma vez; despacho DeepSeek e continuidade agora registrados. Manifesto recuperado: {D/"manifest_v2.json"}. Custo conhecido parcial USD{cost}. AberturaSHA256={opening}.\n'.encode('utf-8'))
    print(json.dumps(dict(recovered=True,manifest=str(D/'manifest_v2.json'),known_partial_cost_usd=str(cost)),ensure_ascii=False))

if __name__=='__main__':main()
