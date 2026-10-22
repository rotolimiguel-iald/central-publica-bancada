# CÉTICO 1 — achado fidelidade_auditorias sobre a ORDEM 013-bis, linha 45 (§2 item 1)

**Veredito: NÃO refutado (refutado=false). Gravidade: IMPORTANTE (mantida).**

## O que medi [REAL — por script, 22/09/2026]
- `ORDEM_013_RINGDOWN/C4_220_INITIAL.json` rows[0] (reading R-B):
  `lnB_joint_spin_curve = 0.029026161519275284`; `lnB_fixed_median_spin = 0.027148326341676743`;
  `lnB_tau_marginal = 0.073650982937286`.
- `ORDEM_013_RINGDOWN/posterior_220_readout.py` docstring l.2–5: «Exact density identity for a spin-dependent
  curve … B = p(df,dtau-g(spin)|d)(0,0)/p(df,dtau|d)(0,0). The shear transformation has Jacobian one; it is not
  mean conditional ratios.» l.77–83: `shift` calculado amostra a amostra de (mass, spin); `central = ratio_pair(data, shift)`
  → gravado como `lnB_joint_spin_curve` (l.90). `median_case = ratio_pair(data, np.full(len(shift), medshift))[0]`
  → `lnB_fixed_median_spin` (l.91). Logo: primário = integral com predição dependente do spin; mediana = secundário.
- `aud_6.txt` (item «Predição dependente de spin amostra a amostra e na mediana»): «identidade de Bayes correta
  (razão de integrais, via cisalhamento com jacobiano 1) … Com o spin fixo na mediana: 0,02715 (reproduzido)».
- `ENTREGA_013_C4a_REGISTRO_POSTERIORES.md` l.14: «o Bayes factor é razão de integrais de densidade corrigida pelo
  prior, não a média de razões condicionais».
- ORDEM 013 l.231 (a frase corrigida): «avaliada amostra a amostra (média da razão condicional) e na mediana».

## Por que o achado se sustenta
A linha 45 da 013-bis diz «razão de densidades marginais na predição avaliada na mediana e, como robustez, a integral
da predição dependente do spin». Os papéis estão trocados em relação ao código e ao JSON da bancada. Defeito adicional
não apontado pelo revisor: «densidades marginais» é impreciso — a estatística primária é a densidade CONJUNTA
(δf̂, δτ̂) em (0,0) após o cisalhamento, com o setor 440 marginalizado; a versão só-marginal de δτ̂ é um TERCEIRO
número (0,0737), reportado à parte. Numa ordem imutável, a bancada leria que seu primário é o da mediana.

## Correção FINAL (texto exato para a linha 45, mantendo estilo e estatutos)
1. **§3 C4, «média da razão condicional».** A média, sobre amostras do posterior, da razão condicional p(δ_L(χ_s) | d)/p(0 | d) **não é um fator de Bayes**. A bancada acertou ao usar a identidade correta: razão das densidades conjuntas (δf̂, δτ̂) em (0,0) com a predição dependente do spin aplicada amostra a amostra sob o posterior de χ (cisalhamento de jacobiano 1; setor 440 marginalizado; ln B = +0,029, `lnB_joint_spin_curve`, primário) e, como robustez, a predição avaliada na mediana de χ (ln B = +0,027, `lnB_fixed_median_spin`) `[REAL — C4_220_INITIAL.json rows[0]; aud_6]`. Vale a versão da bancada; a frase da ordem fica sem efeito.
