[DERIVED sobre larguras REAL — NÃO-CEGO; cenário gaussiano, não sensibilidade física calibrada; AGUARDA REVISÃO INDEPENDENTE]

# E0 — poder da rota IV

O limiar é LRT>25. A simulação perfila a média comum nas hipóteses nula e alternativa; a alternativa adiciona variância não negativa. Os sigma de medição são DP amostrais dos posteriores completos existentes (ddof=1), usados somente como aproximação gaussiana para planejamento. A mistura prospectiva sorteia classes de qualidade com probabilidade uniforme entre os eventos existentes; não seleciona eventos de teste pela largura posterior.

O cálculo usa estatísticas suficientes gaussianas por classe: contagens multinomiais, soma normal e soma de quadrados centrados qui-quadrado. Isso permite calcular N grande sem materializar cada observação, com a mesma distribuição. Há controle por otimização escalar independente em 16 casos e comparação da potência homogênea com a cauda qui-quadrado exata. Esses controles verificam implementação, não natureza.

| População de qualidade | sigma_jit INPUT | N50 exploratório | N90 exploratório | N90 com validação nova | Poder na validação | Limite inferior simultâneo |
|---|---:|---:|---:|---:|---:|---:|
| GW250114_actual_width | 0.019 | 33 | 61 | 61 | 0.9156 | 0.9097455269826061 |
| GW250114_actual_width | 0.0228 | 21 | 39 | 39 | 0.91745 | 0.9116521198378627 |
| GW250114_actual_width | 0.03 | 11 | 22 | 22 | 0.92525 | 0.9197003060215954 |
| GWTC5_31_quality_mixture | 0.019 | 832 | 1588 | 1588 | 0.91115 | 0.905162697912409 |
| GWTC5_31_quality_mixture | 0.0228 | 504 | 996 | 996 | 0.91315 | 0.9072218326772077 |
| GWTC5_31_quality_mixture | 0.03 | 244 | 524 | 524 | 0.91495 | 0.9090758381360665 |
| GWTC5_33_quality_mixture | 0.019 | 908 | 1696 | 1696 | 0.91015 | 0.9041334660516472 |
| GWTC5_33_quality_mixture | 0.0228 | 542 | 1040 | 1144 | 0.9377 | 0.9325832155584126 |
| GWTC5_33_quality_mixture | 0.03 | 266 | 540 | 594 | 0.9326 | 0.9272998633507724 |

A busca inicial usa 4.000 repetições por N. Seu alvo não é certificado com o mesmo intervalo usado para escolhê-lo. Uma segunda grade finita foi gravada antes de novos sorteios: três N por cenário, 27 células, 20.000 repetições por célula. Cada célula recebe alfa=0,05/27 no limite unilateral exato Clopper–Pearson; selecionar uma célula aprovada dessa grade conserva o controle simultâneo. Os novos sorteios usam sementes separadas; o algoritmo estatístico é o mesmo, portanto não se trata de um segundo estimador independente. N50 permanece busca exploratória com erro MC, não inteiro mínimo exato. A grade N90 também não prova minimalidade.

Dois alvos exploratórios da mistura de 33 não passaram o limite inferior de 90% na validação: foram mantidos no resultado e o alvo reportado subiu na grade predefinida. Não se apagou o fracasso nem se usou apenas a potência pontual. As diferenças contra 59/38/21 da gerência para o caso de alta precisão decorrem da largura real, média perfilada e da exigência adicional de incerteza MC explícita; isso será confrontado na integração E0.

Todos estes N são **limites de planejamento condicionados a sigma_sys=0 e à transferência perfeita do jitter ao estimador IMR**. Essas duas condições não foram medidas aqui. Não autorizam resultado de 5sigma, escolha de desenrolamento ou gate verde. O limiar nominal ainda exige calibração do nulo heterogêneo em E2. A inferência dos posteriores completos da rota IV é E5; esta tabela não a substitui. Não houve posterior novo, PE ou forma de onda.

Equivalentes de informação local em delta-f (soma de (sigma_GW250114/sigma_i)^4; não informação de delta-tau): `{"GW250114_actual_width": 1.0, "GWTC5_31_quality_mixture": 1.0846152339870454, "GWTC5_33_quality_mixture": 1.0846169041201217}`.

Tempo medido da busca: 35.327371s; validação: 16.748353s. Uma thread; a parede contínua do orçamento inclui também coordenação e controles. UTC deste adendo 2026-09-22T19:15:05.778160+00:00.

- [refeito/e0_route_iv_power_013bis.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/e0_route_iv_power_013bis.py>) SHA256 `d3af372be301a0372cee7b418a8b1153bc711f0bc74fd28bc2189f507a57e9f4`.
- [refeito/e0_route_iv_power_013bis_v2.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/e0_route_iv_power_013bis_v2.py>) SHA256 `3d6009594c919da22bde0efee23afa93ac070f3f2b19e99ecd5250251d1efcdb`.
- [refeito/validate_e0_mc_targets_013bis.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/validate_e0_mc_targets_013bis.py>) SHA256 `eb1b79f34fc26c6ee2d2b10f333c5211082ca65d9c4ca311864fa4e9bbf52a26`.
- [bis/E0_ROUTE_IV_SMOKE.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E0_ROUTE_IV_SMOKE.json>) SHA256 `266ef0a9cb8cbfae8b7d4aaed1ed5479f57ea0dc40d5191b167bcc00cc1cc2c9`.
- [bis/E0_ROUTE_IV_POWER_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E0_ROUTE_IV_POWER_v2.json>) SHA256 `ae457e82c8c18b5cccf47d60c785d82b3ec3888db7975f2184666c558e4ddd93`.
- [bis/E0_ROUTE_IV_VALIDATION_PLAN.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E0_ROUTE_IV_VALIDATION_PLAN.json>) SHA256 `908727da18cb48a28fcb12f07c9578764af2f266aa08d8ba406735fb18c7fc55`.
- [bis/E0_ROUTE_IV_VALIDATION.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E0_ROUTE_IV_VALIDATION.json>) SHA256 `047554eb39c332a9b19190d241a5c34de2e16293074c5aca500ae00f4e3d1c42`.
- [bis/PART_B_BUDGET_START.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json>) SHA256 `2b3cfefd17cb8f3df845172a3b41f6e457b92b2c5bb164128aa0b40e8919355f`.

Reprodução: WSL /opt/lal_env/bin/python -B nos scripts indicados, em cópia isolada com saídas ausentes; os destinos existentes são recusados. Axiomas: N/A — sem Lean. Não é entrega de B1 nem aceite do portão completo.
