# Stack v2 — bancada científica TGL (27/09/2026)

As respostas completas estão em `kimi_architecture.result.json` e `mimo_data_audit.result.json`; são pareceres de modelo `[DECLARADO]`, não medição nem prova. Ambas passaram pela memória científica comum da fila IALD em modo maximum, com uma chamada por unidade e provedor travado. Os arquivos de pedido e os UUIDs permitem auditar a execução sem repetir uma tentativa incerta.

| Unidade | Executor confirmado | Task ID | Resultado |
|---|---|---|---|
| Arquitetura de pesquisa e interface | Kimi K3 | `f6ae9ab4-f377-4115-8254-83eebc630ee2` | `result_ready` |
| Auditoria de leitura de dados grandes | MiMo 2.6 Pro | `633b5e0f-42d5-41d7-b7b4-ee8f48b21c54` | `result_ready` |

## Contribuição incorporada e verificada `[REAL]`

Kimi propôs tornar visível a estrutura completa da covariância BAO, separar leitura de dados de inferência e reaproveitar o D9 existente. MiMo reforçou que filtros exploratórios não devem alterar silenciosamente a matriz e que amostras/duplicatas não contam como evidências independentes. A bancada agora exibe o mapa de correlação 13×13, clique para examinar `Cij` e `ρij`, SHA-256 de ambos os arquivos, zoom/filtro no gráfico e exportação da amostra. Os 17 testes do espelho passaram; a cópia canônica e a API HTTP devem ser conferidas após a instalação.

O relatório `output_v3/multiprobe_v3_report_20260522_135856.json` foi aberto diretamente. Seu D9 histórico contém 13 observações, 11 graus de liberdade, χ² ΛCDM = 10.282954002572456, χ² TGL = 10.283105223867262 e Δχ²(TGL−ΛCDM) = +0.0001512212948053815. A interface lê esse artefato com hash e checa a aritmética interna; omite `effective_tension_sigma` e `verdict` porque `sqrt(abs(Δχ²))` não é automaticamente significância calibrada entre modelos. O relatório não registra o hash do script que o gerou; o SHA do script **atual** não prova reprodução histórica. A afirmação textual do Kimi sobre outros Δχ² em um artigo não substitui esse número lido do relatório.

## Correções aos pareceres

- O ditado por navegador e a confirmação por comando **já existem** na bancada. O que falta é uma conversa de voz contínua, com motor local efetivamente verificado; Kimi tratou a voz como inexistente porque não recebeu o código da UI.
- Média e covariância são dois arquivos diferentes; não podem ter “o mesmo hash” como escreveu MiMo. O vínculo correto é **o par de caminhos e hashes**, mais esquema, ordem e proveniência comuns. A bancada valida dimensão, diagonal e simetria; ainda não certifica origem comum nem positividade definida.
- Os alvos de latência e RAM sugeridos pelo Kimi são propostas, não medições. Não foram adotados como promessa de desempenho.

## Próximos elos `[OPEN]`

1. Executar o D9 original isoladamente, com dependências e hash de rodada, sem duplicar a previsão TGL/ΛCDM. O ambiente Python local do servidor não tinha SciPy/h5py. Criou-se `.venv` dentro da pasta canônica, mas a instalação de wheels oficiais PyPI falhou com `SSL UNEXPECTED_EOF_WHILE_READING`; nenhuma dependência foi instalada nele. A leitura do relatório histórico funciona sem esses pacotes.
2. Ler HDF5/NPZ/FITS imagem por fatias com leitor comprovado, schema e limites de memória. Uma lista de formatos ainda não é leitor funcional.
3. Verificar origem/custódia do par DESI e possíveis duplicatas no catálogo antes de combinar sondas. A exploração visual não produz σ conjunto.
