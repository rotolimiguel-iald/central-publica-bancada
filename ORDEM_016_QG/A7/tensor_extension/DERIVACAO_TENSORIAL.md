[DERIVED — extensão de um par; REAL — álgebra exata; OPEN — prescrição completa e quebra Ward]
# A7.b — extensão tensorial e contatos entre normalizações

Abertura sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

## Prescrição anterior ao CAS e correção ao lado

Na convenção +---, z=x²−i0 e C=4iπ², usa-se □(1/z)=Cδ da derivação
primitiva. Para kernels de UM PAR de pontos, fixou-se antes desta conta:

    R(u) = FP_(a=0) [(1−a) μ_R^(2a) z^a u].

O mesmo regulador a é usado para todos os kernels relacionados por multiplicação
polinomial. μ_R>0 permanece escala de referência simbólica, não ajustada após
Ward. A continuação meromorfa é o insumo distribucional: o CAS não a constrói.
Assim R(pu)=pR(u) para polinômios p, por linearidade da extração de Laurent.
Isso conserva contrações, mas NÃO implica R(∂u)=∂R(u).

A família diferencial anterior D_n era uma extensão válida de cada potência
separadamente. Ainda não era uma prescrição conjunta multiplicativa, como já
advertia seu relatório. Agora R_2=D_2 conserva exatamente a normalização
primitiva, mas potências superiores recebem contatos finitos determinados.

Se U_n(a)=μ_R^(2a)z^(−n+a), r_n=−1/[4^(n−1)(n−1)!(n−2)!], então

    Res U_n = C r_n □^(n−2)δ,
    D_n = r_n □^(n−1)[log(μ_R²z)/z],
    FP U_n = D_n + (H_(n−1)+H_(n−2)) Res U_n,
    R_n = D_n + (H_(n−1)+H_(n−2)−1) Res U_n.

Aqui H_j é número harmônico; não é Hamiltoniano. Os coeficientes vêm da expansão
de 1/∏_(j=2)^n [4(j−1−a)(j−2−a)]. Exemplo concreto:

    R_3 = D_3 − (3C/64)□δ,
    z D_3 = D_2 + (3C/8)δ,     z R_3 = R_2.

Usou-se z□^mδ=4m(m+1)□^(m−1)δ em quatro dimensões. Para n>=3,

    □R_(n−1) = 4(n−1)(n−2)R_n − 4(2n−3)Res U_n.

Isso exibe o contato que seria perdido ao exigir simultaneamente a recorrência
diferencial sem contatos e multiplicação polinomial sem contatos.

## Tensor de posto dois: o traço verifica a normalização

Para x_μ x_ν/z³, diferenciar z^(−1+a) ANTES de tomar a parte finita fornece

    T_μν(a) = ∂_μ∂_ν[μ_R^(2a)z^(−1+a)]/[4(a−1)(a−2)]
              − η_μν U_2(a)/[2(a−2)].

Aplicando o mesmo fator (1−a), resulta

    R_μν = (1/8)∂_μ∂_ν(1/z) + (1/4)η_μν R_2 − (C/32)η_μν δ.

A contração dá η^μν R_μν=R_2. Sem o último termo, o traço teria o erro
Cδ/8. Equivalentemente,

    ∂_μ∂_ν(1/z) = 8R_μν − 2η_μν R_2 + (C/4)η_μνδ.

Esse contato é de normalização distribucional. NÃO é, sozinho, a anomalia
BRST. Para derivadas, a identidade geral é

    ∂_μ R(u) − R(∂_μu)
      = 2 FP [a(1−a) μ_R^(2a)z^a (x_μ/z)u].

Se a família entre colchetes sem a(1−a) tem coeficientes c_−2/a²+c_−1/a+…,
o resultado é 2(c_−1−c_−2). Usar só 2Res omite o polo duplo dos termos
logarítmicos. Não se presume derivação sem anomalia de normalização.

## Evidência e próximo uso

Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/tensor_extension_check.py`.
rc0 observado na sessão de execução33481; 41 identidades e
8 controles negativos, Sympy 1.14.0.
wall 111.3302405999857s; CPU 108.484375s. Saída estruturada preservada;
nenhum stdout independente. Verificados n=2,…,7 e o tensor acima. Alguns checks
avaliam consequências algébricas de identidades distribucionais assumidas;
não substituem uma prova dessas identidades. Revisão adversarial será externa.

Escopo: kernels homogêneos principais, um par, espaço tangente plano.
Não há extensão de todas as diagonais de grafos, curvatura completa, ajuste de
T10/T11, soma métrica+ghosts+antifields, nem coeficiente de quebra Ward calculado.
O dado permite construir uma tabela de contatos coerente para essa soma.
Não move o item interagente da QG, não altera kernel, um.py ou gate.
