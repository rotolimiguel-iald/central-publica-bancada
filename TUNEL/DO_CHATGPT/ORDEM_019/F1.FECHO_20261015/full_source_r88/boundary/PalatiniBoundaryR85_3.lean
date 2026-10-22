import TGLExt.MetricRicciVariation
import TGLExt.GeometricEinsteinReconstruction
import TGLExt.LeviCivitaLieVariation

/-!
R85 candidate: genuine curved Palatini contraction and its first boundary current.
The connection direction is a (1,2) tensor; its lower connection index is included.
The inverse-metric compatibility used below is proved by the existing kernel lemma.
This does not yet identify W with div(H)-grad(tr h), integrate the df*W term
into Hess(f), or convert covariant divergence to partial_a(sqrt|g| W^a).
No stationarity in P, Euler-Lagrange equation, boundary condition, or H3 is assumed
or concluded. The actual metric family is g+t h, not an independent variation of
g(P) with P fixed. Regularity of the direction C is an explicit local hypothesis.
-/

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.PalatiniBoundaryR85
open Matrix Filter Topology Set ChatgptAudit.CurvedConnection
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci ChatgptAudit.MetricLieConnection
noncomputable section

def directionCovariantDerivative (Gamma C : ConnectionField4) (x : Coordinate4)
    (k j : Fin 4) : Tensor4 :=
  mixedCovariantDerivative Gamma (fun y => C y j) x k -
    ∑ l : Fin 4, Gamma x k l j • C x l

theorem curvature_variation_full_covariant (Gamma C : ConnectionField4)
    (x : Coordinate4) (ht : ∀ i j l, Gamma x i l j = Gamma x j l i)
    (i j : Fin 4) :
    curvatureVariation Gamma C x i j =
      directionCovariantDerivative Gamma C x i j -
      directionCovariantDerivative Gamma C x j i := by
  rw [curvature_variation_covariant_exterior]
  simp only [directionCovariantDerivative, ht i j]
  abel

theorem ricci_variation_palatini (Gamma C : ConnectionField4)
    (x : Coordinate4) (ht : ∀ i j l, Gamma x i l j = Gamma x j l i)
    (b j : Fin 4) :
    ricciVariation Gamma C x b j = ∑ a : Fin 4,
      (directionCovariantDerivative Gamma C x a j a b -
       directionCovariantDerivative Gamma C x j a a b) := by
  unfold ricciVariation
  simp only [curvature_variation_full_covariant Gamma C x ht, Matrix.sub_apply]

def palatiniCurrent (q : TensorField4) (C : ConnectionField4) : VectorField4 :=
  fun x a => ∑ b : Fin 4, ∑ j : Fin 4,
    (q x b j * C x j a b - q x b a * C x j j b)

theorem current_partial (q : TensorField4) (C : ConnectionField4) (x : Coordinate4)
    (hq : ∀ b j, DifferentiableAt ℝ (fun y => q y b j) x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => C y j a b) x)
    (k a : Fin 4) :
    coordinatePartial (fun y => palatiniCurrent q C y a) x k =
      ∑ b : Fin 4, ∑ j : Fin 4,
        (tensorFieldJet q x k b j * C x j a b + q x b j * connectionFirstJet C x k j a b -
         (tensorFieldJet q x k b a * C x j j b + q x b a * connectionFirstJet C x k j j b)) := by
  unfold palatiniCurrent
  have hb (b : Fin 4) : DifferentiableAt ℝ
      (fun y => ∑ j : Fin 4, (q y b j * C y j a b - q y b a * C y j j b)) x := by
    exact DifferentiableAt.fun_sum fun j (_ : j ∈ (Finset.univ : Finset (Fin 4))) =>
      ((hq b j).mul (hC j a b)).sub ((hq b a).mul (hC j j b))
  rw [coordinatePartial_sum (fun b y => ∑ j : Fin 4,
    (q y b j * C y j a b - q y b a * C y j j b)) x hb k]
  apply Finset.sum_congr rfl
  intro b _
  rw [coordinatePartial_sum (fun j y => q y b j * C y j a b - q y b a * C y j j b)
    x (fun j => ((hq b j).mul (hC j a b)).sub ((hq b a).mul (hC j j b))) k]
  apply Finset.sum_congr rfl
  intro j _
  rw [coordinatePartial_sub (fun y => q y b j * C y j a b)
    (fun y => q y b a * C y j j b) x ((hq b j).mul (hC j a b))
    ((hq b a).mul (hC j j b)) k,
    coordinatePartial_mul (fun y => q y b j) (fun y => C y j a b) x (hq b j) (hC j a b) k,
    coordinatePartial_mul (fun y => q y b a) (fun y => C y j j b) x (hq b a) (hC j j b) k]
  rfl

