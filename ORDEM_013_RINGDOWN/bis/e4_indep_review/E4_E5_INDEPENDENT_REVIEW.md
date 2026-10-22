# E4/E5 — revisão numérica independente da execução authorized_001

[REAL] **PASS_CONDITIONAL_ARITHMETIC_ONLY: 310 verificações aprovadas, zero falhas, 8,570956578 s de execução do revisor.** Nenhum bloqueador numérico foi encontrado nos casos predefinidos. O resultado fecha a conferência aritmética condicional descrita abaixo; não fecha BF físico, seleção, calibração de sistemáticas ou a ORDEM013BIS.

O único executável científico chamado nesta rodada foi `independent_review.py --execute`, com WSL `/opt/lal_env/bin/python -B -O` e a autorização/hash fornecidos pelo principal. Não foram alterados produtor, revisor, tolerâncias, plano ou aplicação. A saída original ficou preservada em `runs/authorized_001/INDEPENDENT_REVIEW.json`. Não houve repetição para obter PASS. As leituras posteriores serviram somente para redigir este parecer a partir dos resultados existentes.

## Custódia efetivamente conferida

| Artefato | SHA256 |
|---|---|
| Autorização independente E4_INDEPENDENT_AUTHORIZATION_V1.json | `13dd28a75f9592e204577630dbf01021192ae66f424f3f3df392ef11b96c204b` |
| Registro E2 RINGDOWN_5SIGMA_V1.json | `e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416` |
| Revisor independent_review.py | `a8a2baa6801bf2274a4f6cde061959c538cc98622aab65983ffa82d6a14878dc` |
| Produtor deterministic_e4_e5.py | `c5f8576c76a32f668580aac2386264e719ee8e1c425360d75c1551335063b694` |
| Resultado do produtor DETERMINISTIC_DIAGNOSTICS.json | `a1e441ac0b16687d093d8590f70adae46acba100bee2c0923de17e687b88a55f` |
| Recibo do produtor RESULT_RECEIPT.json | `1f4fb47ad04a1b37b8df458056ed02c4cbdd71512c613e7ee0627aa521e4184b` |
| Resultado desta revisão INDEPENDENT_REVIEW.json | `d8f8d56faf6e6a65735594d9d80a5a3d39c18022f4d4782a2fcf31f241f2205d` |

Os hashes acima foram lidos dos artefatos. O revisor passou pela guarda registrada, pelo vínculo entre pacote produtor/E2 e pelos pins de resultado/recibo e inputs, antes das operações científicas. Os inputs foram novamente conferidos ao fim. Isso não constitui auditoria do incidente de identidade/seed: esse incidente permanece no escopo separado do principal/Russell e não recebe parecer deste revisor.

## E4 Fisher440: cálculo conferido, alcance local

[REAL] Cobertura completa e sem duplicação: **1.920 linhas = dez leituras × duas variantes × quatro PSDs × dois perfis × duas rotas SNR × seis âncoras**. Zero divergências nas comparações de fórmulas, ganho PSD, sigma, correção, N50/N90 e estados OPEN nas linhas cobertas pelo oráculo. O teste de fórmulas usa tolerância relativa 2e-8, absoluta zero; não arredonda previsões minúsculas para zero por tolerância absoluta.

As quatro derivadas foram comparadas com diferenças centrais em passos 3e-5 e 1e-5. Maior erro relativo observado: **1,2438011e-7**, na derivada de frequência com o passo maior, abaixo do limite pré-fixado 1e-5. Para a derivada de tau, os erros foram **3,1793732e-10** e **3,6877173e-11**. O oráculo de Fourier foi validado por essas diferenças; a correspondência com a implementação do produtor foi conferida pelas informações/sigmas de saída, sem instrumentar ou alterar suas funções internas.

A projeção por mínimos quadrados dos componentes real e imaginário concordou com o complemento de Schur nos oito pares PSD/perfil. Exemplos de informação local por rho²:

| PSD | Frequência fixa | Frequência livre, tau_GR fixa |
|---|---:|---:|
| O4 | 0,249713262455 | 0,248151126663 |
| O5 | 0,249074214109 | 0,247484715172 |
| ET | 0,248638586748 | 0,247071988943 |
| CE | 0,248418398702 | 0,246819542063 |

