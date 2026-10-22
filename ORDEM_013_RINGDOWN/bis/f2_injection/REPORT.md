# F2 lateral — diagnóstico das injeções públicas LVK de GW250114

**[REAL — cálculo descritivo NÃO-CEGO; OPEN — contrato integral de lnB e calibração de cobertura; AGUARDA REVISÃO POR OUTRO AGENTE]**

Este agente construiu o cálculo independente; não o aprova adversarialmente. Raiz B: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`. Somente `bis/f2_injection/` recebeu escritas. Não houve PE, leitura de strain, campanha C5, import de produção/um.py, unpickle ou execução de notebook.

**Resultado:** as duas configurações têm mediana positiva de δf220. A mediana de δτ220 é positiva com 44 e negativa sem 44. O ponto GR está dentro da região conjunta de 90% estimada com 44; sem 44, está na fronteira aproximada de 95%, sem classificação robusta de exclusão. Isso não demonstra tendência positiva universal, causalidade exclusiva do 44 nem cobertura frequentista calibrada. lnB permanece `null`, não zero.

## Ordem, unidade de comparação e fonte

F2 exata lida em `../TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:79–87`, especialmente `:85`: pede extrair e descrever `pseobnr_injection/` em E1.3 e diz **uma injeção, com e sem 44, não curva em SNR**. Não multiplicamos os dois resultados como eventos independentes e não somamos ao catálogo. Este é o recorte lateral solicitado, não aceitação integral de F2 nem entrega M2.

Fonte: `cache/public/17018009/controls_extracted/TGR_companion_S250114ax_results/pseobnr_injection/posterior_samples.h5`; 64,331,592 bytes; SHA256 `e2373f81973401adfb78037236d28480155e3d0c428d49d46f822b381111a826`. Identidade conferida com `bis/F2_CONTROL_EXTRACTION.json` e `bis/F2_CONTROL_SCHEMAS.json`, e antes/depois da leitura. Dois grupos `NR_with_44`/`NR_without_44`, cada qual com `posterior_samples` de 20.000 linhas. Foram lidos apenas campos selecionados de posteriores/priors e metadados físicos; nenhum dataset de strain. O recibo atribui licença MIT ao membro; não foi refeito download do tar.

[KNOWN — seção primária consultada online, não artigo integral] O [artigo LVK, apêndice .7, parágrafos da Fig. 11](https://arxiv.org/html/2509.08099v1#A1.SS7) descreve uma simulação SXS:BBH:3617, massas iguais e spins nulos, em ruído gaussiano. A comparação remove os multipolos (4,±4) da injeção, preservando a simulação e os parâmetros. O objetivo original é validar a informação de frequência do 440. Isso não é um ensaio de população nem de cobertura do 220. A coincidência dos nomes e o caminho de configuração SXS_3617 são consistentes com essa identificação; não reconstruí o sinal ou a semente de ruído. A página foi lida via web, não arquivada em bytes nesta tarefa: nenhum SHA web é inventado.

No HDF5, `config_file/config/zero_noise=False` e `gaussian_noise=False` não provam ausência de ruído em dados já preparados externamente. O artigo fornece o contexto gaussiano; não transportei para estas duas configurações a seleção de ruído descrita em outra subseção do artigo.

## Localização e massa posterior positiva do setor 220

As colunas são frações adimensionais arquivadas `domega220` e `dtau220`; não desvios logarítmicos do RD. P(>0) é massa posterior empírica, não p-valor, poder ou probabilidade de física nova. IC abaixo significa intervalo **credível** central, com quantis lineares.

| Configuração | Campo | Mediana | Média | DP amostral | IC 90% | IC 95% | P(>0) |
|---|---|---:|---:|---:|---|---|---:|
| NR_with_44 | domega220 | +0.020948 | +0.021132 | 0.011824 | [+0.002027, +0.040686] | [-0.001662, +0.044839] | 96.555% |
| NR_with_44 | dtau220 | +0.047857 | +0.050132 | 0.064455 | [-0.052369, +0.158419] | [-0.069988, +0.181572] | 77.760% |
| NR_without_44 | domega220 | +0.027949 | +0.029177 | 0.017326 | [+0.003484, +0.058831] | [-0.001479, +0.068004] | 96.950% |
| NR_without_44 | dtau220 | -0.101295 | -0.099935 | 0.042481 | [-0.167947, -0.027785] | [-0.180977, -0.011890] | 1.415% |

[REAL] Ambos os ICs marginais de 90% de δf220 excluem zero, mas ambos os de 95% o incluem. δτ220 com 44 inclui zero a 90% e 95%; sem 44, seu IC de 95% é inteiramente negativo. O intervalo contíguo mais curto de 95% dá as mesmas conclusões de inclusão para esses quatro casos; ele não foi chamado de HPD multimodal.

A diferença **com menos sem 44** entre medianas de δτ220 é +0.149152, e entre medianas de δf220 é -0.007001. Não são diferenças pareadas linha a linha; não há distribuição de repetições/ruídos que permita convertê-las em significância de viés. A covariância entre os dois ensaios não foi recuperada.

| Configuração | P(df>0, dtau>0) | Correlação posterior df/dtau | Pares 220 distintos / 20.000 |
|---|---:|---:|---:|
| NR_with_44 | 0.747800 | -0.200973 | 19997 |
| NR_without_44 | 0.012400 | -0.208044 | 19758 |

Duplicatas são mantidas como parte da medida empírica publicada; contagem de linhas não é ESS. Não há coluna de pesos nesses posteriores; a análise usa pesos iguais. Não revalidei a reamostragem/diagnósticos de convergência do produtor.

## Referência GR e limite de cobertura

Estimamos c₀=P[p̂(df,dtau)≥p̂(0,0)] com KDE gaussiano: 16.000 linhas de treino, 4.000 de consulta fora do treino, uma divisão determinada pela semente 1302212026. GR pertence à região estimada de nível α se c₀≤α. Os multiplicadores de Scott são 0,7/1/1,4, como no registro C4. Não são três dados independentes.

| Configuração | c₀, banda 0,7 | c₀, Scott | c₀, banda 1,4 | Escala binomial Scott, se iid | Suporte local Scott* |
|---|---:|---:|---:|---:|---:|
| NR_with_44 | 0.85925 | 0.86800 | 0.87500 | 0.00535 | 193.28 |
| NR_without_44 | 0.95300 | 0.95075 | 0.95025 | 0.00342 | 60.34 |

*Suporte local = (Σw)²/Σw² dos kernels no ponto GR, não ESS da cadeia. A escala binomial é apenas uma referência condicional iid; não inclui incerteza de treino, dependência das amostras ou viés de KDE.

Sem 44, os booleanos mecânicos no JSON dão `inside_joint_95=false`, pois c₀ ficou ligeiramente acima de 0,95. **Não interpretar como exclusão robusta:** Scott dá 0,95075, distante do corte por só 0,00075, versus escala de consulta ≈0,00342. O suporte local Scott é ≈60; na banda 0,7, ≈28. A borda de 95% não está resolvida. Com 44, o conteúdo 0,85925–0,875 é compatível com inclusão conjunta a 90%/95%. Marginais e região conjunta respondem perguntas diferentes; não há contradição entre suas inclusões.

Os campos `injection_data` têm somente valores não finitos e `meta_data/other/injection_parameters` é a string `None` em ambos os grupos. `METADATA.json` preserva esses NaN como JSON null. [KNOWN/DERIVED] GR fornece a referência df=dtau=0 para o setor 220 de uma simulação GR; [OPEN] os parâmetros numéricos completos da injeção e a realização de ruído não foram recuperados desses campos. Remover o 44 cria um controle de conteúdo modal, não uma segunda população de fontes. Inclusão/exclusão de zero nestes posteriores não estima cobertura frequentista, taxa de falsos positivos ou viés médio do estimador.

## Priors, setor 440 e aplicabilidade do mesmo lnB

[REAL — declarações arquivadas] Em cada grupo, `priors/analytic/domega220` e `dtau220` declaram `Uniform(minimum=-0.8, maximum=2.0, ...)`; `domega440` e `dtau440` declaram `Uniform(minimum=-0.8, maximum=0.8, ...)`. As declarações de todos os priors analíticos são idênticas entre os grupos. Os quatro campos variam nos posteriores. **O 440 é livre na recuperação de ambos os casos**: “without_44” não significa fixar seu desvio a GR durante a recuperação. Priors de outros desvios modais arquivados são DeltaFunction em zero.

O prior 220 assimétrico já atribui P(δ>0)=2/2,8=0,714286. A massa positiva posterior de dtau com 44 (0,7776) excede essa base por apenas 0,063314; sem 44 cai a 0,01415. Essa comparação descritiva impede usar apenas o sinal da mediana como evidência de deslocamento físico. Amostras de prior (5.000 por campo), limites e correlações estão no JSON; correlação amostral próxima de zero não é prova de fatoração global.

| Configuração | Campo 440 | Mediana | DP | IC 90% |
|---|---|---:|---:|---|
| NR_with_44 | domega440 | +0.353479 | 0.223802 | [-0.065093, +0.638272] |
| NR_with_44 | dtau440 | -0.044555 | 0.407335 | [-0.644085, +0.677798] |
| NR_without_44 | domega440 | +0.004839 | 0.449583 | [-0.702078, +0.711496] |
| NR_without_44 | dtau440 | -0.043397 | 0.452636 | [-0.722479, +0.697532] |

A frequência 440 fica mais informativa com o multipolo presente; sem ele, seu posterior é amplo e aproximadamente centrado em zero. Isso descreve estes produtos; não decide sozinho a origem dos deslocamentos do 220.

**lnB não calculado neste diagnóstico (`PRIOR_CONTRACT.json`, `lnB:null`).** Os priors de deformação não são desconhecidos. A aplicação como evidência do mesmo modelo restrito requer também justificar o prior normalizado comum dos parâmetros auxiliares e que a curva de cada leitura esteja no suporte pertinente em todo esse prior. A identidade usada na C4 está em `posterior_220_readout.py:3–7` e `REGISTRO_C4.json` (chaves `priors`/`spin_dependent_model_identity`); não é uma média de razões condicionais.

O HDF5 referencia um `prior_file` externo `QNM_prior_44_narrow.prior`, traz `prior_dict=None` e `default_prior=BBHPriorDict`. Há priors analíticos e amostras de remanescente úteis, mas não reconstruí o arquivo externo, a conversão integral de remanescente ou uma garantia global de suporte das leituras. Os 5.000 spins de prior observados vão até 0,974891/0,964738; uma amostra finita não prova um limite de suporte. Não apliquei um novo corte de spin/prior para tornar a fórmula utilizável, pois isso mudaria o contrato. Trata-se de contrato **parcialmente verificado**, não de prova de impossibilidade futura nem de falta absoluta de priors. A ausência das verdades de injeção, por si só, não bloqueia um Bayes factor.

Reuso futuro tem caminhos exatos: `{NR_with_44,NR_without_44}/posterior_samples` campos `domega220`, `dtau220`, `final_spin_non_evolved`, `final_mass_non_evolved`, `redshift`; priors nos caminhos acima e `priors/samples/`. Qualquer comparação permanece no setor 220, mantendo o 440 como nuisance livre nos dois modelos. Não equivale a um teste de GR em todos os modos e não é diretamente o setor com 440 fixo usado em grande parte do catálogo.

## Reprodução, custo e pendências

Execução numérica: **14.512 s**, uma thread, Python 3.12.3, NumPy 2.5.3, SciPy 1.18.1, h5py 3.16.0. Sem geração de posterior ou campanha de injeções. Verificações internas: integridade antes/depois, 20.000 linhas finitas por grupo nos campos selecionados, quantis ordenados, contagens de sinais, soma dos quadrantes e limites dos priors. Isso é controle do construtor, não auditoria independente de aprovação.

Os scripts recusam sobrescrever resultados. Para revisão, ler os scripts e recalcular em cópia isolada autorizada, mantendo a relação B/bis/f2_injection e os arquivos de entrada; não executar contra saídas já presentes. Comando original, repetido para `inspect_injection.py`, `diagnose_injection.py`, `check_contract.py` e `write_report.py` nessa ordem:

```powershell
wsl -e /opt/lal_env/bin/python -B "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_injection/diagnose_injection.py"
```

Não pagos por este recorte: cobertura frequentista, viés contra parâmetros completos de verdade, generalização a SNR/catálogos, isolamento causal do efeito do 44, lnB com contrato integral, validação da pipeline LVK e aprovação adversarial deste cálculo. Sem comunicação externa ou alteração de gate. Axiomas N/A.

## Localizadores e arquivos escritos

- Quantis, sinais e intervalos: `bis/f2_injection/diagnose_injection.py:39`; HPD: `bis/f2_injection/diagnose_injection.py:59`.
- Priors arquivados: `bis/f2_injection/METADATA.json:261`; checagem de contrato: `bis/f2_injection/PRIOR_CONTRACT.json`.
- Fonte normativa F2: `../TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:85`; contrato anterior: `posterior_220_readout.py:3–7,25–53` e `REGISTRO_C4.json`.

Todos os arquivos escritos nesta tarefa, relativos a B:

1. `bis/f2_injection/inspect_injection.py`
2. `bis/f2_injection/METADATA.json`
3. `bis/f2_injection/diagnose_injection.py`
4. `bis/f2_injection/DESCRIPTIVE_RESULT.json`
5. `bis/f2_injection/check_contract.py`
6. `bis/f2_injection/PRIOR_CONTRACT.json`
7. `bis/f2_injection/write_report.py`
8. `bis/f2_injection/REPORT.md`
9. `bis/f2_injection/RECEIPT.json`

Os hashes completos dos arquivos, código, insumos e fontes locais estão em `RECEIPT.json`; o recibo não inclui seu próprio hash para evitar autorreferência. Fontes online não arquivadas são identificadas por URL e alcance de leitura, sem hash fictício.
