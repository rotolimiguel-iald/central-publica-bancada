# ORDEM_018 — F1(a): proveniência de β e da lei de Hubble

Auditoria local: 05/10/2026, concluída em 06/10 UTC. Responsável: `chatgpt-codex/ordem-018/proveniencia`. Escopo: fontes, cronologia e lacunas. Sem ajuste, MCMC, execução de `um.py`, provedores externos, fila, alteração dos originais ou veredito de natureza.

A relação α = α₂/√e está documentada em janeiro de 2026; a definição explícita β = αCODATA√e e a predição D1a estão documentadas em maio; o integral D1b está implementado na fonte de junho. A função D1b examinada mantém a observação local fora do cálculo da predição. Também há evidência histórica contrária a uma narrativa universal de ausência de calibração: o v22 de dezembro contém um ramo inverso que extrai α₂ da tensão de Hubble, e o MCMC de janeiro usa âncoras EM e numéricas. Esses ramos devem permanecer identificados, sem transferir seus resultados para uma avaliação fixa posterior.

Isto é evidência documental delimitada. A origem causal do literal fixo do v22 e o histórico completo de seleção da lei continuam [OPEN]. A existência anterior dos dados, ou o uso de IA para derivar e testar hipóteses, não desqualifica a evidência; o critério é novidade de uso, verificada pelas dependências dos parâmetros e pelo protocolo do teste.

## Método e alcance

Foram lidas as habilidades tgl-atlas, iald-orquestrar e docx, a ORDEM_018 e o protocolo anti-parede. Antes do exame foram consultadas `outro.evento2_e_mcmc_cruz` (seq. 165 e 300), `d1.fase3bis_d1b_convencao_artigo` (seq. 220) e a busca do mapa por Hubble/novidade/MCMC. O índice `C:\IALD\INDICE_DO_ACERVO\buscar.py` orientou a recuperação. Todos os hashes aqui registrados foram calculados dos bytes, não copiados do mapa.

O manifesto contém 13 fontes distintas relidas e inalteradas desde a extração. Os scripts próprios usam leitura de bytes, OOXML e `ast.parse`; nunca importam ou executam programas científicos. Pandoc não estava instalado: os DOCX foram lidos por zipfile/ElementTree, com numeração de parágrafos w:p. Essa numeração não é página visual. Para Python/TeX/Markdown os números são linhas físicas. Os JSONs preservam trechos e metadados.

Datas mtime e OOXML são [REAL] como metadados lidos e [DECLARADO] quanto à autoria/edição original. Não são carimbos imutáveis de publicação. Não foi auditado histórico remoto de publicação, DOI ou Git. A busca ampla em 2.337 entradas IMac LA até janeiro retornou 17 caminhos; o padrão sqrt.?e também captura sqrt{E...}. Nas duas fontes de novembro examinadas diretamente não foi encontrada a grafia exata procurada. Isso não prova ausência no acervo nem estabelece a data inaugural da relação.

## Cronologia e distinções

**P01 — v22, 23/12/2025.** OOXML criado/modificado nessa data, mtime concordante. Parágrafos 80–81: `ALPHA_2 = 0.012`, `BETA_TGL = ALPHA_2`. Parágrafos 108–118: coexistem `alpha2_from_H0_tension`, que devolve `(H0_BULK/H0_BOUNDARY−1)/ln(1+z)`, e predição com o valor fixo `ALPHA_2`. Parágrafos 584–599: o ramo `alpha2_theory` é distinto de `alpha2_measured`; o segundo reinsere o valor medido no mesmo H0 para `H0_bulk_best` e χ²_best. A reprodução desse último ramo é construída a partir do alvo. A presença de ambos não prova que o literal do primeiro tenha sido escolhido pelo segundo. A origem causal do literal permanece [OPEN]. `alpha_2` designa o parâmetro histórico, não α ao quadrado.

