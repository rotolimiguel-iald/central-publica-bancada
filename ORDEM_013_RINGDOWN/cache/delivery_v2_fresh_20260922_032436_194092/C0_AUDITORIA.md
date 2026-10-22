[REAL — auditoria de cobertura e oráculos; arquivo primário local da literatura pendente]

# C0 — Auditoria do texto de confrontação

24 itens; 38 linhas não vazias exigidas; zero linha descoberta.
A auditoria não declara o objetivo integral encerrado. Referências/hash completos no JSON.

## T01 — linhas 1, 9, 11, 17, 19, 25, 27, 31, 47, 49, 51, 58

**NÃO_APLICÁVEL**

Texto: O Que a TGL Prediz / O Que Falta para a Confrontação / Para que os dados atuais pudessem testar a TGL, seria necessário: / O Que os Dados Mostram / Predição TGL Status Observacional / --- / 🧮 Derivando a Previsão Numérica / A equação mestra GKSL: / --- / 📌 Conclusão da Confrontação / O que os dados dizem: / O que a TGL precisa fazer:

**O que acerta:** São títulos ou transições.

**Frase corrigida:** Organização textual, sem afirmação científica adicional.

Evidências: input

## T02 — linhas 3, 5

**PARCIAL**

Texto: A TGL prediz uma equação mestra GKSL com operadores de salto: / L_k = \sqrt{\beta_{\text{TGL}}} \cdot \sqrt{K_\partial}_{(k)}, \qquad \beta_{\text{TGL}} = \alpha\sqrt{e} \approx 0.01203

**O que acerta:** Existe no programa uma realização finita com L=sqrt(beta)sqrt(K).

**Frase corrigida:** A v369 constrói um salto hermitiano em um proxy positivo 4x4; a fórmula não identifica por si a dinâmica de um horizonte tipo III1.

Evidências: verb, gksl

## T03 — linhas 5

**CANÔNICO**

Texto: L_k = \sqrt{\beta_{\text{TGL}}} \cdot \sqrt{K_\partial}_{(k)}, \qquad \beta_{\text{TGL}} = \alpha\sqrt{e} \approx 0.01203

**O que acerta:** O coeficiente beta é alpha_CODATA2018*sqrt(e).

**Frase corrigida:** Beta é calculado em runtime a partir de alpha e sqrt(e); seu valor sozinho não determina um tempo físico.

Evidências: verb, checks

## T04 — linhas 7

**PARCIAL**

Texto: A escala de tempo de dephasing é \tau_{\text{deph}} \propto 1/\beta_{\text{TGL}}, que para buracos negros estelares deveria cair na faixa de sensibilidade do LIGO O5.

**O que acerta:** A taxa é proporcional a beta mantendo os demais dados fixados.

**Frase corrigida:** Na lei quadrática, tau_deph=2/(beta*tau_star*omega²); uma previsão de detectabilidade em O5 exige relógio, SNR e parâmetros de perturbação.

Evidências: clock, fisher

## T05 — linhas 13, 60

**CERTO_NO_ESSENCIAL**

Texto: 1. Forma funcional específica: A TGL precisa expressar K_\partial em termos de parâmetros observáveis (massa do remanescente, spin, distância) — não apenas como um operador modular abstrato. / 1. Derivar \Gamma_{\text{deph}} em termos de M, a, D (massa, spin, distância)

**O que acerta:** É necessário mapear o gerador e seu relógio aos observáveis.

**Frase corrigida:** O ramo B fornece Gamma=beta*w(chi)²/(2*t_M) sob o relógio INPUT t_M; a distância afeta amplitude/redshift, não necessariamente a taxa local. A escolha física do ramo permanece aberta.

Evidências: old_prediction, clock, mapping

## T06 — linhas 14, 63

**CERTO_NO_ESSENCIAL**

Texto: 2. Assinatura no domínio do tempo: A predição de dephasing deve ser traduzida em uma modificação explícita da forma de onda que possa ser ajustada aos dados do LIGO. / 4. entregar a forma de onda modificada para que grupos independentes possam ajustá-la

**O que acerta:** Uma previsão de strain deve ser executável e reproduzível.

**Frase corrigida:** Há agora um template condicional de ensemble e um desenrolamento de fase explícito; distinguir ambos e calibrar recuperação é necessário antes do confronto de strain.

Evidências: template, mapping

## T07 — linhas 15, 62

**CERTO_NO_ESSENCIAL**

Texto: 3. Bayes factor esperado: A TGL precisa especificar qual \ln B seus modelos produziriam em O4/O5, dado \beta_{\text{TGL}}. / 3. Calcular o Bayes factor esperado para O4/O5

