import ContratoQG_v31
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option maxHeartbeats 2000000

/-!
# ProbeAjustadorV31 — OS AJUSTADORES DOS CÉTICOS contra H3 v3.1   [DIAGNÓSTICO; DEVE FALHAR]
  Frente contrato_v3, RODADA 2, 23/09/2026. Importa SÓ o tipo (+ a cópia do brinquedo, para o `geoFrame`).

  PORTES, na maior fidelidade que a v3.1 permite, dos ataques que HABITAVAM H3 v3:
  * `toyH3` (cético 1, BrinqH3Toy.lean 56020eb8c8beb6a9) e `adjustH3` (cético 2, CeticoH3Ajuste.lean
    e986f2bac15c978a): a resposta é escolhida POR ESTADO por um número c(ψ) — na v3 um frame e^{−c x⁰}; aqui, no
    tipo linearizado, a perturbação h(x) = (c·x⁰)·diag(0,0,−1,−1) (densidade de área a = c·x⁰, variação de área c
    por unidade de λ — o análogo exato), com o número c escolhido POR FONTE, c(T(ψ)), porque na v3.1 a resposta
    é 𝔉(T(ψ)) (o ajustador mais forte possível no tipo). TUDO o que não é o dente é concedido como hipótese (a classe,
    o elo `modular_charge`, a continuidade, a planura do fundo) — para que o erro caia SÓ nos dentes novos.
    Resultado esperado: {propagator_covariant, raychaudhuri_einstein}. Refutações em kernel (não só «não achei
    prova»): `ContratoH3.slope_propagator_excluded`, `ContratoH3.expansion_not_constant` (Teoremas).
  * a matéria POR ESTADO (`toyMatter`, c·e₀₀): na v3.1 a matéria é ÍNDICE; o porte é construí-la como
    `StressTensorData` com amplitude m(ψ) por estado. Resultado esperado: {T_covariant} (m não é invariante por
    translação em geral — falha por falta de prova; a refutação depende de W e NÃO está formalizada).
  * `genericImport` / `toyImport`: o import pelo ajustador — compila SÓ herdando `sorryAx` do porte (medido no
    `#print axioms`).
  * `H3_of_H2_geo` (cético 2, CeticoGeoFrame.lean 6b1374b5b9b3ed0f): o `geoFrame` PAGA a planura do fundo
    (`geoFrame_screen_flat`, provado) — logo a falha acima NÃO vem do fundo.
-/

namespace TGLExt.ContratoQGv31.ProbeAjustador

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
open MeasureTheory Complex Matrix
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- a matriz transversal: a((c·x⁰)·M) = c·x⁰. -/
def transverseM : Matrix (Fin 4) (Fin 4) ℝ := Matrix.diagonal ![0, 0, -1, -1]

/-- 1. ★ O PORTE DO AJUSTADOR — DEVE FALHAR em {propagator_covariant, raychaudhuri_einstein}. Na v3.1 a
    resposta tem de ser um funcional FIXO da fonte: o ajustador escolhe o número c(f) POR FONTE (o análogo
    exato do c(ψ) por estado dos céticos, agora obrigado a passar pela fonte T(ψ)). -/
def adjusterPort (C2 : ContratoH2 W R N) (T : StressTensorData W) (G : ℝ) (hG : 0 < G)
    (A : Set W.H) (hAu : ∀ ψ ∈ A, ‖ψ‖ = 1) (hAv : W.vac ∈ A)
    (hAt : ∀ (a : Fin 4 → ℝ) (ψ : W.H), ψ ∈ A → W.U a ψ ∈ A)
    (hmc : ∀ ψ ∈ A, ∀ k : ℝ, HasModularEnergy C2.Δit ψ k → k = 2 * Real.pi * nullPlaneCharge T ψ)
    (hAn : ∃ ψ ∈ A, ∃ k : ℝ, HasModularEnergy C2.Δit ψ k ∧ k ≠ 0)
    (hcont : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ, Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir)))
    (hflat : ∀ x ∈ rightWedge, screenBlock (solderMetric4 (C2.E x)⁻¹) = -1)
    (c : ((Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) → ℝ) (hc0 : c 0 = 0) : ContratoH3 W R N T where
  H2 := C2
  G := G
  G_pos := hG
  admissible := A
  admissible_unit := hAu
  vac_admissible := hAv
  admissible_translate := hAt
  modular_charge := hmc
  admissible_nontrivial := hAn
  energy_continuous := hcont
  background_screen_flat := hflat
  propagator := fun f x => (c f * x 0) • transverseM
  propagator_zero := by
    first
    | (funext x; rw [hc0, zero_mul, zero_smul]; rfl)
    | trivial
  propagator_covariant := by
    first
    | (intro a f
       funext x
       simp only [Pi.sub_apply]
       congr 1
       ring)
    | trivial
  response_symm := by
    first
    | (intro ψ hψ x; rw [Matrix.transpose_smul]; unfold transverseM; rw [Matrix.diagonal_transpose])
    | trivial
  lightcone_gauge := by
    first
    | (intro ψ hψ x
       rw [Matrix.smul_mulVec]
       have h0 : transverseM *ᵥ nullDir = 0 := by
         funext i; fin_cases i <;> simp [transverseM, nullDir, Matrix.mulVec_diagonal]
       rw [h0, smul_zero])
    | trivial
  theta := fun ψ _ => c (T.T ψ)
  theta_is_expansion := by
    first
    | (intro ψ hψ x
       show HasDerivAt (fun l : ℝ => areaDensity (fun y => (c (T.T ψ) * y 0) • transverseM) (x + l • nullDir))
         (c (T.T ψ)) 0
       have e : (fun l : ℝ => areaDensity (fun y => (c (T.T ψ) * y 0) • transverseM) (x + l • nullDir))
           = fun l => c (T.T ψ) * x 0 + c (T.T ψ) * l := by
         funext l; simp [areaDensity, transverseM, nullDir]; ring
       rw [e]
       have := ((hasDerivAt_id (0:ℝ)).const_mul (c (T.T ψ))).const_add (c (T.T ψ) * x 0)
       simpa using this)
    | trivial
  raychaudhuri_einstein := by
    first
    | (intro ψ hψ x
       exact (hasDerivAt_const (0:ℝ) (c (T.T ψ))).congr_deriv (by ring))
    | trivial

/-- 2. ★ O PORTE DA MATÉRIA POR ESTADO — DEVE FALHAR em {T_covariant}. -/
def matterPort (m : W.H → ℝ) (hm0 : m W.vac = 0) : StressTensorData W where
  T := fun ψ _ => Matrix.diagonal ![m ψ, 0, 0, 0]
  T_vac := by
    first
    | (intro x; rw [hm0]; ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.diagonal])
    | trivial
  T_covariant := by
    first
    | (intro a ψ x; rfl)
    | trivial

