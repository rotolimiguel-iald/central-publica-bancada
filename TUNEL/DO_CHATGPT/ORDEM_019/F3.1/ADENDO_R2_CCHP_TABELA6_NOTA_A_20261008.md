# F3.1 V2 R2 — âncora explícita da Tabela 6, nota a, do CCHP

**Acréscimo ao lado do pacote R2 já registrado; nenhum arquivo pinado foi sobrescrito.** Fonte integral arquivada: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\h0dn_documentary_review\jagb_extension\residual_systematics\sources\cchp_overview.txt`, SHA-256 `e32d608358cc0f0dcc3def744beef4b9afea24a967c8f730c90027dc589b6dcc`.

**[REAL documental]** A fonte dá a distância geométrica de NGC 4258 com erros 0,024 (estatístico) e 0,022 (sistemático) mag na linha 205. A linha 272 dá 0,025 mag para o TRGB na âncora. As linhas 928–938 explicam que o sistemático comum das escalas TRGB/JAGB combina a distância de NGC 4258 com a medida de magnitude de cada método; a **Tabela 6, nota a**, identifica expressamente a incerteza de 1,5% da distância de NGC 4258 e a incerteza do TRGB. A linha 841 publica para o H₀ TRGB `70,39 ±1,22 (stat) ±1,33 (sys) ±0,70 (σ_SN)`.

**[DERIVED, dentro da caixa proposta]** O gerador R2 lê `n=√(0,024²+0,022²)` e `t=0,025` mag, e decompõe **o 1,33 já publicado** em `a₂N=1,33·n/√(n²+t²)=1,0548837955` e `a₂T=1,33·t/√(n²+t²)=0,8100124555` km s⁻¹ Mpc⁻¹. Assim `a₂N/70,39≈1,50%`, coerente com a nota a, e `√(a₂N²+a₂T²)=1,33`. São **tetos de sensibilidade** para termos cruzados da V2, não covariâncias conjuntas medidas. A diagonal `σ_CCHP²` já contém esse 1,33; somá-lo outra vez duplicaria o erro.

O rascunho R2 conserva essas amplitudes e resultados numéricos. Este adendo fornece a âncora de fonte que faltou citar literalmente no JSON/Markdown R2. A fonte e o modelo de caixa ainda exigem a reauditoria c1; nenhuma admissão D-H, dado real ou gate foi alterado.
