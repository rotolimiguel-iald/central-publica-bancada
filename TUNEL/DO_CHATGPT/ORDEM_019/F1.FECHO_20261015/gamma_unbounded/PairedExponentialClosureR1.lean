import PairedExponentialPolarizationR1
import Mathlib.Analysis.LocallyConvex.SeparatingDual

/-! Closed-span membership from two-coordinate analytic polarization.
Hahn-Banach is applied to the quotient of the actual closed submodule. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.PairedExponential
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential

private theorem mem_closed_of_functionals {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]
    (L : Submodule ℂ E) (hL : IsClosed (L : Set E)) (x : E)
    (hx : ∀ l : E →L[ℂ] ℂ, (∀ y ∈ L, l y = 0) → l x = 0) : x ∈ L := by
  letI : IsClosed (L : Set E) := hL
  by_contra hn
  have hq : L.mkQL x ≠ 0 := by
    intro h
    exact hn (Submodule.Quotient.mk_eq_zero.mp h)
  obtain ⟨l,hl⟩ := SeparatingDual.exists_ne_zero (R := ℂ) hq
  apply hl
  apply hx (l.comp L.mkQL)
  intro y hy
  change l (L.mkQL y) = 0
  have h : L.mkQL y = 0 := Submodule.Quotient.mk_eq_zero.mpr hy
  rw [h,map_zero]

private theorem functional_pair (l : (F × F) →L[ℂ] ℂ) :
    ∃ v w : F, ∀ x y : F, l (x,y) = inner ℂ v x + inner ℂ w y := by
  let v := (InnerProductSpace.toDual ℂ F).symm (l.comp (ContinuousLinearMap.inl ℂ F F))
  let w := (InnerProductSpace.toDual ℂ F).symm (l.comp (ContinuousLinearMap.inr ℂ F F))
  refine ⟨v,w,?_⟩
  intro x y
  change l (x,y) = inner ℂ ((InnerProductSpace.toDual ℂ F).symm _) x +
    inner ℂ ((InnerProductSpace.toDual ℂ F).symm _) y
  rw [InnerProductSpace.toDual_symm_apply,InnerProductSpace.toDual_symm_apply]
  change l (x,y) = l (x,0) + l (0,y)
  rw [← map_add]
  congr 1
  exact Prod.ext (add_zero x).symm (zero_add y).symm

def pairCore (K : Submodule ℝ H1) (A : H1 → H1) : Submodule ℂ (F × F) :=
  Submodule.span ℂ ((fun x => (exponential x,exponential (A x))) '' (K : Set H1))

theorem complexification_pair_mem_closure (K : Submodule ℝ H1) (A : H1 → H1)
    (hadd : ∀ x y, A (x+y) = A x + A y)
    (hreal : ∀ (t : ℝ) x, A (t•x) = t•A x)
    (x y : H1) (hx : x ∈ K) (hy : y ∈ K) :
    (exponential (x+Complex.I•y),exponential (A x+Complex.I•A y)) ∈
      (pairCore K A).topologicalClosure := by
  apply mem_closed_of_functionals _ (pairCore K A).isClosed_topologicalClosure
  intro l hl
  obtain ⟨v,w,hvw⟩ := functional_pair l
  rw [hvw]
  apply pair_orthogonal_complexification K A hadd hreal v w
  · intro z hz
    rw [← hvw]
    exact hl _ ((pairCore K A).le_topologicalClosure (Submodule.subset_span ⟨z,hz,rfl⟩))
  · exact hx
  · exact hy

end F1Fecho.PairedExponential
#print axioms F1Fecho.PairedExponential.complexification_pair_mem_closure
