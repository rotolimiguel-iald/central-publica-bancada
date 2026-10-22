[KNOWN — Fröb, Teorema7; DERIVED+CAS — extração polarizada; coeficientes físicos OPEN]

Fonte primária conferida: Markus B. Fröb, arXiv:1803.10235v3,
Teorema7, pp.36–37, https://arxiv.org/pdf/1803.10235v3 . A identidade geradora
usa os produtos temporais da mesma família e conserva a quebra clássica
I(F)=s0F+(F,F)/2. Ela não é uma avaliação do coeficiente na TGL.

Para derivar a condição pertinente, escreva A=hbar a+O(hbar²),
a[e^F]=a1(F)+a2(F,F)/2+..., F=u Vx+v Vy, com u,v pares independentes.
O termo aninhado A[A[e^F]⊗e^F] só contribui a partir de hbar².
A extração de hbar*u*v fornece:

 s0 a2(Vx,Vy)+(Vx,a1(Vy))+(Vy,a1(Vx))
 =a1((Vx,Vy))+a2(s0Vx,Vy)+a2(s0Vy,Vx).                    (*)

Na primeira aridade: s0a1(V)=a1(s0V). Para Vx=Vy=V, (*) tem
2(V,a1(V)) à esquerda e2a2(s0V,V) à direita, além de a1((V,V)).
As duas fórmulas têm fatores compatíveis com a expansão exponencial.

Esta separação evita uma troca de objetos na revisão Kimi: W1 da ação
efetiva não é a1, nem a inserção (I,W) é automaticamente o a2(s0V,V)
de produtos temporais. A fórmula de Jacobi auditada antes permanece válida
para seu objeto; (*) é a condição apropriada à família temporal escolhida.

Aplicação à bancada: o defeito das16componentes do SUBTOTAL não é ainda
o lado esquerdo de (*). Para efetuar a comparação, devem estar na mesma
normalização os termos a1 de uma entrada, o composto a1((Vx,Vy)) e as
duas inserções a2(s0Vx,Vy). s0V inclui as correntes de cutoff e o termo
-hdag[G,chi]w já derivado; não se pode impor s0V=0 para chi variável.
Os dois kernels Euler calculados são apenas parte dessas inserções.
O teste de posto2→3 não é, portanto, teste de toda esta identidade.

Não criamos novos operadores físicos nem ajustamos pesos para anular o
resíduo. Esta é a ordem de montagem que deve ser usada pelos leitores.
10 controles algébricos de fatores/omissões, CPU0.03125s,
rc0. Nenhum diagrama adicional foi calculado neste script. Hipóteses globais
e coeficiente total continuam por conferir. Originais/gate intactos.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
