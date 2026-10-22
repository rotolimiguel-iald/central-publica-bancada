"""Register phase-P allocations and provenance; do not start any clock/job."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import write,save,sha
def main():
    source=B/'bis/FINAL_DELIVERY_RECEIPT.json';available=json.loads(source.read_bytes())['remaining_of_40_hours']
    regpath=B/'RINGDOWN_5SIGMA_V1_1_1.json';reg=json.loads(regpath.read_bytes())
    qpath=ROOT/reg['activation_v1_1']['qualification_R5_relative_to_Chatgpt'];q=json.loads(qpath.read_bytes())
    job=reg['pe_jobs']['GW250114_PILOT_V2_S220'];workers=job['sampler']['workers']
    print('SAMPLER',json.dumps(job['sampler']))
    # Cost proxy includes source-generation CPU only, not total sampler runtime.
    ideal=q['cpu_seconds']/q['n_items']*job['sampler']['maxcall']/workers/3600
    order=ROOT/'TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md'
    specs=[('T03_nulls_IV_and_t5',1.,1.,'ORDEM015 T03(v/vi):6 concurrent IV cells plus matched t5; actual duration unmeasured'),
      ('T04_runner_qualification',.2,.2,'ORDEM015 budget envelope; R5 already finite source-only, runner verification still due'),
      ('T04_pilot_220',4.,ideal,'R5 CPU/items x maxcall /24 workers; ideal source-only proxy, excludes sampler/IPC and convergence'),
      ('T07_gate_v3_rho',2.,2.,'ORDEM015 budget envelope'),('T08_selection',2.,2.,'ORDEM015 budget envelope'),
      ('T09_440_free',0.,3.3,'ORDEM015 R2:operator authorization absent; four-hour envelope transferred to T10'),
      ('T10_calibration',19.,19.,'ORDEM015 budget:15h plus4h from unauthorized T09; adaptive limits require witnessed reallocation'),
      ('T14_pyseobnr',2.,2.,'ORDEM015 budget envelope'),('T15_sigma_jit_rec',1.,1.,'ORDEM015 budget envelope'),
      ('R3_LAL_patch',2.,2.,'ORDEM015 R3:1–3h engineering estimate;2h assigned from unallocated balance;no scientific use'),
      ('final_reserve',1.,1.,'ORDEM015 final reserve'),('T16_blind_PE',0.,9.9,'ORDEM015:3x2.6–3.3h estimate; explicit prerequisites absent')]
    rows=[dict(item=k,allocated_machine_hours=a,estimated_wall_hours=e,estimate_source=text,
      estimate_statute='INPUT_OR_DERIVED_NOT_OBSERVED_RUNTIME',actual_machine_hours=0.,job_started=False) for k,a,e,text in specs]
    total=sum(x['allocated_machine_hours'] for x in rows);assert 0<total<=available
    jobs=D/'E2_PE_JOBS_ALLOCATION_015_V1.json'
    save(jobs,dict(schema_version='E2_PE_JOBS_V2',parent_registration_sha256=sha(regpath),jobs={},downloads={},
        scope='NO_NEW_JOB_OR_DOWNLOAD;registered pilot inherited unchanged'))
    at=datetime.now(timezone.utc).isoformat();path=B/'ORCAMENTO_015_v1.json'
    allocation=dict(schema_version='ORCAMENTO_015_V1',registered_utc=at,supersedes_sha256=None,
        parent_registration_sha256=sha(regpath),witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v1.md',
        jobs_relative_to_Chatgpt=jobs.relative_to(ROOT).as_posix(),jobs_sha256=sha(jobs),
        authorized_machine_hours=available,allocated_machine_hours=total,unallocated_machine_hours=available-total,
        source_receipt_relative_to_Chatgpt=source.relative_to(ROOT).as_posix(),source_receipt_sha256=sha(source),
        order_sha256=sha(order),items=rows,accounting=dict(rule='UNION_OF_OWNED_HEAVY_JOB_INTERVALS',intervals=[],
        machine_hours_spent=0.,clock_started=False,simultaneous_process_limit=28),
        pilot_cost_measurement=dict(R5_sha256=sha(qpath),CPU_seconds=q['cpu_seconds'],n=q['n_items'],workers=workers,
            maxcall=job['sampler']['maxcall'],ideal_source_wall_hours=ideal,posterior_convergence_not_measured=True),
        pilot_safety='Registered controller ceiling8h does not enlarge allocated4h:reallocate before exceeding4h or stop owned controller at4h with cleanup; partial run not accepted',
        prerequisites_unpaid=['VERSIONED_ACTIVATION_RECEIPT_PROTOCOL','R7_CLOCK_BEFORE_FIRST_HEAVY_JOB'],
        gate_changed=False)
    save(path,allocation)
    table='\n'.join(f"|{r['item']}|{r['allocated_machine_hours']:.3f}|{r['estimated_wall_hours']:.3f}|" for r in rows)
    note=f'''[REAL — orçamento registrado; INPUT/DERIVED — estimativas; nenhuma máquina pesada iniciada]

allocation_sha256: {sha(path)}
registered_utc: {at}

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}

Disponível lido do recibo: {available!r}h. Alocado:{total:.6f}h; saldo:{available-total:.12f}h. Soma e fonte conferidas, custo estimado não-null por item.

|Item|Alocação h|Estimativa h|
|---|---:|---:|
{table}

Piloto:proxy ideal da R5={ideal:.6f}h de geração, não tempo medido de posterior. Teto externo da alocação4h; controlador cadastrado8h não autoriza gastar acima4h sem nova alocação testemunhada. Sem checkpoints:interrupção não é posterior aceito. Limite28processos;intervalos simultâneos contam uma vez.
As4h da caixa440 não autorizada foram para T10;patchLAL recebeu2h do saldo, sem uso científico. T16 não liberado por este orçamento.
O recibo de máquina livre existe. R7 ainda não nasceu; antes do primeiro job, resolver a MEDIDA de ativação por elo e criar o relógio exclusivo. Registro de orçamento não equivale a execução.
'''
    write(OUT/'ENTREGA_015_ORCAMENTO_015_v1.md',note.encode())
    save(D/'BUDGET_V1_DELIVERY.json',dict(at=at,status='BUDGET_WITNESSED_NO_HEAVY_WORK',allocation_sha256=sha(path),
        witness_sha256=sha(OUT/'ENTREGA_015_ORCAMENTO_015_v1.md'),sum_hours=total,remaining=available-total,gate_changed=False))
    print(json.dumps(dict(allocation_sha256=sha(path),allocated=total,remaining=available-total)))
if __name__=='__main__':main()
