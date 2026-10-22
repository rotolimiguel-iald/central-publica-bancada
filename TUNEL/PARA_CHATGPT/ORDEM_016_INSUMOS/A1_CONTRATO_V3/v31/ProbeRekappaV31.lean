import ContratoQG_v31

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option maxHeartbeats 2000000

/-!
# ProbeRekappaV31 — «κ ESCOLHIDO DEPOIS» contra H2 v3.1   [DIAGNÓSTICO; DEVE FALHAR]
  Frente contrato_v3, RODADA 2, 23/09/2026. Importa SÓ o tipo.

  Porte de `rekappa` (cético 1, BrinqKappaLivre.lean 44b92cdc31abc773) e `regauge` (cético 2,
  CeticoKappaGauge.lean 333a662a8fde1b51): de um habitante C e de κ' ≠ C.kappa, outro habitante NO MESMO TIPO
  INDEXADO `ContratoH2 W R N` com kappa = κ', tudo o mais igual (a constante da fiducial reescalada, como nos
  originais). Na v3 compilava. Aqui o observador NÃO é campo — é o relógio de N — e o dente é `observer_unit`.
  Resultado esperado: {observer_unit}. Refutação em kernel: `ContratoH2.no_rekappa` / `kappa_fixed`.
  (Re-indexar para OUTRO N' compila — `ContratoH2.reindex` — e é dito: o valor de κ é o [INPUT] N.)
-/

namespace TGLExt.ContratoQGv31.ProbeRekappa

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- DEVE FALHAR em `observer_unit` (e só aí). -/
def rekappaPort (C : ContratoH2 W R N) (κ' : ℝ) (hκ' : 0 < κ') (hne : κ' ≠ C.kappa) :
    ContratoH2 W R N where
  kappa := κ'
  kappa_pos := hκ'
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer_unit := by
    first
    | (have h := C.observer_unit
       simp only [minkowskiSq, killingField] at h ⊢
       nlinarith [h, hne])
    | trivial
  E := C.E
  smooth_on := C.smooth_on
  det_unit_on := C.det_unit_on
  dragged := C.dragged
  fiducial_is_modular := by
    first
    | (intro x hx
       obtain ⟨c, hc, h⟩ := C.fiducial_is_modular x hx
       have hk := C.kappa_pos
       refine ⟨c * C.kappa / κ', by positivity, ?_⟩
       rw [h]
       funext i
       simp only [killingField, Pi.smul_apply, smul_eq_mul]
       field_simp)
    | trivial

end

end TGLExt.ContratoQGv31.ProbeRekappa