**O que acerta:** A viabilidade requer previsão quantitativa de evidência.

**Frase corrigida:** O fator de Bayes é aleatório e depende de SNR, PSD e priors. O forecast pontual local tem média +/-z²/2 e dispersão z; não é um ln B observado.

Evidências: fisher, registration

## T08 — linhas 20

**CONTRADITO_PELO_CANON**

Texto: Dephasing anômalo no ringdown Não testado — falta forma funcional

**O que acerta:** A identificação GKSL-horizonte-strain ainda pede hipóteses explícitas.

**Frase corrigida:** A forma funcional e o rito V346 já existem; a rodada V2 foi inconclusiva por sistemáticas e baixa sensibilidade. Não se deve dizer que nunca foi testado.

Evidências: old_prediction, v2, plan

## T09 — linhas 21, 55

**PARCIAL**

Texto: Ecos de longo atraso Não observados — consistente, mas não confirmatório / 3. Nenhum eco pós-merger foi observado

**O que acerta:** Não observação sem confirmação é uma distinção correta.

**Frase corrigida:** Os ensaios de ecos da casa não estabeleceram detecção; seus controles de sensibilidade e sistemáticas impedem usar ausência de pico como exclusão geral. Não se reabre esse canal nesta ordem.

Evidências: echo, plan

## T10 — linhas 22

**PARCIAL**

Texto: Alargamento não-térmico de QNM Não detectado — constraints de GR são fortes

**O que acerta:** Resultados publicados são compatíveis com Kerr no estudo consultado.

**Frase corrigida:** A precisão depende do modo, observável e modelo. Um limite sobre amortecimento efetivo não é automaticamente um limite sobre decoerência quântica de propagação.

Evidências: lvk, mapping

## T11 — linhas 23

**PARCIAL**

Texto: \beta_{\text{TGL}} = \alpha\sqrt{e} Não medido — requer previsão numérica específica

**O que acerta:** A inferência GW conferida não mede beta de forma independente.

**Frase corrigida:** Na lei quadrática, um relógio livre mede o produto beta*tau_star. Para medir beta é preciso fixar ou identificar o relógio e a partição por informação independente.

Evidências: clock, plan

## T12 — linhas 29

**PARCIAL**

Texto: Para confrontar a TGL com os dados, é necessário derivar a taxa de dephasing a partir do operador modular K_\partial. No formalismo de Tomita-Takesaki, K_\partial = -\ln \Delta, onde \Delta é o operador modular. Para uma fronteira tipo III₁, o espectro de K_\partial é contínuo e não-limitado.

**O que acerta:** K=-log Delta é uma convenção de gerador modular.

**Frase corrigida:** A identificação modular é dependente da álgebra e do estado; o K bilateral tem simetria de sinal. Não se pode tomar sqrt(K) positiva sem especificar outra construção.

Evidências: finite_J, gksl

## T13 — linhas 29

**PARCIAL**

Texto: Para confrontar a TGL com os dados, é necessário derivar a taxa de dephasing a partir do operador modular K_\partial. No formalismo de Tomita-Takesaki, K_\partial = -\ln \Delta, onde \Delta é o operador modular. Para uma fronteira tipo III₁, o espectro de K_\partial é contínuo e não-limitado.

**O que acerta:** O tipo III1 envolve espectro modular amplo, não um corte finito de autovalores.

**Frase corrigida:** Espectro como conjunto contínuo não significa ausência de espectro pontual: estados quase periódicos do fator III1 injetivo fornecem uma ressalva explícita. KΩ=0 já é um autovetor modular.

Evidências: finite_J, almost_periodic

## T14 — linhas 33

**CANÔNICO**

Texto: \frac{d\rho}{dt} = \sum_k \left( L_k \rho L_k^\dagger - \frac{1}{2}\{ L_k^\dagger L_k, \rho \} \right)

**O que acerta:** A expressão é o dissipador GKSL formal.

**Frase corrigida:** A fórmula é válida para operadores limitados na regularização finita; operadores não limitados exigem domínios e existência do semigrupo. O termo Hamiltoniano foi omitido nesse trecho.

Evidências: gksl, verb

## T15 — linhas 35, 37

**CONTRADITO_PELO_CANON**

Texto: com L_k = \sqrt{\beta_{\text{TGL}}} \sqrt{K_\partial}_{(k)} implica uma taxa de decoerência: / \Gamma_{\text{deph}} \sim \beta_{\text{TGL}} \cdot \langle K_\partial \rangle

**O que acerta:** Tr(L†L rho)=beta<K> é uma taxa de saltos na representação escolhida.

