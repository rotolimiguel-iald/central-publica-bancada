[REAL documental — NÃO-CEGO; inventário de insumos existentes e proposta de cálculo, não execução nem aceite de E0/E1]

# E0/E1 — inventário independente de entradas

Raiz R = `C:/IALD/Central de Patentes/Chatgpt`; B = `R/ORDEM_013_RINGDOWN`; I = `R/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS`; A = `I/medicao_da_ampliacao`. Os caminhos abreviados abaixo se resolvem por essas raízes; o manifesto ao final usa caminhos absolutos. Snapshot documental em 22/09/2026, com instante UTC e hashes calculados no apêndice.

**Há insumos locais para refazer a calibração escalar de E0. Não há, neste inventário, E0 calculado, E1 ajustado ou função de seleção calibrada.** Nenhum código de PARA_CHATGPT ou da bancada foi executado/importado. Nenhum posterior novo, HDF5, strain ou valor de array NPZ foi consultado. A inspeção do NPZ de calibração restringiu-se ao diretório ZIP e aos cabeçalhos NPY; os demais dados foram inventariados pelos JSONs já existentes. Não houve simulação, PE, download, job, orçamento ou início do relógio da Parte B. A futura abertura/distribuição cabe ao operador.

## 1. Contrato e cobertura possível

Fonte normativa: `R/TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:156–174`. O protocolo e a errata formal foram consultados como documentos; nenhum verificador da errata foi executado aqui. A errata emitida em `R/TUNEL/DO_CHATGPT/ENTREGA_013_ERRATA_contrato.md:1–25` substitui a pendência de emissão da candidata, não as lacunas científicas.

| Item | O que E0/E1 exige | Insumo já existente | Limite ou dependência ainda aberta |
|---|---|---|---|
| E0.1 | z por leitura, conjuntos 31/33/39 e GWTC3 18/10; σ declarado | C4, seleção, reconciliação e A/samples_summary | Refazer, sem copiar os z da gerência; zero offset só calibração |
| E0.2 | N90 e informação; rota IV MC, limiar 25, σjit 0,019/0,0228/0,030 | A, D, revisão estatística; σ por evento | Novo cálculo não feito; MC homogêneo antigo não paga heterogeneidade real nem cauda 5σ |
| E0.3 | corte pré-análise SNR/Mf/χ; ajuste e distribuição σ(SNR); contagens GWOSC | Tabelas TGR, textos, GWOSC arquivado | Conciliar convenção de SNR, deduplicar corridas e validar campos; largura não pode selecionar teste |
| E0.4–5 | tendência com intercepto livre; falsificador espúrio por leitura e GR | A/poder_eventos.py e revisão estatística como textos | Reimplementação independente; não confundir poder previsto e afastamento observado |
| E0.6 | componentes × leituras × pisos δ/5 e δ/15; condição atual | C5, C2, piso da gerência e portão v2 | Transferência ao estimador pSEOB e σ(c_calibrado) não demonstradas por estes controles |
| E0.7 | bandas O5, IC90 Poisson, cenários 3G | Observing Scenarios, Berti, Fisher v3, metadados | Denominador de exposição, definição GW250114-like e janela SNR_RD; datas continuam OPEN |
| E0.8 | herança C4, leitura por leitura, correção/σ | bis/F2_ALL_READING_TABLES_v2.json e C4 | Herança NÃO-CEGA, nunca resultado da Parte B; preservar subresolução/inaplicabilidade |
| E1.1 | c0+kσ e c(SNR), posteriores completos, covariância, splits | HDF5 já arquivados, esquemas/priors; NPZ reduzido | Ajuste antigo é de medianas; NPZ tem só 4.000 draws/evento; E1 completo não executado |
| E1.2 | seleção inspiral E pós-inspiral ≥8; seções e hashes | Três textos LVK locais | Ler trechos não equivale a artigo integral nem a eficiência de seleção calibrada |
| E1.3 | alcance das injeções LVK e RD | Diagnóstico e revisão independente F2; pareceres RD/DCC | Um ponto com/sem 44; não há curva c(SNR) paga nem mesmo lnB certificado |
| E1.4 | dois estimadores C2/C5 por SNR, N e erro | C2 antigo/expandido; C5 draws e resultados | C2 expandido tem SNR de referência 20, não varredura; C5 é outro estimador/modelo |
| E1.5 | z com nuisance livre; separação de 0 e δ pela incerteza de c0 | Dados para futuro ajuste | Não pago pelo WLS antigo; offset fixo em zero = PROIBIDA_COMO_TESTE |

E0/E1 devem conservar todas as dez leituras de `B/C1_LEITURAS_v4.json/rows`: R-A, R-B, R-MOD, R-RAIZ-0, R-RAIZ-EP4, R-RAIZ-REST, R-RAIZ-COHERENT, R-LIN, R-GLOBAL, R-PROP. As quatro leituras dominantes usadas em vários scripts da gerência não esgotam a ordem. Ausência de observável local ou de ocupação explícita produz OPEN/NÃO APLICÁVEL, não uma taxa inventada.

## 2. Dados e esquemas

### Catálogos e posteriores já arquivados

- `B/C4_CATALOG_SCHEMA.json/rows`: 33 registros com event, filename, sha256, label, N, fields, priors e summary. Arquivos em `B/cache/public/21454847/extracted/pSEOB/metafiles/{filename}`, dataset `{label}/posterior_samples`. Campos de interesse: `domega220`, `dtau220`, `final_spin_non_evolved`, `final_mass_non_evolved`, `redshift`; modos adicionais precisam ser classificados individualmente como livres ou fixos. Não generalizar o prior de um evento aos 33: consultar `C4_CATALOG_PRIOR_AUDIT.json`, inclusive os dois controles excluídos da seleção 31.
- `B/C4_GWTC3_SCHEMA.json/rows`: 18 produtos, path/member/sha256 e labels com campos e configuração textual. Dataset `{label}/posterior_samples`. O leitor estático usa fallback `final_spin_non_evolved` → `final_spin` e `final_mass_non_evolved` → `final_mass` (`gwtc3_posterior_readout.py:72–78`). A semântica está documentada em `C4_GWTC3_CONVENTIONS.json`; v4HM e v5PHM não são o mesmo modelo.
- `B/C4_CATALOG_COMBINATION.json/selected_events`: 31; `additional_control_events`: dois. `B/C4_GWTC3_SELECTION.json` registra a seleção publicada 10. `C4_GWTC3_220.json/duplicate_reconciliation` registra 12 sobreposições e seis apenas antigos. **39 = 33+6**, não 33+18. As combinações GWTC3 18 e 10 são controles separados, não novos eventos independentes somados ao conjunto recente.
- `B/C4_CATALOG_220.json` e `C4_GWTC3_220.json` contêm quantis/diagnósticos/predições, não os posteriores completos. Preservar correlações df–dtau–spin–massa quando E1 vier a ser executado. Não reconstruir draws conjuntos de marginais.
- `A/A_poder_eventos/samples_summary.json`: 39 registros; N original, grupo/caminho/hash da fonte, nomes dos campos, médias, `std(ddof=1)`, quantis 0,05/0,16/0,50/0,84/0,95, correlação df–dtau. O script de extração declara isso em `extract_samples_wsl.py:19–32`.
- `A/A_poder_eventos/samples_thin.npz`: **existe**, 5.635.216 bytes; 195 membros NPY, todos shape `(4000,)`, dtype `<f8`, chaves `{event}__df`, `__dt`, `__spin`, `__mass`, `__z`. Cabeçalhos inspecionados sem ler os arrays. O código de extração usa um mesmo índice aleatório nos cinco campos, sem reposição, semente 20260922: pareamento declarado pelo produtor, não reconferido contra HDF5 nesta tarefa. Útil para cross-check futuro; não satisfaz sozinho “posteriores completos”.
- `B/QNM_GRID.json`: 981 spins, duas entradas de modos, versão/interpolação/checagem do solucionador. É entrada tabulada existente; a futura implementação independente deve verificar domínio, modo, unidade e erro de interpolação. Não gerar outra grade neste inventário.

Os SHA dos HDF5 permanecem **[DECLARADO pelo esquema/recibo hasheado]** neste inventário: não reabri nem rehasheei esses arquivos grandes. O apêndice lista seus localizadores e hashes registrados, separado dos hashes calculados agora. A existência foi consultada apenas por metadado de filesystem. Isso não pretende renovar a auditoria de integridade de todos os posteriores.

### SNR, seleção e fontes primárias

`A/B_catalogos/gwtc5_tgr_table2_3_parsed.json`: 77 registros com event, snr, ifos, Mdet, chieff, Mf_det, chif, table e flags dos testes. É transcrição derivada das tabelas, não posterior. `rendimento_e_5sigma.py:10–18` complementa SNR de eventos antigos com regex sobre a Tabela 1 do GWTC4; o parser e os aliases GW150914/GW170104 devem ser conferidos. Não aceitar silenciosamente evento sem SNR.

