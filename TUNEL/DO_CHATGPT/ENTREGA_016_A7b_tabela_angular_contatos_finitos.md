[DERIVED — componente da extensão fixa; REAL — CAS exato; OPEN — soma Ward]
# A7.b — projetores angulares dos contatos finitos
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T06:06:08.793035+00:00.

Mantemos R=FP_a[(1-a)mu^(2a)z^a .]. Para H_l harmônico, m-l par,
b=(m+4-l)/2 e f=H_l(x)z^(-b-l)L^ell, a representação por derivadas
radiais usa os coeficientes v_r da inversão triangular já construída.
Foi calculada a diferença

    R(f)-sum_r v_r H_l(partial)R(z^-b L^r)
      = C c_(m,l,ell) Box^((m-l)/2) H_l(partial)delta.

| m | l | sem log | log | log² |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1/32 | 3/64 | 3/64 |
| 2 | 0 | 0 | 0 | 0 |
| 2 | 2 | -5/576 | -49/3456 | -179/10368 |
| 3 | 1 | 1/576 | 1/432 | 1/648 |
| 3 | 3 | 13/9216 | 271/110592 | 2245/663552 |
| 4 | 0 | 0 | 0 | 0 |
| 4 | 2 | -7/18432 | -121/221184 | -619/1327104 |
| 4 | 4 | -77/460800 | -8419/27648000 | -381653/829440000 |

Os coeficientes foram calculados pelo motor de contatos e conferidos por
resíduos de Taylor em S3 e parte finita Laurent explícita. Os polos dos logs
foram conservados antes da parte finita. Os projetores zonais também foram
conferidos em famílias harmônicas de dois planos, incluindo graus maiores
que m (contato zero, sem apagar o kernel), e em três nós não unitários.
São 184 verificações e 2 controles negativos,
rc0, CPU9.734375s. Não é prova CAS da existência analítica de
distribuições; as identidades de resíduos permanecem entradas declaradas.

O motor puro devolve coeficientes de monômios q^I para contrair com jatos
simétricos covariantes. A ação do delta dá (-1)^m. Não se divide de novo por
I!: os fatores multinomiais já pertencem ao polinômio. Em nós não unitários,
o projetor é homogeneizado com z=x.x; o kernel de grau -m-4, multiplicado
por z² e pelo projetor de grau m em x, tem grau zero.

Este é um componente reutilizável no cálculo dos kernels reais. Não se
identifica a referência harmônica com uma prescrição que preserve BRST,
não se escolhe contratermo e não se declara Q2 inteira. A auditoria remota
MiMo foi preparada ANTES desses resultados e não os recebeu.
