[DERIVED — contribuição singular de primeira curvatura; REAL — CAS exato; OPEN — soma causal]
# A7.b — bitensores na primeira bolha antifield–ghost
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:14:37.926327+00:00.

**Escopo e convenção da fonte.** Cálculo auxiliar euclidiano do coeficiente K
no espaço-forma, retirando 1/(4pi²) de cada propagador, os fatores globais
4kappa, ghost e a fase da fonte. A fonte externa T^ab no integrando é uma
densidade contravariante, pareada com h_ab por d⁴X. Se o antifield original
for escrito usando o volume, T inclui esse volume e a elevação dos índices.
Não se deve manter T constante e multiplicar novamente pelo volume em X.
O vértice ghost usa o volume em Y; Y=0 em coordenadas normais. Essa convenção
especifica o perfil de coordenadas calculado, não muda a ação069.

**Transporte incluído.** A conexão normal é
Gamma^a_mb=-(K/3)(delta_ab x_m+delta_am x_b-2delta_mb x_a).
Integrá-la ao longo do segmento fornece, com d=X-Y,s=X+Y,

    P^a_b'(X,Y)=delta_ab+(K/6)[delta_ab(X²-Y²)+d_a s_b-2s_a d_b]+… .

Verificados por álgebra: P^t g(X)P=g(Y), inversão X/Y, R^a_bmn,
os jatos de P e do propagador métrico, antes de pôr Y=0. Para o bitensor
com índices baixos G_ab'=g_ac(X)P^c_b',

    G_ab'(x,0)=delta_ab-(K/6)(delta_ab z-x_a x_b),
    partial_Yj G_ab'|Y=0=(K/2)(x_a delta_bj-delta_aj x_b).

O numerador métrico é S_ab,c'd'=(G_ac'G_bd'+G_ad'G_bc'-g_ab(X)g_c'd'(Y))/2.
Usamos os perfis já derivados: H/(4kappa)=(1+Kz/4)S/z
+(K/2)delta_ab delta_cd L+W_H+…; ghost=(1+Kz/4)P/z
-(5K/4)delta_mn L+W_G+… . L=log(mu²z). Só a parte singular geométrica
entra nesta execução; os jatos suaves W continuam uma obrigação explícita.

Os dois vértices são os mesmos: T^ab[c^m partial_m h_ab+2h_am partial_b c^m]
e -(nabla^mu barc^nu)[L_v h_munu-g_munu tr(L_v h)/2]. O script realiza
suas contrações por índices, incluindo derivadas X/Y do transporte, sem
inferir a curvatura a partir de uma massa escalar. O termo quartico de
distância geodésica tem primeiro jato Y e misto XY nulos em Y=0 nesta ordem.

**Controle plano e resultado.** Com fator angular A0=1/(8pi²) retirado e
Taylor de exp(-ip·x), a parte plana reproduz exatamente

    R0(p)v=-(3/8)p²(p v^t+v p^t)+(1/2)p p^t(p·v).

A contribuição singular de ordem K dá o perfil angular local

    R_K(p)v=-(10K/3)(p v^t+v p^t)+(5K/3)delta(p·v).

Os coeficientes de L cancelam nesta contração; os dois coeficientes acima
foram ajustados em três polarizações e conferidos nas quarenta polarizações
axiais e numa combinação densa não axial. O traço de R_K é zero.
**Errata ao lado:** a frase automática do primeiro JSON da auditoria dizia
"trace-reversed". O número mostra "traceless": a diferença para
-(10/3)I_tr(K_gauge v) é -(5/3)delta(p·v), não zero. JSONv2 preserva a
correção e o SHA do predecessor; nenhuma conta foi apagada ou repetida.

Ao omitir os jatos transversais dos dois propagadores, o primeiro controle
muda por -17/4. Portanto esses jatos têm contribuição efetiva. Execuções
rc0: 6+946 assertivas, mais2 da errata; CPU 40.875s.
As muitas assertivas de componentes não são provas analíticas independentes.

**Ainda não pago.** Este perfil usa fontes em coordenadas normais e Taylor
ordinário. Sua comparação com um operador covariante em campos externos
exige transportar também os jatos das fontes/densidade; não identificamos
automaticamente R_K com um novo termo covariante de ação. Faltam W, extensão
finita, contatos do cutoff e reunião com os demais vértices da hierarquia.
O resultado não é a quebra Ward completa, nem prova de seu cancelamento.
Sem alteração de um.py, kernel ou gate. A7.b permanece ativa.