**Frase corrigida:** A taxa de coerência é beta*(sqrt(k_i)-sqrt(k_j))²/2. A média beta<K> não é essa taxa e muda sob L+cI sem mudar o dissipador.

Evidências: crossover, checks, gksl

## T16 — linhas 39

**DIMENSIONALMENTE_INCONSISTENTE**

Texto: Para um buraco negro de massa M, a escala natural de K_\partial é \sim M/M_{\text{Pl}}^2 (em unidades de Planck). Isso daria:

**O que acerta:** A massa fornece uma escala gravitacional natural.

**Frase corrigida:** Em hbar=c=1, M/m_P²=GM é tempo. Não é um gerador modular adimensional nem uma taxa sem fatores adicionais e uma identificação física.

Evidências: checks

## T17 — linhas 41

**DIMENSIONALMENTE_INCONSISTENTE**

Texto: \Gamma_{\text{deph}} \sim \beta_{\text{TGL}} \cdot \frac{M}{M_{\text{Pl}}^2}

**O que acerta:** A expressão tenta relacionar a taxa a uma escala do remanescente.

**Frase corrigida:** Beta*GM/c³ tem unidade de tempo. A lei do ramo B contém ainda omega²/2, tornando Gamma uma taxa.

Evidências: checks, old_prediction

## T18 — linhas 43

**DIMENSIONALMENTE_INCONSISTENTE**

Texto: Para M \sim 60 M_\odot, M/M_{\text{Pl}}^2 \sim 10^{76} em unidades naturais. A taxa de dephasing seria astronomicamente grande — o que está em conflito direto com a observação de ringdowns coerentes.

**O que acerta:** Uma taxa muito maior que a frequência precisaria ser confrontada com coerência observada.

**Frase corrigida:** Para 60 massas solares t_M é cerca de 2.96e-4 s, ou 5.48e39 tempos de Planck. O número 1e76 não é essa taxa; (M_solar/m_P)² é apenas uma hipótese de origem da confusão.

Evidências: checks

## T19 — linhas 45

**CONTRADITO_PELO_CANON**

Texto: Este é o ponto crítico: A TGL precisa de um mecanismo de supressão que reduza K_\partial a valores compatíveis com a coerência observada. Sem isso, a teoria é falsificada pelos próprios dados de O4.

**O que acerta:** Uma leitura física com excesso de perda de coerência pode ser refutada.

**Frase corrigida:** A alegada falsificação por 1e76 não decorre das equações apresentadas. Existem leituras fortemente suprimidas e outras testáveis; cada uma exige confronto com seu observável, sem declarar falsificação global a partir de unidades inconsistentes.

Evidências: checks, clock, registration

## T20 — linhas 53

**PARCIAL**

Texto: 1. GR passa em todos os testes de ringdown com precisão de poucos por cento

**O que acerta:** A frequência fundamental recebeu limites percentuais fortes.

**Frase corrigida:** No GW250114 consultado, o ajuste IMR limita df220 em escala percentual e dtau220 em aproximadamente dez por cento (90%); não se generaliza a todos os testes nem ao ringdown isolado.

Evidências: lvk

## T21 — linhas 54

**PARCIAL**

Texto: 2. Nenhum desvio de QNM foi detectado; GW250114 confirma Kerr com precisão sem precedentes

**O que acerta:** O estudo consultado encontra consistência com Kerr.

**Frase corrigida:** GW250114 fornece limites fortes e dependentes do modelo; consistência não é prova definitiva de Kerr ou confirmação da TGL.

Evidências: lvk

## T22 — linhas 56

**DECLARADO**

Texto: 4. Decoerência de OG é negligenciável na faixa de frequência do LIGO

**O que acerta:** As ondas detectadas permitem estimar coerência e modos sob modelos de sinal.

**Frase corrigida:** O texto não fornece um limite numérico de decoerência de propagação. Coerência de strain, matriz densidade e ruído óptico do interferômetro são observáveis diferentes.

Evidências: mapping, plan

## T23 — linhas 61

**CERTO_NO_ESSENCIAL**

Texto: 2. Mostrar que \Gamma_{\text{deph}} \ll \omega_{\text{QNM}} para buracos negros estelares

**O que acerta:** Gamma/omega quantifica um regime perturbativo.

**Frase corrigida:** Reportar Gamma/omega é necessário, mas detectabilidade é controlada pela correção em tau comparada à incerteza, depois de eliminar degenerescências e sistemáticas.

Evidências: fisher, mapping

## T24 — linhas 65

**PARCIAL**

Texto: Com isso vamos conseguir rodar com precisão nos dados atuais