theorem current_covariant_derivative (q : TensorField4) (Gamma C : ConnectionField4)
    (x : Coordinate4)
    (hq : ∀ b j, DifferentiableAt ℝ (fun y => q y b j) x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => C y j a b) x)
    (hparallel : ∀ k, tensorFieldJet q x k = -Gamma x k * q x - q x * (Gamma x k)ᵀ)
    (k a : Fin 4) :
    covariantVectorDerivative Gamma (palatiniCurrent q C) x k a =
      ∑ b : Fin 4, ∑ j : Fin 4,
        (q x b j * directionCovariantDerivative Gamma C x k j a b -
         q x b a * directionCovariantDerivative Gamma C x k j j b) := by
  change coordinatePartial (fun y => palatiniCurrent q C y a) x k +
    (Gamma x k).mulVec (palatiniCurrent q C x) a = _
  rw [current_partial q C x hq hC k a, hparallel k]
  simp only [directionCovariantDerivative, mixedCovariantDerivative, connectionFirstJet,
    palatiniCurrent, Matrix.mulVec, dotProduct, Matrix.mul_apply, Matrix.sub_apply,
    Matrix.add_apply, Matrix.neg_apply, Matrix.transpose_apply, Matrix.smul_apply,
    Matrix.sum_apply, smul_eq_mul, Fin.sum_univ_four]
  ring

theorem contracted_ricci_is_current_divergence (q : TensorField4)
    (Gamma C : ConnectionField4) (x : Coordinate4)
    (hq : ∀ b j, DifferentiableAt ℝ (fun y => q y b j) x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => C y j a b) x)
    (ht : ∀ i j l, Gamma x i l j = Gamma x j l i)
    (hparallel : ∀ k, tensorFieldJet q x k = -Gamma x k * q x - q x * (Gamma x k)ᵀ) :
    (∑ b : Fin 4, ∑ j : Fin 4, q x b j * ricciVariation Gamma C x b j) =
      vectorExpansion Gamma (palatiniCurrent q C) x := by
  simp only [ricci_variation_palatini Gamma C x ht, vectorExpansion, Matrix.trace, Matrix.diag_apply,
    covariantVectorGradient, current_covariant_derivative q Gamma C x hq hC hparallel]
  simp only [Fin.sum_univ_four]
  ring

theorem actual_metric_ricci_boundary_derivative
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (hi : ∀ y∈U, IsUnit (g y))
    (x : Coordinate4) (hx : x∈U)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => metricConnectionVariation g h y j a b) x) :
    HasDerivAt (fun t => ∑ b : Fin 4, ∑ j : Fin 4,
      (g x)⁻¹ b j * coordinateRicci (perturbedLeviCivita g h t) x b j)
      (vectorExpansion (leviCivitaField g (fun y => (g y)⁻¹))
        (palatiniCurrent (fun y => (g y)⁻¹) (metricConnectionVariation g h)) x) 0 := by
  let Gamma := leviCivitaField g (fun y => (g y)⁻¹)
  have hgi := smooth_matrix_inverse U g hg hi
  have hm : MetricCompatibleOn U g Gamma := by
    intro y hy i
    exact levi_civita_field_metric_compatible U hU g (fun y => (g y)⁻¹) hs
      (fun y hy => actual_inverse_left (g y) (hi y hy))
      (fun y hy => actual_inverse_right (g y) (hi y hy)) y hy i
  have ht : ∀ i j l, Gamma x i l j = Gamma x j l i :=
    levi_civita_field_torsion_free U hU g (fun y => (g y)⁻¹) hs x hx
  have hp := inverse_metric_derivative U hU g (fun y => (g y)⁻¹) Gamma hg hgi hm
    (fun y hy => actual_inverse_left (g y) (hi y hy))
    (fun y hy => actual_inverse_right (g y) (hi y hy)) x hx
  have he := contracted_ricci_is_current_divergence (fun y => (g y)⁻¹) Gamma
    (metricConnectionVariation g h) x (smooth_matrix_differentiableAt U hU _ hgi x hx) hC ht hp
  rw [← he]
  exact HasDerivAt.fun_sum fun b _ => HasDerivAt.fun_sum fun j _ =>
    (metric_ricci_first_variation U hU g h hg hh hi x hx b j).const_mul ((g x)⁻¹ b j)

#print axioms directionCovariantDerivative
#print axioms curvature_variation_full_covariant
#print axioms ricci_variation_palatini
#print axioms palatiniCurrent
#print axioms current_partial
#print axioms current_covariant_derivative
#print axioms contracted_ricci_is_current_divergence
#print axioms actual_metric_ricci_boundary_derivative
end
end ChatgptAudit.PalatiniBoundaryR85
