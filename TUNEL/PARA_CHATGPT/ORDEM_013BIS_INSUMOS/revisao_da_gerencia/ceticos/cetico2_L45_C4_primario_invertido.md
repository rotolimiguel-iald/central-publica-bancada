# CÉTICO 2 — achado L45 §2 item 1 (primário/robustez do C4 invertidos) — NÃO REFUTADO

Data: 22/09/2026. Fontes lidas por script (bancada só-leitura):

1. `ORDEM_013_RINGDOWN/posterior_220_readout.py` (docstring l.2-5): «B = p(df,dtau-g(spin)|d)(0,0)/p(df,dtau|d)(0,0). The shear transformation has Jacobian one; it is not mean conditional ratios.» — g(spin) amostra a amostra.
   l.75 «# Primary R-B…»; l.78 `shift = [prediction(m,a)… for m,a in zip(mass,spin)]` (amostra a amostra); l.81 `central = ratio_pair(data, shift)` → l.90 `lnB_joint_spin_curve=central`;
   l.82-83 `medshift = prediction(median(mass), median(spin))`; `median_case = ratio_pair(data, full(medshift))` → l.91 `lnB_fixed_median_spin=median_case`.
2. `ORDEM_013_RINGDOWN/C4_220_INITIAL.json` rows[0] (lido por json): `lnB_joint_spin_curve = 0.029026161519275284`; `lnB_fixed_median_spin = 0.027148326341676743`; `lnB_tau_marginal = 0.073650982937286`.
3. `TUNEL/DO_CHATGPT/ENTREGA_013_C4b_…md` l.5: «pSEOB primário: 0.029026162» — a bancada NOMEIA o primário = joint_spin_curve.
4. `auditoria/aud_6.txt` l.37: «identidade de Bayes correta (razão de integrais, via cisalhamento com jacobiano 1) … Com o spin fixo na mediana: 0,02715».
5. A própria ORDEM 013-bis l.34 cita «GW250114: ln B(R-B) = +0,029» — o número do primário da bancada (joint_spin_curve), o que contradiz a descrição da l.45 (que chama de primário a versão na mediana = 0,027).

Veredito: a frase da l.45 inverte primário e robustez. Inconsistência interna (l.34 vs l.45) e descrição errada do que a bancada fez, numa ordem que será imutável. Não induz erro de física (as duas quantidades são fatores de Bayes legítimos, diferem 0,002) → IMPORTANTE, não BLOQUEANTE. refutado=false.

Correção FINAL (substitui, na l.45, o trecho entre «A bancada acertou» e «sem efeito.»):

«A bancada acertou ao usar a identidade correta: razão das integrais sob o posterior de χ com a predição dependente do spin, amostra a amostra (cisalhamento de jacobiano 1; **primário** ln B = +0,029, `lnB_joint_spin_curve`) e, **como robustez**, a predição avaliada na mediana de χ (ln B = +0,027, `lnB_fixed_median_spin`) `[REAL — C4_220_INITIAL.json rows[0]; aud_6]`. Vale a versão da bancada; a frase da ordem fica sem efeito.»
