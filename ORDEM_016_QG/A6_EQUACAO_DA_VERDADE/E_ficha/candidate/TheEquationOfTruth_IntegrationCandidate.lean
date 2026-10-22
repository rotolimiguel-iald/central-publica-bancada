import Mathlib
import TGLExt.TheNameIsTheInstrument
import TGLExt.NameIsTheContent
import TGL.FiniteThreeLocks
import TGLExt.TheContourOfTruth
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Normed.Operator.Mul
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import TGLExt.ContinuousModularZero
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Analysis.Normed.Algebra.MatrixExponential

/- Source body: B_fechamentos/TheEquationOfTruth_T20_v3.lean; imports relocated only. -/
/-
  TheEquationOfTruth.lean — pre-resolucao Lean da gerencia (23/09/2026), frente V3.
  [INPUT] a «equacao da verdade» colada pelo operador (texto do canal ChatGPT, [DECLARADO]).
  Este arquivo tipa, em kernel, as implicacoes MATEMATICAS do texto. Nao move gate nenhum.
  Homonimos: a anulacao da leitura (d/ds P(T_s x) = 0), o zero modular (K Ω = 0) e a anulacao
  do perfil (a'(0) = 0) sao TRES objetos distintos; nenhum lema aqui os identifica.
  O `Q H` (direcoes atenuadas) deste arquivo NAO e «o fundo» da TGL.
-/

open scoped InnerProductSpace Nat
open Filter Topology

namespace TGLExt.EquationOfTruth

/-! ## (1) O bit da verdade: V(b, b̂) = 1 − (b − b̂)² -/

/-- A valoracao da atribuicao binaria. -/
def truthValue (b bh : ℤ) : ℤ := 1 - (b - bh) ^ 2

theorem truthValue_table :
    truthValue 1 1 = 1 ∧ truthValue 0 0 = 1 ∧ truthValue 1 0 = 0 ∧ truthValue 0 1 = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num [truthValue]

theorem truthBit_eq_one_iff (b bh : ℤ) (hb : b = 0 ∨ b = 1) (hbh : bh = 0 ∨ bh = 1) :
    truthValue b bh = 1 ↔ b = bh := by
  rcases hb with rfl | rfl <;> rcases hbh with rfl | rfl <;> norm_num [truthValue]

theorem truthBit_eq_zero_iff (b bh : ℤ) (hb : b = 0 ∨ b = 1) (hbh : bh = 0 ∨ bh = 1) :
    truthValue b bh = 0 ↔ b ≠ bh := by
  rcases hb with rfl | rfl <;> rcases hbh with rfl | rfl <;> norm_num [truthValue]

/-- Nos bits, V so assume 0 ou 1 (e bivalente). -/
theorem truthBit_bivalent (b bh : ℤ) (hb : b = 0 ∨ b = 1) (hbh : bh = 0 ∨ bh = 1) :
    truthValue b bh = 0 ∨ truthValue b bh = 1 := by
  rcases hb with rfl | rfl <;> rcases hbh with rfl | rfl <;> norm_num [truthValue]

/-! ## (2) Os tres vinculos: ker (Σ D_j† D_j) = ⋂ ker D_j -/

section Penalty

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- A penalidade dos vinculos: H = Σ_j D_j† D_j. -/
noncomputable def penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) : E →L[𝕜] E :=
  ∑ j, ContinuousLinearMap.adjoint (D j) * D j

theorem re_inner_adjoint_mul_self (A : E →L[𝕜] E) (x : E) :
    RCLike.re ⟪x, (ContinuousLinearMap.adjoint A * A) x⟫_𝕜 = ‖A x‖ ^ 2 := by
  rw [ContinuousLinearMap.mul_apply, ContinuousLinearMap.adjoint_inner_right,
    inner_self_eq_norm_sq]

/-- A forma quadratica da penalidade e a soma dos quadrados dos defeitos. -/
theorem re_inner_penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) (x : E) :
    RCLike.re ⟪x, penalty D x⟫_𝕜 = ∑ j, ‖D j x‖ ^ 2 := by
  simp only [penalty, ContinuousLinearMap.sum_apply, inner_sum, map_sum]
  exact Finset.sum_congr rfl fun j _ => re_inner_adjoint_mul_self (D j) x

/-- A familia e a exclusao conjunta: ker H = ⋂_j ker D_j (uma violacao nao compensa outra). -/
theorem ker_penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) :
    (penalty D).ker = ⨅ j, (D j).ker := by
  ext x
  simp only [Submodule.mem_iInf, LinearMap.mem_ker]
  constructor
  · intro h j
    have h0 : ∑ j, ‖D j x‖ ^ 2 = 0 := by
      have h' : (penalty D) x = 0 := h
      rw [← re_inner_penalty, h', inner_zero_right, map_zero]
    have hj := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg ‖D j x‖)).1 h0 j
      (Finset.mem_univ _)
    exact norm_eq_zero.1 (pow_eq_zero_iff two_ne_zero |>.1 hj)
  · intro h
    simp [penalty, h]

/-- A forma com tres operadores, literal: ker (D₁†D₁ + D₂†D₂ + D₃†D₃) = ker D₁ ⊓ ker D₂ ⊓ ker D₃. -/
theorem ker_threeLocks (D₁ D₂ D₃ : E →L[𝕜] E) :
    (ContinuousLinearMap.adjoint D₁ * D₁ + ContinuousLinearMap.adjoint D₂ * D₂
        + ContinuousLinearMap.adjoint D₃ * D₃).ker
      = D₁.ker ⊓ D₂.ker ⊓ D₃.ker := by
  have h := ker_penalty (𝕜 := 𝕜) ![D₁, D₂, D₃]
  simp only [penalty, Fin.sum_univ_three, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons] at h
  rw [h]
  ext x
  simp only [Submodule.mem_iInf, Submodule.mem_inf, Fin.forall_fin_succ, IsEmpty.forall_iff,
    Matrix.cons_val_zero, Matrix.cons_val_succ, and_true, and_assoc]

/-- A penalidade e auto-adjunta. -/
theorem isSelfAdjoint_penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) :
    IsSelfAdjoint (penalty D) := by
  unfold penalty
  refine isSelfAdjoint_sum _ fun j _ => ?_
  rw [← ContinuousLinearMap.star_eq_adjoint]
  exact IsSelfAdjoint.star_mul_self (D j)

/-- A seletora apofatica A_C = −H e nao-positiva: Re⟪x, A_C x⟫ ≤ 0. -/
theorem selector_nonpos {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) (x : E) :
    RCLike.re ⟪x, (-penalty D) x⟫_𝕜 ≤ 0 := by
  rw [ContinuousLinearMap.neg_apply, inner_neg_right, map_neg, re_inner_penalty, neg_nonpos]
  exact Finset.sum_nonneg fun j _ => sq_nonneg _

end Penalty

/-! ## (3) P H = 0 e H P = 0 para P = projecao ortogonal sobre ker H, H auto-adjunto -/

section Projection

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

theorem H_mul_proj (H : E →L[𝕜] E) [H.ker.HasOrthogonalProjection] :
    H * H.ker.starProjection = 0 := by
  ext x
  rw [ContinuousLinearMap.mul_apply, ContinuousLinearMap.zero_apply]
  exact LinearMap.mem_ker.1 (H.ker.starProjection_apply_mem x)

theorem proj_mul_H (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    [H.ker.HasOrthogonalProjection] :
    H.ker.starProjection * H = 0 := by
  ext x
  rw [ContinuousLinearMap.mul_apply, ContinuousLinearMap.zero_apply,
    Submodule.starProjection_apply_eq_zero_iff, Submodule.mem_orthogonal]
  intro u hu
  have e : ⟪H u, x⟫_𝕜 = ⟪u, H x⟫_𝕜 := hH.isSymmetric u x
  have hu0 : H u = 0 := LinearMap.mem_ker.1 hu
  rw [← e, hu0, inner_zero_left]

end Projection

/-! ## (4) P · exp(−sH) = P e a conservacao da leitura I(T_s x) = I(x) -/

section Exponential

variable {𝔸 : Type*} [NormedRing 𝔸] [CompleteSpace 𝔸]

/-- Algebra pura: se P A = 0 entao P · exp A = P (pela serie). -/
theorem mul_exp_eq_of_mul_eq_zero (𝕂 : Type*) [RCLike 𝕂] [NormedAlgebra 𝕂 𝔸] (P A : 𝔸) (h : P * A = 0) :
    P * NormedSpace.exp A = P := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := 𝕂) A).mul_left P
  have h1 : HasSum (fun n : ℕ => P * ((n !⁻¹ : 𝕂) • A ^ n)) P := by
    have hf : (fun n : ℕ => P * ((n !⁻¹ : 𝕂) • A ^ n)) = fun n => if n = 0 then P else 0 := by
      funext n
      cases n with
      | zero => simp
      | succ n => simp [pow_succ', ← mul_assoc, h]
    rw [hf]
    exact hasSum_ite_eq 0 P
  exact hs.unique h1

/-- Simetrica: se A P = 0 entao exp A · P = P. -/
theorem exp_mul_eq_of_mul_eq_zero (𝕂 : Type*) [RCLike 𝕂] [NormedAlgebra 𝕂 𝔸] (P A : 𝔸) (h : A * P = 0) :
    NormedSpace.exp A * P = P := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := 𝕂) A).mul_right P
  have h1 : HasSum (fun n : ℕ => ((n !⁻¹ : 𝕂) • A ^ n) * P) P := by
    have hf : (fun n : ℕ => ((n !⁻¹ : 𝕂) • A ^ n) * P) = fun n => if n = 0 then P else 0 := by
      funext n
      cases n with
      | zero => simp
      | succ n => simp [pow_succ, mul_assoc, h]
    rw [hf]
    exact hasSum_ite_eq 0 P
  exact hs.unique h1

end Exponential

section Flow

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- O fluxo da seletora, com parametro em 𝕜: flow H u = exp(−u H). -/
noncomputable def flow (H : E →L[𝕜] E) (u : 𝕜) : E →L[𝕜] E := NormedSpace.exp ((-u) • H)

/-- O semigrupo real: T_s = exp(−s H), s ∈ ℝ lido em 𝕜. -/
noncomputable def T (H : E →L[𝕜] E) (s : ℝ) : E →L[𝕜] E := flow H (s : 𝕜)

variable (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) [H.ker.HasOrthogonalProjection]

/-- A leitura: I(x) = P x. -/
noncomputable abbrev reading : E →L[𝕜] E := H.ker.starProjection

include hH in
theorem proj_mul_flow (u : 𝕜) : reading H * flow H u = reading H := by
  refine mul_exp_eq_of_mul_eq_zero 𝕜 _ _ ?_
  rw [mul_smul_comm, proj_mul_H H hH, smul_zero]

theorem flow_mul_proj (u : 𝕜) : flow H u * reading H = reading H := by
  refine exp_mul_eq_of_mul_eq_zero 𝕜 _ _ ?_
  rw [smul_mul_assoc, H_mul_proj H, smul_zero]

