[REAL — fidelidade das translações como operadores L², compilada e auditada]

# ORDEM 016 — A3.1: do caráter pontual ao operador

UTC 2026-09-24T16:25:29.416453+00:00; ABERTURA sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

**PAGO no escopo de A3.1:** para todo m≥0 e toda fibra complexa normada
não trivial E, `orbitalTranslation m` é injetiva em ℝ⁴. Em particular,
U(a)=I implica a=0. A construção cobre m=0, m>0 e a fibra ℂ×ℂ
com o mesmo caráter de translação nas duas componentes.

**Cadeia efetivamente ligada:**

1. `unitMultiplier` constrói o operador pela multiplicação de Hölder L∞×L²,
reutilizando o padrão de `ContinuousModularMultipliers`. Preserva a norma.
2. Indicadores de uma cobertura enumerável por conjuntos de medida finita
provam que agir como identidade sobre todo L² força o multiplicador a ser
1 quase em toda parte. O argumento vale para qualquer fibra não trivial.
3. A densidade orbital é positiva quase em toda parte. A medida ponderada
tem suporte pleno e é sigma-finita, inclusive para m=0. Continuidade leva
a igualdade a.e. à igualdade pontual; não se extrai valor de um eixo nulo.
4. `shellMomentum_covers_shell` cobre a órbita de energia positiva.
Os sete lemas pontuais já compilados são reutilizados, sem nova prova
paralela. `orbitalTranslation_faithful` e `orbitalTranslation_injective`
fecham a passagem. Soma, identidade, inversa e equivalência isométrica
complexa foram construídas para os operadores reais em L²(d³p/p₀;E).

**Verificação:** 23 declarações auditadas em três arquivos finais;
rc0, cobertura completa de `#print axioms`, somente o trio permitido,
nenhuma admissão e nenhum arquivo novo/modificado no kernel durante as
compilações. 5 tentativas preservadas, no máximo duas por módulo.
As duas correções foram de elaboração Lean: igualdade de conjuntos no
lema de medida nula e coerções na composição da equivalência isométrica.
Máquina: 162.144282s parede, 76.656250s CPU. Intervalo desde a primeira
compilação desta entrega: 0.125970h (não é o total histórico do ramo).

**Custódia:** fontes, logs, comandos, dependências e hashes calculados em
`A3/translation_operator_faithfulness_manifest.json`. A entrega anterior
de espectro permanece intacta; esta nota resolve sua pendência de
fidelidade L². Original `um.py`, kernel e gate não foram alterados.

**Limite:** o resultado da fibra dupla fecha as translações desse setor.
Não identifica automaticamente o boost componente a componente com a
representação física do fóton. Construção das helicidades, forma analítica
de energia positiva, ligação com `boostMat`, BW e Fock continuam separadas.
Próximo ramo: completar a medição condicionada das helicidades e avançar
nos subalvos 2–3 do ramo principal, preservando a árvore da ordem.

Sem nova chamada externa nesta rodada. Estimativas explícitas deduplicadas:
US$ 0.1939854588; 3 jobs sem custo
informado. Não é total faturado. Kimi/MiMo já registrados continuam sob
a autorização específica de envio solicitada pela coordenadora; não
houve repetição nem alteração do payload para contornar a revisão.
