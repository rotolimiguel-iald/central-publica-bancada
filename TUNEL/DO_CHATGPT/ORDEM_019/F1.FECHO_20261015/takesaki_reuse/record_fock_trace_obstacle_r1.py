"""Source-anchored status of the trace on the new concrete Fock regular core.
Read sources; write one new derived report. No theorem construction or build.
"""
from pathlib import Path
import datetime, hashlib, json, os
HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
K = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")
def pin(path, patterns):
    raw = path.read_bytes(); lines = raw.decode("utf-8").splitlines()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "anchors": {p: [{"line": i + 1, "text": x} for i,x in enumerate(lines) if p in x]
                        for p in patterns}}
sources = [
    pin(UNIT / "takesaki_fock" / "CanonicalFockRegularCoreR2.lean", ["def fockFlow", "abbrev core", "regular_covariance", "dual_fixes_embedding", "dual_eigencharacter"]),
    pin(UNIT / "wedge_cyclic" / "WedgeCyclicR3.lean", ["canonical_wedge_cyclic", "canonical_wedge_separating"]),
    pin(UNIT / "weyl_net_wiring" / "PairClosedTomitaR2.lean", ["def closedTomita", "closedTomita_graph_eq", "does not assert"]),
    pin(K / "V350DualWeightForm.lean", ["def dualQuadraticIntegral", "theorem dualQuadraticIntegral_dual_invariant", "theorem dualQuadraticIntegral_one"]),
    pin(K / "V350ScalarDualWeight.lean", ["def scalarDualWeight", "scalarDualWeight_faithful", "scalarDualWeight_normal"]),
    pin(K / "V350ScalarDualWeightFaithfulness.lean", ["fixedCore_regularVacuum_separating", "dualQuadraticIntegral_vacuum_faithful", "dualFixedCore_eq_amplified_base"]),
    pin(K / "V350RegularCoreCommutant.lean", ["fibre_mem_regularCore_iff", "twistedCommutantLift_mem"]),
    pin(K / "V351ScalarImaginaryCoreAction.lean", ["matrixUnit_regular_core_conjugation", "scalarTomitaImaginaryPower_core_conjugation"]),
    pin(K / "V351ModularImplementation.lean", ["scalarTomitaImaginaryPower_eq_regular_implementation"]),
    pin(K / "V351ModularCutBalance.lean", ["scalarTomitaImaginaryPower_eq_regular_implementation", "theorem regular", "Balance of the existing"]),
    pin(K / "V351InverseLimitWeight.lean", ["def scalarInverseCutoffWeight", "def scalarInverseLimitWeight"]),
    pin(K / "V351RegularCoreTraceConstruction.lean", ["def scalarInverseLimitTraceData", "tracial :=", "dual_scaling :="]),
    pin(K / "V354RegularLegacyWitness.lean", ["def regularLegacyCore", "canonicalTrace :=", "trace_dual_scaling :="]),
    pin(K / "V354PositiveShiftCompatibility.lean", ["cyclicTraceCandidate_positive"]),
]
report = {
    "unit": "F1.FECHO_20261015", "claim": 845, "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "OBSTACULO_DE_TRANSPORTE_IDENTIFICADO_SEM_AUSENCIA_GLOBAL_ALEGADA",
    "scope": "Leitura delimitada das construcoes atuais; este recibo nao e nova prova Lean nem nova execucao cientifica.",
    "sources": sources,
    "already_constructed": [
        "[REAL por recibos anteriores] M=R(KWR) e o vacuo ciclico/separante na mesma Fock F; U_t=Gamma(B0(-2*pi*t)) preserva M.",
        "[REAL por recibo FOCK_REGULAR_CORE_RECEIPT_R1] N_F={fibre M, Uregular_t}'' em L2(R;F), embedding injetivo, covariancia, grupo dual theta_s e caracteres.",
        "[REAL no kernel original] N_P da torre V351 tem peso perturbado fiel normal semifinito tracial e escala exp(-s); V354 fornece leitor ciclico total compatível com o cone positivo."
    ],
    "weight_that_is_available_without_renaming": {
        "formula": "phi_F(A)=dualQuadraticIntegral(A,testVector(vacuum)), A in (N_F)+",
        "domain": "Positive bounded operators of the ACTUAL Fock regular core on L2(R;F)",
        "reusable_generic_lemmas": ["zero", "additivity on positives", "nonnegative homogeneity", "monotonicity", "dual invariance", "phi_F(1)=infinity because testVector(vacuum) is nonzero"],
        "statute": "DERIVED formula with existing generic lemmas; no new compiled Fock weight module claimed",
        "warning": "This is the dual weight, invariant under theta. It is not the exp(-s)-scaling trace. Infinite unit value does not establish semifiniteness or trace."
    },
    "transport_route": {
        "sufficient_object": "A concrete star-algebra isomorphism Phi:N_F -> N_P with Phi(thetaF_s(A))=thetaP_s(Phi(A)), carrying the actual ordered positive cones and normal suprema.",
        "spatial_sufficient_realization": "A unitary W:L2(R;F) -> L2(R;TowerHilbert P) mapping N_F onto N_P and intertwining the dual character automorphisms gives Phi(A)=W A W*. Mere Hilbert-space isomorphism is insufficient.",
        "conclusion_if_constructed": "tauF(A)=tauP(Phi(A)); positivity/order/normality/semifiniteness/traciality transport, and theta-intertwining gives exp(-s) scaling. No trace_scaling premise on Fock is introduced.",
        "current_status": "OPEN: no such concrete Phi or W was found in the inspected construction. This report does not prove that none can exist.",
        "avoid_overspecification": "Mapping the tower vacuum and its flow as well would be a stronger requirement, needing spectral compatibility. No unsupported impossibility assertion is made."
    },
    "direct_construction_route": {
        "step1": "Generalize the fixed-core identification N_F^theta=fibre(M), and the dual-resolvent membership proof; the existing Fock separating vacuum can then pay the faithfulness argument of V350ScalarDualWeightFaithfulness.",
        "step2": "Construct the scalar GNS for phi_F and identify its actual Tomita imaginary powers with left regular U_t times the commuting right implementation. In V351 this equality is proved on tower matrix units then extended by density.",
        "step3": "Transport/generalize the inverse-generator cutoffs and ModularCutBalance to those SAME GNS and regular representations, then reuse the monotone cutoff construction for tau_F.",
        "concrete_missing_identity": "The Fock pair's closed Tomita graph is constructed, but its polar/modular identification does not follow from closedness or boost covariance. The analogous scalar-dual-weight GNS modular implementation must be established on an actual total core, replacing the tower matrix-unit argument.",
        "scope": "No total trace field is filled merely by naming the V351 trace on another algebra; the construction is not closed by a theorem that assumes its own requested scaling property."
    },
    "no_new_claims": ["No full Takesaki duality", "No Fock-to-tower equivalence", "No faithful semifinite trace on N_F yet", "No change to canonical sources, runtime or gate"]
}
dest = HERE / "FOCK_TRACE_REUSE_AND_OBSTACLE_R1.json"
raw = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode()
tmp = dest.with_name(dest.name + ".tmp")
if dest.exists() or tmp.exists(): raise FileExistsError(dest)
with tmp.open("xb") as f:
    f.write(raw); f.flush(); os.fsync(f.fileno())
assert tmp.stat().st_size == len(raw)
tmp.rename(dest)
print(json.dumps({"report": str(dest), "sha256": hashlib.sha256(raw).hexdigest(), "sources": len(sources)}, ensure_ascii=False))
