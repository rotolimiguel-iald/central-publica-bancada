"""R2: verify the actual isolated v394 consumer against freshly compiled Lean evidence.

This is an incremental verification, not a whole-rite rerun or a new seal.
Run only after ROOT_AUDIT.json has completed. Never imports the canonical um.py.
All output is new; an audit hook forbids network, processes and external writes.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import copy
import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import sys
import time
import traceback

UNIT = Path(__file__).resolve().parents[1]
HERE = UNIT / 'verification'
CANON = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}
MODE = 'INCREMENTAL_DIRECT_LEAN_ROOT_AUDIT_WITH_PINNED_BASELINE_CACHE'
AUDIT_EVENTS = []


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    path = Path(path)
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
            size += len(block)
    return {'path': str(path), 'bytes': size, 'sha256': h.hexdigest()}


def load(path):
    return json.loads(Path(path).read_bytes())


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def new(path, value):
    path = Path(path)
    data = value.encode('utf-8') if isinstance(value, str) else json.dumps(
        value, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8')
    require(not path.exists(), 'Immutable output already exists: ' + str(path))
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    require(temp.read_bytes() == data, 'Temporary output differs')
    # Windows rename refuses an existing destination; never replace an old artifact.
    temp.rename(path)
    return pin(path)


def verify_pin(record):
    got = pin(record['path'])
    require(got['sha256'] == record['sha256'], 'Pin differs: ' + record['path'])
    if 'bytes' in record:
        require(got['bytes'] == record['bytes'], 'Size differs: ' + record['path'])
    return got


def audit_hook(event, args):
    if event.startswith(('socket.', 'subprocess.', 'urllib.')) or event in (
        'os.system', 'os.posix_spawn', 'os.posix_spawnp', 'os.fork', 'os.forkpty',
        'os.exec', 'os.spawn', 'os.startfile', 'os.startfile/2'):
        AUDIT_EVENTS.append({'event': event, 'blocked': True})
        raise PermissionError('Verification audit hook blocks ' + event)
    targets = []
    if event == 'open':
        path, mode, flags = args
        writes = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writes and not isinstance(path, int):
            targets.append(path)
    elif event in ('os.rename', 'os.replace', 'os.link', 'os.symlink'):
        targets.extend(args[:2])
    elif event in ('os.mkdir', 'os.remove', 'os.rmdir', 'os.chmod', 'os.chown', 'os.utime', 'os.truncate'):
        targets.append(args[0])
    for target in targets:
        if isinstance(target, int):
            raise PermissionError('Descriptor-based mutation is not allowed')
        resolved = Path(os.fsdecode(target)).resolve()
        if not resolved.is_relative_to(UNIT):
            AUDIT_EVENTS.append({'event': event, 'path': str(resolved), 'blocked': True})
            raise PermissionError('External write blocked: ' + str(resolved))
        AUDIT_EVENTS.append({'event': event, 'path': str(resolved), 'blocked': False})


def parse_axioms(text):
    # Same public-name grammar as the actual um.py parser; quoted private names
    # are counted separately by the existing complete-coverage consumer.
    axioms = {}
    for name, values in re.findall(r"'([\w.']+)' depends on axioms:\s*\[([^\]]*)\]", text, re.S):
        parsed = [x.strip() for x in values.split(',') if x.strip()]
        require(name not in axioms or axioms[name] == parsed, 'Conflicting axiom rows: ' + name)
        axioms[name] = parsed
    for name in re.findall(r"'([\w.']+)' does not depend on any axioms", text):
        require(name not in axioms or axioms[name] == [], 'Conflicting axiom-free row: ' + name)
        axioms[name] = []
    return axioms


def lean_code_without_comments(text):
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i + 2]
        if depth:
            if pair == '/-': depth += 1; i += 2; continue
            if pair == '-/': depth -= 1; i += 2; continue
            out.append('\n' if text[i] == '\n' else ' '); i += 1; continue
        if string:
            if text[i] == '\\': i += 2; continue
            if text[i] == '"': string = False
            out.append(' '); i += 1; continue
        if pair == '/-': depth = 1; i += 2; continue
        if pair == '--':
            end = text.find('\n', i)
            if end < 0: break
            out.append('\n'); i = end + 1; continue
        if text[i] == '"': string = True; out.append(' '); i += 1; continue
        out.append(text[i]); i += 1
    require(depth == 0 and not string, 'Unclosed Lean comment/string')
    return ''.join(out)


def build_evidence(module, attempt, baseline):
    formal = UNIT / 'formal_verified'
    root = load(formal / 'ROOT_AUDIT.json')
    manifest = load(formal / 'FORMAL_MANIFEST.json')
    cache = load(formal / 'CACHE_RECEIPT.json')
    require(root['passed'] is True and manifest['passed'] is True, 'Lean evidence is not passed')
    require(len(root['results']) == 2 and len(manifest['modules']) == 4, 'Unexpected module coverage')
    records = manifest['modules'] + root['results']
    record_reports, fresh = {}, []
    for record in records:
        require(record['exit_code'] == 0, 'Lean build exit is nonzero')
        require(record['start_utc'] and record['end_utc'] and record['seconds'] >= 0, 'Incomplete real build timing')
        require('4.31.0' in record['toolchain'], 'Wrong Lean toolchain')
        require(record['command'] and record['LEAN_PATH'], 'Missing command/LEAN_PATH')
        for key in ('source', 'stdout', 'stderr', 'olean'):
            verify_pin(record[key])
        source = Path(record['source']['path']).read_text(encoding='utf-8')
        relative = record['relative']
        require(module._EMBEDDED_KERNEL_FILES.get(relative) == source, 'Embedded and compiled source differ: ' + relative)
        require(pin(UNIT / 'candidate/tgl_kernel' / relative)['sha256'] == record['source']['sha256'], 'Materialized source differs')
        if record in manifest['modules']:
            code = lean_code_without_comments(source)
            require(not re.search(r'\b(?:sorry|admit)\b|(?m:^\s*(?:private\s+)?axiom\s+)', code), 'New source has placeholder/custom axiom')
        text = Path(record['stdout']['path']).read_text(encoding='utf-8')
        parsed = parse_axioms(text)
        require((bool(parsed) or record['module'] == 'TGLExt') and all(set(a) <= TRIO for a in parsed.values()), 'Axiom rows absent or outside trio')
        receipt_rows = record['axiom_report']
        for name in set(parsed) & set(receipt_rows):
            require(receipt_rows[name] == parsed[name], 'Receipt disagrees with actual Lean output')
        # The build-receipt parser excludes names containing an apostrophe; the
        # actual um.py parser includes them but excludes guillemet-quoted names.
        require(all("'" in name for name in set(parsed) - set(receipt_rows)), 'Unexpected missing receipt row')
        require(all('«' in name or '»' in name for name in set(receipt_rows) - set(parsed)), 'Unexpected extra receipt row')
        receipt_grammar = {}
        for name, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", text, re.S):
            receipt_grammar[name] = [x.strip() for x in values.split(',') if x.strip()]
        for name in re.findall(r"'([^']+)' does not depend on any axioms", text):
            receipt_grammar[name] = []
        require(receipt_grammar == receipt_rows, 'Receipt parser reconstruction failed')
        record_reports[record['module']] = (text, parsed)
        fresh.append({'module': record['module'], 'source': record['source'], 'stdout': record['stdout'],
                      'olean': record['olean'], 'command': record['command'], 'LEAN_PATH': record['LEAN_PATH'],
                      'start_utc': record['start_utc'], 'end_utc': record['end_utc'], 'seconds': record['seconds'],
                      'exit_code': record['exit_code'], 'parsed_axioms': len(parsed),
                      'receipt_parser_axioms': len(receipt_rows),
                      'additional_apostrophe_names': sorted(set(parsed) - set(receipt_rows)),
                      'excluded_quoted_names': sorted(set(receipt_rows) - set(parsed))})
    text, axioms = record_reports['TGL.Audit']
    coverage = module._v392_axiom_coverage(text, axioms)
    require(coverage.get('ok') is True, 'Whole imported-closure axiom coverage failed: ' + repr(coverage))
    required = module._V394_FORMAL_CONTRACT['theorems']
    require(len(required) == 108 and all(n in axioms and set(axioms[n]) <= TRIO for n in required), 'New theorem coverage failed')
    for record in manifest['modules']:
        for theorem, values in record['axiom_report'].items():
            require(axioms.get(theorem) == values, 'Root audit differs from fresh module: ' + theorem)
    # Baseline cached imports are byte copies. Only the two rebuilt aggregators differ.
    replaced = {Path(r['relative']).with_suffix('.olean').as_posix() for r in root['results']}
    cache_checks = []
    for entry in cache['entries']:
        relative = Path(entry['relative'])
        original = Path(cache['source']) / relative
        copied = Path(cache['destination']) / relative
        require(not original.is_symlink() and not copied.is_symlink(), 'Cache link refused')
        require(not os.path.isjunction(original) and not os.path.isjunction(copied), 'Cache junction refused')
        require(pin(original)['sha256'] == entry['sha256'], 'Canonical cache pin differs')
        if relative.as_posix() not in replaced:
            require(pin(copied)['sha256'] == entry['sha256'], 'Copied cache differs: ' + str(relative))
        cache_checks.append({'relative': str(relative), 'baseline_sha256': entry['sha256'],
                             'rebuilt_aggregator': relative.as_posix() in replaced})
    new(attempt / 'CACHE_CHECKS.json', cache_checks)
    kf = {
        'formal_checker': 'Lean 4', 'build_tool': 'direct Lean against pinned copied imports',
        'verification_mode': MODE, 'mode': 'incremental-direct',
        'formal_dir': str(UNIT / 'candidate/tgl_kernel'), 'lean_version': records[-1]['toolchain'],
        'toolchain_pinned': True, 'lake_build_ok': False, 'full_lake_build_performed': False,
        'whole_rite_rerun': False, 'historical_baseline': baseline['copy'],
        'all_verified_scope': 'Six fresh direct Lean compilations, closure axiom enumeration and pinned cached dependencies. Not a full Lake build.',
        'axiom_report': axioms, 'axiom_coverage_v392': coverage,
        'audit_file_ok': True, 'source_forbidden_tokens_absent': True,
        'source_scan_scope': 'four new modules; baseline sources verified by bytes',
        'sorryAx_absent': all('sorryAx' not in a for a in axioms.values()),
        'trustCompiler_absent': all('Lean.trustCompiler' not in a for a in axioms.values()),
        'custom_TGL_axioms_absent': all(set(a) <= TRIO for a in axioms.values()),
        'fresh_builds': fresh, 'cache_receipt': pin(formal / 'CACHE_RECEIPT.json'),
        'root_audit_receipt': pin(formal / 'ROOT_AUDIT.json'),
        'fresh_manifest': pin(formal / 'FORMAL_MANIFEST.json'),
        'formal_files_sha256': {r['relative']: r['source']['sha256'] for r in records},
        'all_verified': True, 'verdict': 'INCREMENTAL_FORMAL_COMPOSITION_VERIFIED__NOT_FULL_LAKE_BUILD',
    }
    origins = {}
    mappings = [('_LEAN_THEOREM_FLAGS', ''), ('_QG_CERTIFICATE_FLAGS', 'qgc_'),
                ('_QG_FRONTIER_FLAGS', 'qgf_'), ('_QG_PHYSICS_FLAGS', 'qgp_'),
                ('_GRAVITY_PRICE_FLAGS', 'gpf_'), ('_REDUCTION_FLAGS', 'red_'),
                ('_GRAVITY_IMPORT_FLAGS', 'gpi_'), ('_GRAVITY_CITATION_FLAGS', 'gpc_')]
    for map_name, prefix in mappings:
        for key, theorem in getattr(module, map_name).items():
            value = axioms.get(theorem)
            kf[prefix + key] = isinstance(value, list) and set(value) <= TRIO
            origins[prefix + key] = {'theorem': theorem, 'present': theorem in axioms, 'axioms': value,
                                    'source': records[-1]['stdout']['sha256'], 'mapping': map_name}
    new(attempt / 'FLAG_ORIGINS.json', origins)
    return kf


@contextlib.contextmanager
def changed_global(module, name, value):
    old = getattr(module, name)
    setattr(module, name, value)
    try:
        yield
    finally:
        setattr(module, name, old)


def negative_controls(module, core):
    results = []
    def refused(name, candidate_core):
        result = module.tempo_frequencia_v394(candidate_core)
        ok = result.get('all_verified') is False and result.get('runtime_executed') is False
        results.append({'name': name, 'refused_before_runtime': ok, 'verdict': result.get('verdict')})
        require(ok, 'Negative control accepted: ' + name)
    theorem = module._V394_FORMAL_CONTRACT['theorems'][0]
    for label, value in [('absent', None), ('sorryAx', ['sorryAx']), ('custom', ['Invented.axiom']), ('wrong_type', True)]:
        c = copy.deepcopy(core)
        if value is None: c['kernel_formalization']['axiom_report'].pop(theorem)
        else: c['kernel_formalization']['axiom_report'][theorem] = value
        refused('axioms_' + label, c)
    c = copy.deepcopy(core); c['kernel_formalization']['all_verified'] = False
    refused('formal_not_verified', c)
    for name, value in [('n_theorems_clean', 7152), ('n_theorems_expected', 7152), ('n_theorems_clean', True)]:
        c = copy.deepcopy(core); c['external_ladder'][name] = value
        refused('ladder_' + name + '_' + repr(value), c)
    c = copy.deepcopy(core); c['external_ladder'] = {}
    refused('ladder_absent', c)
    rel = next(iter(module._V394_FORMAL_CONTRACT['source_sha256']))
    for label, transform in [('absent', lambda d: d.pop(rel)), ('changed', lambda d: d.__setitem__(rel, d[rel] + '\n'))]:
        embedded = dict(module._EMBEDDED_KERNEL_FILES); transform(embedded)
        with changed_global(module, '_EMBEDDED_KERNEL_FILES', embedded):
            refused('embedded_source_' + label, copy.deepcopy(core))
    contract = copy.deepcopy(module._V394_FORMAL_CONTRACT)
    contract['source_sha256'][rel] = '0' * 64
    with changed_global(module, '_V394_FORMAL_CONTRACT', contract):
        refused('source_pin_changed', copy.deepcopy(core))
    inscriptions = copy.deepcopy(module._V394_INSCRIPTIONS)
    next(iter(inscriptions.values()))['text'] += ' altered'
    with changed_global(module, '_V394_INSCRIPTIONS', inscriptions):
        refused('inscription_changed', copy.deepcopy(core))
    c = copy.deepcopy(core)
    flag = next(k for k in module._LEAN_THEOREM_FLAGS if k.startswith('ext_tf394_'))
    c['kernel_formalization'][flag] = False
    c['external_ladder'] = module.prove_external_ladder(1, c['kernel_formalization'])
    require(c['external_ladder']['n_theorems_clean'] == 7152, 'Real ladder did not consume missing flag')
    refused('real_ladder_missing_flag', c)
    return results


def label_articles(attempt, raw_paths, provenance):
    artifacts = []
    for language, paths in raw_paths.items():
        heading = ('VERIFICACAO INCREMENTAL DA COPIA V394; NAO E NOVO RITO NEM SELO.\n'
                   'Capitulos e dados anteriores foram reaproveitados do core historico v393.\n'
                   'Novos nesta execucao: auditoria Lean incremental, escada, regra v393 e consumidor tempo/frequencia v394.\n'
                   if language == 'pt' else
                   'INCREMENTAL VERIFICATION OF THE V394 COPY; NOT A NEW RITE OR SEAL.\n'
                   'Earlier chapters and results reuse the historical v393 core.\n'
                   'Fresh here: incremental Lean audit, ladder, v393 rule and v394 time/frequency consumer.\n')
        for raw in paths:
            raw = Path(raw); text = raw.read_text(encoding='utf-8')
            if raw.suffix == '.tex':
                require(text.count(r'\begin{document}') == 1, 'Ambiguous TeX document boundary')
                notice = '\n\\section*{' + heading.splitlines()[0].replace(';', ':') + '}\n' + '\n\n'.join(heading.splitlines()[1:]) + '\n'
                labeled = text.replace(r'\begin{document}', r'\begin{document}' + notice, 1)
            else:
                labeled = heading + '\n' + text
            destination = attempt / ('INCREMENTAL_' + raw.name)
            artifacts.append({'raw_real_emit_article': pin(raw), 'labeled_derivative': new(destination, labeled),
                              'label_transformation': 'Only added visible provenance notice; original generated bytes retained.',
                              'baseline': provenance})
    return artifacts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', required=True)
    parser.add_argument('--candidate', type=Path, default=UNIT / 'candidate/um.py')
    args = parser.parse_args()
    require(sys.dont_write_bytecode, 'Launch with -B; no bytecode writes allowed')
    require((UNIT / 'formal_verified/ROOT_AUDIT.json').is_file(), 'Wait for root audit completion; do not poll')
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    attempt = HERE / ('run_' + stamp)
    attempt.mkdir()
    start, tick = utc(), time.perf_counter()
    receipt = {'start_utc': start, 'command': [sys.executable, '-B', '-X', 'utf8', *sys.argv],
               'cwd': os.getcwd(), 'verification_mode': MODE, 'whole_rite_rerun': False,
               'full_lake_build_performed': False, 'new_seal_created': False, 'attempt': str(attempt),
               'script': pin(__file__), 'passed': False}
    protected, before, captured = [], {}, io.StringIO()
    status = 1
    try:
        sys.addaudithook(audit_hook)
        baseline = load(UNIT / 'SOURCE_BASELINE.json')
        integration = load(UNIT / 'INTEGRATION_R1.json')
        candidate = args.candidate.resolve()
        require(candidate.is_relative_to(UNIT), 'Only an isolated candidate inside this unit may be imported')
        if candidate == (UNIT / 'candidate_r2/um.py').resolve():
            revision = load(UNIT / 'INTEGRATION_R2_INSCRIPTION.json')
            verify_pin(revision['candidate_R2'])
            require(Path(revision['candidate_R2']['path']).resolve() == candidate, 'Candidate path mismatch')
            receipt['inscription_revision'] = pin(UNIT / 'INTEGRATION_R2_INSCRIPTION.json')
        else:
            require(candidate == (UNIT / 'candidate/um.py').resolve(), 'Unregistered candidate path')
            verify_pin(integration['candidate'])
        # Safe audit-hook probes emit audit events only; no I/O or child process.
        hook_probes = [('socket.connect', (None, None)), ('subprocess.Popen', (None, [], None, None)),
                       ('open', (str(UNIT.parent / 'BLOCKED_WRITE_PROBE'), 'w', os.O_WRONLY | os.O_CREAT))]
        for event, event_args in hook_probes:
            try:
                sys.audit(event, *event_args)
            except PermissionError:
                pass
            else:
                raise RuntimeError('Audit hook failed its safe probe: ' + event)
        receipt['audit_hook_safe_probes_passed'] = len(hook_probes)
        for record in baseline['copied']:
            verify_pin(record['source']); verify_pin(record['copy'])
            protected.extend((record['source']['path'], record['copy']['path']))
        for record in baseline['embedded_materialized']:
            path = CANON / 'tgl_kernel' / record['relative']
            require(pin(path)['sha256'] == record['candidate']['sha256'], 'Canonical source changed since baseline')
            protected.append(str(path))
        protected.append(str(candidate))
        protected.extend(str(p) for p in (UNIT / 'candidate/tgl_kernel').rglob('*') if p.is_file())
        before = {p: pin(p) for p in sorted(set(protected))}
        new(attempt / 'PINS_BEFORE.json', before)
        receipt['integration'] = pin(UNIT / 'INTEGRATION_R1.json')
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            spec = importlib.util.spec_from_file_location('isolated_um_v394', candidate)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            require(module.UM_VERSION == 'v394', 'Candidate version is not v394')
            baseline_record = next(x for x in baseline['copied'] if Path(x['copy']['path']).name == 'um_absoluto.json')
            kf = build_evidence(module, attempt, baseline_record)
            new(attempt / 'KERNEL_FORMALIZATION_INCREMENTAL.json', kf)
            historical = load(baseline_record['copy']['path'])
            core = copy.deepcopy(historical['core'])
            core['kernel_formalization'] = kf
            core['external_ladder'] = module.prove_external_ladder(1, kf)
            ladder = core['external_ladder']
            require(ladder['all_verified'] is True and ladder['n_theorems_clean'] == ladder['n_theorems_expected'] == 7153, 'Actual external ladder failed')
            new(attempt / 'EXTERNAL_LADDER_ACTUAL.json', ladder)
            rule = module.regra_v393(core)
            new(attempt / 'REGRA_V393_ACTUAL.json', rule)
            require(all(v.get('all_verified') is True for v in rule.values()), 'Existing rule consumers failed')
            result = module.tempo_frequencia_v394(core)
            new(attempt / 'TIME_FREQUENCY_ACTUAL.json', result)
            require(result.get('all_verified') is True and result.get('runtime_executed') is True, 'Actual v394 consumer failed')
            negatives = negative_controls(module, core)
            new(attempt / 'NEGATIVE_CONTROLS.json', negatives)
            refreshed = ['kernel_formalization', 'external_ladder', *rule, 'tempo_frequencia_v394']
            unchanged = [k for k in historical['core'] if k not in refreshed]
            require(all(core[k] == historical['core'][k] for k in unchanged), 'A historical core field changed unexpectedly')
            provenance = {'baseline': baseline_record['copy'], 'baseline_timestamp': historical.get('timestamp'),
                          'historical_core_fields_not_recomputed': unchanged, 'fresh_core_fields': refreshed,
                          'historical_verdict_reused': True, 'gate_changed': False, 'whole_rite_rerun': False,
                          'formal_scope': MODE, 'observed_data_opened': False}
            new(attempt / 'PROVENANCE.json', provenance)
            new(attempt / 'CORE_INCREMENTAL.json', {'core': core, 'verdict': historical['verdict'], 'provenance': provenance})
            articles = attempt / 'articles_raw'
            articles.mkdir()
            module.OUT = str(articles)
            emitted = {}
            for lang in ('pt', 'en'):
                emitted_tex = module.emit_article(core, historical['verdict'], str(attempt / 'CORE_INCREMENTAL.json'), lang)
                text = Path(emitted_tex).read_text(encoding='utf-8')
                require(result['verdict'] in text.replace(r'\_', '_'), 'Article lacks current v394 result')
                emitted[lang] = [emitted_tex, str(articles / ('um_absoluto_' + lang + '.txt'))]
            receipt['articles'] = label_articles(attempt, emitted, baseline_record['copy'])
            receipt.update({'passed': True, 'candidate_version': module.UM_VERSION,
                            'ladder_clean': ladder['n_theorems_clean'], 'ladder_expected': ladder['n_theorems_expected'],
                            'axiom_coverage': kf['axiom_coverage_v392'], 'formal_new_declarations': len(result['formal_theorems']),
                            'runtime_check_count': result['runtime']['check_count'], 'runtime_maxima': result['runtime']['maxima'],
                            'negative_controls': len(negatives), 'all_negative_controls_refused': all(n['refused_before_runtime'] for n in negatives),
                            'verdict': result['verdict'], 'fresh_core_fields': refreshed, 'historical_core_field_count': len(unchanged),
                            'gate_changed': False, 'pdf_compilation_performed': False})
            status = 0
    except Exception as exc:
        receipt.update({'passed': False, 'error': repr(exc), 'traceback': traceback.format_exc()})
    finally:
        new(attempt / 'CAPTURED_STDOUT_STDERR.log', captured.getvalue())
        if before:
            after = {p: pin(p) for p in before}
            new(attempt / 'PINS_AFTER.json', after)
            differences = [p for p in before if before[p] != after[p]]
            receipt['protected_paths_checked'] = len(before)
            receipt['protected_path_changes'] = differences
            if differences:
                status = 1; receipt['passed'] = False
        receipt['audit_hook'] = {'events': AUDIT_EVENTS, 'blocked_events': sum(x['blocked'] for x in AUDIT_EVENTS),
                                 'scope': 'Python audit events: writes restricted to unit; network and subprocess refused. Not an OS sandbox proof.'}
        receipt.update({'end_utc': utc(), 'seconds': time.perf_counter() - tick, 'exit_code': status})
        result_pin = new(attempt / 'VERIFICATION_RECEIPT.json', receipt)
        print(json.dumps({'passed': receipt['passed'], 'exit_code': status, 'receipt': result_pin,
                          'error': receipt.get('error'), 'checks': receipt.get('runtime_check_count')}, ensure_ascii=False))
    return status


if __name__ == '__main__':
    raise SystemExit(main())
