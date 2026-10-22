[DERIVED — convenções e fonte plana; REAL — CAS exato; OPEN — Ward causal completo]
# A7.b — fase de Fourier e orientação da fonte
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T07:34:11.146853+00:00.


Para Fourier exp(-ip.x), o coeficiente racional do motor meromórfico multiplica
C_E*(-i)^m. Para exp(+ip.x), multiplica C_E*i^m. A frase i^m no motor não
pode ser usada sem dizer qual das duas convenções está sendo aplicada.

Derivação: a integral de Schwinger para H_l(x)z^(-(m+l+4)/2+a) dá
(-i)^l*pi²*2^(-m+2a)*Gamma(a-k)/Gamma(N-a)*H_l(p)*(p²)^(k-a),
k=(m-l)/2, N=(m+l+4)/2. A fase (-1)^k da Gamma combina para (-i)^m.
O regulador (1-a) e as derivadas dos logs são mantidos antes da parte finita.

Controle independente: R(d_j U_n)-d_j R(U_n) coincide com o contato local
já calculado para n=2,3,4, todos os eixos. Trinta verificações passaram.
Doze controles negativos com a fase oposta deixam um erro proporcional a
FourierLog, portanto não corrigível apenas por um contato local.

No PAR, a perna móvel usa exp(+ipx). Se m=nx+ny-2r, n=1+[xi>=0]+[yj>=0]
e P_j tem grau j, a fase é i^(m-j)*i^(n-2o+j)/i=(-1)^order.
Com os sinais da integração por partes e potenciais, reproduz o motor em
134 combinações. Nenhuma alteração dos números do par foi necessária.

Na FONTE plana, o teste em X usa exp(-ipX) e o ghost exp(+ipY).
O termo A tem fase +i; o termo B, com a derivada explícita do ghost, -i.
A integração angular independente reproduziu os contatos + referência
diferencial existentes: 18 controles, incluindo o caso não axial. Em
T=e11,p=v=e0, a imagem Einstein da fonte é -3/32, com log zero.
No caso não axial registrado ela é -63/16, também com log zero.

Esses resultados conferem a orientação plana e os sinais do par. Não
autorizam substituir E covariante por E(p) na fonte curva. A execução
completa do par de primeiraK ainda está no mesmo processo93180.
