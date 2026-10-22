**ORDEM_016 / A-7.b — resultado DECLARADO, não auditado localmente.**  
Não executei código nem li arquivos locais. Refaço a álgebra a partir dos trechos/scripts fornecidos. O alcance é: contato misto plano de 2ª ordem, linha suave constante, referência definida por derivação, com `C_E` e prefatores comuns removidos. Não é prova de cancelamento diagramático completo, nem admissibilidade da QME, nem seleção de estado/horizonte.

## 1. Convenções usadas

Sejam \(p\in\mathbb R^4\), \(p^2=p\cdot p\), \(s=p\cdot v\), \(I=\delta\), e \(h\) simétrico. Escrevo a aplicação de quatro coeficientes invariantes como

\[
N_{a,b,c,d}(h)=
a\,p^2h
+b\,p^2\operatorname{tr}(h)I
+c\bigl(pp^T\operatorname{tr}h+I\,p^T h p\bigr)
+\frac d2\bigl(pp^T h+hpp^T\bigr).
\]

O gerador de gauge/ghost do recorte é

\[
G(v)=p v^T+v p^T.
\]

A ação de Einstein linearizada usada no script é

\[
E(h)=-p^2h+p^2\operatorname{tr}(h)I+pp^Th+hpp^T-\operatorname{tr}(h)pp^T-I\,p^Thp,
\]

isto é, na notação acima,

\[
E=N_{-1,1,-1,2},\qquad EG=0.
\]

Para cada setor métrico,

\[
L^{(I/T)}(h)=l_a h+l_b I\operatorname{tr}h,
\]

com

\[
(l_a,l_b)_{I}=(-1/2,-1/8),\qquad
(l_a,l_b)_{T}=(-1/2,+1/4).
\]

A linha suave é \(W_I\) ou \(W_T\); a linha de contato é \(J\). O fator métrico efetivo no script é \(-1/32=(-1/2)(1/16)\), e o ghost tem fator \(+1\) com transposição do vértice da segunda ponta. O emparelhamento da delta põe \(q=-p\): no script, `A1` usa \(+p_i\), `B1` usa \(-p_i\).

## 2. Checagem independente de um componente métrico \(I\) e um \(T\)

Uso a identidade geral

\[
N(G(v)) =
\left(a+\frac d2\right)p^2G(v)
+2(b+c)p^2s\,I
+(2c+d)s\,pp^T.
\tag{1}
\]

Além disso, como \(EG=0\) e

\[
E(sI)=2p^2s\,I-2s\,pp^T,
\]

temos

\[
E L G = E(l_aG+2l_b sI)
=4l_b p^2s\,I-4l_b s\,pp^T.
\tag{2}
\]

Logo, na base

\[
\bigl[\,I\,p^2s,\quad p^2G(v),\quad pp^T s\,\bigr],
\]

o resíduo

\[
N_{\rm bubble}G+E L G
\]

tem coeficientes

\[
\bigl(2(b+c)+4l_b,\; a+d/2,\; 2c+d-4l_b\bigr).
\]

### Setor \(I\)

\[
(a,b,c,d)_I=(23/8,-13/16,1,-2),\qquad l_b=-1/8.
\]

Então

\[
2(b+c)+4l_b
=2(-13/16+1)+4(-1/8)
=-\frac18,
\]

\[
a+d/2=23/8-1=15/8,
\]

\[
2c+d-4l_b=2-2+4/8=1/2.
\]

Portanto

\[
\boxed{W_I:\quad (-1/8,\;15/8,\;1/2)}
\]

na base \([I p^2s,\;p^2G(v),\;pp^Ts]\). Confere com a nota.

### Setor \(T\)

\[
(a,b,c,d)_T=(3/4,-3/8,1/2,-1),\qquad l_b=1/4.
\]

\[
2(b+c)+4l_b
=2(-3/8+1/2)+1
=1/4+1=5/4,
\]

\[
a+d/2=3/4-1/2=1/4,
\]

\[
2c+d-4l_b=1-1-1=-1.
\]

Logo

\[
\boxed{W_T:\quad (5/4,\;1/4,\;-1)}.
\]

