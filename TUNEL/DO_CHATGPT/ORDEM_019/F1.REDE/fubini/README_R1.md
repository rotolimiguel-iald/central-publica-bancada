# F1.REDE — ponte de Fubini L² vetorial, R1

[REAL — compilação local; revisão independente pendente] `FubiniL2.lean` constrói a equivalência, sem assumi-la como campo.
A aplicação é a seção f(q,r) ↦ (r ↦ [q ↦ f(q,r)]), totalizada por zero somente onde a seção não é L² (conjunto nulo provado).
Prova: mensurabilidade pelas distâncias; Fubini do quadrado da norma; linearidade no quociente; sobrejetividade por indicadores finitos e imagem fechada.
Hipóteses genéricas explícitas: medidas SFinite, medida transversal separável, fibra Hilbert real separável e completa, ação escalar normada.
A especialização `canonicalFub` habita o tipo exato `Lp Fib 2 momentumMeasure ≃ₗᵢ[ℂ] RapidityHilbert`; H1, Fib e a medida canônicos permanecem os mesmos.
`canonicalFub_sections` fixa a ação a.e.; `canonicalFub_shift` e `canonical_toRapidity_boost` provam o entrelaçamento, evitando uma identificação abstrata arbitrária.
`canonicalPartialFourier` é a composição efetiva da carta existente, Fubini e Fourier L² vetorial já disponível.
`canonicalPartialFourier_boost` dá o multiplicador 2πs; para B0(−2πt), `canonicalSigma ξ = 4π²ξ` e `canonical_modularGroupIsBoost` comprovam o sinal e a normalização.
[OPEN] J_W, T = Δ^(1/2), Δ = S†S, StandardSubspace e a rede completa não são construídos nesta etapa; nenhum habitante D1a3OutputBGL é reivindicado.
Build final: `attempts/20261013T213116_037514Z`; EXIT 0, 17 declarações impressas apenas com propext/Classical.choice/Quot.sound, zero sorry/admit/axioma novo na fonte.
`BUILD.log` traz comando, toolchain, LEAN_PATH literal, início, fim, segundos e exit; `RECEIPT.json` pina fonte, .olean, log e transcrito de axiomas.
`DELIVERY_R1.json` pina esta entrega, dependências lidas e todos os recibos de tentativa. Nenhum arquivo do Nós, produção, memória, quadro ou gate foi alterado; nenhuma junção foi criada.
