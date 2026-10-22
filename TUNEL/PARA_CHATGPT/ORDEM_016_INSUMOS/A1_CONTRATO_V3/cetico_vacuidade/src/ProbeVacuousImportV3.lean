import ContratoQG_v3
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# ProbeVacuousImportV3 — A SONDA DO VAZIO contra o import INDEXADO   [DIAGNÓSTICO; DEVE FALHAR]
  Frente contrato_v3, 23/09/2026.

  Na v2 a sonda `ProbeVacuousImportH3` COMPILAVA no par legado (rc=0: `produce := fun h => (vazio h).elim`),
  e o leitor tinha de apagar a bandeira por fora (gpi_H3 := gpi_H3 ∧ gpf_H2). Na v3 o tipo do import é
  `ContratoImportH3 W R h2` — INDEXADO por um termo H2 do MESMO par. A sonda do vazio precisa ESCREVER o
  índice, e no par legado / no brinquedo não há termo (teoremas `contratoH2_empty_on_legacy`,
  `toy_not_v3_by_fidelity`). Os dois `def` abaixo DEVEM FALHAR (no índice).

  O que o ex falso ainda produz — e compila — é só a FUNÇÃO `∀ h2, ContratoImportH3 L R h2` (de domínio
  vazio). Ela NÃO é um termo do tipo reservado: o gate exige o termo FECHADO
  `qgImport_H3_… : ContratoImportH3 W₀ R₀ qgPrice_H2_…`, cujo índice é o H2 RESERVADO (gpf_H2 por tipo).
-/

namespace TGLExt.ContratoQGv3.ProbeVacuo

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion ChatgptAudit
open TGLExt.ContratoQGv3 W5Final.Toy

noncomputable section

theorem nullDir_ne_zero : nullDir ≠ 0 := by
  intro h0; have := congrFun h0 0; simp [nullDir] at this

theorem toy_null_one : toyW.U nullDir = 1 := by
  change toyU nullDir = 1
  ext v
  rw [toyU_apply]
  simpa [nullDir] using modularFlow_zero_time (P := mixProfile) v

/-- 1. par legado: o truque ex falso da v2 precisa de um índice — DEVE FALHAR aqui. -/
def vacuousImportLegacy :
    ContratoImportH3 theSpecificAQFTWitness regularModularRealization (Classical.choice ⟨_⟩) where
  produce := fun h => absurd (h.translations_faithful nullDir rfl) nullDir_ne_zero
  same_horizon := fun h => absurd (h.translations_faithful nullDir rfl) nullDir_ne_zero

/-- 2. brinquedo de W5: idem — DEVE FALHAR no índice. -/
def vacuousImportToy : ContratoImportH3 toyW toyR (Classical.choice ⟨_⟩) where
  produce := fun h => absurd (h.translations_faithful nullDir toy_null_one) nullDir_ne_zero
  same_horizon := fun h => absurd (h.translations_faithful nullDir toy_null_one) nullDir_ne_zero

/-- 3. O QUE COMPILA (esperado): a função de índice vazio. Não é termo do tipo reservado. -/
def vacuousImportFun (h2 : ContratoH2 theSpecificAQFTWitness regularModularRealization) :
    ContratoImportH3 theSpecificAQFTWitness regularModularRealization h2 where
  produce := fun h => absurd (h.translations_faithful nullDir rfl) nullDir_ne_zero
  same_horizon := fun h => absurd (h.translations_faithful nullDir rfl) nullDir_ne_zero

#print axioms nullDir_ne_zero
#print axioms toy_null_one
#print axioms vacuousImportFun

end

end TGLExt.ContratoQGv3.ProbeVacuo
