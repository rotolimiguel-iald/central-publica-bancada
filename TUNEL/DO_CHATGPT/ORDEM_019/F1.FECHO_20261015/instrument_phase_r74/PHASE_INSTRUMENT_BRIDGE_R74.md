# R74 — transporte conjunto da fase, do instrumento e do reservatório

**[DERIVED — ligação analítica, sem novo Lean ou campanha]** r69_locality_bridge, 18/10/2026. Reaproveitamento de R57, R64 e R66. Project/preflight R4: revisão 513, lease `df34d007-70c4-43cb-a80a-6e27ddd55e4e`, `ready=true`, owner codex-gerente-tgl. Escopo: matrizes finitas da face 0/1 e demais cortes finitos já nomeados; não transfere identidades CCR bosônicas ao corte hardcore nem fecha R4/R5 integrais.

## 1. Quadro por canal e gerador completo

Sejam n_i,n_o,n_e os números dos dois modos e da excitação OH. Para fases reais C¹ no intervalo observado,

\[
R(t)=e^{i(\chi_i(t)n_i+\chi_o(t)n_o+\chi_e(t)n_e)},\quad
\mathcal S_t(X)=R(t)XR(t)^\dagger,\quad \rho'=\mathcal S_t\rho.
\]

Os números comutam. Logo i dot(R)R†=−Σ_j dot(χ_j)n_j e

\[
h'(t)=R(t)h(t)R(t)^\dagger-\sum_j\dot\chi_j(t)n_j,
\quad L_j'(t)=R(t)L_j(t)R(t)^\dagger.
\tag{1}
\]

Portanto `G'_t = dot(S)_t S_t^{-1} + S_t G_t S_t^{-1}`; seu propagador de dois tempos é `T'(t,s)=S_t T(t,s) S_s^{-1}`. A derivação é a regra do produto aplicada a ρ'; a conexão de Hamiltoniano não pode ser omitida. h=H/ℏ como em R57/R66: χ é adimensional e dot(χ) tem unidade s⁻¹.

Como [n_j,a_j]=−a_j e [n_e,σ₋]=−σ₋, inclusive no corte 0/1,

\[
a_i'=e^{-i\chi_i}a_i,\quad a_o'=e^{-i\chi_o}a_o,
\quad\sigma_-'=e^{-i\chi_e}\sigma_-,\quad Z'=Z.
\]

O termo JC torna-se `g[e^{i(χ_i−χ_e)}a_i†σ₋+e^{i(χ_e−χ_i)}σ₊a_i]`. Uma bomba Ω(σ₊+σ₋) torna-se Ω(e^{iχ_e}σ₊+e^{-iχ_e}σ₋); uma bomba já faseada no laboratório conserva também sua fase original. As perdas isoladas conservam seus dissipadores, mas isso não autoriza apagar fases do instrumento.

Escreva A=a_o†σ₋ e B=σ₊a_i. O salto único é

\[
J'=e^{i(\chi_o-\chi_e)}A+e^{i(\chi_e-\chi_i)}B.
\tag{2}
\]

