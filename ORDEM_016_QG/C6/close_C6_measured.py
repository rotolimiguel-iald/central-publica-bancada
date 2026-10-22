"""Preserve completed graph calculations and close the elapsed C6 timebox."""
from pathlib import Path
from datetime import datetime, timezone
import json, sys

ROOT = Path(__file__).resolve().parents[1]
C, H = ROOT / 'C6', ROOT / 'A7'
sys.path.insert(0, str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT, sha, put, write, append


def main():
    now = datetime.now(timezone.utc)
    start = json.loads((C / 'START.json').read_bytes())
    deadline = datetime.fromisoformat(start['deadline_utc'])
    assert now >= deadline
    dest = C / 'timebox_closure'
    dest.mkdir(exist_ok=False)
    names = ['metric_euler_ghost_vertex', 'ghost_euler_ghost_vertex',
             'ghost_vertices_joint_symbol']
    results, checked = {}, []
    for name in names:
        manifest = C / name / 'manifest.json'
        for entry in json.loads(manifest.read_bytes())['files']:
            p = Path(entry['path'])
            actual = sha(p)
            assert actual == entry['sha256'], (p, actual, entry['sha256'])
            checked.append(dict(path=str(p), sha256=actual))
        results[name] = json.loads((C / name / 'results.json').read_bytes())
    joint = results['ghost_vertices_joint_symbol']
    assert joint['checks'] == 480 and joint['covariant_adjoint_pending']
    assert datetime.fromisoformat(joint['at']) < deadline
    opening = sha(OUT / 'ENTREGA_016_ABERTURA_operador.md')
    log = C / 'ghost_vertices_joint_symbol_check_run.log'
    pending = C / 'ghost_vertices_covariant_adjoint_check.py'
    total = sum(v['checks'] for v in results.values())
    cpu = sum(v['cpu_seconds'] for v in results.values())
    receipt = dict(at=now.isoformat(), status='MEDIDA_TIMEBOX_EXHAUSTED',
        start=start, completed_before_deadline=True, results=results,
        checks_newly_delivered=total, cpu_seconds_newly_delivered=cpu,
        process_observation=dict(session_id=34765, exit_code=0,
            observed_utc=now.isoformat(), log_sha256=sha(log)),
        manifest_entries_verified=len(checked),
        covariant_adjoint=dict(path=str(pending), sha256=sha(pending),
            status='PREPARED_NOT_EXECUTED_TIMEBOX_EXHAUSTED'),
        Q2_status='OPEN', gate_changed=False, new_external_calls=0,
        next='ORDEM015 PartB T01; no restart of C6',
        elapsed_wall_hours=(now-datetime.fromisoformat(start['at'])).total_seconds()/3600,
        elapsed_is_not_active_machine_time=True)
    put(dest / 'results.json', receipt)
    note = f'''[DERIVED+CAS / OPEN — C6 encerrada por teto; Q2 integral não paga]

AberturaSHA256={opening}.

O cálculo iniciado na sessão 34765 concluiu com rc0. O resultado foi gravado
em {joint['at']}, antes do prazo {start['deadline_utc']}; a conclusão foi
conferida em {now.isoformat()}. O prazo não foi reiniciado. A transposição
covariante preparada permanece NÃO EXECUTADA; não é uma prova disponível.

Entregam-se os dois grafos locais com vértice ghost, cutoff constante e
primeira ordem de curvatura, mais os símbolos que conservam independentes
as derivadas nas extremidades. São {total} controles já executados,
CPU {cpu}s: 160 + 160 + 480. Os manifestos foram conferidos byte a byte
({len(checked)} entradas). Não houve nova execução matemática nesta entrega.

Na base w_ab[a delta_ab q_r q² + b(delta_ar q_b + delta_br q_a)q²
+ c q_a q_b q_r], w_ab=1 na diagonal e2 fora dela, as amplitudes locais
de primeira curvatura, com a normalização comum dos motores, são:
- Euler métrico × vértice ghost: (a,b,c)=(-263/768,89/768,9/128).
- Euler ghost × vértice ghost: (a,b,c)=(-4445/4608,-1361/4608,221/128).
Essas tabelas são amplitudes em ondas paralelas locais, sem fator temporal
adicional. Não constituem ainda o operador covariante sobre o ghost:
unir os momentos antes da adjunção apaga a ordem das derivadas e pode
ocultar comutadores de curvatura. As tabelas conjuntas preservam esses dados.

Resultado já entregue e mantido: no setor escalar linearizado, K constante,
prescrição declarada e suporte compacto, N*=N e
B_scalar=-CE/2 integral h.Nh satisfaz s0 B_scalar=A_scalar até K².
Isso não substitui o representante completo de Q2.

Pendência nomeada: Q2FullCausalRepresentativeAndPrimitive. Ainda exige
adjuntar covariantemente os dois grafos, completar a montagem métrica/ghost
e os pesos temporais na mesma prescrição, incluindo cutoff variável,
verificar a consistência WZ e a classe/primitiva integral. O escopo executado
é o auxiliar euclidiano local em espaço de curvatura constante, não uma
conclusão sobre toda a rede lorentziana. C6: MEDIDA, aceitação integral NÃO PAGA.

Log: {log}; SHA256={sha(log)}.
Comando original: symbolic_runtime\\Scripts\\python.exe -X utf8 -B
C6\\ghost_vertices_joint_symbol_check.py; rc0 observado pela sessão34765.
Custo novo de provedor: nenhuma chamada; custos anteriores não recontados.
Próximo ramo autorizado: Parte B / ORDEM015, T01. Gate/originais intactos.
'''
    write(dest / 'MEDIDA.md', note.encode('utf-8'))
    write(OUT / 'ENTREGA_016_MEDIDA_C6_teto_e_grafos_ghost.md', note.encode('utf-8'))
    paths = [Path(__file__), C/'START.json', log, pending, dest/'results.json',
             dest/'MEDIDA.md'] + [C/n/'manifest.json' for n in names]
    put(dest/'manifest.json', dict(opening_sha256=opening,
        files=[dict(path=str(p), sha256=sha(p)) for p in paths],
        verified_source_entries=checked))
    append(OUT/'LEDGER_016.jsonl', json.dumps(dict(at=now.isoformat(),
        event='C6_TIMEBOX_CLOSED_WITH_COMPLETED_GRAPHS', target='C6',
        checks=total, cpu_seconds=cpu, external_call=False,
        manifest_sha256=sha(dest/'manifest.json')), ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md', f'\n{now.isoformat()} | C6 MEDIDA: teto8h vencido; Q2 integral NÃO PAGA. Dois grafos locais e símbolos separados: {total} controles, CPU{cpu}s, rc0; adjunção preparada NÃO EXECUTADA. Próximo: ParteB/T01.\n')
    p=H/'CONTINUIDADE.json'
    state=json.loads(p.read_bytes())
    state.update(at=now.isoformat(), previous_goal_turn='PROGRESS',
        C6_status='MEDIDA_TIMEBOX_EXHAUSTED', C6_closure_manifest=str(dest/'manifest.json'),
        own_live_process=None, pending_orchestration='All C6 units terminal and audited',
        next='ORDEM015 PartB T01 then T02 and T13, prescribed order; no C6 restart',
        remaining_full_goal=['ORDEM015 PartB ordered tree', 'final completion audit and reports'])
    put(p,state,True)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
