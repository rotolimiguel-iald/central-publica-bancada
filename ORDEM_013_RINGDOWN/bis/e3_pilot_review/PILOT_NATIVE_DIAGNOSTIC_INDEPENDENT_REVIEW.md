# Diagnóstico finito do piloto — revisão independente

**FINITE_NATIVE_DIAGNOSIS_REVIEWED_REPAIR_NOT_APPROVED.** Recibo `PILOT_NATIVE_DIAGNOSTIC_INDEPENDENT_REVIEW.json`, SHA256 `3d170b546abe6d3d438c17d6402b95ab8209f90ef4f2a63f9f597aab4dcd8e9a`. Foram89 verificações sobre evidências existentes, sem executar ondas, strain, PE ou posterior. Este documento sucede o parecer preliminar sem sobrescrevê-lo.

[REAL — recibos de A conferidos]10 processos diagnósticos, sendo1 replay de prior e9 children com16 entradas de fonte e15 retornos. Todos dentro dos limites documentados de tempo; arquivos de casos, entradas e logs foram vinculados pelos hashes. A árvore E2 original permanece idêntica aos14 pins registrados.

| Caso | Resultado registrado |
|---|---|
| Sequência8 na configuração original1024 | rc0; draws2/8 retornam None por domínio; os demais retornam ondas finitas |
| DRAW2_1024 e DRAW8_1024 isolados | None por domínio, rc0 |
| DRAW2_2048 e DRAW2_8192 | Ondas finitas nesses pontos |
| DRAW8_2048 | **rc−6**, `free(): invalid next size (normal)`, sem retorno Python |
| LOW_GR_1024 / LOW_GR_2048 | None / onda finita |
| LOW_DEFORMED_8192 | Onda finita nesse ponto |

As massas dos dois erros impressos no log original coincidem exatamente com draws2/8 do replay. Isso não fornece as deformações da chamada que causou SIGSEGV nem prova que a sequência completa de inicialização nativa foi reproduzida. O SIGSEGV original rc−11 não reapareceu na sequência8; o abort rc−6 em2048 é uma falha distinta observada. **Aumentar fmax para2048 não é reparo suficiente.**

[DERIVED — controle escalar leve] Para DRAW2, norma² na banda20–1024 foi7,5919729051×10⁻⁴⁴ em2048 e7,5919742743×10⁻⁴⁴ em8192: diferença relativa1,8035×10⁻⁷. Concordância de norma escalar não demonstra fase complexa, overlap, epoch ou igualdade da onda. Não há arrays diagnósticos preservados nesses recibos para pagar esses controles agora; não os inventar.

## Achados que permanecem para a reparação concreta

- **NF-R2:** faltam adaptador versionado e evidência correspondente. Preservar família/todos os modos, dados/PSD, priors e banda científica20–1024. Separar geração interna de banda da likelihood; revisar deltaF, epoch/fase e transporte. Erro numérico não pode virar -inf para aparar prior. Um wrapper que isola crash deve tornar falha visível; isolamento sozinho não gera likelihood válida para o ponto.
- **NF-R3:** falta revisão do contrato de execução da emenda concreta. ParentE2 e witness original continuam verificados; novos fontes/imports/launcher têm pins próprios e testemunha explícita no túnel. Novo run/output exclusivo em cache. Stop herdado: **2026-09-23T06:35:19.847427 UTC**, sem reiniciar8h. Jobs cegos só consomem a emenda se a declararem explicitamente.
- **NF-R4:** as três entradas C do PLAN_INPUTS apontam a `.c` extraído, mas seus hashes/tamanhos pertencem a `.c.html`. Todos os HTML originais estão preservados e conferem. Corrigir por recibo ao lado com vínculo HTML→texto e ambos os hashes; não precisa repetir ciência. Detalhes em `PILOT_FAILURE_SOURCE_MAPPING_ADENDO.json`.

**NF-R1, qualificação ao lado:** o diagnóstico distingue EDOM de Nyquist e um caso nativo inseguro; a causa exata do SIGSEGV original permanece OPEN. Não exigir descoberta universal da causa nativa como precondição abstrata se um reparo concreto puder demonstrar preservação de suporte e falha visível. Também não anunciar que a causa foi corrigida apenas porque exemplos em8192 passaram. A aprovação depende do código e contrato efetivamente apresentados.

O desenho detalhado de emenda está em `PILOT_NATIVE_FAILURE_PRELIMINARY_REVIEW.md`. A fonte de condicionamento agora disponível corrobora deltaT=0,5/f_nyquist; com fmax1024 e deltaF1/16 resulta fs interno2048, enquanto os dados têm fs4096. A checagem C que gerou os EDOM usa GR550 no ramo HM, não diretamente domega. Compilação reprodutível do binário a partir desse texto não foi demonstrada.

Os controladores diagnósticos documentam retorno/wait, mas não um campo group_absent. Não atribuo a eles uma verificação independente de todos os grupos. O cleanup do piloto original segue seu próprio recibo. Nenhuma nova campanha é solicitada por esta revisão documental.

Kerr V2 permanece fechado apenas como calibração conhecida descritiva, equivalent_reproduction_paid=false; nada aqui altera seu recibo. O observador permanece inativo e fora do gate do piloto/ordem completa. Seu destino cache foi corrigido, com72 testes finitos e recibo em `bis/e3_pilot_observer/IMPLEMENTATION_RECEIPT.json` para revisão separada do principal.
