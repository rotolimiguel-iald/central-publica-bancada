import ContratoQG_v3_Teoremas

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CÉTICO 2 (vacuidade/fidelidade) — κ É CALIBRE NA v3; e a COERÊNCIA DE SINAL de BW com Borchers
  [DIAGNÓSTICO do cético; scratchpad cetico_vacuidade; nunca importado pelo kernel; NÃO cunha nome reservado]

  §1 `kappa_is_gauge`: dado QUALQUER habitante C de `ContratoH2 W R` e QUALQUER κ' > 0, há outro habitante
     C' no MESMO par, com o MESMO Δit, o MESMO grupo de boosts, o MESMO frame E e o MESMO bloco (P), e
     C'.kappa = κ'. Só mudam o observador (ρ = 1/κ') e a constante c da fiducial. Logo o tipo NÃO amarra κ
     a nada espectral: κ é a normalização (calibre) do campo de Killing, escolhida pelo observador.
  §2 coerência de sinal (o que a v3 não confere em kernel, porque `positive_energy` não tem consumidor):
     (a) a covariância do kernel (Ad U(a)·net(O) = net(O+a)) dá a inclusão SEMILATERAL
         Ad U(λn)·net(cunha) ⊆ net(cunha) para λ ≥ 0;
     (b) `bw` + `V_translations` dão Δ^{it} U(λn) Δ^{−it} = U(e^{−2πt} λ n) — a FORMA de Borchers
         (gerador positivo + inclusão semilateral ⟹ e^{−2πt}) [KNOWN: Borchers 1992];
     (c) a orientação de `PositiveEnergy` (semiplano SUPERIOR) é a de U = e^{+ia·P} com a·P ≥ 0.
     Juntos: os sinais de `bw`, `kms` (conferido à mão contra Takesaki/BR) e `positive_energy` são
     COERENTES entre si e com a convenção de covariância do kernel. Não há vacuidade de sinal.
-/

namespace TGLExt.ContratoQGv3.CeticoVacuidade

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open Complex
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- o observador na distância de Rindler ρ = 1/κ'. -/
def gaugeObserver (κ' : ℝ) : Fin 4 → ℝ := ![0, 1 / κ', 0, 0]

/-- RE-CALIBRAR κ: tudo igual, exceto κ, o observador e a constante da fiducial. -/
def regauge (C : ContratoH2 W R) (κ' : ℝ) (hκ' : 0 < κ') : ContratoH2 W R where
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
  observer := gaugeObserver κ'
  observer_in_wedge := by
    show |(![0, 1 / κ', 0, 0] : Fin 4 → ℝ) 0| < (![0, 1 / κ', 0, 0] : Fin 4 → ℝ) 1
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one, abs_zero]
    positivity
  observer_unit := by
    simp [minkowskiSq, killingField, gaugeObserver, hκ'.ne']
  E := C.E
  smooth_on := C.smooth_on
  det_unit_on := C.det_unit_on
  dragged := C.dragged
  fiducial_is_modular := by
    intro x hx
    obtain ⟨c, hc, h⟩ := C.fiducial_is_modular x hx
    refine ⟨c * C.kappa / κ', by have := C.kappa_pos; positivity, ?_⟩
    rw [h]
    unfold killingField
    rw [smul_smul, smul_smul]
    congr 1
    field_simp

/-- [DERIVED] ★★ κ É CALIBRE: todo κ' > 0 é realizado no MESMO par, com o MESMO Δit, o MESMO grupo de boosts,
    o MESMO frame. O tipo v3 não liga κ ao espectro de Δ (que é o mesmo para todos os κ'). -/
theorem kappa_is_gauge (C : ContratoH2 W R) (κ' : ℝ) (hκ' : 0 < κ') :
    ∃ C' : ContratoH2 W R, C'.kappa = κ' ∧ C'.Δit = C.Δit ∧ C'.boost = C.boost ∧ C'.E = C.E :=
  ⟨regauge C κ' hκ', rfl, rfl, rfl, rfl⟩

/-- [DERIVED] a temperatura de Unruh do contrato é, portanto, QUALQUER T > 0 no mesmo par (T = κ'/2π). -/
theorem unruhTemperature_is_free (C : ContratoH2 W R) (T : ℝ) (hT : 0 < T) :
    ∃ C' : ContratoH2 W R, C'.unruhTemperature = T ∧ C'.Δit = C.Δit := by
  refine ⟨regauge C (2 * Real.pi * T) (by positivity), ?_, rfl⟩
  show 2 * Real.pi * T / (2 * Real.pi) = T
  field_simp

/-- [DERIVED] o conjunto dos κ realizados num par habitado é (0, ∞) inteiro. -/
theorem kappa_set_is_all_positive (h : Nonempty (ContratoH2 W R)) :
    {κ : ℝ | ∃ C : ContratoH2 W R, C.kappa = κ} = Set.Ioi 0 := by
  ext κ
  constructor
  · rintro ⟨C, rfl⟩; exact C.kappa_pos
  · intro hκ
    obtain ⟨C⟩ := h
    exact ⟨regauge C κ hκ, rfl⟩

/-! ## §2 — coerência de sinal -/

/-- [DERIVED] a cunha transladada por λn (λ ≥ 0) cabe na cunha. -/
theorem translate_null_subset (l : ℝ) (hl : 0 ≤ l) :
    TGL.SpecificAQFT.translate (l • nullDir) rightWedge ⊆ rightWedge := by
  rintro _ ⟨x, hx, rfl⟩
  have hx' : |x 0| < x 1 := hx
  obtain ⟨h1, h2⟩ := abs_lt.mp hx'
  show |(x + l • nullDir) 0| < (x + l • nullDir) 1
  simp only [Pi.add_apply, Pi.smul_apply, nullDir, smul_eq_mul, Matrix.cons_val_zero,
    Matrix.cons_val_one, mul_one]
  rw [abs_lt]
  constructor <;> linarith

/-- [DERIVED] ★ (a) A INCLUSÃO SEMILATERAL, da covariância e da isotonia do kernel:
    Ad U(λn)·net(cunha) ⊆ net(cunha) para λ ≥ 0. -/
theorem halfsided_inclusion (W : TGLSpecificAQFTWitness) (l : ℝ) (hl : 0 ≤ l)
    (T : W.H →L[ℂ] W.H) (hT : T ∈ W.net rightWedge) :
    W.U (l • nullDir) * T * W.U (-(l • nullDir)) ∈ W.net rightWedge := by
  have h := (W.covariance (l • nullDir) rightWedge T).mp hT
  exact W.isotony _ _ (translate_null_subset l hl) h

/-- [DERIVED] ★ (b) A FORMA DE BORCHERS no contrato: Δ^{it} U(λn) Δ^{−it} = U(e^{−2πt}·λ·n) — o sinal
    que o teorema de Borchers impõe a um gerador positivo com a inclusão semilateral de (a). -/
theorem contract_borchers_form (C : ContratoH2 W R) (t l : ℝ) :
    (C.Δit t).conjStarAlgEquiv (W.U (l • nullDir))
      = W.U ((Real.exp (-(2 * Real.pi * t)) * l) • nullDir) := by
  rw [C.poincare_relation, wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul, mul_comm l]

/-- [DERIVED] (c) a orientação de `PositiveEnergy`: para λ ≥ 0, z ↦ e^{izλ} (a correlação de um autovetor de
    a·P de autovalor λ, com U = e^{+ia·P}) é limitada por 1 no semiplano superior fechado. -/
theorem positiveEnergy_orientation (lam : ℝ) (hlam : 0 ≤ lam) (z : ℂ) (hz : 0 ≤ z.im) :
    ‖Complex.exp (I * z * lam)‖ ≤ 1 := by
  rw [Complex.norm_exp]
  have : (I * z * (lam : ℂ)).re = -(z.im * lam) := by
    simp [Complex.mul_re, Complex.mul_im]
  rw [this, Real.exp_le_one_iff]
  have := mul_nonneg hz hlam
  linarith

#print axioms regauge
#print axioms kappa_is_gauge
#print axioms unruhTemperature_is_free
#print axioms kappa_set_is_all_positive
#print axioms translate_null_subset
#print axioms halfsided_inclusion
#print axioms contract_borchers_form
#print axioms positiveEnergy_orientation

end

end TGLExt.ContratoQGv3.CeticoVacuidade
