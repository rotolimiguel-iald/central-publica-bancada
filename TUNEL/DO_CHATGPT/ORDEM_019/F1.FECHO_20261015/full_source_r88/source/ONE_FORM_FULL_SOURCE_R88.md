# R88 — Primeira variação e fonte do ramo literal de 1-forma

Autor /root/r69_locality_bridge. [DERIVED — demonstração analítica sob contrato nomeado; candidato]. [REAL — 98 controles algébricos locais exatos, execução única, pré-registro por hash]. Não é identificação canônica de Ψ, solução dinâmica, prova Lean ou H3 fornecida. Missão projetada revision572/check ready=true. O operador está sendo consultado sobre o mapa escalar→1-forma; esta nota não responde por ele.

## 1. Contrato R: campo REAL e fonte ainda não escolhida dos demais setores

Reutilize as fontes R87: o Custo escreve L_campo=−¼Φ_abΦ^{ab}, Φ=dΨ, e L_grav=(F0+ξ|Ψ|²)R, mas chama Ψ escalar. Isolamos a leitura literalmente compatível com os índices: A=A_a dx^a é 1-forma REAL, independente da métrica quando variamos g^{ab}; F_ab=∂a A_b−∂b A_a. Não afirmamos A=Psi(P), A=J, A=dphi ou equivalência ao escalar. Seja

    u=g^{ab}A_a A_b, f=F0+ξu,
    S[g,A,χ]=∫√|g| [fR(g)−¼F_ab F^{ab}+L_rest(g,A,χ)].             (1)

F0 e ξ constantes, dimensão4, assinatura(+---), curvatura/LC da carta do kernel. L_rest designa os DEMAIS TERMOS DA MESMA AÇÃO, e χ seus campos; não substituímos L_LCDM por −ρ, nem w_eff(z) por funcional inventado. Suas derivadas funcionais E_rest e T_rest abaixo são objetos ainda a identificar nas fontes completas. A derivação é métrica/Levi-Civita, não variação independente de Cartan. Integrações por partes têm suporte compacto interior ou bordo já legitimamente compensado; R82/R86 tratam essa obrigação, que não é apagada.

A norma u é contração lorentziana, não norma positiva automática. O setor só admite divisão por f se f≠0, condição que não é deduzida de ξ>0. Mantemos as equações sem divisão.

## 2. Variação métrica: o termo adicional obrigatório

Com A e F_ab fixos,

    δu=A_a A_b δg^{ab},
    δ(F²)=2 F_ac F_b{}^c δg^{ab},
    δ√|g|=−½√|g| g_ab δg^{ab}.

Defina S_ab=F_ac F_b{}^c e o tensor Hilbert na convenção EXPLÍCITA

    T_M,ab := −2/√|g| δS_Maxwell/δg^{ab}
             = S_ab−¼g_ab F²,
    T_rest,ab := −2/√|g| δS_rest/δg^{ab}.

Reutilizando a variação integrada de fR, mas incluindo a dependência métrica de f, o Euler métrico E_g (coeficiente de √|g|δg^{ab}) é

    E_g,ab = fG_ab+(g_ab□−∇a∇b)f+ξR A_aA_b
             −½(T_M,ab+T_rest,ab).                              (2)

O termo ξR A_aA_b não está presente se f for um escalar externo independente da métrica. Ele não pode ser retirado por identificar as duas normas. A primeira variação completa é

    δS=∫√|g|[E_g,ab δg^{ab}+E_A^b δA_b+E_χ δχ]+bordo.          (3)

Para todo k nulo, a equação métrica E_g=0 implica, SEM dividir por f,

    2f Ric(k,k) = T_M(k,k)+T_rest(k,k)
                  +2ξ Hess(u)(k,k)−2ξR[A(k)]².                 (4)

Essa é a fonte nula do contrato1-forma, não a hipótese H3 pronta do registro sigma. Para compará-la com coefficient*recordSource, deve-se provar igualdade com TODOS os termos de(4) e a normalização de f.

Equivalentemente, mantendo apenas o coeficiente F0 à esquerda,

    2F0 G = T_full,
    T_full=T_M+T_rest−2ξuG
            +2ξ(Hess u−g□u)−2ξR A⊗A.                         (5)

O aparecimento de G no lado direito é a forma padrão de escrever o termo não minimal como fonte; não é solução explícita para g nem definição independente do registro físico.

### Sinal da carta, sem corrigir silenciosamente o artigo

Na assinatura(+---), o tensor de energia Maxwell usual positivo é −S_ab+g_abF²/4, isto é, −T_M nesta convenção. Por exemplo, F_01=E em Minkowski dá T_M,00=−E²/2. Logo +EH e −¼F² com T=−2δS, tal como(1), NÃO recebe automaticamente a fonte de energia positiva usada em outros ramos. Trocar apenas a definição nominal de T não muda a equação E_g=0. Uma tradução global de assinatura/curvatura/ação ou alteração do sinal relativo exige contrato; não foi feita aqui. O ramo ambiente de09/09 fixa sinais próprios, preservados em R87. A fórmula(2) continua a derivada literal do ramo nomeado.

## 3. Variação da 1-forma, restrição diferencial e gauge

Como δF_ab=∇aδA_b−∇bδA_a,

    δS_Maxwell = ∫√|g| (∇a F^{ab}) δA_b +bordo,
    E_A^b = ∇aF^{ab}+2ξR A^b+E_rest^b,
    E_rest^b=(1/√|g|)δS_rest/δA_b.                             (6)

