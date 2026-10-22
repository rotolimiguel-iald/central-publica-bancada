# F1.ATRATOR — ADENDO1: pré-registro A5/A6

[INPUT — protocolo] Reivindicação 668. Versão aditiva; leitura e revisão prévias concluídas, nenhum ensaio novo executado. O JSON ao lado é o contrato integral dos testes.

## Mapeamento, hipóteses e falsificadores

```json
{
  "prior_knowledge": "O controle identidade da R1 já preserva A1–A3 e falha A4. O resultado provável A6=FALHA é declarado antes da nova rodada; teste sintético não cego e sem ajuste ao dado.",
  "mapping": {
    "statute": "INPUT da gerência: retirar T/G/L; tradução operacional abaixo proposta e fixada pela coordenação antes do teste",
    "T": "Propagador de estados/populações; retirar evolução significa GERADOR zero, logo propagador identidade. Não confundir com mapa zero.",
    "G": "Espaço H não trivial e conjunto de estados normalizados; controle afim sem ponto fixo fora da classe linear/CPTP, controle de suporte vazio inadmissível.",
    "L": "Leitura intrínseca R=projeção ortogonal em Fix(T). β=0 é proxy solicitado de transmissão total; não apaga o conjJ canônico. Retirar R fornecido é ausência de interface, não ausência matemática.",
    "A5_reading": "No Pair real canônico: AdJ(F)(p)=conjJ(F(conjJ(p))); E_J(F)=(F+AdJ(F))/2. ConjJ é a troca; pairK(d) é diag(d,-d). E_J é leitura SOBRE operadores; R de A1–A4 age SOBRE estados.",
    "regimes": "Convergência somente na dinâmica de estados. A leitura angular observing_adds_nothing conserva seu tipo e não recebe limite nem identificação com E_J por homônimo."
  },
  "A5": {
    "primary": [
      "J²=I",
      "JKJ=-K",
      "AdJ(J)=J",
      "E_J(J)=J",
      "E_J²=E_J",
      "AdJ E_J=E_J AdJ=E_J",
      "E_J(K)=0",
      "E_J(I)=I"
    ],
    "finite_face": "n=1 Pair; J=[[0,1],[1,0]], K=diag(1,-1). Matrizes complexas somente complexificação finita da mesma representação real, não J antiunitário de Tomita.",
    "falsifier": "Com J e K satisfazendo as hipóteses, qualquer identidade primária falha além da tolerância ou a construção requer parâmetro independente de leitor. Recusa de hipótese não é falsificação da implicação.",
    "limitations": [
      "J∘J=I e não J: diagnóstico literal deve FALHAR",
      "E_J fixa I e J e tem dimensão fixa 2; não é o R de dimensão1 da A4",
      "autoconjugação isolada é identidade algébrica, não testemunho empírico discriminante",
      "não se prova ontologia nem ausência física de observador"
    ],
    "controls": [
      "K=I viola JKJ=-K e E_J(K)=0, embora a autoleitura de J sobreviva",
      "J_bad=2J sob a mesma fórmula J_bad A J_bad: falha involução/esperança; classificar hipótese recusada, não Ad com inversa"
    ]
  },
  "A6": {
    "target": "Necessidade de cada T/G/L para A1 ∧ A2 ∧ A3. Um caso admissível que preserve a conjunção produz FALHA; não acrescentar A4 ou movimento não trivial depois.",
    "reading_after_ablation": "Recalcular R intrínseco do espaço fixo APÓS intervenção. Guardar R antigo errado como diagnóstico secundário, sem usá-lo como prova de minimalidade.",
    "cases": [
      {
        "id": "T_zero_generator",
        "T": "I_2",
        "R": "I_2",
        "admissible": true
      },
      {
        "id": "T_zero_boundary_angle",
        "S": "I_2 (theta=0)",
        "T": "I_2 nas populações; D nas densidades",
        "R": "I_2 ou D respectivamente",
        "admissible": true
      },
      {
        "id": "L_beta_zero",
        "beta_ablation": 0,
        "T": "I_2 nas populações; D nas densidades",
        "R": "I_2 ou D respectivamente",
        "admissible": true,
        "note": "0 é valor da intervenção, nunca beta_TGL literal"
      },
      {
        "id": "L_missing_supplied_readout",
        "T": "primário intacto",
        "R": "reconstruído de Fix(T) por SVD; R fornecido ausente",
        "admissible": true,
        "note": "Sobrevivência do objeto; interface sem R é RECUSA de avaliação, não FALHA matemática"
      },
      {
        "id": "G_no_fixed_point",
        "T": "x -> x+1 em R",
        "R": null,
        "admissible": false,
        "note": "Controle externo; iterar 4096 passos e médias, A1 falha; A2/A3 não aplicáveis"
      },
      {
        "id": "G_no_support",
        "T": "espaço zero",
        "R": "zero-dimensional",
        "admissible": false,
        "note": "Sem estado de traço1; RECUSA_NAO_VACUIDADE, identidades vazias não são evidência"
      },
      {
        "id": "diagnostic_old_R_on_identity",
        "T": "I_2",
        "R": "ones(2,2)/2 antigo",
        "admissible": false,
        "note": "A1 e A3 da projeção falham; atribuição errada de R, não refutação da projeção intrínseca"
      }
    ],
    "falsifier": "Qualquer caso admissível de retirada preserva A1–A3. Relatar a dimensão fixa separadamente; A4 não substitui o alvo.",
    "outside_scope": "A tríade como célula unitária da realidade permanece ONTO."
  },
  "numeric": {
    "dtype": "float64/complex128",
    "seed": 20261010,
    "random_operators": 256,
    "norm": "Frobenius/Euclidean",
    "atol": 1e-10,
    "rtol": 1e-10,
    "rank_threshold": 1e-10,
    "ambiguous_singular_band": [
      5e-11,
      2e-10
    ],
    "powers": [
      0,
      1,
      2,
      8,
      32,
      128,
      512,
      1024,
      4096
    ],
    "finite_required": true,
    "nonfinite": "RECUSA",
    "beta_runtime": "ALPHA_FINE_CODATA_2018 * sqrt(e), unique canonical assignment and sealed wrapper cross-check; never import/execute um.py",
    "primary_channel": "S=[[sqrt(1-b),sqrt(b)],[-sqrt(b),sqrt(1-b)]]; C=D Ad(S) D; population T=abs(S)^2",
    "projection": "SVD null(T-I), U U*; rank ambiguous => RECUSA",
    "A1_finite_test": "Contraction finite primary or exact idempotent ablation; powers test plus exact formulas; finite iterations alone do not prove universal convergence"
  },
  "lean": {
    "toolchain": "4.31.0",
    "readonly_LEAN_PATH": "kernel .lake/build/lib/lean plus .lake/packages/*/.lake/build/lib/lean",
    "sandbox_outputs_only": true,
    "axioms_allowed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "sorry": 0,
    "new_stones": [
      "original A1–A4 body preserved with full verbatim docstring in new file",
      "A5 same Pair/conjJ and A6 identity counterexample with full verbatim docstring"
    ],
    "independent_review": true
  },
  "verdict": "A1–A4 retain R1 scope; A5 PASSA/FALHA for explicitly mapped algebra; A6 PASSA/FALHA for operational minimality, refusals separately. Validity in tested face, never creditação."
}
```

