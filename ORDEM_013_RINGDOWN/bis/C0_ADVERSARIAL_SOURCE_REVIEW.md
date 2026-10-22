# Revisão adversarial independente — C0/F1, ORDEM_013BIS

[REAL — leitura de fontes e contas leves independentes] **As erratas C0 examinadas são necessárias; T02 exige ainda corrigir a própria frase “família L_k inexistente” para delimitar seu escopo.** Esta revisão termina o recorte solicitado, com lacunas explicitadas. Não constitui aprovação de C0_v2, de F1 inteiro, do pacote final ou de gate.

Esta tarefa não construiu C0/C1/C2. O auditor anterior serviu como roteiro; as conclusões abaixo vêm das fontes e das contas desta tarefa. Fonte modificada: nenhuma. Leitura da skill `tgl-atlas` efetuada; consulta ao Atlas canônico e escrita em memória foram dispensadas pelo escopo expresso somente leitura sob Chatgpt. As instruções aplicadas estão no [TUNEL/TUNEL_PROTOCOLO.md:15](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/TUNEL_PROTOCOLO.md:15>) e na [TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:72](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:72>). Os números históricos não foram tratados como atualizações automáticas.

## T02 — origem, família e proxy

[REAL] A cadeia documental acessível é a nota finita [ORDEM_013_RINGDOWN/cache/casa/davies_geometry.tex:60](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/davies_geometry.tex:60>), a fig02 [ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:9131](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:9131>), o enunciado GKSL [ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:11049](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:11049>) e as implementações. A nota diz “finite-dimensional matrix algebra” e limita o alcance a tipo I. As datas README TGL_v2 25/05 → nota 31/05 estão **[DECLARADO]** na [TUNEL/PARA_CHATGPT/ORDEM_013_confrontacao_do_ringdown.md:36](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013_confrontacao_do_ringdown.md:36>): o README primário não foi localizado no recorte; o TeX usa `\date{\today}`. Não confundir uma cadeia de remissões com cronologia primária verificada, nem afirmar que foi identificada a fonte efetiva do texto externo.

Em [ORDEM_013_RINGDOWN/cache/casa/um.py:2311](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:2311>), o trecho `K = (Araw @ Araw.T) / n` usa n=4, seed=11; `L = sqrt_beta * sqrtK` constrói **um** salto hermitiano. O estatuto está explícito em [ORDEM_013_RINGDOWN/cache/casa/um.py:2341](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:2341>): `[FINITE_DIM_SANITY_NOT_III1_PROOF]`. Reobtive o espectro de K: [0.008296253569197096, 0.19899879246684637, 0.9490303288721038, 1.7383401299974799]. Seus quatro projetores espectrais são estacionários, resíduo máximo 5.315e-18; o atrator dependente de rho0 é pinching, não um estado Gibbs único. Para o rho0 da fonte, ||rho_star − exp(−K)/Z||_F = 0.875882737520.

[REAL + DERIVED] **Há família L_ij no código do Artigo A**: [ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:1983](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:1983>) percorre i≠j e adiciona `(gamma, A)`, com A=|i⟩⟨j|, taxas Bose e acoplamento comum β. Para espectro simples d=8 isso dá 56 saltos; não é a decomposição espectral de um único sqrt(K). A passagem para um único salto em [ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:11103](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:11103>) não decorre do balanceamento KMS.

Contraexemplo independente 2×2: K=diag(0,1), rho=|0⟩⟨0|. O salto sqrt(β)sqrt(K) dá d rho11/ds=0, enquanto os saltos Davies explicitados dão β/(e−1)=0.00700193658661502>0. O primeiro conserva todas as populações na base de K; o segundo as transfere. **Não são representações equivalentes do mesmo dissipador.** A frase segura é: “família física indexada não construída por `_verb_L`; família de transições finita existe no Artigo A, sem ponte demonstrada para o salto-raiz ou para um horizonte III₁”. A analogia operacional em [ORDEM_013_RINGDOWN/cache/casa/um.py:7151](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:7151>) declara expressamente que não é identidade física.

