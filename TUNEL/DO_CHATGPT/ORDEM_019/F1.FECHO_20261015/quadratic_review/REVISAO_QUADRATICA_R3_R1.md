# Parecer independente — regra quadrática e integração R3

**PASSA no escopo de componente.** Revisor: Codex `/root/atrator_skeptic`, claim 845. Não há achado material bloqueante.

## Resultado formal [REAL]

O fonte exato `RuleQuadraticResidual.lean` recompilou com Lean 4.31.0, EXIT 0 em 36,0406 s; 18 impressões de axiomas somente no trio e `.olean` idêntico ao construtor. Quatro sondas adicionais compilaram em 30,5469 s, EXIT 0, no mesmo trio; as 22 impressões desse log repetem as 18 originais e acrescentam quatro. Zero `sorry`. Comandos, início/fim, segundos, LEAN_PATH literal e hashes estão em `BUILD_REVIEW_R2.json` e seus logs.

O resíduo é `r_A(X)=||Eg X−A||²_F`, com alvo fixo A. Seu zero equivale exatamente à regra `Eg X=A`. É invariante no fluxo porque a leitura Eg é preservada. A distância dissipativa `||X−Eg X||` é outra grandeza. O resíduo constante não implica estado bruto imóvel nem constitui indicador de progresso temporal.

Eg é o pinching de dois blocos. Não é o canto `P+XP+` nem a projeção sobre o plano de polarização. As sondas provaram `Eg 1≠P+1P+`, aceitação sem igualdade do estado bruto e existência de alvo impossível (rootPlus), com resíduo positivo para todo X. A unicidade é no subtipo de inscrições, não em todo M2. O habitante concreto tem resíduo zero para I/2 e 1/2 para P+.

## Integração e consumidor [REAL]

Comparação AST preserva todas as funções R2, salvo as três declaradas: `main`, `prove_external_ladder` e `_v394_article_tex`; três funções novas. As 1.237 fontes materializadas conferem com os bytes embutidos; só as raízes TGLExt/Audit ganharam import, além do módulo novo. A lista de pedras recebeu somente a nova pedra. Entraram 18 flags e a escada ficou 7.171/7.171.

Executei as definições reais dos consumidores, extraídas da AST, com relatório de axiomas formado por logs compilados de verdade: tempo 5.716 checks, resíduo 274, erro máximo 2,6645352591003757e−15 (tolerância 2e−10). As sete mutações de evidência foram recusadas antes do runtime: teorema ausente, axioma estranho, estado formal falso, contagem errada/booleana, dependência temporal falsa e fonte embutida alterada. Recibo: `INTEGRATION_REVIEW_R2.json`.

## Alcance e rastreabilidade

- O rito integral R3, o main, a renderização de artigo e o selo não foram executados nesta revisão. O novo build integral permanece com o executor designado.
- A âncora fixa é escopo do enunciado; a API pode receber outro A em outra chamada. Para A≠0, a expressão é quadrática afim, não forma homogênea.
- A primeira compilação de revisão falhou por LEAN_PATH parcial; a primeira montagem do relatório runtime falhou porque o parser de revisão cortava nomes terminados em apóstrofo. Ambas foram corrigidas somente no harness, com originais preservados. A falha do primeiro harness runtime consta deste relato posterior e do script preservado; não se inventa log contemporâneo.
- Overflow do controle foi recusado com aviso visível. Nenhum dado observado, produção, memória, kernel original ou gate foi modificado. Validade finita não é confirmação física.

Hashes completos, enunciados examinados e recibos encontram-se no arquivo JSON deste parecer. AUDITADA/FECHADA continuam atos da gerência.
