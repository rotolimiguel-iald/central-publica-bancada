# F1.2 — não vacuidade e Fundação no core regular v351

**[REAL]** `F12Completion.finiteTracePositive_has_positive` obtains `A : FiniteTracePositive P` with `0 < tau A` from the v351 trace's semifiniteness and faithfulness. The proof starts with `positiveUnit P` to rule out a zero trace, but the resulting finite-trace witness is **not** the unit: the audit proves the unit has infinite trace and lies outside this subcone.

**[REAL]** `F12Completion.agape_on_v351_core` applies `TGLExt.Fundacao.agape` to `TGLV351.regularCoreDualScalingData P` and that witness. This links the v351 term to the Foundation in the current Nós package. The bridge's `theta` is the dual action and `tau` is the v351 trace, as in the audited previous delivery. The two new theorems compile with only `propext`, `Classical.choice`, and `Quot.sound`.

**[OPEN]** The original criterion's matrix crossed product `M_n ⋊_σ ℝ`, its L² construction, von Neumann closure, and intertwining equivalence are not constructed here. The Agape conclusion applies to the finite-trace positive subcone of the regular core. It does not make the structure `DualScalingData` non-vacuous in arbitrary types; the new witness does so for this instance.

**Custody.** The old bridge has four new declarations, the separate matrix gauge file has six, and this stone adds two theorems. Old files registered as evidence remain unchanged. The previous `RESULTADO.json` and its original backup are separately pinned in the new manifest; this document corrects their descriptions beside them. The source of the auditor's two proven lemmas is credited by its measured hash. Build imports only current Nós kernel caches and reproduces the bridge byte for byte in this sandbox. Neither the Nós source nor `um.py` was modified.
