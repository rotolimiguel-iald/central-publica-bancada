"""Register reviewed R57 components without accepting the whole physical bridge."""
import datetime as dt
import subprocess
import sys
import support_r57 as s


def pin(path):
    item = s.pin(path)
    return {k: item[k] for k in ('path', 'sha256')}


def run_once(label, args):
    s.new(label + '_INTENT.json', {'command': args, 'utc': dt.datetime.now(dt.timezone.utc).isoformat()})
    result = subprocess.run(args, capture_output=True, encoding='utf-8')
    path = s.new(label + '_RESULT.json', {'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    if result.returncode:
        raise RuntimeError(str(path))
    print(result.stdout[:1800])
    return path


def main():
    project = s.project()
    task = next(t for t in project['projection']['active'] if t['id'] == 'R5')
    s.call('mission_cli.py', {'operation': 'check', 'reference': str(s.REFERENCE), 'actor': s.ACTOR,
        'expected_revision': project['receipt']['revision'], 'projection_sha256': project['projection_sha256'],
        'task_id': 'R5', 'lease_id': task['lease']['id']}, 'FINAL_CUSTODY_PREFLIGHT')
    paths = [s.ROOT / n for n in ['COMPONENTS_CONSOLIDATED_R57.json', 'RELATORIO_CONSOLIDADO_R57.txt',
        'MEMORY_APPLIED_R57.json', 'MEMORY_REVIEW_R57.json']]
    paths += [s.ROOT.parent / 'review_r57' / 'R57_FINAL_COMPONENT_REVIEW_R2.json']
    delivery = s.new('DELIVERY_CONSOLIDATED_R57.json', {
        'status': 'COMPONENTS_DELIVERED_WITH_SCOPE', 'unit': 'F1.FECHO_20261015', 'claim': 939,
        'author': s.ACTOR['id'], 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'reference': pin(s.REFERENCE), 'evidence': [pin(p) for p in paths],
        'symbolic_checks': 34, 'axiom_reports': 37, 'lean_components': 4,
        'full_R4_satisfied': False, 'full_R5_satisfied': False,
        'next_action': 'Derive physical two-point form from existing device observables and compare with circularSmear; preserve clock calibration and state/dynamics convergence obligations.',
        'scope': 'Local finite-model clock and formal target packets; no physical device realization, global clock, universal H3 or full QG conclusion.'})
    entry = s.new('MAP_ENTRY_CONSOLIDATED_R57.json', {
        'tipo': 'RESULTADO', 'rota_id': 'formal.f1_rede.concrete_bosonic_kinematics', 'dominio': 'FORMAL',
        'titulo': 'R57: relógio local, leitura de fronteira fixa e limite de pacotes no H1',
        'metodo': 'Reaproveitamento de fontes; quatro componentes Lean em sandbox, cálculo simbólico exato e revisão independente de evidências.',
        'resultado': '34 verificações simbólicas; 37 relatórios de axiomas no trio. Oito memórias acrescentadas com backups. R4 e R5 integrais permanecem abertos.',
        'veredito': 'PASS_COMPONENT_WITH_SCOPE', 'estatuto': 'REAL', 'status': 'EM_CURSO', 'olhou_dados': False,
        'defeito': 'Densidade dos pacotes no alvo não identifica excitações, estado nem dinâmica do dispositivo; relógio apenas local no modelo finito.',
        'nao_refazer': 'Reutilizar builds verdes e recibos R57. Não repetir provedores ou converter obstrução da torre produto em impossibilidade geral.',
        'proximo_passo': 'Calcular forma física de duas pontas e sua correspondência com circularSmear; concluir calibração e entrelaçamento.',
        'artefatos': [str(delivery), *[str(p) for p in paths]], 'onde': str(s.ROOT)})
    map_result = run_once('MAP_REGISTER_CONSOLIDATED_R57', [sys.executable, '-B', '-X', 'utf8',
        r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', str(entry), '--quem', s.ACTOR['id']])
    board_result = run_once('BOARD_REGISTER_CONSOLIDATED_R57', [sys.executable, '-B', '-X', 'utf8',
        r'C:\IALD\PROGRAMA_IALD\iald.py', 'avancar', 'F1.FECHO_20261015', '--quem', s.ACTOR['id'],
        '--status', 'EM_CURSO', '--evidencia', str(delivery), '--nota',
        'R57: componentes revisados, 37 relatórios de axiomas/34 verificações simbólicas; oito memórias com backup. Ponte física R4/R5 ainda aberta.'])
    registration = s.new('REGISTRATION_CONSOLIDATED_R57.json', {'delivery': pin(delivery), 'map': pin(map_result), 'board': pin(board_result)})
    state, _ = s.call('session_memory.py', {'operation': 'get', 'reference': str(s.REFERENCE)}, 'FINAL_CUSTODY_GET')
    s.call('session_memory.py', {'operation': 'transition', 'reference': str(s.REFERENCE), 'actor': s.ACTOR,
        'expected_revision': state['revision'], 'event_id': 'r57-consolidated-material-custody-20261017',
        'changes': {'records': [{'id': 'r57-reviewed-components-custodied', 'kind': 'fact', 'statute': 'REAL',
            'sources': [{'kind': 'artifact', 'ref': str(p), 'sha256': pin(p)['sha256']} for p in [delivery, registration]],
            'text': 'R57: quatro componentes Lean,37 relatórios de axiomas no trio e34 verificações simbólicas; revisão independente com alcance. Oito apêndices com backups e registro mapa/quadro. R4/R5 integrais continuam abertos; inversão de fase apenas local e derivada no modelo finito, não Lean nesta rodada.'}],
            'flow': {'phase': 'r57_components_custodied_physical_bridge_open',
                'next_action': 'Revisão final da custódia; depois calcular forma de duas pontas dos observáveis físicos e comparar com circularSmear. Preservar calibração do relógio, limite de estados/dinâmica e R3/R10 pendentes.'}}}, 'FINAL_CUSTODY_TRANSITION')
    print(delivery)


if __name__ == '__main__':
    main()
