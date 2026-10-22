"""Create a new immutable delivery after all requested Lean modules pass."""
from pathlib import Path
import json
import sys
from build_flow import BASE, pin, save

attempt=Path(sys.argv[1]).resolve()
assert attempt.parent == (BASE/'attempts').resolve()
result_path=attempt/'RESULTADO_BUILD.json'
result=json.loads(result_path.read_text(encoding='utf-8'))
assert result['passed'] and result['dependencies_unchanged']
expected=['TimeGravitonScalar','TimeGravitonFlow','TimeGravitonKraus']
assert [x['module'] for x in result['modules']] == expected
for name in expected:
    assert (BASE/'TGLExt'/(name+'.lean')).read_bytes() == (attempt/(name+'.lean')).read_bytes()
reports=[r for m in result['modules'] for r in m['axiom_reports']]
assert reports and all(set(x['axioms']) <= {'propext','Classical.choice','Quot.sound'} for x in reports)
axiom_path=BASE/('AXIOMS_'+attempt.name+'.txt')
save(axiom_path,('\n'.join(x['declaration']+': ['+', '.join(x['axioms'])+']' for x in reports)+'\n').encode())
delivery={
 'unit':'F1.TEMPO.V394', 'scope':'finite M2 continuous flow, sandbox candidate',
 'status':'REAL_COMPILED_SANDBOX_NOT_RATIFIED',
 'build':pin(result_path),'sources':[pin(attempt/(n+'.lean')) for n in expected],
 'oleans':[pin(attempt/(n+'.olean')) for n in expected],
 'axiom_report_count':len(reports),'all_axioms_within_trio':True,'no_source_placeholders':True,
 'consolidated_axioms':pin(axiom_path),
 'proved':[
  'Exact exponential scalar factors equal existing IALDJones.spin; derivative and asymptotic decay.',
  'Concrete two-mode M2 flow: identity at zero, semigroup, continuity, derivative, generator.',
  'Generator equals the transported Hg commutator plus gamma(Eg-Id), and a one-jump GKLS form.',
  'Eg is preserved and fixed; the long-time limit is EgX; fixed-space characterization.',
  'Conjugate rootPlus/rootMinus modes carry frequencies +2omega/-2omega.',
  'A nonzero rootPlus coordinate gives the logarithmic clock and cannot vanish at finite time.',
  'The normalized coherence of the transported density gives the same clock, with initial coherence i/4.',
  'Lifted phase gives elapsed time when omega is nonzero; no global inverse of the angle is claimed.',
  'Both projectors remain fixed; transported source tends to I/2.',
  'Rule admissibility and inscription are preserved; equality is on inscriptions.',
  'For nonnegative gamma and time: explicit three-Kraus action and sum K* K=I.'
 ],
 'limits':[
  'No physical calibration of omega, gamma, or the time unit is supplied by these algebraic proofs.',
  'No unique interpolation follows from discrete samples alone.',
  'Eg is two-block pinching, not the corner PXP or the distinct M4 consumer.',
  'No unique pure attractor; no finite-time arrival; negative times are not certified channels.',
  'Kraus equalities are the finite CP/TP certificate; no universal infinite-dimensional CP API is claimed.',
  'No advanced signal, empirical result, canonical installation, or gate change.'
 ],
 'integration':'Sandbox imports are flat modules; prefix local imports with TGLExt only during candidate transposition and recompile the copied project.',
 'failed_attempts_preserved':[str(p) for p in sorted((BASE/'attempts').iterdir()) if p.is_dir() and p != attempt],
 'scripts':[pin(BASE/'build_flow.py'),pin(BASE/'finish_flow.py')]
}
destination=BASE/('DELIVERY_'+attempt.name+'.json')
save(destination,delivery)
print(json.dumps(pin(destination),ensure_ascii=False))