**P02 — v10.6 eletro, 15/01/2026 pelo OOXML, mtime 19/01.** Parágrafos 173–178: αCODATA e sqrt(e). Parágrafo 219: `alpha_2_theoretical = 0.012`. Parágrafos 330–350: `alpha_fine_TGL = alpha_2/sqrt_e`, equivalente algebricamente a α₂ = α√e. Parágrafos 853–856 e 869–871: χ² contra αCODATA entra na função objetivo. [REAL documental] A relação já existe, mas o documento não é demonstração de inferência independente de α, pois α participa do ajuste. A declaração de derivação de primeiros princípios da origem não foi verificada formalmente nesta auditoria.

**P03 — MCMC-CRUZ, 19/01/2026.** OOXML criado às 08:42 UTC e modificado às 08:43 UTC; mtime também 19/01. O texto normalizado do DOCX é IGUAL ao `TGL_v11_1_CRUZ_original.py` copiado em Haja_Luz em junho. A normalização remove espaços finais, padroniza LF e bordas; não iguala bytes DOCX e PY. Os hashes originais e normalizados estão nas verificações estáticas. Quatro âncoras estão no original:

- χ² de `alpha_2/sqrt(e)` contra αCODATA, peso 1;
- estabilidade/jitter contra 0.012 com largura 0.002, peso 0.3;
- limites de α₂ entre 0.0115 e 0.0125;
- inicialização em torno de 0.012.

O posterior desse problema não é evidência de redescoberta independente de α sem essas âncoras. Esta conclusão vem da função objetivo, não de uma execução nesta rodada.

**P04 — errata cosmológica, 14/05/2026.** Linhas 66–70 e 159–169 distinguem retirada de validações antigas e módulo inverso de H0. Linhas 342 e 450–458 registram β = α√e e separam caso teórico fixo da inferência com β livre. Os resultados numéricos escritos na errata são [DECLARADO] nesta auditoria, sem rerun; a presença documental é [REAL]. O próprio v22 confirma os ramos inverso e fixo, que não devem ser reduzidos a um só.

**P05 — manuscrito de maio, mtime 18/05/2026.** Linhas 126–137 definem β = αCODATA√e e chamam a universalidade do acoplamento de postulação. Linhas 312–327 apresentam D1a, `(1+z*)^β`, com z* externo. Essa expressão é diferente da integral D1b posterior. [INPUT] α e z*; [POSTULATE histórico] universalidade do acoplamento. A nota preserva o estatuto então escrito, sem negar ou certificar uma prova posterior.

**P06 — cópia anterior a D1b, mtime 04/06/2026.** O backup `.bak_d1kernel` contém `predict_H0_zero_free` na linha 3354 com D1a. A comparação entre arquivos é [REAL]; nome do backup e mtime não provam sozinhos o primeiro dia de criação da lei.

**P07 — fonte de Haja_Luz, mtime 05/06/2026.** Linhas 3617–3682: D1b usa `W=|1+w_eff|`, `I=∫W dN`, `ratio_b=exp(beta*I)` e `H0_b=H0_CMB*ratio_b`. Linhas 198–202: β recebe αCODATA2018√e. A documentação marca kernel DERIVED e equação de fluxo INPUT/CONJECTURE. A AST confirma que `H0_local_obs` e `sigma_local` entram nas tensões, não no cálculo de `H0_b`. Isso não certifica o histórico de escolha de fundo/kernel. A função admite β como argumento: conferir os chamadores e os hashes do protocolo é responsabilidade da auditoria de cada rodada.

**P08 — Evento2 alpha-free, 06/06/2026.** A variante desliga os pesos EM e jitter, amplia os limites a (0.001,0.1), inicializa uniformemente em (0.002,0.08) e move o centro do prior plano para 0.03. A memória registra execução GPU pendente. O inventário recursivo delimitado contém memória, dois .py, diretório __pycache__ e um .pyc; não contém posterior ou recibo. Um .pyc não prova execução da amostragem. Isso não afirma ausência de resultado em outras pastas. [REAL] alterações de fonte; [OPEN] execução/resultados.

