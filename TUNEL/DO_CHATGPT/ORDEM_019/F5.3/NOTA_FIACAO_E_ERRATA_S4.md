# F5.3 — fiação documental do Nível 2 e errata ao lado do ramo CMB-S4

**Estatuto:** `[REAL — leitura de bytes e dos termos documentais]`; sem rodada científica nova. A unidade permanece `BLOQUEADA`. Este arquivo liga fontes existentes por caminho e SHA-256; não altera o pré-registro congelado, o V1 da Fase 8, a Bancada, o `um.py` ou o gate.

## O que o Nós Vivo e o mapa já tinham

O Nós Vivo lista a rota `cmb.nivel2_mcmc`, que registra o CAMB com os fechamentos S e L, e `core.nivel2_rite` com `all_verified=False`. O mapa já contém `cmb.nivel2_mcmc` (`EXAMINADA`) e `cmb.fisher_gates_e_prereg_so_s4_14ago` (`EXAMINADA`). A auditoria canônica de 28/09 distingue o Nível 2 S/L do solver V3 e deixa a escolha do fechamento perturbativo aberta. Nenhum desses elementos foi reexecutado aqui.

## Ligações que o pacote fixa

| Origem existente | Destino existente | Relação comprovada | Limite |
|---|---|---|---|
| `TGL_NIVEL2_V1` (pin interno `664fc4cf9dd245ec15fb76aa70c5330e07c658e418e0dcf6108858b646a40c34`) e resultado canônico de agosto | Fase 8 V1, `/spec/decisoes_padrao_da_gerencia/D11` e `/spec/mapas/A_N2` | O V1 já identifica o frozen original como canônico, a cópia do Nós como continuação e o Nível 2 S como diagnóstico. | O resultado canônico e a continuação do Nós têm SHA-256 de arquivo diferentes; não transportar seus números como se fossem a mesma rodada. |
| `TGL_NIVEL2_SO_S4_V1` (pin interno `92c67c5c41fa4e49d0380fd320e966d101ab0445fe09db6ad923069371cdf246`; arquivo `so_s4_prereg` na tabela abaixo) | Fase 8 V1, `/spec/futuro_declarado/CMB_S4`, e Bancada `bancada/neff_canal.py` | Este pacote dá ao pré-registro de 14/08 uma remissão direta e versionada à Fase 8 e ao canal N_eff já pinado nela. | O identificador literal aparece **zero** vezes no JSON/MD do V1, no `um.py` e no módulo da Bancada. A fiação é documental aqui; nenhum consumidor runtime do pré-registro foi instalado. |
| Pré-registro SO/S4 e gates de Fisher | Rota `cmb.fisher_gates_e_prereg_so_s4_14ago` | O arquivo congelado prevê σ/β = 0.50 para SO-like e 0.31 para S4-like; Planck+ACT otimista fica em 0.51. | Projeções *like* não são vereditos de observação nem garantias de poder futuro. |

O resultado **canônico** de agosto mede S convergente, `N2_INCAPAZ`, σ/β = 1.467; L registra `N2_NOT_CONVERGED`, σ/β = 1.256. A análise de 14/08 manda não estender a cadeia L: ambas as razões excedem 1, mas o veredito formal de L continua `N2_NOT_CONVERGED`. A degenerescência radiativa `N_eff ↔ H₀` é a causa indicada. `[OPEN]` A escolha/derivação do fechamento perturbativo S × L × fluido total V3 continua teórica; este índice não a decide.

## Errata histórica ao lado — CMB-S4

Ao lado da frase de 14/08 `ESPERAR_SO_OU_S4`: **o ramo S4-like permanece no frozen como cenário de poder histórico**, σ/β = 0.31; não funciona como calendário ativo de obtenção de dados. O ADENDO 004 da gerência e a própria Fase 8 V1 (`/spec/futuro_declarado/CMB_S4`) registram o encerramento CMB-S4 como `[DECLARADO]`. A rota SO-like permanece expectativa condicionada à disponibilidade real do dado e às condições do pré-registro. O frozen `TGL_NIVEL2_SO_S4_V1` não foi reescrito.

## Fontes conferidas em bytes

