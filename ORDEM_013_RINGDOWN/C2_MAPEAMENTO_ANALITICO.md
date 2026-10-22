[DERIVED condicional; INPUT na identificação física; OPEN na seleção da partição e do desenrolamento]

# Do gerador à leitura de uma onda

21/09/2026. Esta nota complementa a errata da v369 e o plano experimental de 13/09; não acrescenta uma taxa fundamental ao programa nem modifica seu gate.

## 1. O que o gerador determina

Em uma regularização finita, para L=L†=f(H),

    D_L(rho)_ij = -(f(E_i)-f(E_j))² rho_ij / 2.

Segue diretamente de L rho L - {L²,rho}/2. As populações são conservadas. Uma constante real adicionada a L cancela no gerador, embora mude Tr(L² rho). Essa taxa de saltos é dependente da representação do desenrolamento e não é a taxa de coerência. O oráculo em `verify_c0_c3.py` constrói a matriz de Liouville independentemente da fórmula espectral.

Para K positivo e tempo modular s adimensional:

    L=sqrt(beta)*sqrt(K), gamma_ij(s)=beta*(sqrt(k_i)-sqrt(k_j))²/2.

A passagem a segundos requer ds/dt e uma identificação de k_i. K=-log Delta é bilateral; sqrt(K) não é uma raiz autoadjunta positiva. K_+ e |K| dão leis distintas (matrizes medidas em C0_C3_checks.json). Uma densidade de estado pode ser representada no predual/core de tipo III; isso não fornece uma matriz densidade ordinária relativa a um traço normal semifinito na própria álgebra regional de tipo III.

## 2. Lei quadrática e oscilador efetivo

Assumindo H=ħ omega N para um modo efetivo, e um relógio físico tau_star:

    dot rho = -i[H,rho]/ħ - beta*tau_star*[H,[H,rho]]/(2 ħ²),
    rho_nm(t) = exp[-i omega(n-m)t - Gamma*(n-m)²*t] rho_nm(0),
    Gamma = beta*tau_star*omega²/2.

Logo <a>(t)=<a>(0)exp[-i omega t-Gamma t], enquanto <N>(t)=<N>(0). Acrescentar o envelope dissipativo GR exp(-t/tau_GR) é uma segunda hipótese, efetiva: não identifica um QNM aberto com um autovetor normalizável de um Hamiltoniano autoadjunto de sistema fechado.

CONVENÇÃO: Gamma amortece a amplitude média; a potência coerente cai com 2 Gamma. A energia total do oscilador não é dissipada por este termo de dephasing.

Sob essas hipóteses:

    h_mean(t)=A exp[-(1/tau_GR+Gamma)t] cos(omega*t+phi),
    x=Gamma*tau_GR,
    delta_tau=-x/(1+x), delta_f=0.

O delta_f do rito V2 é um resultado do estimador antigo, não uma previsão de deslocamento do gerador. A calibração de viés de frequência permanece necessária.

## 3. Uma realização não é a média

Um desenrolamento unitário admissível da lei quadrática é o jitter gaussiano de tempo. Escolhendo-o explicitamente:

    z(t)=A exp(-t/tau_GR) exp[i(omega*t+phi+sqrt(2 Gamma)*W_t)].

E[z] tem o envelope anterior, mas |z|²=A² exp(-2t/tau_GR) em cada trajetória. A potência que sai da média coerente permanece nas flutuações:

    E|z|²-|Ez|²=A² exp(-2t/tau_GR)(1-exp(-2Gamma*t)).

A correlação é E[z(t)z*(u)]=A² exp[-(t+u)/tau_GR] exp[i omega(t-u)] exp[-Gamma|t-u|]. Para a quadratura real, E[h(t)²] contém também um termo oscilante em 2 omega, amortecido por 4 Gamma; só a média de ciclo coincide com metade da potência complexa. Não se pode substituir essa covariância por perda determinística de energia.

Um ajuste de seno amortecido a uma trajetória pode apresentar deslocamentos de frequência e tempo de amortecimento dependentes de janela, estimador e ruído. Por isso `prediction(observable='realization')` recusa fabricar valores universais. `ringdown(observable='brownian_phase')` fornece uma realização com semente explícita, distinta do template de ensemble. O gerador GKSL não escolhe sozinho qual dessas descrições corresponde ao strain observado. A verificação de recuperação em ruído colorido ainda é pendente.

## 4. Lei-raiz no campo coerente

Sob a escolha dimensional f(N)=sqrt(beta*omega)*sqrt(N), um estado coerente de ocupação média Nbar tem

    <a>(t)/<a>(0) = exp(-i omega t) sum_n Pois(Nbar;n)
                     * exp[-beta*omega*t/(2(sqrt(n+1)+sqrt(n))²)].

Isso não é em geral uma exponencial. Sua taxa inicial é a média de Poisson das taxas adjacentes. Para Nbar grande, gamma_initial ~ beta*omega/(8 Nbar), verificado até Nbar=256 e extrapolado analiticamente. Para Nbar~10^78, a razão gamma_initial/omega é ~beta/(8*10^78), e não beta/2. A escolha Nbar=E_mode/(ħ omega) pressupõe quantização e energia do modo; massa total do remanescente e distância não determinam essa energia sem uma lei de excitação. Não confundir a coerência |0><1| com um campo macroscópico coerente.

## 5. Massa, spin e distância

No ramo B já existente, t_M=GM_det/c³, omega=w(chi)/t_M e tau_GR=t_M/d(chi). Assim

    Gamma=beta*w(chi)²/(2t_M),
    Gamma/omega=beta*w(chi)/2,
    x=beta*w(chi)²/(2d(chi)),
    delta_tau=-x/(1+x).

É uma previsão condicional completa de massa/spin para esse relógio INPUT. D não entra na taxa local; entra na amplitude/SNR e, por um modelo cosmológico, na conversão de massa de fonte para massa de detector. A fonte pode emitir a distâncias diferentes sem alterar sua dinâmica local. No ramo A com relógio da fonte t_P, tau_star,det=(1+z)t_P. A regressão antiga conserva explicitamente sua convenção de relógio de detector.

Para propagação FLRW com ruído local independente [CONJECTURE], a atenuação da coerência espectral é

    Xi=beta*tau_star,source*omega_obs²/2 * integral_0^z (1+z')/H(z') dz'.

Ela depende de D através de z e da cosmologia. Não é automaticamente uma taxa adicional de ringdown na janela de milissegundos. O espectro e sua referência também precisam ser especificados. Aplicar o relógio da massa da fonte em todo o trajeto seria uma nova hipótese não local dependente da fonte, não uma consequência dimensionalmente proibida nem uma lei já derivada.

## 6. Identificabilidade

Um único modo fornece dois parâmetros de forma, frequência e amortecimento. Com M, chi e deformação livres, existe uma degenerescência local: a derivada da forma de onda em relação à deformação pertence ao espaço gerado pelas derivadas em M e chi. Amplitude e fase livres não resolvem isso. As previsões Fisher com M/chi fixos são limites otimistas; um teste físico precisa de informação adicional do inspiral, de outro modo ou de priors independentes. Não se deve contar duas vezes o mesmo inspiral.

Referências de convenção conferidas: [LVK, eqs. (1) e (2), GW250114](https://arxiv.org/html/2509.08099v1); [Simon–Jaksch, abstract consultado, ruído global e referência](https://arxiv.org/abs/quant-ph/0406007). A derivação algébrica acima é desta bancada; a escolha do oscilador e do desenrolamento é explícita, não atribuída a esses artigos como conclusão sobre a TGL.