[INPUT/DERIVED] Para tornar os números interpretáveis, a tabela seguinte reproduz o recorte previamente definido das quatro leituras com comparação de densidade, variante **220+440 deformados**, O4, frequência fixa e **rho440 isolado=40**. Fonte de referência: Mdet=68,1 massas solares, spin=0,68, z=0. Não é a amplitude medida de GW250114 nem SNR IMR/rede.

| Leitura | delta_tau440 | sigma local | Correção/sigma local | N50 contínuo | N90 condicional contínuo |
|---|---:|---:|---:|---:|---:|
| R-B | −0,08216064 | 0,05002870 | 1,642270 | 9,269382 | 14,630010 |
| R-MOD | −0,19599711 | 0,05002870 | 3,917694 | 1,628842 | 2,570828 |
| R-RAIZ-0 | −0,07367832 | 0,05002870 | 1,472721 | 11,526539 | 18,192517 |
| R-LIN | −0,13724469 | 0,05002870 | 2,743319 | 3,321906 | 5,243016 |

Na rota de amplitude fixa, o ganho de rho em relação a O4 é **1; 1,821611425; 8,757643953; 14,222764701**, respectivamente O4/O5/ET/CE. Com âncora O4=40, os rho usados são **40; 72,864457; 350,305758; 568,910588**. Para R-B, N90 contínuo é **14,630010; 4,420241; 0,191577; 0,072700**. Valores inferiores a um são razões contínuas de informação dentro do cenário, não frações físicas de um evento observado.

**Limites críticos:** N50=25/z_local² e N90=(5+1,2815515655)²/z_local² pressupõem Z gaussiano de variância conhecida, fontes idênticas independentes e ausência de sistemáticas. Não representam significância calibrada, contagem astrofísica garantida ou tempo de observação. Fisher é local em GR; uma correção de aproximadamente −0,196 em R-MOD não teve validade global/não linear demonstrada por esta revisão. Liberar frequência neste perfil não equivale a liberar conjuntamente massa e spin, nem resolve sua degenerescência. QNM spline e PSDs são inputs pinados compartilhados pelo produtor e pelo revisor: sua exatidão física externa não foi reprovada nem provada aqui.

A variante somente220 conserva efeito440 zero; PROP/COHERENT permanecem OPEN e GLOBAL zero por construção. Nenhuma leitura foi escolhida como hipótese vencedora. Os 1.920 casos, e não só o recorte exibido, passaram pela conferência de cobertura/formulação.

## Densidades arquivadas: oito comparações independentes, nenhum BF pago

[REAL] Foram usados **todos os 40.776 draws pareados** do produto já arquivado de calibração não cega GW250114, sem thinning/filtro. As oito comparações foram fixadas antes da execução: 220/440 × R-B/R-MOD/R-RAIZ-0/R-LIN. Em cada uma, conferi gaussiana por momentos completos e soma direta dos kernels 2D nas bandas 0,7/1/1,3, com ESS dos kernels, quantis dos shifts pareados e faixa dos estimadores. O oráculo não chama gaussian_kde. As vinte linhas marginais foram conferidas quanto à cobertura e lnB null; isso não equivale a refazer numericamente a densidade de todas as outras leituras.

| Setor | Leitura | Log-razão gaussiana | Faixa dos quatro estimadores |
|---|---|---:|---:|
| 220 | R-B | −0,036927 | [−0,036927; +0,073050] |
| 220 | R-MOD | −0,177251 | [−0,177251; −0,125844] |
| 220 | R-RAIZ-0 | −0,167082 | [−0,167082; −0,109347] |
| 220 | R-LIN | −0,693491 | [−0,693491; −0,662039] |
| 440 | R-B | −0,075426 | [−0,092541; −0,075426] |
| 440 | R-MOD | −0,190315 | [−0,290132; −0,190315] |
| 440 | R-RAIZ-0 | −0,067504 | [−0,081439; −0,067504] |
| 440 | R-LIN | −0,129057 | [−0,176485; −0,129057] |