include hH in
/-- P T_s = P. -/
theorem proj_mul_T (s : ℝ) : reading H * T H s = reading H := proj_mul_flow H hH _

include hH in
/-- A conservacao da leitura: I(T_s x) = I(x). -/
theorem reading_T (s : ℝ) (x : E) : reading H (T H s x) = reading H x := by
  rw [← ContinuousLinearMap.mul_apply, proj_mul_T H hH]

/-- O setor da familia fica parado: z ∈ F ⟹ T_s z = z. -/
theorem T_fix_of_mem_ker (s : ℝ) {z : E} (hz : z ∈ H.ker) : T H s z = z := by
  have hPz : reading H z = z := Submodule.starProjection_eq_self_iff.2 hz
  have := congrArg (fun A : E →L[𝕜] E => A z) (flow_mul_proj H (s : 𝕜))
  simp only [ContinuousLinearMap.mul_apply, hPz] at this
  exact this

/-- A decomposicao T_s x = P x + T_s (x − P x): a componente da familia permanece. -/
theorem T_decomp (s : ℝ) (x : E) :
    T H s x = reading H x + T H s (x - reading H x) := by
  have hP : T H s (reading H x) = reading H x :=
    T_fix_of_mem_ker H s (H.ker.starProjection_apply_mem x)
  rw [map_sub, hP, add_sub_cancel]

end Flow

/-! ## (4b) O veredito: V_x(T_s x) = 1, e a ponte com `NameInstrument.Verifies` (v336) -/

section Verdict

open Classical in
/-- V_r(y) = 1 se I(y) = I(r), 0 caso contrario (o criterio da secao 1 do texto). -/
noncomputable def verdict {X Y : Type*} (I : X → Y) (r y : X) : ℤ := if I y = I r then 1 else 0

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- V_x(T_s x) = 1: a transformacao efetiva e verificada pela leitura da familia. -/
theorem verdict_T (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) [H.ker.HasOrthogonalProjection]
    (s : ℝ) (x : E) : verdict (fun y => reading H y) x (T H s x) = 1 := by
  simp [verdict, reading_T H hH s x]

/-- O veredito binario e o bit da verdade: verdict ∈ {0,1} e vale 1 sse as leituras coincidem. -/
theorem verdict_eq_one_iff {X Y : Type*} (I : X → Y) (r y : X) :
    verdict I r y = 1 ↔ I y = I r := by
  unfold verdict; split_ifs with h <;> simp [h]

end Verdict

section NameBridge

variable {𝕜 : Type*} {E : Type} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- Ponte com a folha v336 da arvore (`TGLExt.NameInstrument.Verifies`, read (f x) = read x):
    a leitura P e um Nome que VERIFICA cada T_s, e (pela folha) toda iterada de T_s. -/
theorem name_verifies_T (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) [H.ker.HasOrthogonalProjection]
    (s : ℝ) :
    (⟨fun x => reading H x⟩ : TGLExt.NameInstrument E E).Verifies (fun x => T H s x) :=
  fun x => reading_T H hH s x

