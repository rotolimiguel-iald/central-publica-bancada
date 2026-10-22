import RecognitionReadout
import RecognitionInverse_v2

set_option autoImplicit false
namespace ORDEM016.D6
noncomputable section
open Set Topology TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Named remaining obligation for one independently specified physical pair.
It includes its own graph/resolvent/polar realization and dense spectral readout.
It contains no comparison with another pair and no U-intertwining conclusion. -/
def PairTomitaAnalyticRealizationMeasured
    (M : StarSubalgebra ℂ (H →L[ℂ] H)) (omega : H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (flow : ℝ → H ≃ₗᵢ[ℂ] H) : Prop :=
  ∃ A : ModularGraphRealization (closure (pairTomitaGraph M omega)),
    A.J=J ∧ ∀ t x, flow t (resolventDampingOperator A.R x)=resolventPhaseOperator A.R t x

/-- A proposed contract consumer, conditional on the two named realization obligations.
The two flows and antiunitaries are parameters fixed before recognition.
No new inhabitant of the physical ContratoH2 is constructed here. -/
theorem same_horizon_by_content_from_realizations
    {M N : StarSubalgebra ℂ (H →L[ℂ] H)} {omega omega' : H}
    (C : ReconhecimentoPeloConteudo M N omega omega')
    (J J' : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (flow flow' : ℝ → H ≃ₗᵢ[ℂ] H)
    (source : PairTomitaAnalyticRealizationMeasured M omega J flow)
    (target : PairTomitaAnalyticRealizationMeasured N omega' J' flow') :
    (∀ x, C.U (J (C.U.symm x))=J' x) ∧
    (∀ t x, C.U (flow t (C.U.symm x))=flow' t x) := by
  obtain ⟨A,hJ,hF⟩ := source
  obtain ⟨B,hJ',hF'⟩ := target
  let F : ModularReadout A := ⟨flow,hF⟩
  let F' : ModularReadout B := ⟨flow',hF'⟩
  have h := same_horizon_by_content_readout C A B F F'
  change (∀ x, C.U (A.J (C.U.symm x))=B.J x) ∧
    (∀ t x, C.U (flow t (C.U.symm x))=flow' t x) at h
  simpa only [hJ,hJ'] using h

#print axioms PairTomitaAnalyticRealizationMeasured
#print axioms same_horizon_by_content_from_realizations
end
end ORDEM016.D6
