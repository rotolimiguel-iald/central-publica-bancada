Partindo da hipótese de que a TGL não descreve corretamente a natureza, os resultados que a sustentariam seriam aqueles que contradizem suas previsões centrais. A teoria é declaradamente falsificável e organiza seu estatuto epistêmico em camadas rígidas — **PROVADO** (teorema no kernel Lean 4), **ARMADO** (previsão falsificável), **INCONCLUSIVO** (teste sem veredito) e **CONFIRMADO** (juízo sobre a natureza, proibido por teorema). A hipótese de falseamento incide justamente sobre as camadas **ARMADO** e **INCONCLUSIVO**: são os pontos onde a natureza ainda não falou.

## 🔬 O que poderia falsear a TGL

### 📉 Dephasing em neutrinos com índice espectral errado

A TGL prevê que o dephasing GKSL escala quadraticamente no infravermelho, \(\Gamma_\omega = \frac{1}{2}\beta\tau_\star\omega^2\), com \(n = -2\). A constante \(\beta_{\text{TGL}} = \alpha\sqrt{e} \approx 0{,}0120313004\) é derivada do axioma único e não ajustável.

**Observação que falsearia:** se experimentos de oscilação de neutrinos (JUNO, DUNE, Hyper-Kamiokande) medissem um dephasing com índice espectral \(n \neq -2\) — por exemplo, \(n = -1\) (ruído \(1/f\)) ou ausência de dephasing dentro da sensibilidade —, a lei \(\Gamma \sim \omega^2\) estaria refutada.

**Alcance:** este é o teste mais direto e o único que o próprio framework classifica como **ARMADO**. O déficit de alcance é de cerca de \(10^{10}\) ordens de magnitude: a previsão é real em forma, mas hoje inatingível. Se um dia for medida, a TGL cai ou se confirma nesse ponto.

**O que continuaria válido como construção matemática:** a derivação de \(\beta_{\text{TGL}} = \alpha\sqrt{e}\) a partir do meio-nat \(S_\partial = \frac{1}{2}\) e a estrutura GKSL com saltos \(L_k = \sqrt{\beta}\sqrt{K_\partial}_{(k)}\) permaneceriam como teoremas formais no kernel Lean. A *forma* da lei de dephasing continuaria sendo um resultado matemático; apenas sua *aplicação à natureza* estaria refutada.

### 🌌 Cosmologia: equação de Friedmann modificada

A lagrangiana TGL contém uma única peça nova: \(\mathcal{L}_{\text{modular}} = \mathcal{L}_{\Lambda\text{CDM}} \cdot \beta_{\text{TGL}} \cdot |1 + w_{\text{eff}}(z)|\). Isso altera a expansão cósmica de forma dependente do redshift.

**Observação que falsearia:** se levantamentos cosmológicos de próxima geração (Euclid, DESI, LSST) medissem a história de expansão \(H(z)\) e encontrassem desvios sistemáticos em relação à TGL, ou se a equação de estado efetiva \(w_{\text{eff}}(z)\) não correspondesse à forma \(|1 + w_{\text{eff}}|\) prevista, a modificação modular estaria excluída.

**Alcance:** este é o canal onde a TGL é mais vulnerável a dados existentes. O framework já registra que os "rostos cosmológicos são os canais vivos", enquanto o dephasing está a \(10^{10}\) ordens do alcance. Um desvio cosmológico consistente com \(\Lambda\)CDM puro e incompatível com a correção modular falsearia a única peça nova da lagrangiana.

**O que continuaria válido como construção matemática:** a estrutura \(\mathcal{L}_{\text{TGL}} = \mathcal{L}_{\text{matéria}} + \mathcal{L}_{\text{campo}} + \mathcal{L}_{\text{grav}} + \mathcal{L}_{\text{modular}}\) e a equação de movimento \((\Box - m_\Psi^2 - \xi R)\Psi = \beta_{\text{TGL}} K_\partial \Psi\) permaneceriam como objetos formais coerentes. A lagrangiana não deixaria de ser matematicamente bem-definida; apenas não descreveria o universo.

