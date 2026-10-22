[REAL no controle condicional; desenrolamento físico OPEN] 2026-09-22T17:33:39.948879+00:00

# C2 — uma realização e a distribuição do estimador

**O detector registra UMA realização; o desenrolamento que a produz é [OPEN]; a C4/C6 desta ordem cobriram só o ensemble.** A Parte B tratará a largura populacional de δf̂ como observável separado, sujeito a transferência e calibração; esta tabela não é teste da natureza.

Foram ajustadas 1000 trajetórias por célula, em 11 cenários de leitura/ocupação e dois regimes de ruído. A execução levou 173.514 s em uma thread. Todas as trajetórias e ajustes estão no JSON; valores nas bordas são mantidos.

O ensaio usa Mdet=68,1 M☉, χ=0,68, SNR da portadora RG=20 e fase 0,37, em um canal H1 ilustrativo. São 128 amostras a 2048 Hz (62,5 ms), o dobro da janela temporal da v1 a 4096 Hz. O ajuste reaproveita o projetor variável de amplitude/fase, δf∈[−0,5;0,5], log(τ/τRG)∈[−2;2] e três pontos iniciais. A janela e a PSD foram explicitadas; os resultados não devem ser subtraídos da v1 como se apenas N tivesse mudado.

O ruído vem dos 256 intervalos fora da fonte de C5_RECOLORED_NOISE, transportados à PSD de referência O4 pela convenção arquivada. São mil sorteios com reposição dessa biblioteca finita, não mil intervalos de ruído independentes nem uma nova PSD medida O4. Os erros padrão ruidosos usam somas da função de influência agrupadas pelo intervalo original; não incluem incerteza da PSD, dependência entre intervalos ou erro de modelo. Sem ruído, os erros padrão são de Monte Carlo IID. A aproximação de influência para o desvio padrão é assintótica.

| Leitura / ocupação | Ruído | média δτ̂ ± EP | dp(δf̂) ± EP | bordas / falhas |
|---|---|---:|---:|---:|
| R-A | sem ruído | 0 ± 0 | 0 ± 0 | 0 / 0 |
| R-A | recolorido | -0.002405633 ± 0.00633 | 0.01830327 ± 0.000913 | 0 / 0 |
| R-B | sem ruído | -0.007781444 ± 0.000734 | 0.02265017 ± 0.000489 | 0 / 0 |
| R-B | recolorido | -0.009530389 ± 0.00615 | 0.02960258 ± 0.000895 | 0 / 0 |
| R-RAIZ-0 | sem ruído | -0.01409408 ± 0.00102 | 0.0314385 ± 0.000682 | 0 / 0 |
| R-RAIZ-0 | recolorido | -0.01545058 ± 0.00608 | 0.03730085 ± 0.00108 | 0 / 0 |
| R-RAIZ-EP4 | sem ruído | 0 ± 0 | 0 ± 0 | 0 / 0 |
| R-RAIZ-EP4 | recolorido | -0.002405633 ± 0.00633 | 0.01830327 ± 0.000913 | 0 / 0 |
| R-RAIZ-REST | sem ruído | 0 ± 0 | 0 ± 0 | 0 / 0 |
| R-RAIZ-REST | recolorido | -0.002405633 ± 0.00633 | 0.01830327 ± 0.000913 | 0 / 0 |
| R-LIN | sem ruído | -0.02473012 ± 0.00251 | 0.05885961 ± 0.00529 | 4 / 0 |
| R-LIN | recolorido | -0.02454503 ± 0.00644 | 0.0604545 ± 0.00455 | 3 / 0 |
| R-MOD | sem ruído | -0.0138133 ± 0.00101 | 0.03109513 ± 0.000675 | 0 / 0 |
| R-MOD | recolorido | -0.013192 ± 0.00605 | 0.03678051 ± 0.00107 | 0 / 0 |
| R-GLOBAL | sem ruído | 0 ± 0 | 0 ± 0 | 0 / 0 |
| R-GLOBAL | recolorido | -0.002405633 ± 0.00633 | 0.01830327 ± 0.000913 | 0 / 0 |
| R-RAIZ-COHERENT N=4 | sem ruído | -0.001844262 ± 0.000267 | 0.008258664 ± 0.000178 | 0 / 0 |
| R-RAIZ-COHERENT N=4 | recolorido | -0.004106894 ± 0.00627 | 0.02015319 ± 0.000866 | 0 / 0 |
| R-RAIZ-COHERENT N=64 | sem ruído | -0.0001433621 ± 6.23e-05 | 0.001939018 ± 4.18e-05 | 0 / 0 |
| R-RAIZ-COHERENT N=64 | recolorido | -0.002526799 ± 0.00632 | 0.01839919 ± 0.000913 | 0 / 0 |
| R-RAIZ-COHERENT N=256 | sem ruído | -5.866093e-05 ± 3.11e-05 | 0.0009680002 ± 2.09e-05 | 0 / 0 |
| R-RAIZ-COHERENT N=256 | recolorido | -0.002454255 ± 0.00632 | 0.01832388 ± 0.000914 | 0 / 0 |