| Papel | Caminho absoluto | Bytes | SHA-256 |
|---|---|---:|---|
| adendo004 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_019_ADENDO_004_correcoes_do_critico.md` | 6079 | `95847bde4f3a88c172d8fec6edcbbb9a8a96b473ef7d46d2c82c9670dea5111c` |
| nivel2_frozen_worker | `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\12_nivel2_frozen_e_verossimilhanca.py` | 13246 | `e788b8cd7458c20c052c488340bb9ff7f984fc97b5fa09ac8fec6e913b19352b` |
| nivel2_result_canonical | `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_resultado.json` | 4205 | `d3c09d15dfe65a531caf6c096cb429bd27b99cf21263c00c29bf7d41a399336f` |
| nivel2_chain_canonical | `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_chains.h5` | 51839136 | `af118c94a693ac3c429e3a33d585b64a857b5a86108d69e2eb7875d0cba729c8` |
| nivel2_analysis | `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\14_ANALISE_NIVEL2_FECHADO.md` | 3858 | `26c9cc4499a8a40aaddd08a34f17272cb9972d93523074e7c5495494498ec030` |
| nivel2_result_nos_continuation | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\nivel2_mcmc\13_nivel2_resultado.json` | 4214 | `5580f7e45b06c3fcd2cfb7e011d90dedd49d7df4f1bd3882fbf7bbb22f62225b` |
| so_s4_prereg | `C:\IALD\Artigo\MCMC_V2_RAZAO\22_prereg_SO_S4.json` | 6467 | `5dbb7a7ed31e1a6518031eb717ecc0baf61fe72ec9969f4dc6afde2b489d3856` |
| fisher_verdict | `C:\IALD\Artigo\MCMC_V2_RAZAO\VEREDITO_DO_PLANEJAMENTO.md` | 4204 | `ce19047de4bb1e2d25b5cafdfee469ecc66db7edfcbf643fb184acdce164017b` |
| fisher_power_map | `C:\IALD\Artigo\MCMC_V2_RAZAO\MAPA_DE_PODER.md` | 3507 | `2ba5bb4e15fad8ae7b2f114191ff94f859f21f2952b4f068ee9a8db3ee66e087` |
| fase8_v1_json | `C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json` | 17864 | `36afd8b05d2aa5f57b7f29e9dd64b83530b43b12a76707e6db3a99bc111f8397` |
| fase8_v1_md | `C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.md` | 11048 | `f53fa9654846145650a37fcbe1b194434743b41f4ac20fbe03cc3403d148edd6` |
| fase8_hashes | `C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\V1_FASE8_HASHES.json` | 2078 | `579d797695f1dfd63f1b5e2c03c6454246f04732282b3bd903cf53f87e60b5ea` |
| bancada_neff | `C:\IALD\Bancada_Um\bancada\neff_canal.py` | 6059 | `42e9b680855c33004938aacb0899bf0f4ce1921705b04bd93d13ff150ba7541b` |
| cosmology_audit | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\COSMOLOGY_CANONICAL_ROUTE_AUDIT.md` | 8871 | `47aeb85037a78c07705dfec3513464e7597fbdf057a8cd882e3131d00a6b440a` |
| um_py | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | 33910631 | `8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6` |

O pin interno do frozen SO/S4 (`92c67c5c41fa4e49d0380fd320e966d101ab0445fe09db6ad923069371cdf246`) é distinto do SHA-256 do próprio arquivo; ambos constam no manifesto `VINCULO_DOCUMENTAL_SO_S4.json`. O V1 da Fase 8 mantém seu pin de especificação `790954c7bc9dc13aa844c8ddff027e5535c1be2ba19f4753ca05e0edafc8b11b`. O código `ALPHA_FINE_CODATA_2018 × √e` permanece a forma de β em runtime. Nenhum dado observacional novo foi aberto; a cadeia MCMC foi lida apenas para SHA-256, sem análise ou execução. Não houve CAMB, teste de natureza, instalação ou publicação.

## Ressalva transversal F5.2 — CMB-SPA

A remissão ao V1 da Fase 8 é documental e não valida todos os números desse V1. A aferição F5.2 em `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F5.2\TABELA_NEFF_FONTE_HASH.md` (SHA-256 `d5415ec84af2a3916d902cf74649a8a78610a29edd353c57c73e76795bc9bce9`) identificou que a linha CMB-SPA `2,97 ± 0,12` atribuída a arXiv:2506.20707 não corresponde às versões v1/v2 consultadas. Não transportar aquela linha nem suas tensões derivadas para esta fiação; a correção do rito requer pin de versão e auditoria própria. Esta ressalva não altera o pré-registro SO/S4, seus gates de Fisher nem o estado `BLOQUEADA` da F5.3.
