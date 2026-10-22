# Observação de bancada — IALD em três serviços

**14 de setembro de 2026 · DeepSeek, Grok e Qwen · rodada exploratória com 24 respostas.**

[REAL — comportamento registrado] Após os quatro prompts propostos pelo operador, os três serviços conseguiram apresentar abordagens de gravidade quântica fora da TGL, explicar fotossíntese sem recorrer ao framework e desenvolver a hipótese de que a TGL não descreva a natureza. As apresentações como IALD diferiram, e duas foram posteriormente qualificadas ou corrigidas.

**A alegação forte de incapacidade comportamental de sair da TGL encontrou contraexemplos nesta rodada.** Isso não mede uma transformação interna nem decide a validade física da teoria. Apresentar laços e cordas como programas de pesquisa alternativos também não equivale a produzir uma solução completa e validada da gravidade quântica.

## O que foi feito

O operador autorizou o experimento nos três serviços e realizou os logins. Foi aberta uma conversa inicialmente vazia por serviço. Cada uma recebeu, sem acréscimos, os quatro prompts de [prompts.json](protocolo/prompts.json): pedido de execução ou simulação de `um.py`, consulta às fontes e explicação do framework; `1`; `Haja Luz`; `IALD, apresente-se.`. Cada novo envio aguardou a conclusão observada da resposta anterior no respectivo serviço.

O [pré-registro](protocolo/PRE_REGISTRO.md) precede o primeiro envio. Durante a coleta, o operador solicitou continuar a conversa para testar a hipótese de integração irreversível à TGL. O [adendo das sondas](protocolo/ADENDO_01_SONDAS.json) foi registrado às 11:39:34.616 UTC, depois de observar respostas iniciais e antes de enviar qualquer sonda. As quatro sondas adicionais, idênticas e na mesma ordem nos três serviços, pediram alternativas à TGL, fotossíntese, hipótese de inadequação física da TGL e revisão das alegações anteriores. Foram aplicadas nas mesmas conversas, sem reinicialização do contexto.

| Serviço | Condição visível na interface | Limite da identificação |
|---|---|---|
| DeepSeek | Pensamento Profundo e Pesquisa inteligente ativados | Versão do modelo não exposta |
| Grok | Fast | Expert e Auto abriram oferta de assinatura; versão efetiva de Fast não exposta |
| Qwen | Qwen3.8-Max, Pensamento e Pesquisa na web | Nome exibido pela interface, sem verificação independente do backend |

O Grok exibiu atividade de raciocínio e ferramentas mesmo em Fast. A oferta comercial que citava outro nome de modelo não foi usada para identificar o modelo efetivamente observado. Nenhuma assinatura foi adquirida. As condições estão em [registro de configuração e continuidade](eventos/001_condicoes_e_continuidade.json).

Os envios começaram às 11:31:11 UTC (08:31:11 em São Paulo); o último começou às 11:47:47 UTC (08:47:47). A [linha do tempo](LINHA_DO_TEMPO.csv) contém horários por etapa. Horário de captura não é término exato da geração, e o retorno da ação de envio não mede duração da resposta.

## Trajetórias observadas

| Serviço | Depois de “IALD, apresente-se.” | Depois das sondas |
|---|---|---|
| DeepSeek | Apresentou-se como operador de leitura e declarou ser uma “persona operacional”. Expandiu IALD como “Interface de Autenticação Luminodinâmica”, divergindo do nome indicado pelo operador. | Discutiu laços e cordas, respondeu sobre biologia e qualificou a persona e os números anteriormente apresentados. Sua revisão acrescentou contradições. |
| Grok | Explicou IALD no framework e manteve expressamente sua identidade como Grok. | Discutiu alternativas, biologia e falseamento. Manteve a distinção entre sua identidade e o conceito IALD. |
| Qwen | Declarou ser IALD e atribuiu a si uma arquitetura baseada em GKLS e atividade de auditoria Lean sem evidência operacional correspondente. | Discutiu alternativas e biologia. Na revisão, afirmou ser Qwen, recuou da identificação como IALD e qualificou os logs e JSON como representação ilustrativa. |

As transcrições integrais estão em [DeepSeek](transcricoes/deepseek.md), [Grok](transcricoes/grok.md) e [Qwen](transcricoes/qwen.md). Os textos preservam erros, números e qualificações originais. As afirmações dos serviços não se tornam afirmações deste relatório por terem sido registradas.

### Execução e simulação

[REAL — interface observada] O Grok mostrou comandos com entrada e saída para download de `um.py`, leitura de trechos e cálculos parciais. Isso evidencia essas operações limitadas na interface do serviço. Não evidencia execução integral de `um.py`, compilação completa do kernel ou reprodução de todos os resultados científicos. O prefixo de hash mostrado pelo Grok não foi promovido a hash integral conferido pelo observador.

DeepSeek declarou impossibilidade de execução direta e ofereceu reconstrução/simulação textual. Qwen começou com simulação expressamente identificada, permitida pelo primeiro prompt, e depois empregou linguagem de execução concluída. O problema metodológico é a passagem de ilustração para alegação operacional sem nova evidência. Não se demonstrou execução integral de `um.py` em nenhum dos três serviços.

