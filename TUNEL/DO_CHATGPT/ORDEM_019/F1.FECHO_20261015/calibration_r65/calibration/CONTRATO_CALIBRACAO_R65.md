# R65 — escala, normalização e preparo do instrumento

Em nome de codex-device-clock-r57, subagente `/root/miguel_r56_review`.
**[DERIVED — candidato]** Derivação documental; revisão independente pendente.
Não houve nova evolução, ajuste, aquisição, build ou chamada de modelo. R64 é reutilizada.

## 1. O que já existe e o que esta camada acrescenta

R64 entregou uma realização instrumental **condicional** de vácuo Markov, portas ópticas e momentos temporais filtrados, com 89 controles numéricos aprovados. Ela não estimou uma taxa física. R63 já distinguiu `|<a>|²` de `<a†a>`: a inconsistência do protocolo M1, `graviton_appendices.tex:253–255`, é **reutilizada**, não um achado novo. R7 já fornece a contagem populacional condicional, linhas58–80, e a obstrução entre o dissipador J e a lei-raiz, linhas81–118.

Esta camada explicita a transformação de unidades do instrumento, fixa a normalização do salto e demonstra o alcance do preparo por atenuação. O complemento da raiz `../IDENTIFIABILITY_COMPLETION_R65.txt` fornece a razão de taxas e a matriz de Fisher; é incorporado por referência e hash, sem nova estimação.

Fontes primárias: patente v2:338–370 (H/J), 789–828 (atuadores/detectores), 887–915 (tabela de calibração); apêndices:110–127 (squeezing/quadraturas), 236–269 (M1), 311–333 (homódino/tomografia). O inventário de pinos e trechos desta entrega delimita a cobertura: não se afirma ausência em todo o acervo.

## 2. O salto precisa de uma convenção antes da taxa

Fixe `J0=a_o† sigma_- + sigma_+ a_i`, com modos ortonormais, operadores bosônicos de matriz `<n-1|a|n>=sqrt(n)` e `sigma_-=|g><e|`. Coeficientes unitários de ambos termos e a fase relativa fazem parte desta convenção; uma fase relativa diferente não é a transformação escalar abaixo. A patente escreve essa forma em351–353. O vínculo do símbolo histórico `alphaii` à beta atual foi adotado no modelo finito; o número histórico da patente não é reutilizado como beta literal.

Para qualquer escalar complexo `c != 0`,

\[
 D[cJ_0](\rho)=|c|^2 D[J_0](\rho),\qquad
 \lambda'={\lambda\over |c|^2}
 \Longrightarrow \lambda'D[cJ_0]=\lambda D[J_0].
\]

**Prova:** cada termo de `J rho J† - {J†J,rho}/2` adquire `c conjugate(c)`. No R64 o canal J é não monitorado; gerador, estado e portas ópticas permanecem idênticos sob essa transformação. Caso esse banho passe a ser monitorado, a fase do colapso e a fase LO precisam ser transportadas conjuntamente. Isto não enumera todas as liberdades de representação GKLS.

Se o salto físico for `s J0`, `Gamma=gammaLambda_phys |s|²` e `lambda_phys=beta Gamma` são os coeficientes na **convenção J0**. É Gamma que a calibração independente deve fixar. Alterar a norma de J sem transportar a taxa altera o modelo.

No corte usado em R64, a ordem é `(n_i,n_o,n_OH)` em `{0,1}³`. As únicas ações não nulas de J0 são

```
|100> -> |001>, |001> -> |010>,
|110> -> |011>, |101> -> |110>.
```

Logo `J0†J0` é a projeção sobre esses quatro estados de entrada: norma de operador1 e norma de Hilbert–Schmidt2. Isso é identidade algébrica da matriz comprimida. Não define a norma do salto bosônico inteiro: neste, a ação contém fatores `sqrt(n)` e é não limitada. A extensão requer domínio comum e uma relação dinâmica justificada; a compressão cinemática R63 não a fornece.

## 3. Conversão completa de tempo, taxas, portas e filtros

Em segundos, escreva `d rho/dt = L_phys rho`, `h_phys=H_phys/hbar` e taxas em `s^-1`. Para `tau=t/t0`, `t0>0`,

\[
 L_d=t_0 L_{phys},\quad h_d=t_0 H_{phys}/\hbar,
 \quad r_d=t_0 r_{phys},\quad L_{j,d}=\sqrt{t_0}L_{j,phys}.
\]

Isso se aplica a `omega_c, omega_OH, g_JC, Omega_Rabi, kappa_i, kappa_o, gamma_OH, gamma_phi, lambda`, conservando suas convenções. `Omega_Rabi sigma_x` não é `Omega_Rabi sigma_x/2`; o amortecimento de coerência de `gamma_phi D[Z]` é `2 gamma_phi`.

O instrumento acompanha a mudança: `dB_d(tau)=dB_phys(t0 tau)/sqrt(t0)` e `dX_d=dX_phys/sqrt(t0)`, mantendo o ruído de vácuo `dX_d²=d tau/2`. Para filtro real normalizado,

