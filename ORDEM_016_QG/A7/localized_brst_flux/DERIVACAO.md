[DERIVED — corrente clássica cúbica fora da casca; Q2 completo OPEN]

## A corrente completa não é apenas c L2

Para a densidade métrica EH completa, sua transformação difeomórfica é
s L=div(c L). Na ordem cúbica, s0 L3+s1 L2=div(c L2).
Ao trocar s1 L2 por sua forma de Euler-Lagrange, deve-se conservar
s1 L2=<E2,L_c h>+div Theta2(L_c h).
Logo a corrente relevante ao setor h²c com a inserção de equação de
movimento é J_BV=c L2-Theta2(L_c h). Ela não é somente c L2.
A ligação com a fonte BV usa a mesma convenção s0 hdagger=Eh já
registrada; esta entrega calcula a identidade métrica correspondente,
não todo o colchete BV localizado de todos os campos.

## Construção explícita do representante de Green

Mantidas as normalizações V2raw=8kappa V2 e V3raw=16kappa V3 e os
fatores Fourier retirados como nos motores anteriores.
Se A porta momento p e B porta q, ponha Q=p+q e
 D(Q)=V2raw(A,Q-q,B,q)-V2raw(A,-q,B,q).
D é polinômio de grau no máximo2 em Q e D(0)=0. Escreva
 D(Q)=Q.L+Q.M.Q, M simétrica. Os coeficientes são recuperados exatamente:
 L_i=(D(e_i)-D(-e_i))/2,
 M_ii=(D(e_i)+D(-e_i))/2,
 M_ij=(D(e_i+e_j)-D(e_i)-D(e_j))/2, i diferente de j.
Então J_green=L+M Q satisfaz Q.J_green=D para qualquer Q.
O termo V2raw(A,-q,B,q) contém somente o símbolo da equação de movimento
da perna B. O outro termo conserva a densidade e seu momento total.
O grau dois é explícito na densidade quadrática EH, não inferido de um
ajuste numérico. Este representante de corrente admite melhorias de
divergência nula; não se afirma unicidade física do representante.

Para as pernas U(p), V(q) e c(k), Q=p+q+k, define-se
 J=2c V2raw(U,p,V,q)
   -2J_green(L_c U,p+k,V,q)-2J_green(L_c V,q+k,U,p).
A identidade de Ward da densidade completa, já conferida no vértice,
implica a identidade exata:
 V3raw(Gc,k,U,p,V,q)
 +2V2raw(L_c U,-q,V,q)+2V2raw(L_c V,-p,U,p)=Q.J.
Os fatores2 decorrem da relação das normalizações brutas quadrática e
cúbica. Não se emprega a Hessiana com gauge em lugar de E2.

O cutoff externo fornece ell=-Q. Assim Q.J=-ell.J é a contribuição
localizada de fronteira, na mesma convenção Fourier, em vez de zero.
Com Q=0 recupera-se a identidade integrada. A relação precisa valer
ANTES de estender produtos singulares, para identificar o termo clássico
que deve ser comparado com sua imagem pelos produtos temporais.

## Verificação e controle negativo

502 verificações exatas: dois controles da corrente quadrática por par
na base simétrica10x10, identidade cúbica fora da casca, identidade com
momento do cutoff e limite Q=0, mais dois controles não vazios.
CPU2.953125s; rc0. Em98 de100 pares o fluxo é não nulo. Em99 de100,
substituir J por 2c V2raw dá resultado diferente.
Exemplo U=V=e00, p=(1,2,-1,1),q=(2,-1,0,3),k=(0,1,1,0),
c=(2,-1,1,3): Q=(3,2,0,4), J=(176,-152,120,-40).
Q.J=64=V3raw+2Euler. Não se converte64 em0 por escolha de extensão.

## Setor ghost e multiplicador: identidade graduada a preservar

O original da fonte BV já descreve +barc C(L_c h). Escrevendo C como
divergência e Z para seu argumento, a localização anterior foi explícita:
 I_gh=integral chi barc div Z
     =-integral [chi dbarc+(dchi)barc] Z.
Com s chi=0, s barc=b, s b=0 e s ímpar, a regra graduada dá
 s I_gh=integral chi [b div Z-barc div(sZ)]
       =-integral chi [(db)Z-(dbarc)sZ]
        -integral(dchi)[b Z-barc sZ].
O sinal menos em s(barc Z)=bZ-barc sZ é obrigatório.
É uma identidade algébrica escrita; não foi feita nesta entrega uma
contagem CAS adicional para ela. Não descartar b por ter sido eliminado
em propagadores internos. Se a fixação de gauge vem de s Psi_chi e o
BRST completo é nilpotente, sua variação total é s²Psi_chi=0; o ghost
isolado não fornece esse cancelamento. A condição de nilpotência e o
restante do setor são hipóteses a verificar na montagem, não um novo
resultado quântico deste cálculo.

## O que falta para Q2

A corrente calculada é clássica, cúbica e plana. Não identifica por si só
os produtos temporais com a primitiva local, não calcula os contatos
quânticos nem prova sua exatidão no BRST interagente. Localizar somente
as interações mantendo S0 sem cutoff também exige distinguir essa ação
de multiplicar a ação inteira por chi; o master equation completo não
pode ser deduzido só de s L=div(c L).
Próximo: inserir a corrente identificada no comparador da prescrição e
calcular as extensões dos kernels completos de fonte e laços. Curvatura,
aridades e a condição causal permanecem obrigações. Gate inalterado.