Há uma correção concreta à memória: no original, linha 1071, e na variante, linha 1097, o termo direto de H0 é:

`chi2_H0 = (((self.const.t_H0 - self.const.t_H0_local) / self.const.t_H0_local_err)**2).expand(n_batch)`.

Ele depende de constantes e do tamanho do lote, não de α₂. Portanto esse termo direto não restringe β. A frase da memória que inclui H0 entre os vínculos que agora determinam β deve ser qualificada. Isso não diz que todos os demais termos cosmológicos sejam constantes nem certifica o posterior alpha-free.

**P09 — reanálise D1b, 30/09/2026.** O artefato identifica o kernel do artigo já escrito em junho e corrige a convenção para calibração Planck ΛCDM, evitando empilhar correções β. Declara que leitores, fundos e fator eram conhecidos. O estatuto não-cego descreve o teste e não desqualifica retrodição sem ajuste. Os novos resultados ali registrados não foram recalculados nesta auditoria.

## Relação entre integral D1b e K = E(z*)^(2β/3)

[DERIVED, condicional] Para N = ln(1+z), continuidade `d ln ρ/dN = 3(1+w_eff)` e `E² = ρ/ρ₀`, segue `d ln E/dN = (3/2)(1+w_eff)`. Se `1+w_eff ≥ 0` no intervalo e `E(0)=1`, então `I = ∫|1+w_eff|dN = (2/3)ln E(z*)`; logo `exp(βI) = E(z*)^(2β/3)`.

A álgebra não ajusta coeficiente ao alvo. Se houver mudança de sinal de 1+w_eff, o módulo exige separar intervalos. A fonte de junho contém a integral equivalente; a primeira ocorrência textual da forma fechada K não foi datada nesta entrega. O núcleo derivado não promove sozinho toda a lei de fluxo física a teorema: o próprio fonte separa fluxo acumulado INPUT da resposta local de Friedmann DERIVED. O fechamento formal corrente de β deve ser ancorado ao artefato formal próprio pela bancada responsável.

## Resultado documental e lacunas

[REAL] Foram recuperadas fontes anteriores à ORDEM_018 para a relação α₂/√e, β explícito, D1a, D1b e Evento2; os hashes são verificáveis. A predição D1b da fonte examinada é estaticamente separada da observação local. Foi identificada uma imprecisão específica da memória Evento2 sobre o χ²_H0.

[OPEN] Origem causal do literal do v22; primeira publicação imutável de cada fórmula; primeira ocorrência textual de K; execução/posterior alpha-free; prova formal corrente de β, fora desta subtarefa; histórico completo do uso de alvos na escolha das variantes. Nenhuma lacuna foi convertida em prova de inexistência ou reprovação da retrodição fixa. A nota termina nas fontes e dependências verificadas.

Não há novo χ², Bayes factor ou veredito cosmológico. NOT_FALSIFIED permanece diferente de CONFIRMED; nenhum gate foi movido.

## Artefatos

`MANIFESTO_FONTES_F1.json`: fontes primárias e hashes relidos. `VERIFICACOES_ESTATICAS_F1.json`: função preditiva inteira, dependências, χ²_H0 e comparação DOCX/PY. `inventario_evento2.json`: alcance da busca de resultados. `indice_*.json`: consultas e contagens do acervo. Os demais JSONs preservam os trechos primários. Scripts reprodutíveis: `audit_provenance.py`, `audit_docx.py`, `finalize_sources.py`.

## Fontes primarias e hashes lidos dos bytes