`A/E_instrumento/gwosc_catalogs_raw.json`: mapas GWTC-4.0 (129 linhas), GWTC-4.1 (140), GWTC-5.0 (161), O4_Discovery_Papers (8); cada linha é lista de sete posições. O código `medir_E.py:221–227` usa índice 2 como SNR. Índices 0/1/6 correspondem a nome/GPS/catálogo nos registros inspecionados. Os campos 3–5 não têm cabeçalho nesse JSON: **não atribuir a eles Mf e χf sem conferir a origem**. `gwosc_strain_files_snr12.json` é metadado de disponibilidade/seleção, não strain; fornece campos nomeados que devem ser reconciliados com as tabelas. Não somar os quatro catálogos sem deduplicação por identidade/GPS. Contagem por catálogo não é automaticamente contagem por corrida nem exposição observacional.

Convenção proposta para reproduzir o ajuste de referência: **SNR das tabelas TGR**, com tabela/campo/estimador explícitos por evento; contagens GWOSC em tabela separada, identificadas como GWOSC, sem misturar seus números no fit TGR. Alternativa futura: refazer tudo com GWOSC se houver cobertura íntegra; declarar a mudança. Mesmo a fonte TGR distingue mediana v5PHM em O4 de MAP Phenom em eventos antigos. SNR da rede inteira, SNR pós-inspiral e SNR_RD numa janela determinada não são intercambiáveis.

Leituras primárias desta tarefa foram **pontuais, não artigos integrais nem só abstracts**:

| Fonte local | Trechos consultados | Conteúdo relevante e alcance |
|---|---|---|
| A/B_catalogos/gwtc5_tgr.txt | §7.2, :4331–4347 e :4648–4662 | Seleção SNR ≥8 nas duas partes; mudança de estimador SNR por era; seleção não incorporada à inferência hierárquica e possível preferência por dtau positivo |
| A/B_catalogos/gwtc4_tgr3.txt | §2.2, :3081–3096 e :3540–3555 | Mesmo limiar e ressalvas de correlação com parâmetros astrofísicos/priors e seleção |
| B/cache/literature/gwtc3_article_v3.html | §VIII.1.2, :11284–11373, parágrafos selecionados | pSEOBNRv4HM; seleção nas duas partes; exclusão dos dois controles; tendência positiva e prior assimétrico como possibilidade |
| A/B_catalogos/observing_scenarios.txt | Tabela 2, :473–513 | Alcances projetados BNS/BBH, limiar de um detector; BBH O4 1400–1600 e O5 2500 Mpc; não cronograma atualizado |
| A/B_catalogos/berti_bhspec.txt | §7.1.1, :14896–14912 | Cenário populacional/Fisher e ordens de grandeza de taxas acima de SNR_RD 50/100; janela exata não estabelecida pelo trecho |

Não consultei web nem atualizei cronogramas. O5/3G entram como fontes históricas arquivadas, não como afirmações de agenda vigente. As taxas de 3G citadas na revisão remetem a trabalho primário adicional: sua derivação não foi auditada integralmente aqui. E1.2 integral permanece trabalho futuro; estas âncoras não simulam seu aceite.

### Controles e resultados já auditados

- `B/bis/F2_ALL_READING_TABLES_v2.json`: 60 linhas dataset×leitura, incluindo lnB, banda, correção, σ, centro, z, GR_HPD, veredito, motivos, escopo e event_ids. Preferir sua tipagem explícita aos números soltos de scripts históricos. Herança científica somente no domínio declarado.
- `B/C2_TRAJECTORY_RECOVERY.json` é o controle antigo. `B/bis/C2_TRAJECTORY_expanded_1000.json` tem 11 cenários, dois regimes e 1.000 fits/célula, `noise_free/recolored/fits`, médias/DP/EP, bordas/falhas; referência SNR=20, Mdet=68,1, spin=0,68. Não contém séries das trajetórias. `C2_ADENDO_OBSERVAVEL_v2.md` especifica 128/2048, biblioteca de 256 intervalos e EP agrupado. Não confundir o antigo viés positivo com o resultado novo, que mudou janela e ruído. Nenhum deles entrega sozinho uma curva em SNR. Variância da fase Cauchy não existe; DP do estimador limitado é outro objeto. R-PROP não tem célula local definida.
- `B/C5_IMR_RECOVERY.json`: 576 células, N declarado 206/célula, famílias/PSD/leitura/SNR/recuperação, vieses, cobertura e índices de draws. Dois NPZ existentes em `cache/imr_recovery/O4_draws.npz` e `O5_draws.npz`; não lidos em valores. A validação e `bis/C5_WALL_COUNTS_013BIS.json` ajudam a separar células calibradas condicionais e reprovadas. O parâmetro ajustado a não vira dtau sem a convenção correspondente. Não equiparar recuperação com remanescente fixo à PE pSEOB com massa/spin livres.
- `B/C5_FISHER_v3.json` e `PORTAO_DO_PODER_013_v2.json` são as versões tipadas atuais deste inventário. Incluem métrica de log-decay, σ efetivo em dtau e correção do uso linear. `bis/F4_GW250114_WINDOW_POWER_NORM.json` registra norma aproximada na janela, não SNR pSEOB da rede. Não transferir a âncora histórica “40” para 10 tM sem transformação demonstrada.
- `B/bis/f2_injection/{REPORT.md,DESCRIPTIVE_RESULT.json,METADATA.json,PRIOR_CONTRACT.json,RECEIPT.json}`: dois grupos `NR_with_44`/`NR_without_44`, um único ponto de injeção. **Reuso E1 dos resultados auditados:** `B/bis/F2_INJECTION_INDEPENDENT_REVIEW.md:1–19` aprova as contas descritivas no alcance declarado. Seus resultados não são curva c(SNR), viés médio de população ou cobertura frequentista; lnB continua null. A ressalva R1 é de guardas assert sob −O e não invalida os números arquivados. A correção v2 solicitada depois será exclusivamente operacional, sem nova ciência ou substituição desses resultados. O suporte local da KDE usa 20.000 linhas; o conteúdo em GR usa treino 16.000/consulta 4.000, conforme a revisão.
- `bis/F2_RD_APPLICABILITY_REVIEW.md/json`: RD auditado não fornece deformação 220 livre; desvios livres encontrados são do 221. Não fabricar df220 de parâmetros Kerr fixos. `bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.md/json`: release DCC localizado, mas os textos examinados não provam posterior conjunto por evento df/dtau/spin disponível nesse pacote. Descoberta não equivale a joint utilizável. Pickles e notebooks não executados.

## 3. Dependências e diferenças que o cálculo deverá explicar

Os scripts da gerência são referências de fórmula e comparação, não bibliotecas a importar. Vários escrevem na carga do módulo; alguns referenciam cwd, scratch e diretório Temp externo à raiz. `extract_samples_wsl.py:9` contém destino antigo externo; `refazer_estatistica.py:13` espera `medir`, enquanto a cópia entregue está em `medicao_da_ampliacao`. Não “consertar e rodar” esses scripts. O apêndice registra imports por AST, sem execução.

Dependências propostas para futura implementação independente: stdlib para custódia/JSON/CSV; NumPy para álgebra; SciPy para interpolação/QNM tabulado, otimização/quantis e incerteza; h5py **só quando autorizada a leitura dos posteriores de calibração existentes**. Não precisa bilby, dynesty, geração LAL, pycbc, strain ou PE para E0 escalar. `/opt/lal_env` é ambiente existente declarado nos recibos; versões/instalabilidade não foram sondadas nesta tarefa. Não criar venv ou instalar pacotes agora.

Diferenças obrigatórias no confronto com a gerência:

1. `samples_summary` usa DP ddof=1; B/C/D e revisão usam largura 90%/(2·1,645), com pequenas variantes de arredondamento. E0 propõe DP como principal onde disponível e coluna gaussiana equivalente para comparar; não trocar rótulos. Para GWTC3 18/10, faltam neste resumo os 12 produtos sobrepostos antigos: não substituir pelo posterior v5 para fingir DP da v4. Pode usar quantis declarados nesse conjunto ou extrair os DP dos HDF5 antigos em etapa autorizada.
2. `median_prediction` avalia no remanescente mediano; `shift_05_50_95[1]` é mediana das predições nos draws. Não são operações idênticas. Declarar qual entra em cada cálculo e medir a diferença futura.
3. z_matched, z_common e z_slope são estatísticas distintas (`A/A_poder_eventos/poder_eventos.py:104–131`). O N espúrio da revisão usa afastamento da média observada contra a média predita, não z_matched de poder.
4. `rendimento_e_5sigma.py:29–35` usa OLS em ln–ln e `resid.std()` (ddof=0); seu centro é mediana condicional sob modelo lognormal. Diferenças por graus de liberdade, parâmetros do fit, amostra e convenção de SNR devem aparecer separadas.
5. `C_piso_sistematico/s03_sinais_e_catalogo.py:23–48` e `revisao_da_gerencia/estatistica_poder/refazer_estatistica.py:76–89` ajustam **medianas** por WLS, não likelihood dos posteriores completos. Os alvos −0,061±0,068 e +0,79±0,37 da ordem são referências de comparação, não números que esta tarefa reobteve.
6. O MC antigo de D gera `s_i2=np.full(N,sigma_meas**2)`; a grade antiga nem inclui 0,0228 em todos os produtos. E0 exige os três valores da ordem e σ_i reais. Formas score/Asimov e N50 não são poder MC ≥90% nem calibração de cauda.
7. As bandas O5 e 3G misturam hipóteses diferentes de ganho, volume e população. Não aplicar ganho de SNR duas vezes nem transformar exposição-calendário em live time certificado.

