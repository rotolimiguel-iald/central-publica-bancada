# Adendo material R85 — incompatibilidade sigma livre e fonte da ação composta

19/10/2026, /root/r69_locality_bridge. Claim996; revisão566, project/check ready.
[DERIVED] Derivação analítica. Preserva integralmente a nota anterior pinada
6ae58c76573309d253691ece03716c06016af8009ba92ba91083060ad1f92128.
Achado identificado pelo root e conferido por este autor e pelo revisor R68.
Não executa novamente o controle de rank nem altera suas evidências.

## 1. Correção de alcance: P16 livre não é candidato sigma cinético on-shell

A nota anterior provou o levantamento de campos métricos pela segunda forma
fundamental M e registrou a condição adicional E_φ radial como via suficiente.
Essa condição NÃO pode ser satisfeita simultaneamente com M livre no setor
sigma cinético puro considerado. A condicional anterior é logicamente correta,
mas, nesse setor, suas premissas conjuntas são impossíveis. Não a promover
como rota habitada para H3.

Com ψ_rest=rφ e normais N=(0,N_rest) de componente selecionada zero,
N_rest é ortogonal a φ e a cada ∂_aφ. Logo os termos de Christoffel e as
primeiras derivadas de r não contribuem à projeção normal, e

    M_ab,N=〈N,II_ab(ψ)〉=r〈N_rest,∂_a∂_bφ〉,
    〈N_rest,□_gφ〉=(1/r) g^{ab}M_ab,N.                 (1)

Se □_gφ=λφ, o lado esquerdo é zero. Se as dez M_α formam base de Sym²,
isso exigiria g^{ab}H_ab=0 para TODO tensor simétrico H, isto é, g⁻¹=0,
contradizendo a não degenerescência. A soma usa os dois termos para índices
fora da diagonal; esse fator2 não altera o argumento nem o rank.

No P16 explicitamente construído, em0 e na base interna anterior a O,

    (□_gφ)_normal=(3/13)e_00−(1/3)(e_11+e_22+e_33) ≠0.

Aqui g⁻¹=diag(3/13,−1/3,−1/3,−1/3), a componente normal de ∂_a∂_bη é e_ab,
e Γ∂φ é tangente. A normalização só acrescenta componente radial e_*.
Rotação O preserva a não nulidade. Potenciais que dependem somente de |φ|²,
ou ξR|φ|², geram termos radiais e não cancelam esse normal. Outras interações,
fontes ou acoplamentos completos podem cancelá-lo; isso requer sua derivação.
Não se conclui que a TGL física esteja refutada.

## 2. Eliminação exata da cinética sigma na ação COMPOSTA

Não é necessário impor E_φ radial para estudar a ação composta: pode-se
eliminar exatamente o termo cinético usando a construção Fisher/reflexão.
Fixe s=P_s∈(0,1), c=ds, h=Σ_j dφ_j⊗dφ_j, r²=4(1−s),

    F=ccᵀ/[s(1−s)]+r²h,
    q=cᵀF⁻¹c=cᵀg⁻¹c>0,
    g=2ccᵀ/q−F,
    g⁻¹=(2/q)(F⁻¹c)(F⁻¹c)ᵀ−F⁻¹.

Contraindo a última fórmula com F, em dimensão4,

    tr(g⁻¹F)=2−4=−2,
    Qσ:=tr(g⁻¹h)=[−2−q/(s(1−s))]/[4(1−s)].           (2)

Para o contrato de ação com cinética Lσ^−=−(c_G/2)Qσ, c_G constante positivo,
a igualdade P a P é

    Lσ^−[P]=A(s)+B(s)q,
    A(s)=c_G/[4(1−s)],
    B(s)=c_G/[8s(1−s)²].                              (3)

Não é aproximação sobre um fundo, nem só coincidência de valores numa solução:
(2) vale em TODA construção P admissível. Assim a ação composta desse setor
pode ser escrita em termos de g(P) e s(P), sem manter uma δφ indevidamente fixa.

## 3. Convenções: sinal da fonte não pode ser trocado por nome

O kernel ScalarMatterDensityVariation.lean:97–98 usa a cinética OPOSTA,
Lσ^+=+(c_G/2)Qσ, e:141–152 prova para δg_ab=h_ab

    δSσ^+=−(1/2)∫√|g| (g⁻¹ Tσ g⁻¹):h.

Logo sua fonte nomeada Tσ é +2/√|g| δSσ^+/δg^{ab}. Já o contrato com
Lσ^− usa a definição Tσ=−2/√|g| δSσ^−/δg^{ab}. Nas duas convenções
PAREADAS o tensor fixando φ é o mesmo:

    Tσ=c_G[h−(Qσ/2)g].

