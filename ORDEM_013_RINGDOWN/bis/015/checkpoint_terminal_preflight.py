"""Publish the completed preparation, retaining the existing live null process."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,ast
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2];R=ROOT/'ORDEM_016_QG';OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha

def main():
    now=datetime.now(timezone.utc).isoformat();p=D/'T04_TERMINAL_PREFLIGHT_PREPARED.json'
    prep=json.loads(p.read_bytes());tests=D/'t04/TERMINAL_GUARD_TESTS.json';v=json.loads(tests.read_bytes())
    assert v['passed']==v['total']==9 and v['source_sha256']==sha(D/'t03_terminal_guard.py')
    old=D/'t04/supervise_t04_v2.py';current=D/'t04/supervise_t04_v3.py'
    def functions(path):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef)}
    x,y=functions(old),functions(current)
    assert all(x[n]==y[n] for n in ('qualify_records','pilot_status'))
    assert not (D/'nulls_campaign_001/RESULT.json').exists(),'Use terminal delivery instead if T03 has ended'
    record=dict(at=now,status='T04_PREFLIGHT_PREPARED_WHILE_T03_RUNNING',
        preparation_sha256=sha(p),fresh_terminal_controls=9,terminal_controls_sha256=sha(tests),
        inherited_record_controls=24,inherited_scope='Two validation functions AST unchanged from V2; not rerun',
        current_supervisor=str(current),budget_preparer=str(D/'prepare_budget_v2_checked.py'),
        process_fixture=str(D/'t04/process_lifecycle_fixture.py'),
        actual_native_400=False,actual_pilot=False,actual_budget_v2=False,actual_process_fixture=False,
        exec_session_id=64813,do_not_restart=True,
        gate_changed=False,canonical_files_changed=False)
    save(D/'T04_PREFLIGHT_DELIVERY.json',record)
    note=f'''[REAL — preparação e controles documentais; execução científica pendente]

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Data: {now}

Revisão local V2: F1/F3/F4/F5 atendidos no escopo inspecionado. Correção adicional: a mera existência de RESULT não basta. O preparador de orçamento e o supervisor atuais exigem término documentado do T03, SUMMARY ligado ao hash do RESULT, entrega no túnel, MEDIDA quando parcial, contabilidade dentro1h e ausência dos processos próprios identificados. Novos controles:9/9; fonteSHA256 {sha(D/'t03_terminal_guard.py')}; testesSHA256 {sha(tests)}. São recibos sintéticos, não ciência nem lifecycle real.

A sugestão inicial de exigir30/30sucessos foi retirada pelo revisor após conferir §3/T04: a ordem manda registrar MEDIDA e continuar. Falha de cauda não se torna sucesso; permanece NÃO PAGA na entrega final. Não foi acrescentado um gate científico ao piloto.

Supervisor atual: t04/supervise_t04_v3.py, SHA256 {sha(current)}. Orçamento: prepare_budget_v2_checked.py, SHA256 {sha(D/'prepare_budget_v2_checked.py')}. Versões anteriores preservadas. Os dois validadores anteriores são idênticos por AST; seus24controles são herdados, não reexecutados nesta versão. O código científico registrado continua intacto.

T03 continua no processo64813; não relançar. Ao terminar: deliver_nulls_campaign.py → prepare_budget_v2_checked.py → conferir a cadeia de alocação → fixture Pool24 → supervise_t04_v3.py qualify → piloto apenas após400pontos aceitos e overflow recusado. A reserva8h/T10 15h ainda NÃO foi publicada; total planejado34,2h inalterado. A fixture só abre após encerramento dos nulos.

Nenhuma API chamada, nenhum gate ou original alterado. O pacote parcial016 continua entregue; relatório final permanece devido após B.
'''
    write(OUT/'ENTREGA_015_T04_preparo_terminal_v3.md',note.encode())
    cp=R/'A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    state.update(at=now,previous_goal_turn='PROGRESS_AND_VERIFIED_WAIT',T04_terminal_preflight=record,
        T04_current_supervisor=str(current),T04_budget_preparer=str(D/'prepare_budget_v2_checked.py'),
        next='POLL_EXISTING_NULLS_64813_NO_RETRY; DELIVER_T03; BUDGET_CHECKED; POOL_FIXTURE; T04_V3_QUALIFY_AND_PILOT',
        next_action='POLL_EXISTING_NULLS_64813_NO_RETRY; DELIVER_T03; BUDGET_CHECKED; POOL_FIXTURE; T04_V3_QUALIFY_AND_PILOT')
    save(cp,state,True)
    progress=OUT/'ENTREGA_016_PROGRESSO.md'
    write(progress,progress.read_bytes()+f'\n{now} | B/T04 preparo terminal |9/9controles de recibo; términoMEDIDA aceito, falha não promovida | T03mesmo processo64813; custo finalpendente\n'.encode(),True)
    print(json.dumps(record))
if __name__=='__main__':main()
