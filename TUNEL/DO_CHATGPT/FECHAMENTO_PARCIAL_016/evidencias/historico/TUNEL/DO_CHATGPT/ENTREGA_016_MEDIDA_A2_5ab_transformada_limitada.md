[DERIVED — 25 declarações compiladas e auditadas isoladamente]

# A-2.5.a e A-2.5.b — transformada limitada

Data UTC: 2026-09-24T14:06:18.670768+00:00. ABERTURA sha256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

Construído por cálculo funcional contínuo, para todo operador limitado D em Hilbert complexo:
`S = sqrt(I+D*D)`, `R=S^(-1)`, `b(D)=D R = D (I+D*D)^(-1/2)`.
Provadas a positividade estrita, a invertibilidade de S e a identidade
`||x||² = ||Rx||² + ||b(D)x||²`.

Conclusões compiladas:

- `ker b(D) = ker D`; S e R fixam pontualmente esse núcleo e preservam seu ortogonal.
- `||b(D)x|| ≤ ||x||`.
- Se `γ≥0` e `γ||y|| ≤ ||Dy||` no complemento ortogonal do núcleo, então
  `γ/sqrt(1+γ²) ||x|| ≤ ||b(D)x||` no mesmo complemento.
- Se um vetor atinge a razão γ para D, Sx atinge a razão transformada para b(D).
  Um limite inferior não é anunciado como mínimo espectral atingido sem essa hipótese.
- `finiteTransform` é uma matriz real de código (Matrix n n ℂ), obtida pela equivalência
  canônica star-algébrica com os operadores euclidianos. A fórmula, o núcleo e o gap
  foram transportados por essa equivalência. A prova comum atende a face finita e
  também ao operador limitado geral, sem duplicar argumentos.

Consulta prévia: V354BoundedPolar.lean já tem a decomposição polar e propriedades do
valor absoluto. Seu boundedAbsolute_ker é privado; a nova prova de ker b(D) usa a raiz
de I+D*D, sua inversa efetiva e fixação do núcleo, não um pressuposto de igualdade de núcleos.

Validação: 25 theorem/lemma cobertos por #print axioms; rc 0; apenas o trio
propext/Classical.choice/Quot.sound; nenhum sorry/axioma novo. Zero alteração detectada
no kernel e zero erro de leitura nos quatro recibos aprovados. Warnings de nomes antigos
de APIs e variável implícita preservados; não são falhas matemáticas.
Comando: `python -X utf8 -B A0/compile_isolated_v2.py <kernel> <fonte> <rótulo> <A2>`.
Tentativas falhas preservadas: import da ordem de operadores ausente/argumentos da
inversa; parâmetros implícitos da equivalência matricial. Nenhum lema excedeu seis ciclos.

Custódia: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\bounded_transform_manifest.json`.
Auditoria: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\bounded_transform_axioms.json`.

- `BoundedTransformCore_v2.lean`: `705b9a8abcd4fa12fb942c855a68bcf0950029bb85f12e2f04858de36b46b1a1`; log `bounded_core_02.log`: `9d2d3079c4a9c904cfaa7a6d49be75ddf48c020982597030372a218002d672d3`.

- `BoundedTransformKernel.lean`: `91ee403e5bc102dee9069610af97240b47a296797e15a362ad5c70f9c52294d0`; log `bounded_kernel_01.log`: `8efdb5ed866f997645fa62f0f47c51d6263891c205d8ad72b62b99d0eb48bb24`.

- `BoundedTransformGap.lean`: `2e78b419bc9e70bd3c9aa842163a270397c767d148ae8045c6bc556bd3caa815`; log `bounded_gap_01.log`: `a01232484883a33d8bd48e569533de0067a785de0158c56550e4cba99d0f5ffe`.

- `BoundedTransformFinite_v2.lean`: `54d4cc0d4c49f939eb5fef91d0201fd07c2b4e140fbd9bbd77bd74492346025b`; log `bounded_finite_02.log`: `88a23431f0e96354fb8b61101396c8890273dedd79b3626c19eadad16e4972bd`.

Máquina: 96.921 s parede, 96.594 s CPU em 6 tentativas.
Bancada decorrida: 578.806 s. Nenhuma chamada externa nova para esta construção;
crítica Kimi anterior recebida e contabilizada separadamente, sem duplicação.
Gasto monetário conhecido agregado por request_id: US$ 0.159306135; valores desconhecidos
continuam desconhecidos, inclusive o custo monetário de Kimi.

Não move o gate nem identifica D com o Dirac microscópico da teoria. Essa identificação
nunca foi escolhida pela bancada. A-2.5.a/b: PAGO no escopo matemático acima.
Próximo ramo A-2.5.c: operador ilimitado LinearPMap, com domínio explícito; não transferir
automaticamente a prova de operador limitado. Controle adversarial A-2.3: revisão recebida,
mas a direção reversa domínio/faixa requerida pelos contraexemplos permanece pendente.
