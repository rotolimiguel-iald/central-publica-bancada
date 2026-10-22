"""Create immutable delivery manifest from a successful build receipt."""
from pathlib import Path
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parent

def entry(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def save_new(p, b):
    with p.open('xb') as f:
        f.write(b)
    assert p.read_bytes() == b

receipt = Path(sys.argv[1]).resolve()
build = json.loads(receipt.read_text(encoding='utf-8'))
assert build['exit_code'] == 0
attempt = receipt.parent
src = attempt / 'BosonicFockGroupActions.lean'
assert src.read_bytes() == (BASE / src.name).read_bytes()
raw = (attempt / 'AXIOMS.txt').read_text(encoding='utf-8')
assert 'sorryAx' not in raw and 'error:' not in raw
declarations = []
axioms = set()
for line in raw.splitlines():
    if line.startswith('LOCAL_DECL\t'):
        _, name, axs = line.split('\t')
        declarations.append(name)
        axioms.update(filter(None, axs.split(',')))
assert axioms <= {'propext', 'Classical.choice', 'Quot.sound'}
assert declarations
deps = []
for p in build['read_only_dependency_paths']:
    directory = Path(p)
    if directory.is_relative_to(BASE):
        deps += [entry(f) for f in sorted(directory.iterdir()) if f.suffix in ('.lean', '.olean') or f.name == 'RECEIPT.json']
failed = BASE / 'attempts/20261013T223724_941209Z'
report = BASE / 'RELATORIO_FOCK_GROUP_ACTIONS_R1.md'
save_new(report, ('# Ações concretas no Fock bosônico\n\n'
    '[REAL — compilado em sandbox; revisão pendente] UF(a)=Γ(U1(a)) e VF(s)=Γ(B0(s)).\n'
    'Leis de zero e adição, inversão de UF, vácuo fixo e inclusão de uma partícula entrelaçada.\n'
    'Covariância VF(s) UF(a) VF(s)⁻¹ = UF(wedgeBoostMap(s,a)) transporta B0_conj por Γ_trans.\n'
    f'EXIT 0; {build["seconds"]:.3f} s; {len(declarations)} declarações locais; apenas o trio; zero sorry.\n'
    'Sem FockCertificate assumido. Continuidade forte será composta em módulo separado.\n'
    'Não se afirma energia positiva no Fock, CCR, álgebra local ou Poincaré completo.\n'
    'A tentativa anterior falhou por namespace ausente e foi preservada integralmente.\n'
    'Nenhuma mudança em produção, kernel, memória ou gate.\n').encode('utf-8'))
result = dict(unit='F1.REDE', stage='concrete Fock translations and wedge boosts',
    status='REAL_COMPILED_SANDBOX__REVIEW_PENDING', receipt=entry(receipt), source=entry(src),
    report=entry(report), start_utc=build['start_utc'], end_utc=build['end_utc'], seconds=build['seconds'],
    exit_code=0, declarations=declarations, axioms=sorted(axioms), sorry=0,
    dependencies=deps, artifacts=[entry(p) for p in sorted(attempt.iterdir()) if p.is_file()],
    scripts=[entry(BASE/'build_fock_group_actions.py'), entry(Path(__file__).resolve())],
    failed_attempts=[entry(p) for p in sorted(failed.iterdir()) if p.is_file()],
    scope='Concrete group laws, invariant vacuum, one-particle intertwiner and boost covariance; no spectral/CCR/local-net claims.',
    kernel_changed=False, memory_changed=False, gate_changed=False)
manifest = BASE / 'RESULTADO_FOCK_GROUP_ACTIONS_R1.json'
save_new(manifest, (json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps(entry(manifest), ensure_ascii=False))
