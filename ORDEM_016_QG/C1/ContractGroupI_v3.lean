import ContractGroupH_v3

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

namespace ContratoH3
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}
  {T : StressTensorData W}
/-! ### consumidores dos campos de significado (resposta ao cético 2: campo sem consumidor é campo sem dente) -/

/-- [DERIVED] (lê `vac_admissible`) o VÁCUO ESTÁ EM EQUILÍBRIO: θ_Ω ≡ 0. -/
theorem theta_vac (C : ContratoH3 W R N T) (x : Fin 4 → ℝ) : C.theta W.vac x = 0 := by
  have h : HasDerivAt (fun l : ℝ => areaDensity (C.response W.vac) (x + l • nullDir)) (C.theta W.vac x) 0 :=
    C.theta_is_expansion W.vac C.vac_admissible x
  have hfun : (fun l : ℝ => areaDensity (C.response W.vac) (x + l • nullDir)) = fun _ => (0:ℝ) := by
    funext l; rw [response_vac]; simp [areaDensity]
  rw [hfun] at h
  exact h.unique (hasDerivAt_const (0:ℝ) (0:ℝ))

theorem windowCharge_covariant (a : Fin 4 → ℝ) (ψ : W.H) (x : Fin 4 → ℝ) (c d : ℝ) :
    windowCharge T (W.U a ψ) x c d = windowCharge T ψ (x - a) c d := by
  unfold windowCharge
  congr 1
  funext l
  rw [nullEnergy_covariant]
  congr 2
  abel

theorem windowArea_covariant (C : ContratoH3 W R N T) (a : Fin 4 → ℝ) (ψ : W.H) (x : Fin 4 → ℝ)
    (c d : ℝ) : windowArea (C.response (W.U a ψ)) x c d = windowArea (C.response ψ) (x - a) c d := by
  unfold windowArea areaDensity
  rw [response_covariant, response_covariant]
  have e1 : x + d • nullDir - a = x - a + d • nullDir := by abel
  have e2 : x + c • nullDir - a = x - a + c • nullDir := by abel
  rw [e1, e2]

/-- [DERIVED] ★ (lê `admissible_translate`) A LEI VALE EM TODA A FAMÍLIA TRANSLADADA DE HORIZONTES: a primeira
    lei da janela do estado U(a)ψ no gerador por x é a do estado ψ no gerador por x − a — o mesmo G, o mesmo T. -/
theorem first_law_translated (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (a : Fin 4 → ℝ) (x : Fin 4 → ℝ) (c d : ℝ)
    (hθ : C.theta (W.U a ψ) (x + d • nullDir) = 0) :
    windowArea (C.response ψ) (x - a) c d = 8 * Real.pi * C.G * windowCharge T ψ (x - a) c d := by
  have h := first_law_window C (C.admissible_translate a ψ hψ) x c d hθ
  rw [windowArea_covariant, windowCharge_covariant] at h
  exact h

/-- [DERIVED] (lê `lightcone_gauge`) o gerador continua NULO na métrica perturbada: δg_nn = nᵀ h n = 0. -/
theorem response_null_null_zero (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) : pairing (C.response ψ x) nullDir nullDir = 0 := by
  unfold pairing ContratoH3.response
  rw [C.lightcone_gauge ψ hψ x, dotProduct_zero]

/-- [DERIVED] (lê `response_symm` + `lightcone_gauge`) o gauge vale nos DOIS índices: nᵀ h = 0. -/
theorem response_row_null (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) : Matrix.vecMul nullDir (C.response ψ x) = 0 := by
  unfold ContratoH3.response
  rw [← Matrix.mulVec_transpose, C.response_symm ψ hψ x, C.lightcone_gauge ψ hψ x]

/-- [DERIVED] ★ (lê `background_screen_flat`) a DENSIDADE DE ÁREA LINEARIZADA É a variação de primeira ordem da
    área da tela do FUNDO DE H2: d/dε √|det(tela(g_H2 + ε h))| em ε = 0 é −(h₂₂ + h₃₃)/2. -/
theorem areaDensity_is_linearized_area (C : ContratoH3 W R N T) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge)
    (h : Matrix (Fin 4) (Fin 4) ℝ) :
    HasDerivAt (fun ε : ℝ => Real.sqrt |(screenBlock (solderMetric4 (C.H2.E x)⁻¹ + ε • h)).det|)
      (-(h 2 2 + h 3 3) / 2) 0 := by
  have hflat := C.background_screen_flat x hx
  have hb : ∀ ε : ℝ, screenBlock (solderMetric4 (C.H2.E x)⁻¹ + ε • h)
      = screenBlock (solderMetric4 (C.H2.E x)⁻¹) + ε • screenBlock h := by
    intro ε; ext i j; fin_cases i <;> fin_cases j <;> simp [screenBlock]
  set p : ℝ → ℝ := fun ε => (-1 + ε * h 2 2) * (-1 + ε * h 3 3) - (ε * h 2 3) * (ε * h 3 2) with hp
  have hdet : ∀ ε : ℝ, (screenBlock (solderMetric4 (C.H2.E x)⁻¹ + ε • h)).det = p ε := by
    intro ε
    rw [hb, hflat, Matrix.det_fin_two]
    simp [screenBlock, hp]
  have hp0 : p 0 = 1 := by simp [hp]
  have hpd : HasDerivAt p (-(h 2 2 + h 3 3)) 0 := by
    have h1 : HasDerivAt (fun ε : ℝ => -1 + ε * h 2 2) (h 2 2) 0 := by
      simpa using ((hasDerivAt_id (0:ℝ)).mul_const (h 2 2)).const_add (-1)
    have h2 : HasDerivAt (fun ε : ℝ => -1 + ε * h 3 3) (h 3 3) 0 := by
      simpa using ((hasDerivAt_id (0:ℝ)).mul_const (h 3 3)).const_add (-1)
    have h3a : HasDerivAt (fun ε : ℝ => ε * h 2 3) (h 2 3) 0 := by
      simpa using (hasDerivAt_id (0:ℝ)).mul_const (h 2 3)
    have h3b : HasDerivAt (fun ε : ℝ => ε * h 3 2) (h 3 2) 0 := by
      simpa using (hasDerivAt_id (0:ℝ)).mul_const (h 3 2)
    have h3 : HasDerivAt (fun ε : ℝ => (ε * h 2 3) * (ε * h 3 2)) 0 0 := by
      refine (h3a.mul h3b).congr_deriv ?_
      simp
    have := (h1.mul h2).sub h3
    refine this.congr_deriv ?_
    simp only [zero_mul, mul_zero, add_zero, zero_add, sub_zero]
    ring
  have hcont : ContinuousAt p 0 := hpd.continuousAt
  have hpos : ∀ᶠ ε in 𝓝 (0:ℝ), 0 < p ε := by
    have : (0:ℝ) < p 0 := by rw [hp0]; norm_num
    exact hcont.eventually (lt_mem_nhds this)
  have hev : (fun ε : ℝ => Real.sqrt |(screenBlock (solderMetric4 (C.H2.E x)⁻¹ + ε • h)).det|)
      =ᶠ[𝓝 (0:ℝ)] fun ε => Real.sqrt (p ε) := by
    filter_upwards [hpos] with ε hε
    rw [hdet, abs_of_pos hε]
  have hsq : HasDerivAt (fun ε => Real.sqrt (p ε)) (-(h 2 2 + h 3 3) / (2 * Real.sqrt (p 0))) 0 :=
    hpd.sqrt (by rw [hp0]; norm_num)
  rw [hp0, Real.sqrt_one, mul_one] at hsq
  exact hsq.congr_of_eventuallyEq hev