### ⚖️ Gravidade quântica: ausência de gráviton ou violação da equação de Einstein

A TGL prova formalmente que a equação de Einstein emerge de três hipóteses \(H_1 \wedge H_2 \wedge H_3\) no kernel Lean, com 6.657 teoremas e zero `sorry`. O portão final admite que "dados mais sensíveis poderiam revisar".

**Observação que falsearia:** se a natureza exibisse violação da equação de Einstein em regimes onde a TGL prevê sua emergência exata, ou se o setor de spin-2 linearizado não correspondesse ao gráviton sem massa, a derivação formal estaria desacoplada da realidade.

**Alcance:** este é o teste mais indireto, porque a TGL não faz uma previsão *distinta* da relatividade geral no regime já testado — ela *recupera* a relatividade geral como limite. O falseamento viria de uma discrepância em um regime onde a TGL prevê desvio (fronteira modular) e a relatividade geral pura não.

**O que continuaria válido como construção matemática:** a *prova formal* de que \(H_1 \wedge H_2 \wedge H_3 \implies \text{pentad}\) é um resultado matemático independente da natureza. O kernel Lean permaneceria correto como artefato formal: ele prova uma implicação, não uma verdade empírica. A estrutura de álgebra tipo III₁, o gerador modular \(K_\partial\) e a dualidade fronteira↔bulk continuariam como matemática válida, mesmo que a física correspondente fosse falsa.

## 🧮 O que o falseamento *não* destruiria

A TGL é construída de modo que a camada **PROVADO** é imune ao falseamento empírico. Se a natureza contradizer a TGL:

| Camada | Estatuto após falseamento |
|---|---|
| **Kernel Lean (6.657 teoremas, zero `sorry`)** | Permanece **matematicamente válido**. A prova de que \(H_1 \wedge H_2 \wedge H_3 \implies \text{pentad}\) é um teorema, não uma observação. |
| **Derivação de \(\beta_{\text{TGL}} = \alpha\sqrt{e}\)** | Permanece como **construção formal**: o meio-nat \(S_\partial = \frac{1}{2}\) seleciona \(\sqrt{e}\), independentemente de a natureza usar esse custo. |
| **Estrutura GKSL com \(L_k = \sqrt{\beta}\sqrt{K_\partial}_{(k)}\)** | Permanece como **exemplo matematicamente coerente** de dissipação canônica em álgebra tipo III₁. |
| **Dualidade \(H_{\text{eff}}\|_\partial = 0 \leftrightarrow H_{\text{bulk}}\) limitado** | Permanece como **resultado estrutural** sobre a impossibilidade de Hamiltoniano limitado em fatores III₁, um teorema de Connes. |
| **Lagrangiana \(\mathcal{L}_{\text{TGL}}\)** | Permanece como **objeto formal bem-definido**, com equações de movimento deriváveis. |

O que cairia seria a **ponte semântica** entre esses objetos formais e a natureza. O framework já proíbe, por teorema próprio, a operação "CONFIRMADO" — precisamente porque reconhece que a passagem do formal para o empírico não é automática.

## 💎 Síntese

A hipótese de que a TGL não descreve a natureza é **cientificamente operacional**: ela aponta para os canais **ARMADOS** (dephasing em neutrinos) e **INCONCLUSIVOS** (cosmologia, ringdown) como os pontos de teste. Um falseamento nesses canais não invalidaria o kernel Lean, a derivação de \(\beta_{\text{TGL}}\) nem a estrutura GKSL — esses permaneceriam como **matemática válida**. O que cairia é a reivindicação de que essa matemática *é* a física. A régua do próprio framework já antecipa isso: **"o número corrige a frase, sempre"** — e o número, nesse caso, seria a observação que contradiz a previsão.