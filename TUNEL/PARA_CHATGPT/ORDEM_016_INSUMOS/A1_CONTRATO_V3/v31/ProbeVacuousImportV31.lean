import ContratoQG_v31
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# ProbeVacuousImportV31 — A SONDA DO VAZIO contra o import INDEXADO   [DIAGNÓSTICO; DEVE FALHAR]
  Frente contrato_v3, RODADA 2, 23/09/2026. Porte da ProbeVacuousImportV3 (a25cce1478c08339) com os índices N, T.

  O tipo do import é `ContratoImportH3 W R N T h2`, indexado por um termo H2 do MESMO (W, R, N). No par legado e
  no brinquedo não há termo (`contratoH2_empty_on_legacy`, `toy_not_v31_by_fidelity`): os dois `def` abaixo DEVEM
  FALHAR (no índice). O que o ex falso ainda produz — e compila — é só a FUNÇÃO de domínio vazio, que não é
  termo do tipo reservado.
-/

namespace TGLExt.ContratoQGv31.ProbeVacuo

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion ChatgptAudit
open TGLExt.ContratoQGv31 W5Final.Toy

noncomputable section

theorem nullDir_ne_zero : nullDir ≠ 0 := by
  intro h0; have := congrFun h0 0; simp [nullDir] at this

theorem toy_null_one : toyW.U nullDir = 1 := by
  change toyU nullDir = 1
  ext v
  rw [toyU_apply]
  simpa [nullDir] using modularFlow_zero_time (P := mixProfile) v

variable (N : KillingNormalization)

/-- 1. par legado: o truque ex falso precisa de um índice — DEVE FALHAR aqui. -/
def vacuousImportLegacy (T : StressTensorData theSpecificAQFTWitness) :
    ContratoImportH3 theSpecificAQFTWitness regularModularRealization N T (Classical.choice ⟨_⟩) where
  produce := fun h => absurd (h.translations_faithful nullDir rfl) nullDir_ne_zero
  same_horizon := fun h => absurd (h.translations_faithful nullDir rfl) nullDir_ne_zero

/-- 2. brinquedo de W5: idem — DEVE FALHAR no índice. -/
def vacuousImportToy (T : StressTensorData toyW) :
    ContratoImportH3 toyW toyR N T (Classical.choice ⟨_⟩) where
  produce := fun h => absurd (h.translations_faithful nullDir toy_null_one) nullDir_ne_zero
  same_horizon := fun h => absurd (h.translations_faithful nullDir toy_null_one) nullDir_ne_zero

/-- 3. O QUE COMPILA (esperado): a função de índice vazio. Não é termo do tipo reservado. -/
def vacuousImportFun (T : StressTensorData theSpecificAQFTWitness)
    (h2 : ContratoH2 theSpecificAQFTWitness regularModularRealization N) :
    ContratoImportH3 theSpecificAQFTWitness regularModularRealization N T h2 where
  produce := fun h => absurd (h.translations_faithful nullDir rfl) nullDir_ne_zero
  same_horizon := fun h => absurd (h.translations_faithful nullDir rfl) nullDir_ne_zero

#print axioms nullDir_ne_zero
#print axioms toy_null_one
#print axioms vacuousImportFun

end

end TGLExt.ContratoQGv31.ProbeVacuo