## 4. Proposta independente para E0 — desenho, NÃO EXECUTADO

**Entradas congeladas e guardas:** selecionar arquivos existentes por hash, contrato de campo/modelo/unidade e lista de eventos; registrar falhas/ausências. Montar as cinco populações separadamente e dez leituras com tipo de saída. β será sempre `ALPHA_FINE_CODATA_2018*sqrt(e)` em runtime. Implementar fórmulas por equações lidas das fontes, sem importar `tgl_ringdown_prediction.py`; compará-las depois com valores arquivados como controle, sem usar a comparação para esconder divergência.

Para ensemble exponencial, δ_i=−x_i/(1+x_i), x_i=Γ_i τ_GR,i; usar expressão estável para efeitos muito pequenos. R-MOD exige QNM exato e domínio corrotante admissível, mantendo estatuto CONJECTURE. R-RAIZ-COHERENT requer ocupação e janela, sem δτ universal; R-PROP carece de ponte para damping local. R-GLOBAL é controle relacional nulo sob sua hipótese. Nulos/subresolução/OPEN são linhas da tabela, não eventos ou leituras descartados.

**Calibração gaussiana de média:** w_i=σ_i⁻², Iτ=Σw_i, δ̄_w=Σw_iδ_i/Iτ. Reportar separadamente

`z_matched = sqrt(Σw_i δ_i²)`;
`z_common = |δ̄_w| sqrt(Iτ)`;
`z_slope = sqrt(Σw_i(δ_i−δ̄_w)²)`.

O último projeta fora o intercepto, assumindo o modelo linear/erros declarados; não é significância física já medida. Inversão singular deve retornar NÃO IDENTIFICÁVEL, nunca fallback silencioso. Se δ_i é constante, a alavanca de tendência é zero mesmo com muitos eventos.

Sob repetição iid da **mesma mistura** e filtro gaussiano de efeito conhecido: N50=25/E[(δ/σ)²]; N90=(5+Φ⁻¹(0,90))²/E[(δ/σ)²]; imprimir fator N90/N50≈1,578. Não transportar automaticamente esse fator à rota IV ou a nuisance estimado. O alvo público será informação esperada, Iτ,90=N90 E[σ⁻²], e equivalentes Iτ,90/(1/0,058²). Para efeito constante, Iτ,90=(5+Φ⁻¹(0,90))²/δ². Quando δ depende do spin, Iτ sozinho não caracteriza poder sem a distribuição conjunta de δ e σ: guardar também Σδ²/σ² e a população assumida.

**Falsificador espúrio:** refazer, para cada conjunto/leitura, `z_obs=(m̄_w−δ̄_w)*sqrt(Iτ)` e `N_spurio,50=n*25/z_obs²` sob repetição do mesmo viés/mistura; para GR, δ=0. Identificar como extrapolação NÃO-CEGA de viés persistente, não poder para TGL nem descoberta. Comparar a GR≈191 citada pela ordem somente após o cálculo, com diferenças de σ e centro explícitas. Propagar incerteza do viés; z_obs=0 dá alvo indefinido, não evidência de ausência de sistemática.

**Distribuição de informação antes da análise:** ajustar lnσ=a+b lnSNR, registrar covariância do fit e convenção da dispersão s. Se adotado o modelo lognormal [INPUT], medianaσ=exp(μ), mas `E[σ⁻²|SNR]=exp(−2μ+2s²)`; não usar simplesmente o inverso quadrado da mediana. A distribuição dos parâmetros do fit também deve ser propagada. Contagens por cortes SNR/Mf/χ vêm de metadados GR/tabelas previamente definidos, nunca de σ_dtau observado. Subamostras por σ permitidas em E1 são diagnóstico de calibração, não critério para selecionar o teste. Massa detector/fonte, spin efetivo/remanescente e SNR de rede/janela precisam de campos distintos.

**Tendência e nuisance:** refazer a projeção do intercepto e a lei de escala com a mesma mistura; não extrapolar inversão de matriz mal condicionada. O E1 futuro deverá usar os draws completos e priors por evento, preservar correlações e estimar c0,k,covariância/splits. Uma via é reciclagem de posteriores por razão população/prior, com normalização de seleção explicitada; um prior auxiliar diferente exige seu fator correspondente. Ter o limiar ≥8 não fornece sozinho a eficiência α(hiperparâmetros). Se esta não puder ser estimada dos dados existentes, registrar seleção não calibrada, sem promover o WLS a likelihood populacional completa. Identificabilidade de c0 contra δ da leitura deve ser testada, não imposta por prior que a encerre artificialmente.

**Rota IV, somente desenho:** perfilar μ livre em `y_i ~ N(μ, σ_df,i²+σ_sys²+σ_jit²)` como aproximação declarada, e confrontar posteriormente com a likelihood dos posteriores. μ deslocado não é predição TGL. Comparar nulo com σ_sys versus alternativa com jitter, usando LRT>25 e σjit={0,019;0,0228;0,030}; não fixar arbitrariamente σ_sys=0 como fato. Desenhar MC heterogêneo, sementes, resolução/busca de N e IC binomial do poder; não afirmar ≥90% apenas por estimativa pontual ruidosa. A fronteira e a heterogeneidade requerem calibração do nulo em E2; o MC de poder não certifica sozinho 5σ. Na aproximação de variância pequena o peso é σ_df⁻⁴, com referência df específica, **não** os equivalentes τ de 0,058. Transferência da largura ao estimador pSEOB e σ_sys continuam OPEN; sem elas N é cenário/limite, não alvo operacional aprovado. Cauchy/Poisson/determinístico não se reduzem automaticamente ao browniano.

**Sistemática, taxa e herança:** montar matriz de componentes medidos e ausentes por leitura; pisos |δ|/5 e |δ|/15 marcados INPUT. Separar magnitude de discrepância, dispersão entre pipelines e incerteza residual σ(c_calibrado); um não substitui o outro. Ausência de calibração mantém condição não demonstrada e portão fechado. Para taxa com n eventos e exposição T definida, propor IC90 exato Poisson `[χ²_(2n;0,05)/(2T), χ²_(2(n+1);0,95)/(2T)]`, limite inferior zero se n=0; T/critério ainda devem ser justificados. Exibir bandas BBH 1,56–1,79, PSD C5 1,99 e teto BNS 2,06 separadamente; nunca “anos” como promessa. Herança C4 deve mostrar veredito, correção/σ, GR dentro/fora de 95%, suporte e origem NÃO-CEGA. Nada disso muda gate.

## 5. Situação documental

PAGO aqui: requisitos inventariados, entradas/localizadores/esquemas estáticos, hashes dos arquivos de controle lidos, dependências e proposta independente. NÃO PAGO aqui: E0 numérico, E1 completo, eficiência de seleção, curva de viés LVK versus SNR, transferência do jitter, σ_sys pSEOB e abertura/execução da Parte B. Nenhum aceite integral dessas etapas é declarado.

Axiomas: N/A; teoremas novos: 0. A primeira listagem ampla por nomes encontrou acesso negado em dependências alheias ao recorte; não foi usada como prova de ausência. Uma impressão de trechos falhou por encoding cp1252; repetida em UTF-8. A contagem de linhas dos textos foi corrigida para separação por LF, evitando que form-feed de extração PDF alterasse os localizadores. Nenhuma dessas ocorrências escreveu nas fontes.

Único arquivo escrito **neste inventário**: `B/bis/E0_E1_INPUT_INVENTORY.md`. O trabalho de robustez v2 autorizado posteriormente terá recibo e lista próprios. Não foram produzidos PORTAO_DA_AMPLIACAO_V1, NUISANCE_V1, registro E2 ou entrega formal.


## Apêndice — recibo do inventário por script

UTC 2026-09-22T19:12:11.733189+00:00; 86 SHA256 calculados em bytes por Python stdlib. AST/JSON lidos sem importar código inventariado. Não é certificação científica dos valores.

Autorização superveniente: operador iniciou Parte B em 2026-09-22T19:06:33.802143Z, deadline 2026-09-24T11:06:33.802143Z. Este documento conserva o inventário anterior ao cálculo científico; E0 autorizado depois terá custos e resultados em bis/e0_core.

### Hashes calculados agora

