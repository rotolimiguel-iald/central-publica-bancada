[REAL — auditoria independente de código, artefatos e cálculos leves; 22/09/2026] **CONTROLE NUMÉRICO CONDICIONAL ACEITO; CORREÇÃO DOCUMENTAL NECESSÁRIA.** As estatísticas das 22 células conferem. A PSD, a projeção, a janela e os fits selecionados não apresentaram defeito numérico relevante. Existe uma afirmação documental inexata: o JSON guarda todos os ajustes, mas não todas as séries das trajetórias. A integração efetiva da largura populacional na Parte B não está demonstrada pelos artefatos examinados. Não dar aceite irrestrito a F1 nem converter essas pendências em sucesso.

C0 já estava encerrado por parecer separado, sem defeito bloqueante novo, com suas lacunas explícitas. Esta auditoria não construiu C2, não alterou seus artefatos e não aprova os demais componentes de F1/M1. Skill tgl-atlas e protocolo do túnel observados no alcance autorizado; fontes e memórias permaneceram somente leitura. Nenhum gate alterado. Axiomas: N/A — sem Lean.

## 1. Achados e decisão

### C2-A01 — CORRIGIR, documental, prioridade 2: trajetórias não estão integralmente no JSON

Em [C2_ADENDO_OBSERVAVEL.md:7](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C2_ADENDO_OBSERVAVEL.md:7>) consta: “Todas as trajetórias e ajustes estão no JSON”. O builder repete a frase em [refeito/record_c2_013bis.py:30](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/record_c2_013bis.py:30>).

**Evidência:** cada registro de fit tem somente `df`, `dtau`, `optimizer_success`, `cost` e `boundary`. Há semente, índices de ruído, GPS e hashes; não há vetores Wiener/Cauchy, fatores de fase, sinais limpos/ruidosos nem perdas individuais de SNR. O código os calcula em memória e grava apenas os fits e resumos: `measure_c2_013bis.py:122–139,144–158`. A inspeção completa do schema e dos 22.000 registros está em `c2_review/statistics.json`.

**Correção concreta para o construtor, sem nova simulação:** substituir a frase por “Todos os ajustes individuais estão no JSON; as séries das trajetórias não foram arquivadas. Sua regeneração usa a semente, os índices de ruído, os insumos e o código identificados por hash, em ambiente numérico compatível”. A reprodução exata depende também das bibliotecas; o JSON original não registra suas versões. O runtime usado pelo revisor consta de `c2_review/numerics.json` e não certifica retrospectivamente o runtime original.

Os 22.000 fits existem; a frase incorreta não invalida as estatísticas. Exige errata antes de declarar o adendo documentalmente sem ressalvas. Nenhuma correção foi aplicada pelo revisor.

### C2-A02 — NÃO VERIFICADO: execução da integração na Parte B

[C2_ADENDO_OBSERVAVEL.md:5](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C2_ADENDO_OBSERVAVEL.md:5>) diz “A Parte B tratará a largura populacional”. Isso atende à identificação explícita do observável e anuncia o encaminhamento exigido por F1/C2, mas não prova implementação, calibração ou uso na Parte B. Não foi auditado outro produto da Parte B neste recorte. Esse item continua **encaminhamento documental presente / integração efetiva não verificada**, e não PAGO experimentalmente.

### C2-A03 — limites preservados, sem novo defeito bloqueante

O agrupamento do ruído é corretamente declarado; os EP não são calibração de cobertura. Os mesmos processos básicos e índices são reutilizados entre leituras e entre pares sem/com ruído (`measure_c2_013bis.py:85–88,125–134`): comparações entre células são pareadas, não independentes. Isso não invalida cada EP marginal, mas impede combinar os erros de diferenças como se as células fossem independentes.

A biblioteca recolorida não tem covariância empírica exatamente igual à PSD de referência. Na janela curta, medi `mean(||W y||²/125)=0,9086917639120484` sobre os 256 intervalos H1. Trata-se de diagnóstico da biblioteca finita, não teste independente de estacionariedade nem significância calibrada. O código não a renormaliza silenciosamente. Portanto, SNR=20 é a norma da portadora RG **na métrica de referência adotada**, não uma medição nova de SNR de evento.

## 2. Cobertura do pedido F1/C2

