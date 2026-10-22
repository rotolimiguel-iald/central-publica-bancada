import ContractGroupG_v3

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CONTRATO v3.1 — OS TEOREMAS (leem os campos do tipo `ContratoQG_v31`)
  [RASCUNHO DE GERÊNCIA — frente contrato_v3, RODADA 2, 23/09/2026; scratchpad; NÃO cunha nome reservado]

  §A  unitariedade das translações.
  §B  o que a v2 pedia como campo e a v3/v3.1 DERIVA (Δit fixa Ω; BW geométrico; Poincaré; não-trivial).
  §C  ★★★ COERÊNCIA ESPECTRAL: todo habitante tem Δ^{it} SEM autovetor fora de ℂΩ (oposto da v2).
  §C' ★ as paredes do cético 1 transpostas (T1–T4): U transversal, boost trivial, torre, momento nulo discreto.
  §C''★ os certificados de sinal do cético 2 transpostos: inclusão semilateral, forma de Borchers, orientação.
  §D  ★★ κ: Unruh como relação KMS (β_Killing·κ = 2π); κ = 1/ρ(N); κ FIXO dado N; (W,R) NÃO fixa κ.
  §E  o implementador é ÚNICO.
  §F  as energias: K = 2πB; ★ a energia BILATERAL não tem termo de 1ª ordem (cético 2, transposto).
  §G  o frame.
  §H  ★★★ H3 v3.1: a lei local ao longo do gerador; BH/Clausius/8πG como teoremas de JANELA (integração
      exata); a energia nula não se anula; a expansão não é constante; G NÃO é predito (Jacobson).
  §I  as paredes no par legado e contra translações que comutam com Δit.
  §J  o import indexado.
  β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt.ContratoQGv31

open TGL.SpecificAQFT TGL.ModularRealization
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace ComplexConjugate

noncomputable section

/-! ## §H — ★★★ H3 v3.1 -/

/-- aritmética de pontos no gerador. -/
theorem shift_point (x : Fin 4 → ℝ) (l μ : ℝ) :
    (x + l • nullDir) + (μ - l) • nullDir = x + μ • nullDir := by
  rw [add_assoc, ← add_smul]
  congr 2
  ring

