# R64 — do estado conjunto às correlações do campo exterior

## Alcance e reutilização

**[KNOWN]** Método de gerador inclinado e momentos de sinais filtrados: Guilmin, Rouchon e Tilloy, arXiv:2212.00176v2, equações 46, 50, 57 e 63–66; HTML custodiado em `../literature`, com pino no plano. **[DERIVED condicional]** Aplicação ao gerador finito já existente da IALD. Reutilizam-se `liouvillian` e as funções puras extraídas por AST em R62. Não se reconstrói o gerador 64×64 nem se repete a campanha de R62/R63.

O levantamento focal de oito fontes não encontrou uma implementação pronta do campo exterior. R7 já dá resposta causal de bombeamento para contagem, mas não esta correlação de dois tempos. R57 já dá o quadro girante sob `LAB_PHASE_LOCKED_DRIVE`. R63 fornece a distinção entre POVM física comprimida e Pauli, com o cancelamento do defeito de segundo momento no decoder cruzado. Nenhum desses nomes é usado como substituto da dilatação abaixo.

## Hipótese nomeada do instrumento

**[INPUT — H_MARKOV_VACUUM_PORTS]** Escolhe-se uma realização unitária/dilatação Markov de vácuo para os cinco operadores de colapso do modelo, com banhos independentes. Monitoram-se as portas

\[
L_i=\sqrt{\kappa_i}\,a_i,\qquad L_o=\sqrt{\kappa_o}\,a_o.
\]

Os outros canais, `√γ σ−`, `√γφ Z` e `√(βγΛ)J`, permanecem no gerador e não são monitorados. O código original guarda pares `(taxa,operador)`: as raízes entram nas portas de leitura, sem aplicá-las duas vezes ao dissipador. Mantém-se a convenção `γφ D[Z]`, cujo amortecimento de coerência é `2γφ`.

Um GKLS isolado não seleciona fisicamente essas portas, o estado do banho ou a realização instrumental. Esses dados adicionais, eficiência ideal, ganho e referência dos osciladores locais são hipóteses explícitas. A existência de uma representação Markov de uma dinâmica finita não prova que os terminais da patente realizem essa representação.

Para a corrente normalizada como quadratura, defina

\[
\mathcal M_{j,\theta}\rho=
\frac{e^{-i\theta}L_j\rho+e^{i\theta}\rho L_j^\dagger}{\sqrt2}.
\]

O incremento normalizado `dXj=dYj/√2` tem ruído de vácuo `dXj dXk=δjk dt/2`. Para `t>s`, a parte regular da correlação é

\[
K_{jk}(t,s)=\operatorname{Tr}\!\left[
\mathcal M_{j,\theta_j(t)}e^{(t-s)\mathcal L}
\mathcal M_{k,\theta_k(s)}\rho(s)\right].
\]

Há ainda `δjk δ(t−s)/2`. No triângulo temporal oposto trocam-se as etiquetas completas de tempo e detector. Não se usa ρ(t) no lugar de ρ(s) nem se substitui a inserção de superoperador por um produto de médias. Este é o contrato de um sinal de medida contínua, condicionado à dilatação nomeada.

## Modos filtrados e ODE reutilizável

Para filtros reais de norma L² um, `Qj=∫₀ᵀ fj(t)dXj(t)`. No banho de entrada, o incremento de Wiener tem dimensão √tempo; um filtro com dimensão tempo⁻¹/² fornece uma quadratura adimensional. Os tempos e taxas da instância computacional continuam adimensionais.

Transportam-se matrizes auxiliares completas, com `u(0)=v(0)=0`:

\[
\dot\rho=\mathcal L\rho,\qquad
\dot u_j=\mathcal Lu_j+f_j\mathcal M_j\rho,
\]
\[
\dot v_{jk}=\mathcal Lv_{jk}
 +f_j\mathcal M_ju_k+f_k\mathcal M_ku_j
 +\frac{\delta_{jk}}2f_jf_k\rho.
\]

Então `E Qj=Tr uj(T)` e `E QjQk=Tr vjk(T)`. A covariância subtrai o produto das médias. Cada bloco conserva a dimensão integral do sistema: OH e suas correlações não são fatorados. Os blocos auxiliares de momentos não são, em geral, estados positivos; positividade/traço unitário são exigidos de ρ. A matriz clássica de covariância das duas correntes compatíveis deve ser positiva.

