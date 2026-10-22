from pathlib import Path
from datetime import datetime,timezone
import sys,json,math,ast,hashlib
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import write,save,sha
def main():
    at=datetime.now(timezone.utc);result=json.loads((D/'RITE_REPLAY_RESULT.json').read_bytes())
    amended=json.loads((D/'AMENDMENT_DELIVERY.json').read_bytes())
    rec=json.loads((D/'RITE_REPLAY_RECEIPT.json').read_bytes());assert rec['returncode']==0
    assert rec['output_sha256']==sha(D/'RITE_REPLAY_RESULT.json')
    t05=json.loads((B/'bis/015/t05/RESULT.json').read_bytes())
    oracle={(v['event'],v['reading']):v for v in t05['paired_predictions'] if v['mode']=='220'}
    count=0;max_abs=0.
    for row in result['paired_qnm_diagnostics']['rows220']:
        old=oracle[row['event'],row['reading']];assert row['N']==old['N'] and row['status']==old['status']
        a,b=row.get('delta_tau_05_50_95'),old.get('delta_tau_05_50_95')
        if a is None:assert b is None
        else:
            for x,y in zip(a,b):
                assert math.isclose(x,y,rel_tol=3e-14,abs_tol=1e-300)
                max_abs=max(max_abs,abs(x-y))
        count+=1
    sources={x['status'] for x in result['source_pins']}
    summary=dict(status='T12_READER_DELIVERED_LAUNCH_ACTIVATION_MEDIDA',at=at.isoformat(),
        registration_sha256=amended['registration_sha256'],role_counts=result['role_counts'],
        paired220_rows=count,paired220_max_abs_delta_from_T05=max_abs,source_pin_states=sorted(sources),
        legacy_tests=53,variant_tests=72,retired_external_loader_test=1,
        four_asts_unchanged=True,read_only_replay_rc=0,heavy_machine_hours=0,gate_changed=False,
        activation='FIXED_BASE_RECEIPT_DOES_NOT_MATCH_LATEST_AMENDMENT',
        opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'))
    save(D/'RESULT.json',summary)
    write(D/'REAPROVEITAMENTO_T12.md',f'''[REAL — consumidor/testes; DERIVED/INPUT — projeções; OPEN — inferência física]
Variante nova; quatro ASTs herdados preservados. Guarda embutida só autoriza leitura de calibração histórica, não PE/cego.
ERRATA AO LADO de bis/e7_prepare/REAPROVEITAMENTO_E7.md:7: N operacional continua null, mas a matriz agora inclui os alvos E0 condicionais já registrados, com teto calculado e limitação até sigma_jit,rec.
Original preservado, SHA256 {sha(B/'bis/e7_prepare/REAPROVEITAMENTO_E7.md')}.
QNM220 é interpolação cúbica da grade pinada, pareada por draw; não solução analítica exata. O 440 é transportado do resultado T05, associado explicitamente ao alias canônico, não nova extração.
Nenhum teste cego, posterior novo, PE, instalação ou chamada remota. Não se importou/executou um.py.
'''.encode())
    text=f'''[REAL — T12 entregue; NÃO-CEGO; MEDIDA — ativação de jobs sob subemenda]

# T12 — E7 na variante rito

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {summary['opening_sha256']}

PAGO: variante em `ORDEM_013_RINGDOWN/bis/e7_prepare_v1_1/producer/`, quatro ASTs idênticos;53 testes históricos passaram e72 testes da variante passaram. Um teste do importador externo foi aposentado porque esse importador foi removido, com novos controles de guarda em seu lugar. Fonte antiga intocada.

PAGO: subemenda V1.1.1 testemunhada, SHA256 {amended['registration_sha256']}. Histórico E7 continua V1; plano, autorização, posterior e recibo anteriores são conferidos sem reetiquetar a extração. A variante só lê o produto histórico explicitamente pinado.

PAGO: replay rc0 em {rec['wall_seconds']:.3f}s de parede; {summary['role_counts']['calibration']} eventos de calibração, test_count=0. Estados dos pins de fontes/tar: {', '.join(sorted(sources))}. {count} linhas220 concordam com T05, maior diferença absoluta {max_abs:.6g};440 transportado do T05, não reextraído. N_alvo operacional=null, alvos E0 e seus tetos ao lado, gate red com causas. lnB e z físico=null, AWAITING_DATA. Condição de leitura, não ganho de sigma.

MEDIDA: `checked_registration()` da guarda V1.1 devolveu `ValueError: V1.1 activation does not match latest registration/witness`. O recibo fixo descreve V1.1 base. Recibo sucessor publicado ao lado, sem substituir o original. Esta entrega não declara ativação da campanha; mecanismo versionado por elo precisa ser resolvido antes do primeiro job. A guarda V1 antiga chegou ao TimeoutError esperado, preservando sua árvore.

Falhas preservadas: caminho do preparador inicialmente errado (nenhuma saída), WSL sem acesso no sandbox (nenhum trabalho científico iniciado), teste positivo detectou alias GW250114 versus GW250114_082203 e estado OPEN_NO_UNIQUE_EXPONENTIAL; corrigidos antes da testemunha. Revisão local independente apontou quatro inconsistências de metadados/escopo; corrigidas e testadas. Nunca se alterou fórmula para fazer teste passar.

Artefatos: `RITE_REPLAY_RESULT.json` SHA256 {sha(D/'RITE_REPLAY_RESULT.json')}; `RITE_REPLAY_RECEIPT.json` {sha(D/'RITE_REPLAY_RECEIPT.json')}; `RESULT.json` {sha(D/'RESULT.json')}; `LAUNCH_GUARDS.json` {sha(D/'LAUNCH_GUARDS.json')}. Manifesto completo: `DELIVERY.json` nesta pasta.

Reprodução de controles: `/opt/lal_env/bin/python -B .../e7_prepare_v1_1/run_tests.py --legacy` e sem `--legacy`. Fixtures em pasta própria, nunca dados físicos. Replay: comando integral em RITE_REPLAY_RECEIPT; usar destino novo porque o produtor recusa sobrescrita. A cadeia pode ganhar elo posterior e recusar o replay antigo como stale, corretamente.

Axiomas: N/A — sem Lean. Horas de máquina pesada:0. Custos externos novos:0; custo da revisão da coordenação não medido, não tratado como zero. Próximo: orçamento015 e resolução da ativação antes de R7.
'''
    write(OUT/'ENTREGA_015_T12_E7_rito.md',text.encode())
    note=f'''[REAL — MEDIDA de integração; nenhum job iniciado]

Abertura016SHA256: {summary['opening_sha256']}

T03(xi) exige nova subemenda; T03(x) nomeou um único marcador de ativação. A guarda em `bis/e2_code_v1_1/registration_guard.py:67–72` compara o hash desse marcador ao último elo. V1.1.1 foi testemunhada; o marcador permanece V1.1. O comando read-only e a recusa estão em `bis/e7_prepare_v1_1/LAUNCH_GUARDS.json`, SHA256 {sha(D/'LAUNCH_GUARDS.json')}.

Não substituí o recibo citado, não enfraqueci a guarda e não iniciei relógio ou campanha. O sucessor versionado está em `bis/e7_prepare_v1_1/E2_V1_1_1_REGISTRATION_RECEIPT.json`, SHA256 {sha(D/'E2_V1_1_1_REGISTRATION_RECEIPT.json')}.

Proposta à gerência: definir recibo de ativação imutável por elo, ajustar a guarda em árvore versionada e re-pinada, testando pai/testemunha/cronologia e rejeição de recibo trocado. Estimativa de engenharia:0,5–1,5h de bancada,0h de máquina pesada [INPUT — estimativa, não medição]. Fora da árvore atualmente desenhada; proposta, não execução.

Enquanto isso: orçamento e preparo independente. Nenhuma MEDIDA aqui reabre matemática A/C/D nem move gate.
'''
    write(OUT/'ENTREGA_015_MEDIDA_ativacao_por_elo.md',note.encode())
    progress=OUT/'ENTREGA_016_PROGRESSO.md'
    write(progress,progress.read_bytes()+f'\n{at.isoformat()} | B/T12 | PAGO consumidor, MEDIDA ativação por elo |53+72 testes;4 AST;replay rc0;test_count0 | máquina0h | ENTREGA_015_T12_E7_rito.md\n'.encode(),True)
    cp=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    state.update(next_action='PART_B_9B_BUDGET_AND_ACTIVATION_MEDIDA',active_process=None,T12_delivery=str(D/'RESULT.json'),
        part_B_activation_issue=str(OUT/'ENTREGA_015_MEDIDA_ativacao_por_elo.md'))
    save(cp,state,True)
    files={p.relative_to(D).as_posix():sha(p) for p in D.rglob('*') if p.is_file() and p.name!='DELIVERY.json'}
    save(D/'DELIVERY.json',dict(at=at.isoformat(),files=files,scope='ENGINEERING_AND_HISTORICAL_CALIBRATION_ONLY',gate_changed=False))
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
