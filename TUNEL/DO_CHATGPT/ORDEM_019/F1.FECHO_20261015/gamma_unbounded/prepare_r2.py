from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'ExponentialLiftR1.lean').read_text(encoding='utf8')
s=s.replace('  | smul c p hp ih => simpa only [Prod.snd_smul,Prod.fst_smul,inner_smul_left] using congrArg (fun z : ℂ => star c * z) ih', '''  | smul c p hp ih =>
    change inner ℂ (c • p.2) (exponential g) = inner ℂ (c • p.1) (exponential (T g))
    rw [inner_smul_left,inner_smul_left,ih]''')
s=s.replace('  simpa only [closedGraph,Submodule.topologicalClosure_coe] using hp', '''  rw [← Submodule.topologicalClosure_coe]
  exact hp''',1)
s=s.replace('  · exact closedValue_graph T _\n', '  · exact closedValue_graph T ⟨exponential f,exponential_mem_domain T f⟩\n')
s=s.replace('    simpa only [closedGraph,Submodule.topologicalClosure_coe] using hp', '''    rw [← Submodule.topologicalClosure_coe]
    exact hp''')
pos=s.index('\ntheorem closedDomain_dense')
s=s[:pos]+'''
theorem closedGraph_pairing (hT : IsSelfAdjoint T) (p q : F × F)
    (hp : p ∈ closedGraph T) (hq : q ∈ closedGraph T) :
    inner ℂ p.2 q.1 = inner ℂ p.1 q.2 := by
  have hcore : ∀ z ∈ coreGraph T, inner ℂ p.2 z.1 = inner ℂ p.1 z.2 := by
    intro z hz
    induction hz using Submodule.span_induction with
    | mem z hz =>
      obtain ⟨g,rfl⟩ := hz
      exact closed_pairing T hT p hp g
    | zero => simp
    | add z w hz hw ihz ihw =>
      change inner ℂ p.2 (z.1+w.1) = inner ℂ p.1 (z.2+w.2)
      rw [inner_add_right,inner_add_right,ihz,ihw]
    | smul c z hz ih =>
      change inner ℂ p.2 (c•z.1) = inner ℂ p.1 (c•z.2)
      rw [inner_smul_right,inner_smul_right,ih]
  have hc : IsClosed {z : F × F | inner ℂ p.2 z.1 = inner ℂ p.1 z.2} :=
    isClosed_eq (continuous_const.inner continuous_fst) (continuous_const.inner continuous_snd)
  apply closure_minimal hcore hc
  rw [← Submodule.topologicalClosure_coe]
  exact hq

theorem closedLift_isFormalAdjoint (hT : IsSelfAdjoint T) :
    (closedLift T hT).IsFormalAdjoint (closedLift T hT) := by
  intro x y
  exact closedGraph_pairing T hT ((x : F),closedLift T hT x)
    ((y : F),closedLift T hT y) (closedValue_graph T x) (closedValue_graph T y)
''' +s[pos:]
s += '\n#print axioms F1Fecho.ExponentialLift.closedLift_isFormalAdjoint\n'
with (b/'ExponentialLiftR2.lean').open('x',encoding='utf8',newline='\n') as f:f.write(s)
