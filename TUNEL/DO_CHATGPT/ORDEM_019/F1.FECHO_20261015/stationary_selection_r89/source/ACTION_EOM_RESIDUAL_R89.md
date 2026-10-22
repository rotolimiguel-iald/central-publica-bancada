# R89 — Resíduo entre a ação escrita e a EOM, com a fronteira |1+w|

Autor: /root/r69_locality_bridge. [DERIVED — conferência funcional por reuso R88; sem teste novo]. Complemento novo à nota SPECTRAL_STATIONARITY_DIAGNOSTIC_R89.md, preservada com seu pino. A obstrução abstrata Gibbs/GKLS já estava em SELECTION_AND_NORMAL_VARIATIONS_R85.md:28–49; R89 a compõe com a identidade modular e os dois exemplos, não reivindica descoberta ou campanha repetida.

## 1. A mesma ação, transcrita com os campos distintos

Custo, tgl_paper_unified.py:10319–10369, escreve L_total=L_matéria+L_campo+L_grav+L_mod,

    L_matéria=barψ(iγ·D−m)ψ−F_YM²/4−|Dφ|²/2−V(φ),
    L_campo=−Φ²/4, Φ_μν=∂_μΨ_ν−∂_νΨ_μ,
    L_grav=(1/(2κ²)+ξ|Ψ|²)R,
    L_mod=β L_ΛCDM |1+w_eff(z)|.

As mesmas linhas10343–10345 denominam Ψ campo escalar de fronteira. As linhas10418–10431 atribuem à variação em Ψ* a EOM

    W(Ψ):=(□−m_Ψ²−ξR)Ψ−βK_∂Ψ=0.                    (W)

ψ fermiónico, φ de Higgs e Ψ luminodinâmico são identificadores e tipos distintos no texto. Os cinéticos/massas de ψ ou φ não podem ser consumidos como os de Ψ sem a representação que os relacione. A regra universal não foi rejeitada: falta conferir sua representação específica ao passar dessas fórmulas para um único funcional diferenciável. A fonte10433 em diante já distingue o estatuto da ponte operador→fonte.

## 2. Se o campo representado é uma 1-forma: diferença exata

R88 derivou, na leitura REAL literal A_μ=Ψ_μ, u=g^{μν}A_μA_ν, F=dA, variação em A com g independente e L_rest mantendo TODOS os outros termos,

    E_A^b=∇_a F^{ab}+2ξR A^b+E_rest^b.              (A)

Com a convenção de curvatura R^a_bcd=∂cΓd−∂dΓc+[Γc,Γd], e Levi-Civita,

    ∇_a F^{ab}=□A^b−∇^b(∇_a A^a)−Ric^b_c A^c.     (M)

Derivação: expandir F^{ab}=∇^aA^b−∇^bA^a e usar
∇_a∇^bA^a=∇^b divA+Ric^b_c A^c. Assim, SE a representação ainda a verificar permitir ler (W) na MESMA 1-forma, a diferença literal entre (A) e W(A) será

    E_A−W(A)=−grad(divA)−Ric·A+3ξR A
              +m_Ψ² A+βK_∂A+E_rest.                (D)

A expressão K_∂A nessa comparação é condicional à sua representação no espaço das 1-formas: não se atribui a um operador abstrato um domínio por nome. (D) não prescreve E_rest igual ao negativo dos demais termos; fornece precisamente o resíduo que a fonte existente terá de produzir se as duas EOM forem equivalentes. Nenhum termo foi ajustado para cancelar o resíduo.

Não se pode impor divA=0 como escolha de gauge automática: ξR A² não é invariante sob A→A+dχ em geral. A divergência de (A) fornece a restrição dinâmica 2ξ div(RA)+divE_rest=0. Em uma região de R constante nãozero, ξ≠0 e E_rest=0, ela pode implicar divA=0; isso ainda deixa o termo Ric·A e não transforma o vetor em escalar. Em R=0 essa inferência particular também não vale.