**O que acerta:** Taxa, template e previsão de evidência tornam o teste operacional.

**Frase corrigida:** A precisão final depende da informação dos dados e da calibração. As próximas etapas são posteriores, injeções e strain registrado; fórmulas e software não garantem poder de decisão.

Evidências: plan, registration

## Referências

- **input**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\PARA_CHATGPT\\ORDEM_013_INSUMOS\\TEXTO_CONFRONTACAO_OPERADOR_21SET_VERBATIM.md', 'locator': 'linhas 1-65', 'sha256': '6600f4e99c79845e7a2e7676cfb3e5772b61907e4c4e2fd810bee876e3c8afa8'}
- **verb**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\cache\\casa\\um.py', 'locator': '2311-2332: _verb_L', 'sha256': 'd9f5bd5dffc3333df707fb44ad0a859448a5042c38711479108c7f4b37538aeb'}
- **crossover**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\cache\\casa\\um.py', 'locator': '2831-2875: prove_dephasing_crossover, errata v369', 'sha256': 'd9f5bd5dffc3333df707fb44ad0a859448a5042c38711479108c7f4b37538aeb'}
- **clock**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\cache\\casa\\um.py', 'locator': '190961-191018: lei e partition_declared', 'sha256': 'd9f5bd5dffc3333df707fb44ad0a859448a5042c38711479108c7f4b37538aeb'}
- **finite_J**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\cache\\casa\\ContinuousModularZero.lean', 'locator': '80-94: modularGen_omega_zero, J_modularGen_J; FACE FINITA, não recompilada nesta ordem', 'sha256': '0dad5794f98ba1cb8519b4c105f63d555b5dc3d8fab7884f8265aebff214f376'}
- **old_prediction**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\cache\\casa\\ringdown_dephasing_v2.py', 'locator': '139-141', 'sha256': '0793c58d6995194b8b119bd54be3883718c2b51bb6f4b5c8b71fe9720544302b'}
- **v2**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\cache\\casa\\RINGDOWN_DEPHASING_V2_RESULT.json', 'locator': 'resultado congelado e per_series[2]', 'sha256': 'ff15f023dd91d8c77fb003b2efd10c91b22d5bcb5047dc2101885fbb634e15c5'}
- **echo**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\cache\\casa\\ECHO_PE_V2_RESULT.json', 'locator': 'resultado antigo; não reexecutado', 'sha256': '3072349afb00ab2c50d8d7740350f6662182ffea545ef363a4b84b3255853c88'}
- **plan**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\cache\\casa\\PLANO_EXPERIMENTAL_5SIGMA.md', 'locator': 'seções 2-4', 'sha256': 'f855e32523fede202ff17568c6d48d220205206bf61ccfa8203039865375f27f'}
- **checks**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\C0_C3_checks.json', 'locator': 'units, jump_rate, signed_modular_extensions, legacy_regression', 'sha256': '0592189981243c503a36967cd9285666e5120c804cca41bb23e233a6bd5230b0'}
- **gksl**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\verify_c0_c3.py', 'locator': 'dissipator e diagonalização independente', 'sha256': 'b232d1390e4b9a32c2f42ee3453e33fd4e34b73b0457c41fc5efb81b25f138fb'}
- **template**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\tgl_ringdown_template.py', 'locator': 'ringdown, convenção e recusa de desenrolamento indevido', 'sha256': 'ef1b4d69a687a84435ccd22d2643cb2917d5dfa9f4339ed075408a7e5b0d502c'}
- **mapping**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\C2_MAPEAMENTO_ANALITICO.md', 'locator': 'seções 1-6', 'sha256': '3b1b04893605f6a01a39e18567903d0a24d678a9fc0276e01b7d99efc9df503e'}
- **fisher**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\C5_FISHER.json', 'locator': 'records, mass_spin_free; previsão condicional, não dados', 'sha256': '71189d65f52d3530e71a1a5ce3a1603b69b57e6166c1fe3c0f7efd887c64fcf9'}
- **registration**: {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\REGISTRO_C4.json', 'locator': 'registro anterior à inspeção local, NÃO-CEGO', 'sha256': '2bebc171ddbcef43d7b50b9076dd806b64829a05a769b6e4fe23b73ec121ac59'}
- **lvk**: {'url': 'https://arxiv.org/html/2509.08099v1', 'locator': 'eqs. (1),(2), parágrafos do ajuste pSEOBNR e SNR; texto principal consultado, arquivo primário local ainda pendente'}
- **almost_periodic**: {'url': 'https://arxiv.org/abs/2406.00874', 'locator': 'abstract consultado: estados quase periódicos e espectro pontual em R_infinito'}