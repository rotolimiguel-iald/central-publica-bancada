"""Reserve the existing controller8h cap, keeping the total authorized sum."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,copy
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import save,write,sha
def main():
    from t03_terminal_guard import require_terminal
    terminal=require_terminal(D)
    measured=D/'nulls_campaign_001/RESULT.json';r=json.loads(measured.read_bytes())
    old=B/'ORCAMENTO_015_v1.json';v=json.loads(old.read_bytes());regpath=B/'RINGDOWN_5SIGMA_V1_1_2.json';reg=json.loads(regpath.read_bytes())
    assert not (B/'ORCAMENTO_015_v2.json').exists()
    cfg=reg['pe_jobs']['GW250114_PILOT_V2_S220'];cap=cfg['wall_budget_seconds']/3600;assert cap==8
    items={x['item']:x for x in v['items']};delta=cap-items['T04_pilot_220']['allocated_machine_hours'];assert delta==4
    items['T04_pilot_220']['allocated_machine_hours']=cap
    items['T10_calibration']['allocated_machine_hours']-=delta
    items['T03_nulls_IV_and_t5'].update(actual_machine_hours=r['machine_hours_union'],job_started=True,
        final_receipt_sha256=sha(measured),status=r['status'])
    assert r['machine_hours_union']<=items['T03_nulls_IV_and_t5']['allocated_machine_hours']
    total=sum(x['allocated_machine_hours'] for x in v['items']);assert total==v['allocated_machine_hours']<=v['authorized_machine_hours']
    at=datetime.now(timezone.utc).isoformat();jobs=D/'E2_PE_JOBS_ALLOCATION_015_V2.json'
    sourcejobs=ROOT/v['jobs_relative_to_Chatgpt'];j=json.loads(sourcejobs.read_bytes());assert not j['jobs'] and not j['downloads']
    j.update(parent_registration_sha256=sha(regpath),scope='NO_NEW_JOB_OR_DOWNLOAD;controller8h and all scientificparameters unchanged')
    save(jobs,j)
    v.update(registered_utc=at,supersedes_sha256=sha(old),parent_registration_sha256=sha(regpath),
        witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v2.md',
        jobs_relative_to_Chatgpt=jobs.relative_to(ROOT).as_posix(),jobs_sha256=sha(jobs),
        prerequisites_unpaid=['T04_NATIVE_400_QUALIFICATION','T04_PROCESS_LIFECYCLE_CHECK'],
        T03_terminal=terminal,T03_terminal_guard_sha256=sha(D/'t03_terminal_guard.py'),
        pilot_safety='Existing registered controller hardcap8h now fully reserved; externalwatchdog is additional, not solebudgetcontrol',
        reallocation_reason='INPUT:prudentialreserve toalign existing hardcap;notclaimofmeasuredposteriorruntime. R5 sourcecost remainsidealproxy;returnunusedreserveafterpilot',
        reallocation_changes={'T04_pilot_220':{'old':4.,'new':8.},'T10_calibration':{'old':19.,'new':15.}},
        accounting=dict(rule='UNION_OF_OWNED_HEAVY_JOB_INTERVALS',clock_started=True,simultaneous_process_limit=28,
            intervals=[dict(target='T03_nulls',receipt_relative_to_Chatgpt=measured.relative_to(ROOT).as_posix(),sha256=sha(measured),
                union_machine_hours=r['machine_hours_union'],CPU_seconds=r['child_cpu_seconds'])],
            machine_hours_spent=r['machine_hours_union']))
    p=B/'ORCAMENTO_015_v2.json';save(p,v)
    note=f'''[REAL — alocação registrada; INPUT — reserva prudencial; DERIVED — proxy de custo]

allocation_sha256: {sha(p)}
registered_utc: {at}

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}

Pai do orçamento:{sha(old)}. Registro corrente:{sha(regpath)}. Total{total!r}hde{v['authorized_machine_hours']!r}h, inalterado. Reserva piloto4→8h e T1019→15h. Nenhum job,prior,semente,código científico ou observável mudou. O controllerjá possuía teto8h; ele agora cabe na reserva, mesmo que o supervisor externo termine inesperadamente.

Motivo: crítica T04-F1.8h é reserva prudencial ANTESdopiloto, não custo medido; proxy R5 continua {items['T04_pilot_220']['estimated_wall_hours']:.8f}h, excluindo IPC/amostrador/convergência. Reconciliar e devolver saldo realmente não consumido após o piloto. A realocação não aumenta o teto total nem autoriza gastar saldo duasvezes.

T03 medido: união{r['machine_hours_union']:.9f}h, CPU{r['child_cpu_seconds']:.6f}s; reciboSHA256{sha(measured)}. Demais itens sem gastos novos nesta entrega. T09/T16 permanecemsem autorização. Zerochamadasremotasnovas. Gateinalterado.
'''
    write(OUT/'ENTREGA_015_ORCAMENTO_015_v2.md',note.encode())
    save(D/'BUDGET_V2_DELIVERY.json',dict(at=at,allocation_sha256=sha(p),witness_sha256=sha(OUT/'ENTREGA_015_ORCAMENTO_015_v2.md'),
        sum_hours=total,available=v['authorized_machine_hours'],spent=r['machine_hours_union'],controller_hard_cap_hours=cap))
    print(json.dumps(dict(status='BUDGET_V2_WITNESSED',sum_hours=total,pilot_hours=cap,calibration_hours=15.,spent=r['machine_hours_union'])))
if __name__=='__main__':main()
