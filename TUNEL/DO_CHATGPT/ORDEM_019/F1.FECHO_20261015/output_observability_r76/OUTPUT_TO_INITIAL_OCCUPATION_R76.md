# R76 — da leitura de saída à ocupação inicial da cavidade

**[DERIVED — demonstração analítica candidata, NOT_LEAN]** r69_locality_bridge, 18/10/2026. Project/preflight R4 e R5 conferidos na revisão 522; leases respectivos `196fb492-4c01-4a53-b2eb-cfcc68b52f37` e `23ecbd46-c105-43ed-908b-de11a856284f`, owner codex-gerente-tgl. Reaproveita o instrumento R64, seu transporte R74, as cotas R75 e a testemunha R72. Nenhum dado observado, ajuste de β, execução, memória ou programa canônico alterado.

## 1. Efeitos de momentos: a ponte de saída ao estado inicial

Fixe o gerador, taxas, portas, preparo do banho, ganhos, filtros, fases e janelas do instrumento. A densidade inicial desconhecida satisfaz ρ=P_{m₀}ρP_{m₀}, Trρ=1. Escreva H₀=P_{m₀}H, dimensão d=(m₀+1)² para o sistema R66 com OH. O suporte inicial é hipótese nomeada; não é deduzido do fato de uma regressão funcionar. Um espectador arbitrário pode ser mantido por tensor identidade: as fórmulas dependem da redução ao fator ativo.

Cada média ou segundo momento **bruto** da hierarquia R64 é um funcional linear da densidade inicial. A hierarquia propaga (ρ,u,v) linearmente e o termo de contato é proporcional a ρ; portanto existe um operador hermitiano único E_ℓ sobre H₀ tal que

\[
y_\ell(\rho)=\operatorname{Tr}_{H_0}(\rho E_\ell).
\tag{1}
\]

Chamamos E_ℓ de “efeito de momento”. Ele não é necessariamente um efeito POVM entre 0 e I: médias de quadratura e momentos cruzados podem ter sinal. Uma covariância centrada r−μ_jμ_k **não é linear em ρ** e não deve ser usada como E_ℓ; seus componentes brutos devem entrar separadamente. Partes real e imaginária de decoders lineares podem ser separadas em dois efeitos hermitianos.

### Construção no corte m≥m₀

Se Q_m é a inclusão H₀→P_mH e F_ℓ^{(m)} é o funcional terminal produzido pela hierarquia, defina

\[
E_\ell^{(m)}=Q_m^\dagger(F_\ell^{(m)})^*(1)Q_m.
\tag{2}
\]

A estrela em (2) é a dualidade entre funcional linear e operador, não uma nova dinâmica. Pode-se obter o efeito propagando o seletor terminal de traço pela hierarquia adjunta, ou aplicando a hierarquia às matrizes-unidade: `(E_ℓ^(m))_{ab}=F_ℓ^(m)(|b><a|)`. Auxiliares não positivos são permitidos por linearidade. O contato diagonal contribui o escalar `½∫|c_j|²` vezes I₀; sua presença precisa ser mantida.

R75 fornece, uniformemente sobre **todas** as densidades em H₀,
`|y_ℓ−y_ℓ^(m)|≤δ_ℓ,cut`. Como a diferença dos efeitos é hermitiana,

\[
\|E_\ell-E_\ell^{(m)}\|_{op}
=\sup_{\rho\ge0,\,\operatorname{Tr}\rho=1}
 |\operatorname{Tr}\rho(E_\ell-E_\ell^{(m)})|
\le\delta_{\ell,cut}.
\tag{3}
\]

Assim os efeitos do instrumento bosônico existem no espaço inicial finito e são aproximados em norma de operador, não apenas para um estado sintético escolhido. Para médias use `δ_cut=2 A_j T₁(d_cut)`; para segundos momentos brutos use `δ_cut=2 A_j A_k T₂(d_cut)`, com d_cut=m−m₀ e constantes R75. As janelas, filtros e ganhos próprios de cada feature entram nessas constantes. O erro de corte do contato é zero.

## 2. Reconstruir um observável, sem exigir tomografia completa

