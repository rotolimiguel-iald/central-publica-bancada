"""Assemble immutable evidence for the physical Maxwell inclusion and typed analytic bridges."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
MODULES = ['WedgePhysicalFourierR2', 'LowerGaussianControlR2', 'LowerGaussianContourR2', 'MaxwellComplexRapidityR3', 'RapidityExponentialSpanR2', 'LowerStripFourierBalanceR4', 'LowerGaussianReflectionR1', 'MaxwellRapidityPolynomialR1', 'RegularizedContourSpaceR4', 'FourierLpPostcompR1', 'ContourFourierBalanceR2', 'FubiniTransposeR2', 'FourierFubiniR3', 'BoundedScalarL2LimitR3', 'MaxwellStripCoefficientR5', 'CircularConjugationR1', 'PartialFourierRepresentativeR4', 'MaxwellContourR2', 'GaussianL2RemovalR4', 'PartialFourierWeightedGraphR2', 'MaxwellFourierBalanceR2', 'MaxwellVectorBalanceR1', 'CanonicalSectionCriterionR2', 'RapidityGaussianR1', 'PhysicalCircularRapidityR1', 'MaxwellCanonicalWedgeR2', 'MaxwellLocalizedInclusionR2', 'RealSubspaceRegularizerUniquenessR2', 'MaxwellInclusionAuditR1']
OUTPUT = BASE / "FINAL_MAXWELL_INCLUSION_RECEIPT_R1.json"
REPORT = BASE / "MAXWELL_INCLUSION_R1.md"

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


scope = ['[REAL] O coeficiente físico Maxwell p∧screen tem extensão analítica na rapidez; a fronteira inferior é a conjugada na fibra real com q refletido. A dependência exponencial dos screens foi demonstrada, sem premissa de crescimento adicionada.', '[REAL] A gaussiana na faixa inferior elimina os termos verticais do contorno e fornece integrabilidade horizontal. O balanço espectral ponderado é provado para o coeficiente vetorial Maxwell efetivo.', '[REAL] Fubini e Fourier parcial reais comutam pela densidade tensorial. A transformada integral por seção é identificada com o representante do operador L², e a identidade ponderada entra no grafo do multiplicador existente.', '[REAL] A mudança circular fixa leva a conjugação dos screens reais à troca de helicidades já presente em Jcandidate. O regulador atua na rapidez do mesmo H1 e converge fortemente à identidade.', '[REAL] circularSmear_mem_KWR: para todo teste Maxwell Schwartz real com suporte na cunha direita, o smear circular pertence ao KWR já construído. O domínio TW e a condição SW f=f são consequências dos termos anteriores; o regulador é removido pela closedness de KWR.', '[REAL] localized_rightWedge_le_KWR estende essa inclusão ao subespaço real fechado gerado pelos testes suportados. Não usa igualdade da cunha como hipótese.', '[REAL — genérico condicional] eq_of_regularizers fornece um critério de igualdade real por regularizadores complexolineares Rn→Id e extensões antilineares limitadas Bn, com preservação de M e igualdade Bn=Rn sobre K. Essas premissas e a densidade do span complexo ainda precisam de consumidores físicos.']
limits = ['A igualdade inversa localized(rightWedge)=KWR ainda não foi provada. O campo wedge_glue não é removido por esta inclusão.', 'Densidade complexa de testes suportados na cunha, covariância por boost do subespaço físico e fornecimento dos regularizadores no critério de unicidade são obrigações posteriores.', 'Localidade causal e a rede global completa não são reivindicadas. Não há novo habitante físico, dado observado, confirmação experimental ou alteração de gate.', 'Construção em sandbox, aguardando revisão independente do pai. Fontes anteriores, kernel canônico, um.py, Bancada de produção e memória não foram alterados.']
report = '# Inclusão física Maxwell na cunha canônica — R1\n\n[REAL — compilado em sandbox; revisão independente pendente.]\n\n'
report += '\n'.join('- '+x for x in scope)+'\n\n## Alcance\n\n'+'\n'.join('- '+x for x in limits)
report += f'\n\n{len(accepted)} builds aceitos, {len(decls)} declarações locais auditadas, só o trio e zero sorry. Comando, início, fim, segundos, LEAN_PATH e toolchain constam dos recibos.\n'
write_new(REPORT,report.encode('utf-8'))
result = {'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'unit':'F1.FECHO_20261015','claim':845,
 'status':'COMPILED_CANDIDATE_INDEPENDENT_REVIEW_PENDING','statute':'REAL','scope':scope,'limits':limits,
 'previous_receipt':pin(BASE/'FINAL_PHYSICAL_LOCALIZATION_RECEIPT_R1.json'),
 'accepted':accepted,'all_local_decl_count':len(decls),'all_local_declarations':[{'name':n,'axioms':list(filter(None,a.split(',')))} for n,a in decls],
 'zero_sorry':True,'axioms_only_trio':True,'failed_attempts_preserved':failed,
 'checked_dependencies_and_artifacts':list(checked.values()),'report':pin(REPORT),
 'scripts':[pin(__file__),pin(BASE/'build_orbital_r3.py')],
 'production_modified':False,'memory_modified':False,'gate_modified':False}
write_new(OUTPUT,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'receipt':pin(OUTPUT),'count':len(decls),'accepted':len(accepted)},ensure_ascii=False))
