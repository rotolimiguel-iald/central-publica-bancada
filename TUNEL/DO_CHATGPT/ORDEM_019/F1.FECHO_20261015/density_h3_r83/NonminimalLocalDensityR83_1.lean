import TGLExt.ScalarMatterDensityVariation
import TGLExt.MetricEinsteinVariation

/-!
R83 sandbox: local first variation of sqrt(|det g_t|) (c0 + xi*u(t)) R(g_t).
The varied metric is covariant g_t = g + t*h; the inverse-metric quadratic
specialization therefore has the negative derivative -g^-1*h*g^-1. This is
different from directly varying an inverse metric in the R82 algebraic reading.
The independent scalar path may itself come from a probability path, but these
lemmas do not grant arbitrary variations of g(P) while P is held fixed.
No integrated action, boundary conditions, integration by parts, stationarity,
H3, physical realization, or global field equation is concluded here.
-/

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section

namespace ChatgptAudit.NonminimalDensityR83
open Matrix Filter Topology Set
  ChatgptAudit.Coherent023 ChatgptAudit.MetricVariation
  ChatgptAudit.MetricRicci ChatgptAudit.CurvedConnection
  ChatgptAudit.ConeVolume ChatgptAudit.ScalarMatterVariation
  ChatgptAudit.MetricEinsteinVariation

def baseScalar (g : TensorField4) (x : Coordinate4) : ℝ :=
  coordinateScalarCurvature (fun y => (g y)⁻¹)
    (leviCivitaField g (fun y => (g y)⁻¹)) x

def localDensity (g h : TensorField4) (x : Coordinate4)
    (c0 xi : ℝ) (u : ℝ → ℝ) (t : ℝ) : ℝ :=
  metricVolumeDensity (g x + t • h x) * (c0 + xi * u t) *
    coordinateScalarCurvature
      (perturbedMetricInverse g h t) (perturbedLeviCivita g h t) x

def densityDerivative (g h : TensorField4) (x : Coordinate4)
    (c0 xi u0 du : ℝ) : ℝ :=
  metricVolumeDensity (g x) / 2 * (h x * (g x)⁻¹).trace *
      (c0 + xi * u0) * baseScalar g x +
    metricVolumeDensity (g x) * xi * du * baseScalar g x +
    metricVolumeDensity (g x) * (c0 + xi * u0) * scalarMetricVariation g h x

theorem local_density_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U)
    (c0 xi : ℝ) (u : ℝ → ℝ) (du : ℝ) (hu : HasDerivAt u du 0) :
    HasDerivAt (localDensity g h x c0 xi u)
      (densityDerivative g h x c0 xi (u 0) du) 0 := by
  have Hv := metric_volume_first_variation (g x) (h x) (hi x hx)
  have Hu := (hu.const_mul xi).const_add c0
  have Hr := metric_scalar_first_variation U hU g h hg hh hi x hx
  unfold localDensity densityDerivative baseScalar
  convert! (Hv.mul Hu).mul Hr using 1
  simp only [zero_smul, add_zero, perturbed_levi_civita_at_zero,
    perturbedMetricInverse, metricPerturbation]
  ring

theorem constant_scalar_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U)
    (c0 xi u0 : ℝ) :
    HasDerivAt (localDensity g h x c0 xi (fun _ => u0))
      (metricVolumeDensity (g x) / 2 * (h x * (g x)⁻¹).trace *
        (c0 + xi * u0) * baseScalar g x +
       metricVolumeDensity (g x) * (c0 + xi * u0) * scalarMetricVariation g h x) 0 := by
  simpa only [densityDerivative, mul_zero, zero_mul, add_zero] using
    local_density_first_variation U hU g h hg hh hi x hx c0 xi
      (fun _ => u0) 0 (hasDerivAt_const (0 : ℝ) u0)

theorem covector_norm_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U)
    (c0 xi : ℝ) (w : Coordinate4) :
    HasDerivAt (localDensity g h x c0 xi
      (fun t => tensorQuad (g x + t • h x)⁻¹ w))
      (metricVolumeDensity (g x) / 2 * (h x * (g x)⁻¹).trace *
        (c0 + xi * tensorQuad (g x)⁻¹ w) * baseScalar g x -
       metricVolumeDensity (g x) * xi * tensorQuad ((g x)⁻¹ * h x * (g x)⁻¹) w *
         baseScalar g x +
       metricVolumeDensity (g x) * (c0 + xi * tensorQuad (g x)⁻¹ w) *
         scalarMetricVariation g h x) 0 := by
  convert! local_density_first_variation U hU g h hg hh hi x hx c0 xi
    (fun t => tensorQuad (g x + t • h x)⁻¹ w)
    (-tensorQuad ((g x)⁻¹ * h x * (g x)⁻¹) w)
    (quadratic_inverse_first_variation (g x) (h x) w (hi x hx)) using 1
  simp only [densityDerivative, zero_smul, add_zero]
  ring

theorem with_scalar_matter_first_variation {J : Type} [Fintype J]
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U)
    (c0 xi : ℝ) (u : ℝ → ℝ) (du : ℝ) (hu : HasDerivAt u du 0)
    (w : J → Coordinate4) (c : J → ℝ) :
    HasDerivAt (fun t => localDensity g h x c0 xi u t +
      scalarMatterDensity (g x + t • h x) w c)
      (densityDerivative g h x c0 xi (u 0) du +
       (-metricVolumeDensity (g x) / 2 *
         (((g x)⁻¹ * h x * (g x)⁻¹) * scalarMatterStress (g x) w c).trace)) 0 := by
  exact (local_density_first_variation U hU g h hg hh hi x hx c0 xi u du hu).add
    (scalar_matter_density_first_variation (g x) (h x) w c (hi x hx))

#print axioms baseScalar
#print axioms localDensity
#print axioms densityDerivative
#print axioms local_density_first_variation
#print axioms constant_scalar_first_variation
#print axioms covector_norm_first_variation
#print axioms with_scalar_matter_first_variation
end ChatgptAudit.NonminimalDensityR83
