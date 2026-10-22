# R79 — primeira variação bosônica, sonda linear e erro de corte

**[DERIVED — demonstração analítica candidata, NOT_LEAN]** Autor: subagente r69_calibration_bridge, em nome do trabalho coordenado por codex-gerente-tgl. 18/10/2026. Claim967, escopo983; project/check R4 revisão536 ready. Nenhuma campanha nova foi executada. Esta nota acrescenta a estimativa que a R78 explicitamente não reivindicava; não altera seus resultados finitos.

## 1. Hipóteses reutilizadas e nova inserção

Reutilizam-se H=Γ_s(C²)⊗C²_OH, N=n_i+n_o+n_e, P_r=1_[0,r](N), T₀(t) conservativo CPTP da R66, e B=-i[h_d,.], b=2|Ω|. T₀ contrai norma-traço inclusive para operadores complexos e preserva P_r T₁ P_r. B tem norma≤b e aumenta o suporte bilateral no máximo em um. O gerador e o salto único J=A+B da fonte permanecem integrais; a letra B da perturbação limitada nesta nota não separa o banho J.

Fixe ρ₀=P_m0 ρ₀ P_m0, Trρ₀=1, m0 inteiro, e tempo T<∞. A sonda da R78 é h_probe=c(a_i+a_i†)/sqrt(2) ou c(a_i-a_i†)/(i sqrt(2)), c real = gain_in sqrt(κ_i), sem calibração material reivindicada. Sua inserção é V(X)=-i[h_probe,X]. Para envelope real u∈L¹[0,T], h_epsilon(t)=h+h_probe epsilon u(t). R78 usa u=1; fixar u antes do teste, sem estado inicial dependente de epsilon.

Para X=P_r X P_r,

    ||V(X)||₁ ≤ 2 ||h_probe P_r|| ||X||₁
               ≤ sqrt(2)|c|(sqrt(r)+sqrt(r+1)) ||X||₁
               ≤ a sqrt(r+1) ||X||₁,       a=2sqrt(2)|c|.                 (1)

A igualdade entre as normas do lado esquerdo/direito do produto usa h_probe simétrico sobre o domínio de partículas finitas. V(X) fica em P_(r+1) T₁ P_(r+1). As mesmas estimativas valem para operadores comprimidos. **Ao contrário da inserção de leitura M da R75, V pode aumentar o suporte.** Essa é a mudança de índice que impede copiar a cota antiga.

## 2. A variação existe como derivada, não apenas como limite formal

Antes de calcular a resposta, pode-se construir a evolução real perturbada como limite dos cortes. Escreva W_epsilon(t)=B+epsilon u(t)V. Sobre suporte P_r, sua norma é≤[b+|epsilon|a|u(t)|]sqrt(r+1), com crescimento de suporte≤1. Um termo Dyson de ordem k intercalado com T₀, aplicado a X suportado em P_m0, tem norma-traço no máximo

    ||X||₁ * w^k/k! * sqrt((m0+k)!/m0!),
    w=bT+|epsilon|a ||u||_L1.                                           (2)

A integração ordenada do produto dos coeficientes dá w^k/k!; os fatores de suporte dão sqrt(prod_(j=1)^k(m0+j)). A razão de termos sucessivos é w sqrt(m0+k+1)/(k+1)→0. Portanto a série converge absolutamente, uniformemente para t≤T e epsilon em compacto, também após multiplicar por qualquer potência fixa de m0+k. Para k≤m−m0 cada termo coincide exatamente com o do corte m; as duas caudas de (2) tendem a zero.

Para epsilon real, cada propagador finito é CPTP. O limite em norma-traço sobre D₀=∪P_rT₁P_r é uma contração e estende-se unicamente por densidade a T₁(H). Traço, positividade completa e continuidade forte passam ao limite. A composição passa pelo limite forte de contrações; para u=1 obtém-se semigrupo, para u variável a família de propagadores com a composição nos intervalos correspondentes. Não se alega aqui unicidade entre todas as extensões possíveis de uma expressão formal GKLS: é a realização definida por este limite compatível.

