[DERIVED — vértice e log local; REAL — CAS exato; OPEN — bolha métrica curva e Q2]
# A7.b — vértice quártico derivativo e tadpole métrico
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T03:36:18.944282+00:00.

**Escopo:** mesmo fundo fixo g, Ric=3K g, Lambda=3K, expansão G=g+h,
ação -(2kappa)^-1 integral sqrt(G)(R(G)-2Lambda), C_g linear. A seção
euclidiana auxilia o coeficiente UV local; não escolhe um estado físico.

**Vértice.** A parte Gamma-Gamma tem duas pernas derivadas e dois campos
sem derivada. Para matrizes A,B não necessariamente comutantes, escreva
W=sqrt(det(I+h))(I+h)^-1, G,T os numeradores de Gamma de primeira ordem.
O segundo diferencial do integrando é

    D²[W (M^-1 G)(M^-1 T)](A,B), M=I+h.

Usam-se D_A M^-1=-A, D²_AB M^-1=AB+BA,
D_A sqrt(det M)=trA/2 e
D²_AB sqrt(det M)=trA trB/4-trAB/2. Somam-se as6 escolhas de pernas sem
derivadas e as2 ordens das pernas derivadas. O código retorna32kappa V4;
não se divide novamente por4!. Integração por partes: módulo divergências,
com cutoff constante. Os contatos de cutoff seguem separados.

Controles:24 permutações Bose; família conforme G=(1+f)g;
V4(Kc,A,B,C)+soma V3(Lc A,B,C)=0; e, com duas pernas g de momento zero,

    32kappa V4(A,p;B,-p;g,0;g,0)=8*(8kappa V2_EH(A,p;B,-p)).

**Jatos do propagador.** Em quadro ortonormal por transporte radial,
D=-(nabla²+E), E=-2K P_TL+6K P_tr, Omega é a curvatura em S²T*.
A conexão foi extraída da métrica e do coframe, não substituída por massas:

    A_i=(K/2-K²r²/24)(x^a delta_ib-delta_ia x_b)+O(K³r5).

Seu divergente covariante e x·A anulam-se nas ordens usadas.
Com u0=1+Kr²/4+19K²r4/480, a recorrência radial fornece

    U1=E+2K I+r²(KE/4+29K² I/60)
       +(1/12)x^i x^j soma_k Omega_ik Omega_jk+… .

O segundo termo de calor diagonal é
a2=E²/2+2KE+29K²I/15+Omega²/12. Aqui a2 multiplica t² (a4 na
convenção por dimensão). A derivada covariante ordenada inclui
Omega_ij(E+2K)/2. Pela identidade de Synge e pela derivada mista do
exponencial de calor, o log de D^-1 tem jato misto A0 L_ij, onde
A0=1/(8pi²) para ln Lambda e

    L_ij=delta_ij(-2P_TL/3+12P_tr)K²
          -(1/12)soma_k{Omega_ik,Omega_jk}.

No caso métrico Omega(E+2K)=0. Soma_i L_ii=E(E+2K), conferida;
no caso escalar a fórmula dá delta_ij E(E+2K)/4. O jato sem derivada
é a1=8K P_tr e o jato com uma derivada é zero na referência invariante.
O propagador físico auxiliar preserva GH=4kappa D^-1 I_tr. Na base
simétrica de10 componentes, sua contração inclui a inversa da matriz de
Gram: S0=I_tr Gram^-1. Esquecer esse fator muda os termos fora da diagonal.

**Tadpole da Hessiana efetiva.** O peso é +(1/2)Tr(GH delta²H), logo
(1/2)*4kappa/(32kappa)=1/16. Para pernas externas A,B,p,-p, resulta

    T_AB/(hbar A0)=K[-2p²trAB+2p²trA trB
       -2(pAp trB+pBp trA)+4pABp]+12K²trAB.

O primeiro bloco tem as duas derivadas externas; o segundo tem as duas
internas. O termo com uma derivada interna é zero nessa referência;
o quartico do potencial já dera zero. Portanto o tadpole log total nesse
recorte está calculado; não se afirma que tadpoles finitos ou com W suave
se anulem. Para A=B=g e momento externo zero, o resultado é48K² hbar A0.

**Verificação:** vértice 98 checks, jatos 126,
tadpole 59, todos rc0. CPU respectivamente0.140625s,
0.453125s,2.734375s. Os55 pares bilineares conferem
os2 invariantes de ordemK²; há controle denso e3 contrações independentes
por extração do polinômio de momento do vértice completo. A primeira
implementação dos jatos falhou por KeyError ao consultar xx[j,i] antes
de preenchê-lo; v1 e log preservados, v2 corrige apenas a ordem da tabela.

**Próximo elo:** contribuições restantes da bolha métrica com correções
dos propagadores e transporte, depois soma com ghost e fonte BV.
Prescrição causal finita, cutoff e Q2 completa permanecem abertos.
Nenhum um.py, kernel, gate ou fonte canônica foi alterado.