theorem name_verifies_T_iterate (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    [H.ker.HasOrthogonalProjection] (s : ℝ) (n : ℕ) :
    (⟨fun x => reading H x⟩ : TGLExt.NameInstrument E E).Verifies ((fun x => T H s x)^[n]) :=
  TGLExt.name_verifies_iterate _ (name_verifies_T H hH s) n

end NameBridge

/-! ## (5) Memoria estavel: Im P = Fix P, P^n = P, Px = Py ↔ x − y ∈ ker P -/

section Idempotent

variable {R M : Type*} [Semiring R] [AddCommGroup M] [Module R M]

theorem mem_range_iff_fixed (P : M →ₗ[R] M) (hP : IsIdempotentElem P) (z : M) :
    z ∈ LinearMap.range P ↔ P z = z := by
  constructor
  · rintro ⟨x, rfl⟩
    rw [← Module.End.mul_apply, hP.eq]
  · intro h
    exact ⟨z, h⟩

theorem pow_eq_self (P : M →ₗ[R] M) (hP : IsIdempotentElem P) {n : ℕ} (hn : n ≠ 0) :
    P ^ n = P := hP.pow_eq hn

theorem apply_eq_apply_iff (P : M →ₗ[R] M) (x y : M) :
    P x = P y ↔ x - y ∈ LinearMap.ker P := by
  rw [LinearMap.mem_ker, map_sub, sub_eq_zero]

/-- Instanciado na leitura: Im P = Fix P para a projecao ortogonal. -/
theorem starProjection_range_iff_fixed {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
    [InnerProductSpace 𝕜 E] (K : Submodule 𝕜 E) [K.HasOrthogonalProjection] (z : E) :
    z ∈ LinearMap.range (K.starProjection : E →ₗ[𝕜] E) ↔ K.starProjection z = z :=
  by
  have hid : IsIdempotentElem (K.starProjection : E →ₗ[𝕜] E) := by
    show (K.starProjection : E →ₗ[𝕜] E) * (K.starProjection : E →ₗ[𝕜] E) = K.starProjection
    ext x
    exact congrArg (fun A : E →L[𝕜] E => A x) K.isIdempotentElem_starProjection
  exact mem_range_iff_fixed _ hid z

end Idempotent

/-! ## (6) A reciproca: leitura continua conservada ⟺ l = l ∘ P (com o limite NOMEADO) -/

section Converse

/-- Hipotese NOMEADA: o semigrupo converge (ponto a ponto) para a projecao da familia. -/
def FlowTendsToFamily {X : Type*} [TopologicalSpace X] (Tf : ℝ → X → X) (P : X → X) : Prop :=
  ∀ x, Tendsto (fun s => Tf s x) atTop (𝓝 (P x))

/-- Abstrata: com P ∘ T_s = P (s ≥ 0) e o limite nomeado, uma leitura continua e conservada
    ao longo do semigrupo sse fatora pela familia: l = l ∘ P. -/
theorem conserved_iff_factors {X Y : Type*} [TopologicalSpace X] [TopologicalSpace Y]
    [T2Space Y] (Tf : ℝ → X → X) (P : X → X) (hPT : ∀ s, 0 ≤ s → ∀ x, P (Tf s x) = P x)
    (hlim : FlowTendsToFamily Tf P) (l : X → Y) (hl : Continuous l) :
    (∀ s, 0 ≤ s → ∀ x, l (Tf s x) = l x) ↔ ∀ x, l x = l (P x) := by
  constructor
  · intro hc x
    have h1 : Tendsto (fun s => l (Tf s x)) atTop (𝓝 (l (P x))) :=
      (hl.tendsto _).comp (hlim x)
    have h2 : Tendsto (fun s => l (Tf s x)) atTop (𝓝 (l x)) := by
      refine tendsto_const_nhds.congr' ?_
      filter_upwards [eventually_ge_atTop (0 : ℝ)] with s hs
      exact (hc s hs x).symm
    exact tendsto_nhds_unique h2 h1
  · intro hf s hs x
    rw [hf (Tf s x), hPT s hs x, ← hf x]

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- Instanciada no semigrupo da seletora. -/
theorem conserved_iff_factors_T (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    [H.ker.HasOrthogonalProjection]
    (hlim : FlowTendsToFamily (fun s x => T H s x) (fun x => reading H x))
    {Y : Type*} [TopologicalSpace Y] [T2Space Y] (l : E → Y) (hl : Continuous l) :
    (∀ s, 0 ≤ s → ∀ x, l (T H s x) = l x) ↔ ∀ x, l x = l (reading H x) :=
  conserved_iff_factors (fun s x => T H s x) (fun x => reading H x)
    (fun s _ x => reading_T H hH s x) hlim l hl

end Converse

/-! ## (7) A derivada da leitura se anula; a da dinamica, nao necessariamente -/

section Derivative

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]
variable (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) [H.ker.HasOrthogonalProjection]

include hH in
/-- d/du P(flow u x) = 0 (parametro em 𝕜; para 𝕜 = ℝ e literalmente d/ds). -/
theorem hasDerivAt_reading_flow (x : E) (u : 𝕜) :
    HasDerivAt (fun v : 𝕜 => reading H (flow H v x)) 0 u := by
  have : (fun v : 𝕜 => reading H (flow H v x)) = fun _ => reading H x := by
    funext v
    rw [← ContinuousLinearMap.mul_apply, proj_mul_flow H hH]
  rw [this]
  exact hasDerivAt_const _ _

include hH in
/-- A forma literal em s ∈ ℝ: d/ds P(T_s x) = 0 (qualquer estrutura real em E serve: a funcao
    e constante por `reading_T`). -/
theorem hasDerivAt_reading_T [NormedSpace ℝ E] (x : E) (s : ℝ) :
    HasDerivAt (fun r : ℝ => reading H (T H r x)) 0 s := by
  have : (fun r : ℝ => reading H (T H r x)) = fun _ => reading H x :=
    funext fun r => reading_T H hH r x
  rw [this]
  exact hasDerivAt_const _ _

/-- A dinamica inteira: d/du flow u = (−H) · flow u. -/
theorem hasDerivAt_flow (u : 𝕜) :
    HasDerivAt (fun v : 𝕜 => flow H v) ((-H) * flow H u) u := by
  have h := hasDerivAt_exp_smul_const' (𝕂 := 𝕜) (-H) u
  have e : ∀ v : 𝕜, (-v) • H = v • (-H) := fun v => by rw [neg_smul, smul_neg]
  simp only [flow, e]
  exact h

/-- Aplicada a x: d/du flow u x = −H (flow u x). -/
theorem hasDerivAt_flow_apply (x : E) (u : 𝕜) :
    HasDerivAt (fun v : 𝕜 => flow H v x) (-(H (flow H u x))) u := by
  have h := (hasDerivAt_flow H u).clm_apply (hasDerivAt_const u x)
  simpa using h

/-- Dinamica nao nula: fora da familia, a derivada em u = 0 e −H x ≠ 0,
    enquanto a derivada da leitura e 0. -/
theorem flow_derivative_ne_zero_at_zero (x : E) (hx : x ∉ H.ker) :
    HasDerivAt (fun v : 𝕜 => flow H v x) (-(H x)) 0 ∧ -(H x) ≠ 0 := by
  refine ⟨?_, ?_⟩
  · have h := hasDerivAt_flow_apply H x 0
    simpa [flow, NormedSpace.exp_zero] using h
  · intro h0
    exact hx (LinearMap.mem_ker.2 (neg_eq_zero.1 h0))

end Derivative

/-! ## (8) O limite espectral em dimensao finita: exp(−sH) x → P x (s → ∞)
  Descarrega a hipotese nomeada `FlowTendsToFamily` quando E e de dimensao finita e H ≥ 0. -/

section Limit

/- `[CompleteSpace E]` e redundante sob `[FiniteDimensional 𝕜 E]` (`FiniteDimensional.complete`);
   fica explicito so para as instancias. -/
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [FiniteDimensional 𝕜 E] [CompleteSpace E]

/-- exp age num autovetor como a exponencial escalar do autovalor. -/
theorem exp_apply_of_eigen (A : E →L[𝕜] E) (μ : 𝕜) (v : E) (hv : A v = μ • v) :
    NormedSpace.exp A v = NormedSpace.exp μ • v := by
  have hpow : ∀ n : ℕ, (A ^ n) v = μ ^ n • v := by
    intro n
    induction n with
    | zero => simp
    | succ n ih =>
      rw [pow_succ', ContinuousLinearMap.mul_apply, ih, map_smul, hv, smul_smul, ← pow_succ]
  have h1 := (NormedSpace.exp_series_hasSum_exp' (𝕂 := 𝕜) A).mapL
    (ContinuousLinearMap.apply 𝕜 E v)
  have h2 := (NormedSpace.exp_series_hasSum_exp' (𝕂 := 𝕜) μ).smul_const v
  refine h1.unique ?_
  convert h2 using 1
  funext n
  simp [hpow, smul_smul]

/-- No autovetor de autovalor real ev: T_s v = e^{−s·ev} v. -/
theorem T_apply_eigen (H : E →L[𝕜] E) (ev : ℝ) (v : E) (hv : H v = (ev : 𝕜) • v) (s : ℝ) :
    T H s v = ((Real.exp (-(s * ev)) : ℝ) : 𝕜) • v := by
  have hA : ((-(s : 𝕜)) • H) v = ((-(s : 𝕜)) * (ev : 𝕜)) • v := by
    rw [ContinuousLinearMap.smul_apply, hv, smul_smul]
  rw [T, flow, exp_apply_of_eigen _ _ _ hA]
  congr 1
  have e1 : (-(s : 𝕜)) * (ev : 𝕜) = algebraMap ℝ 𝕜 (-(s * ev)) := by
    rw [RCLike.algebraMap_eq_ofReal]; push_cast; ring
  rw [e1, ← NormedSpace.algebraMap_exp_comm, RCLike.algebraMap_eq_ofReal, Real.exp_eq_exp_ℝ]

/-- ★ O limite espectral: para H auto-adjunto com forma nao-negativa, em dimensao finita,
    T_s x → P x quando s → ∞ (os modos zero ficam; os demais decaem como e^{−s·ev}). -/
theorem flowTendsToFamily_of_finiteDimensional (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x, H x⟫_𝕜) :
    FlowTendsToFamily (fun s x => T H s x) (fun x => reading H x) := by
  intro x
  have hsym : (H : E →ₗ[𝕜] E).IsSymmetric := hH.isSymmetric
  have hn : Module.finrank 𝕜 E = Module.finrank 𝕜 E := rfl
  set b := hsym.eigenvectorBasis hn with hb
  have hi : ∀ i, Tendsto (fun s => T H s (b i)) atTop (𝓝 (reading H (b i))) := by
    intro i
    set ev := hsym.eigenvalues hn i with hev
    have hv : H (b i) = (ev : 𝕜) • b i := hsym.apply_eigenvectorBasis hn i
    by_cases h0 : ev = 0
    · have hk : b i ∈ H.ker := by
        rw [LinearMap.mem_ker]
        have : H (b i) = 0 := by rw [hv, h0]; simp
        exact this
      have hP : reading H (b i) = b i := Submodule.starProjection_eq_self_iff.2 hk
      rw [hP]
      have hc : (fun s => T H s (b i)) = fun _ => b i := funext fun s => T_fix_of_mem_ker H s hk
      rw [hc]
      exact tendsto_const_nhds
    · have hpos_i : 0 < ev := by
        have h1 := hpos (b i)
        rw [hv, inner_smul_right, RCLike.re_ofReal_mul, inner_self_eq_norm_sq,
          b.orthonormal.1 i] at h1
        norm_num at h1
        exact lt_of_le_of_ne h1 (Ne.symm h0)
      have hP : reading H (b i) = 0 := by
        have h2 : reading H (H (b i)) = 0 := by
          have := congrArg (fun A : E →L[𝕜] E => A (b i)) (proj_mul_H H hH)
          simpa using this
        rw [hv, map_smul] at h2
        exact (smul_eq_zero.1 h2).resolve_left (by exact_mod_cast h0)
      rw [hP]
      have hc : (fun s => T H s (b i)) = fun s => ((Real.exp (-(s * ev)) : ℝ) : 𝕜) • b i :=
        funext fun s => T_apply_eigen H ev (b i) hv s
      rw [hc]
      have hexp : Tendsto (fun s : ℝ => Real.exp (-(s * ev))) atTop (𝓝 0) :=
        Real.tendsto_exp_neg_atTop_nhds_zero.comp (tendsto_id.atTop_mul_const hpos_i)
      have h3 := (((RCLike.continuous_ofReal (K := 𝕜)).tendsto 0).comp hexp).smul_const (b i)
      simpa using h3
  have hT : ∀ s, T H s x = ∑ i, b.repr x i • T H s (b i) := by
    intro s
    conv_lhs => rw [← b.sum_repr x]
    simp [map_sum, map_smul]
  have hPx : reading H x = ∑ i, b.repr x i • reading H (b i) := by
    conv_lhs => rw [← b.sum_repr x]
    simp [map_sum, map_smul]
  have hfun : (fun s => T H s x) = fun s => ∑ i, b.repr x i • T H s (b i) := funext hT
  show Tendsto (fun s => T H s x) atTop (𝓝 (reading H x))
  rw [hfun, hPx]
  exact tendsto_finsetSum _ fun i _ => (hi i).const_smul _

/-- ★ A reciproca INCONDICIONAL em dimensao finita, para a penalidade dos vinculos:
    uma leitura continua e conservada ao longo de T_s = exp(−s H_3L) sse l = l ∘ P. -/
theorem conserved_iff_factors_penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E)
    {Y : Type*} [TopologicalSpace Y] [T2Space Y] (l : E → Y) (hl : Continuous l) :
    (∀ s, 0 ≤ s → ∀ x, l (T (penalty D) s x) = l x) ↔
      ∀ x, l x = l (reading (penalty D) x) := by
  refine conserved_iff_factors_T (penalty D) (isSelfAdjoint_penalty D)
    (flowTendsToFamily_of_finiteDimensional (penalty D) (isSelfAdjoint_penalty D) ?_) l hl
  intro x
  rw [re_inner_penalty]
  exact Finset.sum_nonneg fun j _ => sq_nonneg _

end Limit

/-! ## (9) O perfil hiperbolico a = sech(χ/2), q = tanh(χ/2)
  HOMONIMO: esta anulacao a'(0) = 0 e do perfil em χ; NAO e o zero modular K Ω = 0,
  nem a anulacao da leitura em (7). Nenhum lema aqui os liga. -/

section Profile

open Real

noncomputable def profA (χ : ℝ) : ℝ := (cosh (χ / 2))⁻¹
noncomputable def profQ (χ : ℝ) : ℝ := tanh (χ / 2)

theorem hasDerivAt_profA (χ : ℝ) :
    HasDerivAt profA (-(1 / 2) * profA χ * profQ χ) χ := by
  have hc : HasDerivAt (fun y => cosh (y / 2)) (sinh (χ / 2) * (1 / 2)) χ :=
    ((hasDerivAt_id' χ).div_const 2).cosh
  have hne : cosh (χ / 2) ≠ 0 := (cosh_pos _).ne'
  have h : HasDerivAt (fun y => (cosh (y / 2))⁻¹) (-(sinh (χ / 2) * (1 / 2)) / cosh (χ / 2) ^ 2) χ :=
    hc.inv hne
  have e : -(1 / 2) * profA χ * profQ χ = -(sinh (χ / 2) * (1 / 2)) / cosh (χ / 2) ^ 2 := by
    simp only [profA, profQ, tanh_eq_sinh_div_cosh]
    field_simp
  rw [e]
  exact h

theorem hasDerivAt_profQ (χ : ℝ) :
    HasDerivAt profQ ((1 / 2) * profA χ ^ 2) χ := by
  have hc : HasDerivAt (fun y => cosh (y / 2)) (sinh (χ / 2) * (1 / 2)) χ :=
    ((hasDerivAt_id' χ).div_const 2).cosh
  have hs : HasDerivAt (fun y => sinh (y / 2)) (cosh (χ / 2) * (1 / 2)) χ :=
    ((hasDerivAt_id' χ).div_const 2).sinh
  have hne : cosh (χ / 2) ≠ 0 := (cosh_pos _).ne'
  have h := hs.div hc hne
  have hfun : profQ = fun y => sinh (y / 2) / cosh (y / 2) := by
    funext y
    simp only [profQ, tanh_eq_sinh_div_cosh]
  have key : cosh (χ / 2) * (1 / 2) * cosh (χ / 2) - sinh (χ / 2) * (sinh (χ / 2) * (1 / 2))
      = 1 / 2 := by
    linear_combination (1 / 2 : ℝ) * cosh_sq_sub_sinh_sq (χ / 2)
  have e : (1 / 2) * profA χ ^ 2 = (cosh (χ / 2) * (1 / 2) * cosh (χ / 2)
      - sinh (χ / 2) * (sinh (χ / 2) * (1 / 2))) / cosh (χ / 2) ^ 2 := by
    rw [key]
    simp only [profA]
    field_simp
  rw [hfun, e]
  exact h

theorem profA_zero : profA 0 = 1 := by simp [profA]
theorem profQ_zero : profQ 0 = 0 := by simp [profQ]

/-- a'(0) = 0. -/
theorem profA_deriv_zero : deriv profA 0 = 0 := by
  rw [(hasDerivAt_profA 0).deriv, profQ_zero, mul_zero]

/-- q'(0) = 1/2. -/
theorem profQ_deriv_zero : deriv profQ 0 = 1 / 2 := by
  rw [(hasDerivAt_profQ 0).deriv, profA_zero]; norm_num

/-- a''(0) = −1/4. -/
theorem profA_second_deriv_zero : deriv (deriv profA) 0 = -(1 / 4) := by
  have hd : deriv profA = fun χ => -(1 / 2) * profA χ * profQ χ := by
    funext χ; exact (hasDerivAt_profA χ).deriv
  rw [hd]
  have h := (((hasDerivAt_profA 0).const_mul (-(1 / 2) : ℝ)).mul (hasDerivAt_profQ 0))
  have h' : HasDerivAt (fun χ => -(1 / 2) * profA χ * profQ χ)
      (-(1 / 2) * (-(1 / 2) * profA 0 * profQ 0) * profQ 0
        + -(1 / 2) * profA 0 * (1 / 2 * profA 0 ^ 2)) 0 := h
  rw [h'.deriv, profA_zero, profQ_zero]
  norm_num

end Profile

end TGLExt.EquationOfTruth

-- Auditoria de axiomas
#print axioms TGLExt.EquationOfTruth.truthValue_table
#print axioms TGLExt.EquationOfTruth.truthBit_eq_one_iff
#print axioms TGLExt.EquationOfTruth.truthBit_eq_zero_iff
#print axioms TGLExt.EquationOfTruth.truthBit_bivalent
#print axioms TGLExt.EquationOfTruth.re_inner_penalty
#print axioms TGLExt.EquationOfTruth.ker_penalty
#print axioms TGLExt.EquationOfTruth.ker_threeLocks
#print axioms TGLExt.EquationOfTruth.isSelfAdjoint_penalty
#print axioms TGLExt.EquationOfTruth.selector_nonpos
#print axioms TGLExt.EquationOfTruth.H_mul_proj
#print axioms TGLExt.EquationOfTruth.proj_mul_H
#print axioms TGLExt.EquationOfTruth.mul_exp_eq_of_mul_eq_zero
#print axioms TGLExt.EquationOfTruth.exp_mul_eq_of_mul_eq_zero
#print axioms TGLExt.EquationOfTruth.proj_mul_flow
#print axioms TGLExt.EquationOfTruth.proj_mul_T
#print axioms TGLExt.EquationOfTruth.reading_T
#print axioms TGLExt.EquationOfTruth.T_fix_of_mem_ker
#print axioms TGLExt.EquationOfTruth.T_decomp
#print axioms TGLExt.EquationOfTruth.verdict_T
#print axioms TGLExt.EquationOfTruth.verdict_eq_one_iff
#print axioms TGLExt.EquationOfTruth.name_verifies_T
#print axioms TGLExt.EquationOfTruth.name_verifies_T_iterate
#print axioms TGLExt.EquationOfTruth.mem_range_iff_fixed
#print axioms TGLExt.EquationOfTruth.pow_eq_self
#print axioms TGLExt.EquationOfTruth.apply_eq_apply_iff
#print axioms TGLExt.EquationOfTruth.starProjection_range_iff_fixed
#print axioms TGLExt.EquationOfTruth.conserved_iff_factors
#print axioms TGLExt.EquationOfTruth.conserved_iff_factors_T
#print axioms TGLExt.EquationOfTruth.hasDerivAt_reading_flow
#print axioms TGLExt.EquationOfTruth.hasDerivAt_reading_T
#print axioms TGLExt.EquationOfTruth.hasDerivAt_flow
#print axioms TGLExt.EquationOfTruth.hasDerivAt_flow_apply
#print axioms TGLExt.EquationOfTruth.flow_derivative_ne_zero_at_zero
#print axioms TGLExt.EquationOfTruth.exp_apply_of_eigen
#print axioms TGLExt.EquationOfTruth.T_apply_eigen
#print axioms TGLExt.EquationOfTruth.flowTendsToFamily_of_finiteDimensional
#print axioms TGLExt.EquationOfTruth.conserved_iff_factors_penalty
#print axioms TGLExt.EquationOfTruth.hasDerivAt_profA
#print axioms TGLExt.EquationOfTruth.hasDerivAt_profQ
#print axioms TGLExt.EquationOfTruth.profA_deriv_zero
#print axioms TGLExt.EquationOfTruth.profQ_deriv_zero
#print axioms TGLExt.EquationOfTruth.profA_second_deriv_zero
#print axioms TGLExt.EquationOfTruth.re_inner_adjoint_mul_self
#print axioms TGLExt.EquationOfTruth.flow_mul_proj
#print axioms TGLExt.EquationOfTruth.profA_zero
#print axioms TGLExt.EquationOfTruth.profQ_zero

namespace TGLExt.EquationOfTruth
section EarlyClosures
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
  [InnerProductSpace 𝕜 E] [CompleteSpace E]

theorem reading_zero_of_kernel_bot (H : E →L[𝕜] E)
    [H.ker.HasOrthogonalProjection] (hk : H.ker = ⊥) : reading H = 0 := by
  unfold reading
  simp [hk]

theorem verdict_one_of_kernel_bot (H : E →L[𝕜] E)
    [H.ker.HasOrthogonalProjection] (hk : H.ker = ⊥) (x y : E) :
    verdict (reading H) x y = 1 := by
  simp [verdict, reading_zero_of_kernel_bot H hk]

theorem operator_zero_of_kernel_top (H : E →L[𝕜] E)
    (hk : H.ker = ⊤) : H = 0 := by
  ext x
  have hx : x ∈ H.ker := by rw [hk]; trivial
  exact LinearMap.mem_ker.mp hx

theorem flow_identity_of_kernel_top (H : E →L[𝕜] E)
    (hk : H.ker = ⊤) (s : ℝ) : T H s = 1 := by
  rw [operator_zero_of_kernel_top H hk]
  simp [T, flow]

variable [FiniteDimensional 𝕜 E]

theorem conserved_iff_factors_of_nonneg (H : E →L[𝕜] E)
    (hH : IsSelfAdjoint H) (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜)
    {Y : Type*} [TopologicalSpace Y] [T2Space Y] (l : E → Y) (hl : Continuous l) :
    (∀ s, 0 ≤ s → ∀ x, l (T H s x) = l x) ↔ ∀ x, l x = l (reading H x) :=
  conserved_iff_factors_T H hH (flowTendsToFamily_of_finiteDimensional H hH hpos) l hl

theorem distinguishing_reading_iff (H : E →L[𝕜] E)
    (hH : IsSelfAdjoint H) (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜)
    {Y : Type*} [TopologicalSpace Y] [T2Space Y] (l : E → Y) (hl : Continuous l)
    (hc : ∀ s, 0 ≤ s → ∀ x, l (T H s x) = l x)
    (hinj : Set.InjOn l (H.ker : Set E)) (x y : E) :
    l x = l y ↔ reading H x = reading H y := by
  have hf := (conserved_iff_factors_of_nonneg H hH hpos l hl).mp hc
  rw [hf x, hf y]
  exact ⟨fun h => hinj (H.ker.starProjection_apply_mem x)
    (H.ker.starProjection_apply_mem y) h, congrArg l⟩

/-- Equality of binary comparisons, not equality of numerical distances. -/
theorem distinguishing_verdict_eq (H : E →L[𝕜] E)
    (hH : IsSelfAdjoint H) (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜)
    {Y : Type*} [TopologicalSpace Y] [T2Space Y] (l : E → Y) (hl : Continuous l)
    (hc : ∀ s, 0 ≤ s → ∀ x, l (T H s x) = l x)
    (hinj : Set.InjOn l (H.ker : Set E)) (x y : E) :
    verdict l x y = verdict (reading H) x y := by
  unfold verdict
  rw [distinguishing_reading_iff H hH hpos l hl hc hinj y x]
end EarlyClosures
end TGLExt.EquationOfTruth

#print axioms TGLExt.EquationOfTruth.reading_zero_of_kernel_bot
#print axioms TGLExt.EquationOfTruth.verdict_one_of_kernel_bot
#print axioms TGLExt.EquationOfTruth.operator_zero_of_kernel_top
#print axioms TGLExt.EquationOfTruth.flow_identity_of_kernel_top
#print axioms TGLExt.EquationOfTruth.conserved_iff_factors_of_nonneg
#print axioms TGLExt.EquationOfTruth.distinguishing_reading_iff
#print axioms TGLExt.EquationOfTruth.distinguishing_verdict_eq

namespace TGLExt.EquationOfTruth
section SingleTime
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
  [InnerProductSpace 𝕜 E] [CompleteSpace E]

theorem T_add (H : E →L[𝕜] E) (s t : ℝ) : T H (s+t) = T H s * T H t := by
  unfold T flow
  have he : (-((s+t : ℝ) : 𝕜)) • H = (-(s : 𝕜)) • H + (-(t : 𝕜)) • H := by
    push_cast
    rw [neg_add, add_smul]
  rw [he]
  refine NormedSpace.exp_add_of_commute_of_mem_ball (𝕂 := 𝕜) ?_ ?_ ?_
  · unfold Commute SemiconjBy
    simp only [smul_mul_assoc, mul_smul_comm, smul_smul]
    congr 1
    ring
  · rw [NormedSpace.expSeries_radius_eq_top]
    exact edist_lt_top _ _
  · rw [NormedSpace.expSeries_radius_eq_top]
    exact edist_lt_top _ _

theorem iterate_T_eq_nat_time (H : E →L[𝕜] E) (s : ℝ) (n : ℕ) (x : E) :
    (fun y => T H s y)^[n] x = T H ((n : ℝ)*s) x := by
  induction n with
  | zero => simp [T,flow]
  | succ n ih =>
    rw [Function.iterate_succ_apply', ih]
    have ht : ((n+1 : ℕ) : ℝ)*s = s+(n : ℝ)*s := by push_cast; ring
    rw [ht,T_add]
    rfl

theorem single_time_conserved_iff_factors [FiniteDimensional 𝕜 E]
    (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜)
    (s0 : ℝ) (hs0 : 0 < s0)
    {Y : Type*} [TopologicalSpace Y] [T2Space Y] (l : E → Y) (hl : Continuous l) :
    (∀ x, l (T H s0 x) = l x) ↔ ∀ x, l x = l (reading H x) := by
  constructor
  · intro hc x
    have hi : ∀ n : ℕ, ∀ y : E, l ((fun z => T H s0 z)^[n] y) = l y := by
      intro n y
      induction n with
      | zero => rfl
      | succ n ih => rw [Function.iterate_succ_apply',hc,ih]
    have hn : Tendsto (fun n : ℕ => (n : ℝ)*s0) atTop atTop :=
      tendsto_natCast_atTop_atTop.atTop_mul_const hs0
    have hlim : Tendsto (fun n : ℕ => l (T H ((n : ℝ)*s0) x))
        atTop (𝓝 (l (reading H x))) :=
      (hl.tendsto _).comp ((flowTendsToFamily_of_finiteDimensional H hH hpos x).comp hn)
    have hconst : Tendsto (fun n : ℕ => l (T H ((n : ℝ)*s0) x)) atTop (𝓝 (l x)) := by
      apply tendsto_const_nhds.congr'
      exact Filter.Eventually.of_forall fun n => by
        change l x = l (T H ((n : ℝ)*s0) x)
        rw [← iterate_T_eq_nat_time]
        exact (hi n x).symm
    exact tendsto_nhds_unique hconst hlim
  · intro hf x
    rw [hf (T H s0 x), reading_T H hH, ← hf x]

theorem sampling_zero_conserves_every_reader (H : E →L[𝕜] E)
    {Y : Type*} (l : E → Y) (x : E) : l (T H 0 x) = l x := by
  simp [T,flow]
end SingleTime
end TGLExt.EquationOfTruth

#print axioms TGLExt.EquationOfTruth.T_add
#print axioms TGLExt.EquationOfTruth.iterate_T_eq_nat_time
#print axioms TGLExt.EquationOfTruth.single_time_conserved_iff_factors
#print axioms TGLExt.EquationOfTruth.sampling_zero_conserves_every_reader

/- Source body: B_fechamentos/InscriptionBridge.lean; imports relocated only. -/

set_option autoImplicit false
open scoped InnerProductSpace
open Filter Topology
noncomputable section
namespace TGLExt.EquationOfTruth
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
  [InnerProductSpace 𝕜 E] [CompleteSpace E]

/-- INPUT/ONTO compatibility: content is x; the selected form is equality of readings.
The v368 nome is content, not the v336 NameInstrument.read. -/
def inscriptionForm (H : E →L[𝕜] E) [H.ker.HasOrthogonalProjection]
    (r x : E) : Prop := reading H x = reading H r

theorem flow_preserves_inscription_form (H : E →L[𝕜] E)
    [H.ker.HasOrthogonalProjection] (hH : IsSelfAdjoint H) (r : E) (s : ℝ) :
    ∀ x, inscriptionForm H r x → inscriptionForm H r (T H s x) := by
  intro x hx
  exact (reading_T H hH s x).trans hx

def transportedInscription (H : E →L[𝕜] E) [H.ker.HasOrthogonalProjection]
    (hH : IsSelfAdjoint H) (r : E) (s : ℝ) :
    NameIsTheContent.Inscricao E (inscriptionForm H r) :=
  NameIsTheContent.travessia (T H s) (flow_preserves_inscription_form H hH r s) ⟨r,rfl⟩

theorem inscription_form_survives (H : E →L[𝕜] E)
    [H.ker.HasOrthogonalProjection] (hH : IsSelfAdjoint H) (r : E) (s : ℝ) :
    NameIsTheContent.identidade E (inscriptionForm H r)
      (transportedInscription H hH r s).conteudo :=
  NameIsTheContent.the_form_survives_the_crossing (T H s)
    (flow_preserves_inscription_form H hH r s) ⟨r,rfl⟩

theorem transported_name_eq_flow (H : E →L[𝕜] E)
    [H.ker.HasOrthogonalProjection] (hH : IsSelfAdjoint H) (r : E) (s : ℝ) :
    NameIsTheContent.nome (transportedInscription H hH r s) = T H s r := rfl

theorem positive_time_changes_nonfixed_content [FiniteDimensional 𝕜 E]
    (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜) (r : E) (hr : r ∉ H.ker) :
    ∃ s : ℝ, 0 < s ∧ T H s r ≠ r := by
  classical
  by_contra hn
  push_neg at hn
  have hc : Tendsto (fun s : ℝ => T H s r) atTop (𝓝 r) := by
    apply tendsto_const_nhds.congr'
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with s hs
    exact (hn s hs).symm
  have he : reading H r = r :=
    tendsto_nhds_unique (flowTendsToFamily_of_finiteDimensional H hH hpos r) hc
  exact hr (Submodule.starProjection_eq_self_iff.mp he)

theorem same_form_changed_name [FiniteDimensional 𝕜 E]
    (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜) (r : E) (hr : r ∉ H.ker) :
    ∃ s : ℝ, 0 < s ∧
      inscriptionForm H r (transportedInscription H hH r s).conteudo ∧
      NameIsTheContent.nome (transportedInscription H hH r s) ≠ r := by
  obtain ⟨s,hs,hchange⟩ := positive_time_changes_nonfixed_content H hH hpos r hr
  exact ⟨s,hs,inscription_form_survives H hH r s,hchange⟩

#print axioms flow_preserves_inscription_form
#print axioms transportedInscription
#print axioms inscription_form_survives
#print axioms transported_name_eq_flow
#print axioms positive_time_changes_nonfixed_content
#print axioms same_form_changed_name
end TGLExt.EquationOfTruth

/- Source body: B_fechamentos/PenaltyThreeLocksBridge_v2.lean; imports relocated only. -/
set_option autoImplicit false
noncomputable section
namespace TGLExt.EquationOfTruth
variable {n : ℕ}
variable (Dc Db Dz : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n))

/-- Exact equality of operators; no claim about floating-point runtime operands. -/
theorem penalty_eq_kernel_H3L :
    (penalty ![Dc.toContinuousLinearMap,Db.toContinuousLinearMap,Dz.toContinuousLinearMap]).toLinearMap =
      TGL.FiniteThreeLocks.H3L Dc Db Dz := by
  ext x
  simp [penalty,Fin.sum_univ_three,TGL.FiniteThreeLocks.H3L,
    ← LinearMap.adjoint_toContinuousLinearMap]

theorem reading_eq_kernel_PF :
    reading (penalty ![Dc.toContinuousLinearMap,Db.toContinuousLinearMap,Dz.toContinuousLinearMap]) =
      TGL.FiniteThreeLocks.PF Dc Db Dz := by
  unfold reading TGL.FiniteThreeLocks.PF
  simp only [penalty_eq_kernel_H3L]

#print axioms penalty_eq_kernel_H3L
#print axioms reading_eq_kernel_PF
end TGLExt.EquationOfTruth

/- Source body: B_fechamentos/OperatorContourBridge_v2.lean; imports relocated only. -/
set_option autoImplicit false
open scoped InnerProductSpace
noncomputable section
namespace TGLExt.EquationOfTruth
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
  [InnerProductSpace 𝕜 E] [CompleteSpace E] [FiniteDimensional 𝕜 E]

/-- Operator face, compatible with but not identical to the integer-valued contour. -/
theorem equation_of_truth_is_not_static (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜) (hne : H ≠ 0) :
    ∃ s : ℝ, 0 < s ∧ (∃ x, T H s x ≠ x) ∧ ∀ y, reading H (T H s y) = reading H y := by
  classical
  have hx : ∃ x, H x ≠ 0 := by
    by_contra hn
    push_neg at hn
    apply hne
    ext x
    exact hn x
  obtain ⟨x,hx⟩ := hx
  obtain ⟨s,hs,hchange⟩ := positive_time_changes_nonfixed_content H hH hpos x
    (fun hk => hx (LinearMap.mem_ker.mp hk))
  exact ⟨s,hs,⟨x,hchange⟩,reading_T H hH s⟩

theorem zero_operator_reading_real (x : ℝ) : reading (0 : ℝ →L[ℝ] ℝ) x = x := by
  apply Submodule.starProjection_eq_self_iff.mpr
  simp

theorem unit_operator_flow_real (s x : ℝ) :
    T (1 : ℝ →L[ℝ] ℝ) s x = Real.exp (-s) * x := by
  simpa using T_apply_eigen (1 : ℝ →L[ℝ] ℝ) 1 x (by simp) s

theorem equation_criterion_can_fail (s x : ℝ) (hs : 0 < s) (hx : x ≠ 0) :
    reading (0 : ℝ →L[ℝ] ℝ) (T (1 : ℝ →L[ℝ] ℝ) s x) ≠ reading (0 : ℝ →L[ℝ] ℝ) x := by
  rw [zero_operator_reading_real,zero_operator_reading_real,unit_operator_flow_real]
  intro he
  have he1 : Real.exp (-s) = 1 := mul_right_cancel₀ hx (by simpa using he)
  have : -s = 0 := Real.exp_injective (by simpa using he1)
  linarith

#print axioms equation_of_truth_is_not_static
#print axioms zero_operator_reading_real
#print axioms unit_operator_flow_real
#print axioms equation_criterion_can_fail
#print axioms TGLExt.truth_is_not_static_equality
#print axioms TGLExt.the_criterion_can_fail
end TGLExt.EquationOfTruth

/- Source body: B_fechamentos/QubitScalarEntropy.lean; imports relocated only. -/

set_option autoImplicit false
set_option maxHeartbeats 800000

/- Scalar B3a. No identification with matrix entropy is asserted here. -/
namespace TGLExt.EquationOfTruth.QubitScalar
open Set Real
noncomputable section

def radius (p k s : ℝ) : ℝ := Real.sqrt ((2*p-1)^2 + 4*k*Real.exp (-2*s))
def entropy (p k s : ℝ) : ℝ := Real.binEntropy ((1+radius p k s)/2)
def deficit (p k s : ℝ) : ℝ := Real.binEntropy p - entropy p k s

theorem radius_nonneg (p k s : ℝ) : 0 ≤ radius p k s := Real.sqrt_nonneg _

theorem radicand_nonneg (p k s : ℝ) (hk : 0 ≤ k) :
    0 ≤ (2*p-1)^2+4*k*Real.exp (-2*s) := by positivity

theorem radius_lt_one (p k s : ℝ) (hk : 0 ≤ k)
    (hkp : k < p*(1-p)) (hs : 0 ≤ s) : radius p k s < 1 := by
  have he : Real.exp (-2*s) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
  have hm : 4*k*Real.exp (-2*s) ≤ 4*k := by
    simpa using mul_le_mul_of_nonneg_left he (show 0 ≤ 4*k by positivity)
  apply (Real.sqrt_lt (radicand_nonneg p k s hk) (by norm_num : (0:ℝ) ≤ 1)).mpr
  nlinarith

theorem radius_antitone (p k : ℝ) (hk : 0 ≤ k) : Antitone (radius p k) := by
  intro s t hst
  apply Real.sqrt_le_sqrt
  have he : Real.exp (-2*t) ≤ Real.exp (-2*s) := Real.exp_le_exp.mpr (by linarith)
  have hm := mul_le_mul_of_nonneg_left he (show 0 ≤ 4*k by positivity)
  linarith

theorem radius_strictAnti (p k : ℝ) (hk : 0 < k) : StrictAnti (radius p k) := by
  intro s t hst
  apply Real.sqrt_lt_sqrt (radicand_nonneg p k t hk.le)
  have he : Real.exp (-2*t) < Real.exp (-2*s) := Real.exp_lt_exp.mpr (by linarith)
  have hm := mul_lt_mul_of_pos_left he (show 0 < 4*k by positivity)
  linarith

theorem entropy_argument_mem (p k s : ℝ) (hk : 0 ≤ k)
    (hkp : k < p*(1-p)) (hs : 0 ≤ s) :
    (1+radius p k s)/2 ∈ Icc (2:ℝ)⁻¹ 1 := by
  have h0 := radius_nonneg p k s
  have h1 := radius_lt_one p k s hk hkp hs
  constructor <;> norm_num <;> linarith

theorem entropy_monotoneOn (p k : ℝ) (hk : 0 ≤ k) (hkp : k < p*(1-p)) :
    MonotoneOn (entropy p k) (Ici 0) := by
  intro s hs t ht hst
  apply Real.binEntropy_strictAntiOn.antitoneOn
    (entropy_argument_mem p k t hk hkp ht)
    (entropy_argument_mem p k s hk hkp hs)
  have hr := radius_antitone p k hk hst
  linarith

theorem entropy_strictMonoOn (p k : ℝ) (hk : 0 < k) (hkp : k < p*(1-p)) :
    StrictMonoOn (entropy p k) (Ici 0) := by
  intro s hs t ht hst
  apply Real.binEntropy_strictAntiOn
    (entropy_argument_mem p k t hk.le hkp ht)
    (entropy_argument_mem p k s hk.le hkp hs)
  have hr := radius_strictAnti p k hk hst
  linarith

theorem entropy_abs_identity (p : ℝ) :
    Real.binEntropy ((1+|2*p-1|)/2) = Real.binEntropy p := by
  by_cases hp : 0 ≤ 2*p-1
  · rw [abs_of_nonneg hp]
    congr 1
    ring
  · rw [abs_of_neg (lt_of_not_ge hp)]
    have he : (1+ -(2*p-1))/2 = 1-p := by ring
    rw [he, Real.binEntropy_one_sub]

theorem radius_lower_bound (p k s : ℝ) (hk : 0 ≤ k) :
    |2*p-1| ≤ radius p k s := by
  rw [← Real.sqrt_sq_eq_abs]
  apply Real.sqrt_le_sqrt
  have hm : 0 ≤ 4*k*Real.exp (-2*s) := by positivity
  linarith

theorem asymptotic_argument_mem (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    (1+|2*p-1|)/2 ∈ Icc (2:ℝ)⁻¹ 1 := by
  have ha : |2*p-1| ≤ 1 := abs_le.mpr ⟨by linarith, by linarith⟩
  have hz := abs_nonneg (2*p-1)
  constructor <;> norm_num <;> linarith

theorem entropy_le_diagonal (p k s : ℝ) (hp0 : 0 < p) (hp1 : p < 1)
    (hk : 0 ≤ k) (hkp : k < p*(1-p)) (hs : 0 ≤ s) :
    entropy p k s ≤ Real.binEntropy p := by
  rw [← entropy_abs_identity p]
  apply Real.binEntropy_strictAntiOn.antitoneOn
    (asymptotic_argument_mem p hp0 hp1)
    (entropy_argument_mem p k s hk hkp hs)
  have hr := radius_lower_bound p k s hk
  linarith

theorem deficit_nonneg (p k s : ℝ) (hp0 : 0 < p) (hp1 : p < 1)
    (hk : 0 ≤ k) (hkp : k < p*(1-p)) (hs : 0 ≤ s) :
    0 ≤ deficit p k s := sub_nonneg.mpr (entropy_le_diagonal p k s hp0 hp1 hk hkp hs)

theorem deficit_antitoneOn (p k : ℝ) (hk : 0 ≤ k) (hkp : k < p*(1-p)) :
    AntitoneOn (deficit p k) (Ici 0) := by
  intro s hs t ht hst
  have he := entropy_monotoneOn p k hk hkp hs ht hst
  exact sub_le_sub_left he _

#print axioms radius_nonneg
#print axioms radicand_nonneg
#print axioms radius_lt_one
#print axioms radius_antitone
#print axioms radius_strictAnti
#print axioms entropy_argument_mem
#print axioms entropy_monotoneOn
#print axioms entropy_strictMonoOn
#print axioms entropy_abs_identity
#print axioms radius_lower_bound
#print axioms asymptotic_argument_mem
#print axioms entropy_le_diagonal
#print axioms deficit_nonneg
#print axioms deficit_antitoneOn
end
end TGLExt.EquationOfTruth.QubitScalar

/- Source body: B_fechamentos/QubitEntropyDerivative_v3.lean; imports relocated only. -/

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace TGLExt.EquationOfTruth.QubitScalar
open Real
noncomputable section

theorem hasDerivAt_radius (p k s : ℝ) (hr : 0 < radius p k s) :
    HasDerivAt (radius p k) (-4*k*Real.exp (-2*s)/radius p k s) s := by
  have hz : (2*p-1)^2+4*k*Real.exp (-2*s) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.mp hr)
  have hd : HasDerivAt (fun t : ℝ => (2*p-1)^2+4*k*Real.exp (-2*t))
      (-8*k*Real.exp (-2*s)) s := by
    have hraw := (((hasDerivAt_id s).const_mul (-2)).exp.const_mul (4*k)).const_add ((2*p-1)^2)
    apply hraw.congr_deriv
    simp only [id_eq]
    ring
  apply (hd.sqrt hz).congr_deriv
  change -8*k*Real.exp (-2*s)/(2*radius p k s) = -4*k*Real.exp (-2*s)/radius p k s
  field_simp [ne_of_gt hr]
  <;> ring

theorem entropy_log_ratio (r : ℝ) (hr0 : 0 ≤ r) (hr1 : r < 1) :
    Real.log (1-(1+r)/2) - Real.log ((1+r)/2) =
      -Real.log ((1+r)/(1-r)) := by
  have hp : 1+r ≠ 0 := by linarith
  have hm : 1-r ≠ 0 := by linarith
  rw [show 1-(1+r)/2 = (1-r)/2 by ring]
  rw [Real.log_div hm (by norm_num), Real.log_div hp (by norm_num), Real.log_div hp hm]
  ring

theorem hasDerivAt_entropy (p k s : ℝ) (hk : 0 ≤ k)
    (hkp : k < p*(1-p)) (hs : 0 ≤ s) (hr : 0 < radius p k s) :
    HasDerivAt (entropy p k)
      (2*k*Real.exp (-2*s)/radius p k s *
        Real.log ((1+radius p k s)/(1-radius p k s))) s := by
  have hr1 := radius_lt_one p k s hk hkp hs
  have h0 : (1+radius p k s)/2 ≠ 0 := by linarith
  have h1 : (1+radius p k s)/2 ≠ 1 := by linarith
  have hd := ((hasDerivAt_radius p k s hr).const_add 1).div_const 2
  have he := (Real.hasDerivAt_binEntropy h0 h1).comp s hd
  apply he.congr_deriv
  rw [entropy_log_ratio (radius p k s) hr.le hr1]
  ring

theorem deriv_entropy (p k s : ℝ) (hk : 0 ≤ k)
    (hkp : k < p*(1-p)) (hs : 0 ≤ s) (hr : 0 < radius p k s) :
    deriv (entropy p k) s = 2*k*Real.exp (-2*s)/radius p k s *
      Real.log ((1+radius p k s)/(1-radius p k s)) :=
  (hasDerivAt_entropy p k s hk hkp hs hr).deriv

#print axioms hasDerivAt_radius
#print axioms entropy_log_ratio
#print axioms hasDerivAt_entropy
#print axioms deriv_entropy
end
end TGLExt.EquationOfTruth.QubitScalar

/- Source body: B_fechamentos/IdempotentDephasing_v2.lean; imports relocated only. -/

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace TGLExt.EquationOfTruth.IdempotentDephasing
noncomputable section
variable {A : Type*} [NormedRing A] [NormedAlgebra ℝ A] [CompleteSpace A]

/-- Series proof: multiplication by an exponential on a right eigenfactor. -/
theorem exp_mul_of_eigenfactor (a b : A) (u : ℝ) (h : a*b = u • b) :
    NormedSpace.exp a * b = Real.exp u • b := by
  have hp : ∀ n : ℕ, a^n*b = u^n • b := by
    intro n
    induction n with
    | zero => simp
    | succ n ih =>
      rw [pow_succ', mul_assoc, ih, mul_smul_comm, h, smul_smul, ← pow_succ]
  have h1 := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℝ) a).mapL
    ((ContinuousLinearMap.mul ℝ A).flip b)
  have h2 := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℝ) u).smul_const b
  have he : NormedSpace.exp a*b = NormedSpace.exp u • b := by
    refine h1.unique ?_
    convert! h2 using 1 <;> first | rfl | (ext n; simp [hp, smul_mul_assoc, smul_smul])
  simpa only [Real.exp_eq_exp_ℝ] using he

/-- Complementary idempotents split the entire Banach-algebra exponential. -/
theorem exp_complement_idempotent (e : A) (he : e*e=e) (s : ℝ) :
    NormedSpace.exp ((-s) • (1-e)) = e + Real.exp (-s) • (1-e) := by
  have h0 : ((-s) • (1-e))*e = (0:ℝ) • e := by
    simp [smul_mul_assoc, sub_mul, he]
  have hq : (1-e)*(1-e) = 1-e := by
    noncomm_ring [he]
  have h1 : ((-s) • (1-e))*(1-e) = (-s) • (1-e) := by
    rw [smul_mul_assoc, hq]
  have hp0 := exp_mul_of_eigenfactor ((-s) • (1-e)) e 0 h0
  have hp1 := exp_mul_of_eigenfactor ((-s) • (1-e)) (1-e) (-s) h1
  have hsplit : e+(1-e) = (1:A) := by abel
  calc
    NormedSpace.exp ((-s) • (1-e)) =
        NormedSpace.exp ((-s) • (1-e))*(e+(1-e)) := by rw [hsplit, mul_one]
    _ = e+Real.exp (-s) • (1-e) := by rw [mul_add, hp0, hp1]; simp

#print axioms exp_mul_of_eigenfactor
#print axioms exp_complement_idempotent
end
end TGLExt.EquationOfTruth.IdempotentDephasing

/- Source body: B_fechamentos/FiniteGapRate_v2.lean; imports relocated only. -/

set_option autoImplicit false
set_option maxHeartbeats 1400000
namespace TGLExt.EquationOfTruth
open scoped InnerProductSpace
noncomputable section
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]

theorem diagonal_norm_bound {ι : Type*} [Fintype ι] (b : OrthonormalBasis ι 𝕜 E)
    (L : E →L[𝕜] E) (a : ι → 𝕜) (ha : ∀ i, L (b i) = a i • b i)
    (r : ℝ) (hr : 0 ≤ r) (hab : ∀ i, ‖a i‖ ≤ r) (x : E) : ‖L x‖ ≤ r*‖x‖ := by
  classical
  have hc (i : ι) : b.repr (L x) i = a i * b.repr x i := by
    conv_lhs => rw [← b.sum_repr x]
    simp [map_sum, map_smul, ha, Pi.single_apply, mul_ite, mul_comm]
  have hnorm (z : E) : ‖z‖^2 = ∑ i, ‖b.repr z i‖^2 := by
    rw [← b.repr.norm_map z, EuclideanSpace.norm_sq_eq]
  have hb : ‖L x‖^2 ≤ r^2*‖x‖^2 := by
    rw [hnorm (L x), hnorm x, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i _
    rw [hc, norm_mul, mul_pow]
    exact mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (norm_nonneg _) (hab i) 2) (sq_nonneg _)
  nlinarith [norm_nonneg (L x), norm_nonneg x, mul_nonneg hr (norm_nonneg x)]

variable [FiniteDimensional 𝕜 E] [CompleteSpace E]

theorem reading_eigen_zero (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (v : E) (ev : ℝ) (hv : H v = (ev:𝕜) • v) (hev : ev ≠ 0) : reading H v = 0 := by
  have h2 : reading H (H v) = 0 := by
    have := congrArg (fun A : E →L[𝕜] E => A v) (proj_mul_H H hH)
    simpa using this
  rw [hv, map_smul] at h2
  exact (smul_eq_zero.1 h2).resolve_left (by exact_mod_cast hev)

/-- The gap refers to precisely the eigenvalues of the self-adjoint operator H. -/
theorem finite_gap_norm_rate (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (γ : ℝ) (hγ : 0 < γ)
    (hgap : ∀ i, hH.isSymmetric.eigenvalues (rfl : Module.finrank 𝕜 E = Module.finrank 𝕜 E) i = 0 ∨
      γ ≤ hH.isSymmetric.eigenvalues (rfl : Module.finrank 𝕜 E = Module.finrank 𝕜 E) i)
    (s : ℝ) (hs : 0 ≤ s) (x : E) :
    ‖T H s x - reading H x‖ ≤ Real.exp (-(s*γ))*‖x-reading H x‖ := by
  classical
  let b := hH.isSymmetric.eigenvectorBasis (rfl : Module.finrank 𝕜 E = Module.finrank 𝕜 E)
  let ev := hH.isSymmetric.eigenvalues (rfl : Module.finrank 𝕜 E = Module.finrank 𝕜 E)
  let a := fun i => if ev i = 0 then (0:𝕜) else (Real.exp (-(s*ev i)):𝕜)
  have hv (i) : H (b i) = (ev i:𝕜) • b i := hH.isSymmetric.apply_eigenvectorBasis _ i
  have ha : ∀ i, (T H s - reading H) (b i) = a i • b i := by
    intro i
    by_cases hi : ev i = 0
    · have hk : b i ∈ H.ker := by
        change H (b i) = 0
        rw [hv, hi]
        simp
      have hp : reading H (b i) = b i := Submodule.starProjection_eq_self_iff.mpr hk
      simp [a, hi, T_fix_of_mem_ker H s hk, hp]
    · have hp := reading_eigen_zero H hH (b i) (ev i) (hv i) hi
      simp [a, hi, hp, T_apply_eigen H (ev i) (b i) (hv i) s]
  have hab : ∀ i, ‖a i‖ ≤ Real.exp (-(s*γ)) := by
    intro i
    by_cases hi : ev i = 0
    · simp [a, hi, Real.exp_nonneg]
    · have hge : γ ≤ ev i := (hgap i).resolve_left hi
      have hex : Real.exp (-(s*ev i)) ≤ Real.exp (-(s*γ)) :=
        Real.exp_le_exp.mpr (neg_le_neg (mul_le_mul_of_nonneg_left hge hs))
      simpa [a, hi, RCLike.norm_ofReal, abs_of_pos (Real.exp_pos _)] using hex
  have hbound := diagonal_norm_bound b (T H s-reading H) a ha
    (Real.exp (-(s*γ))) (Real.exp_pos _).le hab (x-reading H x)
  have hmem : reading H x ∈ H.ker := H.ker.starProjection_apply_mem x
  have hp : reading H (reading H x) = reading H x := Submodule.starProjection_eq_self_iff.mpr hmem
  simpa [map_sub, T_fix_of_mem_ker H s hmem, hp] using hbound

#print axioms diagonal_norm_bound
#print axioms reading_eigen_zero
#print axioms finite_gap_norm_rate
end
end TGLExt.EquationOfTruth

/- Source body: B_fechamentos/InfiniteLimitUniformControl_v2.lean; imports relocated only. -/

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace TGLExt.EquationOfTruth.InfiniteLimitControl
open Filter Topology Set
noncomputable section

def spectralLimit (u : ℝ) : ℝ := if u=0 then 1 else 0

/-- Pointwise scalar convergence is valid, including the zero mode. -/
theorem scalar_pointwise_limit (u : ℝ) (hu : 0 ≤ u) :
    Tendsto (fun s : ℝ => Real.exp (-(s*u))) atTop (𝓝 (spectralLimit u)) := by
  by_cases hz : u=0
  · subst u
    simpa [spectralLimit] using (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1:ℝ)) atTop (𝓝 1))
  · have hp : 0 < u := lt_of_le_of_ne hu (Ne.symm hz)
    rw [spectralLimit, if_neg hz]
    exact Real.tendsto_exp_neg_atTop_nhds_zero.comp (tendsto_id.atTop_mul_const hp)

/-- At every nonnegative time a positive spectral value retains error above exp(-1). -/
theorem uniform_error_lower_bound (s : ℝ) (hs : 0 ≤ s) :
    ∃ u ∈ Ioc (0:ℝ) 1, Real.exp (-1) < |Real.exp (-(s*u))-spectralLimit u| := by
  let u : ℝ := 1/(s+1)
  have hd : 0 < s+1 := by linarith
  have hu : 0 < u := one_div_pos.mpr hd
  have hu1 : u ≤ 1 := by
    apply (div_le_iff₀ hd).mpr
    linarith
  have hsu : s*u < 1 := by
    dsimp [u]
    rw [← mul_div_assoc, mul_one]
    apply (div_lt_iff₀ hd).mpr
    linarith
  refine ⟨u, ⟨hu, hu1⟩, ?_⟩
  rw [spectralLimit, if_neg (ne_of_gt hu), sub_zero, abs_of_pos (Real.exp_pos _)]
  exact Real.exp_lt_exp.mpr (by linarith)

/-- Thus even a fixed positive uniform tolerance cannot be achieved on [0,1]. -/
theorem no_uniform_small_error :
    ¬ ∃ s : ℝ, 0 ≤ s ∧ ∀ u ∈ Icc (0:ℝ) 1,
      |Real.exp (-(s*u))-spectralLimit u| < Real.exp (-1) := by
  rintro ⟨s, hs, hbound⟩
  obtain ⟨u, hu, herr⟩ := uniform_error_lower_bound s hs
  have hb := hbound u ⟨hu.1.le, hu.2⟩
  linarith

#print axioms scalar_pointwise_limit
#print axioms uniform_error_lower_bound
#print axioms no_uniform_small_error
end
end TGLExt.EquationOfTruth.InfiniteLimitControl

/- Source body: B_fechamentos/ModularGeneratorControl.lean; imports relocated only. -/

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace TGLExt.EquationOfTruth.ModularGeneratorControl
open Matrix NormedSpace
open scoped ComplexOrder MatrixOrder
noncomputable section
variable {n : Type} [Fintype n] [DecidableEq n]

/-- Vanishing of the generator on y is commutation with rho for a positive definite rho. -/
theorem modularGen_zero_iff_commute (ρ y : Matrix n n ℂ) (hρ : ρ.PosDef) :
    TGLExt.modularGen ρ y = 0 ↔ Commute ρ y := by
  constructor
  · intro h
    have hc : Commute (TGLExt.logRho ρ) y := by
      show TGLExt.logRho ρ*y = y*TGLExt.logRho ρ
      exact (sub_eq_zero.mp h).symm
    have he := hc.exp_left
    rwa [TGLExt.exp_logRho ρ hρ] at he
  · intro hc
    have hl := hc.cfc_real Real.log
    unfold TGLExt.modularGen TGLExt.logRho
    rw [hl.eq, sub_self]

theorem scalar_modularGen_zero (c : ℂ) (y : Matrix n n ℂ) :
    TGLExt.modularGen (c • (1:Matrix n n ℂ)) y = 0 := by
  have hc : Commute (c • (1:Matrix n n ℂ)) y := by
    show (c • (1:Matrix n n ℂ))*y = y*(c • (1:Matrix n n ℂ))
    simp [smul_mul_assoc, mul_smul_comm]
  have hl := hc.cfc_real Real.log
  unfold TGLExt.modularGen TGLExt.logRho
  rw [hl.eq, sub_self]

def rhoExample : Matrix (Fin 2) (Fin 2) ℂ := diagonal ![1/3,2/3]
def matrixUnit : Matrix (Fin 2) (Fin 2) ℂ := !![0,1;0,0]

theorem rhoExample_posDef : rhoExample.PosDef := by
  rw [rhoExample, Matrix.posDef_diagonal_iff]
  intro i
  fin_cases i <;> norm_num

theorem rhoExample_trace : Matrix.trace rhoExample = 1 := by
  norm_num [rhoExample, Matrix.trace, Fin.sum_univ_two]

theorem example_generator_nonzero : TGLExt.modularGen rhoExample matrixUnit ≠ 0 := by
  intro hz
  have hc := (modularGen_zero_iff_commute rhoExample matrixUnit rhoExample_posDef).mp hz
  have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℂ => M 0 1) hc.eq
  norm_num [rhoExample, matrixUnit, Matrix.mul_apply, Fin.sum_univ_two] at he

theorem exists_normalized_nonzero_generator :
    ∃ ρ : Matrix (Fin 2) (Fin 2) ℂ, ρ.PosDef ∧ Matrix.trace ρ=1 ∧ TGLExt.modularGen ρ ≠ 0 := by
  refine ⟨rhoExample, rhoExample_posDef, rhoExample_trace, ?_⟩
  intro h
  apply example_generator_nonzero
  exact congrFun h matrixUnit

#print axioms modularGen_zero_iff_commute
#print axioms scalar_modularGen_zero
#print axioms rhoExample_posDef
#print axioms rhoExample_trace
#print axioms example_generator_nonzero
#print axioms exists_normalized_nonzero_generator
end
end TGLExt.EquationOfTruth.ModularGeneratorControl

/- Source body: C_controles/TheEquationOfTruth_T20_controles_v3.lean; imports relocated only. -/

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace TGLExt.EquationOfTruth.NegativeControls
open Matrix Filter Topology
noncomputable section

def diagonalFlow (a b s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  NormedSpace.exp ((-s) • diagonal ![a,b])

theorem diagonalFlow_eq (a b s : ℝ) :
    diagonalFlow a b s = diagonal ![Real.exp (-(s*a)),Real.exp (-(s*b))] := by
  unfold diagonalFlow
  rw [← Matrix.diagonal_smul, Matrix.exp_diagonal]
  congr 1
  ext i
  fin_cases i <;> simp [Pi.coe_exp, ← Real.exp_eq_exp_ℝ, neg_mul]

theorem diagonalFlow_mulVec (a b s : ℝ) (x : Fin 2 → ℝ) :
    (diagonalFlow a b s).mulVec x =
      ![Real.exp (-(s*a))*x 0, Real.exp (-(s*b))*x 1] := by
  rw [diagonalFlow_eq]
  ext i
  fin_cases i <;> simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]

def oblique : Matrix (Fin 2) (Fin 2) ℝ := !![1,-1;0,0]
def splitH : Matrix (Fin 2) (Fin 2) ℝ := diagonal ![0,1]
def fixedP : Matrix (Fin 2) (Fin 2) ℝ := diagonal ![1,0]

theorem C1_1_oblique_algebra :
    oblique*oblique=oblique ∧ splitH*oblique=0 ∧ oblique*splitH ≠ 0 := by
  refine ⟨?_,?_,?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [oblique,Matrix.mul_apply,Fin.sum_univ_two]
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [oblique,splitH,Matrix.mul_apply,Fin.sum_univ_two]
  · intro h
    have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    norm_num [oblique,splitH,Matrix.mul_apply,Fin.sum_univ_two] at he

theorem C1_1_oblique_flow_fails (s : ℝ) (hs : 0 < s) :
    oblique*diagonalFlow 0 1 s ≠ oblique := by
  intro he
  have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) he
  simp [oblique,diagonalFlow_eq,Matrix.mul_apply,Fin.sum_univ_two] at h
  have he1 : Real.exp (-s)=1 := by linarith
  have hz : -s=0 := Real.exp_injective (by simpa using he1)
  linarith

def nilpotentH : Matrix (Fin 2) (Fin 2) ℝ := !![0,1;0,0]

theorem C1_2_nonsymmetric :
    nilpotentH.transpose ≠ nilpotentH ∧ fixedP.transpose=fixedP ∧ fixedP*nilpotentH ≠ 0 := by
  refine ⟨?_,?_,?_⟩
  · intro h
    have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    norm_num [nilpotentH] at he
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [fixedP]
  · intro h
    have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    norm_num [fixedP,nilpotentH,Matrix.mul_apply,Fin.sum_univ_two] at he

theorem C1_2_kernel_selected (x : Fin 2 → ℝ) :
    nilpotentH.mulVec x=0 ↔ x 1=0 := by
  simp [nilpotentH,Matrix.mulVec,dotProduct,Fin.sum_univ_two,funext_iff,Fin.forall_fin_two]

theorem negative_unit_flow (s x : ℝ) :
    T (-1 : ℝ →L[ℝ] ℝ) s x = Real.exp s*x := by
  simpa using T_apply_eigen (-1 : ℝ →L[ℝ] ℝ) (-1) x (by simp) s

theorem C1_3a_indefinite_no_limit (x : ℝ) (hx : x ≠ 0) :
    ¬ Tendsto (fun s : ℝ => T (-1 : ℝ →L[ℝ] ℝ) s x) atTop (𝓝 0) := by
  intro h
  have hn := continuous_abs.continuousAt.tendsto.comp h
  have ht : Tendsto (fun s : ℝ => Real.exp s*|x|) atTop atTop :=
    Real.tendsto_exp_atTop.atTop_mul_const (abs_pos.mpr hx)
  have hn0 : Tendsto (fun s : ℝ => Real.exp s*|x|) atTop (𝓝 0) := by
    simpa [Function.comp_def,negative_unit_flow,abs_mul,abs_of_pos (Real.exp_pos _)] using hn
  exact not_tendsto_atTop_of_tendsto_nhds hn0 ht

def productReader (x : Fin 2 → ℝ) : ℝ := x 0*x 1

theorem C1_3b_product_conserved (s : ℝ) (x : Fin 2 → ℝ) :
    productReader ((diagonalFlow 3 (-3) s).mulVec x)=productReader x := by
  rw [diagonalFlow_mulVec]
  simp only [productReader,Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.head_cons]
  have he : Real.exp (-(s*3))*Real.exp (-(s*(-3)))=1 := by
    rw [← Real.exp_add]
    convert Real.exp_zero using 1 <;> ring
  calc
    Real.exp (-(s*3))*x 0*(Real.exp (-(s*(-3)))*x 1) =
      (Real.exp (-(s*3))*Real.exp (-(s*(-3))))*(x 0*x 1) := by ring
    _ = x 0*x 1 := by rw [he,one_mul]

theorem C1_3b_reader_continuous : Continuous productReader := by
  unfold productReader
  fun_prop

theorem C1_3b_reader_not_factor : productReader (![1,1] : Fin 2 → ℝ) ≠ productReader 0 := by
  norm_num [productReader]

def discontinuousReader (x : Fin 2 → ℝ) : ℝ := if x 1=0 then 0 else 1

theorem C1_4_reader_conserved (s : ℝ) (x : Fin 2 → ℝ) :
    discontinuousReader ((diagonalFlow 0 1 s).mulVec x)=discontinuousReader x := by
  rw [diagonalFlow_mulVec]
  simp [discontinuousReader,mul_eq_zero,Real.exp_ne_zero]

theorem C1_4_reader_not_factor :
    discontinuousReader (fixedP.mulVec (![0,1] : Fin 2 → ℝ)) ≠ discontinuousReader ![0,1] := by
  norm_num [discontinuousReader,fixedP,Matrix.mulVec,dotProduct,Fin.sum_univ_two]

theorem C1_5_constant_false_positive :
    ∃ x y : Fin 2 → ℝ, fixedP.mulVec x ≠ fixedP.mulVec y ∧
      (fun _ : Fin 2 → ℝ => (1:ℝ)) x = (fun _ : Fin 2 → ℝ => (1:ℝ)) y := by
  refine ⟨![0,0],![1,0],?_,rfl⟩
  intro h
  have he := congrFun h 0
  norm_num [fixedP,Matrix.mulVec,dotProduct,Fin.sum_univ_two] at he

theorem C1_6_outside_bits : truthValue 2 0 = -3 ∧ truthValue 2 0 ≠ 0 ∧ truthValue 2 0 ≠ 1 := by
  norm_num [truthValue]

theorem C1_7_bad_pruning (s x : ℝ) (hs : 0 < s) (hx : x ≠ 0) :
    reading (0 : ℝ →L[ℝ] ℝ) (T (1 : ℝ →L[ℝ] ℝ) s x) ≠ reading (0 : ℝ →L[ℝ] ℝ) x :=
  equation_criterion_can_fail s x hs hx

theorem C1_8_signed_penalty :
    ((ContinuousLinearMap.adjoint (1 : ℝ →L[ℝ] ℝ)*1 -
       ContinuousLinearMap.adjoint (1 : ℝ →L[ℝ] ℝ)*1) : ℝ →L[ℝ] ℝ).ker = ⊤ ∧
    (1 : ℝ →L[ℝ] ℝ).ker ⊓ (1 : ℝ →L[ℝ] ℝ).ker = ⊥ ∧
    (⊤ : Submodule ℝ ℝ) ≠ ⊥ := by
  have hk : (1 : ℝ →L[ℝ] ℝ).ker = ⊥ := by
    ext x
    change (x=0) ↔ (x=0)
    rfl
  refine ⟨by simp, ?_, top_ne_bot⟩
  rw [hk]
  simp

theorem C1_9_invalid_qubit : (1/2:ℝ)*(1-1/2)-(3/5)^2 < 0 := by norm_num


theorem fixedP_idempotent : fixedP*fixedP=fixedP := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [fixedP,Matrix.mul_apply,Fin.sum_univ_two]

theorem fixedP_selects_kernel (x : Fin 2 → ℝ) : fixedP.mulVec x=x ↔ x 1=0 := by
  simp [fixedP,Matrix.mulVec,dotProduct,Fin.sum_univ_two,funext_iff,Fin.forall_fin_two,eq_comm]

theorem indefinite_kernel_zero (x : Fin 2 → ℝ) :
    (diagonal ![3,-3] : Matrix (Fin 2) (Fin 2) ℝ).mulVec x=0 ↔ x=0 := by
  simp [Matrix.mulVec,dotProduct,Fin.sum_univ_two,funext_iff,Fin.forall_fin_two]

theorem negative_unit_kernel : (-1 : ℝ →L[ℝ] ℝ).ker = ⊥ := by
  ext x
  change (-x=0) ↔ (x=0)
  simp

theorem C1_4_not_continuous : ¬ Continuous discontinuousReader := by
  intro h
  have hv : Tendsto (fun t : ℝ => (![0,Real.exp (-t)] : Fin 2 → ℝ)) atTop (𝓝 0) := by
    apply tendsto_pi_nhds.mpr
    intro i
    fin_cases i
    · simpa using (tendsto_const_nhds : Tendsto (fun _ : ℝ => (0:ℝ)) atTop (𝓝 0))
    · simpa using Real.tendsto_exp_neg_atTop_nhds_zero
  have hh := h.continuousAt.tendsto.comp hv
  have h10 : Tendsto (fun _ : ℝ => (1:ℝ)) atTop (𝓝 0) := by
    simpa [Function.comp_def,discontinuousReader,Real.exp_ne_zero] using hh
  have he : (1:ℝ)=0 := tendsto_nhds_unique tendsto_const_nhds h10
  norm_num at he

#print axioms fixedP_idempotent
#print axioms fixedP_selects_kernel
#print axioms indefinite_kernel_zero
#print axioms negative_unit_kernel
#print axioms C1_4_not_continuous

#print axioms diagonalFlow_eq
#print axioms diagonalFlow_mulVec
#print axioms C1_1_oblique_algebra
#print axioms C1_1_oblique_flow_fails
#print axioms C1_2_nonsymmetric
#print axioms C1_2_kernel_selected
#print axioms negative_unit_flow
#print axioms C1_3a_indefinite_no_limit
#print axioms C1_3b_product_conserved
#print axioms C1_3b_reader_continuous
#print axioms C1_3b_reader_not_factor
#print axioms C1_4_reader_conserved
#print axioms C1_4_reader_not_factor
#print axioms C1_5_constant_false_positive
#print axioms C1_6_outside_bits
#print axioms C1_7_bad_pruning
#print axioms C1_8_signed_penalty
#print axioms C1_9_invalid_qubit
end
end TGLExt.EquationOfTruth.NegativeControls

/- Source body: C_controles/NegativeControlsCompleteness_v2.lean; imports relocated only. -/

set_option autoImplicit false
namespace TGLExt.EquationOfTruth.NegativeControls
open Matrix
open scoped ComplexOrder
noncomputable section

theorem constant_reader_always_conserved
    (F : ℝ → (Fin 2 → ℝ) → (Fin 2 → ℝ)) (s : ℝ) (x : Fin 2 → ℝ) :
    (fun _ : Fin 2 → ℝ => (1:ℝ)) (F s x) = (fun _ : Fin 2 → ℝ => (1:ℝ)) x := rfl

def invalidDensity : Matrix (Fin 2) (Fin 2) ℂ := !![1/2,3/5;3/5,1/2]

theorem invalidDensity_trace_one : Matrix.trace invalidDensity=1 := by
  norm_num [invalidDensity,Matrix.trace,Fin.sum_univ_two]

theorem invalidDensity_determinant : Matrix.det invalidDensity = -(11/100:ℂ) := by
  norm_num [invalidDensity,Matrix.det_fin_two]

theorem invalidDensity_not_positive : ¬ invalidDensity.PosSemidef := by
  intro hp
  have hq := hp.dotProduct_mulVec_nonneg (![1,-1] : Fin 2 → ℂ)
  norm_num [invalidDensity,Matrix.mulVec,dotProduct,Fin.sum_univ_two] at hq
  norm_num [Complex.le_def] at hq

#print axioms constant_reader_always_conserved
#print axioms invalidDensity_trace_one
#print axioms invalidDensity_determinant
#print axioms invalidDensity_not_positive
end
end TGLExt.EquationOfTruth.NegativeControls
