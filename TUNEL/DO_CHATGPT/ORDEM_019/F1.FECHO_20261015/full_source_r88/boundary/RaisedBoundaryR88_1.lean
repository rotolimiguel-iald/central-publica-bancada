import SymmetricBoundaryR87_2

/-! R88: actual derivatives of the raised variation and its trace, using the
parallel inverse metric already established for the real Levi-Civita connection.
Connects the R87 current to div(H)-grad(tr h), with H=g^-1 h g^-1.
No Hessian weighted current, action stationarity in P, or full physical source
is asserted here. Canonical sources are imported read-only. -/
set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.RaisedBoundaryR88
open Matrix Filter Topology Set ChatgptAudit.CurvedConnection
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci ChatgptAudit.MetricLieConnection
  ChatgptAudit.PalatiniBoundaryR85 ChatgptAudit.SymmetricBoundaryR87
noncomputable section

/-- Covariant derivative of a tensor with two upper indices, using actual partials. -/
def contravariantTensorDerivative (Gamma : ConnectionField4) (A : TensorField4)
    (x : Coordinate4) (k : Fin 4) : Tensor4 :=
  tensorFieldJet A x k + Gamma x k * A x + A x * (Gamma x k)ᵀ

theorem product_entry_differentiable (A B : TensorField4) (x : Coordinate4)
    (hA : ∀ i j, DifferentiableAt ℝ (fun y => A y i j) x)
    (hB : ∀ i j, DifferentiableAt ℝ (fun y => B y i j) x) :
    ∀ i j, DifferentiableAt ℝ (fun y => (A y * B y) i j) x := by
  intro i j
  change DifferentiableAt ℝ (fun y => ∑ k : Fin 4, A y i k * B y k j) x
  exact DifferentiableAt.fun_sum fun k _ => (hA i k).mul (hB k j)

theorem raised_variation_actual_derivative (q h : TensorField4)
    (Gamma : ConnectionField4) (x : Coordinate4)
    (hq : ∀ i j, DifferentiableAt ℝ (fun y => q y i j) x)
    (hh : ∀ i j, DifferentiableAt ℝ (fun y => h y i j) x)
    (hp : ∀ k, tensorFieldJet q x k = -Gamma x k * q x - q x * (Gamma x k)ᵀ)
    (k : Fin 4) :
    contravariantTensorDerivative Gamma (fun y => q y * h y * q y) x k =
      q x * covariantTensorJet (h x) (tensorFieldJet h x) (Gamma x) k * q x := by
  unfold contravariantTensorDerivative
  rw [tensorFieldJet_mul (fun y => q y * h y) q x
      (product_entry_differentiable q h x hq hh) hq k,
    tensorFieldJet_mul q h x hq hh k, hp k]
  unfold covariantTensorJet
  noncomm_ring

theorem trace_variation_actual_derivative (q h : TensorField4)
    (Gamma : ConnectionField4) (x : Coordinate4)
    (hq : ∀ i j, DifferentiableAt ℝ (fun y => q y i j) x)
    (hh : ∀ i j, DifferentiableAt ℝ (fun y => h y i j) x)
    (hp : ∀ k, tensorFieldJet q x k = -Gamma x k * q x - q x * (Gamma x k)ᵀ)
    (k : Fin 4) :
    coordinatePartial (fun y => Matrix.trace (q y * h y)) x k =
      Matrix.trace (q x * covariantTensorJet (h x) (tensorFieldJet h x) (Gamma x) k) := by
  rw [coordinatePartial_trace (fun y => q y * h y) x
      (product_entry_differentiable q h x hq hh) k,
    tensorFieldJet_mul q h x hq hh k, hp k]
  have ht : Matrix.trace (Gamma x k * q x * h x) =
      Matrix.trace (q x * h x * Gamma x k) := by
    rw [Matrix.mul_assoc, Matrix.trace_mul_comm]
  have he : (-Gamma x k * q x - q x * (Gamma x k)ᵀ) * h x +
      q x * tensorFieldJet h x k =
      q x * covariantTensorJet (h x) (tensorFieldJet h x) (Gamma x) k +
        (q x * h x * Gamma x k - Gamma x k * q x * h x) := by
    unfold covariantTensorJet
    noncomm_ring
  rw [he, Matrix.trace_add, Matrix.trace_sub, ht, sub_self, add_zero]

/-- The parallelism premise used above is a theorem of the actual metric, not input data. -/
theorem actual_inverse_parallel
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4)
    (hg : SmoothMatrixOn U g) (hs : ∀ y∈U, (g y)ᵀ=g y)
    (hi : ∀ y∈U, IsUnit (g y)) (x : Coordinate4) (hx : x∈U) (k : Fin 4) :
    tensorFieldJet (fun y => (g y)⁻¹) x k =
      -(leviCivitaField g (fun y => (g y)⁻¹) x k) * (g x)⁻¹ -
        (g x)⁻¹ * (leviCivitaField g (fun y => (g y)⁻¹) x k)ᵀ := by
  apply inverse_metric_derivative U hU g (fun y => (g y)⁻¹)
    (leviCivitaField g (fun y => (g y)⁻¹)) hg (smooth_matrix_inverse U g hg hi)
    _ (fun y hy => actual_inverse_left (g y) (hi y hy))
    (fun y hy => actual_inverse_right (g y) (hi y hy)) x hx k
  intro y hy i
  exact levi_civita_field_metric_compatible U hU g (fun y => (g y)⁻¹) hs
    (fun y hy => actual_inverse_left (g y) (hi y hy))
    (fun y hy => actual_inverse_right (g y) (hi y hy)) y hy i

theorem actual_palatini_current_divergence_trace
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hd : SmoothMatrixOn U h)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (hh : ∀ y∈U, (h y)ᵀ=h y)
    (hi : ∀ y∈U, IsUnit (g y)) (x : Coordinate4) (hx : x∈U) (a : Fin 4) :
    palatiniCurrent (fun y => (g y)⁻¹) (metricConnectionVariation g h) x a =
      (∑ b : Fin 4, contravariantTensorDerivative
        (leviCivitaField g (fun y => (g y)⁻¹))
        (fun y => (g y)⁻¹ * h y * (g y)⁻¹) x b a b) -
      ∑ k : Fin 4, (g x)⁻¹ a k *
        coordinatePartial (fun y => Matrix.trace ((g y)⁻¹ * h y)) x k := by
  have hq := smooth_matrix_differentiableAt U hU (fun y => (g y)⁻¹)
    (smooth_matrix_inverse U g hg hi) x hx
  have hhd := smooth_matrix_differentiableAt U hU h hd x hx
  have hp := actual_inverse_parallel U hU g hg hs hi x hx
  simp_rw [raised_variation_actual_derivative _ _ _ x hq hhd hp,
    trace_variation_actual_derivative _ _ _ x hq hhd hp]
  exact actual_palatini_current_covariant U hU g h hs hh hi x hx a

#print axioms contravariantTensorDerivative
#print axioms product_entry_differentiable
#print axioms raised_variation_actual_derivative
#print axioms trace_variation_actual_derivative
#print axioms actual_inverse_parallel
#print axioms actual_palatini_current_divergence_trace
end
end ChatgptAudit.RaisedBoundaryR88