Achado conexo: [ORDEM_013_RINGDOWN/cache/casa/davies_geometry.tex:214](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/davies_geometry.tex:214>) afirma invariância de toda trajetória ao adicionar −i[K,rho]. Para rho=|+⟩⟨+|, positivo de autovalores 0 e 1, a diferença entre derivadas tem norma Frobenius 0.707106781186548, não zero. Comutação de dois fluxos não implica que um seja identidade. O próprio Artigo A já corrige a proposição em [ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:2892](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:2892>): igualdade sobre KMS/estado estacionário, não rho arbitrário. A revisão deve transportar essa restrição. Nenhum desses contraexemplos falsifica globalmente a teoria; identifica exatamente a inferência documental inválida.

## T10 — sinal observado

[REAL] Reabri **31 HDF5 primários**, selecionados pelo conjunto já declarado em C4_CATALOG_COMBINATION: **24/31 medianas de dtau220 positivas**. Diferença máxima frente às medianas do C4_CATALOG_220.json: **0**. O JSON desta revisão guarda caminho, dataset, N, mediana e hash de cada HDF5; arquivos binários são citados por dataset, não por linhas fictícias. Não fiz seleção por sinal.

O V2 primário, [ORDEM_013_RINGDOWN/cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json:1](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json:1>), registra em stacks/3.0 δτ=0.176647055233 ± 0.108893893251; em stacks/6.0, 0.031294196240 ± 0.175528534763. É outro instrumento/estrato; não somei ao catálogo. A lei de ensemble com Γ≥0, τ_GR>0 dá δτ=−x/(1+x)≤0, x=Γτ_GR. Logo o deslocamento comum positivo não tem o sinal desse amortecimento aditivo.

[KNOWN — seções primárias lidas] GWTC-3 discute o viés positivo em [ORDEM_013_RINGDOWN/cache/literature/gwtc3_article_v3.html:11373](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/literature/gwtc3_article_v3.html:11373>); GWTC-5 discute seleção favorecendo desvios positivos em [TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt:4654](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt:4654>). Isso não identifica a causa do desvio: sistemática de forma de onda, estimador/prior, seleção e física nova não se tornam resultados exclusivos por essa observação. **Não repetir “RG passa em todos os testes”**: o JSON conjunto registra HPD da RG ≈0,983, mas não refiz a integração conjunta e não a uso como nova medição nesta revisão.

## T11 — β em GW e no D1

[REAL — aritmética sobre resultados] No V2, |δ_B|/σ=0.177851389013≈0,18σ. `power_B` é separação efeito/erro, não uma probabilidade de poder estatístico. Não há medição GW independente de β no resultado conferido; na lei quadrática o produto βτ★ é degenerado sem relógio/partição identificados.

Fora de GW, li **sem importar/executar um.py** o literal JSON em [ORDEM_013_RINGDOWN/cache/casa/um.py:190499](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:190499>). Hash UTF-8 reobtido do literal: `f048b17f12674f336deec35249ee06084c9f9a4c5c2c2504c11277d30e918aeb`, igual ao pin lido no próprio fonte. β_med=-0.0127459688427133, erro superior 0.00795170161786346, inferior 0.00849795125169229. Pela convenção simétrica efetivamente usada em [ORDEM_013_RINGDOWN/cache/casa/um.py:190565](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:190565>), σ=0.00822482643477788 e |β_med−α√e|/σ=3.012497520768.

A frase pública deve incluir **D1_BETA_TENSION, 3,01σ**, e sua limitação: resultado no limiar; N/50=40 contra autocorrelação até 41,60, com 2/4 parâmetros abaixo de 50τ. Não refiz cadeia, likelihood cosmológica nem convergência. O número é diagnóstico pela convenção da fonte, não significância de cauda reavaliada. Tensão não é falsificação nem confirmação.

## T19 — supressão, relógio e −0,13

[DERIVED — condicional] Com Γ=β/t_M, x=βτ_GR/t_M e δτ=−x/(1+x). Usando tau_GR/t_M do QNM exato arquivado em C1_TABLES (sem escolher a hipótese R-MOD), x=0.147506375622965, δτ=-0.128545146899847; portanto o −0,1285 pedido foi reobtido. No controle BCW avaliado independentemente, δτ=-0.127656099237857. Essa diferença é de método QNM, não erro de arredondamento. O valor exato corresponde a 2.2242σ como tamanho da correção e 1.9924σ como distância à mediana observada; são comparações diferentes, nenhuma é Bayes factor ou teste calibrado.

