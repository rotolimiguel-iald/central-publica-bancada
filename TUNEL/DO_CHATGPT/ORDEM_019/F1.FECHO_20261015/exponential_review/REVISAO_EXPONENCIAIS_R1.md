# Revisão independente dos vetores exponenciais e da totalidade

[REAL] PASSA no escopo matemático das duas fontes aceitas. Nenhum achado material.

| Fonte | EXIT | Segundos | Impressões de axiomas | .olean idêntico |
|---|---:|---:|---:|---|
| ExponentialVectorsR3.lean | 0 | 112.245637 | 5 | True |
| ExponentialTotalityR4.lean | 0 | 98.463293 | 8 | True |

As 13 impressões usam apenas propext, Classical.choice e Quot.sound; zero sorry. Logs incluem comando, toolchain Lean 4.31.0, LEAN_PATH literal, início, fim, segundos e exit. Dependências pinadas conferidas antes/depois; totalidade usa a base recompilada independentemente.

- **normalization — PASSA:** O setor n usa x tensor n dividido por sqrt(n!), incluindo setor zero = 1. O quadrado da norma é ||x||^(2n)/n!, sem perda ou duplicação de fatoriais.
- **membership_inner — PASSA:** Memℓp com p=2 deriva da somabilidade da série exponencial. A identidade inner(e(x),e(y))=exp(inner(x,y)) deriva das componentes e lp.hasSum_inner; a conjugação do fator real está consumida.
- **totality — PASSA:** A hipótese temporária de ortogonalidade a todos e(x) implica uma série escalar identicamente zero para e(z*x). A unicidade analítica anula cada coeficiente; positividade dos pesos permite removê-los. O núcleo fechado do funcional inner(v_n,·) contém o span e seu fecho, logo v_n=0. O complemento ortogonal trivial prova totalidade. Não há hipótese de totalidade na conclusão nem substituição de F.
- **second_quantization — PASSA:** Gamma(u)e(x)=e(ux) segue setor a setor das ações unitárias existentes. GammaJ(j,hj)e(x)=e(jx) usa a ação antilinear existente, j antiunitária involutiva e o fato de os pesos serem reais; não afirma que toda antiunitária seja involutiva.
- **nonvacuity — PASSA:** exponential_zero identifica e(0) com o vacuum existente, cuja norma é 1. A família e o Fock são objetos concretos do tipo canônico, não campos postulados de um contrato.

## Alcance

- Revisão independente das duas fontes aceitas e recompilação uma vez de cada; a totalidade importa a base recompilada pelo revisor.
- Os vetores exponenciais são não normalizados: ||e(x)||²=exp(||x||²). A normalização adicional de estados coerentes não é parte desta tarefa.
- Deriva totalidade no Fock de setores fechados gerados por potências diagonais já construído; não reabre a equivalência desse modelo com outras apresentações do Fock.
- Não é revisão independente do lema GramTotalExtensionR4, que foi construído por este agente e é revisto pelo pai.
- Não verifica nesta entrega a construção de Weyl, relações CCR, KMS, BW, certificado físico ou confirmação experimental.
- Não foram alterados originais, memória, produção, kernel do Nós ou gate. Ato AUDITADA/FECHADA permanece da gerência.

Hashes, linhas, fontes e recibos completos: REVISAO_EXPONENCIAIS_R1.json.