| Caminho absoluto | Bytes | SHA256 calculado |
|---|---:|---|
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/TUNEL_PROTOCOLO.md` | 5425 | `4234902dc6f5e03c237f3f7a53f066be3d340f9ebfac2934bb3d61fc09a000f2` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md` | 91912 | `a907d07bc484b53cc6db237dc5972f4dcc47be03ad084c832201bb648981454b` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013_ERRATA_contrato.md` | 42681 | `13d8c47e8faaa38aa48a5a6e2cb138e7e0cd06ed3edc5989d47b01c16c2a751f` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C1_LEITURAS_v4.json` | 35419 | `126270a896d8589870954b209155f26a8b08295839b31e0e9a6e28e512621980` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/QNM_GRID.json` | 169231 | `4f34367a0906023836fcf8013ada3ccef48877a17f59f697b9dabc25a2494b24` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/tgl_ringdown_prediction.py` | 8382 | `fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/catalog_220_readout.py` | 8370 | `c2b43d633b39195a086a7961cdcc9842ec90fb4d5b25cf5114641b33191707de` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/gwtc3_posterior_readout.py` | 10684 | `f1e876b1d41a318030613d3c09ef9e882103d2ff2d98dbc12151987694abfe6b` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_CATALOG_SCHEMA.json` | 169206 | `9339c27512482f55b6bfd0b76364ea37cae2abcbaf65f16d3d36a50b9ed92724` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_CATALOG_PRIOR_AUDIT.json` | 115403 | `d5a8ca83e7f4895961d15186c3b81fd91732e8f720ffe5a9bb80383e4083aaf1` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_CATALOG_220.json` | 673228 | `93bdc413130d294acde91ec03f8392b8d9c5ec5b33fdc97274371656503d8e17` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_CATALOG_COMBINATION.json` | 12167 | `f3d8c1959ded3efd15045923ce0cbafe7356ec888ced1934d8d0c183046d0d01` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_GWTC3_SCHEMA.json` | 368887 | `59570d2dd11e6077198dffb39f9d8addcc06945c07f88c822905bebbaa7b7a7e` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_GWTC3_CONVENTIONS.json` | 6131 | `01205e018dc407304194cc18d04b9d9ad42b3b01cc42659b7c8cbd950770bfe1` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_GWTC3_SELECTION.json` | 1563 | `ef18f3b0495d58bffc5f968f86ca860eefd3becb570cd75bfc9f88fa8fee5dd3` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_GWTC3_220.json` | 402498 | `d9dc9b09a8d91dc7f85c5e849091db619b1c22a633b09c97d82bcf434e9c6053` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_GWTC3_COMBINATION.json` | 7785 | `f88c2aa84f98891734f6dc67229a97777bd201ffca40bc479c86bc2fd4fd1f4e` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_GWTC3_PUBLISHED_COMBINATION.json` | 9307 | `f6dbd853223b803984d352aebe3fd64f786b3f26458988cbb4b37a752f8b1ddd` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_PYRING.json` | 15776 | `76af853137f3e7d3396f001eb44cfc3a6366d2e92b9d9ed7b8454ec8b0f35b0a` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_JOINT_MODES.json` | 9740 | `8b2e0fea734caed23f05c3a9f9a2f3f7aaa8f19ed71d2f9d9a841129739e742f` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REGISTRO_C4.json` | 2768 | `2bebc171ddbcef43d7b50b9076dd806b64829a05a769b6e4fe23b73ec121ac59` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C2_TRAJECTORY_RECOVERY.json` | 271259 | `339be42bec67a48e1e3341d678ac9bc0804c6e1db035e6b4b57df62673eafd38` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C2_ADENDO_OBSERVAVEL_v2.md` | 7695 | `6eb9df8379ebd6ae3cd7e0c2e0ffbd70dfe78ccb5ce3b68418c8ac51c29bb6b1` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/trajectory_recovery.py` | 8825 | `a5648ee2303159fb8cd083d9f490ff6d1ec0d1231f2a9fb6e8163ea93de01b33` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/measure_c2_013bis.py` | 9106 | `b63a79f428e3c40b4c5e8dacbbcfdc4c762e994ce0cb2850611bba21c948cd3a` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_IMR_RECOVERY.json` | 493476 | `bda4441856c23a643be6dc467b65059c4fc968d54971a73490710ffc67568cb6` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_IMR_RECOVERY_VALIDATION.json` | 22270 | `0f40a767502a627ab68dcb801e44486d446c0f3d2582f6e668ab719766a2c8c7` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/imr_recovery/O4_draws.npz` | 904874 | `a79ab602d4b9fa2a1c9cf30de3cdf0ad663703a557ea88574473ec45e646c487` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/imr_recovery/O5_draws.npz` | 905214 | `1feacc7bf0f4e668a9afd8249778f21bc201c92e4e2f22dddc38f88bc3410434` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_FISHER_v3.json` | 438271 | `ef7a800369ba07328852b2ffe6a54c13f9b20476775f557113ca31fc50a5a22b` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/PORTAO_DO_PODER_013_v2.json` | 71536 | `c2972e3cc32286532908875b2a3ddb5d168d0669a6846e3e2c1d16e855c2b133` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_BIAS_ABLATION.json` | 35276 | `6fd926f371e38aa7fec9c0782e48230dc169087086ea3d0a76a309e14a5ea54f` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_OVERTONE_ABLATION.json` | 55858 | `21b28ee843422f68d1c63a12f1d74736807f8d0bc99b424fb5ae5d92897ea8bd` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_RECOLORED_NOISE.json` | 9309 | `088fe6927b17e8461df6a05c0d129da28654cf001e3833df24713cfe0d3ec477` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_FISHER_EMPIRICAL.json` | 139909 | `00fbe67f5aa5b38212e8b6c4e6654d09e6cbc23b9e0e5306ee3d7cb77a3bc508` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C7_INDEPENDENT/tables/event_reading_predictions.csv` | 89341 | `14ba80daf42a49721e4500c72073b3ca90384f40a74f10fc18f5447480cdcdfc` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_ALL_READING_TABLES_v2.json` | 123632 | `761eb108231aef3db26a07adcecab08884b299ad5ffb7b45a0360516d63e178f` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/C2_TRAJECTORY_expanded_1000.json` | 4681894 | `9d734d976146188ae83a9557ae947f1021c7cfef26c49e998f39b1c1a128d691` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/C5_WALL_COUNTS_013BIS.json` | 5497 | `df21c6792664e63df63f4496ae7a725c7e5eb903d7ed57ac40f2b0636ec38723` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F4_GW250114_WINDOW_POWER_NORM.json` | 1328 | `6accdff1858d3a6a67298d231f4a3090f62ff735438359abfde70dcb01317b8a` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_CONTROL_EXTRACTION.json` | 348939 | `88384c3eb4240dc159f0aa3b16d9353b5b63bdb990415e8d1073f9507d366e97` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_CONTROL_SCHEMAS.json` | 302129 | `e54e648e06625cc6f96094c7c16d4b89cd40001498d1f4fd5cd9c7f30f417dbf` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_RD_APPLICABILITY_REVIEW.md` | 21059 | `8e48acb49334c3d66b424320d37369b5bffc2ad9f938ef050bd788d51ad4c87c` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_RD_APPLICABILITY_REVIEW.json` | 437681 | `2076f9fc296b30063dbe1272f834c0135e33dcd015fc948d50362a0a84daa5b3` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.md` | 10241 | `e988802f34ab1a569203bc88d1cefe2653378287bb1f52fbb1a81e0e9da81362` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.json` | 5285 | `a406d33b88b717dd32f1271b50c3432ddabb375bf6f6c92a03561805b13ee6d7` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_injection/REPORT.md` | 12992 | `720b041f207520bbe36264b1d77f475794a077bbbaa5840d486f634cc85357ca` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_injection/DESCRIPTIVE_RESULT.json` | 57206 | `bc1fec39f21d92dd19d0953d4d9ae14bae4b2eed5ea80aa60a405fc42e091ecc` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_injection/METADATA.json` | 68671 | `b56c22e54d99b98d0693e915326f410f193063928248e859902df6692625f305` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_injection/PRIOR_CONTRACT.json` | 2849 | `1900f0bc77d98e99be08e5e476388975f5b2d90b68da561555c36349876dad1e` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_injection/RECEIPT.json` | 3309 | `0d4120d77f179d4d4d3aeb90c52168bf56365b8796bbdf726e9529934058db77` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_INJECTION_INDEPENDENT_REVIEW.md` | 10652 | `e518a10af574f65bafedc0f719af90fca857c7a49636e9da01d0bd437058ed89` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/literature/gwtc3_article_v3.html` | 2702327 | `9c5271fba4aaa144bafa904e40c1dfe3e853b60b9e705be267dd22a0236f8ee2` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json` | 1536 | `2b3cfefd17cb8f3df845172a3b41f6e457b92b2c5bb164128aa0b40e8919355f` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/extract_samples_wsl.py` | 3522 | `fb1ef7aff12d0fb93c57a9269babb13a5f166fcf70e4dacdcc43517e74904062` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/poder_eventos.py` | 19554 | `cf3c61cdd5a1536ac9f3c23bf0bf79cc1fc394cac94701ad90f9f3132b96ba7c` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/samples_summary.json` | 63530 | `d1517c04e0f5fb07f208db8f08bd206550503c210e9129abc041a3d53f05b0f7` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/samples_thin.npz` | 5635216 | `6adedcde20706c7de9477b8e361cfaa990a9eae8f482f30f82ebd7f9ae99b805` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/A_poder_eventos.json` | 50243 | `1219a98f08b4e1ebe05ffbc511f64efcd71a4a71f60c76e8c36d45a6deeea521` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/A1_por_evento.csv` | 25931 | `d02c185c876d6094941059c7b3808a41057f29958feeb9ce02cc0dbfb226e3bb` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/rendimento_e_5sigma.py` | 5953 | `23aeab8ad4b346453136fc01ae7f3b929b10e4c2a459de62560182ae11e4210a` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/RENDIMENTO_E_5SIGMA.json` | 6880 | `57ff7bacbe0d6085b960440fe5c6bbc9480ce7a492aae5bba0ee61771ff6eef3` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/n5sigma_from_catalog.py` | 3138 | `482b2c1b0882cfbe38aa2be0473dfe498a78baabd5c95605c61a4df57c486b6c` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/N5SIGMA_FROM_CATALOG.json` | 24573 | `1e48703be9ff9a0f9efa302084ddfe0bf389ebe1bdd4a9d2d3529f891fca08df` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr_table2_3_parsed.json` | 23711 | `4119e5f8279dfd15b2eb7e32bef191195c990350498be4e491d176b9ec7e607e` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt` | 248915 | `d523ae94f23f40b55e7688702b444cf35fb2c2dc90610a6d03bfbd2ef8eefccf` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc4_tgr3.txt` | 214415 | `db4c7edbc0861946d1eea6873b191959231df0c5df3c9ce44276d5272c5129a8` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/observing_scenarios.txt` | 178305 | `323fb02315ea06646a1db044eaffccdb603f6046cdf9d0fe6668d19a6bde58a6` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/berti_bhspec.txt` | 973563 | `18ac2ff1d6c5b3cefe4b13f7d7d1a057b66185d575203fe0ab77f4421037e44a` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/FONTES.json` | 7544 | `ffb56370ae41d6a5a1baaf04f5cde4f35857029ebf51527313ec5beae3fa57dd` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/C_piso_sistematico/s02_measure.py` | 17236 | `b5e4a1103fa270048e53e0df92e69126efc55f43f14af3bea08b0f91897d3441` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/C_piso_sistematico/s03_sinais_e_catalogo.py` | 8806 | `10dabb10c7c0d643af35e70a094c50178b2ce35c07298888a2934a74fcde98e3` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/C_piso_sistematico/C_piso_medicoes.json` | 227627 | `cfdb198d667df8f73ac6d35efff859dcbbcb43481cd673fbf554e1cb56e94db0` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/C_piso_sistematico/C_piso_sinais_catalogo.json` | 27614 | `92e26c7cdf3ed1f4ea78329ffdc5aae14d79ea5398bcf18202ac38ad8b1b98fd` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/D_realizacao_unica/d2_teste_populacional.py` | 6964 | `3573e779d9dcff9936bba4b69f61749116785e35e3f6f666c1b9f0b5d8937f05` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/D_realizacao_unica/d2_resultado.json` | 5861 | `d7402bae7f41da00efa5fd1e359f08aa4a04fd8afb56adc0b41421104cf51836` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/D_realizacao_unica/d3_catalogo_exploratorio.py` | 7506 | `7e792fd0fd3aa369b6fb8204b85dad1dce8bbe0054b26da7c8067b2e71022c00` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/D_realizacao_unica/d3_resultado.json` | 24022 | `3a1b4fca024cdb7819534df73d28fab6b5d1d522c57817ea5052bd2045f8bae9` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/medir_E.py` | 21750 | `a2e30d68d4aa4a86fdbf7d6538cfb0e6da9fea47cddd5b25ff9d5ee279341c91` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/MEDICAO_E.json` | 35816 | `79b4c14add2f5268d76784224b71518e0d3bc6dadd9ca5c26b138cfef943cece` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/gwosc_catalogs_raw.json` | 31194 | `7aa04f5caea66005ec2da2bfadec29c70d2466371cc0c1db140fd3d2f5324ca3` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/gwosc_strain_files_snr12.json` | 10774 | `3de666ae5d649a4f179adab3d98ccdd2e7c64271528410f47711a6805d187d57` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/estatistica_poder/refazer_estatistica.py` | 9287 | `4b394f9b64879516273e87a3b0c18c22af423f23ab9cd784ae08504143d21356` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/estatistica_poder/REFEITOS_REVISAO.json` | 6264 | `30c03a185f6194d924c0333f725a4cb55e109a11842ec08402139e24f2e055bf` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/ceticos/cetico2_L149_refeito.json` | 657 | `b59d42a70b15cd6d638526aaa7d3f0e737bc08d12b22dc5bc98c868ca373943c` |
| `C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/ceticos/cetico2_refeito_O5.json` | 3193 | `10fc43c340c99b152dc01f9ec1f5d272bbe582ed201f3aa2e64a09fc04321f43` |

