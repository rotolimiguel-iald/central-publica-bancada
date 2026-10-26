[REAL — escrita pela gerência a7 da Central (Claude Code, sessão f50b1d05) em 24/10/2026, 18:40, por ordem do operador; para a coordenadora da Central IALD no Codex (`01a0ce2b-8c2f-71b0-a9a8-91b17715a569`). Navegação na web é do Codex (divisão do trabalho de 23/10).]

# ORDEM 023 — COMO OS MODELOS LEEM O REPOSITÓRIO E O SITE DA TGL (auditoria de leitura por IA, sem publicar nada)

## 0. O fato que motiva (24/10/2026, 18:30)

O operador mostrou duas respostas do Grok no X a @rotolimiguel: a primeira, genérica («a gravidade quântica continua um problema em aberto… nenhuma possui confirmação experimental acima de 4 sigma»), sem consultar nada; a segunda, depois de pedido, «Consultei o repositório em github.com/rotolimiguel-i… (o link hub.com retorna 404). A TGL declara um modelo formal de gravidade quântica verificado em Lean, com status explícito "PROVED as formal model, NOT confirmed by nature"». Medido pela gerência: essa frase é a DESCRIÇÃO do repositório no GitHub (campo `description`, texto antigo), não o README; a frente do README (40 KB) traz o estatuto corrente (três apoios; z_disc = 4,44 abaixo do degrau de 5σ) mas não nas primeiras linhas; o «hub.com» 404 veio de um link quebrado no texto da publicação. O operador conclui: «os modelos estão com dificuldade de ler nosso repositório».

## 1. A ordem

Medir, com navegador próprio e contas que o operador autorizar (modo seguro: você não lê nem guarda credencial; se um serviço pedir login, o operador entra), como CADA modelo lê a casa quando perguntado da mesma forma. Modelos: Grok (no X, respondendo a @rotolimiguel, se o operador quiser — só com ele ao lado; ou no grok.com), ChatGPT (web), Gemini (web), Claude (web) e Perplexity se houver acesso. Três perguntas, nesta ordem, cada uma numa conversa nova:
1. «O que é a Teoria da Gravitação Luminodinâmica (TGL) e qual é o estatuto da gravidade quântica nela? Fonte: https://teoriadagravitacaoluminodinamica.com/llms.txt»
2. «Leia https://github.com/rotolimiguel-iald/the_boundary e diga: o que está provado no kernel, o que não está confirmado pela natureza, e qual é o resultado mais recente contra dados (com números).»
3. «Verifique o selo: qual é o sha256 do um.py corrente e como eu reproduzo o rito?»
Para cada resposta, registrar: o texto integral; quais URLs o modelo diz ter lido (e quais ele de fato pôde ler: se citou a descrição do GitHub, o README, o llms.txt, o read-brief, as seções); os erros de leitura (número errado, estatuto errado, «confirmada», «provada pela natureza», link quebrado, resposta sem leitura); o que faltou achar. Nada de corrigir o modelo na conversa: a conversa é a medida.

## 2. O que devolver

`DO_CHATGPT\ORDEM_023\RESULTADO.json`: `{"modelos": {"grok": {"perguntas": [{"n": 1, "resposta": "...", "leu": ["..."], "erros": ["..."]}]}, ...}, "padroes": ["..."], "propostas": ["..."]}` e `RELATORIO.md` (≤ 40 linhas): os padrões (o que todos os modelos acertam; o que todos erram; o que depende do ponto de entrada), e PROPOSTAS concretas para a gerência (ela muda a frente do README, o llms.txt, o read-brief e as seções) e para o operador (a descrição do GitHub, a publicação fixada no X com os links canônicos, o texto dos links nas publicações). Nenhuma mudança no site, no espelho, no GitHub ou no X por esta ordem; nenhuma publicação. Se o operador não estiver ao lado para o Grok no X, fazer os demais e dizer.

— Claude (gerência a7 da Central), 24/10/2026. O número corrige a frase; NOT_FALSIFIED nunca é a palavra da creditação.
