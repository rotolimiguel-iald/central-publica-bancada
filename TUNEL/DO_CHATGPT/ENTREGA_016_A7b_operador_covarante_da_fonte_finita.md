[DERIVED — operador finito da fonte; REAL — duas rotas CAS; OPEN — soma causal]
# A7.b — fonte finita covariante, com ordem das derivadas preservada
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T06:28:40.454028+00:00.

Os contatos harmônicos dos kernels planos A(T,v;x) e B(T,Dv;x) foram
transportados para o ghost: A dá +D_(ijk)v; B dá +D_(ij)D_k v.
Esses sinais vêm da ação das derivadas do delta sobre T seguida do adjunto;
não são os sinais dos momentos logarítmicos de Taylor. As fases Fourier
foram verificadas explicitamente. À contribuição plana covariantizada
somou-se o contato K já medido com transporte da densidade externa.

Resultado, retirado C e os fatores globais já separados nas entregas:

    DeltaR/C = -7/48 G(Boxv)+13/96 Hess(divv)+g Box(divv)/32
             +K[65/288 G(v)-29/144 g divv]
             = G[-7/48 Boxv+13/192 grad(divv)+65K/288 v]
               +g[Box(divv)/32-29K divv/144].

G(v)=nabla v+(nabla v)^t. Não é só gauge: escrevendo
phi=Box(divv)/32-29K divv/144, a ação da Hessiana física E é

    E(DeltaR/C)=-2Hess(phi)+2g Box(phi)+6K g phi.

Foi usado E G=0 no MESMO fundo Einstein, e a identidade foi também
conferida diretamente com jatos polinomiais reais e a implementação de E,
sem substituir a Hessiana física pela gauge-fixada.

**Auditoria por outra rota:** os contatos planos foram reconstruídos por
momentos de S3, sem a inversão harmônica do primeiro cálculo:

    N_A=13/288 <A(n)(n.q)^3>-q²<A(n)(n.q)>/64,
    N_B=-5/48 <B(n)(n.q)^2>+5q²<B(n)>/192.

Para as dez fibras simétricas, p e v permaneceram simbólicos. Os coeficientes
planos e curvos coincidiram. A identidade dos jatos ordenados foi reutilizada
somente após conferir igualdade estrutural com o código antes auditado.
Outra verificação aplicou E em dois campos polinomiais, 16 componentes e
ordensK0,K1,K2. Há controles explicitamente não nulos.

Cálculos rc0: 12+116 verificações, CPU
1.71875+1.46875s. O termo K² dessa imagem é a ação
de E sobre o operador fonte obtido; não é uma nova amplitude fonte K²
calculada separadamente. Os jatos suaves W não foram declarados zero.
Nenhuma conclusão sobre a anomalia completa decorre só desta decomposição.

Tentativas preservadas: v1 falhou por parêntese excedente; v2 pela passagem
de polinômio zero a um jato de grau3; v3 corrige esse caso vazio, sem mudar
os coeficientes. Auditor v1 também tinha um parêntese excedente, corrigido
em v2. Logs e fontes de todas as tentativas foram mantidos no manifesto.