Na leitura COMPLEXA conjugada literal −barF·F/4, a equação variando barA é E_barA=½divF+ξRA+E_rest,barA. Multiplicar por2 recupera o mesmo operador cinético e +2ξR, mas duplica E_rest,barA. Deve-se comparar após essa normalização; não somar a equação complexa e a real como se tivessem o mesmo campo variável.

## 3. Se Ψ é escalar independente da 1-forma

Sem identificar A com Ψ, o cinético −(dA)²/4 não varia em Ψ*. Para Ψ complexo e u=barΨΨ, o setor exibido contribui ξRΨ; para Ψ real e u=Ψ² contribui2ξRΨ. Não há nas parcelas explicitamente escritas para Ψ, nessa leitura, termo que gere □Ψ nem m_Ψ²Ψ. Esses termos só podem vir de uma representação/cinético/potencial efetivamente fornecidos pelos setores restantes, não da mera presença dos símbolos ψ/φ em L_matéria.

A restrição A=dΨ não resolve essa diferença: dA=0 e a ação restrita tem cinético ξR(dΨ)², cujo Euler real é −2ξ div(RgradΨ), mais o Euler restante, como já calculado em ONE_FORM_FULL_SOURCE_R88.md:112–116. Variar antes ou depois de restringir também testa direções diferentes. Não se propõe esse mapa como escolha física.

Consequentemente, estacionariedade espectral pontual não preenche os termos de (D), não cria um cinético escalar e não resolve a identidade entre os dois operadores de Euler. Trata-se de conferir a primeira variação da MESMA ação, e não de acrescentar um modelo mais fácil que gere (W).

## 4. Regularidade do termo modular na fronteira w=−1

[DERIVED, hipótese condicional de variação admissível] Em um ponto, β constante, L(t)=L0+O(t) real, w(t)=−1+a t+o(t), a≠0. Então

    β L(t)|1+w(t)| = β L0 |a| |t|+o(|t|).

Se L0≠0, os quocientes incrementais pela direita e esquerda são +βL0|a| e −βL0|a|. Portanto não existe primeira variação bilateral linear dessa densidade nessa direção. Incluir o volume suave não corrige o problema: multiplica o coeficiente por seu valor positivo no ponto, pois o módulo vale0 no fundo.

Exceções precisas: se a=0, o incremento é o(t) e a derivada é0; se L0=0 com L suave, o termo é O(t²) e tem derivada0; se w≡−1 em toda família admitida, o termo permanece identicamente0 (caso separado já considerado em R86). Fora da fronteira, a variação existe e é β[|1+w|δL+L sign(1+w)δw], além da parcela de volume.

A não diferenciabilidade PONTUAL não implica automaticamente a da ação integral se o conjunto w=−1 tem medida zero; não se faz essa extrapolação. Se a família parte de w≡−1 numa região de medida positiva e cruza com δw nãozero, a contribuição integrada local é |t|∫βv0 L0|δw|+o(|t|), sob dominação regular; em patch de L0 com sinal fixo e δw nãozero o coeficiente não se anula. Uma fonte Hilbert ordinária requer então delimitar a classe off-shell admitida ou um tratamento não suave. Esta nota não decide se tais trajetórias pertencem ao contrato da TGL nem instala subgradiente ou regularização novos.

## 5. Próxima construção limitada pelo que já foi escrito

A operação de satisfação permanece a referência humana. A tarefa concreta é usar sua representação espectral para fornecer um único mapa de campos com domínio, conferir a identidade de Euler (D) e a variação do termo modular nas direções efetivamente admissíveis. Há dois resultados já reutilizáveis: o ramo Einstein–sigma S³ estacionário, e as primeiras variações locais/integradas R83–R88. Não há razão para reconstruí-los. O residual literal e a regularidade acima são controles funcionais que qualquer ligação completa deve satisfazer. Não se declara ausência universal no acervo, não se escolhe novo Ψ, não se substitui a ação completa por sigma, não se fecha R16 e não se faz outra pergunta abstrata ao operador.
