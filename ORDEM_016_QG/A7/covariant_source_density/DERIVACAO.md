[DERIVED — transporte da fonte externa; REAL — CAS; OPEN — operador covariante completo]
# A7.b — o transporte dos propagadores não dispensa o da fonte
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:26:43.195328+00:00.

O relatório anterior fixou T^ab como densidade contravariante em coordenadas.
Se t^ab representa o tensor fonte no referencial transportado a partir de Y,

    T(X)=sqrt(g(X)) P(X,Y) t(X) P(X,Y)^t,
    P(x,0)=I+(K/6)(Iz-xx^t),   sqrt(g)=1-Kz/2+…,
    T=t-(K/6)[z t+xx^t t+t xx^t]+… .

Essa parcela deve multiplicar o núcleo plano antes da leitura covariante.
Sua ordem em x é2: contribui ao termo de Taylor de ordem1 na parcela v
e de ordem0 na parcela Dv. Não é correção arbitrária dos coeficientes.

Na base 2(v^t t p), tr(t)(p·v), a contribuição geométrica com fonte
coordinate fixa era (-10/3,5/3). Depois de incluir a densidade e o
transporte dos índices da fonte, o perfil passa a **(-23/12,13/12)**.
Ambos os resultados são preservados com a respectiva convenção; não se
deve transportar a propriedade "sem traço" do perfil antigo ao novo.

As colocações das derivadas permanecem separadas:

| termo | coeficiente de 2(vtp) | coeficiente de tr(t)(pv) |
|---|---:|---:|
| Taylor de primeira ordem da fonte, parcela v |13/12|19/12|
| primeiro jato do ghost externo, parcela Dv |-3|-1/2|
| soma do perfil de momentos |-23/12|13/12|

Em posição, a parte explicitamente proporcional a K fornece

    K[-13/6 (nabla_b t^ab)v_a -19/12(nabla_a trt)v^a
       -6 t^ab nabla_a v_b -1/2 trt nabla_a v^a].

Sob integração por partes de primeira ordem e suporte compacto, vira
K[-23/6 t^ab nabla_a v_b+13/12 trt divv]. Isso ainda NÃO identifica
todo o operador covariante: a parte principal contém jatos simétricos
de terceira ordem da fonte e de segunda ordem junto a Dv. Ao transportar
essas derivadas, os comutadores geram termos de curvatura adicionais.
Apagá-los por conservação de momento antes dessa operação seria circular.

CAS: três polarizações de ajuste, compatibilidade da terceira linha,
polarização densa não axial (resultado -33), identidade da densidade
transportada;rc0,CPU36.21875s. A fórmula dos jatos geométricos
usa os controles independentes da entrega anterior. Não é repetição de laço.

Escopo: contribuição singular, duas inserções, primeira ordem K, interior
de cutoff constante. A parte suave não muda esse resíduo, mas seus contatos
finitos foram mantidos na entrega irmã. Ainda faltam a ordenação covariante
completa, a prescrição finita e a soma causal. A7.b ativa; originais/gate intactos.
