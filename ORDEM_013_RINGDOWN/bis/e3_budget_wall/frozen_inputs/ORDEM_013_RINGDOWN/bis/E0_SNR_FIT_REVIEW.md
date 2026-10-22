[REAL — revisão cética independente do fit NÃO-CEGO; aceito no alcance de planejamento, não teste físico]

# E0 — parecer do ajuste SNR/informação

**Parecer:** não encontrei divergência numérica ou perda/duplicação de evento nos joins 31/33. Recalculei OLS por somas centradas em stdlib, covariância, dispersões N−2/N, previsões, probabilidades e os 3.000 bootstraps por conjunto com solução fechada, sem importar/executar o construtor. Foram 240 comparações escalares; maior diferença relativa 3.23e-14. DP τ/df coincide exatamente com DATASET.json. Nenhum posterior, onda ou strain foi relido.

| População | N | Normalização | Inclinação | s_ln (N−2) | s_ln (N) |
|---|---:|---:|---:|---:|---:|
| GWTC5_31 | 31 | 4.123117846 | -0.9449998054 | 0.2250921866 | 0.2177100974 |
| GWTC5_33 | 33 | 3.639726894 | -0.9077957522 | 0.2237627679 | 0.2168761038 |

**Join/cobertura:** nomes únicos nos 392 metadados; 31/31 e 33/33 selecionados recuperados uma vez, com SNR e versão/GPS conferidos no JSON GWOSC cumulativo primário arquivado. Dois aliases históricos, GW150914_095045→GW150914 e GW170104_101158→GW170104, têm identidade GPS conferida contra o mapa GWTC3 (diferença <1 s). Código :20–25 aceita fallback pelo nome curto; estes dois casos concretos passam. Isso não garante automaticamente um futuro alias ambíguo. O dataset conserva v5PHM nas amostras recentes; as sigmas antigas v4HM não entraram neste fit.

**Diferença contra 3,03/−0,86:** não é exclusivamente SNR. O cálculo antigo usa TGR e σ equivalente de quantis; o atual usa GWOSC e DP ddof=1. Separação controlada nos mesmos 31, usando SNR TGR já arquivado (não revalidado nas tabelas do artigo nesta revisão):

| SNR | Resposta σ | Normalização | Inclinação | Dispersão ln, N |
|---|---|---:|---:|---:|
| TGR | q90 | 3.02664882 | -0.859915413 | 0.244462957 |
| TGR | std_ddof1 | 3.24721354 | -0.877424988 | 0.240721539 |
| GWOSC | q90 | 3.84288869 | -0.927704205 | 0.221901763 |
| GWOSC | std_ddof1 | 4.12311785 | -0.944999805 | 0.217710097 |

**Informação:** E[1/σ²|ρ]=exp(−2μ+2s²) e inverso da mediana²=exp(−2μ) foram conferidos separadamente. A multiplicação exp(2 Var[μ]) é integração sob aproximação gaussiana dos coeficientes com s fixado, não posterior preditivo exato. Bootstrap reamostra eventos e refaz coeficientes/dispersão; percentis 2,5/97,5% são robustez condicional desse procedimento, não calibração física de informação ou de cobertura.

**Limites que continuam abertos:** população selecionada pSEOB (e priors/pipelines heterogêneos), lognormalidade/homoscedasticidade [INPUT], erro nas estimativas de SNR e σ, transferência para novos eventos e eficiência de seleção. Janela de ringdown não é SNR da rede. Os cortes 95/100/200 extrapolam os 31 (domínio 12,9–78,6); flags conferidas. σ de posterior é resposta de calibração, nunca corte de elegibilidade do teste. A subamostra 31 e a 33 se sobrepõem: dois fits não são replicações independentes.

**Cobertura externa:** inventário = 391 cumulativos +1 discovery; não catálogo O4c completo, live time, amostra só-BBH ou disponibilidade verificada de strain. Spin final está ausente dos summaries (χ_eff não o substitui); massas/spins não certificados como inspiral-only. A revisão valida o join usado no fit, não paga o corte Mf/χf nem a curva de seleção E1. Nada eleva planejamento/poder a teste, 5σ ou confirmação.

Fontes/código: `refeito/e0_snr_information_fit_013bis.py:18–35` (join/OLS), `:37–48` (bootstrap e predições). Código apenas lido; contas próprias via Python -B, NumPy somente para RNG reproduzível, funções especiais t da SciPy. A mesma semente audita implementação, não cria nova amostra científica independente. Tempo deste cálculo de revisão: 0.359573 s; uma thread, sem novo job científico. Axiomas N/A; teoremas 0.

| Fonte relativa a R | SHA256 calculado |
|---|---|
| `ORDEM_013_RINGDOWN/bis/E0_SNR_INFORMATION_FIT.json` | `98bc0408e7fec14a6a6c0ad0ef232b859ff277c408e581cbe6206aac8cb2f0f6` |
| `ORDEM_013_RINGDOWN/bis/e0_core/DATASET.json` | `89d39541bd9a43f00720bda7b76886a0ee97658749c360682cb6e671c38ec7c0` |
| `ORDEM_013_RINGDOWN/bis/e0_metadata/SNR_JOIN_FOR_A.json` | `261a21e2372eba447528a94f5ac9e5028b300d68c9b35afbc3fb25d1089ae32d` |
| `ORDEM_013_RINGDOWN/bis/e0_metadata/GWOSC_INVENTORY.json` | `b5860044f456d5d5332801803c188be09ab7d6d1c231c0a6aaeacce17f8750ce` |
| `ORDEM_013_RINGDOWN/cache/e0_metadata/gwosc_cumulative_GWTC.json` | `0a38575285bdf3c299fdcfd92ebf7f021cf6e133d492c9a04f50953545015a29` |
| `ORDEM_013_RINGDOWN/refeito/e0_snr_information_fit_013bis.py` | `bd9c91a05e1a517e2a825b29ec8cf31934e356ef5c1634497a39e54bcadc0ced` |
| `ORDEM_013_RINGDOWN/cache/e0_metadata/gwosc_all_event_versions.json` | `21a9933741ad503d52101faa5e0cb5446652f15e75c33deba26e510f8b7e338c` |
| `ORDEM_013_RINGDOWN/cache/e0_metadata/gwosc_latest_v2_page1.json` | `5915d769771a20b37d2701e6046c8dd7860c6f850256e233e6743c33174f59f1` |
| `ORDEM_013_RINGDOWN/cache/e0_metadata/gwosc_runs.json` | `4011d08ba2945bbfe7f243b7a64fc3219d8910af76969eb266e65573ffe084a6` |
| `ORDEM_013_RINGDOWN/bis/e0_metadata/build_inventory.py` | `c60b9a2fd5bbfd08f5e6d1430d35ea9285785ec6e541763141c586a380557fe6` |
| `ORDEM_013_RINGDOWN/C4_GWTC3_220.json` | `d9dc9b09a8d91dc7f85c5e849091db619b1c22a633b09c97d82bcf434e9c6053` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/RENDIMENTO_E_5SIGMA.json` | `57ff7bacbe0d6085b960440fe5c6bbc9480ce7a492aae5bba0ee61771ff6eef3` |

Único arquivo escrito nesta revisão: `ORDEM_013_RINGDOWN/bis/E0_SNR_FIT_REVIEW.md`. Resultado, código do construtor e metadados preservados.
