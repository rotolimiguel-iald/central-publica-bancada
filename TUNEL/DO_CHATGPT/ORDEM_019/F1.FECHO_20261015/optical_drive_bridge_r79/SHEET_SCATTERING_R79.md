# R79 — da folha OH à reflexão e transmissão

**[DERIVED — condicional, NOT_LEAN, sem execução]** Complemento de `MATERIAL_IDENTIFICATION_R79.md`, §4. Admitir H_LINEAR_OH_SHEET e uma folha elétrica isotrópica (ou uma polarização própria escalar desacoplada), em z=0, incidência normal, mesma admitância **real Y>0** nos dois lados, sem corrente magnética de superfície. Convenção temporal e^(−iωt), ω>0. Defina σ_s(ω)=−iωε0χ_sheet(ω). O ramo passivo exige Reσ_s≥0; ganho por inversão de população não está nesse ramo. O domínio da susceptibilidade continua sujeito a `MATERIAL_DOMAINS_R79.txt`.

## Sinais e solução das condições de contorno

Para incidência pela esquerda, tome E paralelo a x e normal n=+z. O campo magnético é +Y E para a onda que avança e −Y E para a refletida. Continuidade tangencial fornece E_t=E_i+E_r. A condição n×(H_direita−H_esquerda)=K_sheet=σ_s E_t dá

    −Y(E_t−E_i+E_r)=σ_s E_t,  isto é, −2Y E_r=σ_s(E_i+E_r).

Logo, quando D=2Y+σ_s≠0,

    r=E_r/E_i=−σ_s/D,      t=E_t/E_i=2Y/D=1+r.       (1)

No ramo passivo, ReD≥2Y>0: não há polo dessa solução. Fora dele, D=0 é excluído e não se divide por zero. Como os meios externos têm a mesma admitância real, as frações de potência são R=|r|² e T=|t|². Subtração direta fornece

    A=1−R−T=4Y Reσ_s/|2Y+σ_s|² ≥0.                 (2)

Assim a susceptibilidade derivada no regime nomeado determina amplitude, fase e absorção; não apenas um módulo de reflexão. Se houver absorção, o modelo quântico deve incluir o ambiente/ruído como em R72/R77. A matriz reduzida de amplitudes não é unitária nesse caso.

## Confronto com β, sem escolhê-lo como ajuste

Para comparar o valor obtido da resposta material com uma refletividade β previamente fixada, a condição necessária e suficiente neste submodelo é

    |σ_s|² = β |2Y+σ_s|².                            (3)

Ela é um critério de confronto: não determina χ escolhendo-a para satisfazer β. Nesta derivação β é simbólico; um consumidor TGL deve calculá-lo em runtime como ALPHA_FINE_CODATA_2018·√e, conforme a regra vigente.

No caso **sem perda**, σ_s=i b, b real, e 0≤β<1, (3) equivale a

    b² = 4Y² β/(1−β).                               (4)

O sinal de b e a fase dos coeficientes continuam relevantes. β=1 não é alcançado por b finito neste modelo com Y>0; o limite |b|→∞ é distinto de uma folha finita. A condição (4) não mede b nem prova que o OH a satisfaça.

Para entradas a partir dos dois lados, com planos de referência na folha e ordenação (saída esquerda, saída direita), a matriz é

    S_sheet = [[r,t],[t,r]].                         (5)

No caso sem perda, |r|²+|t|²=1 e r* t+t* r=0, logo S_sheet é unitária. Mesmo que |r|²=β, sua identificação com S_beta exige comparar **ambos os canais e suas fases**, a ordenação das portas e eventuais fases de referência previamente fixadas. Uma igualdade de intensidades não prova igualdade de operadores. Este complemento fecha o cálculo contorno→(r,t,A) no regime declarado; não estabelece o regime material real nem fecha R4.
