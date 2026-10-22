import RecognitionReadout
import TGLExt.V351ScalarTomitaImaginaryPowers

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ORDEM016.D6
noncomputable section
open Set Topology TGLExt TGLV350.Regular ChatgptAudit.Continuous049

variable (P : SiteProfile)

/-- Identify our adjoint-pairing relation with the existing maximal composition.
This is the scalar GNS construction, not a photon-net identification. -/
theorem scalar_square_relation :
    antilinearSquareGraph (closure (scalarTomitaGraph P)) = (scalarTomitaSquare P).graph := by
  ext p
  constructor
  · rintro ⟨sx,hsx,hpair⟩
    let x : scalarClosedTomitaDomain P := ⟨p.1,⟨sx,hsx⟩⟩
    have hval : scalarClosedTomita P x=sx :=
      scalarTomitaGraph_closure_single_valued P p.1 _ _ (scalarClosedTomita_graph x) hsx
    obtain ⟨ha,hav⟩ := scalarTomitaAdjoint_maximal P (y := scalarClosedTomita P x) (z := p.2)
      (fun y => by
        rw [hval]
        exact (hpair y (scalarClosedTomita P y) (scalarClosedTomita_graph y)).symm)
    let q : scalarTomitaSquareDomain P := ⟨p.1,⟨x.property,ha⟩⟩
    apply (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mpr
    refine ⟨q,rfl,?_⟩
    exact hav
  · intro hp
    obtain ⟨q,hx,hz⟩ := (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mp hp
    refine ⟨scalarClosedTomita P (scalarTomitaSquareInput P q),?_,?_⟩
    · simpa only [scalarTomitaSquareInput_coe,hx] using scalarClosedTomita_graph (scalarTomitaSquareInput P q)
    · intro y sy hy
      rw [← scalarClosedTomita_graph_eq P] at hy
      obtain ⟨t,ht⟩ := hy
      have hty := congrArg Prod.fst ht
      have hts := congrArg Prod.snd ht
      rw [← hty,← hts,← hz]
      exact scalarTomitaSquare_pairing P q t

theorem scalar_resolvent_in_relation (z : ScalarGNSHilbert P) :
    (scalarTomitaResolvent P z,z-scalarTomitaResolvent P z) ∈
      antilinearSquareGraph (closure (scalarTomitaGraph P)) := by
  rw [scalar_square_relation]
  obtain ⟨q,hq,he⟩ := scalarTomitaResolvent_equation P z
  apply (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mpr
  refine ⟨q,hq,?_⟩
  rw [hq] at he
  exact eq_sub_of_add_eq' he

theorem scalar_resolvent_inverse_relation (x y : ScalarGNSHilbert P)
    (h : (x,y) ∈ antilinearSquareGraph (closure (scalarTomitaGraph P))) :
    scalarTomitaResolvent P (x+y)=x := by
  rw [scalar_square_relation] at h
  obtain ⟨q,hx,hy⟩ := (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mp h
  rw [← hx,← hy]
  exact scalarTomitaResolvent_inverse P q

theorem sqrt_damping_factorization {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (R : H →L[ℂ] H) (hR : 0 ≤ R) (h1 : R ≤ 1) :
    CFC.sqrt (resolventDampingOperator R)=CFC.sqrt R*CFC.sqrt (1-R) := by
  have hc := resolvent_sqrt_pair_commute R
  apply CFC.sqrt_unique
  · calc
      _ = CFC.sqrt R * (CFC.sqrt (1-R) * CFC.sqrt R) * CFC.sqrt (1-R) := by simp only [mul_assoc]
      _ = CFC.sqrt R * (CFC.sqrt R * CFC.sqrt (1-R)) * CFC.sqrt (1-R) := by rw [← hc]
      _ = (CFC.sqrt R * CFC.sqrt R) * (CFC.sqrt (1-R) * CFC.sqrt (1-R)) := by simp only [mul_assoc]
      _ = resolventDampingOperator R := by
        rw [CFC.sqrt_mul_sqrt_self R hR,CFC.sqrt_mul_sqrt_self (1-R) (sub_nonneg.mpr h1)]
        rfl
  · exact Commute.mul_nonneg (CFC.sqrt_nonneg R) (CFC.sqrt_nonneg (1-R)) hc

theorem scalar_polar_regularized (z : ScalarGNSHilbert P) :
    (scalarTomitaResolvent P z,
      scalarTomitaPolarFactor P (CFC.sqrt (resolventDampingOperator (scalarTomitaResolvent P)) z)) ∈
      closure (scalarTomitaGraph P) := by
  let R := scalarTomitaResolvent P
  have hroot : (R z,CFC.sqrt (resolventDampingOperator R) z) ∈ (scalarTomitaPositiveRoot P).graph := by
    apply (bounded_graph_param_iff (CFC.sqrt R) (CFC.sqrt (1-R))
      (positive_sqrt_injective R (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_injective P)) _ _).mpr
    refine ⟨CFC.sqrt R z,?_,?_⟩
    · exact congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => T z)
        (CFC.sqrt_mul_sqrt_self R (scalarTomitaResolvent_nonneg P))
    · have he := sqrt_damping_factorization R (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
      rw [resolvent_sqrt_pair_commute R] at he
      exact (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => T z) he).symm
  obtain ⟨u,hu,hv⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mp hroot
  have hs := scalarClosedTomita_graph (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) u)
  have hf := scalarTomitaPolarFactor_root P u
  change scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P u)=
    scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) u) at hf
  rw [← hf] at hs
  change ((u : ScalarGNSHilbert P),scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P u)) ∈ _ at hs
  simpa only [hu,hv] using hs

/-- A concrete analytic realization already present in the scalar GNS tower.
It does not identify this graph with the physical photon wedge graph. -/
def scalarGraphRealization : ModularGraphRealization (closure (scalarTomitaGraph P)) where
  R := scalarTomitaResolvent P
  nonneg := scalarTomitaResolvent_nonneg P
  le_one := scalarTomitaResolvent_le_one P
  injective := scalarTomitaResolvent_injective P
  complement_injective := scalarTomitaResolvent_complement_injective P
  resolvent_mem := scalar_resolvent_in_relation P
  resolvent_inverse := scalar_resolvent_inverse_relation P
  graph_functional := scalarTomitaGraph_closure_single_valued P
  J := scalarTomitaPolarFactor P
  polar_regularized := scalar_polar_regularized P

def scalarGraphReadout : ModularReadout (scalarGraphRealization P) where
  flow := scalarTomitaImaginaryPower P
  spectral_readout := scalarTomitaImaginaryPower_damping P

#print axioms scalar_square_relation
#print axioms scalar_resolvent_in_relation
#print axioms scalar_resolvent_inverse_relation
#print axioms sqrt_damping_factorization
#print axioms scalar_polar_regularized
#print axioms scalarGraphRealization
#print axioms scalarGraphReadout
end
end ORDEM016.D6
