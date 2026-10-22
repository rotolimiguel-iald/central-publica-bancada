import ExponentialTomitaR2

/-! Non-vacuous standard real subspace from the constructed exponential
involution. Its equality with the real standard subspace of the actual
Weyl algebra-vacuum pair remains a separate graph-identification obligation. -/
set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section
namespace F1Fecho.ExponentialTomita
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.ExponentialLift F1Rede.CanonicalWedge
open ChatgptAudit.Continuous049 AuditF13v31

def Kexp : StandardSubspace F :=
  closedAntilinearStandardSubspace canonicalLift.domain Sexp
    Sexp_closed Sexp_maps_domain Sexp_involutive Sexp_dense

theorem Kexp_mem (v : F) : v ∈ Kexp.toClosedSubmodule ↔
    ∃ hv : v ∈ canonicalLift.domain, Sexp ⟨v,hv⟩ = v := Iff.rfl

theorem vacuum_mem_domain : vacuum ∈ canonicalLift.domain := by
  have h := exponential_mem_domain TW (0 : TW.domain)
  simpa only [Subtype.coe_zero,exponential_zero] using h

theorem Sexp_vacuum : Sexp ⟨vacuum,vacuum_mem_domain⟩ = vacuum := by
  have h := Sexp_exponential (0 : TW.domain)
  simpa only [Subtype.coe_zero,map_zero,exponential_zero] using h

theorem vacuum_mem_Kexp : vacuum ∈ Kexp.toClosedSubmodule :=
  (Kexp_mem vacuum).mpr ⟨vacuum_mem_domain,Sexp_vacuum⟩

theorem Kexp_nonzero : ∃ v : F, v ∈ Kexp.toClosedSubmodule ∧ v ≠ 0 := by
  refine ⟨vacuum,vacuum_mem_Kexp,?_⟩
  intro h
  have hn := vacuum_norm
  rw [h,norm_zero] at hn
  norm_num at hn

theorem exponential_KWR_mem_Kexp (f : H1) (hf : f ∈ KWR.toClosedSubmodule) :
    exponential f ∈ Kexp.toClosedSubmodule := by
  obtain ⟨hd,hs⟩ := (KWR_mem f).mp hf
  apply (Kexp_mem (exponential f)).mpr
  refine ⟨exponential_mem_domain TW ⟨f,hd⟩,?_⟩
  exact (Sexp_exponential ⟨f,hd⟩).trans (congrArg exponential hs)

end F1Fecho.ExponentialTomita
#print axioms F1Fecho.ExponentialTomita.Kexp
#print axioms F1Fecho.ExponentialTomita.Sexp_vacuum
#print axioms F1Fecho.ExponentialTomita.vacuum_mem_Kexp
#print axioms F1Fecho.ExponentialTomita.Kexp_nonzero
#print axioms F1Fecho.ExponentialTomita.exponential_KWR_mem_Kexp
