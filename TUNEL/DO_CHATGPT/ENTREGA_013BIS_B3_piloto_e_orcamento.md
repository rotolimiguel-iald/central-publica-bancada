[REAL — B3 entregue com comparação Kerr e parede técnica do piloto IMR; orçamento registrado. Posterior IMR e calibração física NÃO PAGOS.]

# B3 — piloto e orçamento

Abertura `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`. Ficha `7535ec53b4c1851728e5e3a09de400cd17f91362f1faefa7cd773e5358526f59`. Orçamento `892e416585062eef5229e01c2e8a6c5b8d3c4ee8a10a72798c0ab2034e5f42e4`.

| Critério | Resultado e limite |
|---|---|
| Kerr_220_10M | PAGO: comparação de Mf/af, critérios de convergência e revisão. Equivalência integral da versão, strain e PSD NÃO PAGA. |
| Custo IMR | PAGO: custo da tentativa falha. Custo por evento convergido OPEN. |
| Posterior de deformação | NÃO PAGO: SIGSEGV antes de posterior aceito. Nenhum hash/posterior inventado. |
| Comparação delta_tau publicado | NÃO PAGA: falta posterior próprio. Família própria pSEOBNRv4HM_PA alinhada difere da pSEOBNRv5PHM precessante publicada. |
| Alocação E3.2 | PAGA como orçamento de parede: cinco alternativas, pesos esperados e reserva final explícitos. |

## Kerr, evento conhecido e comparação descritiva

Mf está em massas solares no referencial do detector; af é adimensional.

| Parâmetro | Próprio q05 / q50 / q95 | Publicado q05 / q50 / q95 | Diferença de medianas | Diferença/largura em quadratura |
|---|---|---|---:|---:|
| Mf | 69.26809 / 74.57491 / 79.882842 | 66.735452 / 73.505287 / 79.902241 | 1.0696231 | 0.20690757 |
| af | 0.67222921 / 0.76245903 / 0.83090604 | 0.62646944 / 0.75195214 / 0.8347186 | 0.01050689 | 0.12804092 |

N=2128; ESS=3093.851293; delta_logZ=0.099952448; chamadas do sampler=1356580. Há sobreposição dos intervalos90%. A diferença de medianas dividida pela largura em quadratura não é z calibrado: é o mesmo evento, com dados/configurações relacionados. Não é teste independente nem evidência adicional da TGL. A revisão conferiu os posteriores completos e metadados/pins no escopo do parecer; limite de modos/convergência global permanece.

A variante Welch foi recusada por condicionamento. A primeira variante com PSD pública parou parcial e foi conservada; a continuação em nova versão convergiu. A PSD pública usada não foi demonstrada idêntica à PSD externa da análise publicada; os512 live points também diferem dos4096 publicados. O produto tem comparação aceita com limitações, não reprodução equivalente integral.

## Parede do instrumento IMR

Controle original: retorno -11, 11.011139623s de parede; CPU filhos=5.694202s. O grupo do piloto foi confirmado encerrado. Não há posterior aceito, número de chamadas completo ou diferença contra o delta_tau publicado.

Diagnóstico limitado: 10 processos, 16 chamadas/15 retornos. Parede somada dos filhos 13.168752s; CPU 10.400864s. O teto incluiu o replay de metadados e não foi reiniciado. Ausência dos grupos desses diagnósticos não foi medida separadamente.

O fmax interno1024 gera frequência de amostragem interna2048, apesar do grid de dados4096. A recusa EDOM consultada testa o QNM550 da RG. Aumentar fmax para2048 causou aborto nativo−6 num ponto completo do prior. Os oito primeiros draws em1024 não reproduziram o SIGSEGV original. A causa exata desse SIGSEGV permanece OPEN; a possível relação entre buffer dimensionado por dtau220 e extensão440 é hipótese, não prova de causa. Não houve exclusão de pontos problemáticos do prior, corte de modos ou troca silenciosa de likelihood.

A revisão independente fechou o diagnóstico como parede do instrumento atual, sem aprovar continuação da PE. Uma reconstrução/requalificação nativa seria outro desenvolvimento, com fontes/binários e transporte numérico próprios; não foi simulada por retry de Python.

## Alocação