Cada termo Dyson é polinomial em epsilon. A série, e a série com uma inserção marcada para a derivada, convergem uniformemente em compactos: o fator extra k é absorvido pela mesma razão assintótica. Pode-se diferenciar termo a termo em epsilon=0 sobre entradas de suporte finito. Isso também vale para os observáveis ponderados abaixo, pela convergência com fatores polinomiais. Assim a primeira variação definida abaixo é efetivamente a derivada desta evolução e de sua leitura; não se invoca diferenciabilidade em norma de operadores sobre todo T₁ para V ilimitado.

## 3. Uma inserção V entre evoluções com bomba

Se T(t) é a evolução completa não perturbada da R66, a derivada em zero é

    δρ(t)=∫₀ᵗ u(s) T(t−s) V T(s)ρ₀ ds.                                 (3)

A composição V T(s) é definida pela série convergente ponderada; (3) é integral em norma-traço sobre este domínio. Expanda as duas T em Dyson em B. Com n inserções de B ao todo, todos os termos após a inserção V ficam no máximo em P_(m0+n+1). A soma das distribuições n=n₁+n₂ entre os dois intervalos usa

    Σ_(n₁+n₂=n) (t−s)^n₁ s^n₂/(n₁!n₂!) = t^n/n!.

Portanto, escrevendo U=∫₀ᵀ|u(s)|ds e q=bT, o termo de ordem n na soma para δρ tem norma≤a U sqrt(m0+n+1) q^n/n!. Não aparece fator adicional n+1: a posição temporal de V já é integrada em s, e o multinômio soma as posições da bomba.

Para m≥m0+1, os termos coincidem com o corte m quando n≤m−m0−1. Defina

    d=m−m0−1 ≥0,     E_d(q)=Σ_(n>d) q^n/n!,     E_(-1)(q)=exp(q).
    W1(d)=Σ_(n>d) sqrt(m0+n+1) q^n/n!,
    W2(d)=Σ_(n>d) (m0+n+1) q^n/n!
         =(m0+1)E_d(q)+q E_(d−1)(q).                                   (4)

O erro entre o infinito construído e o corte m, ou entre dois cortes M>m, satisfaz

    ||δρ(t)−E_m δρ_m(t)||₁ ≤ 2a U W1(d),       0≤t≤T.                    (5)
    W1(d) ≤ sqrt(E_d(q) W2(d)).

O fator2 soma as duas caudas. **A primeira ordem omitida é n=m−m0**, uma ordem antes da cauda da evolução sem a sonda. Para m=m0, pode-se usar diretamente a soma completa desde n=0, sem afirmar coincidência de termos; não usar E_(-2) por acidente. Todos os limites abaixo são uniformes em tempo compacto e em densidades do mesmo suporte P_m0.

## 4. Saída não limitada: estimativa própria ponderada

A R78 lê z(t)=gain_out Tr[L_out ρ(t)], L_out=sqrt(κ_o)a_o. Defina zeta=|gain_out|sqrt(κ_o). Sobre suporte P_r, o funcional z tem norma≤zeta sqrt(r). Para Q_theta=gain_out(exp(-iθ)L_out+exp(iθ)L_out†)/sqrt(2), a norma da compressão≤sqrt(2)zeta sqrt(r). Esse bound também vale com θ(t) dado; conjugação por R(t) que comuta N preserva a prova quando todo o gerador/instrumento é transportado.

Multiplicar o bound de suporte após V pelo bound do observável dá, diretamente da série,

    |δz(t)−δz_m(t)| ≤ 2a zeta U W2(d),                                  (6)
    |δ<Q_theta(t)>−δ<Q_theta(t)>_m| ≤ 2sqrt(2)a zeta U W2(d).              (7)

