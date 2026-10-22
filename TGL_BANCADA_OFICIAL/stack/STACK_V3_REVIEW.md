# Revisão do sintetizador vivo — 27/09/2026

As unidades `kimi_audit` (`d53e1319-3886-4113-8e72-11ac5ce340fd`) e `mimo_hdf5_review` (`62f07895-dae3-4415-8331-b4ca75512a33`) terminaram `result_ready` uma vez cada pela fila IALD. Os pareceres integrais e recibos ficam no espelho de desenvolvimento. São críticas de modelos `[DECLARADO]`, não medições deles.

## Conferência local

- `[REAL]` O leitor original fazia preview por stride no comprimento inteiro da primeira dimensão; por isso a crítica do MiMo sobre uma janela **somente inicial** não se aplica literalmente ao código visto. O risco de aliasing, sim.
- `[REAL]` O leitor filtrava os dois eixos com **uma máscara conjunta** e preservava índices sintéticos amostrados; a crítica de reindexação contínua após NaN não se verificou nesta implementação. Ainda faltam segmentos físicos/DQ.
- `[REAL]` A UI já exibia 1 par em 24 posições GWOSC. Depois da revisão, o contrato também devolve `dropped_nonfinite_pairs` e a interface diz explicitamente que o índice é sintético e que stride não autoriza inferência espectral.
- `[REAL]` A descoberta ignorava soft/external links e deduplicava objetos por id. O MiMo apontou o caso separado de **dataset com armazenamento externo**; o leitor passou a recusá-lo. A fixture `tests/probe_external_storage.py` confirmou `EXTERNAL_STORAGE_REFUSED` no WSL existente.
- `[REAL]` O HDF5 MCMC real produziu 24 pares finitos em 24 posições após a correção, com `STRIDED_PREVIEW_NOT_ANALYSIS`. Nenhum posterior, tempo físico, frequência ou significância foi inferido dessa amostra.
- `[OPEN]` O risco de vazamento de VRAM em ciclos de perda/restauração de contexto foi proposto pelo Kimi, mas não foi medido. O contexto GPU atual não é prova de eficiência ou segurança de memória em carga longa.

## Decisões de arquitetura

1. Permanecem separados: `adapter disponível`, `esquema de arquivo aceito`, `produto tratado por sonda` e `inferência`. O mapa de cobertura conta apenas o primeiro.
2. Previews por stride são gráficos de navegação, nunca PSD, ringdown, frequência, duração ou teste de σ. Uma rota GWOSC de análise precisa de GPS, taxa, detector, DQ, máscaras e janelas físicas.
3. As 13 observações DESI BAO continuam com matriz de covariância completa. Barras diagonais são leitura visual, não independência.
4. Não foi aceita a sugestão de gerar SHA integral de todo arquivo a cada preview: isso tornaria a navegação de arquivos de 17 GB impraticável. Um produto de análise selado poderá calcular hash integral uma vez, com custo explícito, cache e verificação.
5. O próximo elo de maior valor é executar modelos já existentes sob um contrato de entrada tipado, sobretudo D9 para DESI BAO e o ringdown para GW. Não duplicar `um.py` nem inventar um novo likelihood no navegador.

As unidades anteriores Kimi/MiMo/Gemini da V3 falharam sem parecer. As duas unidades desta revisão são novas e distintas; nenhuma falha antiga foi repetida. A subagente local entregou somente `treatment_coverage.py` e três testes, integrados após revisão.