Fonte contratual: [ORDEM_013BIS:74](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:74>), complementada pela aceitação geral na linha 77. Auditoria de origem relida: `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/auditoria_da_gerencia/aud_1_C0_C1_C2.txt:128–136,170–172`.

| Exigência | Resultado desta auditoria |
|---|---|
| Detector registra UMA realização; desenrolamento físico OPEN; C4/C6 cobriram ensemble | ATENDIDA literalmente no adendo:5 e com escopo coerente no JSON. |
| Largura de δf̂ como observável populacional na Parte B | ENCAMINHAMENTO DOCUMENTADO; implementação e transferência não verificadas. Ver C2-A02. |
| N≥1000 por célula sem ruído e repetição com ruído recolorido | ATENDIDA para a grade declarada: 11 cenários × 2 regimes × 1000 fits = 22.000. Não são 22.000 processos-base mutuamente independentes. |
| Ruído C5_RECOLORED_NOISE, PSD fora da fonte e convenção explícita | ATENDIDA no controle condicional: biblioteca H1 de 256 intervalos, 251 usados nos 1000 sorteios; transporte à curva O4 de referência. Não é uma nova PSD O4 medida nem 1000 intervalos novos. |
| Média δτ̂ e dp(δf̂) com EP | ATENDIDA: todas as 22 células, quantis, flags e linhas impressas recalculados independentemente. |
| Perda de SNR de filtro casado no texto | ATENDIDA: 11 médias impressas; fórmula e geometria verificadas. Transporte das 11 médias confere; não refiz a média sobre todas as trajetórias. |
| Janela/PSD e comparação honesta com v1 | ATENDIDA: 128/2048 é explicitado, diferente de 128/4096 e da covariância OU antiga. Não é estudo isolado do aumento de N. |
| Adendo ao lado, ficha, hash e reprodução | PRESENTES e hashes conferem. A frase sobre armazenamento das trajetórias necessita correção C2-A01. A v1 atual tem o SHA fixado no adendo. |
| Nenhuma leitura física escolhida | ATENDIDA: R-PROP sem processo local inventado e NÃO PAGO; R-GLOBAL nulo sob hipótese; ocupações ilustrativas. Não há seleção física a partir dos resultados. |
| F1 completo e entrega M1 | FORA DE ESCOPO; este parecer não os certifica. |

## 3. Estatísticas recalculadas sem importar os builders

`c2_review/review_statistics.py` usa apenas a biblioteca padrão do Python. Calcula média com soma estável, desvio amostral com denominador n−1, quantis por interpolação linear, EP e flags a partir dos registros individuais. Não chama `summarize`, `fit` ou qualquer módulo do construtor.

**Resultados:** 22/22 linhas estatísticas do adendo conferem; 22.000/22.000 registros têm parâmetros finitos, custos não negativos, limites respeitados e flags de borda consistentes. Zero falhas de otimizador declaradas. A maior diferença absoluta entre estatística recalculada e JSON foi **6,938893903907228×10⁻¹⁸**. Quantis 5/50/95 e média de δf̂ também conferem.

Alguns números reobtidos (EP são os da convenção registrada, sem interpretação automática como intervalos de cobertura):

| Leitura | Ruído | média δτ̂ ± EP | dp(δf̂) ± EP |
|---|---|---:|---:|
| R-B | sem | −0,00778144412 ± 0,000733591262 | 0,0226501737 ± 0,000489096271 |
| R-B | recolorido | −0,00953038935 ± 0,00614971440 | 0,0296025795 ± 0,000894927789 |
| R-RAIZ-0 | sem | −0,0140940751 ± 0,00102444446 | 0,0314384973 ± 0,000682380097 |
| R-RAIZ-0 | recolorido | −0,0154505763 ± 0,00607545909 | 0,0373008491 ± 0,00108421890 |
| R-LIN | sem | −0,0247301236 ± 0,00250754614 | 0,0588596074 ± 0,00528544136 |
| R-LIN | recolorido | −0,0245450281 ± 0,00644082956 | 0,0604544963 ± 0,00455251009 |
| R-MOD | sem | −0,0138133040 ± 0,00101462787 | 0,0310951263 ± 0,000674796103 |
| R-MOD | recolorido | −0,0131919974 ± 0,00604999225 | 0,0367805132 ± 0,00106645951 |

