[DERIVED condicional; INPUT/CONJECTURE na identificação física; nenhuma leitura selecionada]

# Da taxa modular ao ringdown: tabela de leituras

21/09/2026. Complementa `C2_MAPEAMENTO_ANALITICO.md` e os oráculos C0–C3. Os números por evento são calculados por `catalog_220_readout.py`, sem literal de beta. O ramo legado v346 continua disponível com suas constantes próprias. O programa canônico permanece intacto.

## Objetos, relógios e unidades

Defina t_M=GM_f,det/c³, w(χ)=t_M ω_220, d(χ)=t_M/τ_GR, b=α_CODATA2018 sqrt(e), z o redshift. Massa da fonte M_src=M_det/(1+z); dt_det=(1+z)dt_src. Γ abaixo está em s⁻¹, ω em rad/s, t_M e τ★ em s, b e os autovalores modulares k são adimensionais. Uma taxa modular exige multiplicação por ds/dt; b isolado não define segundos.

Para L=f(K) autoadjunto, a taxa de uma coerência é (f(k_i)−f(k_j))²/2. Para L=sqrt(b)sqrt(K), ela é b(sqrt(k_i)−sqrt(k_j))²/2 por unidade de tempo modular. A equação mestre sozinha não identifica K com um modo de Kerr, nem determina o desenrolamento observado por um detector clássico.

**Convenção comum:** se o strain é a média coerente de ensemble e as taxas somam, x=Γτ_GR, δτ=−x/(1+x), δf=0. Potência coerente decai com 2Γ; energia total do oscilador é conservada pelo dephasing. Uma realização de fase e a média de ensemble são observáveis distintos.

| Leitura | Γ no detector; razão Γ/ω | Relógio e hipótese adicional | Escopo do teste |
|---|---|---|---|
| R-A | b(1+z)t_P ω²/2; b(1+z)t_P ω/2 | [INPUT] τ★,src=t_P; regressão v346 mantém seu relógio de detector | Ensemble quadrático; taxa local muito pequena em frequências de OG. Isso não decide sua aplicação universal a fótons. |
| R-B | b w²/(2t_M); b w/2 | [INPUT] τ★,src=GM_src/c³ | Γ escala como M_det⁻¹; δτ depende só de χ. É o ramo já calculado na v346, não um relógio novo derivado de beta. |
| R-MOD | πb(ω−2Ω_H)²/κ; πb(ω−2Ω_H)²/(κω) | [CONJECTURE] oscilador corrotante positivo em KMS e ds/dt=κ/(2π), lei quadrática em K | QNM exato obrigatório; construção finita abaixo prova a implicação sob essas hipóteses, não um estado global Hartle–Hawking em Kerr. |
| R-RAIZ-0 | bω/2; b/2 | [INPUT] K=τ★H/ħ, L=sqrt(b)sqrt(K), s=t/τ★, coerência 0↔1 | τ★ cancela; não representa automaticamente o campo coerente macroscópico. |
| R-RAIZ-EP4 | bω²/[2(sqrt(ω₀+ω)+sqrt(ω₀))²], ω₀=1/[4t_P(1+z)] | [INPUT] fundo E_P/4 na fonte | No regime ω≪ω₀ dá R-A. O fundo E_P, em vez de E_P/4, dá um quarto do coeficiente; errata v369 preservada. |
| R-RAIZ-REST | mesma função-raiz, ω₀=M_src c²/[ħ(1+z)] | [CONJECTURE] massa de repouso como fundo positivo | O deslocamento em K altera sqrt(K); não confundir com a invariância L→L+cI. |
| R-RAIZ-COHERENT | Γ_initial/ω≈b/(8N), N≫1 | [CONJECTURE] oscilador efetivo em estado coerente; N=E_mode/(ħω_src) | Soma de Poisson, geralmente não exponencial. O módulo recusa um Bayes factor de seno amortecido para esta leitura sem outra aproximação validada. N=10^78 é cenário, não energia medida. |
| R-LIN | bω; b | [CONJECTURE] ponte dimensional que fixa coeficiente 1 para uma lei de gap linear | Pode ser desenrolada por ruído de fase de Lévy/Cauchy; não pelo mesmo jitter browniano em H. Não coincide com R-RAIZ-0, cujo coeficiente é 1/2. |
| R-GLOBAL | Γ_rel=0 sob cancelamento comum | [CONDITIONAL] mesmo ruído de tempo em sistema e referência, observável relacional | Não é teorema de invisibilidade de toda interação gravitacional; depende da partição e do observável. |
| R-PROP | Xi=b τ★,src ω_obs²/2 ∫₀ᶻ(1+z')/H(z') dz' | [CONJECTURE] ruído local independente ao longo de FLRW | Atenuação da coerência espectral, não uma taxa adicional de ringdown de milissegundos. Requer modelo de cosmologia, referência e excitação. |

