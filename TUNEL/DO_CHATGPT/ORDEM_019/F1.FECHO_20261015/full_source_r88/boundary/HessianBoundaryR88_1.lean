import RaisedBoundaryR88_1

/-! The weighted Hessian boundary current uses real coordinate derivatives.
For the symmetric actual metric variation H=q h q, the transposed index order
H^{ba} below equals H^{ab}. No Hessian identity or field equation is assumed.
This completes the fixed-inverse contraction v f g^{ab} delta Ric_ab only;
R83 separately contains delta inverse, volume, and scalar-factor terms.
No stationarity in P or complete physical source is claimed. -/
set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.HessianBoundaryR88
open Matrix Filter Topology Set ChatgptAudit.CurvedConnection
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci ChatgptAudit.MetricLieConnection
  ChatgptAudit.PalatiniBoundaryR85 ChatgptAudit.SymmetricBoundaryR87
  ChatgptAudit.RaisedBoundaryR88 ChatgptAudit.WeightedPalatiniR86
  ChatgptAudit.ConeVolume
noncomputable section

def scalarHessian (Gamma : ConnectionField4) (f : Coordinate4 → ℝ)
    (x : Coordinate4) (a b : Fin 4) : ℝ :=
  coordinatePartial (fun y => coordinatePartial f y b) x a -
    ∑ c : Fin 4, Gamma x a c b * coordinatePartial f x c

def hessianPair (Gamma : ConnectionField4) (f : Coordinate4 → ℝ)
    (H : TensorField4) (x : Coordinate4) : ℝ :=
  ∑ a : Fin 4, ∑ b : Fin 4, H x b a * scalarHessian Gamma f x a b

def correctionCurrent (q H : TensorField4) (tau f : Coordinate4 → ℝ) : VectorField4 :=
  fun x a => ∑ b : Fin 4, coordinatePartial f x b * (tau x * q x b a - H x b a)

theorem correction_differentiable (q H : TensorField4) (tau f : Coordinate4 → ℝ)
    (x : Coordinate4)
    (hq : ∀ i j, DifferentiableAt ℝ (fun y => q y i j) x)
    (hH : ∀ i j, DifferentiableAt ℝ (fun y => H y i j) x)
    (ht : DifferentiableAt ℝ tau x)
    (hdf : ∀ b, DifferentiableAt ℝ (fun y => coordinatePartial f y b) x) (a : Fin 4) :
    DifferentiableAt ℝ (fun y => correctionCurrent q H tau f y a) x := by
  unfold correctionCurrent
  exact DifferentiableAt.fun_sum fun b _ => (hdf b).mul ((ht.mul (hq b a)).sub (hH b a))

theorem correction_partial (q H : TensorField4) (tau f : Coordinate4 → ℝ)
    (x : Coordinate4)
    (hq : ∀ i j, DifferentiableAt ℝ (fun y => q y i j) x)
    (hH : ∀ i j, DifferentiableAt ℝ (fun y => H y i j) x)
    (ht : DifferentiableAt ℝ tau x)
    (hdf : ∀ b, DifferentiableAt ℝ (fun y => coordinatePartial f y b) x) (k a : Fin 4) :
    coordinatePartial (fun y => correctionCurrent q H tau f y a) x k =
      ∑ b : Fin 4,
        (coordinatePartial (fun y => coordinatePartial f y b) x k *
          (tau x * q x b a - H x b a) + coordinatePartial f x b *
          (coordinatePartial tau x k * q x b a + tau x * tensorFieldJet q x k b a -
           tensorFieldJet H x k b a)) := by
  unfold correctionCurrent
  rw [coordinatePartial_sum (fun b y => coordinatePartial f y b *
    (tau y*q y b a-H y b a)) x
    (fun b => (hdf b).mul ((ht.mul (hq b a)).sub (hH b a))) k]
  apply Finset.sum_congr rfl
  intro b hb
  rw [coordinatePartial_mul (fun y => coordinatePartial f y b)
    (fun y => tau y*q y b a-H y b a) x (hdf b) ((ht.mul (hq b a)).sub (hH b a)) k,
    coordinatePartial_sub (fun y => tau y*q y b a) (fun y => H y b a) x
      (ht.mul (hq b a)) (hH b a) k,
    coordinatePartial_mul tau (fun y => q y b a) x ht (hq b a) k]
  rfl

theorem correction_divergence (q H : TensorField4) (Gamma : ConnectionField4)
    (tau f : Coordinate4 → ℝ) (x : Coordinate4)
    (hq : ∀ i j, DifferentiableAt ℝ (fun y => q y i j) x)
    (hH : ∀ i j, DifferentiableAt ℝ (fun y => H y i j) x)
    (ht : DifferentiableAt ℝ tau x)
    (hdf : ∀ b, DifferentiableAt ℝ (fun y => coordinatePartial f y b) x)
    (hp : ∀ k, tensorFieldJet q x k = -Gamma x k * q x - q x * (Gamma x k)ᵀ) :
    vectorExpansion Gamma (correctionCurrent q H tau f) x =
      -hessianPair Gamma f H x + tau x * hessianPair Gamma f q x -
      ∑ b : Fin 4, coordinatePartial f x b *
        ((∑ a : Fin 4, contravariantTensorDerivative Gamma H x a b a) -
         ∑ a : Fin 4, q x b a * coordinatePartial tau x a) := by
  simp only [vectorExpansion, Matrix.trace, Matrix.diag_apply, covariantVectorGradient,
    covariantVectorDerivative, vectorPartial, Pi.add_apply,
    correction_partial q H tau f x hq hH ht hdf, hp,
    correctionCurrent, hessianPair, scalarHessian, contravariantTensorDerivative,
    Matrix.mulVec, dotProduct, Matrix.mul_apply, Matrix.sub_apply, Matrix.add_apply,
    Matrix.neg_apply, Matrix.transpose_apply, Fin.sum_univ_four]
  ring

