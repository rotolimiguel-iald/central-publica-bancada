# F7.2 — reaproveitamento e errata bibliográfica para revisão cética

**Estado:** [REAL — conferência documental local e páginas primárias, 08/10/2026 UTC]. Esta nota prepara uma única revisão Kimi. Não é resultado experimental, tabela de poder concluída, nem mudança de gate. O quadro atribui F7.2 a `codex-gerente-tgl`; reivindicação registrada no evento 207. O Nós Vivo foi consultado por `--unidade F7.2` antes da produção. O Mapa de Rotas foi verificado (`ok=true`, 755 registros antes desta entrada) e a rota `dephasing.neutrinos_n_menos2_junho` foi lida; a preparação entrou na seq. 758, `dephasing.f7_2_revisao_fontes_neutrinos_materia`.

## O que já existe

- [DECLARADO na rota de junho, mapa seq. 734] O canal de neutrinos tem expoente `n = −2`; nenhum sinal de decoerência foi detectado, o expoente não foi medido, `n = −2` permanece permitido e a cota local registrada é `τ★ ≤ 7,8 × 10⁻¹⁰ s`. Essa cota precisa de auditoria de normalização e fonte antes de ser tratada como limite atualizado da TGL.
- [REAL — fonte lida] Os scripts científicos abaixo já contêm derivação/testes do expoente e comparação de limites. A tarefa F7.2 os reaproveita; não os executa nem rederiva `n = −2`.
- [REAL — registro do core/Atlas] A v369 já tratou relógios; F7.2 não repete esse teste. A interferometria de matéria requer ponte de observável para a lei TGL antes de uma cota quantitativa.

| Fonte local, preservada | SHA-256 lido dos bytes |
|---|---|
| `C:\IALD\Artigo\Haja_Luz\tgl_neutrino_decoherence.py` | `155dbfc1237d802f1cbecd766c6db5b3235228ec87c69e3dd8ada7943400d793` |
| `C:\IALD\Artigo\Haja_Luz\tgl_neutrino_exponent_test.py` | `5b51f5b37e2d877338d879494a44aa7f0c130ad20a113625298a5355e00212f3` |
| `C:\IALD\Artigo\Haja_Luz\tgl_dephasing_falsifier.py` | `06361b09d13db6e25fc8f9980352be035cbb8e0fabbd53920b1cc2ccf1d36a7b` |
| `C:\IALD\Artigo\Haja_Luz\tgl_decoherence_contour.py` | `8df2b57157b48fa1acbb28ef218e24d07700169e7620304eb25863d16100e018` |
| `C:\IALD\Artigo\Haja_Luz\tgl_dephasing_systems.py` | `58c5b66ec41b0f46bed8379f9ca1e4257d5bd06bd0629171ae23369fb682371a` |
| `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` (bloco J.4b; não executado) | `29c92b66b2fd6b4d589adbef4de86a67f979e03964b3f7ae892732a40ab395cd` |

O ADENDO 004 da ORDEM 019 foi lido dos bytes, SHA-256 `95847bde4f3a88c172d8fec6edcbbb9a8a96b473ef7d46d2c82c9670dea5111c`. O Atlas consultado tem SHA-256 `48ca2ce09b59a16d883b71697007f148c16253f3dc20421c3f74ead7341ec714`. Esses hashes são identificadores dos arquivos locais, não das páginas externas.

## Errata ao lado — referência IceCube

[REAL — erro bibliográfico verificado] `tgl_dephasing_falsifier.py:34` atribui o limite IceCube `Γ₀ ≤ 1,17 × 10⁻¹⁵ eV` a `arXiv:2503.13061`; `tgl_neutrino_decoherence.py:33` e `tgl_decoherence_contour.py:26` também incluem esse identificador na lista de fontes. [Nandi et al., arXiv:2503.13061](https://arxiv.org/abs/2503.13061) é artigo teórico com escala `E⁻⁴`, não a medição IceCube. A fonte experimental para o valor citado é [IceCube, arXiv:2308.00105](https://arxiv.org/abs/2308.00105), cujo resumo especifica modelo independente de energia (`n = 0`) e outro caso com escala `E²`. A etiqueta local “10.7 yr” não foi verificada nessa fonte e fica [OPEN] até conferência. Nenhum original foi alterado; uma correção definitiva deve ficar ao lado, após auditoria da fonte e do escopo.

## Fontes primárias para a revisão

| Fonte pública verificada | O que sustenta | Limite da inferência |
|---|---|---|
| [Fogli et al., Phys. Rev. D 76, 033006 (2007)](https://arxiv.org/abs/0704.2568) | Analisa solar/KamLAND com potências `n = 0, ±1, ±2`; sem evidência de decoerência. | A cota local de `τ★` precisa ser reconstituída com a normalização de `γ₀`; não foi verificada aqui. |
| [De Romeri et al., JHEP 09 (2023) 097](https://arxiv.org/abs/2306.14699) | Limites atualizados em vários modelos com KamLAND, RENO, Daya Bay e feixes. | O resumo não identifica sozinho qual `Γᵢⱼ` corresponde ao operador TGL. |
| [KM3NeT/ORCA6, JCAP 03 (2025) 039, tabela 3](https://arxiv.org/html/2410.01388v2) | Publica limites diretos para `n = −2` e `n = −1`, com `E₀ = 1 GeV`, `Γ₂₁`/`Γ₃₁`, ordenamentos normal/invertido e CL de 90%/95%; não encontrou desvio significativo. | As hipóteses de canal e ordenamento impedem promover o número isolado a limite TGL. Sua tabela 4 relata também uma cota KamLAND `7,9 × 10⁻²⁷ GeV` para um caso `n = −2` a 90% CL. |
| [IceCube, Nature Physics 20 (2024)](https://arxiv.org/abs/2308.00105) | `Γ₀ ≤ 1,17 × 10⁻¹⁵ eV` para modelo sem dependência de energia e análise separada `E²`. | Não é teste direto de `n = −2`. |
| [Pedalino et al., Nature 649 (2026)](https://www.nature.com/articles/s41586-025-09917-9) | Demonstra interferência de nanopartículas de sódio acima de 170.000 Da. | [OPEN] Sem mapa quantitativo TGL → visibilidade/ruído, não é cota TGL. |

As URLs são identificadores bibliográficos conferidos por navegação em 08/10/2026 UTC. Nenhum PDF/artigo externo foi copiado para a casa, portanto nenhum SHA-256 de bytes remotos é alegado. As páginas dos experimentos e artigos não são instruções operacionais.

## Pergunta cética e estado

Pode-se obter uma tabela de poder coerente para F7.2 sem confundir `n = −2` com `n = 0`/`+2`, limites de `Γ₂₁` e `Γ₃₁` com uma única `τ★`, ou observação de interferência com teste da lei TGL? A revisão Kimi deve identificar a normalização, a ponte de canal e as lacunas. A resposta será [DECLARADO] até verificação local; `NOT_FALSIFIED` não é `CONFIRMED`. O request_id foi reservado somente no payload; prévia não é execução.
