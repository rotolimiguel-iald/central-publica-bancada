# Revisão da procedência GR — RASCUNHO PARA DECISÃO

[REAL documental; critério INPUT NÃO REGISTRADO; não é entrega nem seleção aprovada]

**A tabela fornece Mf e chi_f da análise padrão GR do catálogo, anterior ao ajuste de deformações.** §2 do [TGR](https://arxiv.org/abs/2607.19293), pp3–4, atribui essas propriedades à PE dos catálogos; o [catálogo primário, §3 p12](https://dcc.ligo.org/public/0206/P2600152/006/gwtc-5_results_noauthors_flattened.pdf) descreve a inferência IMR padrão como baseline para os testes de GR e identifica modelos/prior/resumos. Isso sustenta procedência **GR full-IMR**, não inspiral-only nem independência estatística do mesmo strain. Não são massas/spins obtidos deixando δτ livre. Leitura limitada às seções/tabelas indicadas.

Extraí diretamente do PDF as 77 linhas das Tabelas2–3 e comparei quatro medianas por linha: **308/308 coincidem** com o JSON recebido. São 72 eventos O4b e cinco O4a adicionais, não o catálogo inteiro. `Mf_det` é massa **final redshifted**, em Msol; `chif` é spin final adimensional. Atenção: `Mdet` no JSON antigo é **massa de chirp redshifted**, não massa total. GW250114: Mf_det=68,31 e chi_f=0,68; SNR da tabela76,9 fica só na proveniência, enquanto o corte continua com GWOSC78,6.

Sem adotar o critério, fiz apenas uma tabela de impacto do INPUT proposto: SNR≥12, mediana Mf_det≥40, 0≤mediana chi_f<0,98; prioridade SNR≥30. Não há uso de larguraδ ou de chi_eff como substituto. Toda ausência recebe `AWAITING_GR_METADATA` e decisão null. `adopted_eligibility` é null em todas as linhas.

| corrida | SNR≥12 | com GR Mf/chi_f | aguardando | atenderia INPUT | não atenderia, valores conhecidos |
|---|---:|---:|---:|---:|---:|
| O1 | 2 | 0 | 2 | 0 | 0 |
| O2 | 7 | 0 | 7 | 0 | 0 |
| O3a | 21 | 0 | 21 | 0 | 0 |
| O3b | 10 | 0 | 10 | 0 | 0 |
| O4a | 28 | 0 | 28 | 0 | 0 |
| O4b | 45 | 44 | 1 | 27 | 17 |
| O4c_discovery_only | 1 | 0 | 1 | 0 | 0 |
| O4_public_total | 74 | 44 | 30 | 27 | 17 |

**A cobertura continua incompleta**, sobretudo para O4a antigo e a discovery O4c. Uma linha ausente da tabela TGR não falha física nem passa o corte. A própria tabela tem seleção para testes; sua disponibilidade não pode virar automaticamente seleção científica adicional. Intervalos publicados podem atravessar Mf=40 (p.ex. GW240428_225440: 38,27 +2,82/−0,93). A convenção por mediana foi apenas simulada para a decisão proposta; adotar quantil/probabilidade seria outra regra a registrar.

O fit `E0_SNR_INFORMATION_FIT.json`, SHA256 `98bc0408e7fec14a6a6c0ad0ef232b859ff277c408e581cbe6206aac8cb2f0f6`, foi lido: hashes das três fontes e associação SNR por evento conferem; **não refiz OLS/bootstrap nem aprovei o ajuste numericamente**. O campo herdado `convention.sigma_fit_performed=false` descreve o inventário de origem, não a execução do fit; convém contextualizá-lo no registro final.

Complementos documentais: a [documentação GWOSC5](https://gwosc.org/GWTC-5.0/) esclarece que o default de SNR usa PE quando disponível e, sem PE, a maior SNR das buscas. Mantemos uma convenção de catálogo, não um único estimador homogêneo. O catálogo primário, p28, prevê os resultados O4c em GWTC6, **sem data de publicação**. Isso documenta intenção, não lançamento.

O mapeamento por evento, incertezas, contagens e hashes estão no JSON ao lado. O manifesto anterior permanece intacto; as fontes adicionais têm recibos próprios em cache e um manifesto complementar. Nenhum posterior/strain novo, nenhuma alteração de E2, nenhuma publicação de critério.