theorem vectorExpansion_add (Gamma : ConnectionField4) (V W : VectorField4)
    (x : Coordinate4)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x)
    (hW : ∀ a, DifferentiableAt ℝ (fun y => W y a) x) :
    vectorExpansion Gamma (fun y a => V y a + W y a) x =
      vectorExpansion Gamma V x + vectorExpansion Gamma W x := by
  have hp (a : Fin 4) := coordinatePartial_add (fun y => V y a) (fun y => W y a)
    x (hV a) (hW a) a
  simp only [vectorExpansion, Matrix.trace, Matrix.diag_apply, covariantVectorGradient,
    covariantVectorDerivative, vectorPartial, Pi.add_apply, Matrix.mulVec, dotProduct,
    hp, Fin.sum_univ_four]
  ring

theorem actual_weighted_hessian_ricci_density
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hd : SmoothMatrixOn U h)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (hh : ∀ y∈U, (h y)ᵀ=h y)
    (hi : ∀ y∈U, IsUnit (g y)) (f : Coordinate4 → ℝ)
    (x : Coordinate4) (hx : x∈U) (hf : DifferentiableAt ℝ f x)
    (hdf : ∀ b, DifferentiableAt ℝ (fun y => coordinatePartial f y b) x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => metricConnectionVariation g h y j a b) x) :
    let q : TensorField4 := fun y => (g y)⁻¹
    let Gamma := leviCivitaField g q
    let H : TensorField4 := fun y => q y * h y * q y
    let tau : Coordinate4 → ℝ := fun y => Matrix.trace (q y * h y)
    let W := palatiniCurrent q (metricConnectionVariation g h)
    let K := correctionCurrent q H tau f
    let B : VectorField4 := fun y a => f y * W y a + K y a
    HasDerivAt (fun t => metricVolumeDensity (g x)*f x *
      (∑ b : Fin 4, ∑ j : Fin 4, q x b j * coordinateRicci (perturbedLeviCivita g h t) x b j))
      ((∑ a : Fin 4, coordinatePartial (fun y => metricVolumeDensity (g y)*B y a) x a) +
       metricVolumeDensity (g x) * (hessianPair Gamma f H x - tau x*hessianPair Gamma f q x)) 0 := by
  intro q Gamma H tau W K B
  have hq := smooth_matrix_differentiableAt U hU (fun y => (g y)⁻¹)
    (smooth_matrix_inverse U g hg hi) x hx
  have hhd := smooth_matrix_differentiableAt U hU h hd x hx
  have hqh := product_entry_differentiable q h x hq hhd
  have hH := product_entry_differentiable (fun y => q y*h y) q x hqh hq
  have ht : DifferentiableAt ℝ tau x := by
    change DifferentiableAt ℝ (fun y => ∑ i : Fin 4, (q y*h y) i i) x
    exact DifferentiableAt.fun_sum fun i _ => hqh i i
  have hp := actual_inverse_parallel U hU g hg hs hi x hx
  have hW : ∀ a, DifferentiableAt ℝ (fun y => W y a) x :=
    current_differentiable q _ x hq hC
  have hK : ∀ a, DifferentiableAt ℝ (fun y => K y a) x :=
    correction_differentiable q H tau f x hq hH ht hdf
  have hB : ∀ a, DifferentiableAt ℝ (fun y => B y a) x :=
    fun a => (hf.mul (hW a)).add (hK a)
  have hWvalue (a : Fin 4) : W x a =
      (∑ b : Fin 4, contravariantTensorDerivative Gamma H x b a b) -
      ∑ k : Fin 4, q x a k * coordinatePartial tau x k :=
    actual_palatini_current_divergence_trace U hU g h hg hd hs hh hi x hx a
  have hk := correction_divergence q H Gamma tau f x hq hH ht hdf hp
  simp_rw [← hWvalue] at hk
  have hv := volume_divergence_levi_civita U hU g hg hs hi B x hx hB
  have hb := vectorExpansion_add Gamma (fun y a => f y*W y a) K x
    (fun a => hf.mul (hW a)) hK
  rw [weighted_vector_divergence Gamma f W x hf hW] at hb
  have hh0 := (actual_metric_ricci_boundary_derivative U hU g h hg hd hs hi x hx hC).const_mul
    (metricVolumeDensity (g x)*f x)
  convert! hh0 using 1
  rw [hv, hb, hk]
  ring

#print axioms scalarHessian
#print axioms hessianPair
#print axioms correctionCurrent
#print axioms correction_differentiable
#print axioms correction_partial
#print axioms correction_divergence
#print axioms vectorExpansion_add
#print axioms actual_weighted_hessian_ricci_density
end
end ChatgptAudit.HessianBoundaryR88