**O sinal de 220/R-B muda com o estimador.** As faixas são sensibilidade a estimador/banda, não intervalos de confiança. As outras sete faixas negativas também não são evidência calibrada de exclusão: o objeto conferido é log p_residual(0)−log p_setor_livre(0), não lnB. Não multiplicar os diagnósticos 220 e440 do mesmo evento.

[DECLARADO NO PRODUTOR; NÃO RECOMPUTADO NESTE REVISOR] A tabela de bordas do produtor dá quantis 5/50/95% de dtau440 **[−0,348908; 0,951878; 3,396836]**, fração a uma largura de kernel da borda **0,0272955**, e massa marginal KDE fora do prior **0,0114608**, sem correção de borda. Esses números foram lidos do resultado pinado; não estão entre as conferências numéricas independentes do script. Eles tornam explícita a limitação de usar densidades gaussianas/KDE não limitadas pelo suporte do prior. ESS de kernel não certifica ESS da cadeia nem precisão física da cauda.

## E5: informação local, forte concentração e inferência ainda aberta

[REAL/DERIVED] A identidade I_i(q=0)=1/(2 sigma_i^4), sob cenário sigma_sys=0, reproduz os pesos/frações e equivalentes. Os membros e a ordem dos quatro conjuntos foram preservados; nenhum evento foi retirado por largura.

| Conjunto arquivado | Eventos | Equivalentes informacionais de GW250114 |
|---|---:|---:|
| GWTC5_31 | 31 | 1,084615234 |
| GWTC5_33 | 33 | 1,084616904 |
| GWTC3_10 | 10 | 0,012669655 |
| GWTC3_18 | 18 | 0,012720742 |

GW250114 concentra aproximadamente **92,1986%** da informação no conjunto31 e **92,1985%** no33. Portanto, adicionar dois eventos nesse cenário quase não altera a informação do canal de variância. Isso não autoriza cortá-los nem reponderar novamente uma likelihood já heteroscedástica. Os equivalentes são relativos ao canal df e às larguras arquivadas; não são equivalentes de detecção física de TGL.

Sigma_sys e transferência de jitter permanecem null. A regra geral é I_i=1/[2(sigma_i²+sigma_sys²)²]; sigma^-4 é seu cenário de piso zero, não uma medição de sistemática nula. Nenhum LRT, cauda de nulo, ajuste populacional, limite de sigma_pop ou utilitário posterior_population_logscore foi executado/revalidado nesta rodada. A calibração da média ajustada e dos efeitos de N finito também não foi paga aqui.

## Pago e não pago nesta revisão

| Item | Estatuto após esta execução |
|---|---|
| Derivadas e Fisher440 local; projeção/Schur; cobertura e fórmulas de 1.920 linhas | [REAL] Conferência numérica paga no contrato condicional |
| PSD/ASD, ganho de norma/amplitude, N50/N90 dos cenários | [REAL/DERIVED] Aritmética conferida; interpretação permanece INPUT |
| Oito pares de densidade, gaussiana/mistura direta, ESS de kernel, shifts | [REAL] Conferência numérica paga; sem BF físico |
| Informação IV, membros, razões/frações e equivalentes dos quatro conjuntos | [REAL/DERIVED] Conferido como proxy local gaussiano |
| Normalização global do modelo restrito/priors de nuisance/seleção | [OPEN] Não pago; lnB continua null |
| Covariância física, sigma_sys, transferência browniana/jitter recuperado | [OPEN] Não pago |
| Nulo calibrado, p físico/5sigma, inferência hierárquica completa | [OPEN] Não executado por este revisor |
| Robustez com440 fixo vs livre na mesma fonte/configuração | [OPEN] Sem produto independente comparável |
| Caudas/bordas e precisão da cadeia | [OPEN] Conferência de densidade não resolve essas limitações |
| Catálogo de alto SNR, elegibilidade/cegueira e incidente de seed | Fora deste escopo de revisão numérica; não certificados aqui |

O resultado independente e os números sustentam a incorporação das **contas condicionais** ao relatório principal, mantendo os qualificadores e OPEN. Não sustentam anunciar experimento físico pago, confirmação, exclusão por lnB, ou fechamento da ordem. E7 permanece congelado e nenhuma extração E7 foi realizada nesta execução. Não houve PE, MC, waveform gerada, dados de teste ou strain novo.