Seu termo de reciclagem inclui
`e^{i(χ_o+χ_i−2χ_e)}A X B†` e seu parceiro conjugado. Os produtos A†B=B†A=0 no modelo da fonte não anulam esses superoperadores. Substituir D[J'] por D[A]+D[B] altera o gerador. O quadro comum χ_i=χ_o=χ_e recupera exatamente o caso R57: J e JC invariantes; quadros diferentes exigem (2).

## 2. Instrumento R64: equivalência antes da integração

A inserção de quadratura de R64 é

\[
\mathcal M_{L,\theta}(X)=
\frac{e^{-i\theta}LX+e^{i\theta}XL^\dagger}{\sqrt2}.
\]

Há duas escritas equivalentes do **mesmo** instrumento:

1. Portas transportadas `L_j'=R L_j R†`, mantendo a fase LO θ_j do laboratório.
2. Portas-base `L_j`, com fase `θ_j'=θ_j+χ_j`, para as portas ópticas de abaixamento.

Em ambos os casos `M'_j(t)=S_t M_j(t) S_t^{-1}`. Isso vale para a fase de cada canal, não só uma portadora comum. O estado, propagador e as inserções têm de usar a mesma convenção.

Para t>s, a expressão R64 transforma-se em
`Tr[M'_j(t) T'(t,s) M'_k(s) ρ'(s)]`.
Substituir as quatro similaridades cancela S_s e S_t sucessivamente, e a invariância do traço devolve exatamente a correlação original. Para qualquer cadeia temporal ordenada de inserções, o mesmo cancelamento prova a igualdade dos momentos regulares. O termo singular de R64 continua `δ_jk δ(t−s)/2`: rotação de fase unitária conserva o ruído de vácuo.

### Filtros e ganhos, com a fase dentro da janela

Para um peso complexo fixado f_j e ganho real g_j, defina
`c_j(t)=g_j conjugate(f_j(t)) exp(−iθ_j(t))` e
`M_c(X)=(c L X+conjugate(c)X L†)/√2`.
É uma corrente real de quadratura com fase e envelope variáveis, não a atribuição simultânea de duas quadraturas incompatíveis. Na escrita de portas-base, `c'_j=e^{-iχ_j}c_j`, isto é, pode-se usar θ'_j=θ_j+χ_j ou f'_j=e^{iχ_j}f_j. Ambas deixam o termo de ruído `|g_j f_j|²/2` igual. Para duas leituras do mesmo banho, a contribuição de contato geral é `Re(c_j conjugate(c_k))/2`; fases comuns daquele banho cancelam. Portas independentes têm contato cruzado nulo.

Os auxiliares de R64 transportam-se `u'_j=S_t u_j`, `v'_{jk}=S_t v_{jk}`. A derivada inclui exatamente a conexão já contida em G'; os termos fonte passam por M' e o termo de ruído por S_tρ. Como S preserva o traço, todos os momentos filtrados e suas covariâncias coincidem. Equivalentemente, o gerador inclinado completo é transportado pela mesma similaridade mais conexão, inclusive sua parcela quadrática escalar: isso cobre a hierarquia inteira quando os momentos existem. Em dimensão finita, no intervalo finito e com filtros admitidos no contrato, não há problema de domínio ilimitado.

Não se pode aplicar uma fase apenas no fim da integral quando χ varia durante o filtro. A compensação é ponto a ponto dentro da janela. Quatro aquisições XX, PP, XP e PX continuam distintas, com o mesmo preparo conforme R64.

## 3. Decoder C/B e a releitura R57

No modelo finito, para operadores-base e ρ'=RρR†,

\[
C'=\operatorname{Tr}(\rho'a_i a_o)=e^{i(\chi_i+\chi_o)}C,
\quad B'=\operatorname{Tr}(\rho'a_i^\dagger a_o)=e^{i(\chi_o-\chi_i)}B.
\tag{3}
\]

Se também se transportam os operadores, as expectativas originais são invariantes. O decoder cruzado de R64 obedece à mesma álgebra para os **modos temporais de saída**; eles não são identificados com operadores instantâneos da cavidade. Para uma mudança constante de referência de cada modo temporal, valem os fatores (3). Para referência variável, valem os filtros transformados do §2, não a multiplicação do resultado final por (3) em um instante escolhido.

O leitor escalar R57 conserva a abertura da fronteira:
`A_β(z)=z S(θ_M)`, `read(A_β(z))=z exp(iθ_M)` e
`D_β(w)=[w exp(−iθ_M)]S(θ_M)`.
A releitura satisfaz `read(D_β(w))=w` na mesma família. Como `z=2 Tr(ρσ₊)`, o quadro OH dá `z'=e^{-iχ_e}z`. Logo `A_β(z')=e^{-iχ_e}A_β(z)` e o resultado lido também recebe esse fator; aplicar D_β ao resultado transformado devolve a matriz transformada. As proporções β e 1−β são preservadas para z≠0; em z=0 não há fase normalizada. Nada exige mudar θ_M.

