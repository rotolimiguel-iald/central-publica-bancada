"""Custody of independent semantic reading and verification of existing logs.

No Lean process is launched by this review. No scientific source is changed.
"""
from pathlib import Path
import hashlib
import json
import datetime as dt
import re

HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
TRIO = {"propext", "Classical.choice", "Quot.sound"}
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):
    return {"path": str(p), "sha256": sha(p), "bytes": p.stat().st_size}
def anchor(p, term):
    lines = p.read_text(encoding="utf-8").splitlines()
    found = [i + 1 for i, line in enumerate(lines) if term in line]
    assert found, term
    return {**pin(p), "term": term, "lines": found}

receipt_paths = [
    UNIT / "network_reuse/attempts/20261015T170236_430848Z/RECEIPT.json",
    UNIT / "network_antiunitary/attempts/20261015T172555_279180Z/RECEIPT.json",
]
checked = []
for path in receipt_paths:
    rec = json.loads(path.read_text(encoding="utf-8"))
    assert rec["exit_code"] == 0 and rec["readonly_dependencies_unchanged"] is True
    for artifact in rec["artifacts"]:
        assert sha(Path(artifact["path"])) == artifact["sha256"]
    log = Path(next(a["path"] for a in rec["artifacts"] if a["path"].endswith("BUILD.log")))
    reports = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        if line.startswith("LOCAL_DECL\t"):
            _, name, axioms = line.split("\t", 2)
            reports[name] = [x for x in axioms.split(",") if x]
    assert reports and all(set(x) <= TRIO for x in reports.values())
    checked.append({"receipt": pin(path), "build": pin(log), "exit_code": rec["exit_code"],
                    "local_declarations_audited": len(reports), "all_trio": True,
                    "build_repeated_by_reviewer": False})

assembly = UNIT / "network_reuse/CanonicalFockAssemblyR1.lean"
anti = UNIT / "network_antiunitary/CanonicalFockAntiAssemblyR4.lean"
gamma = UNIT / "network_antiunitary/BosonicGammaJR5.lean"
tensor = UNIT / "network_antiunitary/AntilinearTensorR4.lean"
assert sha(assembly) == json.loads(receipt_paths[0].read_text())["source"]["sha256"]
assert sha(anti) == json.loads(receipt_paths[1].read_text())["source"]["sha256"]

report = {
    "verdict": "PASS_WITH_SCOPE",
    "reviewer": "codex-subagent-tempo_math_review",
    "unit": "F1.FECHO_20261015", "claim_event": 845,
    "time_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "review_kind": "Independent source-level mathematical/semantic review plus custody and parsing of builder logs; no second compilation",
    "source_files": [pin(p) for p in [assembly, anti, gamma, tensor]],
    "compiled_evidence_checked": checked,
    "findings": [
        {"status": "REAL_SOURCE_REVIEW", "claim": "A montagem usa exatamente F1Rede.BosonicFock.F e o H1 canônico já construído; F, vácuo normalizado, infinitude dimensional, Γ, inclusão e continuidades são pagos por termos, não por campos novos assumindo esses resultados.", "anchors": [anchor(assembly, "def RemainingFockInput.toCertificate"), anchor(assembly, "assembled_F_is_concrete")]},
        {"status": "REAL_SOURCE_REVIEW", "claim": "CanonicalNetInput ainda assume LightNetData e a colagem da cunha direita. A recusa de cunha zero tem peso condicional, e a cunha padrão embutida no Fock tem testemunha não nula independente. Não foi construído um habitante da rede global.", "anchors": [anchor(assembly, "structure CanonicalNetInput"), anchor(assembly, "canonicalWedgeInFock_nonzero")]},
        {"status": "REAL_SOURCE_REVIEW", "claim": "Gamma(J) é construído nos mesmos tensores, completações, setores simétricos e soma ℓ²; a semilinearidade por conjugação é preservada. O setor zero conjuga escalares e fixa 1. A involução e a ação no setor de uma partícula são provadas.", "anchors": [anchor(tensor, "def tensorAnti"), anchor(tensor, "def completionAnti"), anchor(gamma, "def gammaJ"), anchor(gamma, "gammaJ_oneParticle")]},
        {"status": "REAL_SOURCE_REVIEW", "claim": "A segunda montagem paga exatamente J, J_invol e J_vac com canonicalFockJ. A identificação modular fica explicitamente no campo tomita, usando esse mesmo J e Gamma(B0(-2πt)); não é deduzida das identidades cinemáticas.", "anchors": [anchor(anti, "def RemainingAnalyticInput.toRemainingFock"), anchor(anti, "  tomita :"), anchor(anti, "antiunitary_fragment_inhabited")]},
        {"status": "OPEN_NAMED_INPUTS", "claim": "Permanecem energia positiva e unicidade do vácuo sob a premissa espectral, álgebra de Weyl e suas leis, ciclicidade/separação/não comutatividade, BW/KMS, realização Tomita, fluxo modular, núcleo/imersão/ação dual/traço/projeções finitas. O contrato final também requer Maxwell, normalização de Killing e G positivo. A presença dessas entradas não exibe habitante do registro completo.", "anchors": [anchor(assembly, "structure RemainingFockInput"), anchor(assembly, "canonical_contract_from_named_imports"), anchor(anti, "structure RemainingAnalyticInput")]},
    ],
    "material_defects_found": [],
    "nonvacuity": {
        "exhibited": ["Fock cinemático com vácuo de norma 1 e dimensão infinita", "cunha padrão não nula transportada por inclusão isométrica", "fragmento antiunitário concreto com J²=I e JΩ=Ω"],
        "not_exhibited": ["CanonicalNetInput global", "RemainingFockInput", "RemainingAnalyticInput", "MaxwellCertificate", "FockCertificate físico completo"],
    },
    "scientific_scope": "Matemática condicional e construção cinemática em sandbox. Nenhuma afirmação de H3 derivado do estado, equivalência do dispositivo, existência global de soluções ou confirmação física.",
    "canonical_changes": False, "providers_called": False, "gate_changed": False,
}
out = HERE / "NETWORK_SEMANTIC_REVIEW_R1.json"
raw = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode()
with out.open("xb") as f:
    f.write(raw)
print(json.dumps({"verdict": report["verdict"], "path": str(out), "sha256": hashlib.sha256(raw).hexdigest(),
                  "local_decl_counts": [r["local_declarations_audited"] for r in checked]}))