A distância de luminosidade entra na amplitude e no SNR. Não altera a taxa local do mesmo remanescente; relacioná-la ao redshift requer uma cosmologia. A amplitude absoluta requer energia/excitação, orientação e resposta do detector; M, χ e D sozinhos não a determinam. Usar o relógio da massa da fonte durante todo o percurso seria outra hipótese não local dependente da fonte.

## Realização finita da leitura modular e o que ela prova

Escolha um único modo efetivo com ν=ω−mΩ_H>0 e N≥0, e assuma

    ρ_KMS = Z⁻¹ exp[−(2π/κ)ν N],
    K = (2π/κ)ν N + log Z,
    ds/dt = κ/(2π),
    dρ/ds = −b[K,[K,ρ]]/2.

O oscilador tem Z finito porque ν>0. Uma truncagem finita tem um estado fiel e positivo. Para a coerência adjacente, Δk=(2π/κ)ν. Multiplicar a taxa modular b(Δk)²/2 pelo relógio κ/(2π) dá Γ=πbν²/κ. Isso é a leitura R-MOD. O teste usa κ=sqrt(1−χ²)/[2t_M(1+sqrt(1−χ²))] e Ω_H=χ/[2t_M(1+sqrt(1−χ²))].

**Duas escolhas distintas:** esta derivação usa L=sqrt(b)K. Se usarmos L=sqrt(b)sqrt(K), a mesma ponte dá taxas-raiz dependentes do fundo e da ocupação; com fundo zero e 0↔1 dá bν/2, não πbν²/κ. O fundo log Z pode sair do duplo comutador de K, mas não sair gratuitamente de sqrt(K). Portanto não se pode converter a raiz em lei quadrática apenas trocando o nome do gerador.

A realização acima não prova que o estado físico regional de Kerr seja esse oscilador KMS, nem fornece uma quantização autoadjunta de um QNM dissipativo. São precisamente as hipóteses que tornam a previsão condicional. O teorema de Kay–Wald trata estados regulares estacionários sob suas condições globais; não proíbe todo estado em uma região externa. O abstract autoral foi consultado; o texto integral não foi obtido nesta rodada. [Fonte autoral](https://pure.york.ac.uk/portal/en/publications/theorems-on-the-uniqueness-and-thermal-properties-of-stationary-n/).

## Jitter gaussiano não é automaticamente o modelo de saltos de tempo exato

A lei quadrática admite o desenrolamento browniano de C2. Um outro processo, de saltos unitários Poisson, tem gerador r(UρU†−ρ), U=exp(−iεH/ħ), taxas r[1−cos(εν)] e correção de fase r sin(εν). Só para |εν|≪1 sua taxa é rε²ν²/2. A identificação rε²=bτ★ não determina r e ε separadamente. Logo a fórmula quadrática da TGL pode ser tomada como seu gerador, mas não se deve alegar que é o processo de Milburn exato para gaps arbitrários. [Milburn, abstract consultado](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.44.5401).

## Confrontos já registrados pela v369: conservar a partição

O artefato `cache/casa/um_absoluto.json`, `core.clock_test_result_v369`, registra `MODULAR_LAB_BRIDGE_OPEN`. Sua P1 é `NOT_FALSIFIED_UNDERPOWERED`, P2 `EXCLUDED_IN_READING`, P3 `NO_LOCAL_OBSERVABLE`. Portanto a leitura planckiana não recebe um veredito universal apenas por ficar invisível no ringdown: a aplicação à luz e a composição do ruído são parte da hipótese.

No teste atômico registrado, as leituras-raiz de fundo zero e massa de repouso foram excluídas condicionalmente. Isso não autoriza transplantar o número atômico para OG sem a hipótese de universalidade. Os relógios de Unruh terrestre e da massa da Terra também foram excluídos naquela leitura; o da massa do átomo ficou invisível. FP-5 não transforma α ou beta em segundos; também não impede uma previsão condicional que use massa e spin medidos de Kerr.

## Condições necessárias para um resultado observacional

Os posteriores pSEOB tratam desvios de frequências e amortecimentos do sinal clássico. Compará-los à expressão δτ acima testa a identificação com o ensemble. R-RAIZ-COHERENT e R-PROP não ganham artificialmente um número nesse mesmo teste. O ramo global tem B=1 se as hipóteses produzirem exatamente a mesma distribuição observável; isso não é confirmação.

Uma soma de ln B por evento só vale para hipóteses compatíveis e dados independentes. O catálogo atual contém produtos com tratamento diferente dos modos superiores: o GW250114 deixa o 440 livre; os demais fixam suas deformações a RG. Os resultados de `C4_CATALOG_220.json` são explicitamente de setor 220, não de toda a TGL. A seleção publicada de 31 eventos é reportada junto ao controle com os 33 arquivos disponíveis. Nenhum Bayes factor vira sigma por renomeação.

## O que permanece aberto

A identificação física da partição, relógio e observável; recuperação de trajetórias com ruído colorido; modos superiores e robustez do remanescente; strain com registro próprio; pacote final reproduzido. Os teoremas do kernel permanecem com seus enunciados e hipóteses. Esta tabela não os reescreve nem move o gate.
