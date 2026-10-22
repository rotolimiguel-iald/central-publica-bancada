# R79 — da entrada coerente às quadraturas calculadas

[DERIVED — analítico, NOT_LEAN] Em nome de codex-gerente-tgl, 18/10/2026. F1.FECHO_20261015, claim967/escopo983. Reuso R66 (colisões/entrada coerente), R64 (portos exteriores), R74 (quadro/LO) e R78 (primeira variação). Não é calibração empírica do aparelho.

## 1. Hipótese instrumental e identidade algébrica

Nomeamos H_COHERENT_PORT1: a perturbação óptica entra no porto1 da MESMA realização de colisões R66, L1=sqrt(kappa_i)*a_i; porto2=Lout=sqrt(kappa_o)*a_o, sem entrada coerente. A mistura direta dos banhos é a identidade (nenhum termo de passagem direta 1→2). Mantêm-se os outros três banhos, inclusive a entrada coerente OH no canal3 que produz Omega, e o salto J INTEIRO no canal5. Estado inicial do sistema é independente da sonda, como em R78. Essa realização é um INPUT nomeado, não consequência de um GKLS isolado nem uma identificação da matriz S_beta com a matriz de mistura de banhos.

Reaproveitando a expansão R66, agora com vetor de amplitudes alpha_j nas cinco ancillas, b_delta=(|0>+sqrt(delta) sum_j alpha_j|j>)/sqrt(1+delta sum_j|alpha_j|²):

    K0=I+delta[-ih0-(1/2)sum Lj†Lj-sum alpha_j Lj†-(1/2)sum|alpha_j|² I]+O(delta²)
    Kj=sqrt(delta)(Lj+alpha_j I)+O(delta^(3/2)).

No canal reduzido, sum|alpha|² rho cancela; o termo linear é [sum(alpha_j*Lj-alpha_jLj†),rho]. O drive é portanto

    h_drive=i sum_j(alpha_j*Lj-alpha_jLj†),  h=H/hbar.

Não há dissipadores cruzados criados entre portos nem remoção de D[J]. A generalização é uma expansão de matrizes finitas; o estado coerente temporal e a ordem do limite de colisões conservam as ressalvas R66. Para o porto1 e alpha=r+i*s:

    h_in=i sqrt(kappa_i)(alpha* a_i-alpha a_i†)
        =sqrt(2*kappa_i)[s X_i-r P_i],
    X_i=(a_i+a_i†)/sqrt2, P_i=(a_i-a_i†)/(i sqrt2).

Essa identidade vale também em cortes: não requer [a,a†]=I. Na R78,

    h_probe=g_in sqrt(kappa_i)[x X_i+y P_i].

Logo, para kappa_i>0 e g_in>0:

    x=sqrt2*Im(alpha)/g_in,
    y=-sqrt2*Re(alpha)/g_in,
    u=x+i*y=-i sqrt2*alpha/g_in.                     (1)

Trocar o sinal da fase em (1) troca o drive: não é uma equivalência sem transformar a entrada. A mesma conta mantém a bomba OH alpha_3=i*Omega/sqrt(gamma_OH) da R66. Se kappa_i=0, o porto não acopla e esta identificação de drive pelo porto perde sentido; não se divide por zero.

## 2. Saída e coeficientes de campo

No porto2 sem entrada coerente e sem mistura direta, a média exterior é alpha_out=<Lout>. Na convenção R78,

    z=(Q_X+i Q_P)/sqrt2=g_out*<Lout>.

As duas médias de quadratura podem vir de aquisições distintas com o mesmo preparo; não se afirma medição conjunta sem ruído de quadraturas incompatíveis. Para a perturbação constante complexa alpha, combinando (1) com a resposta real-linear já calculada,

    delta alpha_out = H_plus*alpha + H_minus*conj(alpha),
    H_plus = -i sqrt2*h_plus/(g_in*g_out),
    H_minus= +i sqrt2*h_minus/(g_in*g_out).           (2)

Aqui H_plus/H_minus são derivadas transitórias a amplitude constante do porto, com o mesmo preparo em todos os tempos. Não são uma transformada de Fourier em frequência nem a matriz de espalhamento de todos os portos/polarizações. Para envelope variável, a mesma transformação aplica-se ponto a ponto ao núcleo causal de Duhamel; não se substitui uma integral por ganho instantâneo.

(2) resolve a convenção deixada aberta na R78 PARA H_COHERENT_PORT1. Um H_minus não nulo significa, nesse modelo e nesse preparo, que a resposta marginal não é multiplicação complexa por um único escalar. Fases unitárias consistentes dos portos não removem seu módulo. Isto não refuta a lei da patente: é preciso demonstrar que ela se refere exatamente a este preparo, realização instrumental e observável. A primeira variação de média tampouco caracteriza um canal quântico inteiro ou sua capacidade de transmitir informação.

## 3. Unidades e calibração que se pode cancelar

Para t=t0*u, t0>0:

    kappa_dimensionless=t0*kappa_SI,
    L_dimensionless=sqrt(t0)*L_SI,
    alpha_dimensionless=sqrt(t0)*alpha_SI,
    alpha_out_dimensionless=sqrt(t0)*alpha_out_SI.

Alpha_SI tem unidade s^(-1/2); |alpha_SI|² é fluxo de fótons na realização coerente. O quociente/derivada d alpha_out/d alpha cancela sqrt(t0), desde que TODOS os parâmetros e o instante sejam transportados com o mesmo t0. Assim os coeficientes (2) são adimensionais e não precisam de uma escolha arbitrária de relógio para existir. A resposta em segundos continua exigindo t0 e as taxas do sistema; cancelamento de unidade não determina essas taxas.

Se um modo quase monocromático de frequência omega_L e potência P_mode estiver identificado, P_mode=hbar*omega_L*|alpha_SI|². Conversão de potência incidente total em P_mode exige fração acoplada eta_mode; amplitude sqrt(eta_mode*P_total/(hbar*omega_L))*exp(i phi), fase/eficiência especificadas. Não substituir omega_L pela frequência OH sem correspondência modal demonstrada. Esse é um contrato de fluxo energético de modo, não uma medição nem derivação de eta_mode. A frequência de fase, tempo de relaxação e potência limiar são objetos distintos.

## 4. Alcance e ordem das verificações

A conversão é derivada da realização existente, sem ajustar parâmetros à resposta. R78 continua a execução original no corte3. Reexpressar seus números pela transformação (2) é pós-processamento, não experimento novo. Refinar o corte exige a cota da primeira variação com inserção de a/a†; a cota R75 da bomba OH limitada não basta por nome. A R79 separa esse cálculo de planejamento e a única execução adicional em corte selecionado pela cota, antes do resultado refinado.

Ficam abertos a identificação material de H_COHERENT_PORT1 e da superfície OH, taxas e ganho do receptor real, e a realização causal completa R5. Nem a decomposição (2) nem uma identidade formal de porta implicam ganho, imunidade a ruído, transmissão instantânea ou confirmação física. Nenhum original, produção ou gate é alterado.

