# CÉTICO 1 — achado da lente regua_hashes_casa sobre L129 / L159 (citação «may favor…» do GWTC-5.0)

Veredito: **NÃO REFUTADO** (refutado=false). Gravidade mantida: **IMPORTANTE**.

## Refeito por script (22/09/2026, sha256sum | cut -c1-16; stat -c%s)
| arquivo | sha16 | bytes | `grep -c 'may favor'` |
|---|---|---|---|
| `Chatgpt\ORDEM_013_RINGDOWN\cache\literature\gwtc5_tgr_abstract.html` (bancada, só leitura) | `542a5b672c33e586` | 348.283 | **0** |
| `bis\medir\B_catalogos\gwtc5_tgr.txt` = `ORDEM_013BIS_INSUMOS\medicao_da_ampliacao\B_catalogos\gwtc5_tgr.txt` | `d523ae94f23f40b5` | 248.915 | 1 (L4656–4657, dentro da Seção 7.2 «The pSEOBNR analysis», subseção hierárquica; L4654–4658: «selection effects are not accounted for in the current hierarchical inference. For example, the pSEOBNR selection criteria may favor events with positive damping time deviations, as these tend to have a larger ringdown SNR…») |
| `…\B_catalogos\arxiv_2607.19293_gwtc5_tgr.pdf` (idem nos dois lugares) | `4ab5df879daa2f4a` | 1.894.358 | — (PDF; o `.txt` é extração dele, `FONTES.json` L4–7) |
| `FRENTE_B_RESULTADO.md` L6 | `5234a28dd15cea04` (MANIFESTO_B) | 8.615 | cita a frase como `[REAL — lido do PDF e do release]` |
| `cache\literature\gwtc3_article_v3.html` (sha citado na L129 para o GWTC-3) | `9c5271fba4aaa144` | 2.702.327 | confere |

Os sha16/bytes do achado coincidem com os medidos. A ordem (`grep -n "gwtc5\|2607.19293"`) só menciona a fonte nas L129 e L159; a §7 (tabela de insumos) não lista nem o `.txt` nem o PDF; a L277 nomeia `medicao_da_ampliacao\` só por pasta. Logo:
1. L129 cita uma frase `[KNOWN]` sem dizer de que arquivo/sha a gerência a leu — viola a convenção da própria ordem («cada número com fonte e sha16», L143) e a régua (hash lido do artefato, nunca de memória).
2. L159 «hoje só o abstract está em cache» é literalmente verdadeira para o cache da bancada, mas omite que o integral (PDF + extração) já viaja nos insumos da 013-bis com sha — a bancada pode ler que precisa baixar de novo ou que o integral não existe na casa, e pode até rebaixar a citação a «não conferida».

Por que não BLOQUEANTE: a citação existe e é exata; a bancada consegue obter o integral (arXiv:2607.19293) sozinha; não há erro de física, número fabricado nem decisão do operador. Por que não NOTA: é citação sem localização/sha, exatamente o tipo de buraco que a régua manda deixar dito.

## Correção FINAL (texto exato)
Ver campo `correcao_ajustada` do StructuredOutput (reproduzido abaixo).