Quatro aquisições distintas, com o mesmo preparo, filtros e duração, usam as fases XX, PP, XP e PX. Suas correlações cruzadas permitem o mesmo decoder algébrico de R62 para `C_f=⟨B_i(f)B_o(f)⟩` e `B_f=⟨B_i(f)†B_o(f)⟩`. **São modos de saída temporais**, sob H_MARKOV_VACUUM_PORTS, e não os operadores instantâneos de cavidade. Não se atribuem simultaneamente X e P incompatíveis a uma mesma aquisição. A cinemática de Fock/POVM de R63 continua aplicável ao contrato de modos; não se conclui um entrelaçamento da dinâmica finita com o GKLS bosônico da patente.

## Controles fixados antes da execução

O plano pinado estabelece DOP853, `rtol=1e−10`, `atol=1e−12`, tolerância analítica `1e−8`, identidades matriciais `1e−12`, estados/partes imaginárias `1e−9` e limiar de recusa dos controles adulterados `1e−5`.

O controle de referência separado usa `H=0`, `L=√κ a`, `κ=T=1`. Um fóton inicial emite a probabilidade `p=1−e^{−κT}` na janela; com filtro casado `f(t)=√κ e^{−κt/2}/√p`, a média é zero e o segundo momento é `1/2+p`. Para vácuo, é `1/2`. Omitir o termo de ruído deve produzir a recusa por diferença de `1/2`.

Dois portos independentes do mesmo controle, preparados em `(00+e^{iπ/4}11)/√2`, devem produzir `C_f=p e^{iπ/4}/2`, `B_f=0`. A fase não foi escolhida por ajuste: é uma entrada sintética para verificar ambas componentes do decoder. A troca de sinal imaginário deve falhar. Um controle pontual `t=0,8>s=0,2` confere `K(t,s)=κ e^{−κ(t+s)/2}` e recusa o uso incorreto de ρ(t).

Na instância completa, mantêm-se todas as taxas e bombeamento de R62, `γΛ=1` explícito e `β=ALPHA_FINE_CODATA_2018·√e` calculado em runtime. O preparo é `(00+0,5·11)/√1,25` com OH maximamente misto. O filtro é retangular normalizado, T=1. Não se faz varredura, ajuste ou medição de β. Desligar termos é permitido apenas nos controles analíticos separados, nunca para simplificar a instância completa.

## Quadro girante, oscilador local e unidades

Com `R=e^{+iχN}` e `ρrot=RρlabR†`, um abaixador satisfaz `RLR†=e^{−iχ}L`. Logo

\[
R\,\mathcal M_{\theta_{lab}}(\rho_{lab})R^\dagger
=\mathcal M_{\theta_{lab}+\chi}(\rho_{rot}).
\]

Para `χ=ωd t`, a fase correta é `θrot=θlab+ωd t`. Um LO casado, `θlab=θ0−ωd t`, remove a portadora da leitura rotativa. Isso não transforma a portadora externa em relógio interno inferido. A implementação verifica a identidade de fase; não relabela as frequências constantes do modelo como detunings físicos.

Há uma obstrução de sinal à tentativa de calibrar os números sintéticos antigos por simples troca de unidade/carrier. Se ambos fossem detunings do mesmo carrier, com escala temporal positiva t0, teríamos `ΔOH−Δc=t0(ωOH−ωc)`. Os números fixados dão `1,2−1>0`. Para a identificação proposta do modo de cavidade com a faixa óptica do dispositivo, na qual `ωOH<ωc`, o lado direito é negativo. Portanto essa identificação não se obtém por um carrier comum e unidade positiva. Uma nova instância com parâmetros físicos independentes pode ser construída; esta execução não faz tal calibração.

## O que o resultado pode estabelecer

Um PASS verifica a consistência numérica do instrumento condicional, sua normalização, ordem temporal e decodificação sobre o estado conjunto, com controles analíticos. Não demonstra que o aparelho possua o banho/portas escolhidos, que `G_OH` seja derivado, que `γΛ` esteja calibrado ou que β tenha sido inferido. R4, Poincaré, contínuo físico, creditação e gate não são encerrados por esta camada. O resultado e a revisão independente seguem em arquivos próprios, sem alterar as evidências anteriores.
