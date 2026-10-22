"""Assemble immutable evidence for the physical Maxwell inclusion and typed analytic bridges."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
MODULES = ['HalfPlaneBoundaryUniquenessR4', 'DominatedWithinIntegralR3', 'PositiveCoefficientBoundaryR4', 'PositiveCoefficientBothR4', 'RegularCoefficientBoundaryR3', 'RegularSemigroupClosureR3', 'PhysicalWedgeNullGeometryR3', 'SchwartzCutoffDerivativeR4', 'SchwartzCutoffEstimateR5', 'SchwartzCompactDensityR3', 'SchwartzCutoffSupportR1', 'PhysicalWedgeGroupInvariantR3', 'PhysicalWedgeSchwartzClosureR3', 'PhysicalLocalizedBoostR2', 'PhysicalNetGeometryR1', 'PhysicalCanonicalWedgeEqualityR3', 'PhysicalWedgeDensityAuditR1']
OUTPUT = BASE / "FINAL_PHYSICAL_WEDGE_EQUALITY_RECEIPT_R1.json"
REPORT = BASE / "PHYSICAL_WEDGE_EQUALITY_R1.md"

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
    if r["exit_code"] != 0 and any(Path(r["source"]["path"]).stem.startswith(prefix) for prefix in ['HalfPlaneBoundaryUniqueness', 'DominatedWithinIntegral', 'PositiveCoefficientBoundary', 'PositiveCoefficientBoth', 'RegularCoefficientBoundary', 'RegularSemigroupClosure', 'PhysicalWedgeNullGeometry', 'SchwartzCutoffDerivative', 'SchwartzCutoffEstimate', 'SchwartzCompactDensity', 'SchwartzCutoffSupport', 'PhysicalWedgeGroupInvariant', 'PhysicalWedgeSchwartzClosure', 'PhysicalLocalizedBoost', 'PhysicalNetGeometry', 'PhysicalCanonicalWedgeEquality', 'PhysicalWedgeDensityAudit']):
        failed.append({"receipt": pin(rp), "exit_code": r["exit_code"],
                       "source": pin(r["source"]["path"]),
                       "log": pin(rp.parent / "BUILD.log")})


scope = ['[REAL] Os coeficientes positivos de U1 e a unicidade analítica na meia-faixa transformam invariância de semirreta em invariância de grupo do span complexo fechado, usando momentos de energia dos smears físicos reais.', '[REAL] As duas semirretas nulas preservam geometricamente a cunha; a decomposição da translação espacial permite trazer qualquer teste real de suporte limitado à cunha e desfazer a translação no span complexo.', '[REAL] Cutoffs suaves compactos convergem na topologia Schwartz; preservam realidade e o suporte não nulo original. A continuidade do smearing transporta esse limite ao mesmo H1.', '[REAL] DenseRange physicalSmearCLM é consumida da construção independente PhysicalSmearDensityR6 (inverso explícito dos screens, extensão Schwartz 4D e densidade fora do eixo nulo), sem hipótese de totalidade no consumidor final.', '[REAL] physical_right_wedge_eq_KWR identifica a rede física de testes reais suportados com o KWR canônico, usando a inclusão, a invariância por boosts e o critério gaussiano de unicidade já auditados.', '[REAL] physicalNet_wedge_glue, physicalNet_mono, physicalNet_translate e physicalNet_boost fornecem os campos correspondentes da assinatura; a não vacuidade é exibida pelo vetor não zero do KWR canônico.']
limits = ['A condição K_local para regiões com SpacelikeSep no tipo legado não é provada neste lote. A rede não é anunciada como LightNetData completo antes desse termo.', 'A representação física de helicidade e o smearing circular já existem; nenhum rótulo helicidade foi usado para inventar covariância ou localidade.', 'Function.support permanece o suporte não nulo original. Não foi introduzida margem de separação entre tsupports como hipótese escondida.', 'Termos de sandbox, só trio e zero sorry. Nenhuma produção, memória, kernel canônico, um.py, dado observado ou gate alterado.', 'Este recibo é de construção. Revisão independente do pai é etapa separada; os lotes anteriores de inclusão e unicidade já possuem seus próprios pareceres.']
report = '# Igualdade da cunha física Maxwell com KWR — R1\n\n[REAL — compilado em sandbox; revisão independente pendente.]\n\n'
report += '\n'.join('- '+x for x in scope)+'\n\n## Alcance\n\n'+'\n'.join('- '+x for x in limits)
report += f'\n\n{len(accepted)} builds aceitos, {len(decls)} declarações locais auditadas, só o trio e zero sorry. Comando, início, fim, segundos, LEAN_PATH e toolchain constam dos recibos.\n'
write_new(REPORT,report.encode('utf-8'))
result = {'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'unit':'F1.FECHO_20261015','claim':845,
 'status':'COMPILED_CANDIDATE_INDEPENDENT_REVIEW_PENDING','statute':'REAL','scope':scope,'limits':limits,
 'previous_receipt':pin(BASE/'FINAL_MAXWELL_BOOST_UNIQUENESS_RECEIPT_R1.json'),
 'global_density_source':pin(BASE.parent/'maxwell_global'/'PhysicalSmearDensityR6.lean'),
 'accepted':accepted,'all_local_decl_count':len(decls),'all_local_declarations':[{'name':n,'axioms':list(filter(None,a.split(',')))} for n,a in decls],
 'zero_sorry':True,'axioms_only_trio':True,'failed_attempts_preserved':failed,
 'checked_dependencies_and_artifacts':list(checked.values()),'report':pin(REPORT),
 'scripts':[pin(__file__),pin(BASE/'build_orbital_r3.py')],
 'production_modified':False,'memory_modified':False,'gate_modified':False}
write_new(OUTPUT,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'receipt':pin(OUTPUT),'count':len(decls),'accepted':len(accepted)},ensure_ascii=False))
