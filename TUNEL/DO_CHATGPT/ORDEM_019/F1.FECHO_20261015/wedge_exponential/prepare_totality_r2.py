from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'RealSubspaceTotalityR1.lean').read_text(encoding='utf8').replace('import WedgeAnalyticR1','import WedgeAnalyticR2')
s=s.replace('simp only [RCLike.real_smul_eq_coe_smul (K := ℂ)]','simp only [← ofReal_smul_H1]')
s=s.replace('simpa only [RCLike.real_smul_eq_coe_smul (K := ℂ)] using K.smul_mem t hy','rw [ofReal_smul_H1]\n    exact K.smul_mem t hy')
s=s.replace('(innerSL ℂ (v n : TensorHilbert n)).analyticAt.comp','((innerSL ℂ (v n : TensorHilbert n)).analyticAt _).comp')
s=s.replace('end F1Fecho.WedgeExponential',r'''theorem standard_complex_span_dense (K : StandardSubspace H1) :
    (Submodule.span ℂ (K.toClosedSubmodule : Set H1)).topologicalClosure = ⊤ := by
  let p := Submodule.span ℂ (K.toClosedSubmodule : Set H1)
  let C : ClosedSubmodule ℝ H1 :=
    { toSubmodule := p.topologicalClosure.restrictScalars ℝ
      isClosed' := p.isClosed_topologicalClosure }
  have hk : K.toClosedSubmodule ≤ C := by
    intro x hx
    exact p.le_topologicalClosure (Submodule.subset_span hx)
  have hi : K.toClosedSubmodule.mulI ≤ C := by
    intro x hx
    change x ∈ K.toClosedSubmodule.toSubmodule.map
      (scalarSMulCLE H1 Complex.UnitI).toLinearMap at hx
    obtain ⟨y,hy,rfl⟩ := hx
    change Complex.I • y ∈ p.topologicalClosure
    exact p.topologicalClosure.smul_mem Complex.I (p.le_topologicalClosure (Submodule.subset_span hy))
  have ht : (⊤ : ClosedSubmodule ℝ H1) ≤ C := by
    rw [← K.IsCyclic]
    exact sup_le hk hi
  apply top_unique
  intro x _
  exact ht (by trivial : x ∈ (⊤ : ClosedSubmodule ℝ H1))

theorem standard_exponential_total (K : StandardSubspace H1) :
    (Submodule.span ℂ (exponential '' (K.toClosedSubmodule : Set H1))).topologicalClosure = ⊤ :=
  exponential_real_subspace_total K.toClosedSubmodule.toSubmodule (standard_complex_span_dense K)

theorem canonical_wedge_exponential_total :
    (Submodule.span ℂ (exponential ''
      (F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule : Set H1))).topologicalClosure = ⊤ :=
  standard_exponential_total F1Rede.CanonicalWedge.spectralOutput.KWR

end F1Fecho.WedgeExponential''')
s+='\n#print axioms F1Fecho.WedgeExponential.standard_complex_span_dense\n#print axioms F1Fecho.WedgeExponential.standard_exponential_total\n#print axioms F1Fecho.WedgeExponential.canonical_wedge_exponential_total\n'
with (b/'RealSubspaceTotalityR2.lean').open('x',encoding='utf8',newline='\n') as f:f.write(s)
