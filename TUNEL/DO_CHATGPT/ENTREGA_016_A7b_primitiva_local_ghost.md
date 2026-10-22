[DERIVED — primitiva local do bracket principal; REAL — CAS exato; OPEN — vértice completo e anomalia finita]
# A7.b — a correção local depende também da métrica

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T23:36:43.037428+00:00.

A mudança linear do ghost F(p)v=-3p²v/8+p(p·v)/4 já obtida no h*c
não reproduzia sozinha o triângulo c*cc. Resolvemos o problema local adicional,
sem ajustar o triângulo e sem trocar os vértices que o produziram.
Todos os coeficientes abaixo retiram o fator comum4κA0, A0=1/(8π²), com as
mesmas convenções principais Euclidianas anteriores. Não é novo estado físico.

## Identidade e representante

Defina B(p,v;r,w)=(v·r)w-(w·p)v e
δ_F B=B(Fv,w)+B(v,Fw)-F(p+r)B(v,w).
Existe a seguinte operação local Z(H,k;l,v), linear no tensor simétrico H
e no ghost v, com duas derivadas (momentos k,l):

    Z = v trH[-k²/24+3(k·l)/16-5l²/48]
        -v[3(k·Hl)/8+7(l·Hl)/24]
        +(Hv)[k²/12+(k·l)/4-l²/24]
        +(Hk)(k·v)/12+(Hl)(l·v)/4.

O triângulo medido B1 satisfaz, exatamente,

    B1-δ_F B=Z(K_pv,p;r,w)-Z(K_rw,r;p,v).

K_pv=p⊗v+v⊗p. O sistema racional tem100equações,21coeficientes,
rank13=rank aumentado e8parâmetros livres. Fixá-los em zero escolhe UM
representante; não prova canonicidade/unicidade. Verificamos a identidade em
64polarizações completas (4saídas×4v×4w), com p=a e0,r=b e0+c e1 simbólicos;
covariância O4 e extensão polinomial cobrem os pares de momentos. Um exemplo
de referência independente, já calculado, reproduz7/24. Omitir Z ou inverter
seu sinal falha. Não é uma busca limitada a pontos numéricos.

## O que essa mudança conecta — e o resíduo que fica

Uma candidata à correção do gerador, compatível com a mudança de coordenada
do ghost c_antigo=c+εF(c)-εZ(h,c), é

    R1coord(H,k;l,v)=L_F(l)v H-K_(k+l)Z(H,k;l,v).

Conferimos seus sinais na identidade principal h*cc completa, não apenas
pela interpretação de coordenadas:160componentes polinomiais se anulam.
Também comparamos com o vértice medido R1=G-M/4. O resíduo
S=R1-R1coord NÃO é zero:48componentes na restrição a entradas de gauge
são não nulas. Entretanto, os160pares satisfazem

    S(K_rw,r;p,v)=S(K_pv,p;r,w).

Essa simetria é um requisito para procurar uma primitiva métrica quadrática;
não basta para demonstrar que tal primitiva existe para H arbitrário.
A inversão do sinal de Z quebra34componentes do controle da identidade.
Não afirmamos que a mudança do ghost reproduza a ação ou o vértice inteiro.

As duas execuções terminaram rc0:65+320checagens, controles negativos acima,
CPU 6.578125s e wall
6.595865700044669s. Manifestos preservam fontes, planos,
resultados, logs e o motor puro. Não houve nova chamada remota para calculá-las.

Próximo passo do ramo A7.b: testar a primitiva métrica e as condições finitas
causais/curvas permitidas. O cálculo presente é do coeficiente logarítmico
principal, não A(e^V) finita, não cohomologia removida integralmente.
full_Q2=false; nenhum original/kernel/gate foi alterado.
