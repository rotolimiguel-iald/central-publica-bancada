[DERIVED — resíduo ghost integrado condicionado; REAL — CAS exato; OPEN — Q2 causal]
# A7.b — contribuição ghost curva quadrática em todos os componentes
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T03:05:26.267576+00:00.

**Objeto.** Q(h)=C_g L_c(g+h), com g FIXO no espaço-forma4D, Ric=3K g.
Somente h varia. Do operador reduzido Qtilde=(I+h)^-1Q e do resíduo de calor
da entrega anterior, mantidas suas hipóteses analíticas, foi calculado o
termo quadrático inteiro. Não se diferenciou o calor livre on-shell.
Notação: t=trh, u_nu=nabla^mu h_mu,nu, d=divu; todos os produtos usam g.

**Resultado integrado, módulo divergências:**

    a4_2[h] = (box h)^2/24+7(box t)^2/96-d(box t)/8
              -(nabla u)^2/24+d²/12
            +K[7(nabla h)^2/12-17(nabla t)^2/12
                +(7/2)u·nabla t-(79/24)u²]
            +(13K²/6)(4h²-t²).

O fator angular e a ponderação do determinante seguem a convenção da bolha
anterior. A polarização bilinear plana reproduz exatamente os cinco
coeficientes [1/12,7/48,-1/8,-1/12,1/6], sem ajuste de normalização.

Uma forma ordenada de sua Hessiana, com G(v)_ab=nabla_a v_b+nabla_b v_a,
é (a integração usa volume de fundo, não uma segunda densidade variável):

    Hghost(h) = box²h/12+(7/48)g box²t
      -(Hess(box t)+g box d)/8-G(box u)/24+Hess(d)/6
      +K[-7box h/6+(17/6)g box t
          -(7/2)(Hess t+g d)+(79/24)G(u)]
      +(13K²/3)(4h-g t).

Essa fórmula é o segundo diferencial da densidade integrada acima; box u
é o laplaciano covariante de vetor/covetor. Não se permutam suas derivadas
como escalares. A forma integrada, e não uma extensão temporal finita,
é o objeto demonstrado pela redução algébrica desta entrega.

**Como foi obtido.** A expressão-mãe é
tr{5K[-hB-A_mu A^mu/4]+(B-boxh)^2/8+F²/48+Omega0[A,A]/24}.
Cada termo foi convertido em palavras ordenadas de derivadas covariantes.
O adjunto inverte a palavra e acrescenta (-1)^n; a contração de fibras
continua explícita. O operador não reduzido tem3080 termos; o representante
de quatro derivadas tem1060. A diferença a primeira ordem emK fixa os quatro
coeficientes de gradiente; a ordemK² fixa os dois coeficientes sem derivadas.

Os jatos foram calculados em coordenadas normais, sem projetar fora
comutadores. Para a ordemK há dois algoritmos: inserção única de Gamma
diferenciada e recorrência direta da derivada de cada slot tensorial.
Para K² usa-se a conexão cúbica extraída independentemente da métrica exata:

    g=I-(K/3)(zI-xx^t)+(2K²/45)(z²I-zxx^t)+…,
    Gamma2^a_bc= -z(x_b delta_ac+x_c delta_ab)/45
                 -(2z/15)x_a delta_bc+(8/45)x_a x_b x_c.

Conferidos64 componentes em cada ordem da conexão,2560 jatos de quarta
derivada por dois algoritmos, os55 pares bilineares da base simétrica em
cada ordem e um controle denso não axial. Covariância O(4) e homogeneidade
estendem o teste completo axial: o operador local de ordem4 tem somente
as ordens p⁴,Kp²,K². Essas verificações dão a identidade diferencial
algébrica no espaço-forma, condicionada à expressão-mãe de calor.

**Controles.** No canal h=f g, a redução devolve
integral[7(box f)²/8-19K(df)²/2], medido antes independentemente; o potencial
K² se anula para h=f g constante covariante. Descartar os comutadores muda
o primeiro controleK por -34/9. Apagar o potencialK² muda por104/3.
2913 checks de componentes,2 negativos,rc0,CPU 4.25s.
Os coeficientes foram explorados antes desta verificação, registrado no plano;
não se apresenta esse ajuste como análise cega nem como2913 provas distintas.

**Alcance.** As condições ainda são as da redução de calor: classificação
local do resíduo, ciclicidade do resíduo de símbolos sob o fator multiplicativo,
h formalmente pequeno, suporte compacto ou divergências mantidas à parte.
Não é igualdade de determinantes FINITOS. Com cutoff variável há contatos
a restaurar. Não inclui a Hessiana métrica, tadpoles métricos, fontes BV nem
a soma de ghost1/Q2. A continuação causal completa permanece aberta.
Nenhuma alteração de um.py, kernel, gate ou originais. Próximo cálculo:
vértices cúbico/quártico métricos de curvatura e sua combinação com a fonte.