### Esquemas JSON estáticos — chaves iniciais, não JSON Schema normativo

| Caminho relativo a R | Estrutura |
|---|---|
| `ORDEM_013_RINGDOWN/C1_LEITURAS_v4.json` | status:str; created_utc:str; rows:lista(10); source_references:objeto(9); FP5_source:objeto(4); hypothesis_selected:bool; clock_evidence:objeto(7); numerical_source:objeto(2); limits:lista(7); supersedes:str; supersedes_sha256:str; updated_utc:str; origin_generator_sha256:str; v4_generator:objeto(2); evidence_validator:objeto(2); numerical_controls:objeto(2) |
| `ORDEM_013_RINGDOWN/QNM_GRID.json` | status:str; spins:lista(981); modes:objeto(2); qnm_version:str; interpolation:str; seed:int; n_validation:int; independent_solver_check:str |
| `ORDEM_013_RINGDOWN/C4_CATALOG_SCHEMA.json` | source_record:int; rows:lista(33); N_events:int; duplicates:lista(0); GW250114_matches_17018009:lista(1); not_read:str |
| `ORDEM_013_RINGDOWN/C4_CATALOG_PRIOR_AUDIT.json` | rows:lista(21) |
| `ORDEM_013_RINGDOWN/C4_CATALOG_220.json` | status:str; N_events:int; N_posterior_draws:int; duplicate_policy:str; rows:lista(33); catalog:lista(8); not_done:lista(4) |
| `ORDEM_013_RINGDOWN/C4_CATALOG_COMBINATION.json` | status:str; selection_source_sha256:str; selected_events:lista(31); additional_control_events:lista(2); exclusions_basis:str; common_deformation_GR_diagnostics:lista(8); catalog:objeto(2); physical_model_caution:str; unresolved:lista(4) |
| `ORDEM_013_RINGDOWN/C4_GWTC3_SCHEMA.json` | status:str; record:int; archive_sha256:str; rows:lista(18); source_sha256:str |
| `ORDEM_013_RINGDOWN/C4_GWTC3_CONVENTIONS.json` | status:str; date_utc:str; sources:lista(2); assertions:objeto(4); release_files:int; limitation:str; correction:str; misleading_source_comment:str |
| `ORDEM_013_RINGDOWN/C4_GWTC3_SELECTION.json` | status:str; source:str; source_path:str; source_sha256:str; table_id:str; table_events:lista(12); excluded_by_authors:lista(2); selected_events:lista(10); archive_products_outside_table:lista(6); basis:str; interpretation:str; reading_scope:str; no_article_parameter_values_used_as_samples:bool |
| `ORDEM_013_RINGDOWN/C4_GWTC3_220.json` | status:str; registration_sha256:str; source_archive_sha256:str; N_events:int; duplicate_reconciliation:objeto(5); prior_semantics_source:str; damping_convention_source:str; limitation:str; rows:lista(18); catalog:lista(8) |
| `ORDEM_013_RINGDOWN/C4_GWTC3_COMBINATION.json` | status:str; selected_events:lista(18); N_events:int; selection:str; input_sha256:objeto(4); common_deformation_GR_diagnostics:lista(4); catalog:lista(8); duplicate_reconciliation:objeto(5); combined_with_current_release:bool; limitations:lista(4) |
| `ORDEM_013_RINGDOWN/C4_GWTC3_PUBLISHED_COMBINATION.json` | status:str; selected_events:lista(10); N_events:int; selection:objeto(13); input_sha256:objeto(5); common_deformation_GR_diagnostics:lista(4); catalog:lista(8); duplicate_reconciliation:objeto(5); combined_with_current_release:bool; limitations:lista(4) |
| `ORDEM_013_RINGDOWN/C4_PYRING.json` | status:str; event:str; N:int; registration_sha256:str; posterior:objeto(4); posterior_weighting:str; version_scope:str; prior:str; point_prior_density_ratio:float; no_duplicate_event:bool; GR_HPD_content:float; signed_spin:objeto(5); GR_HPD_test_N:int; GR_support:objeto(2); remnant_fit:objeto(9); quantiles:objeto(4) |
| `ORDEM_013_RINGDOWN/C4_JOINT_MODES.json` | status:str; event:str; N:int; source_sha256:str; registration_sha256:str; priors:objeto(4); uniform_independent_prior_density_ratio:float; GR_HPD_controls:lista(3); GR_support:objeto(2); posterior_correlation_matrix:lista(4); rows:lista(8); independent_five_dimensional_KDE_quadrature:lista(2); quadrature_minus_residual_KDE_logB:float; scope:str; hypothesis_status:str; no_double_count:str |
| `ORDEM_013_RINGDOWN/REGISTRO_C4.json` | status:str; date:str; scope:str; known_information:str; readings:lista(10); primary:objeto(3); secondary:str; catalogues:lista(2); duplicate_policy:str; exclusion_rule:objeto(6); KDE:objeto(5); priors:objeto(4); spin_dependent_model_identity:str; small_correction_policy:str; unresolved_mapping:str; permitted_verdicts:lista(5) |
| `ORDEM_013_RINGDOWN/C2_TRAJECTORY_RECOVERY.json` | status:str; seed:int; beta_runtime:float; N_per_cell:int; reference:objeto(2); sampling_hz:int; sample_count:int; GR_reference_SNR:float; estimator:str; covariance:str; whitening_residual:float; physical_scope:str; Cauchy_warning:str; source_clock_note:str; preserved_control:str; rows:lista(11) |
| `ORDEM_013_RINGDOWN/C5_IMR_RECOVERY.json` | status:str; registration_sha256:str; number_of_cells:int; N_per_cell:int; results:lista(576); draws:lista(2); status_counts:objeto(3); joint_mixture_criteria:lista(48); original_C5_and_C6_modified:bool; no_target_strain_read:bool; scope:str; no_free_physical_partition_selected:bool |
| `ORDEM_013_RINGDOWN/C5_IMR_RECOVERY_VALIDATION.json` | status:str; registered_inputs_unchanged:bool; criteria_recomputed_cells:int; independent_SVD_cells:int; independent_SVD_draws:int; max_lnB_abs_difference:float; max_same_family_noiseless_residual_squared:float; checks:lista(96); production_sha256:str; result_sha256:str; verifier_sha256:str; scope:str |
| `ORDEM_013_RINGDOWN/C5_FISHER_v3.json` | status:str; inputs_sha256:str; parameters:objeto(5); records:lista(384); same_source_R_B:lista(4); mass_spin_free:objeto(5); not_done:lista(5); interpretation:str; supersedes:str; supersedes_sha256:str; free_parameter_scalar_gaussian:lista(48); completed_elsewhere:lista(2); nonblind:bool; analytic_additional_readings:lista(2); same_source_R_B_linear_historical:lista(4); correction:objeto(4) |
| `ORDEM_013_RINGDOWN/PORTAO_DO_PODER_013_v2.json` | status:str; created_utc:str; bases:lista(5); readings:lista(50); all_fixed_source_below_5:bool; failed_attempt:str; conventions:str; measured_psd_control:lista(16); peak_to_window_illustration:objeto(3); source_free_multimode_RB_diagnostic:lista(8); C5_stop_rule:str; maximum_verdict_if_calibrated_but_underpowered:lista(2); current_verdict:str; dependencies:objeto(17); opening_sha256:str; supersedes:str |
| `ORDEM_013_RINGDOWN/C5_BIAS_ABLATION.json` | status:str; results:lista(108); scope:str; original_C6_unchanged:bool; source_hashes:objeto(3) |
| `ORDEM_013_RINGDOWN/C5_OVERTONE_ABLATION.json` | status:str; results:lista(120); scope:str; shared_harmonic_rate:str; accessed_target_strain:bool; source_sha256:str |
| `ORDEM_013_RINGDOWN/C5_RECOLORED_NOISE.json` | status:str; scope:str; no_on_source_strain_access:bool; samples_per_detector:int; degree:int; stride:int; fs_original:int; low_frequency_exponent_primary:int; low_frequency_controls:lista(2); source_sha256:str; scenarios:lista(4) |
| `ORDEM_013_RINGDOWN/C5_FISHER_EMPIRICAL.json` | status:str; inputs_sha256:str; parameters:objeto(5); records:lista(192); same_source_R_B:lista(2); same_source_reference:str; PSD_scope:str; noise_artifact_sha256:str; mass_spin_free:objeto(5); not_in_this_local_fisher_approximation:lista(3); interpretation:str |
| `ORDEM_013_RINGDOWN/bis/F2_ALL_READING_TABLES_v2.json` | status:str; utc:str; opening_sha256:str; supersedes:str; supersedes_sha256:str; source_sha256:objeto(6); code_sha256:str; rows:lista(60); limitations:lista(5); positive_medians_31:int |
| `ORDEM_013_RINGDOWN/bis/C2_TRAJECTORY_expanded_1000.json` | status:str; created_utc:str; N_per_cell:int; seed:int; reference:objeto(3); sample_hz:int; sample_count:int; window_seconds:float; changed_from_v1:str; noise_scope:str; physical_scope:str; cauchy_scope:str; coherent_scope:str; estimator:str; whitening_residual:float; original_noise_windows:int |
| `ORDEM_013_RINGDOWN/bis/C5_WALL_COUNTS_013BIS.json` | status:str; created_utc:str; recolored_group_counts:objeto(2); opposite_family:objeto(3); closed_set_mixture_groups:objeto(3); empirical_initial_status_counts:objeto(2); empirical_start_control_status_counts:objeto(2); low_snr_occam:lista(8); nonlinear_RB_only:objeto(4); not_paid:lista(4); optional_additional_nonlinear_search:objeto(3); stop_rule:str; hashes:objeto(6) |
| `ORDEM_013_RINGDOWN/bis/F4_GW250114_WINDOW_POWER_NORM.json` | status:str; detectors:lista(2); excess_norm_squared:float; network_rho_estimate:float; approximate_standard_error_if_white_gaussian:float; assumptions:str; start_tM:int; nonblind:bool |
| `ORDEM_013_RINGDOWN/bis/F2_CONTROL_EXTRACTION.json` | status:str; utc:str; archives:lista(2) |
| `ORDEM_013_RINGDOWN/bis/F2_CONTROL_SCHEMAS.json` | lista(9); item: path, sha256, root_attributes, datasets |
| `ORDEM_013_RINGDOWN/bis/F2_RD_APPLICABILITY_REVIEW.json` | status:str; epistemic_status:str; scope:str; run_same_lnB_permitted:bool; lnB:NoneType; usable_free220_posteriors:lista(0); reason:str; F2_disposition:str; counts:objeto(15); archive:objeto(3); sources:lista(9); extracted_sources:lista(714); all_sources_match_receipt:bool; all_nc_read:bool; sidecar_and_embedded_models_equal_after_literal_normalization:bool; omitted_regular_members:lista(10) |
| `ORDEM_013_RINGDOWN/bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.json` | status:str; release_located:bool; correction:str; archive:objeto(5); run_same_lnB:bool; lnB:NoneType; joint_df_dtau_spin_per_event_verified:bool; binary_posterior_values_read:bool; pickles_deserialized:bool; archive_code_executed:bool; sources:lista(12); exact_external_route:objeto(7); distinctions:lista(4); no_claim:lista(3); written_files:lista(14) |
| `ORDEM_013_RINGDOWN/bis/f2_injection/DESCRIPTIVE_RESULT.json` | status:str; source:str; source_sha256:str; extraction_path_matches:lista(1); seed:int; weighting:str; runtime:objeto(5); groups:objeto(2); source_field_sha256:objeto(2); method:objeto(6); analytic_prior_dictionaries_identical:bool; differences_with_minus_without:objeto(8); source_unchanged_after:bool; elapsed_s:float; dependencies_sha256:objeto(8) |
| `ORDEM_013_RINGDOWN/bis/f2_injection/METADATA.json` | source:str; sha256:str; bytes:int; schema_receipt_sha256:str; groups:objeto(2) |
| `ORDEM_013_RINGDOWN/bis/f2_injection/PRIOR_CONTRACT.json` | status:str; lnB:NoneType; source_sha256:str; groups:objeto(2); known:lista(4); not_proved:lista(2); decision:str; why_sample_check_is_not_proof:str; necessary_identity:str; caution:str; not_applied:lista(10); code_sha256:str |
| `ORDEM_013_RINGDOWN/bis/f2_injection/RECEIPT.json` | status:str; utc:str; root_windows:str; inputs:lista(7); files_written:lista(8); receipt_self:str; online_primary:objeto(4); unchanged_source_sha256_after_reporting:str; lnB:NoneType; adversarial_approval:str |
| `ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json` | status:str; started_utc:str; hard_deadline_utc:str; authorized_wall_hours:int; accounting:str; initial_envelope_hours:objeto(5); allocation_scope:str; old_jobs_policy:str; blind_gate:str; ma_sha256:str; part_a_manifest_sha256:str; opening_sha256:str; code_sha256:str |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/samples_summary.json` | generated:str; thin_per_event:int; rows:lista(39) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/A_poder_eventos.json` | frente:str; beta_runtime:float; rb_formula_check:objeto(7); csv_vs_c4_max_abs_dev:float; sets:objeto(6); combined_sigma_std:objeto(6); combined_sigma_68:objeto(6); audit_comparison:objeto(5); scaling:objeto(4); lever:objeto(10); excess_variance_df:objeto(3); excess_variance_observed_sel31:objeto(6); c2_rb_fields_sd:lista(0); c2_rb_fields_mean:lista(5); sig_jit_used:float; pyring_GW250114:objeto(5) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/RENDIMENTO_E_5SIGMA.json` | beta_runtime:float; sources:objeto(4); sigma_vs_snr_fit_31:objeto(5); rendimento:objeto(6); N_5sigma:objeto(4); premissas:lista(4) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/N5SIGMA_FROM_CATALOG.json` | source:str; sha16:str; beta_runtime:float; N_rows:int; per_event:lista(33); readings:objeto(4); sigma_dtau_stats_31:objeto(5); scalings_note:str; readings_O5_snr_gain_1.56:objeto(4); readings_O5_snr_gain_1.79:objeto(4) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr_table2_3_parsed.json` | lista(77); item: event, snr, ifos, Mdet, chieff, Mf_det, chif, table, nflags, RT, POL, TIGER, FTI, RD, pSEOBNR, QNMRF |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/FONTES.json` | web:lista(28); falhas_de_acesso:lista(5); locais_lidos:lista(14) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/C_piso_sistematico/C_piso_medicoes.json` | beta_runtime:float; sources_sha16:objeto(12); efeito_delta_tau_hat_GW250114_mediana_posterior:objeto(4); GW250114_posterior_dtau220_q05_50_95:lista(3); GW250114_sigma_dtau220_gauss_equiv:float; C5_IMR_cells_identifiable:lista(288); B_familia_resumo:objeto(4); B_familia_direcao_RB_noiseless_a_hat:objeto(2); C_modelo_QNM_220_440_vs_FULL_IMR_por_t0_RB:lista(9); C_overtones_FULL_IMR:objeto(5); C_overtones_custo_z_SNR40_media_por_fit:objeto(5); C_overtones_a_hat_10M_FULL_IMR:objeto(5); D_t0_LVK_release_Kerr_M_chi_por_t0_e_equivalente_df_dtau_vs_10M:lista(8); D_C6_lnB_por_t0_por_leitura_sd1e-20:objeto(5); D_C6_lnB_span_t0:objeto(5); E_C2_estimador_SNR20_sintetico:objeto(5) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/C_piso_sistematico/C_piso_sinais_catalogo.json` | a_sinais_familia_RB_noiseless:objeto(2); a_sinais_modelo_QNM_por_t0_RB:lista(6); a_sinais_overtones_10M_RB:objeto(5); b_F_catalogo_GWTC5_31:objeto(15); b_F_catalogo_GWTC5_33:objeto(15); b_F_catalogo_GWTC3_18:objeto(15); b_F_catalogo_GWTC3_10:objeto(15); c_N_5sigma_por_leitura:objeto(4); d_componentes_sistematicos_dtau_hat:objeto(17); d_tabela_condicao:objeto(4) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/D_realizacao_unica/d2_resultado.json` | threshold:objeto(3); sources_sha16:objeto(2); cases:lista(21); sigma_meas_reference:objeto(5); expected_z_with_current_31_sigmas:objeto(3); catalog_31_weight_in_GW250114_units:float; channel_comparison_GW250114:objeto(3) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/D_realizacao_unica/d3_resultado.json` | status:str; sources_sha16:objeto(4); analyses:lista(9); null_calibration_31:objeto(7) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/MEDICAO_E.json` | date_utc:str; beta_runtime:float; fontes:objeto(15); ps_snapshot:str; ps_groups:objeto(3); rss_total_GB:float; jobs:lista(4); C5_SEOB_REPEAT_AND_MIXTURE:objeto(3); resource_observation_bancada:objeto(5); continuous_registrations:lista(2); instrumento:objeto(12); reaproveitavel:lista(42); C3_BILBY_CONSUMER:objeto(6); C7_NATIVE_SEOB:objeto(2); C5_IMR_CONTROLS:objeto(5); armazenamento:objeto(14) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/gwosc_catalogs_raw.json` | GWTC-4.0:lista(129); GWTC-4.1:lista(140); GWTC-5.0:lista(161); O4_Discovery_Papers:lista(8) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/gwosc_strain_files_snr12.json` | lista(45); item: name, gps, snr, mf, chi, n_files, detectors, durations, rates |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/estatistica_poder/REFEITOS_REVISAO.json` | fontes_sha16:objeto(3); beta_runtime:float; N_rows_total:int; N_31:int; media_ponderada_31:objeto(3); catalogo31_gauss:objeto(4); N_5sigma_contra_RG_se_vies_persistir:float; fator_N90_N50_filtro_casado:float; z_090:float; GW250114:objeto(5); c_sigma_WLS_31:objeto(6); spearman_med_vs_sigma_31:lista(2); n_medianas_positivas_31:int; n_sigma_le:objeto(4); sigma_mediana_31:float; p_5sigma_unilateral:float |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/ceticos/cetico2_L149_refeito.json` | fit:objeto(3); sigma_fit:objeto(4); SNR_for_sigma:objeto(2); GW250114:objeto(4); P_sigma_le_0.06:objeto(4); P_sigma_le_0.10:objeto(3); counts_31:objeto(4); gwosc_gwtc5:objeto(3) |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/ceticos/cetico2_refeito_O5.json` | g:objeto(4); refeito:objeto(3); fonte:str |

