"""Source-only R7 diagnosis. Never invokes Lean, providers, or process control."""
import datetime as dt
import difflib
import hashlib
import json
import os
import re
from pathlib import Path

from finish_requirement_reviews import OUT, BASE, REFERENCE, ACTOR, fresh, pin, read
from accept_reviewed_requirement import call

AREA = BASE / 'gns_coefficient_tomita'
SOURCE = AREA / 'CanonicalFockPolarRightCutoffOrderR10.lean'
CURRENT = AREA / 'attempts/20261016T105344_102192Z'
CANDIDATE = OUT / 'CanonicalFockPolarRightCutoffOrderR11Candidate.lean'

def fresh_bytes(path, raw):
    assert not path.exists(), path
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    assert path.read_bytes() == raw

def source_entry(path, patterns):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    anchors = {p: [i + 1 for i, line in enumerate(lines) if p in line] for p in patterns}
    assert all(anchors.values()), (path, anchors)
    return {**pin(path), 'anchors': anchors}

def signatures(text):
    return [re.sub(r'\s+', ' ', m.group(0)).strip() for m in re.finditer(
        r'^(?:private )?(?:theorem|def)\s+\w+[\s\S]*?:=', text, re.M)]

def main():
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    raw = SOURCE.read_bytes()
    start = read(CURRENT / 'START_RECEIPT.json')
    assert hashlib.sha256(raw).hexdigest() == start['source']['sha256']
    assert raw == Path(start['source']['path']).read_bytes()
    original = raw.decode('utf-8').replace('\r\n', '\n')
    candidate = original
    local_instances = ('local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace\n'
        'local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=\n'
        '  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace\n')
    assert candidate.count(local_instances) == 3
    candidate = candidate.replace(local_instances, '', 1)
    ambient = '(H := TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F)'
    old = 'GenericClosedEquationsCFC.closed_subalgebra_cfc_of_eq core.toStarSubalgebra'
    assert candidate.count(old) == 2
    candidate = candidate.replace(old, 'GenericClosedEquationsCFC.closed_subalgebra_cfc_of_eq\n    ' + ambient + ' core.toStarSubalgebra')
    old = 'GenericClosedEquationsCFC.closed_subalgebra_mem_of_eq_cfc core.toStarSubalgebra'
    assert candidate.count(old) == 1
    candidate = candidate.replace(old, 'GenericClosedEquationsCFC.closed_subalgebra_mem_of_eq_cfc\n    ' + ambient + ' core.toStarSubalgebra')
    old = '(regularSineWindowCore m) (regularSineWindowCore_right J hreg m) _ _'
    assert candidate.count(old) == 1
    candidate = candidate.replace(old, '(regularSineWindowCore m) (regularSineWindowCore_right J hreg m)\n    (fun z : ℂ => (Real.sigmoid (m * (2 * z.re - 1)) : ℂ))\n    (regularSineResolvent fockFlow m)')
    old = '(scalarPolarRightAlgebra J) (scalarPolarRightAlgebra_isClosed J) b hb _ _'
    assert candidate.count(old) == 1
    candidate = candidate.replace(old, '(scalarPolarRightAlgebra J) (scalarPolarRightAlgebra_isClosed J) b hb\n    (fun z : ℂ => (Real.sqrt z.re : ℂ)) (hilbertPositiveSqrt b.val)')
    # Keep local GNS Star/order instances in the two actual GNS consumer blocks.
    # Markers are placed before doc comments so documentation stays on declarations.
    insertions = []
    for m in re.finditer(r'^(?:private )?(?:theorem|def)\s+(\w+)', candidate, re.M):
        pos = m.start()
        before = candidate[:pos].rstrip()
        if before.endswith('-/'):
            docpos = before.rfind('/--')
            if docpos >= 0 and '-/' not in before[docpos:-2]:
                pos = docpos
        marker = '#eval do\n  IO.println "R7_STAGE ' + m.group(1) + '"\n  (← IO.getStdout).flush\n\n'
        insertions.append((pos, marker))
    for pos, marker in reversed(insertions):
        candidate = candidate[:pos] + marker + candidate[pos:]
    candidate = candidate.replace('import CanonicalFockPolarRightClosureR10\n',
        'import CanonicalFockPolarRightClosureR10\n\n/-! Experimental source-only candidate, DECLARADO, NOT COMPILED.\n'
        'Alternative to R10: do not import both modules with duplicate declaration names.\n'
        'Explicit ambient CFC carrier and arguments; remove GNS instances only from CFC block.\n'
        'Mathematical statement text and the two GNS consumer proof bodies are preserved. -/\n', 1)
    assert signatures(candidate) == signatures(original)
    assert re.findall(r'^#print axioms .+$', original, re.M) == re.findall(r'^#print axioms .+$', candidate, re.M)
    assert re.findall(r'^import .+$', original, re.M) == re.findall(r'^import .+$', candidate, re.M)
    assert not re.search(r'\b(sorry|admit|axiom)\b', candidate)
    assert candidate.count(local_instances) == 2
    fresh_bytes(CANDIDATE, candidate.encode('utf-8'))
    diff = ''.join(difflib.unified_diff(original.splitlines(True), candidate.splitlines(True),
        fromfile=SOURCE.name, tofile=CANDIDATE.name))
    fresh_bytes(OUT / 'R7_R11_CANDIDATE.diff', diff.encode('utf-8'))

    log_raw = (CURRENT / 'RUNNING_OUTPUT.log').read_bytes()
    log_snapshot = OUT / 'R7_R10_RUNNING_OUTPUT_SNAPSHOT.log'
    fresh_bytes(log_snapshot, log_raw)
    sources = [
        source_entry(SOURCE, ['regularSineResolvent_right', 'regularInverseGeneratorCutoff_right',
                             'scalarRightAction_sqrt', 'scalarPolarRight_commutes_left',
                             'scalarWeight_right_perturbed_mono', 'local instance']),
        source_entry(AREA / 'CanonicalFockPolarRightClosureR10.lean', ['scalarRightAction_cfc', 'continuous_left_mul', 'scalarRightAction_closed_of_bounded_strongStar']),
        source_entry(AREA / 'GenericClosedEquationsCFCR5.lean', ['closed_subalgebra_cfc_of_eq', 'closed_subalgebra_mem_of_eq_cfc']),
        source_entry(AREA / 'GeneralSineResolventApproxR2.lean', ['regularSineResolvent_cfc', 'regularSineResolvent_tendsto']),
        source_entry(AREA / 'GeneralRegularCutoffCFCR1.lean', ['regularInverseGeneratorCutoff_cfc']),
        source_entry(AREA / 'CanonicalFockPolarRightAlgebraR6.lean', ['scalarPolarRightAlgebra']),
        source_entry(AREA / 'CanonicalFockGNSOrderR4.lean', ['scalarGNSRepresentation_mono']),
        source_entry(BASE / 'takesaki_fock/CanonicalFockRegularCoreR2.lean', ['fockFlow', 'abbrev core']),
        source_entry(BASE / 'takesaki_fock/CanonicalFockGNSR5.lean', ['GNSSubspace', 'GNSHilbert', 'gnsCompleteSpace']),
        source_entry(BASE / 'takesaki_fock/CanonicalFockGNSRepresentationR6.lean', ['scalarGNSRepresentation']),
        source_entry(BASE / 'takesaki_fock/CanonicalFockRegularRightGNSR11.lean', ['regularRightCoreElement']),
        source_entry(BASE / 'takesaki_fock/ClosedSubmoduleRestrictionR2.lean', ['endomorphismStar']),
    ]
    history = []
    for name in ['20261016T083950_407103Z', '20261016T085556_271957Z', '20261016T101531_954005Z',
                 '20261016T103236_490151Z', '20261016T104804_321967Z']:
        attempt = AREA / 'attempts' / name
        receipt = read(attempt / 'RECEIPT.json')
        logfile = attempt / 'RUNNING_OUTPUT.log'
        lines = logfile.read_text(encoding='utf-8').splitlines()
        relevant = [{'line': i+1, 'text': s} for i,s in enumerate(lines)
                    if re.search(r'(import took|timeout|isDefEq|failed to synthesize|rewriteSeq took|obtain took|^\s+(elaboration|typeclass inference|type checking) )',s)]
        src = Path(receipt['source']['path'])
        assert pin(src)['sha256'] == receipt['source']['sha256']
        history.append({'attempt': name, 'seconds': receipt['seconds'], 'exit_code': receipt['exit_code'],
                        'source': pin(src), 'receipt': pin(attempt / 'RECEIPT.json'), 'log': pin(logfile),
                        'relevant_log_lines': relevant})
    sync = call({'operation':'project','reference':str(REFERENCE),'max_chars':60000})
    assert sync['exit_code'] == 0 and sync['response']['ok']
    projection = sync['response']['result']['projection']
    assert projection['context_id'] == '34290aaa-3dcc-51d5-b224-f3eeec93509b'
    task = next(t for t in projection['active'] if t['id'] == 'R7')
    assert task['status'] == 'working' and task['lease']['owner'] == ACTOR
    fresh(OUT / 'R7_COST_FINAL_REVIEW_PROJECT.json', sync)
    fresh(OUT / 'R7_R11_CANDIDATE_SOURCE_CHECK.json', {
        'time_utc':now, 'source':pin(SOURCE), 'candidate':pin(CANDIDATE), 'diff':pin(OUT/'R7_R11_CANDIDATE.diff'),
        'declaration_headers_text_equal':True, 'declaration_count':len(signatures(original)),
        'imports_text_equal':True, 'print_axioms_requests_text_equal':True,
        'no_sorry_admit_or_new_axiom_tokens':True, 'stage_markers':len(insertions),
        'local_gns_instance_blocks_removed':1, 'local_gns_consumer_blocks_preserved':2,
        'compiled':False, 'proof_equivalence_verified_by_lean':False,
        'note':'Syntactic preservation only. Inferred instances and elaborated proof terms require an authorized future compilation.'})
    report = {
        'protocol':'iald-independent-component-diagnosis/v1', 'created_utc':now, 'actor':ACTOR,
        'mission_reference':pin(REFERENCE), 'context_id':projection['context_id'], 'revision_observed':projection['revision'],
        'task_id':'R7', 'criterion':task['criterion'], 'lease':task['lease'],
        'verdict':'DIAGNOSIS_WITH_UNCOMPILED_CANDIDATE__R7_REMAINS_OPEN',
        'facts':[
            '[REAL] Historical R9 has deterministic isDefEq timeouts at source lines 187, 223 and 248, where sine resolvent CFC, inverse cutoff CFC and positive-root CFC are transported to the concrete algebra. The first two logged tactics took 104s and 105s.',
            '[REAL] ClosureR10 alone returned exit 0 in 338.649656s, with import 313s, elaboration 2.56s and typeclass inference 12.3s. Its closedness/CFC generic lemmas therefore have a successful existing compilation, distinct from CutoffOrderR10.',
            '[REAL] CutoffOrderR10 source equals the immutable execution copy and START pin. The observed running log is pinned separately; it lacks a declaration marker. No active elaboration location can be established from this log.',
            '[REAL] First block installs GNSHilbert completeness/Star locally while the CFC carrier is RegularHilbert F. core, GNSHilbert, weightContext and scalarPolarRightAlgebra are definitions/abbreviations through deeply nested carriers; GNSHilbert is a closed subspace in a different regular Hilbert space.',
            '[REAL] endomorphismStar is defined by inferInstance for the closed submodule. This is an alternative definitional path to the adjoint, not evidence of a mathematically different involution.'
        ],
        'diagnosis':{
            'statute':'CONJECTURE_SUPPORTED_BY_HISTORICAL_ERRORS',
            'likely_cost':'Definitional equality and typeclass inference across concrete regular/Fock/GNS carriers at the CFC boundary; local GNS instances can cause unsuccessful candidate checks or alternate instance paths before the ambient solution.',
            'confidence':'Moderate for CFC/definitional-equality family; low for exact current declaration or a single responsible instance. No trace/stack was collected from the live build.',
            'not_established':['Current R10 is in the same tactic as R9','All elapsed time is typeclass search','The candidate compiles','The candidate improves performance'],
            'already_fixed_in_R10':'R10 already replaces R9 rw/obtain at concrete CFC sites by generic equality-transport lemmas. Recommending only that replacement would repeat an existing fix.'},
        'candidate':{
            **pin(CANDIDATE), 'statute':'DECLARADO_EXPERIMENTAL_UNCOMPILED',
            'changes':['Remove local GNS CompleteSpace and Star only from the first CFC block; retain both GNS consumer blocks.',
                       'Fix H explicitly to TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F at the three generic CFC applications.',
                       'Supply the exact sigmoid/sqrt functions and target operators instead of two metavariables.',
                       'Emit and flush one stage marker before each declaration for any future authorized run; do not increase heartbeats.'],
            'source_checks':pin(OUT/'R7_R11_CANDIDATE_SOURCE_CHECK.json'),
            'limits':'Alternative module with original declaration names. Do not co-import with R10. Textual statements unchanged does not prove equality of elaborated terms or successful compilation.',
            'fallback_if_still_slow':'After a permitted diagnostic identifies the site, specialize the compiled generic CFC/equality transport to the explicit ambient carrier before substituting the concrete core. Keep transport generic in the subtype equality and avoid unfolding weightContext/GNSSubspace inside rewrite matching. Do not add axioms or a second representation.'},
        'preserved_target':[
            'Original fockFlow and regular core, not an abstract replacement for the physical Fock carrier.',
            'Same J and hreg hypotheses, same spectral resolvent/inverse cutoff/positive square root, with no independent root.',
            'Same right-action commutation on the full weight ideal and dense extension.',
            'Same perturbed weight norm formula and b*star b <= c*star c comparison; no weakened inequality or new premise.',
            'R7 whole Takesaki/crossed-product/action/weight/trace linkage remains OPEN; diagnostic is not requirement acceptance.'
        ],
        'current_attempt':{'start':pin(CURRENT/'START_RECEIPT.json'), 'source':pin(Path(start['source']['path'])),
                           'log_snapshot':pin(log_snapshot), 'log_text_at_observation':log_raw.decode('utf-8'),
                           'terminal_receipt_exists_at_observation':(CURRENT/'RECEIPT.json').exists(),
                           'process_status':'Not queried in this investigation. Root reported PID165856 identity at 12:38 UTC, about 5742s user CPU and 3.5GB working set; DECLARADO by coordinator, not independent measurement.',
                           'decision':'No duplicate build and no process termination. Root decides execution after a verified terminal result or documented cancellation.'},
        'sources':sources, 'historical_attempts':history,
        'activity':{'new_compilations':0,'provider_calls':0,'process_queries':0,'process_terminations':0,
                    'production_edits':0,'global_memory_edits':0,'scientific_accepts':0},
        'mission_closeout':'Lease preserved on coordinator instruction; R7 remains working and substantively OPEN. No submit/accept, gate or global board closure.'
    }
    fresh(OUT/'R7_COMPILE_COST_REVIEW_R1.json', report)
    assert SOURCE.read_bytes() == raw
    print(json.dumps({'report':pin(OUT/'R7_COMPILE_COST_REVIEW_R1.json'),'candidate':pin(CANDIDATE),
                      'revision':projection['revision'],'declarations':len(signatures(original))},ensure_ascii=False))

if __name__ == '__main__':
    main()