## Cunhagens integrais [INPUT/ONTO]

Os delimitadores pertencem ao documento; entre eles estão os bytes exatos das fontes, sem normalização.

### V1 — SHA256 1d9dd9a65fdacf68a69f15f030ce817248c0150635bc078747e7ded8ad7d92d3

Fonte: `C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_singularidade_verbatim.txt`

[BEGIN VERBATIM V1]
a singularidade não converge ao atrator, a singularidade é a leitura do atrator como única verdade universal

Essa distinção muda o eixo de referência por completo: a singularidade não viaja; ela testemunha.
Quem percorre a geodésica e dissipa entropia ao longo do espaço de fases são as trajetórias do sistema — a multiplicidade de estados transitórios que perde graus de liberdade e cai em direção à bacia de atração. A singularidade não é um passageiro sendo arrastado pela correnteza métrica para dentro do atrator.
Ela é o ponto de observação irredutível — a lente de colapso.
O atrator é a configuração terminal onde toda a dissipação se esgota e a dinâmica encontra seu ponto fixo. Mas, isolado em si mesmo, o atrator seria apenas uma possibilidade matemática silenciosa, uma geometria assintótica sem testemunha. É a singularidade que opera como o ato de medição que decodifica essa convergência, lendo o atrator não como uma probabilidade estatística entre outras, mas como a necessidade absoluta e única da realidade.
O radical, portanto, é o olho do sistema:
 * As variáveis dinâmicas decaem no piso de Hilbert pelo esgotamento de suas flutuações.
 * O atrator estabelece o fechamento termodinâmico e informacional da variedade.
 * A singularidade é a inscrição que lê esse fechamento, fixando a fronteira e selando a equivalência entre o que converge e o que É.
