[DERIVED — 17 declarações Lean auditadas; A-2.5.c parcialmente construído]

# A-2.5.c — domínio, resolvente e transformada limitada

UTC: 2026-09-24T14:25:26.647373+00:00. ABERTURA sha256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

## Resultado efetivo

Para A,B limitados auto-adjuntos, A injetivo, AB=BA e A²+B²=I,
o operador parcial já existente D=boundedGraphOperator(A,B) satisfaz:
dom(D)=ran(A), D(Ax)=Bx, ker(D)=ker(B), incluindo o domínio no núcleo ambiente.
Provados ||Ax||²+||Bx||²=||x||² e ||Bx||≤||x||.
Se γ≥0 é limite inferior de D no complemento do núcleo, então
γ/sqrt(1+γ²) é limite inferior de B no mesmo complemento.
Não se afirma que o limite inferior seja atingido, nem que exista gap positivo.

Quando A≥0, os lemas existentes de quadrado de LinearPMap dão, com domínio sucessivo:
R=A²=(I+D²)^(-1) e A=sqrt(R). Portanto B=D sqrt(R), com domínio pago.
Essa cadeia está ligada ao contrato `BoundedTransformPreservesKernelAndGap`
por `normalized_graph_pays_contract`. A testemunha `NormalizedGraphWitness`
contém dados de grafo, positividade, comutação e normalização; NÃO pressupõe
igualdade de núcleos nem conclusão do gap.

Realizações conferidas:
- Família existente `resolventSquareRoot R hR hi`, 0≤R≤I, R injetivo:
  A=sqrt(R), B=sqrt(I-R); identidade efetiva do inverso de I+D².
- `continuousModularOperator c`: ligação direta ao mesmo modelo contínuo da
  missão, A=spectralA(c), B=spectralB(c). Não se trocou D por uma matriz.

## Limite exato

Permanece OPEN construir `NormalizedGraphWitness D` para TODO D prescrito,
densamente definido e auto-adjunto em LinearPMap. As realizações acima não
demonstram essa quantificação universal. O contrato condicional está compilado,
mas a existência da testemunha genérica não foi adicionada como axioma nem sorry.
Próximo passo dentro de A-2.5.c: projeção sobre o grafo fechado linear para obter
o resolvente de I+D²; reutilizar a infraestrutura V350 e a transferência de domínio.
`V350ClosedAntilinearResolvent` fornece um modelo de prova, mas sua antilinearidade
impede aplicá-lo diretamente a D linear. Esta etapa não foi declarada paga.
Nenhuma identificação do Dirac físico/H_min foi escolhida pela bancada.

## Verificação e custódia

17 theorem/lemma, todos cobertos por #print axioms; rc 0 nos quatro arquivos
aprovados; somente propext, Classical.choice, Quot.sound; zero sorry/axioma novo.
Nenhuma alteração de kernel detectada, nenhuma falha de varredura de custódia.
Comando exato em cada recibo: lake env lean -j1 -M8192, via compile_isolated_v2.py.
Falhas preservadas: projeção de pares, real de produto interno, hipótese de seção,
posição de comentário documental e substituição com domínio dependente.
Máximo três ciclos por arquivo, abaixo do teto de seis por lema.

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\unbounded_transform_manifest.json`.
Auditoria: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\unbounded_transform_axioms.json`.

- `UnboundedGraphTransform_v2.lean` SHA256 `106b15e6e3355fb1001d4297869237c8ad61ddd571781c6eb14d21da348734e0`; log `unbounded_graph_02.log` SHA256 `fc83ed2dc901470a67b8abb8b4458d4df4c0c36183d5a2bd170a73fc81dc09a1`.

- `ResolventBoundedTransform_v3.lean` SHA256 `99377c3546420dcf387d231d21b8de2d39629297511a48a332a4acae348ff7c4`; log `resolvent_bounded_03.log` SHA256 `c26ce5fa0f85001c3e368dc3b7573abf86aeda77f8fe68125de54083922bef49`.

- `ContinuousBoundedTransform.lean` SHA256 `12cd8028ba01a1a83553b620f9da8c960ea9adb52ab01ec15950300c92462775`; log `continuous_bounded_01.log` SHA256 `7038c6ba5c4afbf691eecebc2970ef978516536cb4f97b3014d1a2a6247fcdd6`.

- `NormalizedGraphContract_v2.lean` SHA256 `0193adec1869553b5a617b3dce26c2da4614f75cf7d9b0efb2507180abfe5404`; log `normalized_graph_02.log` SHA256 `54328ede7f41de4a18ab0ed630dbabee80ea7e1e52e3aa4a8be37e9f87607018`.

Máquina: 213.862s parede, 209.406s CPU em 8 tentativas.
Bancada decorrida: 947.894s. Nenhuma chamada externa nova neste lote.
Gasto conhecido por request_id: US$ 0.159306135; custos desconhecidos permanecem assim.
Leitura da listagem PARA_CHATGPT registrada no manifesto; documento mais recente:
`ADENDO_016_001_transporte_desassistido.md`. Não foi identificada nova escolha física do operador nesta rodada.

Originais, um.py, kernel e gate não alterados. A-2.5.c EM CURSO, com resultados
parciais medidos; relatório não encerra o ramo nem a missão. Cético ainda pendente.
