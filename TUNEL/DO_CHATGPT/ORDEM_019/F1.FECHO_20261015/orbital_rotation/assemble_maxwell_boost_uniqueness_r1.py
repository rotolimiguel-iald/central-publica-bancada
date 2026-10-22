"""Assemble immutable evidence for the physical Maxwell inclusion and typed analytic bridges."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
MODULES = ['CanonicalWedgeUniquenessR5', 'SpacetimeLorentzFourierR3', 'CovariantTensorPullbackR3', 'MaxwellBoostContractionR1', 'PhysicalTensorLorentzR7', 'PhysicalSmearBoostR2', 'MaxwellBoostUniquenessAuditR1']
OUTPUT = BASE / "FINAL_MAXWELL_BOOST_UNIQUENESS_RECEIPT_R1.json"
REPORT = BASE / "MAXWELL_BOOST_UNIQUENESS_R1.md"

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
    if r["exit_code"] != 0 and any(Path(r["source"]["path"]).stem.startswith(prefix) for prefix in ["CanonicalWedgeUniqueness", "SpacetimeLorentzFourier", "CovariantTensorPullback", "MaxwellBoostContraction", "PhysicalTensorLorentz", "PhysicalSmearBoost", "MaxwellBoostUniquenessAudit"]):
        failed.append({"receipt": pin(rp), "exit_code": r["exit_code"],
                       "source": pin(r["source"]["path"]),
                       "log": pin(rp.parent / "BUILD.log")})


scope = ['[REAL] Transformação tensorial covariante de testes Maxwell pela matriz Lorentz inversa: realidade, suporte e fórmula Fourier física são provados no mesmo domínio Schwartz.', '[REAL] A contração do bivector p∧screen com o tensor transformado coincide com o coeficiente anterior no momento transformado; nenhum novo fator de gauge é assumido.', '[REAL] physicalSmear_boost e circularSmear_boost demonstram covariância por boost longitudinal no mesmo H1, nas bases real e circular respectivamente.', '[REAL] localized_wedge_boost preserva o subespaço real fechado de testes físicos suportados na cunha direita.', '[REAL] Os regularizadores gaussianos concretos fornecem a hipótese funcional do critério genérico de unicidade: imagem no domínio TW, extensão antilinear limitada do Tomita e preservação de M por médias reais de boosts.', '[REAL — condicional explícito] localized_wedge_eq_KWR_of_complex_dense prova localized(rightWedge)=KWR assumindo apenas a densidade de seu span complexo; esta obrigação segue em construção separada.']
limits = ['A densidade complexa localizada não foi assumida como habitante nem declarada resolvida neste lote. O campo wedge_glue não é removido antes de consumir uma prova de densidade.', 'A covariância deste lote é a do boost longitudinal físico; localidade causal e a rede global completa não são reivindicadas.', 'As provas são termos de sandbox. Não houve escrita no kernel canônico, um.py, Bancada de produção, memória, dados observados ou gate.', 'A revisão independente pelo pai já leu o critério de unicidade; o restante do lote aguarda seu exame. Não se reivindica recompilação independente neste recibo de construção.']
report = '# Covariância física por boost e unicidade da cunha — R1\n\n[REAL — compilado em sandbox; revisão independente pendente.]\n\n'
report += '\n'.join('- '+x for x in scope)+'\n\n## Alcance\n\n'+'\n'.join('- '+x for x in limits)
report += f'\n\n{len(accepted)} builds aceitos, {len(decls)} declarações locais auditadas, só o trio e zero sorry. Comando, início, fim, segundos, LEAN_PATH e toolchain constam dos recibos.\n'
write_new(REPORT,report.encode('utf-8'))
result = {'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'unit':'F1.FECHO_20261015','claim':845,
 'status':'COMPILED_CANDIDATE_INDEPENDENT_REVIEW_PENDING','statute':'REAL','scope':scope,'limits':limits,
 'previous_receipt':pin(BASE/'FINAL_MAXWELL_INCLUSION_RECEIPT_R1.json'),
 'accepted':accepted,'all_local_decl_count':len(decls),'all_local_declarations':[{'name':n,'axioms':list(filter(None,a.split(',')))} for n,a in decls],
 'zero_sorry':True,'axioms_only_trio':True,'failed_attempts_preserved':failed,
 'checked_dependencies_and_artifacts':list(checked.values()),'report':pin(REPORT),
 'scripts':[pin(__file__),pin(BASE/'build_orbital_r3.py')],
 'production_modified':False,'memory_modified':False,'gate_modified':False}
write_new(OUTPUT,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'receipt':pin(OUTPUT),'count':len(decls),'accepted':len(accepted)},ensure_ascii=False))
