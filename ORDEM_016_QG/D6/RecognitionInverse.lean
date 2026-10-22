import RecognitionGraph_v2

set_option autoImplicit false
namespace ORDEM016.D6
noncomputable section
open Set Topology
variable {H K : Type*}
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
variable {M : StarSubalgebra ℂ (H →L[ℂ] H)}
  {N : StarSubalgebra ℂ (K →L[ℂ] K)} {omega : H} {omega' : K}

def ReconhecimentoPeloConteudo.symm (R : ReconhecimentoPeloConteudo M N omega omega') :
    ReconhecimentoPeloConteudo N M omega' omega where
  U := R.U.symm
  reference := by rw [← R.reference]; simp
  algebra := by
    intro B
    simpa only [StarAlgEquiv.apply_symm_apply,LinearIsometryEquiv.symm_conjStarAlgEquiv] using
      (R.algebra (R.U.conjStarAlgEquiv.symm B)).symm

theorem recognized_domains_equal (R : ReconhecimentoPeloConteudo M N omega omega')
    (D : Set H) (E : Set K) (S : D → H) (T : E → K)
    (hs : Set.range (fun x : D => ((x : H),S x)) = closure (pairTomitaGraph M omega))
    (ht : Set.range (fun y : E => ((y : K),T y)) = closure (pairTomitaGraph N omega')) :
    R.U '' D = E := by
  ext y
  constructor
  · rintro ⟨x,hx,rfl⟩
    obtain ⟨z,hz,_⟩ := recognition_identifies_closed_operator R D E S T hs ht ⟨x,hx⟩
    exact hz ▸ z.property
  · intro hy
    obtain ⟨x,hx,_⟩ := recognition_identifies_closed_operator R.symm E D T S ht hs ⟨y,hy⟩
    refine ⟨x,x.property,?_⟩
    change (x : H)=R.U.symm y at hx
    rw [hx]; exact R.U.apply_symm_apply y

#print axioms ReconhecimentoPeloConteudo.symm
#print axioms recognized_domains_equal
end
end ORDEM016.D6