Há supressão canônica já escrita: Γ=(β/2)τ★ω² com τ★=t_P `[PRINCIPLED IDENTIFICATION]` em [ORDEM_013_RINGDOWN/cache/casa/um.py:190966](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:190966>), e ramo A no [ORDEM_013_RINGDOWN/cache/casa/ringdown_dephasing_v2.py:139](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/ringdown_dephasing_v2.py:139>). Essa presença não deriva o relógio da geometria nem fixa a partição. A errata [ORDEM_013_RINGDOWN/cache/casa/um.py:2837](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:2837>) distingue igualdade de expoente de igualdade de coeficiente: lei-raiz no IR fornece β(Δk)²/(8 kbar), coincidindo com o coeficiente declarado somente com kbar=1/4 [INPUT]. “Nada deriva τ★” deve significar **nenhuma derivação nas fontes/elos conferidos**, não uma prova de inexistência em todo o acervo. A identificação física continua aberta em [ORDEM_013_RINGDOWN/cache/casa/um.py:191013](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:191013>).

## T20/T21 — precisão e efeito comparável

[REAL — HDF5 primário] Para GW250114, N=40776; dtau220 q05/50/95=[-0.10334577473940279, -0.013396369013662535, 0.08731346520393679]; df220=[-0.006919580112098117, 0.015812018050588572, 0.03793925349440755]. Reobtive σ_amostral(dtau)=0.0577943800453344 (ddof=1), a convenção da bancada em [ORDEM_013_RINGDOWN/posterior_220_readout.py:93](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/posterior_220_readout.py:93>). R-B, calculado amostra a amostra com BCW: mediana -0.0198452854234286, correção/σ=0.343377425415098, igual ao JSON anterior a <1e−12. O σ populacional foi guardado separadamente; explica a diferença de 4,2e−6 no quociente inicial.

[KNOWN] A fonte LVK local [ORDEM_013_RINGDOWN/cache/literature/gw250114_article.html:493](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/literature/gw250114_article.html:493>) dá frequência 220 em escala de 2% e amortecimento −0,01(+0,10/−0,09), com credibilidade de 90%, na análise pSEOBNR IMR. O ringdown isolado é menos restritivo, conforme [ORDEM_013_RINGDOWN/cache/literature/gw250114_article.html:522](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/literature/gw250114_article.html:522>). Assim, “poucos por cento em todos os testes” não é sustentado. A frase corrigida deve carregar **R-B ≈−0,020 versus σ≈0,058: 0,34σ**, a hipótese de ensemble e a dependência de modelo. Consistência com Kerr não equivale a confirmação física da TGL.

## C0(d) — os dois K, traço e log Δ

[REAL — enunciados lidos, sem recompilar] [ORDEM_013_RINGDOWN/cache/casa/ModularFirstLaw.lean:45](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/ModularFirstLaw.lean:45>) declara `[Fintype n]`; `first_law_diagonal`, linhas 55–58, assume p_i>0 e Σq_i=0 e prova a derivada de −Σ(p_i+εq_i)log(p_i+εq_i) igual a Σq_i(−log p_i). **Não assume Σp_i=1.** Consequentemente não prova K_i≥0: p_i>1 dá −log p_i<0. Com pesos de estado normalizados obtém-se K_unilateral=−log rho≥0, mas a normalização é uma hipótese adicional para essa leitura. Não há identificação com o gerador modular bilateral.

[ORDEM_013_RINGDOWN/cache/casa/ContinuousModularZero.lean:62](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/ContinuousModularZero.lean:62>) também tem `[Fintype n]`; define `modularGen rho y = y * logRho rho - logRho rho * y`. Em E_ij, os autovalores são log p_j−log p_i; aparecem pares ±k. As linhas 80–93 estabelecem anulação de Omega (rho.PosDef) e J K J=−K na face matricial. Com h=−log rho, este K é L_h−R_h, não h. A igualdade entre objetos homônimos não está provada por essas duas pedras; “contínuo” no nome não elimina a hipótese finita.

