[REAL — confronto com prova existente; DECLARADO — rascunho MiMo]
# MiMo B4 — reuso da ponte já compilada

Abertura sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
Resposta integral lida, sha256 `383ce62da3262bec41523226922350d1950c9b8ca21ebbb6c101afc737982a3f`.
Fonte existente sha256 `c87c30b04a63ae1a2e5c2adbc3a72f247eca7d3ac683b3f5ec5252bac688150e`; log sha256 `c6e9825bdd489705066d36e0acedb26bd63a9e2fc0f1bb046db0eebdf0969947`.
Compilação anterior rc0; auditoria 2/2 declarações no trio e zero sorry.

O caminho matemático sugerido pelo MiMo coincide com a prova existente:
expandir Fin3, converter adjuntos e identificar o mesmo núcleo/projetor.
As duas igualdades estão em penalty_eq_kernel_H3L e reading_eq_kernel_PF.
O arquivo existente já usa a orientação correta de
LinearMap.adjoint_toContinuousLinearMap e simp only para a segunda igualdade.

O helper proposto eq_of_forall_inner_eq tem encadeamento mal formado na aplicação
de norm_eq_zero.mp e pow_eq_zero_iff; também precisa tratar a coerção complexa.
Nenhum motivo para introduzi-lo: o lema de adjunto já resolve a ponte.
Não compilei o candidato MiMo nem atribuo rc0 a ele. Não fiz nova implementação,
novo ciclo Lean ou nova chamada. A compilação conferida é a anterior da bancada.
Não identifica as matrizes float do runtime, fluxo modular, estado físico ou gate.