Isso liga leitura, transformação e releitura já existentes. Não torna `G_OH=a exp(iω_OH t)` uma solução universal: R57 já exibe o termo de amortecimento e os acoplamentos que impedem essa identificação automática. A escolha de referencial tampouco deriva tanh(P/P_th), o preparo ou a interpretação de z como sinal efetivamente implementado no receptor.

## 4. Reservatório R66 e o sinal da amplitude coerente

R66 usa uma única ancilla C⁶, cinco saltos e
`V=Σ_j(L_j⊗|j><0|−L_j†⊗|0><j|)`.
Com as portas transportadas L_j', `V'=(R⊗I)V(R†⊗I)`. Mantendo o estado da ancilla e seu coeficiente α no canal 3, a bomba derivada é

\[
h'_{drive}=i(\alpha^*L_3'-\alpha L_3'^\dagger)
             =R h_{drive}R^\dagger.
\tag{4}
\]

Para L₃=√γ_OH σ₋ e α=iΩ/√γ_OH, com γ_OH>0, isso dá
`h'_drive=Ω(e^{-iχ_e}σ₋+e^{iχ_e}σ₊)`.
O coeficiente α não muda quando só o sistema é conjugado. A conexão `−Σ dot(χ)n` entra no Hamiltoniano-base transportado h₀', separadamente da bomba gerada pelo banho.

**Se a fase de L₃' for absorvida na referência do banho**, use W|0>=|0>, W|3>=e^{iχ_e}|3>. Então
`(I⊗W)V(L₃')(I⊗W†)=V(L₃)` nesse canal e o estado da ancilla transforma-se em

\[
\frac{|0\rangle+\sqrt\delta\,\alpha'|3\rangle}
 {\sqrt{1+\delta|\alpha'|^2}},\qquad
\boxed{\alpha'=e^{+i\chi_e}\alpha}.
\tag{5}
\]

Usando L₃ base e α' em `i(α'^*L₃−α'L₃†)`, recupera-se (4). O sinal negativo para α' seria incorreto. Geralmente rephasing L→e^{iφ}L exige α→e^{iφ}α para conservar a mesma bomba; alterar apenas um troca a realização. As fases do canal 5 não podem ser absorvidas separadamente nas duas parcelas de J, pois há apenas um índice de banho para sua soma.

Para um quadro variável, o transporte **exato de um passo** entre t_k e t_{k+1} é `U'_k=(R(t_{k+1})⊗I)U_k(R(t_k)†⊗I)`. Seus Kraus satisfazem `K'_{j,k}=R(t_{k+1})K_{j,k}R(t_k)†`; composições cancelam os R internos. Isso fornece equivalência exata de canais finitos, e sua expansão local produz h₀' com a conexão e L_j'(t). Uma exponencial congelada no instante t_k é apenas sua aproximação de pequeno passo; não se declara igualdade finita entre ela e U'_k para fases variáveis. A mudança de referência do banho deve também acompanhar cada bin.

Nenhuma transformação faz γ_OH=0 admitir α=iΩ/√γ_OH: permanece a alternativa de drive explícito indicada em R66. Os limites e estados de banho são os da realização escolhida, não qualquer reservatório material.

## 5. Compatibilidade algébrica com a rede e alcance

Para observáveis limitados A,B que comutam, `[UAU†,UBU†]=U[A,B]U†=0`. Portanto transportar simultaneamente a rede por `A'(O)=U A(O)U†` conserva sua localidade. Isso não afirma `U A(O)U†=A(O)` para cada região original. A realização local de osciladores R71 fornece seu vínculo próprio; o quadro de fase desta nota não constrói por si uma nova representação de Poincaré, a localização instrumental que faltar nem a lei relativística de seu relógio.

O resultado é o transporte completo e consistente da **mesma** dinâmica, leitura, filtros, decoder e realização de banho no escopo finito. Taxas, γ_Λ, calibração temporal, ganho e a identificação da resposta física continuam exigindo seus dados próprios. O produto λ=βγ_Λ e sua degenerescência de identificabilidade de R64 não são alterados por similaridade. β permanece o valor em runtime da fonte; nenhuma inferência experimental, nova frequência física ou fechamento global é reivindicado.