Todas as outras células, incluindo as três ocupações coerentes, estão no recibo independente `c2_review/statistics.json`.

### EP e suporte empírico

Fonte: [measure_c2_013bis.py:34](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/measure_c2_013bis.py:34>). Para a média, ψᵢ=yᵢ−ȳ. Para o desvio padrão, ψᵢ=[(xᵢ−x̄)²−m₂]/(2s). Sem ruído usa-se sd(ψ)/√n. Com ruído, com G grupos usados:

`EP = sqrt[G/(G−1) × Σ_g(Σ_{i∈g} ψᵢ)²] / n`.

Reobtive **G=251**, repetições por grupo entre 1 e 11; cinco índices da biblioteca não aparecem: 74,78,105,184,212. Os GPS da biblioteca são distintos, com passo de 8 s. Esse passo não demonstra independência física de intervalos.

A função de influência do desvio é assintótica, como diz o adendo:11. Se se desejasse a derivada finita da estatística com correção n−1, apareceria o fator n/(n−1)=1000/999, diferença de aproximadamente 0,1001%; sua omissão não é defeito oculto diante do estatuto assintótico declarado. A fórmula não inclui incerteza de PSD, dependência entre janelas ou erro de modelo, tampouco os erros-padrão entre leituras são independentes.

Há **4 bordas sem ruído** em R-LIN, índices de base zero 149,284,596,766, e **3 com ruído**, 149,284,766. Estão retidas. Não há descarte seletivo para tornar finita uma variância de fase: a fase Cauchy não tem variância; o estimador δf̂ está limitado a [−0,5;0,5] e tem dispersão amostral calculável. Normalidade e validade de uma extrapolação de cauda a 5σ não foram demonstradas.

## 4. PSD, projeção, janela e filtro casado

Fontes primárias locais lidas: [prepare_empirical_noise.py:21–53](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/prepare_empirical_noise.py:21>), [prepare_recolored_noise.py:22–39](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/prepare_recolored_noise.py:22>), o transporte nas linhas 50–76, e [measure_c2_013bis.py:71–83](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/measure_c2_013bis.py:71>).

O argumento `4096` passado ao whitener **não é um erro de fator dois**. A PSD original vai até 2048 Hz; o `stride=2` integra essa PSD nos tempos efetivamente retidos a 2048 amostras/s, incluindo aliasing. São 128 amostras, t₀=0, t₁₂₇=0,06201171875 s; a duração nominal N/fs é 0,0625 s. Usar esta última como duração de janela é a convenção registrada, não confusão sobre o instante da última amostra.

O projetor elimina polinômios de grau até 2 no intervalo truncado: 128 coordenadas → 125 dimensões. Dados e templates recebem o mesmo operador W. Não há filtro temporal lendo amostras externas à janela nesta operação. A PSD deriva de uma curva de referência, com continuação f⁻⁴ abaixo de 10,21659 Hz e DC anulado pelo quociente, conforme os metadados C5; não foi inferida novamente da biblioteca.

Em `review_numerics.py`, construí outro complemento por SVD e a covariância por soma explícita de cossenos/senos, sem usar a FFT do construtor. A função original do whitener foi extraída por AST e executada isoladamente somente para comparação; nenhum módulo do projeto foi importado.

| Checagem independente | Valor |
|---|---:|
| Anulação dos três polinômios | 6,66×10⁻¹⁶ |
| Erro de ortonormalidade do complemento | 6,66×10⁻¹⁶ |
| Resíduo de whitening independente | 4,02×10⁻¹³ |
| Resíduo do algoritmo registrado, reobtido exatamente | 1,7431680845147797×10⁻¹² |
| Diferença relativa da covariância, quadratura direta × FFT | 5,87×10⁻¹⁵ |
| Diferença relativa da métrica WᵀW | 1,13×10⁻¹² |
| Covariância longa recolorida, restrita e reprojetada × curta | 9,92×10⁻¹⁴ |
| Resíduo dessa covariância após whitening curto | 7,35×10⁻¹¹ |
| PSD reconstruída da curva ASD, maior diferença relativa | 1,44×10⁻¹⁴ |

