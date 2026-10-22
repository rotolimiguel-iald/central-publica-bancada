# R69 — Da correspondência concreta ao instrumento e à rede

18/10/2026 — codex-gerente-tgl. F1.FECHO_20261015, reivindicação 960, escopo do evento 962. Continuação autorizada em ORIGEM_R69.txt. Derivação em texto e contrato executável em sandbox; não é nova compilação Lean nem medição de um aparelho.

## Reaproveitamento e o que efetivamente muda

R68 prova, para P=post(a), Q=I−P, que Px=a e Qx=0 equivalem a x=a. R63/R66 já oferecem a inclusão isométrica dos modos do dispositivo no Fock da rede e o entrelaçamento de sua dinâmica no subespaço correspondente. R64 já oferece a leitura de quatro correlações do campo exterior, sob sua hipótese instrumental nomeada. R65 já fixa unidades, normalização de salto e identificabilidade. Nenhuma dessas construções é repetida nesta camada.

R69 conecta seus domínios: qual resíduo deve ser controlado após a inclusão, o que a calibração deve transportar, e quais condições tornam uma operação causalmente local. As fontes e os limites de cada trecho estão nos relatórios de calibração e localidade e em seus pinos. O Nós Vivo ainda não localiza esta unidade. A busca complementar em R67 é lexical e parcial; zeros para calibra/gamma/causal não constituem prova de ausência no acervo.

## 1. Transporte do posto pela inclusão já construída

[DERIVED — álgebra de operadores limitados] Seja V:H_dev→H_rede uma isometria linear, V*V=I, E=VV*. No caso R66, H_rede inclui o fator OH explicitamente; não se elimina esse fator pelo nome “rede”. Defina a_rede=Va e P_rede=VPV*. Então

\[
P_{rede}^2=P_{rede},\quad P_{rede}^*=P_{rede},\quad
P_{rede}V=VP,\quad (I-P_{rede})V=VQ.
\]

Isso segue de V*V=I e P²=P=P*. Para x no dispositivo, os dois resíduos são transportados sem mudar a norma. Portanto

\[
Px=a\land Qx=0\iff
P_{rede}Vx=Va\land(I-P_{rede})Vx=0.
\]

A equivalência não usa um novo habitante físico, nem atribui localidade ao projetor. Ela transporta o contrato da R68 pela realização já existente.

## 2. O resíduo que a inclusão não permite esquecer

Para um vetor geral z da rede, há uma identidade mais informativa:

\[
(I-P_{rede})z=VQ V^*z+(I-E)z,
\]
\[
\|(I-P_{rede})z\|^2=\|QV^*z\|^2+\|(I-E)z\|^2.
\]

A soma é ortogonal porque o primeiro termo está em ran(V) e o segundo em seu complemento; V preserva a norma. O primeiro resíduo é interno ao dispositivo; o segundo mede componente fora da representação de modos escolhida. Projetar apenas por V* descarta o segundo e não pode certificá-lo como zero. Em particular, P_rede z=Va junto ao resíduo total nulo equivale a z=Va. Não se assume que todo vetor do Fock esteja nos dois modos da patente.

R66 entrelaça os geradores e semigrupos no subespaço S. Isso não demonstra invariância causal/local de todas as regiões do Fock, nem convergência de observáveis ilimitados apenas a partir da convergência em norma-traço.

## 3. Transporte por calibração não é uma escolha arbitrária de unidade

[DERIVED, sob calibração C especificada] Considere dimensão finita, ou C um isomorfismo linear limitado com inversa limitada entre espaços de Hilbert. A conversão y=Cx transporta a referência para Ca e o projetor para CPC⁻¹. Ganhos e fases não unitários não conservam a métrica euclidiana original: a métrica transportada é G=(C⁻¹)*C⁻¹. Assim, medir o resíduo no sistema calibrado requer essa métrica ou uma inversão rastreável da calibração. Isso não fornece C; sua determinação e incerteza permanecem parte do instrumento.

