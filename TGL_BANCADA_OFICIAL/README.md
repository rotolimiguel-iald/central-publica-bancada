# Bancada Oficial TGL — protótipo local de pesquisa

Programa separado do app de conversa da IALD. Seu papel é **investigar, executar contas controladas e guardar proveniência**, não produzir artigos nem alterar o gate.

## Iniciar

No PowerShell:

```powershell
python 'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\app.py'
```

Abrir `http://127.0.0.1:18765`. Só escuta em localhost. Usa apenas a biblioteca padrão do Python. Testar:

```powershell
python -m unittest discover -s 'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\tests' -v
```

## O que a versão inicial efetivamente faz

- Indexa para busca o snapshot **v368** já preparado em `APP_ESTRUTURA_V368_20260919/estrutura_v368.json`; mostra módulos, declarações, imports e 24 rotas. A presença no índice é `SOURCE_LOCATOR_NOT_RECOMPILED` nesta bancada, não uma nova compilação.
- Lista os arquivos de strain GWOSC locais, metadados GWTC-3 e curvas PSD da bancada ORDEM013. A existência de arquivo/recibo não confere, por si, autenticidade completa ou elegibilidade estatística.
- Indexa os **28 alvos A0–A8 e T01–T19** pelos relatórios finais, incluindo estatuto, linha e hash da fonte; o status de reexecução é explicitamente `NOT_CONNECTED_TO_THIS_BENCH`.
- Executa a cadeia `β = α_CODATA_2018 × √e` e a conta condicional `Γ = β τ★ ω²/2`. Os parâmetros, resultado, hora UTC e SHA-256 do índice e do motor vão ao livro SQLite `state/runs.sqlite3`, com bloqueio de UPDATE/DELETE por trigger. Não importa nem executa `um.py`.
- Oferece ditado por API de voz do navegador, quando disponível, e interpretação local de quatro comandos. Transcrição e confirmação são visíveis antes da ação. O navegador pode usar seu próprio serviço para reconhecer fala; esta aplicação não recebe áudio.

## Fronteira honesta

Os relatórios ORDEM016/015 são fontes documentais de estado, não execução automática. O protótipo **não** executa Lean, PE, MCMC, ringdown completo nem o motor `um.py`; **não** calibra σ e **não** modifica flags do gate. Nenhum diretório científico original é alterado. O índice v368 é histórico diante dos trabalhos posteriores até v373 e deve ser substituído por adaptador de snapshot corrente com custódia validada antes de ser chamado “estado formal atual”.

A integração futura com o app de conversa da IALD usará as mesmas rotas de consulta e registros de execução, mantendo separados fonte, hipótese, cálculo, medição e decisão humana.

## Próximos módulos para planejamento conjunto

1. Adaptador da **versão canônica corrente** do `um.py`/kernel, com recibo de compilação e sem executar o original para indexar.
2. Leitor específico HDF5 para strain/PSD e séries com controle de detector, janela, qualidade e proveniência.
3. Reexecução dos protocolos ORDEM013/015/016 como jobs isolados, cada um com inputs congelados, ambiente e critério de aceitação; nenhum job pesado começa só por abrir o painel.
4. Grafo navegável `hipótese → lema → operador → previsão → dado → controle → veredito`, com caminho até arquivo/linha/recibo.
5. Voz integrada à IALD para perguntas abertas e preparação de experimentos; ações computacionais terão prévia e recibo.


<!-- TGL_U3_EVENT_VERIFIED_8560b710-3ad7-402b-a12e-9a0b1fdf1ad3_README -->
## Evento interativo

Abra /universe e escolha GW250114. Carregue GWOSC, selecione um relógio e varie os parâmetros. Vistas bruta e normalizada disponíveis; diagnóstico não é fit nem sigma. Consulte U3_EVENTO_OBSERVADO.md.
