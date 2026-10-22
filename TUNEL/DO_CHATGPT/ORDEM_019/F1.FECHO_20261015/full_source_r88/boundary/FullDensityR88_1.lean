import HessianBoundaryR88_2
import IntegratedDensityR84_1

/-! R88 full local variation of volume * F(t,x) * R(g+t h), with all
inverse-metric, volume, scalar-factor and Hessian boundary terms retained.
The integral corollary reuses R84 dominated differentiation, with its explicit
measure support, measurability, integrability and uniform Lipschitz hypotheses.
No stationarity, restriction of P variations, or complete physical source is inferred.
The boundary divergence is retained: no zero boundary flux is presumed. -/
set_option autoImplicit false
set_option maxHeartbeats 16000000
set_option maxRecDepth 3000
namespace ChatgptAudit.FullDensityR88
open Matrix Filter Topology Set MeasureTheory
  ChatgptAudit.CurvedConnection ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci
  ChatgptAudit.MetricEinsteinVariation ChatgptAudit.ConeVolume
  ChatgptAudit.NonminimalDensityR83 ChatgptAudit.IntegratedDensityR84
  ChatgptAudit.HessianBoundaryR88
noncomputable section

def fullBoundaryCurrent (g h : TensorField4) (f : Coordinate4 → ℝ) : VectorField4 :=
  let q : TensorField4 := fun y => (g y)⁻¹
  let H : TensorField4 := fun y => q y*h y*q y
  let tau : Coordinate4 → ℝ := fun y => Matrix.trace (q y*h y)
  let W := ChatgptAudit.PalatiniBoundaryR85.palatiniCurrent q (metricConnectionVariation g h)
  fun y a => f y*W y a + correctionCurrent q H tau f y a

def ricciBoundaryDerivative (g h : TensorField4) (f : Coordinate4 → ℝ)
    (x : Coordinate4) : ℝ :=
  let q : TensorField4 := fun y => (g y)⁻¹
  let Gamma := leviCivitaField g q
  let H : TensorField4 := fun y => q y*h y*q y
  (∑ a : Fin 4, coordinatePartial
    (fun y => metricVolumeDensity (g y)*fullBoundaryCurrent g h f y a) x a) +
  metricVolumeDensity (g x) * (hessianPair Gamma f H x -
    Matrix.trace (q x*h x)*hessianPair Gamma f q x)

def fullBoundaryDensityDerivative (g h : TensorField4)
    (F : ℝ → Coordinate4 → ℝ) (dF : Coordinate4 → ℝ) (x : Coordinate4) : ℝ :=
  metricVolumeDensity (g x)/2 * Matrix.trace (h x*(g x)⁻¹)*F 0 x*baseScalar g x +
  metricVolumeDensity (g x)*dF x*baseScalar g x -
  metricVolumeDensity (g x)*F 0 x *
    (∑ i : Fin 4, ∑ j : Fin 4, ((g x)⁻¹*h x*(g x)⁻¹) i j *
      coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) x i j) +
  ricciBoundaryDerivative g h (F 0) x

theorem scalar_variation_split (g h : TensorField4) (x : Coordinate4) :
    scalarMetricVariation g h x =
      -(∑ i : Fin 4, ∑ j : Fin 4, ((g x)⁻¹*h x*(g x)⁻¹) i j *
        coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) x i j) +
      (∑ i : Fin 4, ∑ j : Fin 4, (g x)⁻¹ i j *
        ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
          (metricConnectionVariation g h) x i j) := by
  simp only [scalarMetricVariation, neg_mul, Matrix.neg_apply, Fin.sum_univ_four]
  ring

theorem weighted_ricci_boundary_equation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hd : SmoothMatrixOn U h)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (hh : ∀ y∈U, (h y)ᵀ=h y)
    (hi : ∀ y∈U, IsUnit (g y)) (f : Coordinate4 → ℝ)
    (x : Coordinate4) (hx : x∈U) (hf : DifferentiableAt ℝ f x)
    (hdf : ∀ b, DifferentiableAt ℝ (fun y => coordinatePartial f y b) x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => metricConnectionVariation g h y j a b) x) :
    ricciBoundaryDerivative g h f x = metricVolumeDensity (g x)*f x *
      (∑ i : Fin 4, ∑ j : Fin 4, (g x)⁻¹ i j *
        ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
          (metricConnectionVariation g h) x i j) := by
  have hc := actual_weighted_hessian_ricci_density U hU g h hg hd hs hh hi f x hx hf hdf hC
  have hr := HasDerivAt.fun_sum fun i (_ : i∈(Finset.univ : Finset (Fin 4))) =>
    HasDerivAt.fun_sum fun j (_ : j∈(Finset.univ : Finset (Fin 4))) =>
      (metric_ricci_first_variation U hU g h hg hd hi x hx i j).const_mul ((g x)⁻¹ i j)
  exact hc.unique (hr.const_mul (metricVolumeDensity (g x)*f x))

