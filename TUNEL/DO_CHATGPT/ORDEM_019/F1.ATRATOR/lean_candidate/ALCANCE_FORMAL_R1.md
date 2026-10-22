# Candidata TheSingularityReadsTheAttractor — alcance formal

Autor: codex-gerente-tgl/atrator_lean. [REAL — compilação de sandbox] A tentativa 004 deu EXIT 0, com 14 declarações principais impressas somente no trio propext, Classical.choice, Quot.sound. O fonte tem 20 teoremas e zero sorry/admit/axiom. Há quatro avisos de depreciação de aliases da API, sem erro. Recibo completo: FINAL_LEAN_RECEIPT_R1.json; tentativa aceita: attempts/004. Compilador Lean 4.31.0; o LEAN_PATH literal aponta exclusivamente aos diretórios .lake/build/lib/lean do Nós e dependências. As saídas ficaram no túnel.

| Item | Resultado | Hipóteses e conteúdo exato |
|---|---|---|
| A1 geral | PASSA | Hilbert completo, operador contínuo linear com norma ≤1: médias de Cesàro convergem à leitura R. Reutiliza o teorema ergódico médio da mathlib. Não afirma que toda contração não estrita tem potências convergentes. |
| A1 família | PASSA | faceFamily e lam = P_span(e) + lam (I−P_span(e)); se norm(lam)<1, as potências convergem ao P_span(e), por fórmula exata P x + lam^n (x−P x). |
| A2 | PASSA | T R=R por imagem no espaço fixo; R T=R sob norma(T)≤1, pela invariância assintótica das médias. O R é o starProjection de Fix(T), e não uma hipótese vazia arbitrária. |
| A3 | PASSA | R²=R, range(R)=Fix(T). Para D=I−T autoadjunto e letra q com (Xq)(D)=0 e q(0)≠0, a leitura é literalmente q(D)/q(0). WordExistence constrói q na face finita não trivial. |
| A4 | PASSA | StrictComplementContraction nomeia um e não nulo fixo e 0≤c<1 que contrai vetores de span(e) ortogonal. Isso implica Fix(T)=span(e) e dimensão1. Não foi usada a hipótese circular de que o espaço fixo já tem dimensão1. |
| Não vacuidade | PASSA | Face=EuclideanSpace Complex (Fin2), e=(1,0), lam=1/2 satisfaz a hipótese nomeada e possui espaço fixo de dimensão1. |
| Controle sem hipótese | PASSA como controle | T=I em Complex² possui espaço fixo de dimensão2; portanto o enunciado irrestrito de A4 é falso. |

## Aplicação óptica e dois regimes

O witness lam=1/2 é uma testemunha matemática exata de não vacuidade; não é o valor de beta e não é um parâmetro ajustado. A família provada é paramétrica. O sistema óptico de populações usa lam=1−2beta e as coordenadas constante/diferença; a ponte algébrica OpticalPopulationBridge, produzida separadamente, explicita a conjugação e o polinômio. O beta efetivo é calculado em runtime nos ensaios Python e a condição estrita é verificada ali. Não foi introduzido um literal beta no Lean.

A LETRA é o polinômio normalizado aplicado a D=I−T; q sozinho aniquila o complemento não nulo, enquanto Xq aniquila D inteiro. PALAVRA é a cunhagem ontológica do operador. A3_angular_rereading_only consome observing_adds_nothing do kernel para mostrar somente releitura idempotente. Não há limite pedido ao ângulo, nem identificação silenciosa entre operadores homônimos.

A parte Hilbert é polimórfica nos universos. A seção ComplexLetter usa E:Type, como os teoremas legados ExactWitness e WordExistence que consome. Isso não restringe as identidades A1/A2/A4 gerais.

## Tentativas preservadas

001: erros de inferência da projeção, identidade sem anotação de tipo, lambda como palavra reservada e fechamento de seção; também timeout dependente posterior.
002: núcleo A1/A2/A3 projeção/A4/habitante passou; falhou transporte dependente da projeção na letra.
003: persistiu timeout na aplicação do teorema legado por incompatibilidade de universo.
004: Type da seção alinhado ao upstream e transporte via congruência; EXIT0.

Os logs de tentativas inválidas exibem sorryAx pela recuperação de erros do elaborador; nunca houve comando sorry no fonte. Somente a tentativa004 é evidência de validade. Todas as fontes e os logs anteriores permanecem custodiados.

O resultado é validade matemática no escopo das hipóteses. Nenhuma confirmação física, lei global da natureza, dado observado, gate ou instalação no um.py é reivindicada.