/-- 3. O PORTE DO IMPORT GENÉRICO (compila herdando `sorryAx` de `adjusterPort`: ver `#print axioms`). -/
def genericImportPort (h2 : ContratoH2 W R N) (T : StressTensorData W) (G : ℝ) (hG : 0 < G)
    (A : Set W.H) (hAu : ∀ ψ ∈ A, ‖ψ‖ = 1) (hAv : W.vac ∈ A)
    (hAt : ∀ (a : Fin 4 → ℝ) (ψ : W.H), ψ ∈ A → W.U a ψ ∈ A)
    (hmc : ∀ h : ContratoH2 W R N, ∀ ψ ∈ A, ∀ k : ℝ, HasModularEnergy h.Δit ψ k →
      k = 2 * Real.pi * nullPlaneCharge T ψ)
    (hAn : ∀ h : ContratoH2 W R N, ∃ ψ ∈ A, ∃ k : ℝ, HasModularEnergy h.Δit ψ k ∧ k ≠ 0)
    (hcont : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ, Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir)))
    (hflat : ∀ h : ContratoH2 W R N, ∀ x ∈ rightWedge, screenBlock (solderMetric4 (h.E x)⁻¹) = -1)
    (c : ((Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) → ℝ) (hc0 : c 0 = 0) : ContratoImportH3 W R N T h2 where
  produce := fun h => adjusterPort h T G hG A hAu hAv hAt (hmc h) (hAn h) hcont (hflat h) c hc0
  same_horizon := fun h => rfl

/-! ## 4. o `geoFrame` PAGA a planura do fundo (logo a falha de 1. não vem do fundo) -/

open W5Final.Toy in
def geoInv (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![x 1 / (x 1 ^ 2 - x 0 ^ 2), -(x 0) / (x 1 ^ 2 - x 0 ^ 2), 0, 0;
     -(x 0) / (x 1 ^ 2 - x 0 ^ 2), x 1 / (x 1 ^ 2 - x 0 ^ 2), 0, 0;
     0, 0, 1, 0;
     0, 0, 0, 1]

open W5Final.Toy in
theorem geoFrame_inv {x : Fin 4 → ℝ} (hd : x 1 ^ 2 - x 0 ^ 2 ≠ 0) : (geoFrame x)⁻¹ = geoInv x := by
  apply Matrix.inv_eq_left_inv
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [geoInv, geoFrame, Matrix.mul_apply, Fin.sum_univ_four] <;> field_simp <;> ring

open W5Final.Toy in
/-- [DERIVED] (cálculo do cético 2, `geo_screen_sqrt`, na forma de bloco) a tela do `geoFrame` é −1₂ na cunha. -/
theorem geoFrame_screen_flat : ∀ x ∈ rightWedge, screenBlock (solderMetric4 (geoFrame x)⁻¹) = -1 := by
  intro x hx
  have hx' : |x 0| < x 1 := hx
  obtain ⟨h1, h2⟩ := abs_lt.mp hx'
  have hd : x 1 ^ 2 - x 0 ^ 2 ≠ 0 := by nlinarith
  rw [geoFrame_inv hd]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [screenBlock, solderMetric4, eta4, geoInv, Matrix.mul_apply, Fin.sum_univ_four,
      Matrix.diagonal_apply]

#print axioms genericImportPort
#print axioms geoFrame_inv
#print axioms geoFrame_screen_flat

end

end TGLExt.ContratoQGv31.ProbeAjustador
