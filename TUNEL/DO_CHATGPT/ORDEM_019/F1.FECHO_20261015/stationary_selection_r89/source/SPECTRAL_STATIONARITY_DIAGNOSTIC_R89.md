# R89 — Identidade espectral do mesmo registro e seleção estacionária

Autor: /root/r69_locality_bridge. [DERIVED — análise em dimensão finita e primeira variação funcional; não nova execução nem prova Lean]. Referência própria projetada e check ready na revisão575. Esta nota cumpre a correção humana: parte da regra de satisfação já existente, não propõe nova escolha de Ψ nem nova pergunta. Preserva a ação completa e distingue os ramos já demonstrados.

## 1. A satisfação espectral que é automática

Seja U uma carta e P_i(x)>0 suave, Σ_iP_i=1. Em base FIXA, ρ(P)=diag(P_i) é fiel. Defina H_ρ=−logρ, Ω_ρ=√ρ e o superoperador modular K_ρ(X)=Xlogρ−logρX. ContinuousModularZero.lean:65–94 já fornece K_ρΩ_ρ=0 e JK_ρJ=−K_ρ. Não confundimos K_ρ com a matriz H_ρ.

Como funções do mesmo operador comutam,

    [H_ρ,ρ]=0, K_ρΩ_ρ=0,
    D_ρ=f(ρ) ⇒ [D_ρ,ρ]=0,
    L_ρ(ρ)=β(D_ρρD_ρ−{D_ρ²,ρ}/2)=0.

Aqui f é real no espectro, D autoadjunto, β>0; para o fornecedor da Ponte/um.py, D=√H_ρ é admissível pois −log P_i≥0. Nada nessa conclusão restringe o gradiente espacial de P. O resultado vale para TODO P positivo normalizado, inclusive todos os P que satisfazem posto4/Fisher positivo e relógio nãozero. Não é uma equação gravitacional escondida: é identidade do cálculo funcional do mesmo registro.

## 2. Derivar o comutador não produz uma restrição nova

Para uma curva ρ_ε fiel e H_ε=−logρ_ε, a derivação da igualdade dá

    δ[H,ρ]=[δH,ρ]+[H,δρ]=0.                         (I)

Em base própria no ponto, seja h(t)=−log t. A derivada de h é o mapa de quocientes divididos:

    (δH)_ij=h^[1](p_i,p_j) δρ_ij,
    h^[1](u,v)=(h(u)−h(v))/(u−v), u≠v; h^[1](u,u)=h′(u).

Logo o coeficiente de δρ_ij em (I) é (p_j−p_i)h^[1](p_i,p_j)+h(p_i)−h(p_j)=0. Nos blocos degenerados ambos os gaps são zero. Para a curva diagonal da casa, δH=diag(−δp_i/p_i) e ambos os comutadores se anulam separadamente. A regra do produto sozinha e a identidade [h(ρ_ε),ρ_ε]=0 já provam (I); o quociente dividido exibe o cancelamento, sem exigir espectro simples. A mesma afirmação vale para D=f(ρ), quando o cálculo funcional é diferenciável na faixa espectral considerada.

No GNS, a derivada correta é (δK)Ω+KδΩ=0. Omitir δK enquanto se varia P seria variar o estado com o gerador FIXO, outro problema legítimo, mas diferente da família same-P. Pela mesma razão, todas as derivadas espaciais da identidade anulam-se automaticamente, incluindo os termos de derivada do operador; elas não se tornam Euler–Lagrange da ação completa.

## 3. O gradiente tem objeto e parâmetro de variação definidos

R88 recuperou Φ_D(X)=β||[D,X]||²_HS/4 e L_DX=−∇_XΦ_D(X), com D FIXO ao diferenciar X. O conjunto de mínimos é o comutante, não em geral um único estado. E_D é a pinçagem nos blocos espectrais; E_DX=alvo é a condição de satisfação já tipada em RuleTruthContract e TheRuleInTheContinuousMotor.

Na família composta X=ρ(P), D=D(P),

    Φ_{D(P)}(ρ(P))=0 para todo P,
    δΦ = (β/2) Re<[D,ρ],[δD,ρ]+[D,δρ]>=0.

Esta é a primeira variação de um funcional IDENTICAMENTE ZERO. Não é δS_full[P]. O símbolo de gradiente negativo não permite identificar seus domínios nem suas métricas de variação por homonímia. Para o fluxo GKLS, o tempo de relaxação e x da carta também são variáveis distintas: estacionário para cada gerador em x não fornece equações diferenciais relacionando x e x+dx.

Reuso adicional: VariationalInhabitant.lean:87–98 prova Gibbs crítico sob logp_i+h_i=c com h FIXO durante a variação de p. Qualquer p positivo pode satisfazer a hipótese escolhendo h_i=−logp_i no ponto-base; isso não constrói uma lei independente que selecione o campo espacial P. Se h também varia com P, deve-se incluir −Σp_i δh_i. Não se apaga esse termo para converter uma família de problemas de energia livre em uma única ação gravitacional.

## 4. Três alvos que não podem ser confundidos

