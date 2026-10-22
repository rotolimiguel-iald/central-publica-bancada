[DERIVED — canal de traço do resíduo ghost; REAL — CAS; OPEN — Q2 causal]
# A7.b — primeiro operador curvo no canal de traço ghost
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:52:46.462755+00:00.

Partimos da redução em fundo fixo de ghost_minimal_heat/DERIVACAO.md,
SHA256 `3415ce095d72805d7b1ef551eb42b01c046f04712bdc3e265b08bc2705add759`. Suas condições analíticas
continuam explícitas: resíduo local de calor/ciclicidade de símbolos, h pequeno
como série formal, resultado integrado módulo divergências. Não é parte finita.

Para h=f g, defina v=df, S=Hess f e d=box f. No referencial ortonormal,

    C=-df, A_mu=v_mu I-v e_mu^t, B=-S, D=B-box h=-S-d I,
    F_mu,nu=-S[:,mu]e_nu^t+S[:,nu]e_mu^t.

As contrações matriciais, verificadas para v e S simbólicos arbitrários, são

    tr sum A_mu A^mu=3v²,
    tr D²=tr S²+6d²,
    tr sum F_mu,nu F^mu,nu=2tr S²-2d²,
    tr sum Omega0_mu,nu[A^mu,A^nu]=-6K v².

Portanto, ponto a ponto para esta representante do resíduo,

    a4_2(f g)=|Hess f|²/6+17(box f)²/24+5K f box f-4K|df|².

Com f compacto, integral f box f=-integral|df|². A outra redução não pode
ser feita como se as derivadas comutassem sobre df. Por integração por partes,
integral|Hess f|²=-integral df·(grad box f+Ric(df)); Ric=3K g. Logo

    integral|Hess f|²=integral(box f)²-3K integral|df|²,
    integral a4_2(f g)=integral[7(box f)²/8-(19K/2)|df|²].

Sua Hessiana no canal f, com o fator angular da bolha retirado, é

    **H_ghost,trace = (7/4)box²+19K box.**

O termo K² f² é zero neste canal. Isso é compatível com f constante:
Q(f)=(1+f)Q(0), cujo fator multiplicativo não tem resíduo log nas condições
declaradas. Não há alegação de igualdade dos determinantes finitos.
Em K=0, a polarização identidade/identidade no resultado antigo dá7p⁴/4,
o mesmo coeficiente, sem ajuste. Omitir o comutador de conexão muda a ação
por -K|df|²/4; omitir Ric na identidade integrada muda por -K|df|²/2.

23 checks,3 negativos,rc0,CPU 0.0625s. Não é a Hessiana
tensorial hh completa nem sua soma com o setor métrico. Não foi feita a
continuação causal inteira; derivadas do cutoff reaparecem se ele for variável.
Contribuição escrita e rastreável, sem novo teorema Lean, original ou gate.