/-- [DERIVED] a carga nula de uma energia nula identicamente nula é 0. -/
theorem nullPlaneCharge_of_zero {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (ψ : W.H)
    (h : ∀ x, nullEnergy T ψ x = 0) : nullPlaneCharge T ψ = 0 := by
  unfold nullPlaneCharge
  have : (fun p : ℝ × (Fin 2 → ℝ) => p.1 * nullEnergy T ψ (p.1 • nullDir + screenEmbed p.2))
      = fun _ => (0:ℝ) := by
    funext p; rw [h, mul_zero]
  rw [this, integral_zero]

/-- [DERIVED] o vácuo não tem energia nula (T_vac). -/
theorem nullEnergy_vac {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (x : Fin 4 → ℝ) :
    nullEnergy T W.vac x = 0 := by
  simp [nullEnergy, pairing, T.T_vac]

/-- [DERIVED] a energia nula é covariante (T_covariant). -/
theorem nullEnergy_covariant {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (a : Fin 4 → ℝ)
    (ψ : W.H) (x : Fin 4 → ℝ) : nullEnergy T (W.U a ψ) x = nullEnergy T ψ (x - a) := by
  simp [nullEnergy, T.T_covariant]

theorem areaDensity_smul (c : ℝ) (h : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) (x : Fin 4 → ℝ) :
    areaDensity (fun y => c • h y) x = c * areaDensity h x := by
  simp [areaDensity]
  ring

namespace ContratoH3

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}
  {T : StressTensorData W}

/-- [DERIVED] a resposta do vácuo é nula (T_vac + propagator_zero). -/
theorem response_vac (C : ContratoH3 W R N T) : C.response W.vac = 0 := by
  unfold ContratoH3.response
  have h : T.T W.vac = 0 := by funext x; exact T.T_vac x
  rw [h, C.propagator_zero]

/-- [DERIVED] ★ a COVARIÂNCIA DA RESPOSTA é teorema (T_covariant + propagator_covariant). -/
theorem response_covariant (C : ContratoH3 W R N T) (a : Fin 4 → ℝ) (ψ : W.H) (x : Fin 4 → ℝ) :
    C.response (W.U a ψ) x = C.response ψ (x - a) := by
  unfold ContratoH3.response
  have h : T.T (W.U a ψ) = fun y => T.T ψ (y - a) := by funext y; exact T.T_covariant a ψ y
  rw [h, C.propagator_covariant]

/-- [DERIVED] ★★ MESMA FONTE, MESMA GEOMETRIA: dois estados com o mesmo ⟨T⟩ têm a mesma resposta (não há escolha
    por estado — a objeção central dos dois céticos). -/
theorem same_source_same_geometry (C : ContratoH3 W R N T) {ψ φ : W.H} (h : T.T ψ = T.T φ) :
    C.response ψ = C.response φ := by
  unfold ContratoH3.response
  rw [h]

/-- [DERIVED] θ é a derivada da densidade de área em TODO parâmetro do gerador (não só em 0). -/
theorem theta_along (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ)
    (l : ℝ) :
    HasDerivAt (fun μ => areaDensity (C.response ψ) (x + μ • nullDir))
      (C.theta ψ (x + l • nullDir)) l := by
  have h := C.theta_is_expansion ψ hψ (x + l • nullDir)
  have h' : HasDerivAt (fun ν : ℝ => areaDensity (C.response ψ) ((x + l • nullDir) + ν • nullDir))
      (C.theta ψ (x + l • nullDir)) (l - l) := by rw [sub_self]; exact h
  have h2 := h'.comp_sub_const l l
  have e : (fun μ : ℝ => areaDensity (C.response ψ) (x + μ • nullDir))
      = fun μ => areaDensity (C.response ψ) ((x + l • nullDir) + (μ - l) • nullDir) := by
    funext μ; rw [shift_point]
  rw [e]; exact h2

/-- [DERIVED] a lei local em TODO parâmetro do gerador. -/
theorem theta_deriv_along (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (l : ℝ) :
    HasDerivAt (fun μ => C.theta ψ (x + μ • nullDir))
      (-(8 * Real.pi * C.G) * nullEnergy T ψ (x + l • nullDir)) l := by
  have h := C.raychaudhuri_einstein ψ hψ (x + l • nullDir)
  have h' : HasDerivAt (fun ν : ℝ => C.theta ψ ((x + l • nullDir) + ν • nullDir))
      (-(8 * Real.pi * C.G) * nullEnergy T ψ (x + l • nullDir)) (l - l) := by
    rw [sub_self]; exact h
  have h2 := h'.comp_sub_const l l
  have e : (fun μ : ℝ => C.theta ψ (x + μ • nullDir))
      = fun μ => C.theta ψ ((x + l • nullDir) + (μ - l) • nullDir) := by
    funext μ; rw [shift_point]
  rw [e]; exact h2

/-- [DERIVED] ★★★ A PRIMEIRA LEI DA JANELA (integração EXATA, sem janela pequena): em todo gerador nulo por x,
    para todo corte c e toda janela [c, d] cuja expansão se anula no fim (equilíbrio, θ(d) = 0),
        a(d) − a(c) = 8πG ∫_c^d (λ − c) T_nn(x + λn) dλ.
    Prova: F(μ) = (μ − c)θ(μ) − a(μ) tem F′ = (μ − c)·θ′ = −8πG(μ − c)T_nn (FTC). -/
theorem first_law_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowArea (C.response ψ) x c d = 8 * Real.pi * C.G * windowCharge T ψ x c d := by
  have hcont : Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir)) :=
    C.energy_continuous ψ hψ x
  have hF : ∀ μ ∈ Set.uIcc c d,
      HasDerivAt (fun μ => (μ - c) * C.theta ψ (x + μ • nullDir)
          - areaDensity (C.response ψ) (x + μ • nullDir))
        (-(8 * Real.pi * C.G) * ((μ - c) * nullEnergy T ψ (x + μ • nullDir))) μ := by
    intro μ _
    have h1 := ((hasDerivAt_id μ).sub_const c).mul (theta_deriv_along C hψ x μ)
    have h2 := theta_along C hψ x μ
    refine (h1.sub h2).congr_deriv ?_
    simp only [id]
    ring
  have hint : IntervalIntegrable
      (fun μ => -(8 * Real.pi * C.G) * ((μ - c) * nullEnergy T ψ (x + μ • nullDir))) volume c d := by
    apply Continuous.intervalIntegrable
    exact continuous_const.mul ((continuous_id.sub continuous_const).mul hcont)
  have hI := intervalIntegral.integral_eq_sub_of_hasDerivAt hF hint
  rw [intervalIntegral.integral_const_mul] at hI
  unfold windowArea windowCharge
  rw [hθ] at hI
  simp only [sub_self, zero_mul, mul_zero, zero_sub] at hI
  linarith [hI]

/-- [DERIVED] ★★ BEKENSTEIN–HAWKING DA JANELA: δS = δA/(4G), com δS = 2π × a carga unilateral do corte. -/
theorem bekenstein_hawking_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowEntropy T ψ x c d = windowArea (C.response ψ) x c d / (4 * C.G) := by
  rw [first_law_window C hψ x c d hθ]
  unfold windowEntropy
  have hG := C.G_pos.ne'
  field_simp
  ring

/-- [DERIVED] CLAUSIUS da janela: δQ = T_U·δS — IDENTIDADE (δS := δQ/T_U, a leitura do cético 2). -/
theorem clausius_window (C : ContratoH3 W R N T) (ψ : W.H) (x : Fin 4 → ℝ) (c d : ℝ) :
    windowHeat C.H2.kappa T ψ x c d = C.H2.unruhTemperature * windowEntropy T ψ x c d := by
  unfold windowHeat windowEntropy ContratoH2.unruhTemperature
  field_simp

/-- [DERIVED] ★ o 8πG da janela: δQ = κ·δA/(8πG). -/
theorem einstein_coefficient_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowHeat C.H2.kappa T ψ x c d
      = C.H2.kappa * windowArea (C.response ψ) x c d / (8 * Real.pi * C.G) := by
  rw [clausius_window, bekenstein_hawking_window C hψ x c d hθ]
  unfold ContratoH2.unruhTemperature
  exact einstein_coefficient_from_clausius _ _ _ C.G_pos.ne'

/-- [DERIVED] κ cancela: δQ/T_U = δS. -/
theorem kappa_cancels_window (C : ContratoH3 W R N T) (ψ : W.H) (x : Fin 4 → ℝ) (c d : ℝ) :
    windowHeat C.H2.kappa T ψ x c d / C.H2.unruhTemperature = windowEntropy T ψ x c d := by
  rw [clausius_window]
  have hT : C.H2.unruhTemperature ≠ 0 := by
    unfold ContratoH2.unruhTemperature
    exact div_ne_zero C.H2.kappa_pos.ne' (by positivity)
  field_simp

/-- [DERIVED] ★ a energia nula NÃO se anula: há estado admissível e ponto com T_nn ≠ 0
    (de `admissible_nontrivial` + `modular_charge`). -/
theorem nontrivial_null_energy (C : ContratoH3 W R N T) :
    ∃ ψ ∈ C.admissible, ∃ x : Fin 4 → ℝ, nullEnergy T ψ x ≠ 0 := by
  obtain ⟨ψ, hψ, k, hk, hk0⟩ := C.admissible_nontrivial
  refine ⟨ψ, hψ, ?_⟩
  by_contra hcon
  push_neg at hcon
  have h := C.modular_charge ψ hψ k hk
  rw [nullPlaneCharge_of_zero T ψ hcon, mul_zero] at h
  exact hk0 h

/-- [DERIVED] ★★ A EXPANSÃO NÃO É CONSTANTE: em todo habitante há estado admissível e gerador em que θ varia.
    (Refuta todo «ajustador» cuja densidade de área é afim ao longo dos geradores.) -/
theorem expansion_not_constant (C : ContratoH3 W R N T) :
    ∃ ψ ∈ C.admissible, ∃ x : Fin 4 → ℝ, ∃ l : ℝ,
      C.theta ψ (x + l • nullDir) ≠ C.theta ψ (x + 0 • nullDir) := by
  obtain ⟨ψ, hψ, x, hx⟩ := nontrivial_null_energy C
  refine ⟨ψ, hψ, x, ?_⟩
  by_contra hcon
  push_neg at hcon
  have hfun : (fun l : ℝ => C.theta ψ (x + l • nullDir)) = fun _ => C.theta ψ (x + 0 • nullDir) := by
    funext l; exact hcon l
  have h := C.raychaudhuri_einstein ψ hψ x
  rw [hfun] at h
  have h0 := h.unique (hasDerivAt_const (0:ℝ) (C.theta ψ (x + 0 • nullDir)))
  have hG : 8 * Real.pi * C.G ≠ 0 := by have := C.G_pos; positivity
  rcases mul_eq_zero.mp h0 with h1 | h1
  · exact hG (neg_eq_zero.mp h1)
  · exact hx h1

/-- [DERIVED] a resposta nula é recusada: se `response ψ = 0` para todo estado admissível, contradição. -/
theorem response_not_identically_zero (C : ContratoH3 W R N T) :
    ¬ ∀ ψ ∈ C.admissible, C.response ψ = 0 := by
  intro h0
  obtain ⟨ψ, hψ, x, l, hne⟩ := expansion_not_constant C
  apply hne
  have hz : ∀ y, C.theta ψ y = 0 := by
    intro y
    have h : HasDerivAt (fun l : ℝ => areaDensity (C.response ψ) (y + l • nullDir)) (C.theta ψ y) 0 :=
      C.theta_is_expansion ψ hψ y
    have hfun : (fun l : ℝ => areaDensity (C.response ψ) (y + l • nullDir)) = fun _ => (0:ℝ) := by
      funext l; rw [h0 ψ hψ]; simp [areaDensity]
    rw [hfun] at h
    exact h.unique (hasDerivAt_const (0:ℝ) (0:ℝ))
  rw [hz, hz]

/-- [DERIVED] ★★ (refuta o ajustador «inclinação por estado» dos céticos, porte linear de `toyResp`/`expFrame`)
    NENHUM habitante tem resposta da forma h_ψ(x) = (c(ψ)·x⁰)·M: a covariância força c ≡ 0, e então a
    resposta é nula — recusada acima. -/
theorem slope_response_excluded (C : ContratoH3 W R N T) (c : W.H → ℝ)
    (M : Matrix (Fin 4) (Fin 4) ℝ) (hresp : ∀ ψ x, C.response ψ x = (c ψ * x 0) • M) : False := by
  apply response_not_identically_zero C
  intro ψ hψ
  by_cases hM : M = 0
  · funext x; rw [hresp, hM, smul_zero]; rfl
  · have hc : c ψ = 0 := by
      have h := C.response_covariant ![1, 0, 0, 0] ψ 0
      rw [hresp, hresp] at h
      simp only [Pi.zero_apply, mul_zero, zero_smul, zero_sub, Pi.neg_apply] at h
      have h' : (c ψ * -(1:ℝ)) • M = 0 := by
        simpa using h.symm
      rcases smul_eq_zero.mp h' with h1 | h1
      · linarith
      · exact absurd h1 hM
    funext x; rw [hresp, hc, zero_mul, zero_smul]; rfl

/-- [DERIVED] ★★ (refuta o porte exponencial do ajustador) NENHUM habitante tem resposta
    h_ψ(x) = (e^{c(ψ)·x⁰} − 1)·M: a covariância força e^{−c(ψ)} = 1, logo c ≡ 0 e a resposta é nula. -/
theorem exp_response_excluded (C : ContratoH3 W R N T) (c : W.H → ℝ)
    (M : Matrix (Fin 4) (Fin 4) ℝ)
    (hresp : ∀ ψ x, C.response ψ x = (Real.exp (c ψ * x 0) - 1) • M) : False := by
  apply response_not_identically_zero C
  intro ψ hψ
  by_cases hM : M = 0
  · funext x; rw [hresp, hM, smul_zero]; rfl
  · have hc : c ψ = 0 := by
      have h := C.response_covariant ![1, 0, 0, 0] ψ 0
      rw [hresp, hresp] at h
      simp only [Pi.zero_apply, mul_zero, Real.exp_zero, sub_self, zero_smul, zero_sub,
        Pi.neg_apply] at h
      have h' : (Real.exp (c ψ * -(1:ℝ)) - 1) • M = 0 := by
        simpa using h.symm
      rcases smul_eq_zero.mp h' with h1 | h1
      · have h2 : Real.exp (c ψ * -(1:ℝ)) = 1 := by linarith
        have h3 := Real.exp_eq_one_iff _ |>.mp h2
        linarith
      · exact absurd h1 hM
    funext x; rw [hresp, hc, zero_mul, Real.exp_zero, sub_self, zero_smul]; rfl

/-- [DERIVED] ★★ o ajustador POR FONTE (o porte mais forte dos céticos na v3.1) é excluído: nenhum habitante
    tem propagador da forma 𝔉(f)(x) = (c(f)·x⁰)·M. -/
theorem slope_propagator_excluded (C : ContratoH3 W R N T)
    (c : ((Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) → ℝ) (M : Matrix (Fin 4) (Fin 4) ℝ)
    (hP : ∀ f x, C.propagator f x = (c f * x 0) • M) : False :=
  slope_response_excluded C (fun ψ => c (T.T ψ)) M (fun ψ x => hP (T.T ψ) x)

/-- [DERIVED] ★★ idem para o porte exponencial por fonte. -/
theorem exp_propagator_excluded (C : ContratoH3 W R N T)
    (c : ((Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) → ℝ) (M : Matrix (Fin 4) (Fin 4) ℝ)
    (hP : ∀ f x, C.propagator f x = (Real.exp (c f * x 0) - 1) • M) : False :=
  exp_response_excluded C (fun ψ => c (T.T ψ)) M (fun ψ x => hP (T.T ψ) x)

/-- ★ G NÃO É PREDITO (rota de Jacobson, G = 1/(4ħη) é entrada): de todo habitante sai outro, com o MESMO H2, a
    MESMA classe e o MESMO T, e G' arbitrário — a resposta escala por G'/G. [KNOWN: Jacobson 1995.] -/
def rescaleG (C : ContratoH3 W R N T) (G' : ℝ) (hG' : 0 < G') : ContratoH3 W R N T where
  H2 := C.H2
  G := G'
  G_pos := hG'
  admissible := C.admissible
  admissible_unit := C.admissible_unit
  vac_admissible := C.vac_admissible
  admissible_translate := C.admissible_translate
  modular_charge := C.modular_charge
  admissible_nontrivial := C.admissible_nontrivial
  energy_continuous := C.energy_continuous
  background_screen_flat := C.background_screen_flat
  propagator := fun f x => (G' / C.G) • C.propagator f x
  propagator_zero := by
    funext x
    rw [C.propagator_zero]
    simp
  propagator_covariant := by
    intro a f
    funext x
    rw [C.propagator_covariant]
  response_symm := by
    intro ψ hψ x
    rw [Matrix.transpose_smul, C.response_symm ψ hψ x]
  lightcone_gauge := by
    intro ψ hψ x
    rw [Matrix.smul_mulVec, C.lightcone_gauge ψ hψ x, smul_zero]
  theta := fun ψ x => (G' / C.G) * C.theta ψ x
  theta_is_expansion := by
    intro ψ hψ x
    have h := (C.theta_is_expansion ψ hψ x).const_mul (G' / C.G)
    have e : (fun l : ℝ => areaDensity (fun y => (G' / C.G) • C.propagator (T.T ψ) y) (x + l • nullDir))
        = fun l => (G' / C.G) * areaDensity (C.propagator (T.T ψ)) (x + l • nullDir) := by
      funext l; exact areaDensity_smul _ _ _
    rw [e]; exact h
  raychaudhuri_einstein := by
    intro ψ hψ x
    have h := (C.raychaudhuri_einstein ψ hψ x).const_mul (G' / C.G)
    refine h.congr_deriv ?_
    have hG := C.G_pos.ne'
    field_simp

theorem G_not_predicted (C : ContratoH3 W R N T) (G' : ℝ) (hG' : 0 < G') :
    ∃ C' : ContratoH3 W R N T, C'.H2 = C.H2 ∧ C'.G = G' ∧ C'.admissible = C.admissible :=
  ⟨rescaleG C G' hG', rfl, rfl, rfl⟩


end ContratoH3

end
end TGLExt.ContratoQGv31

#print axioms TGLExt.ContratoQGv31.shift_point
#print axioms TGLExt.ContratoQGv31.nullPlaneCharge_of_zero
#print axioms TGLExt.ContratoQGv31.nullEnergy_vac
#print axioms TGLExt.ContratoQGv31.nullEnergy_covariant
#print axioms TGLExt.ContratoQGv31.areaDensity_smul
#print axioms TGLExt.ContratoQGv31.ContratoH3.response_vac
#print axioms TGLExt.ContratoQGv31.ContratoH3.response_covariant
#print axioms TGLExt.ContratoQGv31.ContratoH3.same_source_same_geometry
#print axioms TGLExt.ContratoQGv31.ContratoH3.theta_along
#print axioms TGLExt.ContratoQGv31.ContratoH3.theta_deriv_along
#print axioms TGLExt.ContratoQGv31.ContratoH3.first_law_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.bekenstein_hawking_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.clausius_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.einstein_coefficient_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.kappa_cancels_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.nontrivial_null_energy
#print axioms TGLExt.ContratoQGv31.ContratoH3.expansion_not_constant
#print axioms TGLExt.ContratoQGv31.ContratoH3.response_not_identically_zero
#print axioms TGLExt.ContratoQGv31.ContratoH3.slope_response_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH3.exp_response_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH3.slope_propagator_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH3.exp_propagator_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH3.rescaleG
#print axioms TGLExt.ContratoQGv31.ContratoH3.G_not_predicted