As derivadas funcionais de L_rest incluem seus termos derivativos, se existirem. Não inserir um termo βK A ou massa que ainda não tenha sido fornecido pela mesma ação. Tomando a divergência, a antissimetria e o Ricci simétrico dão ∇b∇aF^{ab}=0; portanto a EOM vetorial exige

    2ξ∇b(RA^b)+∇bE_rest^b=0.                                 (7)

Isso é restrição dinâmica e não identidade de gauge do setor não minimal. De fato, sob A→A+dχ, F fica fixo mas

    u→u+2 A·dχ+(dχ)².

Logo ξRu quebra a invariância eletromagnética dessa transformação em geral; ξ=0, R=0 ou compensações explícitas seriam casos especiais. Não afirmar que o termo −¼F², isoladamente gauge-invariante, torna a ação inteira gauge-invariante.

## 4. Identidade de Noether e conservação com todas as equações materiais

Para difeomorfismo infinitesimal X, δg^{ab}=−2∇^{(a}X^{b)} e
δA_a=X^b∇bA_a+A_b∇aX^b. Inserir em(3) e integrar por partes dá, quando χ está on-shell,

    2∇^a E_g,ab + E_A^a F_ba − A_b∇aE_A^a =0.                 (8)

Se χ não está on-shell, somar seu termo Noether. Para χ escalar, ele é E_χ∂bχ; campos com índices carregam também as parcelas de sua transformação de Lie. Não se omite essa contribuição sob rótulo 'rest'.

Usando E_g=F0G−T_full/2 e Bianchi,

    ∇^a T_full,ab = E_A^aF_ba−A_b∇aE_A^a                     (9)

com χ on-shell. Assim E_A=0 E as demais equações materiais dão conservação da fonte COMPLETA. T_M isolado geralmente troca energia com ξRu e os demais termos; não deve ser declarado conservado separadamente. (8) é identidade fora da casca das EOM vetoriais; não demonstra que o A(P) ainda não construído satisfaz(6). Tampouco a conservação sozinha prova(4).

## 5. Contrato C: extensão COMPLEXA literal, explicitamente distinta

Se A é complexo, a extensão REAL da densidade que usamos para comparação é

    u=g^{ab}bar(A_a)A_b,
    L_C=(F0+ξu)R−¼ bar(F_ab)F^{ab}+L_rest,C.                  (10)

Os fatores são escolha nomeada C; '−¼F²' sem barra poderia ser uma ação complexa diferente. Nesta extensão u é real mas continua lorentziano. Defina

    C_ab=Re[bar(A_a)A_b],
    S_C,ab=Re[bar(F_ac)F_b{}^c],
    T_M,C=S_C−¼g bar(F)·F.

δu=C_abδg^{ab}; (2),(4),(5) valem substituindo A⊗A por C e F² por barF·F. A variação independente em barA fornece

    E_barA^b=½∇aF^{ab}+ξR A^b+E_rest,barA^b.                 (11)

A equação conjugada vem de A. Na restrição real ambas as variações se somam, reproduzindo(6). A normalização alternativa −½barF·F, usual se A codifica dois campos reais sem fator1/sqrt2, teria coeficiente1 em ∇F e tensor Maxwell duplicado; não misturá-la com(10). A Noether(8) ganha 2Re[E_barA^a barF_ba−barA_b∇aE_barA^a] em lugar da parcela real, com ação total real. Nenhuma dessas escolhas identifica automaticamente A com a fase de outro campo.

## 6. A equação escalar não emerge da troca de nomes

A EOM(6) é equação de 1-forma com operador Maxwell, acoplamento vetorial ξR e restrição(7). A fonte do Custo10418–10431 enuncia, para escalar, (□−m²−ξR)ψ=βKψ. O índice, símbolo principal e termos de massa/fonte dessas duas expressões não coincidem por notação.

Há uma ligação condicional exata já isolada em R87: se A=dψ, F=d²ψ=0. Substituir ANTES de variar define a ação escalar reduzida com ξR(dψ)²; seu Euler do setor exibido é −2ξ∇a(R∇^aψ)=0, somado ao Euler dos termos restantes. Não é Klein–Gordon com massa e fonte βK dadas. Além disso, restringir antes de variar só testa variações δA=dδψ e não equivale à EOM vetorial livre. Sem novo mapa/interação não se pode apresentar o ramo calculado como a EOM escalar do artigo.

## 7. Controle exato e resultado entregue

EXACT_PLAN_R88.json foi pinado ANTES da única execução de exact_source_variation_r88.py. Em24 combinações racionais (2métricas inversas,2covetores,2tensores antissimétricos,3variações simétricas), verificaram-se δu, δF², a derivada da densidade incluindo δR fornecido independentemente e o traço Maxwell em4D:96 identidades. Mais2 identidades complexas:98resíduos exatamente zero. O controle que omite a derivada métrica de u dá resíduo NÃO ZERO nos24casos. EXIT0, 1,847437s, SymPy conforme resultado. Os controles são locais: não computam curvatura completa, EOM integrada ou Noether; essas provas são analíticas acima e reutilizam os fornecedores da variação de R.

[DERIVED] A primeira variação e a fonte do ramo1-forma agora estão explícitas, incluindo o termo que seria perdido pela norma escalar. [OPEN] Mapa de Ψ para A, estado/material L_rest e sua resposta fora do fundo, sinais físicos comuns e demonstração de E_g=E_A=E_χ=0 na construção same-P. Nada foi instalado no kernel, no programa ou na memória.
