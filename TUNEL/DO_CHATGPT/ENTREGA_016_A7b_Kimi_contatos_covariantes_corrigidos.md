[REAL — auditoria exata da resposta; DERIVED — diferencial corrigido; OPEN — Q2 completa]
# A7.b — contatos covariantes: revisão recebida e correções locais
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T05:36:53.995373+00:00.

Kimi jobb9d7e1a5-06fd-4f6d-8ed8-e82084aff2e8, execução
b71c38c7-e6fa-4938-bd0f-b8d7436f5c3f, respostaSHA256
`4840b8bea1a25b9e01673279d13799280f1b96d66d543d1f400f1e40a40b66ef`. Recebimento pela API oficial, sem nova
execução. Uso:318099entrada,67007saída,309760cache,385106total.
Custo monetário desconhecido, não zero. Sua resposta fica preservada
e DECLARADO; a fórmula-mestre não foi aceita como escrita.

## Correções que decidem a divergência
1. **Fator2 e ordem dos ghosts (§2/§5).** Com u,c ímpares, E par,
B simétrico paralelo e J^lambda=u B c^lambda E, a identidade certa é

    E B(c.nabla u)+u B(c.nabla E)
       =2u B[c.nabla E+(div c)E/2]-div J.

Kimi escreveu metade do lado direito. O teste exterior fixou
E=5,dE=7,B=1: na base[du*c,u*c,u*dc], a diferença é[-5/2,7/2,0].
O contato integrado é +(A0/2)(nabla chi)J na ordem u*c.
Reescrevê-lo como +(A0/2)c*u*BE troca seu sinal. A fonte anterior
antifield_quadratic_primitive já tinha a identidade correta; foi
reutilizada, não substituída por uma votação entre modelos.

2. **Objeto D1 (§0/§3).** A fonte usa somente a derivada do ghost:

    D1(j)E_ab=(1/4)[(j_a^r-j^r_a)E_rb
                           +(j_b^r-j^r_b)E_ra],  j_a^r=nabla_a c^r.

É antissimétrico entre as fibras e anula a métrica. A expressão da
resposta passou a derivar também u, portanto mudou o operador.
Contraexemplo: c=e0 constante e E11=x1 dão D1=0, enquanto o D
redefinido dá componente01=-1/4. A covariantização correta não cria
esse termo. Por Leibniz graduada e antissimetria,

    s0[-A0 u D1(j)u/6]=-A0 u D1(j)E/3.

Nessa escrita não há derivada em u na parcelaD1; portanto não é
necessária uma integração por partes que invente um contatochi nela.

3. **Curvatura (§4).** Mantida a mesma conexão normal da bancada,

    [nabla_mu,nabla_nu]T_ab
     =K(g_a_mu T_nu_b-g_a_nu T_mu_b
                   +g_b_mu T_a_nu-g_b_nu T_a_mu),
    [nabla^rho,nabla_mu]h_rho_nu=4K h_mu_nu-Kg_mu_nu trh.

C1 da resposta concorda com a conexão; C2/C3 têm o sinal oposto.
O CAS encontrou168 componentesC2 e28 componentesC3 que rejeitam
esses sinais. Teste sobre dez fibras completas, sem ajustar ao
resultado desejado. As reordenaçõesIII/IV da resposta precisam do
mesmo sinal corrigido; sua soma anunciada6Kh não é transportada.

4. **Realidade (§6).** Coeficientes reais não resolvem a involução BV.
Reutilizada a auditoria bv_reality: na convenção fixada u é antirreal,
c é real, star reverte produtos, F é ímpar antirreal e sF é real.
Esse resultado já existia antes da revisão; sua presença foi
conferida. A realidade do gerador não linear completo continua fora
do alcance dessa verificação. Não se acrescentou fator i.

## Diferencial local corrigido, sem nova escolha de prescrição
Com s0u=E, s0c=s0E=0, cutoff inerte e os fatores A0 da fonte:

    s0F_extra = A0 integral chi u B[c.nabla E+(div c)E/2]
               -A0/3 integral chi u D1(nabla c)E
               +A0/2 integral (nabla_lambda chi)J^lambda
               -A0/2 boundary integral chi J.n.

E é o operador físico, sem eliminar b na definição inicial:

    E=-Box Itr h+2Kh+Kg trh-2C*Ch,
    u=4kappa(h*+C*barc).

O termoC*Ch e os antighosts do deslocamento permanecem. A substituição
do termo algébricoE_K separa explicitamente

    B(E_K)=-K h/3-2K g trh/3,
    D1(j)E_K=2K D1(j)h.

Os outros termosK gerados ao reordenar as três derivadas são
determinados pelos comutadores corrigidos acima. Não se confunde a
parcela algébricaE_K com toda a curvatura do operador reordenado.

5081 verificações, CPU0.765625s, rc0.
Isso corrige o lado da PRIMITIVA a comparar aos laços. Não calcula
novo coeficiente de anomalia finita, não escolhe contratermo e não
fecha Q2 inteira. Nenhum original, kernel ou gate alterado.
