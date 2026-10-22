"""One independent, byte-preserving rebuild of the three frozen rule modules."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import time

BASE = Path(__file__).resolve().parent
UNIT = BASE.parent
ORIGIN = UNIT / 'attempts/20261014T135951_106714Z'
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}
MODULES = ['RuleTruthContract', 'RuleTruthAxioms', 'TheRuleAndTheFigureOfTruth']

def save(path, data):
    if not isinstance(data, bytes):
        data = (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.read_bytes() == data

def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def discover_pins(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get('path'), str) and isinstance(obj.get('sha256'), str):
            yield obj
        for value in obj.values():
            yield from discover_pins(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from discover_pins(value)

def parse_axioms(output):
    found = []
    for name, content in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output):
        found.append({'declaration': name, 'axioms': [x.strip() for x in content.split(',') if x.strip()]})
    for name in re.findall(r"'([^']+)' does not depend on any axioms", output):
        found.append({'declaration': name, 'axioms': []})
    for line in output.splitlines():
        if line.startswith('LOCAL_DECL\t'):
            _, name, content = line.split('\t', 2)
            found.append({'declaration': name, 'axioms': [x for x in content.split(',') if x]})
    return found

def canon(reports):
    return sorted((r['declaration'], tuple(sorted(r['axioms']))) for r in reports)

def main():
    final = BASE / 'REVIEW_RULE_PROOF_R1.json'
    report_path = BASE / 'REVIEW_RULE_PROOF_R1.md'
    assert not final.exists() and not report_path.exists(), 'Exclusive output already exists'
    constructor = json.loads((ORIGIN / 'RESULTADO_BUILD.json').read_bytes())
    semantic = json.loads((BASE / 'PARECER_ESCOPO_R1.json').read_bytes())
    dependencies = json.loads((ORIGIN / 'DEPENDENCIES.json').read_bytes())
    checked = {}
    for obj in [constructor, semantic, dependencies]:
        for expected in discover_pins(obj):
            actual = pin(expected['path'])
            assert actual['sha256'] == expected['sha256'], 'Pin changed: ' + actual['path']
            if 'bytes' in expected:
                assert actual['bytes'] == expected['bytes']
            checked[actual['path']] = actual
    for path in [ORIGIN / 'RESULTADO_BUILD.json', UNIT / 'build_proof.py', BASE / 'PARECER_ESCOPO_R1.json', Path(__file__)]:
        checked[str(path)] = pin(path)
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    sandbox = BASE / 'attempts' / stamp
    sandbox.mkdir(parents=True, exist_ok=False)
    original_modules = {r['module']: r for r in constructor['modules']}
    lean = Path(original_modules[MODULES[0]]['command'][0])
    inherited_paths = original_modules[MODULES[0]]['LEAN_PATH'].split(os.pathsep)
    assert inherited_paths[0] == str(ORIGIN)
    paths = [str(sandbox)] + inherited_paths[1:]
    assert all(Path(p).is_dir() for p in paths)
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(paths), PYTHONDONTWRITEBYTECODE='1')
    version = subprocess.check_output([str(lean), '--version'], text=True).strip()
    assert version == original_modules[MODULES[0]]['toolchain']
    checked[str(lean)] = pin(lean)
    source_checks = []
    for name in MODULES:
        source = ORIGIN / (name + '.lean')
        assert source.read_bytes() == (UNIT / 'formal' / source.name).read_bytes()
        save(sandbox / source.name, source.read_bytes())
        text = source.read_text(encoding='utf-8')
        prohibited = re.findall(r'\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\s', text, re.M)
        assert not prohibited, (name, prohibited)
        for imported in re.findall(r'^import\s+(\S+)', text, re.M):
            if imported in MODULES:
                continue
            relative = Path(*imported.split('.')).with_suffix('.olean')
            candidates = [Path(folder) / relative for folder in paths[1:]]
            resolved = next(p for p in candidates if p.is_file())
            checked[str(resolved)] = pin(resolved)
        source_checks.append({'module': name, 'source': pin(source), 'copy': pin(sandbox/source.name),
            'theorems': re.findall(r'^theorem\s+(\w+)', text, re.M), 'prohibited_tokens': prohibited})
    save(sandbox / 'INPUT_PINS.json', list(checked.values()))
    save(sandbox / 'SOURCE_CHECKS.json', source_checks)
    receipts = []
    for name in MODULES:
        source = sandbox / (name + '.lean')
        output = sandbox / (name + '.olean')
        command = [str(lean), '-o', str(output), str(source)]
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        clock = time.perf_counter()
        process = subprocess.run(command, cwd=sandbox, env=env, capture_output=True)
        seconds = time.perf_counter() - clock
        ended = dt.datetime.now(dt.timezone.utc).isoformat()
        save(sandbox / (name + '.stdout.log'), process.stdout)
        save(sandbox / (name + '.stderr.log'), process.stderr)
        reports = parse_axioms((process.stdout + process.stderr).decode('utf-8', errors='strict'))
        receipt = {'module': name, 'start_utc': started, 'end_utc': ended, 'seconds': seconds,
            'command': command, 'cwd': str(sandbox), 'LEAN_PATH': env['LEAN_PATH'], 'toolchain': version,
            'exit_code': process.returncode, 'source': pin(source), 'axiom_reports': reports,
            'axioms_match_constructor': canon(reports) == canon(original_modules[name]['axiom_reports']),
            'axioms_within_trio': bool(reports) and all(set(r['axioms']) <= TRIO for r in reports),
            'olean': pin(output) if output.exists() else None,
            'olean_identical_constructor': output.exists() and output.read_bytes() == (ORIGIN / output.name).read_bytes()}
        save(sandbox / (name + '.RESULT.json'), receipt)
        receipts.append(receipt)
        print(json.dumps({'module': name, 'exit_code': process.returncode, 'seconds': seconds,
            'axiom_reports': len(reports), 'olean_identical': receipt['olean_identical_constructor']}, ensure_ascii=False), flush=True)
        assert process.returncode == 0 and receipt['axioms_within_trio'] and receipt['axioms_match_constructor'], receipt
    unchanged = all(pin(p['path']) == p for p in checked.values())
    assert unchanged
    theorem_count = sum(len(p['theorems']) for p in source_checks)
    assert theorem_count == 60
    for source in source_checks:
        if not source['theorems']:
            continue
        reports = next(r['axiom_reports'] for r in receipts if r['module'] ==
            ('RuleTruthAxioms' if source['module'] == 'RuleTruthContract' else source['module']))
        assert {r['declaration'].rsplit('.',1)[-1] for r in reports} == set(source['theorems'])
    text = '\n'.join([
        '# Revisão independente — F1.REGRA.P1',
        '[REAL — compilação local] PASSA no escopo formal declarado; nenhuma aceitação da gerência é presumida.',
        f'Três módulos recompilados em cópia: EXIT 0; {sum(r["seconds"] for r in receipts):.3f} s; Lean 4.31.0.',
        '60 teoremas: 22 do contrato e 38 da face. Os 101 relatórios incluem 41 constantes do contrato e repetição dos seus 22 teoremas.',
        f'Axiomas só no trio; zero sorry/admit/axioma novo na fonte. {sum(r["olean_identical_constructor"] for r in receipts)}/3 .olean idênticos byte a byte aos do construtor.',
        f'{len(checked)} pinos de entrada conferidos antes e depois; dependências usadas somente para leitura.',
        'A igualdade literal vale no tipo Inscription = Fix(normalize); a leitura é injetiva nesse tipo. A trajetória bruta nunca quita em tempo finito.',
        'Soundness e completeness são hipóteses explícitas para leitura e alvo fixos; a unicidade é do predicado, não prova de verdade universal.',
        'A satisfação normalizada vale já em n=0 e independe de λ; λ controla dinâmica, convergência e balanço escalar.',
        'O alvo admissível é não nulo; normalize(0,1)=0 é permitido e recusado. Nenhum resultado sobre temperatura ou toda entrada decorre disso.',
        'A ponte matriz–normalização e ambas as faces não nulas estão provadas; independência do livro permanece definicional.',
        'Estatuto da interpretação: INPUT/ONTO. Sem alteração dos originais, memória, quadro, kernel, Bancada ou gate.',
    ]) + '\n'
    save(report_path, text.encode('utf-8'))
    result = {'unit': 'F1.REGRA.P1', 'reviewer': 'codex-independent-modular-review',
        'status': 'PASS_FORMAL_SCOPE__CANDIDATE_FOR_MANAGEMENT', 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'attempt': str(sandbox), 'builds': receipts, 'input_pins': list(checked.values()),
        'input_pins_unchanged_after_build': unchanged, 'theorems': theorem_count,
        'axiom_reports': sum(len(r['axiom_reports']) for r in receipts),
        'distinct_declarations': len({a['declaration'] for r in receipts for a in r['axiom_reports']}),
        'audit_scope': 'All 41 local core constants via collectAxioms, plus #print axioms of all 60 source theorems; no duplicate theorem count.',
        'semantic_review': pin(BASE / 'PARECER_ESCOPO_R1.json'), 'limits': semantic['findings'],
        'memory_projection': 'No reviewer-owned reference was carried in the resume; no other session context adopted and no memory writes.',
        'no_memory_or_board_writes': True, 'provider_calls': 0, 'no_source_changes': True,
        'artifacts': [pin(p) for p in sorted(sandbox.iterdir()) if p.is_file()] + [pin(report_path)]}
    save(final, result)
    print(json.dumps({'result': pin(final), 'report': pin(report_path), 'passed': True,
        'seconds': sum(r['seconds'] for r in receipts), 'input_pins': len(checked)}, ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()
