from pathlib import Path
from datetime import datetime,timezone
import sys,json
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[2];ROOT=B.parent;R=ROOT/'ORDEM_016_QG';OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha
now=datetime.now(timezone.utc).isoformat();tests=D/'SUPERVISOR_V2_RECORD_TESTS.json';v=json.loads(tests.read_bytes())
assert len(v['tests'])==24 and all(t['passed'] for t in v['tests'])
assert v['source_sha256']==sha(D/'supervise_t04_v2.py')
rec=dict(at=now,status='T04_SUPERVISOR_V2_PREPARED_NOT_SCIENTIFICALLY_EXECUTED',
    source_sha256=sha(D/'supervise_t04_v2.py'),record_tests_sha256=sha(tests),
    local_review_sha256=sha(D/'review/T04_LOCAL_STATIC_REVIEW.json'),record_controls=24,
    pending=['T03 existing session64813 completion and deliver_nulls_campaign.py',
        'Witness allocationv2 reserving8h pilot and15hT10,totalunchanged34.2h; prudentialreserve notmeasuredruntime',
        'Inspect fixed Pool24 processcreation lifecycle; atmost27processes architecture; nofakekernelhardcapclaim',
        'Only afterT03: run400qualification via supervise_t04_v2.py qualify, thenpilot ifaccepted',
        'Unconfirmedcleanup forbidsfollowingjob;inspectownedgroupbeforecontinuing'],
    scientific_runs=0,gate_changed=False,canonical_files_changed=False)
save(D/'PREPARATION_V2_DELIVERY.json',rec)
note=f'''[REAL — revisão e controles de software; piloto não executado]

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Data: {now}

Revisão local independente: {rec['local_review_sha256']}. Versão anterior preservada. V2: {rec['source_sha256']}; controles dos dois validadores:24/24, SHA256 {rec['record_tests_sha256']}. O teste cobre apenas classificação e pareamento de registros; não é teste de lifecycle completo nem fonte nativa.

Correções: preflight antes de reservar pasta, pareamento exato400PRECALL/RETURN e resumo, qualificação incompleta sai com erro, piloto classifica ausência/falha/partial/cleanup, processo seguinte vedado até confirmar limpeza. V2 lê a alocação corrente e recusa se o limite interno do controlador exceder o reservado.

Antes do piloto: alocação v2 deve reservar8h para coincidir com o hardcap já registrado, transferindo4h de T10(19→15); total34,2h permanece. Reserva prudencial não é custo medido; reconciliar saldo real depois. Até esta nota, essa alocação ainda NÃO foi publicada.

Limite de processos: a arquitetura inspecionada tem supervisor+controller+runner+Pool24=27[DERIVED]; snapshots não são hardcapdeSO. cgroup pids.max conta threads e não se confunde com esse limite. A verificação de lifecycle fica depois do término dos nulos para não somar processos acima28. Nenhuma alteração de código científico, job pinado, semente cega, original ou gate.

T03 continua na sessão64813, controlador próprio com1halocada. Não reiniciar. Próximo: recibo finaldosnulos→entregaT03→preflightT04.
'''
write(OUT/'ENTREGA_015_T04_preparo_supervisao_v2.md',note.encode())
cp=R/'A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
state.update(at=now,previous_goal_turn='PROGRESS_AND_VERIFIED_WAIT',T04_supervisor_preparation=rec,
    T04_current_supervisor=str(D/'supervise_t04_v2.py'),next='POLL_EXISTING_NULLS_64813_NO_RETRY; THEN_DELIVER_T03_AND_T04_PRECONDITIONS',
    next_action='POLL_EXISTING_NULLS_64813_NO_RETRY; THEN_DELIVER_T03_AND_T04_PRECONDITIONS')
save(cp,state,True)
p=OUT/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n{now} | B/T04 preparo |24controles de registros; revisão local incorporada na v2; nenhuma PE | T03 ainda emexecução, custo finalpendente\n'.encode(),True)
print(json.dumps(dict(status=rec['status'],controls=24)))
