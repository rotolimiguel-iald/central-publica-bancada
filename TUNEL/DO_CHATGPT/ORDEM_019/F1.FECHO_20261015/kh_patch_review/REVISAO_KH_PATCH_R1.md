# Revisão KH-N1 R1

**REQUER CORREÇÃO — vínculo entre contrato e evidência.**

[REAL] A validação aceita três alterações de contagem com o mesmo log pinado: decl e axiom_report_entries +1; thm +1; lacuna de regex +1 e entradas −1. O hash conserva bytes, mas o código não lê os totais desses bytes. O recibo de auditoria também é apenas pinado; seu conteúdo não é vinculado ao log, às fontes e ao exit informado no contrato. `audit_exit_code=False` passa por igualdade com zero.

Exigir uma linha TOTAL única, reconstrução de entradas/lacuna/axiomas a partir do log, comparação integral e recibo tipado ligando exit inteiro zero, log e conjunto exato de fontes. A pré-medição deve continuar anterior ao rito.

[REAL] A estrutura do patch passa: só três atribuições AST mudam; a spec v393 original permanece em extras; os pisos históricos e as igualdades v394 estão separados. Recusas de hash adulterado, booleano em decl e axioma externo continuam funcionando. Nenhum main, candidato ou produção foi executado/escrito.

Detalhes, fontes, hashes e oito sondas em REVISAO_KH_PATCH_R1.json.
