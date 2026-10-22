[DERIVED — operador logarítmico na primeira curvatura; REAL — CAS; OPEN — soma causal]
# A7.b — adjunto, operador covariante e resíduo medido
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T04:27:50.333290+00:00.

O perfil radial anterior deixou uma derivada na perna externa B ancorada.
Sua transferência por partes não é substituição de momento em espaço curvo:
troca sym(nabla^4) por nabla_j sym(nabla^3). A diferença atua na fibra
tensorial e nos índices de derivada. Foi calculada, sem impor Ward=0.

**Jatos.** Para h=e A e^t exp(ipx), e=I-K(zI-xx)/6, os jatos covariantes
totalmente simétricos de ordem2/4 não têm termoK. O jato com uma derivada
externa a sym(nabla^3) tem termoK não nulo. Verificação4551checks,
1620 jatos externos não nulos; calibração escalar Box² exp(ipx)|K=2Kp².

**Adjunto da bolha.** Os dois setores que contêm gradB dão

    -1/6 T2 [nabla_j sym(nabla^3)-sym(nabla^4)]A
    -1/2 T1 [nabla_j sym(nabla^3)-sym(nabla^4)]A,

com T2/T1 as contrações angulares dos vértices de duas/uma derivadas
internas na ponta X. Derivadas na ponta Y foram transferidas só aqui.
Na base ordenada [p²trAB,p²trA trB,pAp trB,pBp trA,pABp], resulta

    delta = [83/9,-25/6,28/9,145/18,-134/9].

Somando ao perfil derivativo anterior, os coeficientes mistos tornam-se
iguais a269/9. Isso foi consequência da conta, não condição de ajuste.
Auditoria independente por contração inteira:100 pares, três momentos
fora do eixo e calibrações,106checks. Excluir o adjunto volta a quebrar
a igualdade. Os primeiros cinco casos serviram só para extrair a tabela.

**Mesmo símbolo para todos os setores.** Agora usamos a quantização por
derivadas covariantes completamente simetrizadas. Sob essa convenção,
o símbolo em quadro radial identifica os coeficientes locais. A parte
principal de ordem4 continua sendo a tabela plana já paga. Na ordemKp²,
incluindo potencial, peso-1/2 da bolha e tadpole:

    métrica: ['1/3', '35/18', '1/18', '1/18', '-17/9']
    ghost:   ['41/36', '-7/3', '26/9', '26/9', '-35/6']
    soma:    ['53/36', '-7/18', '53/18', '53/18', '-139/18'].

Todos divididos por hbar*A0, A0=1/(8pi²), com K retirado. O ghost foi
avaliado de seu operador com derivadas ordenadas, não da variação do calor
livre. Há100 pares e três controles não axiais nessa conversão (106checks).
Coeficientes iguais nas posições3/4 significam compatibilidade com o
adjunto neste recorte; não são uma identidade Ward por si só.

**O teste de Ward NÃO zerou.** Com G(v)=nabla v+(nabla v)^t e a fase i
retirada, a aplicação do operador montado fornece

    (H_loop G)_K = K[-(1/2)p²(pv^t+vp^t)
                         -2pp^t(p.v)+(3/2)g p²(p.v)].

A fonte previamente calculada fornece (E R)_K=4K(pp^t-gp²)(p.v).
Portanto a combinação com sinal mais tem coeficientes[-1/2,2,-5/2]
na base[p²G,pp(p.v),gp²(p.v)]. O sinal oposto também não zera;
para p=e0,v=e1 a fonte é zero e(H_loop G)01=-K/2 nos dois casos.

O avaliador passa a Ward CLÁSSICA E G=0 em256 componentes e a Ward
plana do operador de laço. Jatos ímpares e probes:960checks; teste
adicional do resíduo em15 polarizações e da família local:252checks.
O resíduo é real no cálculo executado; ainda não está identificado como
a anomalia causal completa da prescrição. Falta reconciliar os contatos,
ordens superiores e normalizações das diferentes representações.

**Família algébrica localizada, não adotada:** neste setor homogêneo,
um acréscimo à Hessiana de ordemK com coeficientes

    (d1,d2,d3,d4)=(1/2-t/2,9/4+t/2,-1-t/2,t)

cancelaria a combinação local indicada. Isso localiza uma liberdade
de contratermos na ordem testada; não escolhe t, não autoriza modificar
a prescrição, não demonstra Wess-Zumino/BRST completo nem QME finita.
É necessário verificar a extensão na hierarquia causal antes de usar
essa família. Nenhum coeficiente da conta foi trocado para obter zero.

Execuções deste pacote rc0; 6231 checks, CPU169.359375s. A parteK²,
os termos finitos dependentes de estado/cutoff e Q2 completa permanecem
abertos. Gate, um.py e kernel intactos. Resultados não enviados aos
revisores independentes em espera.
