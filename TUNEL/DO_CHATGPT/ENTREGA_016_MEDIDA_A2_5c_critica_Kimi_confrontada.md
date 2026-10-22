[REAL — confronto documental com provas compiladas; parecer externo DECLARADO]

# A-2.5.c — crítica Kimi recebida e reconciliada

Data UTC: 2026-09-24T14:56:15.032718+00:00. ABERTURA sha256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
Resposta bruta: `a25c_kimi_scope_answer.md`, sha256 `217bc85101aafcbd431595d558c7b18d8cf98505a6e75f20ad7dc0f1e52bcd04`.
Recibo: `a25c_kimi_scope_receipt.json`. Uma execução, 1069.484 s,
uso `{"prompt_tokens": 317314, "completion_tokens": 38452, "cached_input_tokens": 256, "total_tokens": 355766}`. Custo monetário não informado.

O Kimi leu apenas os quatro arquivos do primeiro pacote (17 declarações), sem os módulos
importados. Não executou Lean. A revisão não cobre por extensão os 55 teoremas atuais.
As 12 fontes, logs e recibos atuais foram reconferidos por hash: rc 0, auditoria PASSA,
55 declarações e nenhuma alteração de kernel registrada.

| Ressalva do parecer | Confronto com o estado atual |
|---|---|
| R1: inversa à direita não basta | O módulo canônico V350PartialPositiveResolvent já contém partialOneAdd_injective e partialPositiveResolvent_inverse: R((I+D²)u)=u no domínio efetivo. selfadjointSquareResolvent instancia essa construção; não falta criar outra inversa. |
| P1: resolvente para D prescrito | selfadjoint_one_add_square_onto e selfadjointSquareResolvent, auditados. |
| P4: igualdade dos domínios | sameSquare_domain_eq, selfadjoint_absolute_domain e selfadjoint_normalizer_range, auditados. |
| P3: distinguir D de sua raiz positiva | unboundedTransform é literalmente D composto com normalizedInput = sqrt(R). Só a NORMA é comparada à de sqrt(1-R); não se substitui D por sua raiz positiva. |
| Gap ótimo | O contrato transporta limites inferiores. unboundedTransform_attainment transporta uma igualdade de normas dada; não declara por si só supremo espectral ou vetor não nulo no setor ortogonal. |

A construção atual não monta todos os campos de NormalizedGraphWitness para D arbitrário:
ela prova diretamente o contrato solicitado. Em particular, não declarar um novo teorema
de auto-adjunção/comutação do b construído que não esteja nessas fontes.
O controle unboundedTransform_ne_nonzero_idempotent impede identificá-lo literalmente
com um projetor não nulo. regularMinimalLock conserva seu papel de representante mínimo.

[REAL — correção de estado ao manifesto anterior] Kimi concluído. DeepSeek autorizado pelo
operador, porém a prévia classificou o pedido deep e excluiu seu tier standard: selected=null,
nenhum job nem envio à API. Evidência: a25c_deepseek_hypothesis_preview.json.
Não houve nova chamada, mudança de tier nem substituição de executor.

Próximo ramo: A-3.0 → A-3.d. Originais, gate e memórias canônicas intactos.