Também confere.

## 3. Tabela \(N_{\rm bubble}G+E L G\) e \(N_{\rm eff}\)

A primitiva é

\[
N_{\rm eff}=N_{\rm bubble}+E L+L E.
\]

Calculando \(EL+LE\), com \(L(h)=l_a h+l_b I\operatorname{tr}h\), obtém-se a correção

\[
\Delta(a,b,c,d)=
\bigl(-2l_a,\;2l_a+4l_b,\;-2l_a-2l_b,\;4l_a\bigr).
\tag{3}
\]

Assim:

| setor | \(N_{\rm bubble}\) | \((l_a,l_b)\) | \(N_{\rm bubble}G+E L G\) | \(N_{\rm eff}\) |
|---|---:|---:|---:|---:|
| \(W_I\) | \((23/8,-13/16,1,-2)\) | \((-1/2,-1/8)\) | \((-1/8,15/8,1/2)\) | \((31/8,-37/16,9/4,-4)\) |
| \(W_T\) | \((3/4,-3/8,1/2,-1)\) | \((-1/2,1/4)\) | \((5/4,1/4,-1)\) | \((7/4,-3/8,1,-3)\) |
| \(W_G\) | \((0,0,0,0)\) | — | \((0,0,0,0)\) | \((0,0,0,0)\) |

A propriedade fundamental é

\[
N_{\rm eff}G
=N_{\rm bubble}G+E L G+L E G
=N_{\rm bubble}G+E R_W,
\]

pois \(EG=0\) e \(R_W=L G\). Portanto a primitiva reproduz exatamente o resíduo medido na direção \(G\); o termo \(LE\) não muda \(N G\), mas é necessário para a adjunção.

## 4. Núcleo dos quatro coeficientes em \(N G\)

Por (1), a aplicação

\[
(a,b,c,d)\longmapsto N_{a,b,c,d}G
\]

tem coeficientes

\[
K_1=2(b+c),\qquad K_2=a+d/2,\qquad K_3=2c+d
\]

na base \([I p^2s,\;p^2G(v),\;pp^Ts]\). O núcleo é dado por

\[
b=-c,\qquad a=-d/2,\qquad d=-2c.
\]

Logo

\[
(a,b,c,d)=c(1,-1,1,-2).
\]

Mas

\[
E=N_{-1,1,-1,2},
\]

de modo que o núcleo é exatamente

\[
\boxed{\ker\bigl(N\mapsto NG\bigr)=\operatorname{span}\{E\}}
\]

na classe dos quatro invariantes \(p^2\operatorname{tr}AB\), \(p^2\operatorname{tr}A\operatorname{tr}B\), \((pAp)\operatorname{tr}B+(pBp)\operatorname{tr}A\), \(pABp\). Portanto, **dentro dessa classe**, a ambiguidade exibida \(\eta E\) é toda a ambiguidade de \(NG\). Fora dessa classe, há outros operadores que podem anular \(G\); a nota não os cobre.

## 5. Transposição, multiplicidade e o erro por omitir \(LE\)

Em fibra simétrica, se \(a<b\), a entrada fora da diagonal aparece duas vezes. O script da primitiva evita erro de multiplicidade construindo a base com

\[
v[a,b]=v[b,a]=1
\]

para \(a<b\), e testando

\[
\operatorname{tr}\bigl(v\,N(w)-N(v)\,w\bigr)=0.
\]

Isso está correto para matrizes simétricas completas. Se se usar apenas o triângulo superior com peso unitário, é preciso multiplicar os termos fora da diagonal por \(2\) no produto interno; caso contrário o teste de adjunção fica errado.

Se omitirmos \(LE\), definindo

\[
N'=N_{\rm bubble}+E L,
\]

então

\[
N'G=N_{\rm eff}G,
\]

porque \(LEG=0\). O erro não aparece no resíduo de Ward. Ele aparece na adjunção:

\[
N'-N'^\dagger
=E L-L E
=-2l_b\bigl(\operatorname{tr}(h)pp^T-I\,p^Thp\bigr).
\tag{4}
\]

