import PalatiniBoundaryR85_3
import TGLExt.ScalarMatterDensityVariation

/-!
R86: density transport of the actual curved Palatini current, with scalar weight f.
The volume partial is derived, not assumed: differentiability of sqrt|det| plus
the existing affine variation identifies its full differential, then metric
compatibility reduces the trace to the Levi-Civita connection trace.
The final derivative contracts Ricci against a FIXED inverse metric at t=0.
It is one component of delta(v f R), not the whole scalar-density variation.
The df.W bulk remainder is explicit. Its Hessian rewrite and W in terms of
raised h are not proved here. No stationarity, boundary data or H3 is asserted.
-/
set_option autoImplicit false
set_option maxHeartbeats 12000000
namespace ChatgptAudit.WeightedPalatiniR86
open Matrix Filter Topology Set ChatgptAudit.CurvedConnection
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci ChatgptAudit.MetricLieConnection
  ChatgptAudit.ScalarMatterVariation ChatgptAudit.ConeVolume
  ChatgptAudit.PalatiniBoundaryR85
noncomputable section
open scoped Matrix.Norms.Operator

theorem volume_differentiable (G : Tensor4) (hG : IsUnit G) :
    DifferentiableAt ℝ metricVolumeDensity G := by
  have hn : G.det ≠ 0 := (G.isUnit_iff_isUnit_det.mp hG).ne_zero
  have hd : DifferentiableAt ℝ (fun A : Tensor4 => A.det) G :=
    (determinantMultilinear.hasFDerivAt G).differentiableAt
  exact (hd.abs hn).sqrt (abs_ne_zero.mpr hn)

theorem volume_fderiv_apply (G H : Tensor4) (hG : IsUnit G) :
    fderiv ℝ metricVolumeDensity G H = metricVolumeDensity G/2*(H*G⁻¹).trace := by
  have hd := ((volume_differentiable G hG).hasFDerivAt).comp_hasDerivAt_of_eq
    (0:ℝ) (matrix_affine_derivative G H) (by simp)
  exact hd.unique (metric_volume_first_variation G H hG)

theorem field_fderiv_coordinate (g : TensorField4) (x : Coordinate4)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x) (k : Fin 4) :
    fderiv ℝ g x (Pi.single k 1) = tensorFieldJet g x k := by
  have hd : DifferentiableAt ℝ g x := differentiableAt_pi.mpr
    (fun a => differentiableAt_pi.mpr (hg a))
  ext a b
  change (fderiv ℝ g x (Pi.single k 1)) a b =
    fderiv ℝ (fun y => g y a b) x (Pi.single k 1)
  rw [fderiv_apply (differentiableAt_pi.mp hd a) b, fderiv_apply hd a]
  rfl

theorem volume_field_partial (g : TensorField4) (x : Coordinate4)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x)
    (hi : IsUnit (g x)) (k : Fin 4) :
    coordinatePartial (fun y => metricVolumeDensity (g y)) x k =
      metricVolumeDensity (g x)/2 * (tensorFieldJet g x k * (g x)⁻¹).trace := by
  have hd : DifferentiableAt ℝ g x := differentiableAt_pi.mpr
    (fun a => differentiableAt_pi.mpr (hg a))
  unfold coordinatePartial
  change (fderiv ℝ (metricVolumeDensity ∘ g) x) (Pi.single k 1) = _
  rw [fderiv_comp x (volume_differentiable (g x) hi) hd]
  change fderiv ℝ metricVolumeDensity (g x) (fderiv ℝ g x (Pi.single k 1)) = _
  rw [field_fderiv_coordinate g x hg k, volume_fderiv_apply (g x) _ hi]

theorem compatible_trace (G Q A D : Tensor4)
    (hl : Q*G=1) (hr : G*Q=1) (hc : D=Aᵀ*G+G*A) :
    (D*Q).trace = 2*A.trace := by
  rw [hc, Matrix.add_mul, Matrix.trace_add]
  have hfirst : (Aᵀ*G*Q).trace=A.trace := by
    rw [Matrix.mul_assoc, hr, mul_one, Matrix.trace_transpose]
  have hsecond : (G*A*Q).trace=A.trace := by
    rw [Matrix.trace_mul_cycle, hl, one_mul]
  rw [hfirst,hsecond]
  ring

theorem volume_partial_levi_civita
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4)
    (hg : SmoothMatrixOn U g) (hs : ∀ y∈U, (g y)ᵀ=g y)
    (hi : ∀ y∈U, IsUnit (g y)) (x : Coordinate4) (hx : x∈U) (k : Fin 4) :
    coordinatePartial (fun y => metricVolumeDensity (g y)) x k =
      metricVolumeDensity (g x) * (leviCivitaField g (fun y => (g y)⁻¹) x k).trace := by
  let Gamma := leviCivitaField g (fun y => (g y)⁻¹)
  have hm : MetricCompatibleOn U g Gamma := by
    intro y hy i
    exact levi_civita_field_metric_compatible U hU g (fun y => (g y)⁻¹) hs
      (fun y hy => actual_inverse_left (g y) (hi y hy))
      (fun y hy => actual_inverse_right (g y) (hi y hy)) y hy i
  rw [volume_field_partial g x (smooth_matrix_differentiableAt U hU g hg x hx) (hi x hx) k]
  rw [compatible_trace (g x) (g x)⁻¹ (Gamma x k) (tensorFieldJet g x k)
    (actual_inverse_left (g x) (hi x hx)) (actual_inverse_right (g x) (hi x hx))
    (metric_compatibility_formula U g Gamma hm x hx k)]
  dsimp [Gamma]
  ring

