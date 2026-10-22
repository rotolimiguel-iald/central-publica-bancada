import NonminimalLocalDensityR83_2
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.MeasureTheory.Integral.DivergenceTheorem

/-!
R84 candidate: dominated differentiation of the actual local R83 density.
The measure may be restricted to a chart/domain; its support in U, measurability,
integrability and a spatially integrable UNIFORM local Lipschitz bound are named.
No Euler-Lagrange equality or stationarity is assumed or concluded.
The separate box theorem supplies a divergence/face-flux rule, not the missing
identification of the curvature variation with a specific boundary current.
The subtraction of kernel scalarMatterDensity is an explicit sign choice giving
the positive stress-variation contribution with that kernel's definition of T.
It is not a universal physical convention. R83's addition remains valid.
Nothing here grants independent metric variations for g(P) at fixed P.
-/

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace ChatgptAudit.IntegratedDensityR84
open Matrix Filter Topology Set MeasureTheory
  ChatgptAudit.Coherent023 ChatgptAudit.MetricVariation
  ChatgptAudit.ConeVolume ChatgptAudit.ScalarMatterVariation
  ChatgptAudit.NonminimalDensityR83
open scoped Topology

def gravitationalDensity (g h : TensorField4) (c0 xi : ℝ)
    (u : ℝ → Coordinate4 → ℝ) (t : ℝ) (x : Coordinate4) : ℝ :=
  localDensity g h x c0 xi (fun s => u s x) t

def gravitationalDerivative (g h : TensorField4) (c0 xi : ℝ)
    (u : ℝ → Coordinate4 → ℝ) (du : Coordinate4 → ℝ) (x : Coordinate4) : ℝ :=
  densityDerivative g h x c0 xi (u 0 x) (du x)

theorem integrated_gravitational_first_variation
    (μ : Measure Coordinate4) (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (hμU : ∀ᵐ x ∂μ, x ∈ U)
    (c0 xi : ℝ) (u : ℝ → Coordinate4 → ℝ) (du : Coordinate4 → ℝ)
    (hu : ∀ x ∈ U, HasDerivAt (fun t => u t x) (du x) 0)
    (s : Set ℝ) (hs : s ∈ 𝓝 (0 : ℝ)) (bound : Coordinate4 → ℝ)
    (h_meas : ∀ᶠ t in 𝓝 (0 : ℝ), AEStronglyMeasurable (gravitationalDensity g h c0 xi u t) μ)
    (h_int : Integrable (gravitationalDensity g h c0 xi u 0) μ)
    (h_dmeas : AEStronglyMeasurable (gravitationalDerivative g h c0 xi u du) μ)
    (h_lip : ∀ᵐ x ∂μ, LipschitzOnWith (Real.nnabs (bound x))
      (fun t => gravitationalDensity g h c0 xi u t x) s)
    (h_bound : Integrable bound μ) :
    Integrable (gravitationalDerivative g h c0 xi u du) μ ∧
    HasDerivAt (fun t => ∫ x, gravitationalDensity g h c0 xi u t x ∂μ)
      (∫ x, gravitationalDerivative g h c0 xi u du x ∂μ) 0 := by
  apply hasDerivAt_integral_of_dominated_loc_of_lip hs h_meas h_int h_dmeas h_lip h_bound
  exact hμU.mono fun x hx =>
    local_density_first_variation U hU g h hg hh hi x hx c0 xi
      (fun t => u t x) (du x) (hu x hx)

def subtractedMatterDensity {J : Type} [Fintype J]
    (g h : TensorField4) (c0 xi : ℝ) (u : ℝ → Coordinate4 → ℝ)
    (w : Coordinate4 → J → Coordinate4) (c : J → ℝ) (t : ℝ) (x : Coordinate4) : ℝ :=
  gravitationalDensity g h c0 xi u t x - scalarMatterDensity (g x + t • h x) (w x) c

def subtractedMatterDerivative {J : Type} [Fintype J]
    (g h : TensorField4) (c0 xi : ℝ) (u : ℝ → Coordinate4 → ℝ)
    (du : Coordinate4 → ℝ) (w : Coordinate4 → J → Coordinate4) (c : J → ℝ)
    (x : Coordinate4) : ℝ :=
  gravitationalDerivative g h c0 xi u du x + metricVolumeDensity (g x) / 2 *
    (((g x)⁻¹ * h x * (g x)⁻¹) * scalarMatterStress (g x) (w x) c).trace

theorem subtracted_matter_local_first_variation {J : Type} [Fintype J]
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U)
    (c0 xi : ℝ) (u : ℝ → Coordinate4 → ℝ) (du : Coordinate4 → ℝ)
    (hu : HasDerivAt (fun t => u t x) (du x) 0)
    (w : Coordinate4 → J → Coordinate4) (c : J → ℝ) :
    HasDerivAt (fun t => subtractedMatterDensity g h c0 xi u w c t x)
      (subtractedMatterDerivative g h c0 xi u du w c x) 0 := by
  unfold subtractedMatterDensity subtractedMatterDerivative gravitationalDensity gravitationalDerivative
  convert! (local_density_first_variation U hU g h hg hh hi x hx c0 xi
    (fun t => u t x) (du x) hu).sub
    (scalar_matter_density_first_variation (g x) (h x) (w x) c (hi x hx)) using 1
  ring