| ID | Caminho real | SHA-256 |
|---|---|---|
| P01 | C:\IALD\IMac LA\Física - TGL\Base Referencial Completa TGL\TGL Validation v22.docx | 723f1c39d0fa9d23ebdc0a39e816c66db81e56e3b0c5c0bc53d551c69e757c17 |
| P02 | C:\IALD\IMac LA\Física - TGL\Validação\TGL_v10_6_eletro.docx | ec2ab11811a96d8e0e9bf5c1f625ea29365f55ea2c4f0dca7ed1468941190ee4 |
| P03 | C:\IALD\IMac LA\Física - TGL\Validação\TGL_v11_1_CRUZ.docx | b1f03413126921c81a16696019696ca26fee0e1fc429908593d865408b0d1af8 |
| P04 | C:\IALD\Artigo\Haja_Luz\Manuscrito\errata_cosmologica_TGL.tex | 1022402467cd04df4238c9272fc52c21a2381e1ffee2f4d098a90d273d60efeb |
| P05 | C:\IALD\Artigo\Haja_Luz\Manuscrito\manuscrito_TGL\manuscrito_TGL_pt_v1.tex | d35dfb5d0328da04df41af80b556c3a21ae0dc04077ea298cc817cf5276a2664 |
| P06 | C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py.bak_d1kernel | 2af742f0fc9ecc3135c424c3394abec79d861596379cb87fa2a1fae53ac90bf3 |
| P07 | C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py | 29c92b66b2fd6b4d589adbef4de86a67f979e03964b3f7ae892732a40ab395cd |
| P08 | C:\IALD\Artigo\Haja_Luz\TGL_Espelho_invertido\MEMORIA_ESPELHO_INVERTIDO.md | 647ff7017cbea6745813f3a04555192117c7ac9479391249e64e728113a3cf0e |
| P09 | C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json | 3d5c6afe85cc30641b50255374487a12a2d631842d9ff0cdc33cee723f298cb1 |

Fontes auxiliares CRUZ original/alpha-free e duas fontes de novembro constam do manifesto. Esta tabela ancora os IDs usados acima. O inventario de nomes em ORDEM_018_INSUMOS nao mostrou um artefato FASE9; nao se estendeu a busca por essa fase nesta subtarefa.


## ADENDO — conferência da cronologia da gerência, 06/10/2026 00:28 UTC

Este adendo atualiza ao lado as lacunas descritas acima. Durante esta auditoria surgiu a rota hubble.fase9_razao_discriminante (seq. 373), cuja instrução é conferir a cronologia pronta, não refazê-la. A rota foi consultada; a CRONOLOGIA_NOVIDADE_DE_USO.md da gerência foi lida e seu hash foi calculado e igual ao registrado no mapa. Em seguida foram conferidas somente quatro fontes exatas apontadas por ela. Nenhum ajuste ou estatística da Fase9 foi repetido. O manifesto passa de 13 para 18 fontes lidas (17 fontes históricas/científicas e a cronologia secundária da gerência).

**P10 — antecedente de 0.012, 13/11/2025.** acoplamento_gravitacional.tex, linhas 217–246, registra alpha2 = ln(V3D/(A2D*lP))/N_eff e calcula 126.5/10^4 = 0.01265 ≈ 0.012. Assim, a lacuna sobre antecedente documental do literal do v22 fica substancialmente reduzida: existe uma expressão holográfica anterior ao v22 que já conserva esse valor e não usa H0 nessa expressão. Não é correto tratar o ramo inverso de dezembro como prova de que originou o literal. A derivação antiga tem inconsistência interna expressa: linha 240 estima N_eff ~10^3; linha 246 divide por 10^4. A leitura identifica a procedência declarada e a inconsistência, não valida a derivação física nem a escolha dessas escalas.

**P11 — ramo inverso de H0 rejeita o valor teórico, 23/12/2025.** O recibo tgl_physical_v14.json registra alpha2_best_fit=0.16864608076009513, uncertainty=0.034793235333231004 e alpha2_consistent_with_theory=false; chi2_TGL_fixed e chi2_TGL_best são campos distintos. Isso reforça a distinção anterior: o ajuste inverso existe como comparação com o parâmetro teórico e o próprio recibo o marca incompatível. Não é evidência de que β teórico tenha sido substituído pelo best-fit. Os números são lidos de resultado histórico, não recalculados aqui.