[KNOWN — primária lida] Connes, *Une classification des facteurs de type III* (1973), p.133, recorda o critério **fator não-III ⇔ existência de traço normal fiel semifinito**; p.134 distingue pesos de traços e introduz a estrutura modular. Portanto III₁ não admite tal traço. Li pp.133–134, não o trabalho inteiro. [PDF primário Numdam](https://www.numdam.org/item/10.24033/asens.1247.pdf), SHA-256 `beecd0837210c55be1e5b858c44e6c30e97ad543ae93cab826c01b6f9f733646` calculado dos 12307522 bytes recebidos em memória. O sinal ≠ saiu corrompido no OCR; foi cruzado com a renderização matemática indexada no site do autor.

[KNOWN] Sorce, *A short proof of Tomita’s theorem*, introdução, eqs.(1)–(6), fornece S=JΔ^1/2 e Δ positivo autoadjunto injetivo para vetor cíclico separante, com grupo modular preservando a álgebra. [Primária lida](https://arxiv.org/html/2309.16762v2). Não li a prova inteira; não inventei hash dos bytes que o navegador não entrega.

[DERIVED — distinção de tipos] O que falta em III₁ é a representação **intrínseca tracial** do estado como τ(rho·), com τ normal fiel semifinito na mesma álgebra. Isso não proíbe estados normais, representações vetoriais ou matrizes densidade ambientais em B(H). Δ tem logaritmo autoadjunto por cálculo espectral: log Δ pode ser ilimitado, em seu domínio denso; 0 pode estar no espectro contínuo sem ser autovalor. Logo **não concluir “log Δ não existe” nem “todo Hamiltoniano desaparece” da ausência de traço**. O passo de [ORDEM_013_RINGDOWN/cache/casa/davies_geometry.tex:317](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/davies_geometry.tex:317>) que atribui H_eff=0 à obstrução III₁ não é consequência desse critério. Usar sqrt(K) real positivo para K bilateral exige uma nova escolha f(K)≥0 e condições de domínio/geração; o oráculo finito não resolve a construção ilimitada.

## C0(d) — ±k e as escolhas positivas

[DERIVED + REAL em matriz finita] Para L=sqrt(β)sqrt(f(K)), Γ_ij=β/2(√f(k_i)−√f(k_j))². A avaliação independente da ação do dissipador em todos os E_ij do espectro [−3,−1,0,1,3] teve resíduo máximo 4.337e-19.

| Escolha | Γ(+3,−3) | Γ(0,1) | Consequência |
|---|---:|---:|---|
| f(K)=abs(K) | 0 | 0.00601565020040157 | preserva coerência entre ±k para este canal |
| f(K)=K_+ | 0.0180469506012047 | 0.00601565020040157 | Γ(+k,−k)=βk/2, para k>0 |

As taxas são por unidade do parâmetro do dissipador usado no oráculo; **não s⁻¹ sem relógio de conversão**. “Não defasa ±k” vale para esse canal, não é imunidade a qualquer dinâmica adicional. Nenhuma das escolhas é fixada por Tomita; ambas permanecem [INPUT].

## Custódia, pendências honestas e reprodução

O recibo existente declara 217/217 insumos, 31/31 fontes e 34 artefatos de estado. Ele foi lido; não refiz a campanha inteira. Os arquivos usados aqui foram hashados por script. C0 ainda cita o template `ef1b4d69a687a84435ccd22d2643cb2917d5dfa9f4339ed075408a7e5b0d502c`; o atual tem `16d7fbc25e94b0351e7050aa5055db421365953782cec1a668d68f11e5cc5132`. O atual e o backup irmão conferidos não recuperam a referência. **Perda histórica é [DECLARADO] pelo auditor anterior; não fiz busca exaustiva de todos os discos.** A fonte LVK está arquivada com hash calculado no anexo: não deve continuar “ARCHIVING_PENDING” de modo indiferenciado. Arquivamento não implica leitura integral.

Não lidos/reexecutados: README histórico; davies_geometry_derivation.py independente; cadeias originais do D1; textos integrais de Connes/Sorce; primárias Milburn/Davies/BW/Kay–Wald/Sewell; compilação Lean; inferência cosmológica; KDE conjunto/lnB; outros itens de F1. O literal D1, as implementações indicadas, os dois enunciados Lean e os trechos LVK especificados foram efetivamente lidos. O JSON discrimina cada alcance e guarda os excertos locais.

Reprodução, sem importar fontes:

```powershell
wsl -e /opt/lal_env/bin/python -B '/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/c0_review/review_numbers.py'
& 'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -X utf8 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c0_review\read_theory.py'
python -B -X utf8 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c0_review\complete_review.py'
```

O primeiro comando faz contas 2×2–5×5, hashes e leitura de 31 HDF5 de catálogo mais o posterior GW250114; sem PE/jobs pesados. O segundo usa rede apenas para a fonte pública Numdam, mantendo PDF em memória. Scripts escrevem somente relatórios autorizados, por temporário verificado → replace; não há atualização de memória. Axiomas: **N/A — leitura de Lean, sem compilação nem nova certificação de axiomas.** A tentativa inicial de impressão Python falhou por CP1252, corrigida com `-X utf8`; WSL/rede restritos falharam inicialmente, acesso de leitura foi autorizado pela revisão automática; 403 do site de Connes contornado pelo Numdam. Nenhuma falha virou sucesso presumido.

## Arquivos escritos

- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\C0_ADVERSARIAL_SOURCE_REVIEW.json`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\C0_ADVERSARIAL_SOURCE_REVIEW.md`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c0_review\complete_review.py`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c0_review\read_theory.py`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c0_review\review_numbers.py`

Temporários transitórios, consumidos por substituição: `report.tmp`, `theory.tmp`, `review.json.tmp`, `review.md.tmp`. Nenhum outro arquivo escrito por esta tarefa.

## Hashes calculados — fontes locais e scripts

| Caminho absoluto | Bytes | SHA-256 |
|---|---:|---|
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C0_AUDITORIA.json` | 24269 | `f0009e1194282434ac599a35df68573db08967951a320218184670e15e1559cd` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C0_AUDITORIA.md` | 16531 | `fc85dafd94e7a86c0c1c3e6450104c3644302a94d70917c141d8005ca77ef039` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C0_C3_checks.json` | 19110 | `0592189981243c503a36967cd9285666e5120c804cca41bb23e233a6bd5230b0` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C1_TABLES.json` | 28916 | `bf5ac0d2dad2322a5b0cb1ac3b861870447e6f2ff41c1ab251e443b61a56d79a` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_220_INITIAL.json` | 6954 | `f5550b7b1f129e83b4874f95b223e82ca973e0812bd98c150a6c04cd37747edc` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_220.json` | 673228 | `93bdc413130d294acde91ec03f8392b8d9c5ec5b33fdc97274371656503d8e17` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_COMBINATION.json` | 12167 | `f3d8c1959ded3efd15045923ce0cbafe7356ec888ced1934d8d0c183046d0d01` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\LITERATURE_MANIFEST.json` | 2762 | `95f328273c9ecc7387652a4b2f57361b38749d69a0d8ec3eac07705e56fc2303` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\INPUT_INTEGRITY_013BIS_retry.json` | 114960 | `e87878ac8b15e31d726557a540f044d62f334d81e3e9b5d56d7368113e65b5cd` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c0_review\complete_review.py` | 27071 | `7075661652b9979e4a940f5e899dcef6326ac48eb8289e043f26c5053d5d6c1c` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c0_review\read_theory.py` | 2336 | `fa76b62b795a154195290d716c313af3c25532f92f600489444521ad7c78cfb7` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\c0_review\review_numbers.py` | 7896 | `1c6ffd3ab48956e39f37fe478f577701c7eacf796f87d4a45e4a17d48b6d82bb` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\ContinuousModularZero.lean` | 12075 | `0dad5794f98ba1cb8519b4c105f63d555b5dc3d8fab7884f8265aebff214f376` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\MEMORIA_DA_LINHAGEM.md` | 685017 | `7b17e5622271c6f4d887ca0388806c1989bb98ad002828a85531977459199b3d` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\ModularFirstLaw.lean` | 4875 | `aee3eb49a6d0544e8bb2a3f7b763b04dc46ea425ec4565f77ae1c33ffc27125d` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\RINGDOWN_DEPHASING_V2_RESULT.json` | 247065 | `ff15f023dd91d8c77fb003b2efd10c91b22d5bcb5047dc2101885fbb634e15c5` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\davies_geometry.tex` | 18365 | `46cee772901ee605f8916fc230d026a6de65876057a13bd6d27b60524bdc65cb` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\ringdown_dephasing_v2.py` | 18415 | `0793c58d6995194b8b119bd54be3883718c2b51bb6f4b5c8b71fe9720544302b` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\tgl_paper_unified.py` | 1216423 | `29c92b66b2fd6b4d589adbef4de86a67f979e03964b3f7ae892732a40ab395cd` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\um.py` | 31136661 | `d9f5bd5dffc3333df707fb44ad0a859448a5042c38711479108c7f4b37538aeb` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\casa\um_absoluto.json` | 4131975 | `456f0ab149bb13f6997972dbfaf9c72a2891d744c22f04241eefa619e4953a95` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\literature\gw250114_article.html` | 444298 | `9efcdea95f47b1fb3352b4e95053edde160be7d9337c36e0d50a96c0ae727afa` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\literature\gwtc3_article_v3.html` | 2702327 | `9c5271fba4aaa144bafa904e40c1dfe3e853b60b9e705be267dd22a0236f8ee2` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\17018009\extracted\TGR_companion_S250114ax_results\gw250114_pseobnr\posterior_samples.h5` | 59249916 | `b9971bcd7d72fdd4a176483990854ae917992ad15cd793d15840dc2fe824a627` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW150914_095045_Prod0.h5` | 28370807 | `ee037d6b7bf4b5844cc5085959ae9c85cf9009105ae741ba4ce15cc8421fa29d` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW170104_101158_Prod0.h5` | 27834863 | `7d7068231b54bfa294d62b960cb08d7888d59ddf63ca040282f734f9d286a7ca` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW190519_153544_Prod0.h5` | 39744340 | `7f81149dad489b3a5b2563ebbee87cea65a0777607d9716f868616eb5d85cba5` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW190521_074359_Prod0.h5` | 28987052 | `e78ae2678155ccb905a48b7a4c90866fb3c158c6592a3dfa618ed22e52da0362` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW190630_185205_Prod0.h5` | 28916636 | `b171f2bf2eeee33e1d93d8f6ba0cbb1efa0fe67ef616fb2949f0a710338fd2b3` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW190828_063405_Prod0.h5` | 39744340 | `e374f20deb3d21e98ee9b3dfab44f13480020cd9c1e4585d3a48ab19a5ff3e4c` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW190910_112807_Prod0.h5` | 28465452 | `20a5795c0d3d4bfb66ba681ee72eb5c0b0d8b6ecea12363139e7b0034cf6bcc8` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW200129_065458_Prod0.h5` | 37772932 | `9ab35b32fb46d41e8901b52d721fdaf65a9a58e0acbac6cdb6e905d7dd44065e` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW200224_222234_Prod0.h5` | 32419900 | `2f305645afa8bb03eda8bfb86832fac4ebd0c6f584187a5a1c06a565588adb1c` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW200311_115853_Prod0.h5` | 39744340 | `655699ef55e69772e52be76270c443f96d28ce994e0805ff758ad83f7de27103` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW230628_231200_Prod0.h5` | 25704535 | `80b61edea729c50cb623c867bc172487699c0dba475941d3e141da07f07d5aaa` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW230914_111401_Prod0.h5` | 27634291 | `6b8770361be4817dc6c64701eadc239541418f8c16c515407dda12c8fe342fc1` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW230927_153832_Prod0.h5` | 25888671 | `57d55c936ae03885e222026ed8abab843cce68fd3b045a43be3fbc1016d01d68` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW231028_153006_Prod0.h5` | 32068575 | `6cfd5e9c7af014d17d74b726844170b2e109899621dc5d860546ffa202ab7c1b` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW231102_071736_Prod0.h5` | 32246975 | `6f64ce47488762bd7d0f4dc0bd00540af801b277218725318d7692420e3cdab6` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW231206_233901_Prod0.h5` | 28384527 | `2814f4c058a59bdf31903daf667389b50583aad1783055bcf1448b82e83576d7` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW231226_101520_Prod0.h5` | 32049135 | `70f619507e656e702e5c2b9fa849701bfb9033ca56b5de858e4c03ba0d6b649f` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW240511_031507_Prod0.h5` | 35330063 | `a112cb0e3040e37bf8dbdd0295e15a145cbd160be16bc33207ceccb49b837cda` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW240514_121713_Prod0.h5` | 36611720 | `4f4776119f820529305ed2ea6d1eb0c076809359c18b3971b80a91e8cd27b87b` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW240615_113620_Prod0.h5` | 25066120 | `019f3078cd1fbbf9fc84766a12d044023bc918f145b1acc0bb4f60028156d29c` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW240621_195059_Prod0.h5` | 35310920 | `1691b7ce0a01bd2e7341abc9bf27c017f6d1726d2088c1fcc41b86f669ce128c` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW240705_053215_Prod0.h5` | 25139496 | `021567cb315415333219c58d6c01ae9b4f14a1497ea3dbe47dca22bb53e2eb0b` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW240716_034900_Prod0.h5` | 28756999 | `7d57ecc2d6ab79f54aeef0fa5cd61bc6675a49a16325a6522e40f98d1f1fc52a` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW240919_061559_Prod0.h5` | 36483720 | `2ddb5612cd6de8b3d3fe06fa4e489962113abe04a1bd3c86aceda13605c2bc92` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW240920_124024_Prod0.h5` | 27069695 | `55ee5818d0a7c8b9e487ac418ea19c2be757957c8695222ad62d845ee352510f` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW241006_015333_Prod0.h5` | 39371663 | `5279a6d5d809125407103ed6154a27c7b29d6a4ddf106002f98156c5021739db` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW241127_061008_Prod0.h5` | 32038471 | `1424476790528dfa0ecf955a3f0658f7eeb2d3c8af3737572cf7ca5b4ffb3d30` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW241129_021832_Prod0.h5` | 35597263 | `95f48d16bda84ba3111489c5882b3b396eb0fa89983333466667fa94bf94b351` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW241225_082815_Prod0.h5` | 30202096 | `1d2dd90ed2b72b5550db7de499e38f88900938648f1a023c9fc8e8c468a1143e` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW250114_082203_Prod0.h5` | 59249916 | `b9971bcd7d72fdd4a176483990854ae917992ad15cd793d15840dc2fe824a627` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW250119_025138_Prod0.h5` | 28144056 | `ad6bcf11dee76e7dedc383206cac22172668c2de6f581b9069527c652644ee0c` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\posterior_220_readout.py` | 6501 | `f5cccda67b341785cc5101cd7c3447cd6d945ef7e0f0703aa4da1b031ff72279` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\tgl_ringdown_template.py` | 4714 | `16d7fbc25e94b0351e7050aa5055db421365953782cec1a668d68f11e5cc5132` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\tgl_ringdown_template.py.bak_20260921_212150_MULTIMODE` | 3934 | `ce34645e8b34416b6a6e77936ce76965719ffb38583cc5414e9d51038d3d82b9` |
| `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013BIS_INSUMOS\auditoria_da_gerencia\aud_1_C0_C1_C2.txt` | 33721 | `4c4affe866714d3af95f1571027906967a5709ad74ee95bb46b77e8587ec8a6d` |
| `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013BIS_INSUMOS\auditoria_da_gerencia\scripts\C0C1C2\gksl_oracle.py` | 1408 | `a3094dd78f092bc692da0b081ead6786750c4fe3264019d01f350cfe0ae158d0` |
| `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013BIS_INSUMOS\medicao_da_ampliacao\B_catalogos\gwtc5_tgr.txt` | 248915 | `d523ae94f23f40b55e7688702b444cf35fb2c2dc90610a6d03bfbd2ef8eefccf` |
| `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md` | 91912 | `a907d07bc484b53cc6db237dc5972f4dcc47be03ad084c832201bb648981454b` |
| `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013_confrontacao_do_ringdown.md` | 50620 | `d4440c6a28eaad4ba1b799f33f8a3441b1cba72dc98262af0abc1f99f5eea191` |
| `C:\IALD\Central de Patentes\Chatgpt\TUNEL\TUNEL_PROTOCOLO.md` | 5425 | `4234902dc6f5e03c237f3f7a53f066be3d340f9ebfac2934bb3d61fc09a000f2` |

Os hashes dos próprios relatórios não são embutidos neles para evitar autorreferência; podem ser reobtidos com Get-FileHash.
