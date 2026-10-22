[DERIVED — operador logarítmico covariante de uma bolha, condicionado aos parametrices; REAL — CAS; OPEN — Q2 completa]
# A7.b — a fonte curva não é anulada separadamente pela Hessiana
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:33:25.015269+00:00.

Modelo087, K constante, primeira ordem K, setor sigma projetado, cálculo
euclidiano auxiliar. Mantidos os vértices069 e o transporte dos propagadores
e da densidade externa já verificados. O coeficiente abaixo é dividido por
A0=1/(8pi²), pela fase Fourier comum e pelos fatores globais da bolha
registrados na normalização relativa. Não é um resultado Lorentziano completo.

**Resultado.** Escreva K_gauge(v)_ab=nabla_a v_b+nabla_b v_a, distinto da
curvatura K. A contribuição logarítmica da bolha marcada, como operador local,
é

    R(v)=3/8 K_gauge(Box v)-1/2 Hess(div v)
           +K[-37/8 K_gauge(v)+2g div(v)]+O(K²)
        =K_gauge(3/8 Box v-1/4 grad(div v)-37K/8 v)
           +2K g div(v)+O(K²).

Em K=0, seu símbolo é exatamente
-(3/8)p²(pv^t+vp^t)+(1/2)pp^t(p·v), o calculado anteriormente.
A novidade é que o termo 2K g div(v) não pertence à parcela de puro gauge
exibida; não foi eliminado por um ajuste de coeficiente.

**Como as derivadas foram transportadas.** O núcleo plano foi mantido como
A_ab,r(x)v^r+B_ab,r^s(x)D_s v^r. Seu resíduo local antes de integrar por
partes contém

    <A x_i x_j x_k>/6 (nabla_(ijk)T^ab)v^r
      +<B^s x_i x_j>/2 (nabla_(ij)T^ab)(nabla_s v^r).

Os colchetes são médias angulares exatas. Adjungir a primeira parcela dá
-nabla_(ijk)v e a segunda +nabla_(ij)nabla_s v. Nenhuma comutação foi
presumida. No ponto normal, gamma^r_jb,i é a derivada da conexão dividida
por K; para v(x)=v exp(ipx),

    (nabla_i nabla_j nabla_k v)^r / i
      =-p_i p_j p_k v^r+K sum_b[
          gamma^r_kb,j p_i v^b+gamma^r_kb,i p_j v^b
          +gamma^r_jb,i p_k v^b-gamma^b_jk,i p_b v^r].

Essa fórmula foi conferida por recursão independente das derivadas
covariantes para todos os256 componentes, com p,v simbólicos. A parte K
explícita dos jatos de fonte, já derivada na entrega anterior, é somada
depois. Ajuste em três polarizações e teste denso não axial dão (-37/8,2)
na base residual K_gauge(v),g div(v). A Hessiana do escalar div(v) comuta
no controle, sem impor comutação às derivadas do vetor.

**Consequência medida.** A identidade clássica H_EH K_gauge=0 já consta
das fontes; não é provada novamente aqui. No normalizado E=4kappa H_EH,
a parte principal aplicada ao resto de primeira curvatura fornece

    E0[2K g div(v)] -> 4K(pp^t-gp²)(p·v),

com a mesma fase Fourier retirada. Para p=v=(1,0,0,0), componente11=-4K.
Assim o cancelamento separado da fonte plana não se estende a esta ordem.
A soma métrica e os demais termos da identidade devem ser calculados com
os mesmos pesos antes de concluir cancelamento ou quebra Ward.

Execuções rc0: 27+273assertivas,CPU1.1875s; logs e fontes
custodiados no manifesto. Componentes de um mesmo tensor não contam como
provas analíticas independentes. Esta é derivação escrita+CAS do resíduo
logarítmico de uma bolha. O contato finito dependente de W já foi separado;
faltam extensões finitas, cutoff variável e soma causal. Não há afirmação
de anomalia quântica completa, mudança de kernel, um.py ou gate.
