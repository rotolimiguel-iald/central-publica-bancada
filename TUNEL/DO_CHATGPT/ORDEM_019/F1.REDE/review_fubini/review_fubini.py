"""Independent, additive review of the frozen Fubini candidate; no source edits."""
from __future__ import annotations
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import time

BASE = Path(__file__).resolve().parent
AUTHOR = BASE.parent / 'fubini'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def pin(p):
    return {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}

def save(p, b):
    with p.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    if p.read_bytes() != b:
        raise OSError(str(p))

def save_json(p, x):
    save(p, (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode())

def main():
    delivery_path = AUTHOR / 'DELIVERY_R1.json'
    delivery = json.loads(delivery_path.read_bytes())
    source = AUTHOR / 'FubiniL2.lean'
    if sha(source) != delivery['build']['source_sha256']:
        raise ValueError('Delivered source changed')
    for row in delivery['dependencies_read_only'] + delivery['artifacts']:
        if sha(Path(row['path'])) != row['sha256']:
            raise ValueError('Pin mismatch: ' + row['path'])
    out = BASE / dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    out.mkdir(exist_ok=False)
    save(out / 'FubiniL2.lean', source.read_bytes())
    save(out / 'AUTHOR_DELIVERY.json', delivery_path.read_bytes())
    save(out / 'AUTHOR_RECEIPT.json', (Path(delivery['final_attempt']) / 'RECEIPT.json').read_bytes())
    paths = [KERNEL / '.lake/build/lib/lean']
    paths += sorted((KERNEL / '.lake/packages').glob('*/.lake/build/lib/lean'))
    paths += [LEAN.parent.parent / 'lib/lean']
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [out] + paths)))
    version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
    builds = []
    def compile_file(name):
        command = [str(LEAN), '-o', str(out / (name + '.olean')), str(out / (name + '.lean'))]
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        t0 = time.perf_counter()
        p = subprocess.run(command, cwd=out, env=env, capture_output=True, check=False)
        seconds = time.perf_counter() - t0
        end = dt.datetime.now(dt.timezone.utc).isoformat()
        meta = {'command': command, 'cwd': str(out), 'toolchain': version,
                'LEAN_PATH': env['LEAN_PATH'], 'start_utc': start, 'end_utc': end,
                'seconds': seconds, 'exit_code': p.returncode}
        raw = p.stdout + p.stderr
        save(out / (name + '_STDOUT.txt'), raw)
        save(out / (name + '_BUILD.log'), (json.dumps(meta, ensure_ascii=False, indent=2) + '\n\nSTDOUT+STDERR\n').encode() + raw)
        builds.append(meta)
        if p.returncode:
            save_json(out / 'FAILED_REVIEW.json', {'builds': builds, 'source': pin(source)})
            print(raw.decode('utf-8', 'replace'))
            raise SystemExit(p.returncode)
        return raw.decode('utf-8', 'replace')
    output = compile_file('FubiniL2')
    text = source.read_text(encoding='utf-8')
    canonical_start = text.index('namespace Canonical')
    declarations = []
    for m in re.finditer(r'^(?:noncomputable )?(?:def|theorem) ([A-Za-z_][A-Za-z_0-9]*)', text, re.M):
        declarations.append('F1Rede.' + ('Canonical.' if m.start() > canonical_start else '') + m.group(1))
    probe = '''import FubiniL2
open MeasureTheory TGLExt.ImportedSQ AuditF13v31 F1Rede.Canonical
example : Function.Surjective canonicalFub := canonicalFub.surjective
example : Function.Surjective canonicalPartialFourier := canonicalPartialFourier.surjective
example (f : H1) : canonicalPartialFourier.symm (canonicalPartialFourier f) = f :=
  canonicalPartialFourier.symm_apply_apply f
#check F1Rede.fubiniL2Equiv
#check F1Rede.curryLinearIsometry_surjective
#check canonicalFub
#check canonicalPartialFourier
#check canonical_modularGroupIsBoost
'''
    probe += ''.join('#print axioms ' + n + '\n' for n in declarations)
    probe += '\nopen Lean in\nrun_cmd do\n  for n in [' + ', '.join('``' + n for n in declarations) + '] do\n'
    probe += '''    let axs ← collectAxioms n
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    let ci ← getConstInfo n
    match ci with
    | .axiomInfo _ => throwError "NEW_AXIOM_REFUSED: {n}"
    | _ => pure ()
'''
    save(out / 'ReviewProbe.lean', probe.encode())
    audit = compile_file('ReviewProbe')
    checks = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit)
    if len(checks) != len(declarations):
        raise ValueError('Incomplete axiom print coverage')
    if sha(source) != delivery['build']['source_sha256']:
        raise ValueError('Source changed during review')
    old_olean = Path(delivery['final_attempt']) / 'FubiniL2.olean'
    receipt = {
        'unit': 'F1.REDE', 'reviewer': 'codex-takesaki-local-lemmas',
        'verdict': 'PASSA_NO_ESCOPO_D1A1_E_ENTRELACAMENTO_B0',
        'status': 'REAL_KERNEL_RECOMPILED_INDEPENDENTLY; SEMANTIC_REVIEW',
        'source': pin(source), 'delivery': pin(delivery_path), 'builds': builds,
        'dependencies': delivery['dependencies_read_only'],
        'declaration_count': len(declarations), 'axiom_prints': checks,
        'all_axioms_subset_of_trio': True,
        'sorry_admit_axiom_tokens': re.findall(r'\b(?:sorry|admit|axiom)\b', text),
        'copied_olean': pin(out / 'FubiniL2.olean'), 'author_olean': pin(old_olean),
        'olean_byte_identical': sha(out / 'FubiniL2.olean') == sha(old_olean),
        'semantic_checks': [
            {'check': 'strong_measurability', 'result': 'PASSA', 'anchor': 'FubiniL2.lean:85', 'reason': 'Good sections form a measurable set. Distances to every L2 vector are measurable; separability gives second countability and strong measurability. Bad sections are zero on a null set.'},
            {'check': 'integral_and_norm', 'result': 'PASSA', 'anchor': 'FubiniL2.lean:122', 'reason': 'Square norm is integrable from MemLp 2, then integral_prod_symm and a.e. section equality establish squared-norm disintegration. This proves norm preservation.'},
            {'check': 'surjectivity', 'result': 'PASSA', 'anchor': 'FubiniL2.lean:220', 'reason': 'Finite-measure indicator functions have explicit rectangular preimages. Lp induction uses addition and closed range of an isometry from the complete product L2. Surjectivity is proved, not assumed.'},
            {'check': 'unchanged_canonical_H1_measure_Fib', 'result': 'PASSA', 'anchor': 'FubiniL2.lean:246', 'reason': 'Fib is EuclideanSpace complex (Fin 2). momentumMeasure is Lebesgue on Transverse times real rapidity. H1 remains Lp Fib 2 orbitalMeasure(0); existing toRapidity supplies the equivalence before currification.'},
            {'check': 'boost_intertwining', 'result': 'PASSA', 'anchor': 'FubiniL2.lean:265', 'reason': 'A.e. sections intertwine productRapidityShift with actual real shift. Existing orbitalScalarBoost_intertwines and fourier_shift yield negative-sign Fourier character with 2*pi*s, hence sigma=4*pi^2*xi for B0(-2*pi*t).'},
            {'check': 'actual_surjective_canonical_objects', 'result': 'PASSA', 'anchor': 'ReviewProbe.lean:3', 'reason': 'Independent examples type surjectivity of both canonical equivalences and inverse cancellation with no proof parameters.'},
        ],
        'general_assumptions': ['SFinite mu and nu', 'IsSeparable mu', 'SeparableSpace E', 'CompleteSpace E', 'Real inner product compatible with norm', 'NormedField k and NormedSpace k E'],
        'scope_limits': ['ModularGroupIsBoost is the explicitly defined spectral boost identity, not yet a theorem about the modular operator of a constructed standard wedge.', 'This source does not construct J_W, a Tomita operator, Delta=SdagS, K(W), a four-dimensional net, or second quantization.'],
        'findings': [], 'production_changed': False, 'memory_changed': False,
        'created_junction': False,
        'artifacts': [pin(p) for p in sorted(out.iterdir()) if p.is_file()],
    }
    save_json(out / 'REVIEW_RESULT.json', receipt)
    print(json.dumps({'review': str(out / 'REVIEW_RESULT.json'), 'sha256': sha(out / 'REVIEW_RESULT.json'), 'builds': [{'exit': b['exit_code'], 'seconds': b['seconds']} for b in builds], 'declarations': len(declarations), 'olean_byte_identical': receipt['olean_byte_identical']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
