"""Persist the sole active pilot handle and immutable launch identity."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;R=ROOT/'ORDEM_016_QG';OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha

def main():
    pilot=D/'t04/pilot';planp=pilot/'PLAN.json';p=json.loads(planp.read_bytes())
    cache=B/'cache/E3_PSEOB_PILOT_V2_S220';launchp=cache/'LAUNCH_CONTEXT.json';launch=json.loads(launchp.read_bytes())
    q=json.loads((D/'t04/QUALIFICATION_DELIVERY.json').read_bytes())
    assert p['blind'] is False and launch['job']=='GW250114_PILOT_V2_S220'
    assert p['registration_sha256']==launch['registration_sha256']
    assert p['allocated_seconds']==28800
    assert not (pilot/'RESULT.json').exists(),'Pilot finished: review terminal receipt instead'
    snapshot=D/'t04/PILOT_LAUNCH_LOG_SNAPSHOT.txt';write(snapshot,(cache/'PRIVATE.log').read_bytes())
    text=snapshot.read_text();assert 'pool with 24 processes' in text and 'Generating initial points' in text
    at=datetime.now(timezone.utc).isoformat()
    record=dict(at=at,status='PILOT_RUNNING_NO_POSTERIOR_VERDICT',exec_session_id=78755,
        job=launch['job'],controller_pid=launch['controller_pid'],controller_start_ticks=launch['controller_start_ticks'],
        started_utc=p['start_utc'],controller_stop_utc=launch['stop_utc'],allocated_seconds=p['allocated_seconds'],
        registration_sha256=launch['registration_sha256'],allocation_sha256=p['allocation_sha256'],
        plan_sha256=sha(planp),launch_context_sha256=sha(launchp),snapshot_sha256=sha(snapshot),
        source_supervisor=str(D/'t04/supervise_t04_v3.py'),workers=24,
        process_observation=dict(source='live exec78755 stdout',observed_counts=[27,27,27],elapsed_seconds=[30.039727878,60.049483476,90.058584268],
            scope='Three live snapshots; not proof of maximum throughout run'),
        machine_hours_before_pilot=q['machine_hours_spent'],blind=False,gate_changed=False,do_not_restart=True,
        next='Poll78755. Inspect t04/pilot/RESULT and calibration CONTROLLER/ANALYST_STATUS/convergence; branchT04 by measured status, never rerun static job')
    save(D/'t04/PILOT_ACTIVE_CHECKPOINT.json',record)
    note=f'''[REAL — NÃO-CEGO; piloto em execução, nenhum veredito de posterior]

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Data: {at}

Job: {launch['job']}. Início supervisor: {p['start_utc']}. Teto8h, conforme orçamentoSHA256 {p['allocation_sha256']}. RegistroSHA256 {launch['registration_sha256']}; planoSHA256 {sha(planp)}; LAUNCH_CONTEXTsha256 {sha(launchp)}. Qualificação400concluída antes, conforme ENTREGA_015_T04_qualificacao_400.md.

Pool24 iniciado;27processos próprios observados em três snapshots ao redor30/60/90s. Snapshot imutável do logSHA256 {sha(snapshot)}. O amostrador iniciou pontos do prior. Não há posterior aceito, convergência nem sigmafísico nesta entrega.

Processo ativo78755: acompanhar, nunca relançar. Máquina antes do piloto={q['machine_hours_spent']:.9f}h; custo destejob só será encerrado no recibo terminal. Se falhar, a árvoreC/D/E/H/FdaT04 manda, com novoIDapenasquando autorizado pelo ramo e orçamento antes. R3vem depois do T04; nenhuma outra campanha pesada foi aberta.

T03 permaneceMEDIDA:0/30células. Nenhum gate ou original foi alterado pela bancada. Recibo de continuidadeSHA256 {sha(D/'t04/PILOT_ACTIVE_CHECKPOINT.json')}.
'''
    write(OUT/'ENTREGA_015_T04_piloto_iniciado.md',note.encode())
    cp=R/'A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    state.update(at=at,previous_goal_turn='PROGRESS_AND_VERIFIED_WAIT',active_process=record,
        next='POLL_EXISTING_PILOT_78755; NO_RELAUNCH; ON_TERMINAL_REVIEW_T04_BRANCH',
        next_action='POLL_EXISTING_PILOT_78755; NO_RELAUNCH; ON_TERMINAL_REVIEW_T04_BRANCH')
    save(cp,state,True)
    progress=OUT/'ENTREGA_016_PROGRESSO.md'
    write(progress,progress.read_bytes()+f'\n{at} | B/T04 pilotoA | execução78755única,24workers,27processosobservados; semveredito | custofinalpendente; prévio{q["machine_hours_spent"]:.9f}h\n'.encode(),True)
    print(json.dumps({k:record[k] for k in ('status','exec_session_id','job','workers','started_utc')}))
if __name__=='__main__':main()