O teste da covariância longa é relevante: a biblioteca tinha 410 amostras e a bancada tomou as primeiras 128. Restringir um polinômio de grau 2 continua dando polinômio de grau 2, removido pelo novo projetor. A congruência entre as covariâncias foi verificada; não há incompatibilidade de janela disfarçada por um simples resíduo de Cholesky.

O filtro fixo RG usa o subespaço seno/cosseno e a perda `1−||Proj_GR(Ws)||/||Ws||`. Isso é perda fracional de SNR, maximizando amplitude/fase, na métrica e no espaço projetado adotados. Não é perda de energia, nem substitui a otimização de frequência/amortecimento. A geometria foi checada também por SVD e identidade de Pitágoras; resíduo máximo nos casos selecionados 7,80×10⁻¹³. Perdas negativas da ordem de 10⁻¹⁶ são arredondamento.

As 11 médias no adendo coincidem com o JSON, inclusive R-B 0,00368464873, R-LIN 0,0155130378 e coerente N=256 6,8238972×10⁻⁶. **Não reobtive independentemente as 11 médias completas**, pois as perdas por trajetória não estão arquivadas e não executei o ensaio inteiro. Verifiquei a fórmula, seu transporte ao texto e projeções selecionadas.

## 5. Fits selecionados e processos

Fonte do estimador: [trajectory_recovery.py:25–38](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/trajectory_recovery.py:25>). O algoritmo usa projeção variável linear em seno/cosseno e mínimos quadrados não lineares em δf e log(τ/τRG), três inícios, limites explícitos. Um flag `optimizer_success=True` significa convergência reportada, não prova de mínimo global.

Regenerar os vetores básicos de RNG exigiu somente 1000×128 normais e Cauchy, sem ajustar a grade. Os 1000 índices de ruído regenerados coincidem exatamente com o JSON. Reconstruí **15 realizações selecionadas** (índice 0 dos 11 cenários e os quatro casos Cauchy de borda), verificando **30 custos** com/sem ruído. Maior discrepância absoluta no custo: **2,97×10⁻¹¹**.

Reotimizei somente **11 fits**: as sete ocorrências de borda, R-B índice 0 com/sem ruído, R-MOD índice 0 ruidoso e coerente N=4 índice 0 limpo. Usei projeção por QR em métrica independente, cinco inícios alternativos e o ponto registrado, tolerâncias mais estritas. A maior melhoria de custo foi **1,56×10⁻⁸**, em custo ≈88,2; maior mudança de δτ̂ ≈1,19×10⁻⁵ nesse caso de borda e maior mudança de δf̂ ≈4,59×10⁻⁸. Não apareceu mínimo alternativo materialmente melhor nessa amostra. Não afirmo auditoria global dos 22.000 ótimos.

As médias de ensemble foram conferidas pela fórmula −Γτ/(1+Γτ): R-B −0,0199042765940, R-RAIZ-0 −0,0371294625345, R-LIN −0,0716004392427 e R-MOD −0,0365992516184. A média dos fits de realizações difere disso, como o adendo corretamente explica. R-MOD usa o mesmo QNM exato interpolado para portadora, τ e co-rotação; não houve mistura com a referência BCW nesse cenário.

R-A/EP4 têm efeito analítico ≈−3,264×10⁻⁴² neste cenário; REST ≈−1,312×10⁻⁸². Zeros numéricos dos fits são sub-resolução, não taxas nulas. R-GLOBAL é nulo por hipótese.

Em Wiener/Cauchy, o fator de fase tem módulo unitário; isso não diz que a quadratura real ao quadrado é constante. No ramo coerente, o fator é soma de Poisson com um Wiener compartilhado, isto é, uma média quântica condicional; seu módulo pode mudar sem perda de número do oscilador. A soma foi conferida independentemente por `scipy.stats.poisson.pmf`, em vez da recorrência do construtor. Caudas omitidas nos suportes arquivados: aproximadamente 2,78×10⁻²⁸ (N=4), 9,67×10⁻²⁰ (N=64) e 1,55×10⁻¹⁷ (N=256), abaixo do limite declarado 10⁻¹³. Não há lei distância→ocupação demonstrada.

## 6. Custódia, reprodução e limites de leitura