Escolha A=N_b=n_i+n_o ou A=N_total=n_i+n_o+n_e, comprimido a H₀. N_b coincide com o número dos modos locais da R72 quando se usa a identificação unitária R71; isso não identifica por decreto esses modos com os da cavidade física. Ambos os A são positivos e limitados por m₀I₀. Sua expectativa é uma **ocupação adimensional**, não energia em joules; uma energia física exige pesos/unidades e Hamiltoniano próprios.

Dados efeitos aproximados hermitianos \widetilde E_ℓ, escolha coeficientes reais a,w_ℓ e um limite superior certificado para

\[
\eta=\left\|A-aI_0-\sum_\ell w_\ell\widetilde E_\ell\right\|_{op}.
\tag{4}
\]

Não é necessário que os efeitos abranjam todo o espaço de matrizes: basta reconhecer A. Uma pseudoinversa pode escolher os pesos a partir dos efeitos; ela não prova por si que o resíduo seja pequeno. Reportar η, norma dos pesos, condicionamento e tolerância usada para decidir posto. Um rcond numérico não prova uma dependência linear exata. Um bound de Frobenius do resíduo, com erro de avaliação controlado, também é um majorante válido de η, ainda que menos preciso.

A escolha dos pesos, do alvo, das features e do limiar de certificado deve preceder o uso dos dados observados. Ela é construção de um estimador para um observável com modelo fixado; não é ajuste de β. Não modificar as taxas para fazer η ou a ocupação estimada diminuírem.

## 3. Intervalo com todos os erros

Sejam y_ℓ,obs os valores observados e δ_ℓ,exp seus limites de erro **simultâneos**. Some separadamente:

- δ_ℓ,cut, fornecido pela R75 para o mesmo suporte inicial/janela;
- δ_ℓ,num, erro da construção de \widetilde E_ℓ e dos cálculos do instrumento;
- δ_ℓ,model, erro entre o instrumento físico admitido e o modelo fixado, uniforme na classe de estados permitida.

Não declarar δ_model=0 para um aparelho real por ele ter o nome da patente. Em controles sintéticos, zero pode significar que a mesma equação define geração e reconstrução, e esse alcance deve ser dito. Incerteza dos parâmetros do gerador pode ser incorporada por um conjunto independente Θ e pelo bound `sup_{θ∈Θ}||E_ℓ(θ)−E_ℓ(θ₀)||op`; a existência desse bound não significa que já tenha sido calculado.

Defina

\[
v=a+\sum_\ell w_\ell y_{\ell,obs},\qquad
\Delta=\eta+\sum_\ell|w_\ell|
(\delta_{\ell,cut}+\delta_{\ell,num}+\delta_{\ell,model}+\delta_{\ell,exp}).
\tag{5}
\]

Então, no evento de cobertura simultânea dos erros experimentais,

\[
\boxed{\operatorname{Tr}\rho A\in[v-\Delta,v+\Delta].}
\tag{6}
\]

Prova: a contribuição do resíduo é limitada por ||ρ||₁η=η; substituir cada expectativa por sua leitura acrescenta no máximo |w_ℓ| vezes o erro correspondente, pela desigualdade triangular. A contribuição aI é exata porque o traço é conhecido. A cobertura não resulta de somar probabilidades implicitamente; deve ser conjunta ou construída, por exemplo, com alocação explícita de erros por união.

Compare o intervalo com [0,m₀]. Se a interseção for vazia, recuse por inconsistência dos dados/hipóteses. Em particular, um limite superior negativo não pode ser zerado silenciosamente. Se a interseção não é vazia, pode-se usar o limite superior U=min(m₀,v+Δ) e o inferior max(0,v−Δ), registrando o uso dos limites espectrais. Grande norma dos pesos pode tornar U pouco informativo apesar de η pequeno; nesse caso recuse o certificado pretendido, sem selecionar novos pesos depois dos dados para encobrir o erro.

## 4. Certificado de preparo R72, agora por saída

Para A=N_b, P_vac é o projetor do vácuo dos dois modos, tensor identidade em OH/espectador. Para A=N_total, P_vac também exige OH no fundamental. Em ambos os casos `I−P_vac≤A`. Portanto um U válido implica

\[
p_0=\operatorname{Tr}\rho P_{vac}\ge1-U.
\tag{7}
\]

