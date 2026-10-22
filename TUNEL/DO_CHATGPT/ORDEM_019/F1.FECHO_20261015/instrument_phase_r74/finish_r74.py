"""Register a reviewed instrument bridge; never close integral R4 or R5."""
import datetime as dt
import json
import subprocess
import sys
import support_r74 as s


def once(label, command):
    s.new(label + '_INTENT.json', {'command': command, 'utc': dt.datetime.now(dt.timezone.utc).isoformat()})
    proc = subprocess.run(command, capture_output=True, encoding='utf-8')
    path = s.new(label + '_RESULT.json', {'exit_code': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr})
    if proc.returncode:
        raise RuntimeError(str(path))
    return path


def main():
    assert sys.argv[1:] == ['--apply']
    assert not (s.ROOT / 'DELIVERY_R74.json').exists()
    review = json.loads((s.ROOT / 'REVIEW_R74.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer'] != s.ACTOR['id']
    for item in review['evidence']:
        assert s.pin(item['path']) == item
    for name in ['finish_r74.py', 'support_r74.py', 'memory_r74.py', 'MEMORY_PLAN_R74.json', 'MEMORY_APPEND_R74.txt', 'RESULT_R74.json']:
        assert s.pin(s.ROOT / name) in review['evidence']
    result = json.loads((s.ROOT / 'RESULT_R74.json').read_text(encoding='utf-8'))
    assert result['passed'] is True and result['exit_code'] == 0
    mission = s.project('FINISH_PROJECT')
    task = next(x for x in mission['projection']['active'] if x['id'] == 'R4')
    s.call({'operation': 'check', 'reference': s.REF, 'actor': s.ACTOR,
            'expected_revision': mission['receipt']['revision'], 'projection_sha256': mission['projection_sha256'],
            'task_id': 'R4', 'lease_id': task['lease']['id']}, 'FINISH_CHECK')
    once('MEMORY_APPLY', [sys.executable, '-B', '-X', 'utf8', str(s.ROOT / 'memory_r74.py'), 'apply'])
    delivery = s.new('DELIVERY_R74.json', {
        'status': 'REVIEWED_PHASE_INSTRUMENT_BRIDGE', 'unit': 'F1.FECHO_20261015',
        'claim': 967, 'scope_event': 973, 'author': s.ACTOR['id'],
        'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'evidence': [s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix != '.pyc'],
        'scope': 'Finite full-generator phase transport and synthetic filtered readout; prior R57/R64/R66 reused.',
        'R4_R5_integrally_satisfied': False, 'physical_measurements': 0, 'new_lean_builds': 0,
        'canonical_changed': False, 'gate_changed': False})
    entry = s.new('MAP_ENTRY_R74.json', {
        'tipo': 'RESULTADO', 'rota_id': 'formal.f1_rede.concrete_bosonic_kinematics', 'dominio': 'FORMAL',
        'titulo': 'R74: transporte de fase do gerador completo ao instrumento de leitura',
        'metodo': 'Reuso R57, R64 e R66; derivacao por conjugacao e consumidor sintetico preregistrado, revisao distinta.',
        'resultado': 'Gerador, salto conjunto, bombeamento e leitura transportados com a mesma referencia. Resultados e controles por item em RESULT_R74.json.',
        'veredito': 'PASS_COMPONENT_WITH_SCOPE', 'estatuto': 'DERIVED', 'status': 'EM_CURSO', 'olhou_dados': False,
        'defeito': 'Teste sintetico finito nao calibra Gamma, ganhos ou materiais; nao identifica arbitrariamente GOH com sinal de saida nem fecha R4/R5 integrais.',
        'nao_refazer': 'Reusar reconhecimento R57 e continuidade M2. Fases variaveis acompanham a coleta; nao pedir nova definicao ao operador.',
        'proximo_passo': 'Usar consumidor transportado ao ligar perfis materiais e calibracoes dos canais do mesmo aparelho; preservar contratos locais e banho comum.',
        'artefatos': [str(delivery), str(s.ROOT / 'RESULT_R74.json'), str(s.ROOT / 'MEMORY_APPEND_R74.txt')],
        'onde': str(s.ROOT), 'refs': ['formal.anchored_name_contour']})
    mapped = once('MAP_REGISTER', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', str(entry), '--quem', s.ACTOR['id']])
    boarded = once('BOARD_REGISTER', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\PROGRAMA_IALD\iald.py', 'avancar', 'F1.FECHO_20261015', '--quem', s.ACTOR['id'], '--status', 'EM_CURSO', '--evidencia', str(delivery), '--nota', 'R74: ponte de fase gerador-reservatorio-instrumento revisada; verificacao sintetica. Claim967scope973, memoria combackup. R4/R5 integrais abertos; semproducao/gate.'])
    registration = s.new('REGISTRATION_R74.json', {'delivery': s.pin(delivery), 'map': s.pin(mapped), 'board': s.pin(boarded)})
    s.mutate('release', 'RELEASE_R4', task_id='R4', reason='Componente R74 concluido e revisado. Reusar transporte de fase; identificacao e calibracao fisica integrais seguem abertas.', sources=[s.pin(delivery)])
    state = s.call({'operation': 'get', 'reference': s.REF}, 'FINISH_GET', 'session_memory.py')
    handles = list(state['p']['handles'])
    assert not any(h.get('id') == 'r74-synthetic-instrument-execution' for h in handles)
    run = json.loads((s.ROOT / 'RESULT_R74.json').read_text(encoding='utf-8'))
    handles.append({'id': 'r74-synthetic-instrument-execution', 'status': 'completed',
                    'agent': '/root', 'started_utc': run['started_utc'], 'ended_utc': run['ended_utc'],
                    'execution_count': 1, 'result': s.pin(s.ROOT / 'RESULT_R74.json')})
    s.call({'operation': 'transition', 'reference': s.REF, 'actor': s.ACTOR,
            'expected_revision': state['revision'], 'event_id': 'r74-phase-instrument-bridge-recorded',
            'changes': {'records': [{'id': 'r74-phase-instrument-bridge', 'kind': 'fact', 'statute': 'DERIVED',
                'sources': [{'kind': 'artifact', 'ref': str(p), 'sha256': s.pin(p)['sha256']} for p in (delivery, registration)],
                'text': (s.ROOT / 'MEMORY_APPEND_R74.txt').read_text(encoding='utf-8')}],
                'flow': {'phase': 'r74_phase_instrument_bridge_reviewed',
                    'next_action': 'Reusar consumidor de fase e seus contratos, ligar perfis e calibracoes dos canais do mesmo dispositivo. Nao refazer R57/M2/R64/R66/R74 nem perguntar novamente o mecanismo. R4/R5 integrais abertos; claim/check antes de avancar.',
                    'handles': handles}}}, 'FINISH_TRANSITION', 'session_memory.py')
    print(delivery)


if __name__ == '__main__':
    main()