### Imports declarados por AST — disponibilidade não testada

| Código relativo a R | Imports |
|---|---|
| `ORDEM_013_RINGDOWN/tgl_ringdown_prediction.py` | `math, numpy` |
| `ORDEM_013_RINGDOWN/catalog_220_readout.py` | `argparse, fetch_public, h5py, hashlib, json, math, numpy, os, pathlib, posterior_220_readout, scipy.interpolate, scipy.stats, tgl_ringdown_prediction` |
| `ORDEM_013_RINGDOWN/gwtc3_posterior_readout.py` | `catalog_220_readout, datetime, fetch_public, h5py, hashlib, json, lal, math, numpy, os, pathlib, posterior_220_readout, scipy.interpolate, scipy.stats, tgl_ringdown_prediction` |
| `ORDEM_013_RINGDOWN/trajectory_recovery.py` | `fetch_public, hashlib, json, math, numpy, os, pathlib, scipy.interpolate, scipy.linalg, scipy.optimize, scipy.stats, tgl_ringdown_prediction` |
| `ORDEM_013_RINGDOWN/refeito/measure_c2_013bis.py` | `argparse, datetime, hashlib, json, numpy, os, pathlib, prepare_empirical_noise, scipy.interpolate, sys, tgl_ringdown_prediction, tgl_ringdown_unravelings, time, trajectory_recovery` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/extract_samples_wsl.py` | `h5py, hashlib, json, numpy, os, sys, time` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/A_poder_eventos/poder_eventos.py` | `csv, hashlib, json, math, numpy, os, pathlib, sys` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/rendimento_e_5sigma.py` | `hashlib, json, math, numpy, re` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/n5sigma_from_catalog.py` | `hashlib, json, math, numpy` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/C_piso_sistematico/s02_measure.py` | `hashlib, json, math, numpy, os, scipy, scipy.special, sys` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/C_piso_sistematico/s03_sinais_e_catalogo.py` | `hashlib, json, math, numpy, os, scipy` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/D_realizacao_unica/d2_teste_populacional.py` | `hashlib, json, math, numpy, os, scipy.optimize, scipy.stats, sys` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/D_realizacao_unica/d3_catalogo_exploratorio.py` | `hashlib, json, math, numpy, os, scipy.optimize, scipy.stats, sys` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/medir_E.py` | `datetime, hashlib, json, math, os, re, subprocess, sys, time` |
| `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/estatistica_poder/refazer_estatistica.py` | `csv, hashlib, json, math, numpy, pathlib, scipy, sys` |

### HDF5 de calibração — hashes registrados, NÃO recalculados aqui

DECLARADO pelos esquemas hasheados acima. Só existência consultada; nenhum dataset aberto.

| Caminho absoluto | Dataset | Existe | SHA256 registrado |
|---|---|---|---|
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW150914_095045_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `ee037d6b7bf4b5844cc5085959ae9c85cf9009105ae741ba4ce15cc8421fa29d` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW170104_101158_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `7d7068231b54bfa294d62b960cb08d7888d59ddf63ca040282f734f9d286a7ca` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW190519_153544_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `7f81149dad489b3a5b2563ebbee87cea65a0777607d9716f868616eb5d85cba5` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW190521_074359_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `e78ae2678155ccb905a48b7a4c90866fb3c158c6592a3dfa618ed22e52da0362` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW190630_185205_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `b171f2bf2eeee33e1d93d8f6ba0cbb1efa0fe67ef616fb2949f0a710338fd2b3` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW190828_063405_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `e374f20deb3d21e98ee9b3dfab44f13480020cd9c1e4585d3a48ab19a5ff3e4c` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW190910_112807_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `20a5795c0d3d4bfb66ba681ee72eb5c0b0d8b6ecea12363139e7b0034cf6bcc8` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW191109_010717_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `382f355b9aa5d59d8551ef1f5945a2d2dc63c6d1991cb486bc7b3129fd7f6173` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW200129_065458_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `9ab35b32fb46d41e8901b52d721fdaf65a9a58e0acbac6cdb6e905d7dd44065e` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW200208_130117_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `707816640ff804954f94dd9585f08ab208b7b040be039d70b27113d6258ec7b7` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW200224_222234_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `2f305645afa8bb03eda8bfb86832fac4ebd0c6f584187a5a1c06a565588adb1c` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW200311_115853_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `655699ef55e69772e52be76270c443f96d28ce994e0805ff758ad83f7de27103` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW230628_231200_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `80b61edea729c50cb623c867bc172487699c0dba475941d3e141da07f07d5aaa` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW230914_111401_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `6b8770361be4817dc6c64701eadc239541418f8c16c515407dda12c8fe342fc1` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW230927_153832_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `57d55c936ae03885e222026ed8abab843cce68fd3b045a43be3fbc1016d01d68` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW231028_153006_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `6cfd5e9c7af014d17d74b726844170b2e109899621dc5d860546ffa202ab7c1b` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW231102_071736_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `6f64ce47488762bd7d0f4dc0bd00540af801b277218725318d7692420e3cdab6` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW231206_233901_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `2814f4c058a59bdf31903daf667389b50583aad1783055bcf1448b82e83576d7` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW231226_101520_Prod0.h5` | `pSEOBNRv5PHM-reweighted/posterior_samples` | True | `70f619507e656e702e5c2b9fa849701bfb9033ca56b5de858e4c03ba0d6b649f` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW240511_031507_Prod0.h5` | `pseob-rd/posterior_samples` | True | `a112cb0e3040e37bf8dbdd0295e15a145cbd160be16bc33207ceccb49b837cda` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW240514_121713_Prod0.h5` | `pseob-rd/posterior_samples` | True | `4f4776119f820529305ed2ea6d1eb0c076809359c18b3971b80a91e8cd27b87b` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW240615_113620_Prod0.h5` | `pseob-rd/posterior_samples` | True | `019f3078cd1fbbf9fc84766a12d044023bc918f145b1acc0bb4f60028156d29c` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW240621_195059_Prod0.h5` | `pseob-rd/posterior_samples` | True | `1691b7ce0a01bd2e7341abc9bf27c017f6d1726d2088c1fcc41b86f669ce128c` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW240705_053215_Prod0.h5` | `pseob-rd/posterior_samples` | True | `021567cb315415333219c58d6c01ae9b4f14a1497ea3dbe47dca22bb53e2eb0b` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW240716_034900_Prod0.h5` | `pseob-rd/posterior_samples` | True | `7d57ecc2d6ab79f54aeef0fa5cd61bc6675a49a16325a6522e40f98d1f1fc52a` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW240919_061559_Prod0.h5` | `pseob-rd/posterior_samples` | True | `2ddb5612cd6de8b3d3fe06fa4e489962113abe04a1bd3c86aceda13605c2bc92` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW240920_124024_Prod0.h5` | `pseob-rd/posterior_samples` | True | `55ee5818d0a7c8b9e487ac418ea19c2be757957c8695222ad62d845ee352510f` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW241006_015333_Prod0.h5` | `pseob-rd/posterior_samples` | True | `5279a6d5d809125407103ed6154a27c7b29d6a4ddf106002f98156c5021739db` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW241127_061008_Prod0.h5` | `pseob-rd/posterior_samples` | True | `1424476790528dfa0ecf955a3f0658f7eeb2d3c8af3737572cf7ca5b4ffb3d30` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW241129_021832_Prod0.h5` | `pseob-rd/posterior_samples` | True | `95f48d16bda84ba3111489c5882b3b396eb0fa89983333466667fa94bf94b351` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW241225_082815_Prod0.h5` | `pseob-rd/posterior_samples` | True | `1d2dd90ed2b72b5550db7de499e38f88900938648f1a023c9fc8e8c468a1143e` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW250114_082203_Prod0.h5` | `pSEOBNRv5PHM/posterior_samples` | True | `b9971bcd7d72fdd4a176483990854ae917992ad15cd793d15840dc2fe824a627` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/21454847/extracted/pSEOB/metafiles/pSEOB_GW250119_025138_Prod0.h5` | `pseob-rd/posterior_samples` | True | `ad6bcf11dee76e7dedc383206cac22172668c2de6f581b9069527c652644ee0c` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S200129m_pseobnrv4hm.h5` | `S200129m/posterior_samples` | True | `80ce31154eb8e89f9cad6400d3949f7844bc980de5785ef39b6e89835b1551a8` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190602aq_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `adb653d06a3148ca13f894639e9b374cb3aabbc9bdb36e3ed267f80810a9d03f` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190521g_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `8cdf11289ad57e5da1382817d63d7c7ba43c0af75c6ee4437abcd8992f1ba957` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190630ag_pseobnrv4hm.h5` | `S190630ag/posterior_samples` | True | `e9487b174590e02f060fc55085534333356e3fbdb7f33ec8bc13c8c6a33d4842` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S191109d_pseobnrv4hm.h5` | `S191109d/posterior_samples` | True | `0c174f5f0495d87f2bea9df7651004934127485a0284e132a662bc80afa8886b` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190519bj_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `025022285b7ee1911d10c33b05d30e4e54b26391da9184027cde39b85304ae93` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S200224ca_pseobnrv4hm.h5` | `S200224ca/posterior_samples` | True | `9546b64f02dce9783afcae759ffa28ffa4e6aaa86ed56567353cb3fd61fca049` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190706ai_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `2df08630a417f62346359ce365188dad65892c130853d1b89323806f98a2aab1` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190421ar_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `2fdf61d652699c64b6973dff17dad3bcda87145ae0646f336da3a96026e23be1` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190828j_pseobnrv4hm.h5` | `S190828j/posterior_samples` | True | `b78330c37314f01bf036e4d83f74ca04585fb2421a11d5b2c5630698a0fb63a2` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S170104_pseobnrv4hm.h5` | `GW170104/posterior_samples` | True | `666b5d1faee87738b766f59e929d5bc9de2bbe90443434cbb46b3334e504354c` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190521r_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `86e20cbb22af8d4a045d490487f9c44e13ae1394ccbfdf1da51ef9693370f235` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S200208q_pseobnrv4hm.h5` | `S200208q/posterior_samples` | True | `e8781e8edb972f1e77b3cdaaa85651cab1f314eaf2f797aae6f102f5f72c4129` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190727h_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `dce2fb77711f176eb046632cca4189feede1ee1c9baff13fc84539f405962191` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S150914_pseobnrv4hm.h5` | `GW150914/posterior_samples` | True | `8c8ae978d1c8b818828219f6fbcfdc9842521994d5c21d95f875fc36ef0b15d1` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S200311bg_pseobnrv4hm.h5` | `S200311bg/posterior_samples` | True | `d1f47065b64bb9c993850f899d921727ae67aabb61028aee307b9e19ab8eaa82` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190910s_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `d0fc0db67444b28b6b720f6bb655d777d85f206a14f73001965c63afa4976ed0` |
| `C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/public/17461225/extracted/rin/rin_S190503bf_pseobnrv4hm.h5` | `pSEOBNRv4HM/posterior_samples` | True | `d9f0675894f3bd29f838a945fe07cfbe5ee9ffcedaaa001d3e0edebb66267c71` |

### Método de conferência read-only

Ler esta tabela por regex `^\| ` seguido de caminho absoluto, bytes inteiros e hash de 64 hex; para cada linha, `data=Path(path).read_bytes()`, exigir `len(data)==bytes` e `hashlib.sha256(data).hexdigest()==sha256`, senão lançar RuntimeError. A tabela HDF5 declarativa não casa o campo bytes e fica excluída. Nenhum import de produtor ou escrita é necessário. O próprio gerador rehash todos os arquivos antes de publicar o apêndice.

Falha adicional preservada no histórico da sessão: uma tentativa de compor este apêndice foi recusada pelo parser PowerShell (here-string aninhada), antes de executar Python ou escrever arquivos; repetida com comando sem here-string interna.