Se U<1, a redução ao fator cujo vácuo está certificado está a distância-traço no máximo 2√U do vácuo. Para o estado conjunto, a mesma cota vale em relação ao produto desse vácuo com o restante **condicionado**, conforme a prova R72. Não determina o estado do espectador nem certifica o vetor global Ω_b específico.

Para certificar um preparo com tolerância ε_*<1, fixe ε_* antes e exija U≤ε_* além das demais condições. Se U≥1, sobra somente o limite trivial p₀≥0 e distância≤2; é `NO_CERTIFICATE`, não falha da teoria. Um intervalo largo também pode recusar um limiar mais estrito mesmo com U<1. As leituras de saída não foram simplesmente tratadas como quadraturas internas: a passagem foi feita pelos efeitos e pelo resíduo (4).

Sem o suporte inicial P_{m₀} ou uma cota apropriada da cauda inicial, este certificado não se estende automaticamente ao Fock inteiro. Pequena probabilidade fora do corte não controla sozinha a expectativa de A ilimitado; é necessária informação de momento/energia dessa cauda. O corte usado para gerar efeitos e o suporte inicial admitido são dois objetos distintos.

## 5. Critério exato de identificabilidade e pares indistinguíveis

Em H₀ finito, defina S=span_ℝ{I₀,E₁,…,E_L}, com produto interno Hilbert–Schmidt real em matrizes hermitianas. Se A∈S, há reconstrução afim exata de TrρA para todos os estados. Se A∉S, ponha D=A−Π_SA. Então

\[
D=D^\dagger\ne0,\quad\operatorname{Tr}D=0,\quad
\operatorname{Tr}(DE_\ell)=0,\quad
\operatorname{Tr}(DA)=\|D\|_{HS}^2>0.
\]

Escolha 0<ε<1/(d||D||op). Os estados

\[
\rho_\pm=I_0/d\pm\varepsilon D
\tag{8}
\]

são positivos e de traço um, dão **todas as mesmas leituras y_ℓ**, mas
`Tr(Aρ_+)−Tr(Aρ_-)=2ε||D||HS²>0`.
Logo nenhum estimador, linear ou não, baseado apenas nessa lista de leituras determina A universalmente nessa classe. Não foi necessário variar β, γ_Λ ou o gerador. Se outras restrições sobre os estados foram previamente justificadas, sua classe pode mudar o critério; elas não podem ser inventadas depois para excluir o par.

Para efeitos numéricos/comprimidos, a nulidade da matriz de features mostra primeiro indistinguibilidade **naquele modelo aproximado**. Para transferi-la ao instrumento bosônico verdadeiro, use (3): diferenças remanescentes são limitadas, por exemplo, por `||ρ_+−ρ_-||₁ δ_ℓ,cut`, acrescidas dos demais erros. Não promover um singular value pequeno a igualdade exata. O contraexemplo de porta desacoplada da R72 é exato: κ_i=κ_o=0 faz as inserções de saída nulas; só resta shot noise proporcional a I, que não distingue N_b ou N_total não constantes, mesmo com os outros termos do gerador presentes.

## 6. Transporte de fase e parâmetros físicos

Sob o transporte completo R74, o estado inicial muda por ρ'=R(0)ρR(0)† e o efeito inicial por E'_ℓ=R(0)E_ℓR(0)†. É R(0), não a fase apenas no fim da janela: todas as fases intermediárias já estão dentro do instrumento. A'=R(0)AR(0)†. Como R comuta com N e P_{m₀}, a compressão é preservada e o resíduo transforma-se unitariamente, mantendo sua norma η. Os mesmos pesos e cotas servem. Para os alvos de número desta nota A'=A. Alterar LO/filtro sem o transporte correspondente não satisfaz essa identidade.

As taxas, γ_Λ, calibração de fase/tempo, ganhos e resposta material são entradas fixadas ou calibradas independentemente. A ponte é condicional a elas. Não se obtém γ_Λ independente ajustando as próprias leituras geradas pelo mesmo modelo; a degenerescência λ=βγ_Λ já registrada em R64 permanece. O resultado novo é um critério e um intervalo verificáveis para inferir a ocupação inicial a partir das leituras admitidas — incluindo um resultado negativo quando elas não bastam — sem proclamar observabilidade física já medida ou fechamento integral R4/R5.