theorem full_density_derivative_eq_boundary
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hd : SmoothMatrixOn U h)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (hh : ∀ y∈U, (h y)ᵀ=h y)
    (hi : ∀ y∈U, IsUnit (g y)) (F : ℝ → Coordinate4 → ℝ)
    (dF : Coordinate4 → ℝ) (x : Coordinate4) (hx : x∈U)
    (hf : DifferentiableAt ℝ (F 0) x)
    (hdf : ∀ b, DifferentiableAt ℝ (fun y => coordinatePartial (F 0) y b) x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => metricConnectionVariation g h y j a b) x) :
    densityDerivative g h x 0 1 (F 0 x) (dF x) = fullBoundaryDensityDerivative g h F dF x := by
  unfold densityDerivative fullBoundaryDensityDerivative
  rw [scalar_variation_split, weighted_ricci_boundary_equation U hU g h hg hd hs hh hi
    (F 0) x hx hf hdf hC]
  ring

theorem full_local_density_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hd : SmoothMatrixOn U h)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (hh : ∀ y∈U, (h y)ᵀ=h y)
    (hi : ∀ y∈U, IsUnit (g y)) (F : ℝ → Coordinate4 → ℝ)
    (dF : Coordinate4 → ℝ) (x : Coordinate4) (hx : x∈U)
    (hF : HasDerivAt (fun t => F t x) (dF x) 0)
    (hf : DifferentiableAt ℝ (F 0) x)
    (hdf : ∀ b, DifferentiableAt ℝ (fun y => coordinatePartial (F 0) y b) x)
    (hC : ∀ j a b, DifferentiableAt ℝ (fun y => metricConnectionVariation g h y j a b) x) :
    HasDerivAt (localDensity g h x 0 1 (fun t => F t x))
      (fullBoundaryDensityDerivative g h F dF x) 0 := by
  rw [← full_density_derivative_eq_boundary U hU g h hg hd hs hh hi F dF x hx hf hdf hC]
  exact local_density_first_variation U hU g h hg hd hi x hx 0 1 (fun t => F t x) (dF x) hF

theorem full_integrated_density_first_variation
    (mu : Measure Coordinate4) (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hd : SmoothMatrixOn U h)
    (hsym : ∀ y∈U, (g y)ᵀ=g y) (hhs : ∀ y∈U, (h y)ᵀ=h y)
    (hi : ∀ y∈U, IsUnit (g y)) (hmuU : ∀ᵐ x ∂mu, x∈U)
    (F : ℝ → Coordinate4 → ℝ) (dF : Coordinate4 → ℝ)
    (hF : ∀ x∈U, HasDerivAt (fun t => F t x) (dF x) 0)
    (hf : ∀ x∈U, DifferentiableAt ℝ (F 0) x)
    (hdf : ∀ x∈U, ∀ b, DifferentiableAt ℝ (fun y => coordinatePartial (F 0) y b) x)
    (hC : ∀ x∈U, ∀ j a b, DifferentiableAt ℝ (fun y => metricConnectionVariation g h y j a b) x)
    (s : Set ℝ) (hs : s∈𝓝 (0 : ℝ)) (bound : Coordinate4 → ℝ)
    (h_meas : ∀ᶠ t in 𝓝 (0 : ℝ), AEStronglyMeasurable (gravitationalDensity g h 0 1 F t) mu)
    (h_int : Integrable (gravitationalDensity g h 0 1 F 0) mu)
    (h_dmeas : AEStronglyMeasurable (gravitationalDerivative g h 0 1 F dF) mu)
    (h_lip : ∀ᵐ x ∂mu, LipschitzOnWith (Real.nnabs (bound x))
      (fun t => gravitationalDensity g h 0 1 F t x) s)
    (h_bound : Integrable bound mu) :
    Integrable (fullBoundaryDensityDerivative g h F dF) mu ∧
    HasDerivAt (fun t => ∫ x, gravitationalDensity g h 0 1 F t x ∂mu)
      (∫ x, fullBoundaryDensityDerivative g h F dF x ∂mu) 0 := by
  have old := integrated_gravitational_first_variation mu U hU g h hg hd hi hmuU
    0 1 F dF hF s hs bound h_meas h_int h_dmeas h_lip h_bound
  have he : gravitationalDerivative g h 0 1 F dF =ᵐ[mu] fullBoundaryDensityDerivative g h F dF :=
    hmuU.mono fun x hx => full_density_derivative_eq_boundary U hU g h hg hd hsym hhs hi
      F dF x hx (hf x hx) (hdf x hx) (hC x hx)
  refine ⟨old.1.congr he, ?_⟩
  simpa only [integral_congr_ae he] using old.2

#print axioms fullBoundaryCurrent
#print axioms ricciBoundaryDerivative
#print axioms fullBoundaryDensityDerivative
#print axioms scalar_variation_split
#print axioms weighted_ricci_boundary_equation
#print axioms full_density_derivative_eq_boundary
#print axioms full_local_density_first_variation
#print axioms full_integrated_density_first_variation
end
end ChatgptAudit.FullDensityR88