theorem volume_divergence_levi_civita
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4)
    (hg : SmoothMatrixOn U g) (hs : ∀ y∈U, (g y)ᵀ=g y)
    (hi : ∀ y∈U, IsUnit (g y)) (V : VectorField4) (x : Coordinate4) (hx : x∈U)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) :
    (∑ a : Fin 4, coordinatePartial (fun y => metricVolumeDensity (g y)*V y a) x a) =
      metricVolumeDensity (g x) * vectorExpansion
        (leviCivitaField g (fun y => (g y)⁻¹)) V x := by
  let Gamma := leviCivitaField g (fun y => (g y)⁻¹)
  have hdg : DifferentiableAt ℝ g x := differentiableAt_pi.mpr fun a =>
    differentiableAt_pi.mpr (smooth_matrix_differentiableAt U hU g hg x hx a)
  have hv : DifferentiableAt ℝ (fun y => metricVolumeDensity (g y)) x :=
    (volume_differentiable (g x) (hi x hx)).comp x hdg
  have ht : ∀ i j l, Gamma x i l j=Gamma x j l i :=
    levi_civita_field_torsion_free U hU g (fun y => (g y)⁻¹) hs x hx
  have htr (a : Fin 4) : (Gamma x a).trace = ∑ j : Fin 4, Gamma x j j a := by
    change (∑ j : Fin 4, Gamma x a j j)=_
    exact Finset.sum_congr rfl (fun j _ => ht a j j)
  have hprod (a : Fin 4) := coordinatePartial_mul
    (fun y => metricVolumeDensity (g y)) (fun y => V y a) x hv (hV a) a
  simp only [hprod, volume_partial_levi_civita U hU g hg hs hi x hx]
  change (∑ a : Fin 4, (metricVolumeDensity (g x)*(Gamma x a).trace*V x a +
    metricVolumeDensity (g x)*coordinatePartial (fun y => V y a) x a)) =
    metricVolumeDensity (g x)*vectorExpansion Gamma V x
  simp only [htr, vectorExpansion, Matrix.trace, Matrix.diag_apply, covariantVectorGradient,
    covariantVectorDerivative, vectorPartial, Pi.add_apply, Matrix.mulVec, dotProduct,
    Fin.sum_univ_four]
  ring

theorem weighted_vector_divergence (Gamma : ConnectionField4) (f : Coordinate4 → ℝ)
    (V : VectorField4) (x : Coordinate4) (hf : DifferentiableAt ℝ f x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) :
    vectorExpansion Gamma (fun y a => f y*V y a) x =
      f x*vectorExpansion Gamma V x + ∑ a : Fin 4, coordinatePartial f x a*V x a := by
  have hprod (a : Fin 4) := coordinatePartial_mul f (fun y => V y a) x hf (hV a) a
  simp only [vectorExpansion, Matrix.trace, Matrix.diag_apply, covariantVectorGradient,
    covariantVectorDerivative, vectorPartial, Pi.add_apply, Matrix.mulVec, dotProduct,
    hprod, Fin.sum_univ_four]
  ring

theorem current_differentiable (q : TensorField4) (C : ConnectionField4) (x : Coordinate4)
    (hq : ∀ b j, DifferentiableAt ℝ (fun y => q y b j) x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => C y j a b) x) (a : Fin 4) :
    DifferentiableAt ℝ (fun y => palatiniCurrent q C y a) x := by
  unfold palatiniCurrent
  exact DifferentiableAt.fun_sum fun b (_ : b∈(Finset.univ : Finset (Fin 4))) =>
    DifferentiableAt.fun_sum fun j (_ : j∈(Finset.univ : Finset (Fin 4))) =>
      ((hq b j).mul (hC j a b)).sub ((hq b a).mul (hC j j b))

theorem actual_weighted_ricci_density_derivative
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (hi : ∀ y∈U, IsUnit (g y))
    (f : Coordinate4 → ℝ) (x : Coordinate4) (hx : x∈U)
    (hf : DifferentiableAt ℝ f x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => metricConnectionVariation g h y j a b) x) :
    let W := palatiniCurrent (fun y => (g y)⁻¹) (metricConnectionVariation g h)
    HasDerivAt (fun t => metricVolumeDensity (g x)*f x *
      (∑ b : Fin 4, ∑ j : Fin 4, (g x)⁻¹ b j * coordinateRicci (perturbedLeviCivita g h t) x b j))
      ((∑ a : Fin 4, coordinatePartial
         (fun y => metricVolumeDensity (g y)*(f y*W y a)) x a) -
       metricVolumeDensity (g x)*(∑ a : Fin 4, coordinatePartial f x a*W x a)) 0 := by
  intro W
  have hW : ∀ a, DifferentiableAt ℝ (fun y => W y a) x :=
    current_differentiable _ _ x (smooth_matrix_differentiableAt U hU _
      (smooth_matrix_inverse U g hg hi) x hx) hC
  have hvol := volume_divergence_levi_civita U hU g hg hs hi
    (fun y a => f y*W y a) x hx (fun a => hf.mul (hW a))
  rw [weighted_vector_divergence _ f W x hf hW] at hvol
  have H := (actual_metric_ricci_boundary_derivative U hU g h hg hh hs hi x hx hC).const_mul
    (metricVolumeDensity (g x)*f x)
  convert! H using 1
  rw [hvol]
  ring

#print axioms volume_differentiable
#print axioms volume_fderiv_apply
#print axioms field_fderiv_coordinate
#print axioms volume_field_partial
#print axioms compatible_trace
#print axioms volume_partial_levi_civita
#print axioms volume_divergence_levi_civita
#print axioms weighted_vector_divergence
#print axioms current_differentiable
#print axioms actual_weighted_ricci_density_derivative
end
end ChatgptAudit.WeightedPalatiniR86