Exemplo concreto: tome \(h=I\), \(p=(1,0,0,0)\). Para \(W_I\), \(l_b=-1/8\), logo

\[
N'-N'^\dagger
=\frac14(4pp^T-I)
=\operatorname{diag}(3/4,-1/4,-1/4,-1/4)\neq 0.
\]

Para \(W_T\), \(l_b=1/4\),

\[
N'-N'^\dagger
=-\frac12(4pp^T-I)
=\operatorname{diag}(-3/2,1/2,1/2,1/2)\neq 0.
\]

Portanto omitir \(LE\) passa num teste de Ward mas falha no teste de adjunção. O teste relevante é a adjunção, como o operador observou.

## 6. Ghost-1, ghost0 e anomalia ghost1

O setor ghost neste recorte tem \(W_G=\delta_{ab}\) e coeficientes medidos

\[
(0,0,0,0).
\]

O ghost usa fator \(+1\) e transposição do vértice da segunda ponta. Se alguém confundir:

- **gerador de ghost-1** com \(L_W\);
- **variação de ação ghost0** com fonte ghost-1;
- **anomalia ghost1** com um coeficiente local de contato;

introduz uma linha ghost não nula que não existe no cálculo medido. O erro é detectável exatamente pela tabela ghost \((0,0,0,0)\): qualquer coeficiente ghost diferente de zero, ou qualquer falha em cancelar o bloco ghost após a transposição, indica mistura de setores. A anomalia ghost1 é um objeto cohomológico/BRST separado; não é o mesmo que a variação de ação ghost0, nem substitui \(L_W\) no contato misto.

## 7. Sinais de integração por partes e \(q=-p\)

No script, a segunda ponta usa `-p_i`. Isso não é escolha opcional: é a codificação de \(q=-p\) no emparelhamento da delta. Se se usar \(+p\) na segunda ponta, a bilinear métrica, que é bilinear nos dois vértices derivados, troca de sinal globalmente; a linha \(W_I\), por exemplo, deixaria de ser \((23/8,-13/16,1,-2)\) e apareceria com sinal oposto. Portanto o \(q=-p\) é testável já na tabela de coeficientes. Também não se deve substituir \(\partial\) por \(ip\) “sem avisar”: neste recorte \(p\) é símbolo de derivada real. A troca de sinal em integração por partes é absorvida por \(q=-p\); omiti-la altera os termos lineares em \(p\) e quebra o ajuste sobredeterminado.

## 8. Resposta à pergunta única

**Dentro dos trechos fornecidos e das convenções anexas**, os coeficientes e a primitiva seguem algebraicamente, sem ajuste escondido visível:

- as tabelas \(W_I,W_T,W_G\) e os resíduos \(N_{\rm bubble}G+E L G\) se reproduzem;
- \(N_{\rm eff}=N_{\rm bubble}+E L+L E\) reproduz \(N_{\rm eff}G=N_{\rm bubble}G+E R_W\);
- o núcleo de \(N\mapsto NG\) na classe de quatro invariantes é exatamente \(\operatorname{span}\{E\}\);
- omitir \(LE\) é invisível a \(NG\), mas detectável por adjunção;
- o setor ghost deve permanecer zero, e a transposição ghost é parte da convenção;
- \(q=-p\) e o fator métrico \(-1/32=(-1/2)(1/16)\) são consistentes com o script.

**Lacuna declarada:** não é possível refazer a contração diretamente “desde os vértices brutos” com os trechos carregados, porque não estão presentes os módulos importados que definem `vertex_data`, `sandwich`, `lincomb`, `transpose`, `position_metric_bubble_engine`, `ghost_direct_position_engine`, etc. O resultado permanece **DECLARADO** até auditoria local com esses arquivos e com os `results.json` correspondentes.

**Alcance exato:** isto estabelece uma primitiva local de 2ª ordem de contato misto plano, com linha suave constante, relativa à referência definida por derivação, não uma prova de cancelamento diagramático completo, não uma prova de admissibilidade física de toda primitiva, não uma seleção de estado físico, não uma continuação lorentziana e não um fechamento da QME.