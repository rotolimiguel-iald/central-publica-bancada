import TGLExt.FLRWGeometry

set_option autoImplicit false
set_option maxHeartbeats 2400000

/-! Order 012 B2: components and conservation for the same metric construction. -/
namespace ChatgptAudit.FLRW
open Matrix TGLExt ChatgptAudit.GeneralMetric
open scoped ContDiff
noncomputable section

theorem flrw_einstein_tensor (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) :
    geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x =
      Matrix.diagonal ![3*(flrwHubble a (x 0))^2,
        -(2*a (x 0)*deriv (deriv a) (x 0)+(deriv a (x 0))^2),
        -(2*a (x 0)*deriv (deriv a) (x 0)+(deriv a (x 0))^2),
        -(2*a (x 0)*deriv (deriv a) (x 0)+(deriv a (x 0))^2)] := by
  have hz := (hpos x hx).ne'
  unfold geometricEinsteinTensor coordinateScalarCurvature
  rw [flrw_ricci U hU a ha hpos x hx, flrw_metric_inverse a x hz]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [flrwInverse, flrwMetric, flrwHubble, Matrix.diagonal, Fin.sum_univ_four] <;>
    field_simp <;> ring

theorem flrw_einstein_00 (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) :
    geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x 0 0 =
      3*(flrwHubble a (x 0))^2 := by
  simp [flrw_einstein_tensor U hU a ha hpos x hx]

theorem flrw_einstein_spatial (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) (hi : i ≠ 0) :
    geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x i i =
      -(2*a (x 0)*deriv (deriv a) (x 0)+(deriv a (x 0))^2) := by
  rw [flrw_einstein_tensor U hU a ha hpos x hx]
  fin_cases i <;> simp_all

theorem flrw_null_ricci (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) (k : SpacetimeVector)
    (hk : tensorQuad (flrwMetric a x) k = 0) :
    tensorQuad (coordinateRicci
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x) k =
      2*((flrwHubble a (x 0))^2-deriv (deriv a) (x 0)/a (x 0))*(k 0)^2 := by
  have hz := (hpos x hx).ne'
  have hn : (k 0)^2 = (a (x 0))^2*((k 1)^2+(k 2)^2+(k 3)^2) := by
    simp [tensorQuad, flrwMetric, dotProduct, Matrix.mulVec, Fin.sum_univ_four,
      Matrix.diagonal] at hk
    nlinarith [hk]
  rw [flrw_ricci U hU a ha hpos x hx]
  simp only [tensorQuad, dotProduct, Matrix.mulVec, Fin.sum_univ_four]
  simp [Matrix.diagonal]
  calc
    _ = (-3*deriv (deriv a) (x 0)/a (x 0))*(k 0)^2 +
        (a (x 0)*deriv (deriv a) (x 0)+2*(deriv a (x 0))^2)*
          ((k 1)^2+(k 2)^2+(k 3)^2) := by ring
    _ = _ := by rw [hn]; unfold flrwHubble; field_simp; ring

def flrwStress (a rho pressure : ℝ → ℝ) : TensorField4 := fun x =>
  Matrix.diagonal ![rho (x 0), pressure (x 0)*(a (x 0))^2,
    pressure (x 0)*(a (x 0))^2, pressure (x 0)*(a (x 0))^2]

theorem flrw_stress_symmetric (a rho pressure : ℝ → ℝ) (x : Coordinate4) :
    (flrwStress a rho pressure x)ᵀ = flrwStress a rho pressure x := by
  simp [flrwStress]

theorem flrw_stress_differentiable (U : Set Coordinate4) (a rho pressure : ℝ → ℝ)
    (ha : ∀ x∈U, DifferentiableAt ℝ a (x 0))
    (hr : ∀ x∈U, DifferentiableAt ℝ rho (x 0))
    (hp : ∀ x∈U, DifferentiableAt ℝ pressure (x 0)) :
    ∀ i j, DifferentiableOn ℝ (fun x => flrwStress a rho pressure x i j) U := by
  intro i j x hx
  have ht : DifferentiableAt ℝ (fun y : Coordinate4 => y 0) x := by fun_prop
  have hd : DifferentiableAt ℝ (fun y : Coordinate4 => pressure (y 0)*(a (y 0))^2) x :=
    ((hp x hx).comp x ht).mul (((ha x hx).comp x ht).pow 2)
  have hdr := (hr x hx).comp x ht
  fin_cases i <;> fin_cases j <;> dsimp [flrwStress, Matrix.diagonal] <;>
    first | fun_prop | exact hd.differentiableWithinAt |
      exact hdr.differentiableWithinAt

