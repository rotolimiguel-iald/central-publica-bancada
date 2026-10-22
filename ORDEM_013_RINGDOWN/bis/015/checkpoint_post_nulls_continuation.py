from pathlib import Path
from datetime import datetime,timezone
import json,sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2];OUT=ROOT/'TUNEL/DO_CHATGPT';R=ROOT/'ORDEM_016_QG'
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha
now=datetime.now(timezone.utc).isoformat()
plan=D/'post_nulls_001/PLAN.json';p=json.loads(plan.read_bytes())
assert p['script_sha256']==sha(D/'finish_nulls_and_qualify_t04.py')
record=dict(at=now,status='LIVE_WAIT_FOR_EXISTING_T03',exec_session_id=96991,
    original_nulls_session_id=64813,plan_sha256=sha(plan),script_sha256=p['script_sha256'],
    next='Poll96991;inspectRESULTandexisting64813;neverrelaunch. It deliversT03,budget,fixture,qualify;NOPE.',
    process_rule='Oneextra supervisoryprocess;Poolfixture27+thisparent1=28conditionaltopology',
    native_pilot_launched=False,do_not_restart=True)
save(D/'POST_NULLS_ACTIVE_CHECKPOINT.json',record)
cp=R/'A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
state.update(at=now,previous_goal_turn='PROGRESS_AND_VERIFIED_WAIT',post_nulls_execution=record,
    next='POLL96991_AND64813; REVIEW_POST_NULLS_RESULT; PILOT_ONLY_AFTER_ACTUAL_400AND_RECEIPTS',
    next_action='POLL96991_AND64813; REVIEW_POST_NULLS_RESULT; PILOT_ONLY_AFTER_ACTUAL_400AND_RECEIPTS',
    R3_build_environment=str(D/'r3/BUILD_ENVIRONMENT.json'))
save(cp,state,True)
note=f'''[REAL — continuação única iniciada; resultados científicos ainda pendentes]

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Data: {now}

Processo96991 aguarda o RESULT final da campanhaT03 existente64813. Não inicia nem repete células. PlanoSHA256 {sha(plan)}; scriptSHA256 {p['script_sha256']}. Após término: entregaT03 → guarda terminal documentada → orçamentoV2 → cadeia verificada → fixturePool24 → qualificação400. Interrompe com recibo ao primeiro erro; nunca iniciaPE. A fixture conta27processos na própria subárvore e este pai adiciona1, total28condicional; segue sem concorrência com os nulos.

Estado da ciência nesta abertura: piloto não lançado, qualificação ainda aguardando. A espera deste controlador não é outro intervalo de máquina somado aos nulos. Custos efetivos virão dos recibos de cada etapa. Manifesto de ferramentasR3: SHA256 {sha(D/'r3/BUILD_ENVIRONMENT.json')}; leitura somente, nenhuma instalação/build.

Próximo: conferir os recibos em bis/015/post_nulls_001 e t04/qualify; piloto só após aceitação real. Nenhum gate, original ou dado cego alterado/aberto. Chamadas remotas0.
'''
write(OUT/'ENTREGA_015_T04_continuacao_encadeada.md',note.encode())
progress=OUT/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n{now} | B/T03→T04 | continuação única96991aguarda64813; termina antes daPE | custo finalpendente; não repetir\n'.encode(),True)
print(json.dumps(record))
