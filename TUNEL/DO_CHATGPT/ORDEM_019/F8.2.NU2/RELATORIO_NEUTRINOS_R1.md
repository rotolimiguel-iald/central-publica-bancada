# Neutrinos, luminosidade bolométrica e escala v388 — exame delimitado

09/10/2026 · codex-gerente-tgl · unidade F8.2.NU2, reivindicação 618.

## Resultado

[REAL/DERIVED] O operador espectral e os controles sintéticos foram calculados e reproduzidos independentemente. Não foi calculada significância observada, nem um funcional físico TGL que determine simultaneamente emissão de neutrinos, luminosidade e massa de uma Ia. A capacidade de 5σ deste teste permanece [OPEN]. O exame de compatibilidade da Bancada, solicitado depois, está em F0.3.B1; estes cálculos são de sandbox e não foram executados pelo motor instalado da Bancada.

## Reaproveitamento e escala correta

Consulta F7.2: canal n=-2, dez fontes e limites publicados já existem; não foram reconstruídos. F8.2.SN1 fornece a sensibilidade Coulomb da EOS fria e a conservação de energia para desfasamento com H fixo. Os inventários locais desta unidade registram fontes, linhas e hashes.

[REAL — leitura de fonte] O um.py consultado é v391. A Ponte Einstein Cartan Miguel.tex:1367–1371 e um.py:165419–165421 mantêm β do desfasamento independente da frequência. TheCouplingRunsBoundedBelow.lean:22–26 distingue β₀ da fronteira e β(χ) do bulk. O Atlas:35126 registra que na lei de desfasamento entra β₀. Portanto a fórmula com β(E) discutida antes nesta conversa é uma extensão condicional, não a previsão vigente desse canal. β₀ foi calculado em runtime a partir de ALPHA_FINE_CODATA_2018 lido por regex do programa, sem executar ou importar o um.py. τ★ é [INPUT]; Kfac=1 é hipótese, e o K desse fator histórico é Kretschmann, não K∂ modular.

## O que o operador efetivamente faz

Para H fixo e a≥0, dρ/dt=−i[H,ρ]−a[H,[H,ρ]]. Na base de energia, a dissipação suprime os termos fora da diagonal; mantém populações, traço e energia média. Se ρ já é diagonal, [H,ρ]=0 e o desfasamento adicional é exatamente nulo, qualquer que seja a taxa. Isto não prova ausência de efeito na produção ou em matéria variável: aí é preciso definir H(x), a base do dissipador e as taxas fracas.

[KNOWN — modelo publicado] Wright et al., §IV.1, Eq.(10), tratam os neutrinos da Ia na Terra como estados já decoerentes na base de massa. A previsão de sinal citada é de um modelo de explosão, não uma amostra observada de neutrinos de Ia. https://arxiv.org/html/1605.01408v2

[DERIVED] Para dissipador proporcional a H, Γij∝(Δm²ij/E)². Nos valores de referência declarados no plano, Γ21:Γ31:Γ32 = 1:1111,111…:1045,444…. O limite JUNO 4,1×10⁻²⁷ GeV a 90% CL é de outra textura, Γ21=Γ31, Γ32=0, e não pode ser transferido diretamente. Fonte: Beccaria–Ternes, Eq.(13)/Tabela I, https://arxiv.org/html/2606.13362v1 .

## Controles numéricos, sem dado observado

[REAL — cálculo condicional] Para τ★=tP, Kfac=1, β₀ fixo, vácuo, 52,5 km e energias de 2 a 8 MeV, max|ΔP|=1,7880671599537207×10⁻³⁹. Um experimento ideal de fluxo plano, sem resolução nem fundo, com normalização perfilada, dá exposição formal não oscilada N=8,632408517595953×10⁷⁹ para distância estatística nominal 5. Isto não é poder do JUNO real, nem cota universal sobre toda a TGL: a normalização τ★ e o matching permanecem abertos.

A implementação preserva o efeito minúsculo com expm1; subtrair probabilidades float64 arredondaria para zero. Um segundo cálculo, Decimal com 95 dígitos, reproduziu N com diferença relativa 1,20×10⁻¹⁴. O teste de estado diagonal é nulo por álgebra, distinto desse efeito minúsculo em estado coerente. A revisão independente está em review/REVIEW_R1.md e cobre os cálculos e inventários enumerados; não revisou este relatório, escrito posteriormente.

[CONJECTURE — cenário contrafactual] A substituição β→β(χ(E)) foi mantida separada. Com τ★ e Kfac fixos, a cota abstrata √e/β₀≈137 só multiplica a taxa por cerca de duas ordens. Não é matching físico; o contrato físico de acoplamento ainda restringe β<1. Quando Kfac=r^β também varia, a derivada completa é n_eff=−2+dlnτ★/dlnE+β′(1/β+ln r)+β dlnr/dlnE. Ela foi conferida por diferenças finitas em funções sintéticas, sem escolher χ(E) a partir dos dados.

## Dados públicos: o que existe

O inventário data_inventory distingue metadados consultados de bytes custodiados. Há releases oficiais KamLAND com espectros/eventos e grades de oscilação padrão; a existência deles não entrega automaticamente uma verossimilhança para este dissipador. O primeiro artigo JUNO fornece source data/suplementos, mas declara dados brutos e código não públicos. O anúncio JUNO de setembro foi localizado; não foi localizado, no escopo examinado, um pacote numérico completo de resposta/covariância para reinterpretar esse canal. Nenhum dado de ajuste foi baixado ou composto nesta unidade.

Fontes: https://www.awa.tohoku.ac.jp/KamLAND/4th_result_data_release/4th_result_data_release.html ; https://www.nature.com/articles/s41586-026-10538-z ; https://arxiv.org/html/2609.37895v1 .

A análise SN1987A de arXiv:2503.04573 distingue perturbação de fase e perda de neutrinos. Seus limites fortes de perda não são limites do dissipador preservador de traço aqui considerado. Não se deve confundir SN1987A, de colapso do núcleo, com Ia. https://arxiv.org/html/2503.04573v1

## Caminho verificável para o teste proposto

1. Fixar a incidência física: propagação coerente em matéria ou alteração da emissão/captura na fonte. Uma alteração depois da emissão não modifica retroativamente Ye e a massa estelar.
2. Fornecer o operador, τ★, curvatura e escala, com unidades e fonte teórica; preservar o canal β₀ atual até eventual derivação/reconciliação.
3. Derivar a resposta conjunta de fluxo espectral, Ye/EOS e luminosidade. Massa inferida da mesma luminosidade não é uma segunda medida independente.
4. Só então aplicar resposta do detector, covariâncias, alternativas físicas e teste sintético de poder pré-fixado. Havendo poder, preparar teste sobre dados públicos na identidade correta.

A Bancada respondeu em tempo real e o canal F7.2 v2 devolveu SEM_LIMITE_TGL e mapping OPEN. Sua função atual é proveniência, não cálculo do espectro. A infraestrutura disponível não elimina os elos físicos acima. Não houve contato com Claude, provedor, modificação da Bancada, do Nós ou do gate.