theorem flrw_stress_jet (a rho pressure : ℝ → ℝ) (x : Coordinate4)
    (ha : DifferentiableAt ℝ a (x 0)) (hr : DifferentiableAt ℝ rho (x 0))
    (hp : DifferentiableAt ℝ pressure (x 0)) (i : Fin 4) :
    tensorFieldJet (flrwStress a rho pressure) x i = if i = 0 then
      Matrix.diagonal ![deriv rho (x 0),
        deriv pressure (x 0)*(a (x 0))^2 + pressure (x 0)*(2*a (x 0)*deriv a (x 0)),
        deriv pressure (x 0)*(a (x 0))^2 + pressure (x 0)*(2*a (x 0)*deriv a (x 0)),
        deriv pressure (x 0)*(a (x 0))^2 + pressure (x 0)*(2*a (x 0)*deriv a (x 0))]
      else 0 := by
  have hd : HasDerivAt (fun t => pressure t*(a t)^2)
      (deriv pressure (x 0)*(a (x 0))^2 + pressure (x 0)*(2*a (x 0)*deriv a (x 0)))
      (x 0) := by
    simpa [mul_assoc] using! hp.hasDerivAt.mul (ha.hasDerivAt.pow 2)
  have hs (j : Fin 4) := coordinatePartial_time_function _ _ x hd j
  have hrt (j : Fin 4) := coordinatePartial_time_function _ _ x hr.hasDerivAt j
  have hc (c : ℝ) (j : Fin 4) : coordinatePartial (fun _ => c) x j = 0 := by
    simp [coordinatePartial]
  by_cases hi : i = 0 <;> ext j k <;> fin_cases j <;> fin_cases k <;>
    simp [tensorFieldJet, flrwStress, Matrix.diagonal, hs, hrt, hc, hi]

theorem flrw_stress_divergence (a rho pressure : ℝ → ℝ) (x : Coordinate4)
    (hz : a (x 0) ≠ 0) (ha : DifferentiableAt ℝ a (x 0))
    (hr : DifferentiableAt ℝ rho (x 0)) (hp : DifferentiableAt ℝ pressure (x 0)) :
    tensorFieldDivergence (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
      (flrwStress a rho pressure) x =
      ![deriv rho (x 0)+3*flrwHubble a (x 0)*(rho (x 0)+pressure (x 0)),0,0,0] := by
  funext j
  fin_cases j <;>
    simp [tensorFieldDivergence, tensorJetDivergence, covariantTensorJet,
      flrw_metric_inverse a x hz, flrw_connection a x hz ha, flrw_stress_jet a rho pressure x ha hr hp,
      flrwStress, flrwInverse, flrwConnection, flrwConnectionForm, flrwHubble,
      Matrix.mul_apply, Fin.sum_univ_four, Matrix.diagonal, Matrix.vecHead, Matrix.vecTail] <;>
    field_simp <;> ring

theorem flrw_continuity (a rho pressure : ℝ → ℝ) (x : Coordinate4)
    (hz : a (x 0) ≠ 0) (ha : DifferentiableAt ℝ a (x 0))
    (hr : DifferentiableAt ℝ rho (x 0)) (hp : DifferentiableAt ℝ pressure (x 0))
    (hdiv : tensorFieldDivergence (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
      (flrwStress a rho pressure) x 0 = 0) :
    deriv rho (x 0)+3*flrwHubble a (x 0)*(rho (x 0)+pressure (x 0)) = 0 := by
  simpa [flrw_stress_divergence a rho pressure x hz ha hr hp] using hdiv

end
end ChatgptAudit.FLRW
