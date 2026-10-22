[REAL — controle de uniformidade provado; OPEN — limite forte geral ainda não formalizado]

# A6.B1d — MEDIDA da rota por cálculo funcional

Abertura do operador, SHA256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

A API `tendsto_cfc_fun`, em `Continuity.lean`:83, exige **TendstoUniformlyOn** no espectro; não recebe convergência pontual. A leitura do enunciado e a hipótese estão transcritas e custodiadas no manifesto.

Compilados e auditados três teoremas: para λ≥0, exp(−sλ) converge pontualmente ao indicador de λ=0; para cada s≥0, λ=1/(s+1) pertence a (0,1] e o erro é maior que exp(−1); logo a tolerância uniforme exp(−1) não pode ser atingida nesse intervalo. O primeiro probe falhou por composição de filtros e orientação de uma identidade de fração; a segunda versão compilou rc0, somente trio. Fontes/logs das duas tentativas preservados.

**Alcance:** isso impede a aplicação geral direta daquela API ao limite espectral descontínuo. Não refuta a convergência forte e não constrói o operador diagonal em ℓ²; o controle formal atual é escalar. A propriedade operatorial exigida continua NÃO PAGA nesta rodada:

`bounded_positive_strong_limit`: H limitado, auto-adjunto e não negativo em Hilbert completo ⇒ T_s x→P_ker(H)x para cada x, sem hipótese de dimensão finita ou gap.

Rota analítica alternativa identificada: construir estimativa para exp(−sH)H, contração uniforme e densidade de ker(H)+ran(H), e usar `EquicontinuousAt.tendsto_of_mem_closure` (Equicontinuity.lean:963). Outra rota é representar a norma residual por uma medida espectral e aplicar convergência dominada. Esses passos não foram compilados aqui. Não substituí a conclusão por um novo axioma; a recíproca infinita existente continua condicionada a `FlowTendsToFamily`, como prevê a receita. Ausência de gap não autoriza limite em norma.

MEDIDA delimita a formalização atual, sem declarar parede física. O controle da API foi pago; a passagem forte geral permanece aberta. Revisão Kimi B1d já estava preparada, sem nova chamada. Próximo ramo da árvore: B8 e controles C. Teto de duas horas não foi esgotado; não se alega que seja impossível completar a formalização.

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A6_EQUACAO_DA_VERDADE\B_fechamentos\infinite_measure_and_modular_manifest.json`. Duas compilações B1d, tempo de máquina 25.984177s; comandos, rc, hashes e avisos no manifesto. Não move gate.