Novas PE=0; injeções=0; downloads de strain cego=0. A decisão decorre da falta de instrumento validado neste registro, não de esgotamento das40h nem de impossibilidade geral do método. A custódia e o registro científico ficam preservados. Jobs vazios no documento não removem jobs estáticos antigos do guard; não existe autorização para relançar o piloto estático.

Reserva final2h contada desde 2026-09-22T23:02:56.988802+00:00; stop 2026-09-23T01:02:56.988802+00:00. Saldo de ciência não alocado/devolvido na medição: 34.060226h, não gasto. Atraso de revisão consome reserva; o relógio não reinicia.

| Alternativa | Decisão e limite |
|---|---|
| i. Calibrar apenas pisos R-LIN/R-MOD | Coeficientes recalculados abaixo; nenhum sigma_inj/custo de recuperação qualificada medido. Piso mais largo não corrige falha nativa. Custo por programa qualificado OPEN; alocação0. |
| ii. Calibrar somente bins de SNR alto | Menor largura é expectativa condicional; viés abaixo do piso não demonstrado. Nenhum bin ou evento admitido por este candidato. Custo por programa qualificado OPEN; alocação0. |
| iii. PE reduzida com amplitude marginalizada | Alternativa metodológica da ordem; instrumento diferente, sem implementação/custo/convergência validados neste escopo. Nenhum workaround executado. Custo por programa qualificado OPEN; alocação0. |
| iv. Reutilizar injeções públicas LVK | Diagnóstico F2 existente revisado pode ser reutilizado descritivamente; duas recuperações com/sem44 não são curva c(SNR), cobertura repetida nem sigma_sys calibrado. Zero PE nova. Custo por programa qualificado OPEN; alocação0. |
| v. pSEOBNRv5PHM via pyseobnr em venv próprio | Instalabilidade, custo e qualificação não medidos aqui; sem instalação, rebuild ou troca de runtime. Custo permanece null. Custo por programa qualificado OPEN; alocação0. |

N=(sigma_inj/piso)², sob média de réplicas independentes sem viés. Sigma_inj é INPUT ilustrativo, não medição do piloto. Exemplo comum sigma=.058, cinco bins×duas famílias:

| Leitura | N por célula (ceil, piso /5) | N dez células |
|---|---:|---:|
| R-B | 214 | 2140 |
| R-MOD | 62 | 620 |
| R-RAIZ-0 | 62 | 620 |
| R-LIN | 17 | 170 |

As dez leituras e o piso /15 estão no JSON, inclusive coeficientes sub-resolução sem alvo operacional. Nenhuma contagem acima calibra uma cauda5σ ou um viés desconhecido. Horas por programa = N × custo de recuperação; o segundo fator continua OPEN.

## Candidatas e informação esperada

14 candidatas documentais,10 sem hold e4 com hold, ausência de publicação limitada ao escopo pesquisado. Ordenação por SNR anterior à PE. E[I] usa dispersão lognormal fixa e covariância de coeficientes preservada; não é informação observada, ganho/hora nem poder de teste. Ajustes31 e33 são alternativas sobrepostas, não se somam.

| Evento | SNR | Hold | Proxy31 | E[I]31 | Proxy33 | E[I]33 |
|---|---:|---|---:|---:|---:|---:|
| GW230919_215712 | 16.8 | não | 12.17258 | 13.47072 | 12.66262 | 13.99631 |
| GW241111_111552 | 16.3 | não | 11.49695 | 12.72304 | 11.98671 | 13.24921 |
| GW240930_035959 | 16.1 | sim | 11.23179 | 12.4296 | 11.72101 | 12.95553 |
| GW240513_183302 | 14.5 | não | 9.215811 | 10.19863 | 9.692421 | 10.71328 |
| GW240920_073424 | 14.0 | não | 8.624423 | 9.544175 | 9.094163 | 10.05201 |
| GW250118_170523 | 13.9 | não | 8.508363 | 9.415738 | 8.976569 | 9.922027 |
| GW241130_034908 | 13.8 | não | 8.393045 | 9.288122 | 8.859663 | 9.792808 |
| GW240923_204006 | 13.6 | não | 8.164632 | 9.035349 | 8.627918 | 9.536655 |
| GW241210_060606 | 13.4 | não | 7.939189 | 8.785864 | 8.398937 | 9.283556 |
| GW240615_160735 | 13.1 | sim | 7.606604 | 8.417811 | 8.060661 | 8.909652 |
| GW250109_010541 | 13.1 | não | 7.606604 | 8.417811 | 8.060661 | 8.909652 |
| GW240515_005301 | 12.8 | sim | 7.28073 | 8.057184 | 7.728646 | 8.542667 |
| GW241102_144729 | 12.7 | sim | 7.173599 | 7.938628 | 7.61937 | 8.421881 |
| GW250104_015122 | 12.1 | não | 6.546549 | 7.244706 | 6.97844 | 7.713445 |

