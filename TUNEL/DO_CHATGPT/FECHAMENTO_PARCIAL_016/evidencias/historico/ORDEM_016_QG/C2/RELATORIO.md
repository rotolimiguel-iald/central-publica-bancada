[REAL — C2: critério de largura provado; necessidade a partir da isotonia nomeada]

AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

Cinco enunciados novos compilaram com rc0 e axiomas somente do trio.
Para m_a(z)=exp(i a exp(z)), a>0 e w>0, ficou provado:
**contração em toda a faixa 0≤Im z≤w + borda conjugada ⇔ w=π**.
A restrição anterior w<2π foi retirada das hipóteses: se w≥2π,
o ponto z=3πi/2 tem norma exp(a)>1, contradizendo a contração.
A borda conjugada permanece essencial: a faixa π/2 contrai, mas falha
na borda. Positividade e contração sozinhas não selecionam π.

Foram reconferidos os hashes de fontes, recibos rc0 e logs do pacote
A2/density_separation_manifest.json: a densidade gaussiana real e
halfline_isotony para U e K efetivos já estavam pagos. Foram reutilizados,
nunca recriados nem contados como novas provas. O parâmetro desse K é
c=2π²; a largura analítica é π. A ponte Fourier existente identifica
a fase com log do símbolo do Delta construído, mas não é automaticamente
um teorema regional BW/KMS.

**Lema ainda não pago: IsotonyImpliesStripMultiplierCriterion.** Para w>0 e
K_w=rapidityStandardSubspace(2πw), deduzir de U(a)K_w⊆K_w para todo
a≥0 o critério analítico de contração e borda conjugada usado acima.
O novo resultado paga a conclusão a partir desse critério; não transforma
uma condição suficiente de preservação em condição necessária.
Não foi criado axiom Lean para ocultar essa lacuna. Este é o lema nomeado
previsto na aceitação C2. A crítica C2.2 terminou por APITimeoutError,
não por resultado matemático; a chamada terminal não foi repetida.

Auditoria: AXIOM_AUDIT.json; comando, logs e recibos width_01/02 preservados.
Recursos: 2 compilações, parede 19.108s, CPU 18.891s;
bancada 0.1616h/teto12h. Não move o gate, não constrói H2 regional.
Próximo C3: integrar as doze fontes A6 mantendo corpos e hipóteses.