1. **Alvo que acompanha o estado:** Y(P,x)=ρ(P,x), leitura E_{D(P,x)}. A satisfação E_Dρ=Y é automática. Não seleciona os campos P.
2. **Alvo completo fixo e constante:** Y independente de P e de x, na mesma base. Como E_D(diagP)=diagP, E_Dρ=Y implica ρ=Y; se Y é diagonal admitido, P é constante. Então dP=0, Fisher não tem posto4 e o relógio selecionado é zero. Se Y não é diagonal nessa base, não há solução dessa forma. Logo esse alvo não é o fornecedor geométrico não degenerado de SelectedProbabilityData.
3. **Alvo fixado como campo Y(x), ou leitura parcial:** Y(x) independente da incógnita pode ter posto4; sua satisfação completa impõe P=diagY(x), mas as equações de movimento desse campo ainda têm de ser verificadas. Uma leitura parcial R(P)=Y deixa fibras; a regra pode selecionar uma fibra sem tornar a ação constante nela. Idempotência não elimina esse problema. Para variações restritas à fibra, δS deve anular ker DR; equivalentemente seu diferencial pertence ao anulador dessa tangente, quando a fibra é regular. Isso é estacionariedade RESTRITA, não estacionariedade ambiente nem H3 automático.

## 5. Controle positivo e controle negativo já existentes

**Positivo P5:** P5_COVARIANT_STATIONARITY_R88.txt:4–44 e sua precisão de domínio demonstram que todo P5 positivo de posto4 é localmente uma carta do simplex. No ramo AMBIENTE Einstein–sigma S³ já escolhido em setembro, κc=4 e Λ=3/4 anulam os coeficientes métricos, materiais e do multiplicador. A covariância transporta a solução e a primeira variação compacta é zero. Para κc diferente, a mesma satisfação espectral ainda vale, mas Ric(k,k)=κT(k,k) não vale nas direções nulas nãozero (U não vazio). Isto é um contraste dentro da MESMA classe P5: o critério espectral não determina a compatibilidade dos coeficientes. Não se está propondo variar constantes físicas para ajustar um resultado; é uma não-implicação lógica e a compatibilidade do ramo permanece fixada como na fonte.

**Negativo P16:** o P16 normalizado/positivo e de posto4 construído em R85 também satisfaz todas as identidades do §1. P16_RESULT_R86.json já calculou, sem novo teste aqui, para o setor EH–sigma COMPOSTO explicitamente delimitado,

    E_s=740 c_G/1521,
    E_ab k^a k^b=140 F_c/117+2 c_G/9>0 (F_c,c_G>0).

INTEGRATED_VARIATION_AND_STATIONARITY_R86.txt:94–105 constrói uma variação admissível de suporte compacto com δS_red<0. Assim o mesmo campo de probabilidades pode satisfazer sua identidade modular e não ser estacionário para esse setor. P16 tem alvo sigma S14, não S³: não refuta o ramo P5. Esses dois fatos refutam a inferência genérica 'identidade do mesmo estado ⇒ estacionariedade de qualquer ação associada'. NÃO refutam a TGL completa. Os termos adicionais do Custo podem modificar os resíduos; não foram omitidos sob alegação de representar a ação inteira.

## 6. Critério efetivo e próxima ligação executável

Seja F(P)=(g(P),A(P),χ(P),...) o mapa de campos da MESMA ação completa, incluindo norma métrica, acoplamento não minimal e resposta fora do fundo do termo modular. Denote E_full os coeficientes Euler da variação integrada com contorno admitido. Então, para v=δP de traço zero e suporte compacto,

    δS_full[P](v)=<E_full(F(P)), DF_P v>
                =<DF_P^* E_full, v>.                       (II)

O adjunto em (II) é formal após integrações por partes, pois DF pode conter derivadas de v. Criticidade no espaço de probabilidades exige que a projeção de DF_P^*E_full na tangente Σv_i=0 se anule; em uma carta regular sem outras restrições isso equivale a todos os Euler reduzidos diferirem apenas por multiplicador comum. Para inferir equações ambientes/nulas deve-se ainda usar alcance das variações ou verificar os coeficientes ambientes, como já feito no P5. Não basta a variação na órbita de difeomorfismos.

Uma ponte dinâmica suficiente, verificável e não nominal seria demonstrar que um gerador INDEPENDENTEMENTE construído sobre o espaço de campos satisfaz V(P)=−M_P Proj_tan(DF_P^*E_full), onde M_P é positiva e injetiva na tangente relevante, com condições de contorno compatíveis. Então V(P)=0 realmente implicaria criticidade reduzida. A família pontual L_{ρ(P)}ρ(P)=0 não fornece essa identidade: se a fornecesse com M injetiva, faria a ação crítica em todos os P; o controle R86 já exclui isso para o setor reduzido. Esta nota não inventa M, V ou a ação; explicita a identidade que deve ser consumida pela seleção já escrita.

Próximo avanço concreto: reaproveitar P5 como testemunha já estacionária; transportar o DIFERENCIAL da representação espectral recuperada para cada campo que a ação completa realmente usa, compor (II) com os Eulers R88 sem descartar E_rest/T_rest, e testar se a regra tem alvo independente que anule esse resíduo. O que falta é essa igualdade de operadores/funcionais com seus domínios, não outra definição verbal de satisfação. Não fazer nova pergunta abstrata ao operador.

## 7. Escopo

Demonstrações algébricas/variacionais nesta nota são [DERIVED], sem nova compilação ou execução científica. As fontes formais foram lidas; seus builds históricos não foram refeitos. Controle P16 e ramo P5 são reutilizados com pinos atuais. Não houve pesquisa global, dados observados, chamada externa, alteração de memória/cânone/gate, nem conclusão sobre a ação completa com um setor em seu lugar.