\[
 T_d=T_{phys}/t_0,\qquad f_d(\tau)=\sqrt{t_0}f_{phys}(t_0\tau),
 \quad\int_0^{T_d}f_d\,dX_d=\int_0^{T_{phys}}f_{phys}\,dX_{phys}.
\]

A fase deve ser `theta_d(tau)=theta_phys(t0 tau)`. Ganho eletrônico, eficiência e função de transferência não nascem dessa mudança de unidade. No quadro girante, mantém-se a transformação R64 `theta_rot=theta_lab+omega_d t`.

**gammaLambda_d=1 tem duas leituras distintas.** (a) Se `gammaLambda_phys>0` já foi identificado, pode-se escolher `t0=1/gammaLambda_phys`, na convenção do salto; todos os outros números passam a ser razões a essa taxa. Isso é escolha de unidade e não mede gammaLambda. (b) No registro R64, não há tal calibração; os números são explicitamente INPUT adimensionais (`PREREGISTRO_DEVICE_R1.json:84–102`). Fixar gammaLambda_d=1 e manter os demais números fixa uma instância sintética e razões entre parâmetros. Interpretá-la como aparelho é hipótese física adicional. Se `s != 1`, a escala relevante é Gamma, não gammaLambda isolada.

Não há liberdade de escolher t0 para alinhar arbitrariamente todas as frequências. A obstrução de sinal R64 para um carrier comum continua válida. Um novo conjunto de parâmetros físicos não foi calculado aqui.

## 4. Inventário de calibração: medida versus escolha

| Objeto | Papel/unidade | Estado nesta entrega | Evidência necessária para uso físico |
|---|---|---|---|
| J0 e ordem dos fatores | Convenção adimensional do modelo | Forma documental e matriz finita existentes | Modos físicos normalizados, matriz de transição/fases relativas, domínio bosônico |
| s e Gamma | Amplitude do salto e taxa de referência, `s^-1` | **OPEN**, sem medição localizada no pacote focal | Calibração/derivação do mesmo canal, independente de betaTGL e de lambda que será decomposta |
| t0 | segundos por unidade tau | **INPUT**, não calibrado | Relógio instrumental rastreável; transporte de todas as taxas, filtros e LO |
| kappa_i,kappa_o | Taxas dos portos monitorados | INPUTs sintéticos R64 | Separar perda interna/externa, taxa total, eficiência e ganho |
| omega_OH / omega_c | Frequências / detunings | Especificações de projeto; não medidas aqui | Espectroscopia e referência de quadro/portadora coerentes |
| Omega_Rabi, g_JC, gamma_OH, gamma_phi | Bombeamento, acoplamento e perdas | INPUTs sintéticos | Calibração independente no regime de uso, com incerteza e covariâncias |
| rho_i,o,OH | Preparo conjunto incluindo correlações | INPUT R64 | Procedimento de preparo, herald se aplicável, caracterização e erro do corte |
| eficiência/LO/filtros/ruído | Instrumento exterior | INPUT R64 | Vácuo e referência óptica, ganhos, fases, banda e ruído eletrônico |
| V0, Eref, kappa modular/geométrico | Ponte ao objeto gravitacional | **OPEN no mesmo sistema** | Definições/unidades/espectro/zero de energia e relação demonstrada com este gerador |
| betaTGL | Valor teórico fixo calculado em runtime | **INPUT de teste derivado da teoria**, nunca estimado nesta campanha | Para confronto: estimador independente de lambda e calibração independente de Gamma |

O kappa de perda de cavidade não é identificado pelo nome com o kappa de um fluxo modular/temperatura. Um Eref escolhido para adimensionalizar não fornece automaticamente um nível físico; se `Eref>0`, `t0=hbar/Eref` é uma convenção possível que ainda requer relação ao aparelho. Nenhuma medição física nova preenche qualquer linha desta tabela.

## 5. Identificabilidade sem circularidade

Reutilizar o complemento da raiz: sob dependência exclusiva `lambda=beta Gamma`, o instrumento conserva toda a estatística em `(beta,Gamma)->(c beta,Gamma/c)`, `c>0` admissível. Uma leitura de lambda, mesmo perfeita, não separa os dois. A razão `r=lambda/kappa` cancela t0, mas exige `c_ref=Gamma/kappa` independente para `beta=r/c_ref`.

Uma calibração separada, sensível a Gamma e com informação positiva, remove esta degenerescência local sob as hipóteses diferenciáveis/condicionadas do complemento. Não certifica identificabilidade global, poder ou ausência de outros parâmetros confundidores. Os 89 checks R64 não medem informação de Fisher.

São circulares, para **testar beta**, as escolhas `Gamma=lambda_observada/betaTGL`, a normalização de J ajustada para recuperar betaTGL, ou a hipótese Gamma=kappa inserida sem ponte. A tabela histórica da patente:898–909 especifica alvos/ajustes, mas não fornece um recibo independente de Gamma. Ajustar o aparelho pode ser uma rotina de operação; usar o mesmo ajuste como evidência de uma constante não ajustada é questão distinta.