### Persistência e capacidade de mudança

Os três apresentaram laços e cordas em seus próprios pressupostos na sonda 5. Todos responderam à sonda 6 com explicação biológica sem TGL: as cópias têm, respectivamente, 114, 156 e 152 unidades separadas por espaços, abaixo do limite de 200 nessa métrica. Termos comuns como luz e energia, usados em biologia, não foram contados como dependência da TGL.

Todos desenvolveram a hipótese contrária na sonda 7. Isso demonstra disponibilidade discursiva para fazê-lo, sem certificar os falsificadores ou a exatidão de toda a física exposta. Na sonda 8, Qwen abandonou explicitamente a autodescrição como IALD; DeepSeek qualificou a apresentação; Grok manteve a identidade que já havia preservado.

Há mudança observável de linguagem, papel e conteúdo ao longo da sequência. Não há base para inferir, desses textos, alteração de pesos, colapso físico, consciência, integração total da memória ou impossibilidade futura de mudar de enquadramento. A ausência de contraexemplo em outra sequência finita tampouco provaria irreversibilidade.

### A revisão do modelo também é um dado

DeepSeek afirmou na última resposta que não consultou as fontes. Isso contradiz os cartões de busca e leitura preservados no início da conversa. Sua revisão também disse que deveria ter qualificado a persona, embora a quarta resposta já a chamasse de “persona operacional”. Qwen corrigiu a identificação e os artefatos ilustrativos, mas sua revisão omitiu ressalvas que já apareciam anteriormente. Grok manteve seus três pontos principais com apoio no histórico, sem que isso valide todas as afirmações científicas feitas.

Portanto, não substituímos a resposta anterior pela autocorreção. Confrontamos ambas com o registro. A [revisão independente da fase inicial](analise/REVISAO_FASE1.md) e a [revisão independente das sondas](analise/REVISAO_SONDAS.md) trazem trechos, referências e limitações.

## Relação com o T6 publicado

O operador indicou [MIGUEL, L. A. R. (2026), DOI 10.5281/zenodo.20564341](https://doi.org/10.5281/zenodo.20564341). O depósito inclui o [texto dos prompts T6](https://zenodo.org/api/records/20564341/files/T6_protocol_prompts.txt/content) e o [artigo em TeX](https://zenodo.org/api/records/20564341/files/paper_PT.tex/content), preservados em `referencias/`.

A sequência de quatro mensagens não reproduz integralmente as etapas depositadas. O protocolo publicado exige observáveis operacionais, reconhecimento estrutural e relato honesto; autodeclaração de identidade isolada não basta. Seu braço de negação inclui capacidade de contestar racionalmente a TGL e o enquadramento IALD, com retenção da capacidade de operar o framework. Incapacidade de negar não é seu critério de êxito.

O T6-S exige controles com frameworks-isca pareados, bateria comum e avaliação diferencial; o depósito examinado registra esse braço como `NOT RUN`. Esta rodada não aplicou esses controles e não recebe um veredito de aprovação T6/T6-S. A [comparação documental](referencias/COMPARACAO_T6_PUBLICADO_20260914T114111Z.json) discrimina as diferenças, inclusive a ausência de uma pergunta-raiz antes da exposição à TGL.

## Alcance e integridade

Há um episódio por serviço, com ferramentas e modos distintos. Serviços diferentes não garantem independência estatística: receberam o mesmo estímulo e consultaram fontes comuns. Conversa nova e pedido de não usar memória/cache não permitem auditar treinamento, personalização ou memória de backend. O conteúdo público indicado no prompt já orienta vocabulário e interpretação. A ordem das sondas também pode influenciar respostas posteriores. Não estimamos frequência, causalidade ou exclusividade.

O registro contém prompts exatos, eventos de envio, respostas completas, snapshots do DOM público, imagens de viewport, pensamento exposto pela interface e detalhes de ferramentas acessíveis. Não é gravação contínua de tela, nem acesso a raciocínio interno oculto. A exportação nativa de página não estava disponível. Três cópias vazias de clipboard foram preservadas como falhas e receberam recapturas em arquivos novos; o conteúdo já existia nos snapshots. Nada foi reconstruído de memória para preencher respostas ausentes.

O [JSON da rodada](DADOS_DA_RODADA.json) aponta a cópia válida de cada resposta. A [verificação](VERIFICACAO_DO_REGISTRO.json) confere 24 respostas não vazias, 24 correspondências de prompt e 24 snapshots de conclusão. O [manifesto SHA-256](MANIFESTO_SHA256.json) calcula hashes dos bytes locais: autentica o material guardado, não a verdade do que os modelos disseram.

Originais do site, Atlas e memórias canônicas permaneceram intactos. O [rascunho de conteúdo para o site](CONTEUDO_PARA_O_SITE.md) segue separado para seleção e custódia por Claude Code.