/-- a PROJEÇÃO no consumidor legado `HorizonEquilibriumData`, numa janela de equilíbrio DADA (os números são
    CALCULADOS: δA = a(d) − a(c), δS = 2π·carga, δQ = κ·carga). -/
def toHorizonData (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) : HorizonEquilibriumData where
  kappa := C.H2.kappa
  G := C.G
  G_pos := C.G_pos
  dA := windowArea (C.response ψ) x c d
  dS := windowEntropy T ψ x c d
  dQ := windowHeat C.H2.kappa T ψ x c d
  area_entropy := bekenstein_hawking_window C hψ x c d hθ
  clausius := by
    have := clausius_window C ψ x c d
    unfold ContratoH2.unruhTemperature at this
    exact this

/-- [DERIVED] ★★ o contrato ALIMENTA o teorema mestre (v74), numa janela de equilíbrio dada. -/
theorem feeds_the_master (C : ContratoH3 W R N T)
    {L : Type} [Lattice L] [BoundedOrder L] {Tr : SubadditiveTraceData L}
    (S : SusyRelativeData L Tr) {x₀ : Fin 4 → ℝ} (hx₀ : x₀ ∈ rightWedge)
    {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ) (c d : ℝ)
    (hθ : C.theta ψ (x + d • nullDir) = 0) :
    (0 < Tr.tau S.ker ∧ Tr.tau S.ker < ⊤) ∧
      Tr.tau S.ker / Tr.tau S.ker = 1 ∧
      ((C.H2.E x₀)⁻¹ * C.H2.E x₀ = 1 ∧ LorentzByCongruence (solderMetric4 (C.H2.E x₀)⁻¹)) ∧
      (C.toHorizonData hψ x c d hθ).dQ = (C.toHorizonData hψ x c d hθ).kappa
        * (C.toHorizonData hψ x c d hθ).dA / (8 * Real.pi * (C.toHorizonData hψ x c d hθ).G) :=
  emergence_master_full_triad S (C.H2.E x₀) (C.H2.det_unit_on x₀ hx₀) (C.toHorizonData hψ x c d hθ)

end ContratoH3

end
end TGLExt.ContratoQGv31

#print axioms TGLExt.ContratoQGv31.ContratoH3.theta_vac
#print axioms TGLExt.ContratoQGv31.ContratoH3.windowCharge_covariant
#print axioms TGLExt.ContratoQGv31.ContratoH3.windowArea_covariant
#print axioms TGLExt.ContratoQGv31.ContratoH3.first_law_translated
#print axioms TGLExt.ContratoQGv31.ContratoH3.response_null_null_zero
#print axioms TGLExt.ContratoQGv31.ContratoH3.response_row_null
#print axioms TGLExt.ContratoQGv31.ContratoH3.areaDensity_is_linearized_area
#print axioms TGLExt.ContratoQGv31.ContratoH3.toHorizonData
#print axioms TGLExt.ContratoQGv31.ContratoH3.feeds_the_master