Os zeros ajustados das leituras de efeito minúsculo são resolução numérica do estimador; não anulam suas taxas analíticas. Em R-LIN, o processo é Cauchy: sua fase não tem variância. A dispersão tabelada pertence ao estimador limitado, que atingiu bordas; não é uma variância da fase nem demonstra normalidade.

## Perda do filtro casado

A perda abaixo é 1−||projeção na base seno/cosseno RG||/||sinal limpo||, com frequência e amortecimento RG fixos e fase/amplitude maximizadas. É perda fracional de SNR frente ao filtro ótimo do sinal, não perda de energia. Resíduos negativos de ordem 10⁻¹⁶ são arredondamento e foram preservados.

| Leitura / ocupação | Perda média fracional de SNR |
|---|---:|
| R-A | -2.22044605e-16 |
| R-B | 0.00368464873 |
| R-RAIZ-0 | 0.00700460408 |
| R-RAIZ-EP4 | -2.22044605e-16 |
| R-RAIZ-REST | -2.22044605e-16 |
| R-LIN | 0.0155130378 |
| R-MOD | 0.00690800428 |
| R-GLOBAL | -2.22044605e-16 |
| R-RAIZ-COHERENT N=4 | 0.00049594675 |
| R-RAIZ-COHERENT N=64 | 2.73792154e-05 |
| R-RAIZ-COHERENT N=256 | 6.8238972e-06 |

Wiener e Cauchy de fase preservam o módulo da portadora em cada trajetória, mas a média coerente decai. No ramo coerente, o fator é uma média quântica condicional ⟨a⟩ com soma de Poisson e um Wiener comum; |⟨a⟩|² não é a energia do oscilador. N=4,64,256 são cenários ilustrativos, sem lei distância→ocupação. O gerador GKSL sozinho não seleciona nenhum desses readouts clássicos.

R-PROP é expoente acumulado de propagação e não fornece, no módulo atual, um processo temporal local único de ringdown. Não se inventou sua célula estocástica; essa conversão permanece NÃO PAGA. R-GLOBAL fornece o controle nulo relacional sob sua hipótese. Os demais ramos têm seus processos nomeados no JSON.

## Reprodução e custódia

`wsl -e /opt/lal_env/bin/python -B "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/measure_c2_013bis.py" --n 1000 --tag expanded_1000`
O comando recusa resultado existente; uma repetição usa tag nova e preserva a saída anterior. Não há PE, acesso a strain da fonte ou alteração dos resultados C4/C6.

JSON de resultados SHA256 9d734d976146188ae83a9557ae947f1021c7cfef26c49e998f39b1c1a128d691. Código SHA256 b63a79f428e3c40b4c5e8dacbbcfdc4c762e994ce0cb2850611bba21c948cd3a.
C2_TRAJECTORY_RECOVERY.json anterior SHA256 339be42bec67a48e1e3341d678ac9bc0804c6e1db035e6b4b57df62673eafd38; intacto. C5_RECOLORED_NOISE.json SHA256 088fe6927b17e8461df6a05c0d129da28654cf001e3833df24713cfe0d3ec477.
Abertura do operador SHA256 0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0.

PAGO: ampliação condicional, médias/dispersões com EP, ruído fora da fonte recolorido e perda do filtro. NÃO PAGO: identificação do desenrolamento físico, calibração IMR/duas famílias, transferência ao posterior de eventos e conversão R-PROP. Nenhum gate alterado. Tentativa benchmark preservada em bis/C2_TRAJECTORY_benchmark.json; não houve falha de execução nesta ampliação. Axiomas: N/A — sem Lean.
