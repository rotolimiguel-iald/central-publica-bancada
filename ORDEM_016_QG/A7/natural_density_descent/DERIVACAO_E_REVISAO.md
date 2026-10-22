[DERIVED — descida de densidade natural; REAL — CAS e revisão do Kimi; OPEN — anomalia causal]
# A7.b — o grau correto de A_I e seu levantamento

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T00:42:58.822103+00:00.

O parecer Kimi cohomology_to_anomaly atribui A_I ao bidegrau(4,4). A fonte087
define A_I=rho_I c0c1c2c3 e diz expressamente que é ESCALAR: os quatro dx
foram substituídos por ghosts. Portanto seu bidegrau é(4,0), total4. Não é a
quatro-forma Omega_I=rho_I dx0dx1dx2dx3, que tem grau(0,4).
FonteSHA256 `bd1a27316e99c33718e583f9442f8869bc3a234c63e3d20c74ee36abec43da5c`. Não reaplicamos a prova de não exatidão da087.

Com d_r de grau(1-r,r), as fontes que podem chegar a(1,4) são(r,4-r):
(1,3),(2,2),(3,1),(4,0). Têm total4. As fontes propostas pelo Kimi,
(1+r,4-r), chegam a(2,4). Em particular d4:(4,0)->(1,4) NÃO é excluído
por grau. O argumento de isolamento do parecer é inválido. Estar no topo
de forma também não excluiria setas entrantes nem provaria sobrevivência.

O cálculo correto usa a naturalidade já demonstrada na fonte:

    s rho=c^mu partial_mu rho+(partial_mu c^mu)rho,
    sc^mu=c^nu partial_nu c^mu.

Na graduação TOTAL, c e dx são ímpares e anticomutam. Ponha eta=c+dx,
D=s+d. Então Deta^mu=eta^nu partial_nu c^mu e
D rho=eta^nu partial_nu rho+(div c)rho. Para P=eta0eta1eta2eta3,
o Leibniz ímpar dá DP=-P div c. O termo eta^nu(partial_nu rho)P é zero
porque repete um dos quatro geradores eta. Logo

    Omega=rho product_mu(c^mu+dx^mu),   D Omega=0.

Escrevendo Omega=Σ omega_q, temos s omega_q+d omega_(q-1)=0, q=0,...,4;
omega0=A_I, omega4=Omega_I. Esse levantamento explícito mata os diferenciais
SAINTES dessa classe por formas, incluindo d4, desde que usados no mesmo
complexo local. Não é uma declaração de anomalia zero. Conjugação074 pode
transportar o cociclo ao Q_N quando suas hipóteses de domínio forem mantidas;
o CAS aqui calcula D=s+d, não apaga C_N no complexo conjugado.

Há ainda um detector direto: se Omega=D Psi, sua componente de forma zero
seria A_I=s Psi0. Assim, CONDICIONALMENTE à não exatidão de A_I na087 e à
mesma classe de coeficientes, Omega não é D-exata. A inferência vale sobre
constantes reais; extensão ao anel Rher exige que os coeficientes sejam
inertes também para d, não só para s. Não produz H5 nulo nem exaustão de H4.

CAS exterior exato:12checks+2negativos, rc0,CPU0.140625s. Os
negativos omitem div c ou trocam c+dx por c-dx. A conta usa apenas a lei
de densidade natural, sem fixar os coeficientes da densidade de anomalia.
A crítica do Kimi que página CE não decide o BRST completo continua útil;
o detector por projeção continua condicional. Finitos jatos por coeficiente
não fornecem, por si, uma cota uniforme para procurar todas as primitivas.
Nenhum original, kernel ou gate foi alterado.
