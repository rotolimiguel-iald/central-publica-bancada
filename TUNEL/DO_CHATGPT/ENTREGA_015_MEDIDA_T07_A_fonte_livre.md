[REAL — medição local; OPEN — z_free e inferência física]

# ORDEM 015, T07(a): busca de fonte livre

Quatro leituras concluíram com rc 0 e candidatos finitos. Nenhuma das oito etapas Powell convergiu: todas atingiram maxfev. O valor é a norma residual de um candidato a=0 contra o alvo a=1 na fonte registrada, SEOBNRv4HM/O4/SNR40; é limite superior construtivo do mínimo global do objetivo numérico, não limite inferior, z calibrado, exclusão de GR ou σ. O controle a=0/a=0 é na mesma fonte e está ao quadrado; não se compara diretamente às normas da tabela.

| Leitura | Norma 8192 | Norma 16384 | Avaliações | Convergência | SHA256 resultado |
|---|---:|---:|---:|---|---|
| R-B | 0.321177439 | 0.320747091 | 501 | NÃO | `2d69a66b7082b9ee316197bcbe4577a972574f4e1f8cc850a2442f48ee803aff` |
| R-MOD | 0.577924314 | 0.57775042 | 501 | NÃO | `be5aee6dd3e8cca7735d0a88a47cb03668fbf1e4849d80253dd0456818fdfb31` |
| R-RAIZ-0 | 0.589593286 | 0.590616033 | 501 | NÃO | `ec5c22d8fc545a48b3ab54c372930bd9f2798e491420c0240616412e67083800` |
| R-LIN | 1.13754572 | 1.13622156 | 501 | NÃO | `5eaf8bbc0c8804b79678abe146511923998c92b72da08e5047c839c5a2d4a4dd` |

Tempo de máquina conservador: 0.413100 h, do recibo de início ao último arquivo. Log `T07_RUN_v2.log`: `79bb2c0b6e94a6e70f392e186c8aeb1f380c408e09b8d192e04bf24464513f47`. Runner: `610e8ecebf180570702e86227bac71acf4755502a5f48874257d98d3af928f38`. Registro: `d0a2b5013a892d63cd8e083b8a5956c2ca378f8680ce12a967887fb8f6089110`. JSON consolidado: `aa14a98646428fb0d6531df2f745097828d895cfab16ff2ae8657bb5cc9b103e`.

O teto de uma hora foi respeitado por controle externo de timeout. O hash do runner foi conferido depois da execução. O revisor Kimi fez análise estática do texto apresentado; seu parecer não executa nem prova o cálculo. Sem T07(b), a tabela de ρ dos eventos de calibração e o N₉₀ recalculado continuam pendentes. Gate inalterado.