R83 somou densidade gravitacional e scalarMatterDensity positiva, apenas como
teorema de derivação local. Não transformá-lo silenciosamente numa ação
EH−sigma com equação Einstein de sinal positivo. O sinal RELATIVO matéria/EH
precisa ser escolhido/identificado na ação física completa.

No contrato Lσ^− da equação(3), variar a métrica inversa mantendo s fixo dá

    δ(√|g|L_eff)=√|g|[B c_a c_b−(L_eff/2)g_ab]δg^{ab},
    T_eff=(A+Bq)g−2B ccᵀ.                            (4)

Se for usado Lσ^+ reduzido=−A−Bq junto da convenção +2, o tensor (4)
permanece igual. Isso não torna iguais os sinais relativos das ações totais.
T_eff é a fonte de Hilbert da ação REDUZIDA definida em(3), não a fonte
Tσ de SelectedSigmaRecord fixando φ. Essa distinção é o resultado material.

## 4. Contraste nulo: a redução muda efetivamente a fonte

Para ℓ não nulo e g-nulo, a relação g(ℓ,ℓ)=0 implica F(ℓ,ℓ)=2(c·ℓ)²/q.
Consequentemente

    Tσ(ℓ,ℓ)=c_G/r² [2/q−1/(s(1−s))](c·ℓ)²,
    T_eff(ℓ,ℓ)=−c_G/[4s(1−s)²](c·ℓ)².               (5)

Como F≥ccᵀ/[s(1−s)] em ordem positiva, conjugação por F⁻¹/² implica
0<q≤s(1−s). O covetor c é timelike para g; por isso c·ℓ≠0 para ℓ nulo
não zero. Logo Tσ(ℓ,ℓ)>0 enquanto T_eff(ℓ,ℓ)<0. O primeiro é o tensor da
leitura sigma existente; o segundo inclui a variação induzida da mesma matéria
pela mudança de P. Não podem ser identificados.

Controle algébrico exato no P16 em0, com ℓ=(1,√13/3,0,0):

    s=1/4, c·ℓ=1/2, q=3/52, r²=3,
    Tσ(ℓ,ℓ)=22c_G/9,    T_eff(ℓ,ℓ)=−4c_G/9.

Esses números seguem de substituição racional em(5), sem nova campanha;
o radical só verifica g(ℓ,ℓ)=13/3−3·13/9=0. Para cinética/gravitacional
simplificadas com coeficiente positivo, Einstein com T_eff não pode ser ao
mesmo tempo H3 com Tσ positivo. Uma constante cosmológica não muda a projeção
nula. Isso limita ESSE setor truncado, não a fonte completa da TGL.

## 5. O que o levantamento livre permite concluir de modo correto

Considere explicitamente, como contrato simplificado,

    S_red[g,s]=∫√|g| [F_c R + A(s)+B(s)g⁻¹(ds,ds)],

F_c constante não nula, com contorno legitimamente tratado. A igualdade
funcional composta decorre de(2)–(3), caso a ação original seja justamente esse
setor EH−sigma. A condição de rank10 já construída permite variações g livres
com s fixo. PORTANTO, se uma dinâmica independente realmente produzir
estacionariedade de S_red[g(P),s(P)], sua equação métrica é

    F_c G_ab=(1/2)T_eff,ab,

e não a equação com Tσ. Isso é identificação derivada do Euler da ação
composta, não prova de que a configuração seja estacionária.

Pode-se também levantar conjuntamente (δg,δs): primeiro tome uma variação
normalizada com δs arbitrária e δφ=0; ela produz algum δg=W. Depois use o
levantamento normal de relógio fixo para substituir W por qualquer H desejado.
Os dois suportes permanecem compactos. Assim a equação escalar desse setor,
quando houver estacionariedade, é

    A'(s)+B'(s)q−2∇_a[B(s)∇^a s]=0.

Nenhuma dessas equações foi imposta como campo da estrutura para chamar a
construção de sucesso. O progresso é: a fonte efetiva e as equações necessárias
foram identificadas exatamente, preservando todas as variações same-P.
Faltam a seleção dinâmica independente e a ação/fonte completas com os outros
termos do artigo. Não acrescentar uma hipótese E=0 para encerrar a missão.

Fontes herdadas: manifesto SOURCE_PINS_SELECTION_R85.json, controles de rank
EXACT_RANK_RESULT_R85.json; novas âncoras ScalarMatterDensityVariation:97–118,
141–152 e pedra R83 final. Sem nova execução Lean, produção, memória ou gate.
