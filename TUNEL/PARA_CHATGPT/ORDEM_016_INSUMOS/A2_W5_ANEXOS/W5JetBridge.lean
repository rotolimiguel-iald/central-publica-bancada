import ContratoQG
import TGLExt.ModularSignatureObstruction
import TGLExt.ClosureCertificate

set_option autoImplicit false

/-!
# W5_final — três pontes pequenas para a ORDEM 014 (A3 = H2), sobre o ANEXO A

  [RASCUNHO DE GERÊNCIA, frente W5_final, 23/09/2026 — scratchpad; NÃO entra no kernel nesta sessão]

  1. HOMÔNIMO ATÉ PROVA, pago aqui: `ChatgptAudit.boost4` (ModularSignatureObstruction.lean:26, onde
     vivem as paredes 1 e 2) e `TGLExt.boostMat` (PoincareGroup.lean:153, que o ANEXO A usa em
     `wedgeBoostMap`/`dragged`) são DUAS definições da mesma matriz sem lema algum ligando-as
     (grep em 23/09). `boost4_eq_boostMat` é a ponte; sem ela, citar a parede 2 contra o contrato
     seria o erro de encadear homônimos (regra dos dois regimes, item 2).
  2. O JATO: `killingField κ` (definido no ANEXO A por fórmula) É a derivada em s = 0 da ação
     geométrica s ↦ wedgeBoostMap (κ·s) — o campo de Killing é LIDO da ação, não posto.
     Isto NÃO amarra κ ao parâmetro KMS de Δit (C4 do cético W2 continua [OPEN]).
  3. O TIPO DO FRAME: o frame do jato não é um `SmoothFrameData` global (det = κ·x¹ anula-se em
     x¹ = 0) — `jetFrame_is_not_a_global_SmoothFrameData`.

  Estatutos: tudo [DERIVED] (provado aqui). β jamais aparece. Sem sorry, sem axiom.
-/

namespace W5Final

open TGLExt TGLExt.ContratoQG Matrix

/-- [DERIVED] ★ a ponte do homônimo: as duas matrizes de boost do kernel coincidem entrada a entrada. -/
theorem boost4_eq_boostMat (s : ℝ) : ChatgptAudit.boost4 s = TGLExt.boostMat s := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [ChatgptAudit.boost4, TGLExt.boostMat]

/-- [DERIVED] a parede 2 (`no_injective_isometric_boost_intertwiner`) reescrita com a matriz do ANEXO A:
    nenhuma isometria entrelaça injetivamente ℝ⁴ com `boostMat s`, s ≠ 0 — em QUALQUER H. -/
theorem no_injective_isometric_boostMat_intertwiner {H : Type*}
    [NormedAddCommGroup H] [NormedSpace ℝ H] (U : H →ₗᵢ[ℝ] H)
    (F : (Fin 4 → ℝ) →ₗ[ℝ] H) (hF : Function.Injective F) {s : ℝ}
    (hintertwine : ∀ v, U (F v) = F ((TGLExt.boostMat s).mulVec v)) : s = 0 :=
  ChatgptAudit.no_injective_isometric_boost_intertwiner U F hF
    (fun v => by rw [boost4_eq_boostMat]; exact hintertwine v)

/-- a ação geométrica em coordenadas. -/
theorem wedgeBoostMap_eq (s : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s x = ![Real.cosh s * x 0 + Real.sinh s * x 1,
                          Real.sinh s * x 0 + Real.cosh s * x 1, x 2, x 3] := by
  funext i
  fin_cases i <;> simp [wedgeBoostMap, TGLExt.boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

/-- [DERIVED] ★ O JATO: o campo de Killing do ANEXO A é a derivada, em s = 0, da ação geométrica do boost
    à taxa de rapidez κ: d/ds|₀ Λ(κs)·x = κ·(x¹, x⁰, 0, 0) = killingField κ x. -/
theorem killingField_is_the_jet (κ : ℝ) (x : Fin 4 → ℝ) :
    HasDerivAt (fun s : ℝ => wedgeBoostMap (κ * s) x) (killingField κ x) 0 := by
  have hl : HasDerivAt (fun s : ℝ => κ * s) κ 0 := by
    simpa using (hasDerivAt_id (0 : ℝ)).const_mul κ
  have h0 : HasDerivAt (fun s : ℝ => Real.cosh (κ * s) * x 0 + Real.sinh (κ * s) * x 1)
      (κ * x 1) 0 := by
    refine (((hl.cosh).mul_const (x 0)).add ((hl.sinh).mul_const (x 1))).congr_deriv ?_
    simp
  have h1 : HasDerivAt (fun s : ℝ => Real.sinh (κ * s) * x 0 + Real.cosh (κ * s) * x 1)
      (κ * x 0) 0 := by
    refine (((hl.sinh).mul_const (x 0)).add ((hl.cosh).mul_const (x 1))).congr_deriv ?_
    simp
  rw [hasDerivAt_pi]
  intro i
  fin_cases i
  · simpa [wedgeBoostMap_eq, killingField] using h0
  · simpa [wedgeBoostMap_eq, killingField] using h1
  · simpa [wedgeBoostMap_eq, killingField] using hasDerivAt_const (0 : ℝ) (x 2)
  · simpa [wedgeBoostMap_eq, killingField] using hasDerivAt_const (0 : ℝ) (x 3)

/-- [DERIVED] ★ o frame do jato NÃO é um `SmoothFrameData` (o tipo global de ClosureCertificate.lean:98):
    em x = 0 (na aresta, no hiperplano x¹ = 0) o determinante é κ·0 = 0. -/
theorem jetFrame_is_not_a_global_SmoothFrameData (κ : ℝ) :
    ¬ ∃ f : SmoothFrameData, f.E = jetFrame κ := by
  rintro ⟨f, hf⟩
  have h := f.det_unit 0
  rw [hf, jetFrame_det] at h
  simp at h

/-- [DERIVED] fora da cunha o frame do jato TAMBÉM é invertível onde x¹ ≠ 0 (ex.: x = (2,1,0,0), κ = 1):
    a regionalidade é do hiperplano x¹ = 0, não da fronteira da cunha (D1 do cético de W5). -/
theorem jetFrame_invertible_off_wedge :
    (![2, 1, 0, 0] : Fin 4 → ℝ) ∉ TGL.SpecificAQFT.rightWedge ∧
      IsUnit (jetFrame 1 ![2, 1, 0, 0]).det := by
  refine ⟨?_, ?_⟩
  · intro h
    have h' : |(![(2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1 := h
    simp at h'
  · rw [jetFrame_det]
    simp

#print axioms boost4_eq_boostMat
#print axioms no_injective_isometric_boostMat_intertwiner
#print axioms killingField_is_the_jet
#print axioms jetFrame_is_not_a_global_SmoothFrameData
#print axioms jetFrame_invertible_off_wedge

end W5Final
