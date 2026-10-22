"""Register reviewed bosonic filtered moments and cutoff bounds; keep integral R4/R5 open."""
import datetime as dt
import json
import subprocess
import sys
import support_r75 as s


def once(label, command):
    s.new(label + '_INTENT.json', {'command': command, 'utc': dt.datetime.now(dt.timezone.utc).isoformat()})
    proc = subprocess.run(command, capture_output=True, encoding='utf-8')
    path = s.new(label + '_RESULT.json', {'exit_code': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr})
    if proc.returncode:
        raise RuntimeError(str(path))
    return path


def main():
    assert sys.argv[1:] == ['--apply']
    assert not (s.ROOT / 'DELIVERY_R75.json').exists()
    review = json.loads((s.ROOT / 'REVIEW_R75.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer'] != s.ACTOR['id']
    for item in review['evidence']:
        assert s.pin(item['path']) == item
    for name in ['finish_r75.py', 'support_r75.py', 'memory_r75.py', 'MEMORY_PLAN_R75.json', 'MEMORY_APPEND_R75.txt', 'RESULT_R75.json']:
        assert s.pin(s.ROOT / name) in review['evidence']
    result = json.loads((s.ROOT / 'RESULT_R75.json').read_text(encoding='utf-8'))
    assert result['passed'] is True and result['exit_code'] == 0
    mission = s.project('FINISH_PROJECT')
    for task_id in ('R4', 'R5'):
        task = next(x for x in mission['projection']['active'] if x['id'] == task_id)
        s.call({'operation': 'check', 'reference': s.REF, 'actor': s.ACTOR,
                'expected_revision': mission['receipt']['revision'], 'projection_sha256': mission['projection_sha256'],
                'task_id': task_id, 'lease_id': task['lease']['id']}, 'FINISH_CHECK_' + task_id)
    once('MEMORY_APPLY', [sys.executable, '-B', '-X', 'utf8', str(s.ROOT / 'memory_r75.py'), 'apply'])
    delivery = s.new('DELIVERY_R75.json', {
        'status': 'REVIEWED_BOSONIC_FILTERED_MOMENTS_COMPONENT', 'unit': 'F1.FECHO_20261015',
        'claim': 967, 'scope_event': 975, 'author': s.ACTOR['id'],
        'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'evidence': [s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix != '.pyc'],
        'scope': 'Analytic first/second filtered moment limits, covariances and decoder with explicit total-number cutoff bounds; finite-support initial state and finite time. Synthetic finite-cutoff controls reuse R57/R64/R66/R74. No unbounded HP unitary or physical calibration claimed.',
        'R4_R5_integrally_satisfied': False, 'physical_measurements': 0, 'new_lean_builds': 0,
        'canonical_changed': False, 'gate_changed': False})
    entry = s.new('MAP_ENTRY_R75.json', {
        'tipo': 'RESULTADO', 'rota_id': 'formal.f1_rede.concrete_bosonic_kinematics', 'dominio': 'FORMAL',
        'titulo': 'R75: momentos filtrados bosonicos com erro explicito de corte',
        'metodo': 'Reuso R57/R64/R66/R74; series Dyson com insercoes de leitura, suporte bilateral e caudas ponderadas; consumidor sintetico preregistrado e revisao distinta.',
        'resultado': 'Primeiros e segundos momentos, covariancias e decoder possuem limite funcional com cotas de corte para suporte inicial e tempo finitos. Contato de ruido preservado; controles sinteticos por item em RESULT_R75.json.',
        'veredito': 'PASS_COMPONENT_WITH_SCOPE', 'estatuto': 'DERIVED', 'status': 'EM_CURSO', 'olhou_dados': False,
        'defeito': 'Limite de momentos nao constroi unitaria HP ilimitada, distribuicao completa de trajetorias nem realizacao fisica. Gamma, ganhos, materiais e relogio continuam sem calibracao por esta camada; R4/R5 integrais abertos.',
        'nao_refazer': 'Reusar semigrupo e reservatorio R66, localizacao R71, perfis/energia R72, transporte R74 e cotas R75. Nao converter corte hardcore em bosonico nem pedir novamente o mecanismo ja construido.',
        'proximo_passo': 'Integrar o consumidor de momentos aos perfis e a resposta instrumental do mesmo dispositivo; obter calibracoes independentes de relogio, ganhos e Gamma, conservando banho, preparo e criterios integrais R4/R5.',
        'artefatos': [str(delivery), str(s.ROOT / 'RESULT_R75.json'), str(s.ROOT / 'MEMORY_APPEND_R75.txt')],
        'onde': str(s.ROOT), 'refs': ['formal.anchored_name_contour']})
    mapped = once('MAP_REGISTER', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', str(entry), '--quem', s.ACTOR['id']])
    boarded = once('BOARD_REGISTER', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\PROGRAMA_IALD\iald.py', 'avancar', 'F1.FECHO_20261015', '--quem', s.ACTOR['id'], '--status', 'EM_CURSO', '--evidencia', str(delivery), '--nota', 'R75: momentos filtrados bosonicos e cotas de corte revisados; verificacao sintetica. Reivindicacao 967, escopo 975, memoria com backup. R4/R5 integrais abertos; sem producao ou gate.'])
    registration = s.new('REGISTRATION_R75.json', {'delivery': s.pin(delivery), 'map': s.pin(mapped), 'board': s.pin(boarded)})
    s.mutate('release', 'RELEASE_R4', task_id='R4', reason='Componente de momentos bosonicos R75 concluido e revisado. Integracao instrumental e calibracao fisica do mesmo dispositivo seguem abertas.', sources=[s.pin(delivery)])
    s.mutate('release', 'RELEASE_R5', task_id='R5', reason='Componente de momentos bosonicos R75 entregue; realizacao integral da rede permanece aberta.', sources=[s.pin(delivery)])
    state = s.call({'operation': 'get', 'reference': s.REF}, 'FINISH_GET', 'session_memory.py')
    handles = list(state['p']['handles'])
    assert not any(h.get('id') == 'r75-synthetic-bosonic-readout-execution' for h in handles)
    run = json.loads((s.ROOT / 'RESULT_R75.json').read_text(encoding='utf-8'))
    handles.append({'id': 'r75-synthetic-bosonic-readout-execution', 'status': 'completed',
                    'agent': '/root', 'started_utc': run['started_utc'], 'ended_utc': run['ended_utc'],
                    'execution_count': 1, 'result': s.pin(s.ROOT / 'RESULT_R75.json')})
    s.call({'operation': 'transition', 'reference': s.REF, 'actor': s.ACTOR,
            'expected_revision': state['revision'], 'event_id': 'r75-bosonic-filtered-moments-recorded',
            'changes': {'records': [{'id': 'r75-bosonic-filtered-moments', 'kind': 'fact', 'statute': 'DERIVED',
                'sources': [{'kind': 'artifact', 'ref': str(p), 'sha256': s.pin(p)['sha256']} for p in (delivery, registration)],
                'text': (s.ROOT / 'MEMORY_APPEND_R75.txt').read_text(encoding='utf-8')}],
                'flow': {'phase': 'r75_bosonic_filtered_moments_reviewed',
                    'next_action': 'Integrar os momentos filtrados e suas cotas aos perfis reconhecidos e a resposta instrumental do mesmo dispositivo. Calibrar relogio, ganhos e Gamma por informacao independente; manter preparo/banho e realizacao fisica integral abertos. Reusar R57/R64/R66/R71/R72/R74/R75 sem repetir construcoes satisfeitas. R4/R5 integrais abertos; claim/check antes de avancar.',
                    'handles': handles}}}, 'FINISH_TRANSITION', 'session_memory.py')
    print(delivery)


if __name__ == '__main__':
    main()

