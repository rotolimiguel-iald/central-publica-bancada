[DERIVED — vértices localizados planos e laços fora da diagonal; Q2 OPEN]

## Corrente métrica e sinal

Mantida a ação S_EH=-1/(2kappa) integral chi sqrt(g)R e a identidade
sqrt(g)R=C_GammaGamma+div B, com a corrente previamente construída
B^mu=sqrt(g)(g^ab Gamma^mu_ab-g^mu,a Gamma^b_ab).
A contribuição da corrente na ação localizada é
+1/(2kappa) integral (partial_mu chi)B^mu.

b3 é a polarização cúbica dessa corrente, com o fator Fourier i removido.
Os vértices matriciais existentes armazenam o polinômio Fourier V3raw=16k V3.
Na mesma convenção, o novo vértice é
W_local=chi W_GammaGamma-8 (partial_mu chi)b3^mu.
Para momento total Q das três pernas e momento ell=-Q do cutoff:
-8 ell.b3=+8Q.b3=eh_boundary_vertex_raw. Isso confere o sinal relativo,
não se identifica uma derivada física real com ip sem a convenção dita.

Realização: os jatos internos são (B,partial_0 B,...,partial_3 B).
Se a derivada de b3 atua numa perna interna, preenche blocos 10/01 de W0.
Se atua em h externo, preenche o bloco00 de Wi. Não se acrescenta uma
perna: é a corrente do mesmo vértice. A avaliação matricial reproduz o
vértice completo para40 configurações, incluindo troca das pernas internas.
A identidade de Ward cúbica independente, com Q diferente de0, confere:
V3raw(Gc,U,V)+2 V2raw(L_c U,V)+2 V2raw(U,L_c V)
=2(Q.c)V2raw(U,V). Aqui V2 e V3 são as densidades EH completas.
São166 verificações; trocar o sinal ou omitir a corrente altera controles.

## Localização nas duas extremidades

O novo motor conserva separadamente cinco variantes de cada vértice:
chi vezes o vértice bulk e quatro partial_l chi vezes a corrente.
A adjunção atua também nesses coeficientes. Por isso a integração em X
pede HessX chi, e a integração em Y pode pedir thirdY chi. Descartar os
jatos de ordem superior porque o vértice original só tinha h/Dh é incorreto.
Para os dois tensores externos11 e01, no ponto(1,2,-1,1),97 verificações
conferem a recuperação do caso constante e dos dados GammaGamma anteriores.
Os termos métricos completos e os intermediários estão ambos preservados.

## Ghost: conservar a integração por partes, com sua fronteira

O vértice dirigido existente representa -(partial_mu barc_nu)Z^mu,nu,
com Z a variação de calibre linear em h. A densidade não integrada
barc_nu partial_mu Z^mu,nu, localizada ANTES da integração, obedece
integral chi barc div Z=-integral(chi dbarc+dchi barc)Z.
Portanto a correção é -(dchi)barc Z. Ela é construída substituindo, em
cada coluna derivada de barc do vértice existente, d_mu barc por
(partial_mu chi)barc; a normalização e a orientação dirigida são preservadas.

A comparação de20 configurações com a fórmula explícita de Z confere
o vértice original e o corrigido, sem usar o motor de corrente métrica.
Todos20 controles mudam se a fronteira ghost for omitida. A soma dos laços
usa transposição no segundo vértice ghost e /16 no par métrico, como antes.
São91 verificações nesta etapa. Não é uma escolha implícita de nova
prescrição: as duas densidades, equivalentes a cutoff constante, e a
diferença dchi que as relaciona ficam EXPLÍCITAS. O representante usado
na prescrição causal final terá de conservar essa mesma relação.

## Resultado que distingue bulk, fluxo e anomalia

Para h11,c0, X-Y=(1,2,-1,1), chiX=chiY=1 no ponto:
* Todos os demais jatos nulos: ghost_full-metric_full/2=0.
* dchiY=e0:3960/117649.
* dchiY=e0 e dchiX=e0-e1:57856/117649.
* Somente partial_Y0 partial_Y0 partial_Y1 chiY=1:-12/2401.

O último exemplo mostra concretamente a dependência do terceiro jato.
Os valores intermediários sem fronteira ghost continuam nos arquivos;
não são a soma completa calculada nesta entrega.

Não se exige que o fluxo de uma interação localizada por cutoff variável
se anule. Não chamar esse valor fora da diagonal de anomalia quântica.
A fonte localizada, a variação BRST dos termos de cutoff, as contribuições
de contato da extensão, curvatura e aridades superiores ainda precisam
ser montadas na mesma prescrição. Não foi calculado Q2 completo.
Nenhum original, kernel, definição de horizonte ou gate foi alterado.