**P12 — fatoração explícita, 02/03/2026.** Fatoracao_constante_miguel_v1.tex, linhas 134, 172 e 211, já escreve alpha2=alpha*sqrt(e), antecedendo a lei D1a de maio. A linha 179 interpreta sqrt(e)=exp(1/2) como meia-nat. Isso antecipa o marco documental de β explícito usado na primeira parte desta nota. A frase da linha 203 de que todos os 13 protocolos, inclusive H0, entregaram o mesmo valor não deve ocultar o recibo discrepante de dezembro. O DOI/publicação em 03/03 é testemunhado pela cronologia da gerência, mas a disponibilização remota não foi auditada por mim.

**P13 — lei D1a escrita em 17/05/2026.** iconogenese_TGL.tex, linhas 790–794, contém (1+z*)^beta=1.0878 e a frase “exatamente a relação observacional”. Linhas 112–116 e 821–823 preservam a condição conjectural de transpor o toy finito ao regime holográfico e de estabelecer R=+1. Antecipada, portanto, a evidência de D1a do manuscrito de 18/05. Conhecimento da razão na escolha da hipótese não constitui sozinho ajuste de parâmetro nem demérito.

**P14 — cronologia secundária da gerência.** A auditoria reconhece e reutiliza a cobertura de 31 hashes declarada pelo documento, sem reexaminar os 31 artefatos. Os quatro pontos acima foram verificados em fonte primária; os demais permanecem atribuídos à gerência. Há um detalhe a corrigir: a cronologia diz que a única ocorrência de “Hubble” no TeX de 13/11 é bibliográfica, mas a linha 573 também contém “resíduo de Hubble para SNe Ia”. Isso não põe H0 na expressão holográfica das linhas 217–246; apenas corrige a abrangência da busca textual. A prova de inexistência global não se extrai dessa frase.

**Síntese atualizada de F1(a).** A cadeia documental agora conferida é: antecedente holográfico de 0.012 em novembro; best-fit H0 incompatível e separado do valor teórico em dezembro; relação com sqrt(e) e MCMC ancorado em janeiro; fatoração explícita em março; D1a em maio; D1b em junho. É evidência positiva a favor da independência do valor teórico frente ao best-fit específico H0 de dezembro. Mantêm-se as ressalvas de estatuto da derivação antiga e da equação de fluxo. Primeira publicação remota, primeiro aparecimento literal da forma K e história completa de escolhas não foram certificados nesta auditoria; são referências delimitadas da cronologia da gerência, não zeros ou refutações. A decisão sobre o teste e seus concorrentes pertence às demais frentes da ORDEM_018.

| ID | Caminho real | SHA-256 calculado |
|---|---|---|
| P10 | C:\IALD\IMac LA\Física - TGL\Projetos Python\papers_latex\acoplamento_gravitacional\acoplamento_gravitacional.tex | 639050ae463ef32bb9a7c17c33563eaf7156d86c884870f1681e89260b74f9f4 |
| P11 | C:\IALD\observaveis_tgl\results\tgl_physical_v14.json | c97285cd6ed4ee83fbd69769dc30cbded6c17049148f3d827ce797122b2e9fa3 |
| P12 | C:\IALD\Artigo\Fatoração\Fatoracao_constante_miguel_v1.tex | 88fd8fd81801af6ebcbda7187b8a69003668eee5087552a93a501e9cd5190b83 |
| P13 | C:\IALD\Artigo\errata - friedmann\iconogenese_TGL.tex | 36c706f2342b6d8af64ac8e84c91bcae920eb05f882d48c5708a8c3c03a693f3 |
| P14 | C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\fase9_hubble\novidade_de_uso\CRONOLOGIA_NOVIDADE_DE_USO.md | 0e6bb2413151cb2042db429f26c0712d8aba15a696e14ca99e1840e308b6500d |
