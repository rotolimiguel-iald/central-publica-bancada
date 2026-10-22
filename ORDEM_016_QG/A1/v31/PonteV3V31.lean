import ContratoQG_v3
import ContratoQG_v31

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# PonteV3V31 — H2 v3 ≅ H2 v3.1 a menos do ÍNDICE N   [DEVE COMPILAR]
  Frente contrato_v3, RODADA 2, 23/09/2026. Lê os oleans da v3 (74e2f6be62211c04) SÓ PARA LEITURA (XPATH).

  Certifica que a ÚNICA mudança de H2 da v3 para a v3.1 é promover o observador fiducial a índice externo N:
  todo habitante v3 dá um habitante v3.1 sobre N := (observer, observer_in_wedge) e vice-versa. Logo nada do que
  a rodada 1 mediu sobre H2 (coerência espectral, paredes, brinquedo, legado) se perde, e o que muda é só a
  LEITURA de κ (calibre ⟶ índice). Os homônimos (`KMSAt`, `wedgeBoostMap`, `nullDir`, `killingField`,
  `PositiveEnergy`) coincidem por definição (delta), lema a lema.
-/

namespace TGLExt.ContratoQGv31.Ponte

open TGL.SpecificAQFT TGL.ModularRealization

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

theorem wedgeBoostMap_bridge (s : ℝ) (x : Fin 4 → ℝ) :
    TGLExt.ContratoQGv3.wedgeBoostMap s x = TGLExt.ContratoQGv31.wedgeBoostMap s x := rfl
theorem nullDir_bridge : TGLExt.ContratoQGv3.nullDir = TGLExt.ContratoQGv31.nullDir := rfl
theorem killingField_bridge (κ : ℝ) (x : Fin 4 → ℝ) :
    TGLExt.ContratoQGv3.killingField κ x = TGLExt.ContratoQGv31.killingField κ x := rfl
theorem kms_bridge (α : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) (β : ℝ) :
    TGLExt.ContratoQGv3.KMSAt W α β ↔ TGLExt.ContratoQGv31.KMSAt W α β := Iff.rfl
theorem posEnergy_bridge : TGLExt.ContratoQGv3.PositiveEnergy W ↔ TGLExt.ContratoQGv31.PositiveEnergy W :=
  Iff.rfl

def boost_v31_of_v3 (B : TGLExt.ContratoQGv3.WedgeBoostRep W) : TGLExt.ContratoQGv31.WedgeBoostRep W where
  V := B.V
  V_zero := B.V_zero
  V_add := B.V_add
  V_continuous := B.V_continuous
  V_vac := B.V_vac
  V_translations := B.V_translations
  V_net := B.V_net

def boost_v3_of_v31 (B : TGLExt.ContratoQGv31.WedgeBoostRep W) : TGLExt.ContratoQGv3.WedgeBoostRep W where
  V := B.V
  V_zero := B.V_zero
  V_add := B.V_add
  V_continuous := B.V_continuous
  V_vac := B.V_vac
  V_translations := B.V_translations
  V_net := B.V_net

/-- o índice que um habitante v3 carrega: o seu observador fiducial. -/
def indexOf (C : TGLExt.ContratoQGv3.ContratoH2 W R) : TGLExt.ContratoQGv31.KillingNormalization :=
  ⟨C.observer, C.observer_in_wedge⟩

def v31_of_v3 (C : TGLExt.ContratoQGv3.ContratoH2 W R) :
    TGLExt.ContratoQGv31.ContratoH2 W R (indexOf C) where
  kappa := C.kappa
  kappa_pos := C.kappa_pos
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := boost_v31_of_v3 C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer_unit := C.observer_unit
  E := C.E
  smooth_on := C.smooth_on
  det_unit_on := C.det_unit_on
  dragged := C.dragged
  fiducial_is_modular := C.fiducial_is_modular

def v3_of_v31 {N : TGLExt.ContratoQGv31.KillingNormalization}
    (C : TGLExt.ContratoQGv31.ContratoH2 W R N) : TGLExt.ContratoQGv3.ContratoH2 W R where
  kappa := C.kappa
  kappa_pos := C.kappa_pos
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := boost_v3_of_v31 C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer := N.point
  observer_in_wedge := N.point_in_wedge
  observer_unit := C.observer_unit
  E := C.E
  smooth_on := C.smooth_on
  det_unit_on := C.det_unit_on
  dragged := C.dragged
  fiducial_is_modular := C.fiducial_is_modular

/-- [DERIVED] ★ H2 v3 habitado ⟺ H2 v3.1 habitado para ALGUM índice N: a mudança de H2 é SÓ o índice. -/
theorem h2_v3_iff_v31 :
    Nonempty (TGLExt.ContratoQGv3.ContratoH2 W R) ↔
      ∃ N : TGLExt.ContratoQGv31.KillingNormalization, Nonempty (TGLExt.ContratoQGv31.ContratoH2 W R N) :=
  ⟨fun ⟨C⟩ => ⟨indexOf C, ⟨v31_of_v3 C⟩⟩, fun ⟨_, ⟨C⟩⟩ => ⟨v3_of_v31 C⟩⟩

/-- [DERIVED] e o Δit é o mesmo nas duas leituras (nada do espectro muda). -/
theorem same_Δit (C : TGLExt.ContratoQGv3.ContratoH2 W R) : (v31_of_v3 C).Δit = C.Δit := rfl

#print axioms boost_v31_of_v3
#print axioms boost_v3_of_v31
#print axioms v31_of_v3
#print axioms v3_of_v31
#print axioms h2_v3_iff_v31
#print axioms same_Δit

end

end TGLExt.ContratoQGv31.Ponte