## Custos, reprodução e fontes

Kerr controladores V1+V2: 1035.302019s; CPU filhos 1026.449371s. Diagnóstico Welch separado: 3.402372s. Esses tempos explicam o consumo; não são somados novamente ao relógio contínuo da ParteB. Custo de waveform isolada, de Kerr e de PE IMR não são intercambiáveis.

Comandos e variantes exatas estão em E3_KERR_LAUNCH_V1/V2, nos manifests e no LAUNCH_CONTEXT do piloto; Os comandos abreviados a seguir são localizadores, não comandos completos de replay: `bis/e2_code/run_controlled.py --job GW250114_PILOT` foi a tentativa IMR. O orçamento foi registrado por `refeito/activate_wall_budget_v2_013bis.py --review ... --review-sha256 ...`. Reproduzir somente em cópia isolada; destinos originais não se sobrescrevem. N/A — sem Lean.

Falhas conservadas: Welch, Kerr parcial, SIGSEGV, abort−6 e correção ao lado do mapeamento HTML/texto das fontes. O diagnóstico contém os comandos/entradas precall; os manifests listam cada artefato e fonte primária. Nenhuma inferência de natureza nem escolha de leitura foi feita.

- [ORDEM_013_RINGDOWN/ORCAMENTO_40H.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/ORCAMENTO_40H.json>) — `892e416585062eef5229e01c2e8a6c5b8d3c4ee8a10a72798c0ab2034e5f42e4` (126793 B).
- [ORDEM_013_RINGDOWN/bis/E3_WALL_BUDGET_ACTIVATION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E3_WALL_BUDGET_ACTIVATION_V1.json>) — `15a24c061d3e8adf989399203f46b27f255a5c8feb3951ba2fb943cb9125b7d5` (761 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_review/E3_WALL_BUDGET_CANDIDATE_REVIEW_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_review/E3_WALL_BUDGET_CANDIDATE_REVIEW_v2.json>) — `cbea2938b692b79206cf87977567ba060963a0a835e1bb10502a4dad1ce51943` (95501 B).
- [ORDEM_013_RINGDOWN/bis/e3_budget_wall/MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_budget_wall/MANIFEST.json>) — `c049aa8c257e9706882bc8853aeda81c0245764d8417570f4769433c475f01c8` (6677 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_failure_diagnostic/MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_failure_diagnostic/MANIFEST.json>) — `f24326c2c202547495f91018545f8eb10f0f7e327c984873a6cf73f5c537aa01` (35308 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json>) — `9c56068518044bf077b12fb3c7d2a85eb8fb7eb5d1411467ebac30d094b29893` (54926 B).
- [ORDEM_013_RINGDOWN/bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json>) — `0e92967fd6f228ad2e6bc003b0ed8a67a994a6fdc6d660013e99c66a686248c7` (2190412 B).
- [ORDEM_013_RINGDOWN/bis/E3_KERR_LAUNCH_V2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E3_KERR_LAUNCH_V2.json>) — `4d56e6bc1906a644ddd6554d7330cd1e1aa8263b5ff1f75ce868022aa529a305` (917 B).
- [ORDEM_013_RINGDOWN/cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json>) — `39e0073a17aa9236420cf93232786f5a289593359aa40e1c01103474c1821efb` (3636 B).
- [ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V1/CONTROLLER.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V1/CONTROLLER.json>) — `bf3f874342d15c4d7687380baf52710237dab7a67fb4ffc0a759a3f59506d72b` (828 B).
- [ORDEM_013_RINGDOWN/bis/e3_blind_review/REVIEW_RECEIPT_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_blind_review/REVIEW_RECEIPT_V1.json>) — `e456d058f41847acc37d45d58543d34a4be638fedce1ee2eeeaad7b2603ee920` (1596 B).
- [ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B3.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B3.md>) — `7535ec53b4c1851728e5e3a09de400cd17f91362f1faefa7cd773e5358526f59` (613 B).
