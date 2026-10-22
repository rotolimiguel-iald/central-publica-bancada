# Levantamento Lean F1.ATRATOR — 10/10/2026

Autor: codex-gerente-tgl/atrator_lean. [REAL] Leitura de fontes; nenhuma compilação candidata nesta etapa. Hashes lidos dos bytes em SOURCE_HASHES_R1.json.

## Já existe
- Mathlib/Analysis/InnerProductSpace/MeanErgodic.lean:96: ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection. Hilbert completo, operador contínuo linear, norma ≤1; as médias de Birkhoff/Cesàro convergem à projeção no espaço fixo. Não afirma convergência pontual das potências.
- Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean:124 starProjection; :149 imagem no subespaço; :173 e :185 unicidade da projeção; :240 eq_self_iff; :248 isIdempotentElem_starProjection; :252 range_starProjection.
- Mathlib/Dynamics/BirkhoffSum/NormedSpace.lean:79: diferença entre as médias da órbita de Tx e de x tende a zero quando a órbita é limitada. Isso prova R T = R usando unicidade do limite.
- TGLExt/TheAxiomAndTheFalseWitness.lean:104–164: axiomFlow P t=P+exp(-t)(1-P), semigrupo, fixação do posto, limite e fórmula exponencial. A forma de contração do complemento já existe; reaproveitar, não reivindicar construção nova.
- TGLExt/ExactWitness.lean:109: exact_witness_of_annihilating_word. Para D autoadjunto, aeval D (X*q)=0, q(0)≠0 e q real, (ker D).starProjection = q(0)⁻¹ • aeval D q. TGLExt/WordExistence.lean:170 demonstra existência finita de q quando ker D não trivial.
- TGLExt/TheObserverReadsTheAngle.lean:114: observing_adds_nothing; P+ (P+ Oθ)=P+ Oθ. A fonte prova idempotência de leitura angular; não prova limite angular.
- work/leitura_cria_o_objeto_07out/Palavra.lean:16–20 cunhagem LETRA para o polinômio normalizado; :97 rereading_adds_nothing reaproveita o teorema anterior. Esta candidata está no sandbox da gerência, não no TGLExt vigente.

## Construção que falta na entrega
1. A1: wrapper explícito do teorema ergódico médio, com R=starProjection de Fix(T).
2. A2: T R=R pela imagem da projeção; R T=R pela diferença das médias e unicidade do limite.
3. A3: R²=R e imagem=Fix(T), e a ligação literal D=1-T, ker D=Fix(T), à LETRA.
4. A4: hipótese nomeada StrictComplementContraction T e: e≠0, T e=e e existe 0≤c<1 que contrai vetores em (span{e})⊥. Provar Fix(T)=span{e}, portanto dimensão 1. A hipótese não será a própria conclusão.
5. Habitante: H=EuclideanSpace ℂ (Fin 2), e=(1,0), T=P+λ(I-P), |λ|<1. É a face óptica em coordenadas constante/diferença, λ=1−2β. Contraexemplo sem hipótese T=I, dimensão fixa 2. A mudança de coordenadas e o canal óptico literal serão medidos no Python, sem alegar uma isometria formal ainda não escrita.

## Pin e build previstos
Lean 4.31.0: C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe.
Mathlib no lake-manifest.json: fabf563a7c95a166b8d7b6efca11c8b4dc9d911f.
LEAN_PATH só para .lake/build/lib/lean do Nós e packages/*/.lake/build/lib/lean, todos usados como leitura. Saídas .olean e logs só em F1.ATRATOR/lean_sandbox. Sem junction e sem lake build no Nós.