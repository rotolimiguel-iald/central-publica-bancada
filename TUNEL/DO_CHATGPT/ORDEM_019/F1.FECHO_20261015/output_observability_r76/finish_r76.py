"""Register reviewed output-to-initial-occupation observability; keep integral R4/R5 open."""
import datetime as dt
import json
import subprocess
import sys
import support_r76 as s


def once(label, command):
    s.new(label + '_INTENT.json', {'command': command, 'utc': dt.datetime.now(dt.timezone.utc).isoformat()})
    proc = subprocess.run(command, capture_output=True, encoding='utf-8')
    path = s.new(label + '_RESULT.json', {'exit_code': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr})
    if proc.returncode:
        raise RuntimeError(str(path))
    return path


def main():
    assert sys.argv[1:] == ['--apply']
    assert not (s.ROOT / 'DELIVERY_R76.json').exists()
    review = json.loads((s.ROOT / 'REVIEW_R76.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer'] != s.ACTOR['id']
    for item in review['evidence']:
        assert s.pin(item['path']) == item
    for name in ['finish_r76.py', 'support_r76.py', 'memory_r76.py', 'MEMORY_PLAN_R76.json', 'MEMORY_APPEND_R76.txt', 'RESULT_R76.json']:
        assert s.pin(s.ROOT / name) in review['evidence']
    result = json.loads((s.ROOT / 'RESULT_R76.json').read_text(encoding='utf-8'))
    assert result['passed'] is True and result['exit_code'] == 0
    mission = s.project('FINISH_PROJECT')
    for task_id in ('R4', 'R5'):
        task = next(x for x in mission['projection']['active'] if x['id'] == task_id)
        s.call({'operation': 'check', 'reference': s.REF, 'actor': s.ACTOR,
                'expected_revision': mission['receipt']['revision'], 'projection_sha256': mission['projection_sha256'],
                'task_id': task_id, 'lease_id': task['lease']['id']}, 'FINISH_CHECK_' + task_id)
    once('MEMORY_APPLY', [sys.executable, '-B', '-X', 'utf8', str(s.ROOT / 'memory_r76.py'), 'apply'])
    delivery = s.new('DELIVERY_R76.json', {
        'status': 'REVIEWED_OUTPUT_OBSERVABILITY_COMPONENT', 'unit': 'F1.FECHO_20261015',
        'claim': 967, 'scope_event': 977, 'author': s.ACTOR['id'],
        'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'evidence': [s.pin(p) for p in sorted(s.ROOT.rglob('*')) if p.is_file() and p.suffix != '.pyc'],
        'scope': 'Instrument effects and robust reconstruction of initial occupation on a named finite preparation support, with R75 cutoff and measurement/model error budget. Synthetic observability and negative controls; no independent physical calibration claimed.',
        'R4_R5_integrally_satisfied': False, 'physical_measurements': 0, 'new_lean_builds': 0,
        'canonical_changed': False, 'gate_changed': False})
    entry = s.new('MAP_ENTRY_R76.json', {
        'tipo': 'RESULTADO', 'rota_id': 'formal.f1_rede.concrete_bosonic_kinematics', 'dominio': 'FORMAL',
        'titulo': 'R76: observabilidade da ocupacao inicial pela leitura de saida',
        'metodo': 'Reuso R64/R66/R72/R74/R75; efeitos do instrumento e residuos espectrais com propagacao de incertezas; consumidor sintetico preregistrado e revisao distinta.',
        'resultado': 'Criterio explicito de recuperacao da ocupacao inicial a partir dos momentos de saida; condicionamento, residuos e intervalo robusto expostos. Resultado cientifico por alvo em RESULT_R76.json, sem presumir observabilidade util.',
        'veredito': 'PASS_COMPONENT_WITH_SCOPE', 'estatuto': 'DERIVED', 'status': 'EM_CURSO', 'olhou_dados': False,
        'defeito': 'Instrumento condicionado ao mesmo gerador/preparo e calibracoes; reconstrucao pode amplificar erro. Posto numerico nao comprova precisao fisica. Gamma e realizacao integral R4/R5 seguem abertos.',
        'nao_refazer': 'Reusar semigrupo/reservatorio R66, localizacao R71, testemunha R72, fases R74 e cotas R75. R76 acrescenta criterio de observabilidade, nao redefine reconhecimento.',
        'proximo_passo': 'Usar diagnostico R76 para escolher a proxima ligacao material sem repetir campanhas; preservar orcamento de erros, parametros independentes e realizacao integral aberta.',
        'artefatos': [str(delivery), str(s.ROOT / 'RESULT_R76.json'), str(s.ROOT / 'MEMORY_APPEND_R76.txt')],
        'onde': str(s.ROOT), 'refs': ['formal.anchored_name_contour']})
    mapped = once('MAP_REGISTER', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', str(entry), '--quem', s.ACTOR['id']])
    boarded = once('BOARD_REGISTER', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\PROGRAMA_IALD\iald.py', 'avancar', 'F1.FECHO_20261015', '--quem', s.ACTOR['id'], '--status', 'EM_CURSO', '--evidencia', str(delivery), '--nota', 'R76: criterio de observabilidade saida-preparo e verificacao sintetica revisados. Reivindicacao967, escopo977, memoria com backup. Resultado por alvo, sem presumir calibracao; R4/R5 integrais abertos.'])
    registration = s.new('REGISTRATION_R76.json', {'delivery': s.pin(delivery), 'map': s.pin(mapped), 'board': s.pin(boarded)})
    s.mutate('release', 'RELEASE_R4', task_id='R4', reason='Componente R76 concluido e revisado: observabilidade e incertezas explicitadas. Calibracao fisica do mesmo dispositivo segue aberta.', sources=[s.pin(delivery)])
    s.mutate('release', 'RELEASE_R5', task_id='R5', reason='Componente R76 entregue; realizacao integral da rede permanece aberta.', sources=[s.pin(delivery)])
    state = s.call({'operation': 'get', 'reference': s.REF}, 'FINISH_GET', 'session_memory.py')
    handles = list(state['p']['handles'])
    assert not any(h.get('id') == 'r76-synthetic-observability-execution' for h in handles)
    run = json.loads((s.ROOT / 'RESULT_R76.json').read_text(encoding='utf-8'))
    handles.append({'id': 'r76-synthetic-observability-execution', 'status': 'completed',
                    'agent': '/root', 'started_utc': run['started_utc'], 'ended_utc': run['ended_utc'],
                    'execution_count': 1, 'result': s.pin(s.ROOT / 'RESULT_R76.json')})
    s.call({'operation': 'transition', 'reference': s.REF, 'actor': s.ACTOR,
            'expected_revision': state['revision'], 'event_id': 'r76-output-observability-recorded',
            'changes': {'records': [{'id': 'r76-output-observability', 'kind': 'fact', 'statute': 'DERIVED',
                'sources': [{'kind': 'artifact', 'ref': str(p), 'sha256': s.pin(p)['sha256']} for p in (delivery, registration)],
                'text': (s.ROOT / 'MEMORY_APPEND_R76.txt').read_text(encoding='utf-8')}],
                'flow': {'phase': 'r76_output_observability_reviewed',
                    'next_action': 'R76 ligou saida a testemunha N_b sob suporte P1; N_total com OH permanece inconclusivo por erro amplificado. Proximo foco: leitor/controle OH ja no acervo ou cota mais informativa, desenho novo preregistrado antes de executar. Nao repetir R57/R64/R66/R71/R72/R74/R75/R76. Calibracoes independentes e realizacao integral abertas; claim/check antes de avancar.',
                    'handles': handles}}}, 'FINISH_TRANSITION', 'session_memory.py')
    print(delivery)


if __name__ == '__main__':
    main()


