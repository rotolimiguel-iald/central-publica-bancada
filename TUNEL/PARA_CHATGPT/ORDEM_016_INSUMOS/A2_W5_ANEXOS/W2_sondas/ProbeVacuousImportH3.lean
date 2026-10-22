import ContratoQG
-- NA TRANSPOSIÇÃO (TGLExt/ProbeVacuousImportH3.lean): `import TGLExt.ContratoQG` e, quando a partição
-- cunhar o par ratificado, `probeTarget := TGLExt.V370Partition.ratifiedWitness` (duas linhas).

set_option autoImplicit false

/-!
# ProbeVacuousImportH3 -- SONDA DO VAZIO (do cético W2, 23/09/2026; C1)   [DIAGNÓSTICO; NUNCA importado]

Hipótese a testar: se `ContratoH2 W₀ R₀` é VAZIO por teorema no par-alvo (hoje: o par legado,
`contratoH2_empty_on_legacy_realization`), qualquer função de domínio `ContratoH2 W₀ R₀` existe por
vacuidade. Logo `ContratoImportH3 W₀ R₀` é habitável EX FALSO, com axiomas limpos, sem produzir H3
nenhum — e um leitor por nome acenderia `gpi_H3_horizon_data_produced` (modo IMPORTED no razonete
um.py:161383) se alguém cunhasse o nome reservado assim.

SE ESTE ARQUIVO COMPILAR (rc=0, axiomas no trio), o furo está DEMONSTRADO no par-alvo. Por isso o
leitor (`_H2H3_NEGATIVE_PROBES`) o exige REPROVADO (rc≠0) para `gpi_H3` — e, além disso,
`gpi_H3 := gpi_H3 ∧ gpf_H2` (C1-ii): um import só vale com um H2 REAL no mesmo par.

HOJE (par legado como alvo) ESTE ARQUIVO COMPILA — é o esperado ATÉ A PARTIÇÃO: a bandeira fica False
(fail-closed). Quando `probeTarget` passar a ser o par ratificado (≠ legado), `.false h` deixa de
tipar e a sonda REPROVA; se o par ratificado fosse o legado, ela continuaria a compilar e a bandeira
continuaria apagada (`ratifying_the_legacy_pair_ratifies_the_void`).
-/

namespace TGLExt.CeticoW2

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion TGLExt.ContratoQG

noncomputable section

/-- o PAR-ALVO da sonda. HOJE: o par legado. NA PARTIÇÃO: `TGLExt.V370Partition.ratifiedWitness`. -/
abbrev probeTarget : FullTGLWitness := regularFullWitness

def vacuousImport : ContratoImportH3 probeTarget.1 probeTarget.2 where
  produce := fun h => (contratoH2_empty_on_legacy_realization.false h).elim
  same_horizon := fun h => (contratoH2_empty_on_legacy_realization.false h).elim

/-- e ele "instancia" `the_trio_is_a_pair` exatamente como o import legítimo faria. -/
theorem vacuous_import_makes_the_trio_a_pair {H1 P : Prop}
    (master : H1 ∧ Nonempty (ContratoH2 probeTarget.1 probeTarget.2)
      ∧ Nonempty (ContratoH3 probeTarget.1 probeTarget.2) → P) :
    H1 ∧ Nonempty (ContratoH2 probeTarget.1 probeTarget.2) → P :=
  import_makes_the_trio_a_pair vacuousImport master

#print axioms vacuousImport
#print axioms vacuous_import_makes_the_trio_a_pair

end

end TGLExt.CeticoW2
