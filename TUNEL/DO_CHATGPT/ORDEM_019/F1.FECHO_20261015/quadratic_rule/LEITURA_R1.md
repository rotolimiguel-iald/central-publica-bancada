# Regra quadrática — F1.FECHO_20261015

[REAL — compilado] `RuleQuadraticResidual.lean`: 18 declarações com axiomas somente
propext, Classical.choice e Quot.sound; EXIT 0; nenhum sorry/admit/axioma novo.
Reivindicação delegada 845, codex-gerente-tgl. A aceitação independente cabe à gerência.

## Forma e reaproveitamento

`residual A X := TGLExt.purityR (Eg X - A)`, em M2. `purityR` é a soma dos módulos
quadrados das entradas, isto é, Frobenius², não a norma matricial padrão implícita.
Reutiliza PageInformation.purityR e purityR_eq, Bicommutant.frob_self_eq_zero_iff,
RuleTruthContract.Admissible, TimeGravitonMatrix.Eg e TimeGravitonFlow.reading_flow.
Não refaz a rede, a leitura ou o fluxo. A consulta da unidade nova ao Nós Vivo devolveu
"unidade não está no grafo"; foram abertas diretamente as fontes já levantadas.

## Resultados

- PASSA: residual A X ≥ 0; residual A X = 0 sse Eg X = A, a regra já tipada.
- PASSA: residual A (T_t X) = residual A X, para o mesmo alvo A; continuidade e derivada zero.
- PASSA: numa inscrição fixa A, seu próprio resíduo é zero; entre inscrições, zero sse igualdade.
- PASSA: se Eg A ≠ A, o alvo é impossível e o resíduo é estritamente positivo para todo X.
- PASSA: o alvo A=I/2 é fixo e aceita transportedRho, embora a densidade bruta seja diferente de A.
- PASSA: a mesma transportedRho tem residual P+ = 1/2, e continua rejeitada em todo tempo.
- PASSA: inhabited_and_discriminating exibe os testemunhos anteriores simultaneamente.

## Hipóteses e alcance

As identidades de resíduo valem para parâmetros reais arbitrários do fluxo algébrico;
o setor de canal físico usa taxa e tempo não negativos, como no contrato já construído.
O alvo é argumento fixado antes da avaliação, não é redefinido como Eg(X) para cada entrada.
A invariância não é hipótese: decorre de reading_flow. Ela não mede a aproximação do
estado bruto ao alvo, e não é um escore decrescente de progresso nem um relógio.
O alvo realizável pode ser carregado como `RuleContinuousMotor.Inscription Eg`.
O caso de alvo impossível não é universalmente vazio: Eg(rootPlus)=0 e rootPlus≠0
já estão provados na base reutilizada; não se afirma que esse rootPlus seja densidade.
Esta pedra prova o contrato no M2 especificado, sem declarar extensão global 4D,
confirmação natural, instalação no original, escrita de memória ou mudança de gate.

## Reprodução

O recibo de build contém comando, início/fim UTC, duração, toolchain e LEAN_PATH literal.
Cada execução de build_quadratic.py cria snapshot, logs e .olean novos numa pasta própria.
As bibliotecas já copiadas de formal_verified e os packages canônicos são somente lidos.
O fonte de entrega é byte a byte o snapshot compilado. Não houve tentativa falha nesta entrega.
