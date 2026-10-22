import WeylSegalGeneratorR3

/-! The constructed exponential domain is invariant under every field Weyl
operator. The actual real derivative there equals i sqrt(2) times Segal.
This identifies a densely defined generator restriction; maximality and
essential self-adjointness are not conclusions of this module. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.Creation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential F1Fecho.Annihilation

theorem Weyl_preserves_domain (f : H1) (x : domain) :
    FieldWeyl.W f (x:F) ∈ domain := by
  classical
  obtain ⟨c,hc⟩ := x.property
  rw [← hc]
  change FieldWeyl.W f (∑ g ∈ c.support,c g • exponential g) ∈ domain
  rw [map_sum]
  apply Submodule.sum_mem
  intro g hg
  rw [map_smul,FieldWeyl.W,ConcreteWeyl.W_exponential]
  exact domain.smul_mem _ (domain.smul_mem _ (exponential_mem_domain _))

theorem Weyl_domain_hasDerivAt (f : H1) (x : domain) :
    HasDerivAt (fun t : ℝ => FieldWeyl.W ((t:ℂ) • f) (x:F))
      ((Complex.I * (Real.sqrt 2:ℂ)) • segal f x) 0 := by
  classical
  let c := preimage x
  let y : H1 → domain := fun g => ⟨exponential g,exponential_mem_domain g⟩
  have hy : ∑ g ∈ c.support,c g • y g = x := by
    apply Subtype.ext
    change synthesize c = (x:F)
    exact preimage_spec x
  have hd := HasDerivAt.fun_sum (u := c.support) (fun g hg =>
    (Weyl_exponential_segal f g).const_smul (c g))
  convert hd using 1
  · funext t
    rw [← hy]
    change FieldWeyl.W ((t:ℂ) • f) (∑ g ∈ c.support,c g • exponential g) = _
    simp only [map_sum,map_smul]
  · change (Complex.I * (Real.sqrt 2:ℂ)) • (segal f).toFun x = _
    rw [← hy,map_sum]
    simp only [map_smul,Finset.smul_sum,smul_comm]

end F1Fecho.Creation
#print axioms F1Fecho.Creation.Weyl_preserves_domain
#print axioms F1Fecho.Creation.Weyl_domain_hasDerivAt
