"""Create an immutable receipt for the scalar orbital rotation construction."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
MODULES = ['ScreenChargeConjugationR2', 'ScreenHalfTurnR3', 'ScreenGeometricReflectionR4', 'ScreenReflectionAuditR1']
OUTPUT = BASE / "FINAL_SCREEN_REFLECTION_RECEIPT_R1.json"
REPORT = BASE / "SCREEN_REFLECTION_R1.md"

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

def write_new(p, b):
    if p.exists():
        raise RuntimeError(f"Existing output refused: {p}")
    tmp = p.with_name(p.name + ".tmp")
    with tmp.open("xb") as f:
        f.write(b)
    if tmp.read_bytes() != b:
        raise RuntimeError("Temporary bytes differ")
    tmp.rename(p)

if OUTPUT.exists() or REPORT.exists():
    raise RuntimeError("Existing final evidence refused before assembly")

receipts = [(p, json.loads(p.read_text(encoding="utf-8")))
            for p in sorted((BASE / "attempts").glob("*/RECEIPT.json"))]
accepted, checked = [], {}
for mod in MODULES:
    src = BASE / (mod + ".lean")
    srcpin = pin(src)
    if re.search(r"\bsorry\b", src.read_text(encoding="utf-8")):
        raise RuntimeError("Sorry token refused")
    matches = [(p, r) for p, r in receipts if r["exit_code"] == 0
               and Path(r["source"]["path"]).stem == mod
               and r["source"]["sha256"] == srcpin["sha256"]]
    if not matches:
        raise RuntimeError(f"No accepted compilation: {mod}")
    rp, r = matches[-1]
    if not r["readonly_dependencies_unchanged"]:
        raise RuntimeError("Dependencies changed during compilation")
    for entry in [r["source"], *r["dependencies"], *r["artifacts"]]:
        if pin(entry["path"])["sha256"] != entry["sha256"]:
            raise RuntimeError(f"Pin differs: {entry['path']}")
        checked[entry["path"]] = entry
    accepted.append({"module": mod, "source": srcpin, "receipt": pin(rp),
                     "exit_code": r["exit_code"], "seconds": r["seconds"],
                     "start_utc": r["start_utc"], "end_utc": r["end_utc"],
                     "LEAN_PATH": r["LEAN_PATH"], "toolchain": r["toolchain"]})

audit_dir = Path(accepted[-1]["receipt"]["path"]).parent
audit = (audit_dir / "AXIOMS.txt").read_text(encoding="utf-8")
decls = re.findall(r"^LOCAL_DECL\t([^\t\r\n]+)\t([^\r\n]*)", audit, re.M)
counts = re.findall(r"^AUDITED_COUNT\t([0-9]+)", audit, re.M)
if len(counts) != 1 or len(decls) != int(counts[0]) or not decls:
    raise RuntimeError("Incomplete all-local audit")
trio = {"propext", "Classical.choice", "Quot.sound"}
for name, ax in decls:
    if not set(filter(None, ax.split(","))) <= trio:
        raise RuntimeError(f"Non-trio declaration: {name}")

failed = []
for rp, r in receipts:
    if r["exit_code"] != 0:
        failed.append({"receipt": pin(rp), "exit_code": r["exit_code"],
                       "source": pin(r["source"]["path"]),
                       "log": pin(rp.parent / "BUILD.log")})


scope = [
    'Theta is the actual fibre-swapped conjugation lifted to the unchanged canonical H1. It is antiunitary, involutive, commutes with the determinant-one helicity action and reverses U1 translations.',
    'The concrete half-turn is (t,x1,x2,x3) -> (t,x1,-x2,-x3). Its generated Lorentz element is involutive; its screen matrix is identity almost everywhere and its helicity action is transverse momentum reflection.',
    'The previously constructed spectral Jcandidate equals helicityUnitary(halfTurn) after Theta. The existing FourierConjugation and GeometricIdentification theorems are reused without reconstructing Fourier.',
    'Jcandidate conjugates the proper helicity action by halfTurn*L*halfTurn. The existing Jcandidate translation-reflection theorem is preserved and imported.'
]
limits = [
    'This proves the concrete geometric reflection identity and covariance. It does not alone construct the local real-subspace net or prove the CanonicalNetInput wedge_glue.',
    'The determinant-one condition is explicit; no statement about arbitrary improper helicity mixing is inferred.',
    'The existing KWR, positive half-modular TW, modular boost and canonical Fock space remain the same objects. No physical measurement or gate change is claimed.',
    'Independent review of these three new modules remains with the parent. The preceding screen representation already has a separate parent semantic review.'
]
report = '# Reflexão geométrica no H1 canônico — R1\n\n[REAL — compilado em sandbox; revisão independente pendente.]\n\n'
report += '\n'.join('- '+x for x in scope)+'\n\n## Alcance\n\n'+'\n'.join('- '+x for x in limits)
report += f'\n\n{len(accepted)} builds aceitos, {len(decls)} declarações locais auditadas, só o trio e zero sorry. Comando, início, fim, segundos, LEAN_PATH e toolchain constam dos recibos.\n'
write_new(REPORT,report.encode('utf-8'))
result = {'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'unit':'F1.FECHO_20261015','claim':845,
 'status':'COMPILED_CANDIDATE_INDEPENDENT_REVIEW_PENDING','statute':'REAL','scope':scope,'limits':limits,
 'previous_receipt':pin(BASE/'FINAL_SCREEN_LORENTZ_RECEIPT_R1.json'),
 'accepted':accepted,'all_local_decl_count':len(decls),'all_local_declarations':[{'name':n,'axioms':list(filter(None,a.split(',')))} for n,a in decls],
 'zero_sorry':True,'axioms_only_trio':True,'failed_attempts_preserved':failed,
 'checked_dependencies_and_artifacts':list(checked.values()),'report':pin(REPORT),
 'scripts':[pin(__file__),pin(BASE/'build_orbital_r1.py')],
 'production_modified':False,'memory_modified':False,'gate_modified':False}
write_new(OUTPUT,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'receipt':pin(OUTPUT),'count':len(decls),'accepted':len(accepted)},ensure_ascii=False))
