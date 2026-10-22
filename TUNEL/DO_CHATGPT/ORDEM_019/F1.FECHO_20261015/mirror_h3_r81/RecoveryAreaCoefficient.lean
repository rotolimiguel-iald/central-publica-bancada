import TGLExt.UnitaryEntropyResponse

/-!
Candidate R81: expose the remaining second-order geometric coefficient.
Reuses the existing unitary entropy theorem. No universal H3, physical
recovery device, metric, source, or area coefficient is constructed here.
The area coefficient is an explicit hypothesis, not a definition of area
by entropy. This scalar bridge must still be instantiated with inducedArea
of the same geometric record, at every point and null direction.
-/
set_option autoImplicit false
namespace IALD.R81
open Filter Topology ChatgptAudit.Unitary022 ChatgptAudit.Micro021
  ChatgptAudit.Flow019 ChatgptAudit.Flow020

theorem unitary_area_matching_iff_coefficients
    (a b frequency u v eta areaCoefficient : ℝ) (area : ℝ → ℝ)
    (hs : u^2+v^2=1) (hu : 0<u) (hv : 0<v)
    (hArea : Tendsto (fun t => (area t-area 0)/t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 areaCoefficient)) :
    Tendsto (fun t => microscopicAreaError
      (unitaryStateCurve a b frequency u v hs) eta area t/t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 0) ↔
      unitaryResponse a b frequency u v = eta*areaCoefficient := by
  have hlim : Tendsto (fun t => microscopicAreaError
      (unitaryStateCurve a b frequency u v hs) eta area t/t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (unitaryResponse a b frequency u v-eta*areaCoefficient)) := by
    convert (unitary_entropy_quadratic_limit a b frequency u v hs hu hv).sub
      (hArea.const_mul eta) using 1 <;>
      simp only [microscopicAreaError, unitaryStateCurve] <;> congr 1 <;> funext t <;> ring
  constructor
  · intro hzero
    have he := tendsto_nhds_unique hlim hzero
    exact sub_eq_zero.mp he
  · intro he
    simpa only [he, sub_self] using hlim

#print axioms unitary_area_matching_iff_coefficients
end IALD.R81