theorem integrated_subtracted_matter_first_variation {J : Type} [Fintype J]
    (μ : Measure Coordinate4) (U : Set Coordinate4) (hU : IsOpen U)
    (g h : TensorField4) (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (hμU : ∀ᵐ x ∂μ, x ∈ U)
    (c0 xi : ℝ) (u : ℝ → Coordinate4 → ℝ) (du : Coordinate4 → ℝ)
    (hu : ∀ x ∈ U, HasDerivAt (fun t => u t x) (du x) 0)
    (w : Coordinate4 → J → Coordinate4) (c : J → ℝ)
    (s : Set ℝ) (hs : s ∈ 𝓝 (0 : ℝ)) (bound : Coordinate4 → ℝ)
    (h_meas : ∀ᶠ t in 𝓝 (0 : ℝ), AEStronglyMeasurable (subtractedMatterDensity g h c0 xi u w c t) μ)
    (h_int : Integrable (subtractedMatterDensity g h c0 xi u w c 0) μ)
    (h_dmeas : AEStronglyMeasurable (subtractedMatterDerivative g h c0 xi u du w c) μ)
    (h_lip : ∀ᵐ x ∂μ, LipschitzOnWith (Real.nnabs (bound x))
      (fun t => subtractedMatterDensity g h c0 xi u w c t x) s)
    (h_bound : Integrable bound μ) :
    Integrable (subtractedMatterDerivative g h c0 xi u du w c) μ ∧
    HasDerivAt (fun t => ∫ x, subtractedMatterDensity g h c0 xi u w c t x ∂μ)
      (∫ x, subtractedMatterDerivative g h c0 xi u du w c x ∂μ) 0 := by
  apply hasDerivAt_integral_of_dominated_loc_of_lip hs h_meas h_int h_dmeas h_lip h_bound
  exact hμU.mono fun x hx =>
    subtracted_matter_local_first_variation U hU g h hg hh hi x hx c0 xi u du (hu x hx) w c

def boxDivergence (V' : Coordinate4 → Coordinate4 →L[ℝ] Coordinate4) (x : Coordinate4) : ℝ :=
  ∑ i : Fin 4, V' x (Pi.single i 1) i

def boxFlux (a b : Coordinate4) (V : Coordinate4 → Coordinate4) : ℝ :=
  ∑ i : Fin 4,
    ((∫ y in Icc (a ∘ i.succAbove) (b ∘ i.succAbove), V (i.insertNth (b i) y) i) -
      ∫ y in Icc (a ∘ i.succAbove) (b ∘ i.succAbove), V (i.insertNth (a i) y) i)

theorem four_dimensional_divergence_flux (a b : Coordinate4) (hab : a ≤ b)
    (V : Coordinate4 → Coordinate4) (V' : Coordinate4 → Coordinate4 →L[ℝ] Coordinate4)
    (hcont : ContinuousOn V (Icc a b))
    (hderiv : ∀ x ∈ Set.pi Set.univ (fun i => Ioo (a i) (b i)), HasFDerivAt V (V' x) x)
    (hint : IntegrableOn (boxDivergence V') (Icc a b)) :
    (∫ x in Icc a b, boxDivergence V' x) = boxFlux a b V := by
  exact integral_divergence_of_hasFDerivAt_off_countable a b hab V V' ∅ countable_empty
    hcont (fun x hx => hderiv x hx.1) hint

theorem four_dimensional_divergence_zero_of_face_data (a b : Coordinate4) (hab : a ≤ b)
    (V : Coordinate4 → Coordinate4) (V' : Coordinate4 → Coordinate4 →L[ℝ] Coordinate4)
    (hcont : ContinuousOn V (Icc a b))
    (hderiv : ∀ x ∈ Set.pi Set.univ (fun i => Ioo (a i) (b i)), HasFDerivAt V (V' x) x)
    (hint : IntegrableOn (boxDivergence V') (Icc a b))
    (hfront : ∀ (i : Fin 4) (y : Fin 3 → ℝ),
      y ∈ Icc (a ∘ i.succAbove) (b ∘ i.succAbove) → V (i.insertNth (b i) y) i = 0)
    (hback : ∀ (i : Fin 4) (y : Fin 3 → ℝ),
      y ∈ Icc (a ∘ i.succAbove) (b ∘ i.succAbove) → V (i.insertNth (a i) y) i = 0) :
    (∫ x in Icc a b, boxDivergence V' x) = 0 := by
  rw [four_dimensional_divergence_flux a b hab V V' hcont hderiv hint]
  unfold boxFlux
  apply Finset.sum_eq_zero
  intro i _
  have hf : (∫ y in Icc (a ∘ i.succAbove) (b ∘ i.succAbove), V (i.insertNth (b i) y) i) = 0 := by
    calc
      _ = ∫ _y in Icc (a ∘ i.succAbove) (b ∘ i.succAbove), (0 : ℝ) :=
        setIntegral_congr_fun measurableSet_Icc (hfront i)
      _ = 0 := integral_zero _ _
  have hb : (∫ y in Icc (a ∘ i.succAbove) (b ∘ i.succAbove), V (i.insertNth (a i) y) i) = 0 := by
    calc
      _ = ∫ _y in Icc (a ∘ i.succAbove) (b ∘ i.succAbove), (0 : ℝ) :=
        setIntegral_congr_fun measurableSet_Icc (hback i)
      _ = 0 := integral_zero _ _
  rw [hf, hb, sub_self]

#print axioms gravitationalDensity
#print axioms gravitationalDerivative
#print axioms integrated_gravitational_first_variation
#print axioms subtractedMatterDensity
#print axioms subtractedMatterDerivative
#print axioms subtracted_matter_local_first_variation
#print axioms integrated_subtracted_matter_first_variation
#print axioms boxDivergence
#print axioms boxFlux
#print axioms four_dimensional_divergence_flux
#print axioms four_dimensional_divergence_zero_of_face_data
end ChatgptAudit.IntegratedDensityR84
