# Revisão Lean independente — F1.ATRATOR

Autor: atrator_skeptic, sob reivindicação 664. Protocolo ACOM recuperado na própria referência; a coordenação serializa as transições.

**Veredito técnico: PASSA no alcance dos enunciados.** Nenhum achado material pendente. O ato administrativo AUDITADA/FECHADA continua com a c1. Os nomes singularidade, leitura e atrator conservam a interpretação [ONTO]; os resultados abaixo são matemáticos condicionais.

## Recompilação independente [REAL]

Ambas as fontes finais foram copiadas em bytes para `review/lean_independent`, verificadas contra os recibos dos construtores e compiladas sem alterar seus originais. Todos os diretórios do LEAN_PATH pertencem ao `.lake` do Nós; só foram usados para resolver imports. Fontes, logs e .olean novos ficam no sandbox, sem junção NTFS. Não se executou lake build nem se instalou a candidata.

| Fonte | EXIT | Segundos | Impressões de axiomas | .olean idêntico |
|---|---:|---:|---:|---|
| TheSingularityReadsTheAttractor.lean | 0 | 59.258029 | 14 | Sim, byte a byte |
| OpticalPopulationBridgeR2.lean | 0 | 22.435016 | 15 | Sim, byte a byte |

Toolchain: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`. As 29 impressões dependem apenas de propext, Classical.choice e Quot.sound. Zero `sorry` nas duas fontes; nenhum sorryAx nos logs. A principal contém 20 teoremas (14 pontos de impressão, abrangendo as conclusões pedidas); a ponte contém 15 e imprime todos. Os recibos e logs independentes guardam comando, início, fim, segundos, LEAN_PATH literal, saída, código, hashes de fonte e objeto. Hashes medidos no JSON ao lado.

## A1 — PASSA, com as duas modalidades ditas

`A1_cesaro` exige Hilbert completo e operador linear contínuo com norma ≤1. Reaproveita o teorema ergódico médio de mathlib e conclui convergência de `birkhoffAverage` para `reading T`, definido como a projeção ortogonal no espaço fixo. Não promete convergência das potências para toda contração.

`faceFamily_iterate` demonstra exatamente T^n x=P x+λ^n(x−P x). `A1_face_orbit` usa ∥λ∥<1 para a convergência forte da família dissipativa. Para e não nulo, A4 identifica Fix(T)=span(e), de modo que este P é a mesma leitura. Nenhum limite da órbita angular aparece.

## A2 — PASSA

`A2_evolution_after_reading` prova TR=R porque a imagem da projeção pertence ao espaço fixo, sem exigir contração. `A2_reading_after_evolution` usa a contração e a unicidade do limite de Cesàro para RT=R. `A2_reading_stationary` reúne ambas como igualdades de composição de operadores, não apenas numa amostra de vetores.

## A3 — PASSA

A escolha `reading T := starProjection(Fix T)` é explícita. Sua idempotência e a igualdade da imagem com o espaço fixo são teoremas; não há campo livre que apenas postule idempotência. A existência e a normalização da letra reaproveitam WordExistence/ExactWitness com D=I−T e ker(D)=Fix(T).

`A3_normalized_letter` exige D auto-adjunto, (Xq)(D)=0, q(0)≠0 e coeficientes reais no sentido da conjugação; conclui R=q(D)/q(0). `A3_letter_exists_finite` demonstra existência de q em dimensão finita com espaço fixo não trivial. Não aplica indevidamente o aniquilador inteiro como projeção.

`A3_angular_rereading_only` reaproveita a identidade `observing_adds_nothing` exatamente no seu tipo. Não identifica por homonímia a projeção angular projPlus com R de populações. PALAVRA permanece a cunhagem da leitura; a letra normalizada é a ponte matemática que efetivamente está provada.

## A4 — PASSA e não vacuidade exibida

`StrictComplementContraction T e` contém e≠0, Te=e e uma constante 0≤c<1 que limita ∥Tx∥ no complemento ortogonal de span(e). Nenhum campo assume Fix(T)=span(e), dimensão 1 ou a própria conclusão. A prova subtrai a projeção em span(e); um ponto fixo no complemento teria norma ≤c vezes a mesma norma, forçando zero. Obtém Fix(T)=span(e) e finrank 1.

`concrete_hypothesis_inhabited` fornece H=ℂ², e=single 0 1, λ=1/2 na família P+λ(I−P). Esse é um habitante exato e não trivial. **λ=1/2 é testemunha de não vacuidade, não o valor de β nem o fator transitório do ensaio físico.** A mesma família é demonstrada para qualquer λ de norma <1. O contraexemplo identidade em ℂ² tem dimensão fixa 2, mostrando o peso da hipótese; por A4, a identidade não pode satisfazê-la.

## Ponte óptica — PASSA no alcance algébrico

A ponte demonstra para b simbólico T=[[1−b,b],[b,1−b]]=R+(1−2b)(I−R), RT=TR=R, R²=R, simetria, inversa da base soma/diferença e conjugação à diagonal diag(1,1−2b). Para 0<b<1/2, prova 0<1−2b<1. Demonstra também a letra q(D)/q(0), o aniquilador Xq, o controle b=0 e x+1≠x do controle afim.

A base soma/diferença é declaradamente não normalizada, com inversa formal explícita; não é apresentada como isometria normalizada. A candidata Hilbert e a ponte de matrizes são resultados complementares: não se afirma que um único teorema contém o extrator Python, a constante CODATA, as matrizes densidade e a dinâmica inteira GKLS. A avaliação de β a partir do programa pinado é a etapa numérica já auditada. O canal completo de densidade e sua propriedade CPTP foram verificados na rodada numérica; esta ponte Lean trata populações.

## Limites preservados

Unicidade refere-se ao espaço fixo de dimensão 1; unicidade de um estado exige a normalização de soma/traço. Não comutatividade isolada de saltos não foi usada como hipótese universal. O pilar v384/v385 permanece reaproveitamento documental de sua grade numérica, sem nova prova geral atribuída a ele. A prova não deriva confirmação empírica, ontologia universal nem um efeito a 5σ. Nada no Nós, Bancada de produção, um.py ou gate foi alterado por esta revisão.
