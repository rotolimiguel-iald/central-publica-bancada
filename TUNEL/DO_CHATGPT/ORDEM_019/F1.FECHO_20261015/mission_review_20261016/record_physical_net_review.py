"""Pin the bounded source review; inspect existing build receipts, never compile."""
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
from finish_requirement_reviews import OUT, BASE, REFERENCE, PYTHON, CLI, ACTOR, pin, fresh, read

def main():
    area = BASE / 'orbital_rotation'
    source = area / 'PhysicalCanonicalNetCompleteR1.lean'
    manifest = read(area / 'PhysicalCanonicalNetCompleteR1_SOURCE.json')
    assert pin(source)['sha256'] == manifest['sha256']
    for entry in manifest['reused_sources']:
        assert pin(entry['path'])['sha256'] == entry['sha256']
    attempt = area / 'attempts/20261016T120556_913253Z'
    start = read(attempt / 'START_RECEIPT.json')
    assert pin(start['source']['path'])['sha256'] == manifest['sha256']
    roots = [Path(x) for x in start['LEAN_PATH'].split(';')]
    imports = re.findall(r'^import (\S+)', source.read_text(encoding='utf-8'), re.M)
    imported = []
    for module in imports:
        rel = Path(*module.split('.')).with_suffix('.olean')
        paths = [root / rel for root in roots if (root / rel).is_file()]
        assert paths, module
        built = paths[0]
        info = {'module': module, 'resolved_olean': pin(built)}
        local_source = built.with_suffix('.lean')
        receipt_path = built.parent / 'RECEIPT.json'
        if receipt_path.exists() and local_source.exists():
            receipt = read(receipt_path)
            assert receipt['exit_code'] == 0, module
            checked = []
            for entry in [receipt['source']] + receipt['artifacts']:
                actual = pin(entry['path'])
                assert actual['sha256'] == entry['sha256'], entry['path']
                checked.append(actual)
            working = area / (module + '.lean')
            if module == 'CanonicalFockAssemblyR1':
                working = BASE / 'network_reuse/CanonicalFockAssemblyR1.lean'
            if working.exists():
                assert pin(working)['sha256'] == pin(local_source)['sha256'], module
                info['read_source_matches_build_copy'] = True
            info.update(receipt=pin(receipt_path), source=pin(local_source), checked_artifacts=checked,
                        prior_exit_code=0, whole_transitive_closure_reaudited=False)
        else:
            info['scope'] = 'Imported existing canonical object; no new compilation or complete transitive audit.'
        imported.append(info)

    names = [
        'PhysicalCompactNetCovarianceR1', 'PhysicalSymplecticPairingR7',
        'PhysicalFrameWedgeLocalityR2', 'PhysicalCompactNetGeometryR1',
        'PhysicalCanonicalWedgeEqualityR3', 'PhysicalWedgeSchwartzClosureR3',
        'GenericSymplecticSpanR2', 'PhysicalCompactPairLocalityR1',
        'SpacelikePairNeighborhoodR2', 'PhysicalOppositeWedgeR4',
        'PhysicalSmearTranslationR2', 'PhysicalSmearBoostR2', 'SpacelikePairWedgesR2',
        'PhysicalFockNetRealizationR1']
    read_sources = [source] + [area / (name + '.lean') for name in names] + [
        BASE / 'network_reuse/CanonicalFockAssemblyR1.lean',
        BASE / 'weyl_net_wiring/CanonicalModularCoreAssemblyR1.lean',
        BASE / 'kms_strip/attempts/20261016T034103_939807Z/PhysicalSmearDensityR6.lean',
        BASE / 'kms_strip/attempts/20261015T234935_821667Z/PhysicalSchwartzMaxwellR1.lean']
    lines = source.read_text(encoding='utf-8').splitlines()
    anchors = {name: next(i+1 for i, line in enumerate(lines) if re.search(r'\b' + name + r'\b', line))
        for name in ['physical_compact_spacelike_zero', 'shifted_compact_wedge_tsupport',
                     'wedge_smear_mem_compact', 'compactLocalized_rightWedge_eq',
                     'compactLocalized_locality', 'compactPhysicalNet_wedge_glue',
                     'physicalCanonicalNet', 'physical_canonical_net_zero_refused']}
    build = {'start_receipt': pin(attempt / 'START_RECEIPT.json'),
             'build_source': pin(start['source']['path']), 'pid_at_start': start['pid'],
             'new_builds_launched': 0, 'waits_or_process_polls': 0}
    terminal = attempt / 'RECEIPT.json'
    if terminal.exists():
        receipt = read(terminal)
        checked = []
        for entry in [receipt['source']] + receipt['artifacts']:
            actual = pin(entry['path'])
            assert actual['sha256'] == entry['sha256'], entry['path']
            checked.append(actual)
        text = (attempt / 'AXIOMS.txt').read_text(encoding='utf-8') if (attempt / 'AXIOMS.txt').exists() else ''
        entries = re.findall(r"'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]", text)
        own = {name: [a.strip() for a in value.split(',') if a.strip()] for name,value in entries
               if name.startswith('F1Fecho.MaxwellLocalization.')}
        expected = re.findall(r'^#print axioms (\S+)', source.read_text(encoding='utf-8'), re.M)
        clean = len(own) >= len(expected) and all(name in own for name in expected)
        clean = clean and all(set(values) <= {'propext','Classical.choice','Quot.sound'} for values in own.values())
        build.update(status='TERMINAL_RECEIPT_INSPECTED', receipt=pin(terminal),
                     exit_code=receipt['exit_code'], checked_artifacts=checked,
                     own_axioms=own, expected_prints=expected, clean_expected_prints=clean)
        compiled = receipt['exit_code'] == 0 and clean
    else:
        build.update(status='PENDING_NO_TERMINAL_RECEIPT_AT_REVIEW',
                     running_output_bytes=(attempt / 'RUNNING_OUTPUT.log').stat().st_size,
                     compilation_verified=False)
        compiled = False
    proc = subprocess.run([PYTHON,'-B','-X','utf8',CLI],
        input=json.dumps({'operation':'project','reference':str(REFERENCE),'max_chars':60000}),
        capture_output=True,text=True,encoding='utf-8',check=True)
    sync = json.loads(proc.stdout)
    assert sync['ok']
    p = sync['result']['projection']
    assert p['context_id'] == read(REFERENCE)['context_id']
    fresh(OUT / 'PHYSICAL_GLOBAL_NET_POST_REVIEW_PROJECT.json', sync)
    report = {
        'unit': 'F1.FECHO_20261015', 'reviewer': ACTOR,
        'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'mission_reference': pin(REFERENCE), 'project_before_revision_observed': 17,
        'project_after': pin(OUT / 'PHYSICAL_GLOBAL_NET_POST_REVIEW_PROJECT.json'),
        'project_after_revision': p['revision'],
        'task_statuses': {t['id']:t['status'] for t in p['active']+p['settled'] if t['id'] in {'R5','R6'}},
        'verdict': 'PASS_BOUNDED_SOURCE_REVIEW' if compiled else 'PASS_SOURCE_REVIEW_PENDING_COMPILATION',
        'accept_performed': False, 'source': pin(source),
        'source_manifest': pin(area / 'PhysicalCanonicalNetCompleteR1_SOURCE.json'),
        'source_lines': anchors, 'read_sources': [pin(q) for q in read_sources],
        'resolved_direct_imports': imported, 'build': build,
        'findings': [],
        'criterion_checks': [
            {'item':'compactLocalized por testes Maxwell reais','result':'PASS_SOURCE',
             'reason':'compactSupportedGenerators exige IsRealTest, suporte compacto e tsupport contido na região. Usa circularSmear = circularH1.symm composed with physicalSmearCLM, no mesmo H1. physicalSmearCLM vem do Fourier físico e contração Maxwell; não de uma escolha arbitrária de subespaços.'},
            {'item':'localidade causal sem premissa acrescentada','result':'PASS_SOURCE',
             'reason':'compact_pair_zero tem hipótese local genérica, descarregada por physical_frame_test_pair_zero. Cunhas opostas vêm da geometria de cada par spacelike e do transporte unitário da dualidade física. Partições finitas reais cobrem suportes compactos; closed_spans_zero estende a ortogonalidade aos fechos reais. Não há hipótese global de localidade no consumidor.'},
            {'item':'comparação da cunha compacta com KWR','result':'PASS_SOURCE',
             'reason':'cutoff preserva suporte/realidade; deslocamento espacial positivo coloca o suporte fechado na cunha aberta; continuidade de circularSmear e U1 remove cutoff e deslocamento. Obtém compactLocalized=localized na cunha e compõe com physical_right_wedge_eq_KWR. A densidade global usada por esse último é fornecida por perfil compacto fora do eixo e tensor dual explícito em PhysicalSmearDensityR6.'},
            {'item':'exclusão da rede nula','result':'PASS_SOURCE',
             'reason':'physicalCanonicalNet recebe wedge_glue provado. canonical_wedge_nonzero transporta o vetor não nulo de spectralOutput; zero_wedge_refused contradiz a hipótese de cunha igual a bottom. Não se acrescenta premissa de não nulidade.'},
            {'item':'covariância','result':'PASS_SOURCE_WITH_SCOPE',
             'reason':'Translações e boosts B0 são ligados na estrutura LightNetData; o módulo de covariância conserva ainda o resultado para generatedLorentz. A presente revisão não substitui R5 por esses campos nem certifica dispositivo ou grupo externo mais amplo só pelo nome.'}
        ],
        'optional_fock_source_review': {
            'source':pin(area / 'PhysicalFockNetRealizationR1.lean'),
            'status':'READ_ONLY_NOT_COMPILED_BY_THIS_REVIEW',
            'assessment':'Composição coerente por leitura: net O = FieldWeyl.R(physicalCanonicalNet.K O); CCR, geradores, regularidade e covariância usam o mesmo Fock. net_wedge_eq transfere ciclicidade, separação, não comutatividade, KMS e realização Tomita para KWR. canonicalFockJ conserva oneParticle e vácuo. O arquivo não exige RemainingModularCoreInput ou traço/PF para esses teoremas.',
            'limit':'Leitura do consumidor e da montagem modular importada; não é nova auditoria de todos os teoremas transitivos, não prova compilação deste novo arquivo e não aceita R6.'
        },
        'limitations': [
            'Rede de Maxwell livre em Minkowski, com separação estritamente spacelike; não é realização de dispositivo.',
            'Não identifica por definição a rede compacta com a antiga rede Schwartz em todas as regiões; a igualdade demonstrada aqui é da cunha direita.',
            'H3 curvo em todas as direções, fonte de matéria/certificado Maxwell conjunto, traço/PF e obrigações restantes mantêm critérios próprios.',
            'Sem recibo terminal válido, leitura favorável não equivale a compilação; silêncio ou ausência de PID não permite inferir sucesso/falha.',
            'Nenhum aceite R5/R6, alteração de ciência/produção, gate, quadro, memória global ou chamada de provedor.'
        ], 'script':pin(__file__)
    }
    fresh(OUT / 'PHYSICAL_GLOBAL_NET_REVIEW_R1.json', report)
    print(json.dumps({'report':pin(OUT / 'PHYSICAL_GLOBAL_NET_REVIEW_R1.json'),
        'verdict':report['verdict'], 'direct_imports':len(imported), 'read_sources':len(read_sources),
        'build_status':build['status'], 'project_after_revision':p['revision']},ensure_ascii=False))

if __name__ == '__main__':
    main()
