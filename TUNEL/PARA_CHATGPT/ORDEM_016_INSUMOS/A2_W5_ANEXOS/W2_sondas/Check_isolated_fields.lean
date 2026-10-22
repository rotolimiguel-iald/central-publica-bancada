import ContratoQG

set_option autoImplicit false

/-!
# Check_isolated_fields -- ISOLAMENTO (C3; generaliza o `Check_rfl_dA.lean` do cético W2)

No `ProbeTrivialH3.lean`, `dA_eq := by rfl`, `dS_eq := by simp [...]` e `clausius := by rfl` NÃO
acusam erro porque o goal contém o sorry sintético do campo `H2` (SUPRESSÃO, não prova). Este
arquivo isola as três obrigações com um `C : ContratoH2 W₀ R₀` GENÉRICO (hipótese): se cada uma
falhar aqui (rc≠0, três erros), fica medido que os três campos calculados MORDEM — só não aparecem
no log do probe por supressão. ESTE ARQUIVO DEVE FALHAR AO COMPILAR.
-/

namespace TGLExt.CeticoW2

open TGL.SpecificAQFT TGL.ModularRealization ChatgptAudit TGLV354.TraceCompletion TGLExt.ContratoQG

noncomputable section

example (C : ContratoH2 theSpecificAQFTWitness regularModularRealization) :
    (1 : ℝ) = areaVariation C (Set.Icc 0 1) 1 := by rfl

example (C : ContratoH2 theSpecificAQFTWitness regularModularRealization) :
    (1 / 4 : ℝ) = ChatgptAudit.Response028.prefixEntropyIncrement C.profile mixProfile 0 := by
  simp [ChatgptAudit.Response028.prefixEntropyIncrement]

example (C : ContratoH2 theSpecificAQFTWitness regularModularRealization) :
    (1 / (8 * Real.pi) : ℝ) = (C.kappa / (2 * Real.pi)) * (1 / 4) := by rfl

end

end TGLExt.CeticoW2