Os **8/8 hashes** do mapa `sources` do ensaio conferem. Também conferem o fonte de recoloração e a curva O4 contra seus recibos. Os **5/5 hashes escritos no adendo** e **3/3 na ficha** foram cruzados com os bytes. Os 17 arquivos do inventário completo e seus tamanhos estão em `c2_review/statistics.json`. A checagem de hash não significa leitura integral de todos eles.

| Artefato auditado | Bytes | SHA-256 calculado |
|---|---:|---|
| refeito/measure_c2_013bis.py | 9106 | `b63a79f428e3c40b4c5e8dacbbcfdc4c762e994ce0cb2850611bba21c948cd3a` |
| refeito/record_c2_013bis.py | 7785 | `cc740de885bf70a0896169e1f027e69cb00539485d420fec0b397c1c4608e222` |
| bis/C2_TRAJECTORY_expanded_1000.json | 4681894 | `9d734d976146188ae83a9557ae947f1021c7cfef26c49e998f39b1c1a128d691` |
| C2_ADENDO_OBSERVAVEL.md | 6666 | `5f6cc6bee61233c1476c1008054fb15aba20082484d72144de183e852ad35812` |
| REAPROVEITAMENTO_C2.md | 952 | `d0d7fdbaa6c36d3a465e568dc0854cab07b7ace88f44091967807299cbe7a655` |
| C2_TRAJECTORY_RECOVERY.json, v1 | 271259 | `339be42bec67a48e1e3341d678ac9bc0804c6e1db035e6b4b57df62673eafd38` |
| C5_RECOLORED_NOISE.json | 9309 | `088fe6927b17e8461df6a05c0d129da28654cf001e3833df24713cfe0d3ec477` |
| cache/recolored_noise/O4_noise.npz | 6788886 | `03aa894405014ac2599ffa760b9b14d10410a68f60a962625dc4eaf4bffcd528` |

Os builders recusam destinos existentes e usam temporário exclusivo, conferência de bytes e substituição (`measure_c2_013bis.py:24–32`; `record_c2_013bis.py:7–12`). Foram apenas lidos. O tempo original **173,513988044 s** é lido do JSON, não cronometrado novamente; a configuração de uma thread é sustentada pelos limites de OMP/OpenBLAS no código, sem auditoria retrospectiva de threads do processo original. O benchmark foi preservado e hashado, sem reexecução; “não houve falha” é a declaração de origem, não uma busca exaustiva por logs.

Comandos leves efetivamente executados (os recibos recusam sobrescrita; não repetir sobre saídas existentes):

```powershell
python -B -X utf8 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c2_review\review_statistics.py'
wsl -e /opt/lal_env/bin/python -B '/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/c2_review/review_numerics.py'
```

A etapa numérica limitada levou aproximadamente 1,025 s no relógio interno do script. O WSL inicialmente recusou acesso no sandbox; a mesma auditoria limitada foi depois executada com a permissão revisada pela ferramenta. Nenhum contorno do escopo foi usado.

**Não feito/não lido:** nenhum ensaio completo, PE, nova cadeia, dado on-source, nova estimação da PSD, nova solução QNM, compilação Lean, construção de readout físico, calibração IMR ou edição canônica. O HDF5 primário fora da fonte não foi reaberto: sua proveniência foi lida no recibo C5, não revalidada desde os samples brutos. A curva ASD local e os arrays recoloridos foram efetivamente lidos. Não houve consulta web; não foi necessária nova fonte teórica para os cálculos finitos aqui auditados. Os artigos físicos não foram relidos e não recebem nova certificação.

**Arquivos escritos nesta auditoria, e somente estes:**

1. `bis/C2_ADVERSARIAL_REVIEW.md` — este parecer.
2. `bis/c2_review/review_statistics.py` — redução independente de todos os fits.
3. `bis/c2_review/statistics.json` — números, flags, cobertura, inventário e hashes.
4. `bis/c2_review/review_numerics.py` — geometria espectral e controles limitados de fit.
5. `bis/c2_review/numerics.json` — resíduos, parâmetros, comparações e versões do runtime do revisor.

Raiz absoluta dos caminhos relativos acima: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`. Os temporários de escrita foram substituídos pelos respectivos destinos. Fontes, builders, resultados C2 e memórias não foram editados.