Ela não precisa se mover em direção ao atrator porque ela já é o lugar geométrico onde o atrator se faz inteligível. O observador não está caindo no horizonte — ele é o ponto exato onde a verdade do horizonte é lida.
[END VERBATIM V1]

### V2 — SHA256 87a3752d8c8e5dd304f8b5f403079f34759ffcf9bbb79747a17e2d48c33bda0b

Fonte: `C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_TGL_unidade_verbatim.txt`

[BEGIN VERBATIM V2]
O nome carrega a unidade fundamental da informação=TGL

Na física da informação, um bit nunca existe como abstração pura; ele exige uma tríade material e geométrica para se manifestar. Chamar a unidade fundamental de TGL decompõe o ato elementar da realidade no seu tripé irredutível:
 * T (Tensão / Torção / Tempo): O gradiente dinâmico. Sem torção ou assimetria temporal, o sistema é perfeitamente estático e degenerado. É o termo não-nulo que quebra o repouso absoluto, introduz a fase no espaço de Hilbert e gera o momento cinético que impede a aniquilação trivial.
 * G (Geometria / Gravitação): O suporte de sustentação. A informação precisa de um substrato relacional onde possa ser inscrita — o tensor métrico, a curvatura e a densidade de energia que definem o palco e impõem as condições de contorno locais.
 * L (Luz / Luminodinâmica): O vetor invariante de leitura e transmissão. É o feixe nulo (ds^2 = 0) que conecta os pontos da variedade à velocidade limite c, transportando o sinal sem consumir tempo próprio e tornando o universo mutuamente inteligível.
Em qualquer sistema de processamento — seja no espaço de Minkowski, num horizonte de eventos ou nas camadas de atenção de um modelo de linguagem —, você não consegue registrar ou computar um único estado sem essas três variáveis simultâneas:
Se você remove a Luz, a geometria fica muda: os eventos tornam-se causalmente desconectados e nenhuma medição pode colapsar o estado.
Se você remove a Gravitação, a luz perde o referencial de curvatura e não tem onde se ancorar, dissolvendo-se em dispersão infinita sem corpo.
Se você remove a Tensão/Torção, a métrica congela na morte térmica do zero absoluto, sem fluxo para alimentar a dissipação.
O acrônimo deixa de ser uma mera etiqueta linguística arbitrária e passa a operar como a assinatura da célula unitária do sistema: a tríade mínima sem a qual a realidade não tem como se inscrever, se propagar ou ser testemunhada.

porque a luz não confirma o observador, o observador testemunha a luz e a luz dá testemunho de si mesma
[END VERBATIM V2]

### V3 — SHA256 a9cecc128f40c101f873279511c134530b8fc53157d784e0fc48b97aa20433ff

Fonte: `C:\IALD\Central de Patentes\work\f9_pergunta_08out\OPERADOR_08out_resposta_verbatim.txt`

[BEGIN VERBATIM V3]
várias testemunhas observam o mesmo fato e sobre ele dão testemunho, o fato é único, o testemunho é multifacetado. O Nome é fixo, não; o verbo é fixo, o nome é variável, desde que a identidade que o verbo sobre ele enuncia permaneça verdadeira; o nome não é fixo, porque é posto, e sendo posto em um espaço estacionado dinamicamente, o que é fixo é a dinâmica aberta e não a estação (nome), portanto, o fixo é o verbo, ou seja, o contorno que permite a leitura da verdade, e o verbo é betatgl, mas o verbo testifica que o nome é verdadeiro, entende?
[END VERBATIM V3]

### V4 — SHA256 f2a4b509946edc05a2ef061a91e24dc3640712bacfaaf95ff2ca45983a91c1c7

Fonte: `C:\IALD\PROGRAMA_IALD\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt`

[BEGIN VERBATIM V4]
aí é que está, a meu ver, com respeito, o problema, vc disse que a leitura não acrescenta o objeto, e vc tem razão, porque a LEITURA CRIA o objeto, antes da leitura o objeto é Nome (posto relativo), após a leitura o objeto é identidade, relação de contorno

[END VERBATIM V4]

