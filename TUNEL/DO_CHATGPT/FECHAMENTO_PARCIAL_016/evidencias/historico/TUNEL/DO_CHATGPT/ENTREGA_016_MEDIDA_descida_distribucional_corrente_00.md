[DERIVED — identidade distribucional medida na componente00; Q2 integral OPEN]

A diferença de consistência anteriormente medida na componente00 é reproduzida
exatamente pela descida da corrente de campo já construída. Foram mantidos os
cinco blocos e seus pesos: Ymetric/2, Ymixed, Yghost, Xmetric, Xmixed. Não se
escolheu tau, nem se ajustou coeficiente, nem se acrescentou grafo por analogia.

Se P_C é o núcleo da corrente estendida e F_C seu núcleo fora da diagonal,
escreva P_C=R(F_C)+A_C, onde A_C é o contato local já calculado. Variar o h
externo produz -(d_i+lambda_i)P_C. Com C_i(F)=R(d_iF)-d_iR(F), resulta

 -(d_i+lambda_i)R(F)=R(-(d_i+lambda_i)F)+C_i(F).

A parcela C_i(F) não está contida simplesmente na variação de A_C. É o
contato da derivada EXTERNA com a extensão. O coeficiente simétrico h_(i0)
entra uma vez quando i!=0 e duas quando i=0. Para cada orientação dos cutoffs
calculamos a soma correspondente, conservando x simbólico, não só um ponto.

Para lambda=(1,-1,0,0),eta=(1,0,0,0) e a ordem trocada, a parte bilocal
antissimetrizada da componente00 é identicamente ZERO como função racional
de x, com z=x.x. A descida é portanto local nesta componente. A multiplicação
do cutoff em X e a passagem ao operador local dão q->q-lambda e depois
q->D+lambda+eta, isto é, q->D+eta no contato adicional.

Somando a variação do contato antigo à nova parcela e aplicando a adjunção
ponderada D->-D-L, obteve-se exatamente o polinômio inteiro de grau5 antes
medido para a componente00 do defeito de h,c. Diferença: ZERO.
Controle em D=0: ambos -9259/1920, diferença0, nas unidades CE=-4pi².
Isto explica essa diferença como termo da identidade INHOMOGÊNEA; não diz
que o representante isolado virou cociclo homogêneo nem que a anomalia acabou.
A identificação geral com J2, outras componentes/cutoffs e o modelo curvo
continuam sob seus escopos; nenhuma classe de cohomologia foi promovida.

ERRATA PRESERVADA: v1 leu parts.Ymetric como se ainda faltasse o fator1/2.
O produtor full_current_contact_matrix.py já o aplicava. A leitura local v1
estava errada, embora os oito núcleos racionais e os contatos externos estivessem
corretos. V2 soma parts diretamente, verifica a soma contra polynomial e reutiliza
os oito núcleos, sem repetir loops. O predecessor e seu hash constam da V2.

Comandos: runtime SymPy A4, -X utf8 -B, scripts
current_distributional_descendant_probe.py e ..._v2.py. Ambos rc0 observados
nas ferramentas;18controles na V2;CPU conjunta111.359375s. Não houve captura
independente de stdout em arquivo; resultados estruturados/checkpoints e hashes
estão preservados. O rc0 da v1 não aprova sua leitura de peso corrigida.

Ampliação registrada, ainda NÃO concluída: current_distributional_descendant_matrix.py,
session19789, processo próprio observado ativo. Calcula40componentes h/c nas duas
orientações e as16componentes de dois ghosts, reutilizando8núcleos. Não reiniciar
por demora; consultar o mesmo handle e depois seus resultados. Não presumir
que as16entradas repetirão a identidade00. Orquestração externa prossegue separada.
Originais/kernel/gate intactos. Abertura sha256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
