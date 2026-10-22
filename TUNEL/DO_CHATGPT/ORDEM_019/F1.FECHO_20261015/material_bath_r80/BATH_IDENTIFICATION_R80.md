# R80 — o que torna o banho realmente comum

[DERIVED — demonstração algébrica, NOT_LEAN] Codex-gerente-tgl, 19/10/2026. F1.FECHO_20261015, reivindicação985. Reuso R66 (realização por colisões), R74 (transporte inteiro de J e do instrumento) e R79 (identificação dipolar e cota contínua). Esta nota não reconstrói essas peças e não identifica um aparelho por decreto.

## 1. Critério necessário e suficiente no contrato de dois canais

Fixe os operadores F1=a_out†σ− e F2=σ+a_in e a convenção

    D_C(ρ)=Σ_ab C_ab(F_a ρ F_b† − {F_b†F_a,ρ}/2).

Uma realização por canais L_μ=Σ_a v_aμ F_a fornece C_ab=Σ_μ v_aμ conj(v_bμ). Logo C é a Gram positiva das duas linhas v1,v2. Isto é uma parametrização de um gerador já reduzido, não uma derivação microscópica universal.

Para λ>0, o alvo λD[F1+F2] é realizado por essa matriz exatamente quando

    ||v1||²=||v2||²=λ e ||v1−v2||²=0.

Prova: ||v1−v2||²=C11+C22−2 Re C12. Com diagonais λ e C positivo, |C12|≤λ. O resíduo zero força Re C12=λ e, pela desigualdade, Im C12=0. Reciprocamente C=λ[[1,1],[1,1]] dá as duas condições. A base F1,F2 e a fase relativa são fixadas; igualdade de matrizes é suficiente para igualdade dos geradores. Não afirmamos unicidade de uma representação GKLS arbitrária sem fixar redundâncias da base.

**Posto1 sozinho não basta.** C=λ[[1,−1],[−1,1]] é positiva de posto1, mas corresponde a λD[F1−F2]. Em geral |C12|=λ permite uma fase: C12=λe^(iφ) corresponde ao salto √λ(F1+e^(−iφ)F2). Essa fase precisa ser transportada ao Hamiltoniano/bomba/leitura conforme R74; não se apaga só no dissipador.

Com diagonais iguais e C12=λζ, |ζ|≤1, os autovalores são λ(1±|ζ|). A razão entre o segundo e o primeiro é (1−|ζ|)/(1+|ζ|). ζ=0 descreve dois canais independentes; |ζ|=1 dá apenas um canal; ζ=1 seleciona a fase exigida pelo J da fonte. Para λ=0, o banho é nulo: satisfaz trivialmente a igualdade de matrizes, mas não testemunha um canal ativo. O verificador recusa esse caso para o requisito de não vacuidade.

## 2. Compatibilidade temporal: reutilizar a fase exige conservar sua diferença

No domínio algébrico de ocupação finita, com h0=ω_i n_i+ω_o n_o+ω_e n_e,

    [h0,F1]=(ω_o−ω_e)F1,
    [h0,F2]=(ω_e−ω_i)F2.

Assim F1(t)=exp(iν1 t)F1, F2(t)=exp(iν2 t)F2 e o coeficiente cruzado no dissipador transportado contém exp(iδt), onde δ=ν1−ν2=ω_i+ω_o−2ω_e. A média uniforme numa janela [0,τ] é exatamente

    m(δ,τ)=exp(iδτ/2) sinc(δτ/2), sinc(0)=1.

Isso é integração elementar, não uma aproximação de banho provada. Se a redução adotada É essa média, C12 passa a C12 m, as diagonais ficam iguais e a positividade é preservada porque |m|≤1. Para τ>0 e δ≠0, |m|<1: um canal inicialmente de posto1 não permanece de posto1 na média. Na média infinita, o cruzamento desaparece quando δ≠0.

**[INPUT — H_STATIONARY_SECULAR]** Uma redução estacionária/secular que separa essas frequências nuas não pode simultaneamente conservar o salto único constante da fonte quando δ≠0. A afirmação é restrita a essa redução e a esse h0. No sistema fortemente acoplado, devem-se decompor operadores no Hamiltoniano completo; com drive, usar o referencial/período apropriado. Não se chama frequência nua de frequência vestida.

Um bombeamento/engenharia de reservatório pode fornecer fases m1(t),m2(t), exigindo (ν1−ν2)t+arg m1(t)−arg m2(t) constante para remover essa diferença. Esta é uma condição de ligação, não um mecanismo já identificado. Mudar o nome do referencial não cria a correlação: o transporte R74 mantém integralmente as fases distintas de J. A existência de uma bomba de OH também não demonstra que ela modula cada termo do banho dessa maneira.

No ramo condicional em que ambos a_i,a_o são os modos ópticos780nm e ω_e é a transição OH da patente, a diferença acima é grande e não zero. A fonte deve dizer se a_i,a_o são esses modos, envelopes/conversões ou modos efetivos distintos. Não resolver essa identidade escolhendo frequências efetivas que façam δ desaparecer sem derivar a transformação física.

## 3. Modo brilhante: alinhamento da bomba e preservação dinâmica são requisitos separados

Reusar R79: b=g/||g||, P=bb†, Ω_B=b†Ω, Ω_dark=(I−P)Ω. No setor zero/uma excitação, a redução coerente ao modo brilhante exige Ω_dark=0. Se D=diag(Δ_s) contém detunings reais, a condição adicional é (I−P)Db=0; ela equivale a todos os Δ_s com g_s≠0 serem iguais. Prova: Db=μb implica Δ_s=μ em cada componente não nula; a recíproca é imediata. Isso não garante invariância sob dissipadores/interações adicionais: cada um precisa de sua própria verificação. Tampouco torna várias excitações um qubit.

Assim há dois resíduos calculáveis a partir dos perfis existentes, sem ajustar β: ||Ω_dark|| e ||(I−P)Db||. E há dois testes do banho: igualdade das intensidades e igualdade complexa das linhas de acoplamento. Nenhuma gramática ontológica substitui esses resíduos; nenhuma ausência desses dados apaga as construções R66–R79.

## 4. O próximo objeto consumível

`material_contract_r80.py` verifica um registro explícito de g_s, Ω_s, detunings, C11,C22,C12, α,γΛ e diferença de frequência do modelo reduzido. β=α√e é calculado em runtime; λ=βγΛ. Valores, unidades, procedência e tolerâncias são entradas explícitas. Dados ausentes, booleanos, não finitos, C não positiva ou canal nulo são recusados. O resultado técnico só diz compatibilidade com esse contrato algébrico e tolerâncias; não certifica a redução física, o aparato, a rede global, o regime de folha ou a TGL experimentalmente.

O registro material da casa permanece OPEN se esses elementos não forem recuperados como um conjunto ligado ao mesmo aparelho. Exemplos sintéticos não preenchem o registro material. Não haverá nova trajetória R78/R79 nesta etapa.
