"""Publish actual T04 qualification and conservative disjoint interval costs."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,math
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;R=ROOT/'ORDEM_016_QG';OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha

def main():
    qp=D/'t04/qualify/RESULT.json';q=json.loads(qp.read_bytes())
    fp=D/'t04/process_lifecycle_fixture_001/RESULT.json';f=json.loads(fp.read_bytes())
    postp=D/'post_nulls_001/RESULT.json';post=json.loads(postp.read_bytes())
    np=D/'nulls_campaign_001/SUMMARY.json';n=json.loads(np.read_bytes())
    op=D/'t04/qualify/OVERFLOW.json';o=json.loads(op.read_bytes())
    assert post['status']=='T04_READY_FOR_MANUAL_RECEIPT_REVIEW_BEFORE_PILOT'
    assert post['qualification_sha256']==sha(qp)
    assert q['status']=='T04_ADAPTER_400_QUALIFIED' and q['finite']==q['returned']==400 and q['returncode']==0
    calls=[json.loads(line) for line in (D/'t04/qualify/CALLS.jsonl').read_text().splitlines()]
    assert len(calls)==801 and calls[-1]['source_calls']==400 and calls[-1]['edom']==0
    assert o['status']=='OVERFLOW_REJECTED_BEFORE_NATIVE_BACKEND' and o['native_calls']==0
    assert f['status']=='POOL24_LIFECYCLE_OBSERVED' and f['cleanup_confirmed'] and f['returncode']==0
    budget=B/'ORCAMENTO_015_v2.json';a=json.loads(budget.read_bytes())
    assert q['allocation_sha256']==sha(budget)
    step_seconds=sum(s['wall_seconds'] for s in post['steps'] if s['stage'] in ('supervise_t04_v3','process_lifecycle_fixture'))
    assert step_seconds/3600<=next(x['allocated_machine_hours'] for x in a['items'] if x['item']=='T04_runner_qualification')
    spent=n['machine_hours']+step_seconds/3600
    receipt=dict(at=datetime.now(timezone.utc).isoformat(),status='T04_QUALIFICATION_MEASURED_PILOT_NOT_YET_LAUNCHED',
        calls=400,finite=400,EDOM=0,native_abort=0,overflow_negative=o,
        qualification_wall_seconds=q['wall_seconds'],qualification_cpu_seconds=q['children_cpu_seconds'],
        fixture_wall_seconds=f['wall_seconds'],fixture_cpu_seconds=f['children_cpu_seconds'],
        fixture_peak_processes=f['peak_observed_processes_including_supervisor'],
        fixture_total_including_continuation_parent=f['peak_observed_processes_including_supervisor']+1,
        process_scope='Observed fixture and conditional topology, not OS-enforced maximum',
        accounted_T04_qualification_hours=step_seconds/3600,
        accounting='Disjoint T03union plus conservative outerwall of fixture andqualification; parent wait not added',
        machine_hours_spent=spent,authorized_machine_hours=a['authorized_machine_hours'],
        remaining_machine_hours=a['authorized_machine_hours']-spent,
        unpaid_T03=dict(completed_cells=n['completed'],registered_cells=n['registered'],physical_sigma=None),
        files={str(p):sha(p) for p in (qp,fp,postp,np,op,budget,D/'t04/qualify/CALLS.jsonl')},
        next_job='GW250114_PILOT_V2_S220',next_supervisor='t04/supervise_t04_v3.py pilot',
        new_external_calls=0,gate_changed=False)
    save(D/'t04/QUALIFICATION_DELIVERY.json',receipt)
    note=f'''[REAL — NÃO-CEGO; qualificação nativa e controle operacional, sem posterior ou detecção]

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Data: {receipt['at']}

400/400formas finitas, 0EDOM, 0aborto; pareamento PRECALL/RETURN exato. Fonte4096Hz, amostragem interna8192Hz e banda20–1024Hz conforme jobregistrado. Controleoverflow recusado ANTES do backend(0chamadas nativas nessecontrole). Qualificação: parede{q['wall_seconds']:.6f}s, CPU{q['children_cpu_seconds']:.6f}s. RESULTsha256 {sha(qp)}; CALLSsha256 {sha(D/'t04/qualify/CALLS.jsonl')}; OVERFLOWsha256 {sha(op)}.

Fixture:24workers, pico observado{f['peak_observed_processes_including_supervisor']}na subárvore, +1pai de continuação={receipt['fixture_total_including_continuation_parent']}; limpeza confirmada. Isso mede lifecycle e topologia condicional, não é hardcapdeSO. RESULTsha256 {sha(fp)}. O pai de continuação terminou com rc0 e não lançouPE.

T03 ficouMEDIDA: {n['completed']}/{n['registered']}células concluídas; seis tentativas encerradas no teto e24não iniciadas. Nenhum p ou sigma físico. CustoT03 {n['machine_hours']:.9f}h. São pendências reais, não sucesso por silêncio. Limite sintético não calibrado nesta campanha.

OrçamentoV2 testemunhado e cadeia conferida: SHA256 {sha(budget)}; piloto8h, T1015h, total34,2hsem aumento. Contabilidade conservadora dafixture+qualificação pelo relógio externo={step_seconds:.6f}s. Máquina acumulada={spent:.9f}h de{a['authorized_machine_hours']!r}h; saldo={receipt['remaining_machine_hours']:.9f}h. Espera do controlador não somada novamente.

→ CONTINUE: piloto registradoGW250114_PILOT_V2_S220, mesmo código científico, dados, semente e24workers. Esta entrega antecede o lançamento; aceitação exige posterior e convergência medidos. Recibo completoSHA256 {sha(D/'t04/QUALIFICATION_DELIVERY.json')}. Gateinalterado; nenhuma chamada remota.
'''
    write(OUT/'ENTREGA_015_T04_qualificacao_400.md',note.encode())
    cp=R/'A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    state.update(at=receipt['at'],previous_goal_turn='PROGRESS',active_process=None,
        post_nulls_execution=dict(exec_session_id=96991,status='COMPLETED',returncode=0,result_sha256=sha(postp)),
        T04_qualification_receipt=str(D/'t04/QUALIFICATION_DELIVERY.json'),part_B_machine_hours=spent,
        next='LAUNCH_REGISTERED_PILOT_ONCE_USING_SUPERVISOR_V3',next_action='LAUNCH_REGISTERED_PILOT_ONCE_USING_SUPERVISOR_V3')
    save(cp,state,True)
    progress=OUT/'ENTREGA_016_PROGRESSO.md'
    write(progress,progress.read_bytes()+f"\n{receipt['at']} | B/T04 qualificação |400/400finito;0EDOM;overflowrecusado;Pool24limpo | máquinaacumulada{spent:.9f}h | próximopiloto\n".encode(),True)
    print(json.dumps({k:receipt[k] for k in ('status','calls','EDOM','machine_hours_spent','remaining_machine_hours')}))
if __name__=='__main__':main()