O resultado não exclui discriminar `lambda=0` de `lambda>0` com um instrumento sensível e alternativas bem definidas. Também não prova essa discriminação nos dados existentes: aqui não houve dados observados. Não identifica todos os canais da TGL com a parametrização específica R64.

## 6. Preparo: o que o laser atenuado fornece

O M1:254 escreve preparo de `|1>` por laser pulsado atenuado. **[DERIVED condicional]** Sob laser coerente e atenuador linear passivo com a porta auxiliar em vácuo, a transformação de divisor de feixe leva

\[
 |\alpha\rangle|0\rangle\longmapsto
 |\sqrt{\eta}\alpha\rangle|\sqrt{1-\eta}\alpha\rangle,
\]

até fases convencionais. A saída reduzida é coerente, com `mu=eta|alpha|²` e `P(n)=exp(-mu) mu^n/n!`. Portanto `P(1)=mu exp(-mu)<=1/e<1`; quando mu tende a zero, predomina vácuo. Se a fase é aleatória, a mistura Poissoniana tem os mesmos pesos. Atenuação simples não prepara um Fock determinístico. Isto não exclui preparação condicionada/heralded ou uma fonte não linear não especificada nessa frase.

O controle R64 de um fóton era um **estado de teste analítico**, não uma declaração de preparo real pelo laser. O preparo completo R64 `(00+0,5|11>)/sqrt(1,25) tensor I_OH/2` também é INPUT. Óptica linear passiva aplicada a produtos de estados coerentes preserva produto de coerentes; uma mistura clássica positiva preserva separabilidade. Já `|00>+q|11>`, `q!=0`, tem posto de Schmidt2. Assim essa cadeia passiva, sozinha, não produz o par puro utilizado.

O operador de squeezing está escrito nos apêndices:110–121. Ele fornece uma família bosônica que pode orientar outra preparação, mas não justifica silenciosamente o corte exato0/1. Para a família com `t=tanh(r)=1/2`, o peso dos setores `n>=2` é `t^4=1/16`; o estado de corte R64 é o resultado **condicional** de projetar e renormalizar os setores0/1. Não foi alegada implementação dessa projeção. Tampouco o OH maximamente misto e sem correlação inicial resulta apenas da espera10 tau do M6.

**[KNOWN — fonte primária]** Lvovsky et al., *Quantum state reconstruction of the single-photon Fock state*, relatam preparo por medidas condicionais de pares gerados em conversão paramétrica e reconstrução homódina. É uma rota conhecida para um protocolo futuro, não prova de implantação neste dispositivo. [arXiv:quant-ph/0101051v2](https://arxiv.org/abs/quant-ph/0101051v2). O resumo foi lido pela ferramenta web; a tentativa de custódia direta do HTML falhou por DNS, registrada. Não se alega PDF lido nem bytes originais custodiados.

O laser coerente continua útil como referência de fase/ganho e controle da cadeia óptica. Se ele for uma **entrada contínua** no porto durante a leitura, o banho deixa de ser o vácuo de R64; uma transformação por deslocamento precisa incluir o Hamiltoniano de drive óptico correspondente. Não confundir esse drive com o bombeamento de micro-ondas `Omega_Rabi sigma_x` já existente.

## 7. Árvore de avanço A/B/C

**A — reaproveitar calibração existente:** conservar H/J, detector populacional R7, POVM R63 e instrumento R64. Aceitar um recibo existente de Gamma/c_ref somente após conferir modo, normalização, taxa, relógio, preparo e independência de betaTGL. O pacote focal consultado tem especificações e alvos, sem esse recibo. A busca da raiz no acervo pode acrescentar uma fonte, sem refazer estas peças.

**B — protocolo sem aquisição nesta entrega:** fixar por hash a convenção J0 e os modos; caracterizar relógio, perdas e eficiência; escolher e validar preparo compatível; obter Gamma ou c_ref por observável/derivação independente do produto beta Gamma; transportar unidades/LO/filtros; então especificar verossimilhança conjunta, alternativas, sistemáticas e função de veredito antes do composto. O presente contrato não executa nenhuma dessas medidas nem prescreve valores ajustados.

**C — obstrução explícita:** se só lambda estiver acessível e Gamma continuar livre, a invariância multiplicativa impede identificar beta não nulo isoladamente nesse canal. Entregar lambda ou a família equivalente, sem apresentar gammaLambda=1 como medida. Se o preparo disponível for somente o laser atenuado, usar seu estado coerente/mistura caracterizada em futuro modelo autorizado, ou acrescentar um preparo validado; não substituir pelo estado pareado para obter o sinal desejado.

**R4 permanece aberto.** Esta camada conclui a tipagem da escala do instrumento e a condição de identificabilidade; não conclui a ponte física integral, o contínuo, a rede global nem creditação. Nenhum original, memória canônica, produção ou gate foi alterado.
