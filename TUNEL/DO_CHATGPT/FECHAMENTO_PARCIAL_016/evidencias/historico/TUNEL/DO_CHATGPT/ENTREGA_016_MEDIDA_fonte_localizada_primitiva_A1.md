[DERIVED+CAS — fonte de consistência localizada da primitiva; Q2 completa OPEN]

A continuação de volume anterior fornece a1=alpha_W div(c),
a2=alpha_W div(c trh)/2 e q0a2+q1a1=0 para o diferencial não localizado.
Agora localizamos a interação: q1_chi h=chi Lie_c h, q1_chi c=chi w,
w=c.nabla c. Para duas funções independentes chi e eta, a regra de produto dá

 q0(chi eta a2)+[q1_chi(eta a1)+q1_eta(chi a1)]/2
 =alpha_W(eta dchi+chi deta).w/2.

Para chi=eta, a fonte é alpha_W chi dchi.w, em geral não nula.
Seu endereço BV é preciso: q_localizado²h=u[Kg,chi]w+O(u²), pois
Kg(chi w)-chi Kg w=[Kg,chi]w. O termo de anticampo da inserção I1=s0Vchi
é -hdag[Kg,chi]w nas coordenadas B. Com B1chi=alpha_W int chi trh/2,
(I1chi,B1chi)=alpha_W int chi dchi.w. O traço do comutador é
tr[Kg,chi]w=2dchi.w. Não se trata de uma nova anomalia por si só: é a
fonte da identidade INHOMOGÊNEA já exigida pela localização.

São 10 verificações exatas, CPU 0.046875s, rc0,
incluindo duas assinaturas, polarização, chi=eta, cutoffs constantes e
integração por partes. Suporte compacto elimina a integral da divergência
total; não elimina as derivadas dos cutoffs que restam. O controle que
descarta essa fonte falha. Nenhum tau foi escolhido para ajustar resíduo.

Este resultado liga a primitiva conhecida de A1 ao setor de anticampos
I1. Ainda não identifica o representante A2(Vchi,Veta) nem soma todos os
termos de consistência de duas entradas. O contato Euler composto e sua
normalização distribucional permanecem o passo seguinte da mesma árvore.
Originais e gate intactos. AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