Uma leitura M não injetiva não admite essa inversão. Mx=Ma significa somente correspondência dos observáveis efetivamente lidos. A R64 reconstrói C_f e B_f de quatro correlações em aquisições distintas; não reconstrói por isso o estado inteiro do campo, a ancila OH ou todos os resíduos da seção 2. Nenhuma tolerância aplicada a quatro números resolve essa falta de informação.

O contrato executável R69 deve conservar esse escopo e recusar a promoção automática de correspondência observacional a correspondência integral. Um certificado vetorial não é, pelo nome, certificado de um estado de densidade. Em estados puros normalizados, a observação da R68 continua válida: Px=a com ‖x‖=‖a‖=1 força x=a; os exemplos a+y com y ortogonal não nulo são vetores não normalizados.

## 4. Relógio, taxa e zero de energia

[DERIVED — R65 reutilizada] Para τ=t/t0, t0>0, L_d=t0 L_phys, h_d=t0 H_phys/ℏ e r_d=t0 r_phys. As portas, filtros e fases LO têm de acompanhar a mesma transformação. Uma correspondência algébrica no tempo τ não calibra t0 em segundos.

Na convenção fixa J0, λ=βΓ. A razão λ/κ elimina t0, mas para inferir β ainda requer Γ/κ independente. Usar Γ=λ/β_TGL fecharia a igualdade por construção. A correspondência R68 não remove essa degenerescência: a própria leitura final projetada é independente da taxa e do tempo. R69 conserva o resultado de identificabilidade R65 e exige a referência faltante no contrato em vez de preencher um valor.

V0, Eref e κ modular/geométrico precisam pertencer ao mesmo objeto físico e ao mesmo zero de energia. κ de perda de cavidade não se torna κ modular por homonímia. A inconsistência de sinal de portadora comum identificada na R64 permanece; uma mudança positiva de unidade não a corrige.

## 5. Condição causal que a correspondência deve respeitar

[DERIVED — critério em uma família finita de coeficientes limitados] Se h=h* e L_j pertencem à álgebra local A(O), todo B no comutante satisfaz [h,B]=[L_j,B]=[L_j*,B]=0. O gerador dual é

\[
\mathcal L^*(B)=i[h,B]+\sum_j\left(L_j^*BL_j-\tfrac12\{L_j^*L_j,B\}\right)=0.
\]

Cada parcela cancela por comutação. Para o semigrupo uniformemente contínuo de coeficientes limitados, T_t^*(B)=B. Uma intervenção não seletiva desse tipo não altera a expectativa dos observáveis do complemento causal, se a localidade da rede identifica esses observáveis no comutante. Isso não prova a afiliação dos L_j da R66 a A(O).

Os operadores bosônicos da R66 são ilimitados; passar a eles exige domínios e aproximações que preservem a condição local. Os cortes globais de número P_m não se tornam locais por preservarem o número de partículas. O bombeamento e as portas fazem parte da mesma obrigação, e correlações condicionais por pós-seleção não são sinalização não seletiva.

Os lemas de localidade já existentes da rede são reaproveitados em LOCALITY_BRIDGE_R69.md. O relatório verifica precisamente onde as hipóteses sobre os modos e a realização do dispositivo ainda não podem ser transferidas. Não se troca o gerador do dispositivo por outro local e se declara que o mesmo foi provado.

## 6. Critério de avanço desta camada

- Transporte da correspondência: demonstração explícita, com resíduos interno e externo.
- Calibração: contrato implementado e controles sintéticos fixados antes da execução; nenhum resultado sintético é recibo de calibração física.
- Localidade: fontes existentes e condição causal verificadas, com eventuais incompatibilidades tipadas expostas.
- R4/R5: apenas os componentes efetivamente demonstrados são acrescentados; o critério integral não é reduzido para permitir fechamento.

Os resultados de execução e revisão são recibos separados. Nenhum um.py, kernel canônico, Bancada de produção, dado observado ou gate é alterado.