São cotas absolutas uniformes. A passagem do observável não limitado é controlada pela série, não apenas por convergência em norma-traço dos estados. E_d e q E_(d−1) tendem a zero, logo a resposta de saída possui limite único neste modelo e domínio.

Para o núcleo sem envelope K_zX(t,s), a mesma prova dá erro≤2a zeta W2(d), uniformemente 0≤s≤t≤T. Para uma leitura filtrada ∫v(t)δz(t)dt, multiplica-se (6) por ||v||_L1 (ou integra-se a cota pontual mais estreita). Não se usa um único fator de fase no tempo final para filtros com fase variável.

Duas sondas X/P com o mesmo |c| têm o mesmo erro ε_z de (6). Na convenção u=x+iy, h_+=(R_X−iR_Y)/2 e h_-=(R_X+iR_Y)/2, cada erro é≤(ε_X+ε_Y)/2=ε_z. Não se impõe h_-=0, nem se identifica h_+ com G_OH. Divisão para extrair fase/ganho relativo exige piso independente de amplitude: as cotas absolutas não autorizam uma fase bem condicionada perto do zero.

Como diagnósticos opcionais, n_o e a_i†a_o têm compressões de norma≤r em P_r: para o segundo, a norma máxima sqrt((n_i+1)n_o) é≤r para r≥1, e é zero para r=0. Suas primeiras variações têm erro≤2a U Σ_(n>d)(m0+n+1)^(3/2)q^n/n!, também convergente. Isso se refere aos observáveis intracavidade, não a correlações temporais do detector.

## 5. Forma computável e utilização no plano

Para q≥0 e d≥0 com q/(d+2)<1,

    E_d(q) ≤ [q^(d+1)/(d+1)!]/[1−q/(d+2)].                              (8)

Ao calcular o segundo termo de W2, exigir também q/(d+1)<1 se d−1≥0; para d=0 usar E_(-1)=exp(q). Fora desse regime, usar a série convergente ou outro majorante positivo, nunca denominador não positivo. A fórmula evita subtração de exponenciais próximas. Se q=0 e d≥0, W2=0: sem a bomba, a primeira variação do suporte finito é exata já em m≥m0+1, mesmo que a evolução para epsilon≠0 não preserve esse suporte.

Exemplo de parametrização, **sem avaliação numérica nesta nota**: inserir os parâmetros fixados de R78 (m0=1, T=0,75, u=1, a=2sqrt(2)*1,3*sqrt(κ_i), zeta=0,8*sqrt(κ_o), q=2|Ω|T). Para m=3 usa-se d=1, portanto W2=2E_1+qE_0. Para comparar m=3 com m=4, a mesma expressão do menor corte controla a diferença. Valores de beta continuam calculados em runtime; a desigualdade só requer as taxas finitas/não negativas da realização R66. A cota pode ser maior que a resposta: isso torna uma conclusão quantitativa inconclusiva, não autoriza substituir a cota pelo resíduo observado.

## 6. Alcance e limite concreto

[DERIVED] Fechada nesta nota a passagem m→∞, uniforme em tempo finito, para a primeira variação R78 e suas leituras lineares no modelo R66 com preparo de suporte finito; com cota explícita independente do corte maior. A sonda linear ilimitada foi tratada por estimativa nova, não pela cota da bomba copiada por nome. A prova é analítica em texto e requer revisão; nenhum termo Lean nem execução nova é alegado.

[OPEN] Realização material, identificação de laser/RF com c,u, Gamma independente, geometria/localidade, validade da lei tanh e correspondência com g_OH S_beta continuam separadas. Não há construção HP global da saída, erro estatístico, calibração física, resultado experimental ou fechamento integral R4/R5. Estados iniciais fora de suporte finito e T→∞ precisam de hipóteses próprias. A desigualdade vale tanto para resposta nula como não nula e não obriga um alvo físico.
