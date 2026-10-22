# D — semântica documental dos indicadores e da calibração

Pedido `c1fe821a-9c84-4659-8778-382645875498` — 06/10/2026. Entrega documental para revisão da coordenação ROOT.

**Resultado:** o dicionário O4, os canais de origem e as convenções públicas da calibração foram identificados. Os caminhos internos dos envelopes nos PEDataRelease e sua presença/cobertura efetiva por detector continuam **[OPEN]**. Nenhuma janela está liberada por este relatório.

## 1. O que foi qualificado

**[KNOWN — documentação oficial consultada]** O4a e O4b usam nove bits DQ e cinco bits de ausência de injeção. O esquema de 16 kHz foi lido; o documento técnico afirma expressamente a equivalência de indicadores com 4 kHz. A presença dessas estruturas nos arquivos locais não foi examinada.

| Bit | DQ | Bit | Ausência de injeção |
|---:|---|---:|---|
| 0 | DATA | 0 | NO_CBC_HW_INJ |
| 1 | CBC_CAT1 | 1 | NO_BURST_HW_INJ |
| 2 | CBC_CAT2 | 2 | NO_DETCHAR_HW_INJ |
| 3 | CBC_CAT3 | 3 | NO_CW_HW_INJ |
| 4 | BURST_CAT1 | 4 | NO_STOCH_HW_INJ |
| 5 | BURST_CAT2 | | |
| 6 | BURST_CAT3 | | |
| 7 | STOCH_CAT1 | | |
| 8 | CW_CAT1 | | |

Bit ligado significa passar a categoria, ou ausência da injeção indicada. No JSON do esquema, `mask=0/1` distingue DQ/INJ; o valor numérico de cada bit é `1 << bit`. Não tratar o campo `mask` como essa potência. O guia genérico histórico com sete bits não é o dicionário O4 completo. Fontes: [O4a](https://gwosc.org/archive/dataset/O4a_16KHZ_R1/), [O4b](https://gwosc.org/archive/dataset/O4b_16KHZ_R1/) e [JSON O4a](https://gwosc.org/archive/dataset/O4a_16KHZ_R1/json/).

DATA agrega ANALYSIS_READY, CBC_CAT1 e BURST_CAT1 no O4. Não implica ausência de injeções, estacionariedade ou adequação científica ao ringdown. [Definição oficial](https://gwosc.org/datadef/).

**[KNOWN]** As máscaras têm 1 Hz. Os arquivos bulk têm 4096 s; as categorias são cumulativas dentro do grupo de análise, sem equivalência entre grupos. GWF usa `{ifo}:GWOSC-4KHZ_R1_STRAIN`, `...DQMASK` e `...INJMASK`; esses nomes não são caminhos HDF5. R1 é revisão de canal, não a calibração C01. O documento também distingue a faixa de calibração da banda segura após redução de amostragem: recomenda 16 kHz para estudos por volta de 1700 Hz ou acima. [Detalhes O4](https://gwosc.org/O4/o4_details/).

## 2. Relógio, dicionário e leitor existente

**[REAL — inspeção estática de fonte, sem execução]** `sources_local/strain_io.py` seleciona os bits pela posição de cada nome em DQShortnames/InjShortnames. Exige vetores inteiros, nomes requeridos e formas iguais. Confere o comprimento contra a duração do strain, mas presume o início das máscaras em `meta/GPSstart` e a cadência de 1 Hz. Não lê separadamente atributos temporais dessas máscaras nem confronta o dicionário completo com as posições publicadas.

**[DERIVED — contrato proposto]** Antes de utilizar esse leitor numa rodada autorizada: conferir origem, cadência, cobertura, nomes únicos e posições. Para a convenção de intervalos semiabertos, o índice seria `floor((t-t_DQ0)/Delta_DQ)`; todos os segundos que intersectam cada janela onsource/offsource devem satisfazer os bits exigidos. A convenção de borda é proposta explícita de implementação; não foi medida nos arquivos. Comprimento igual não prova origem temporal igual. Não se deve interpolar máscaras ou preencher lacunas.

O mapeamento guarda como **esperados pelo código**, e não observados, `quality/simple/DQmask`, `quality/simple/DQShortnames`, `quality/injections/Injmask`, `quality/injections/InjShortnames`, `strain/Strain` e `meta/GPSstart`. Não foi executado o leitor nem o hash de qualquer container científico.

## 3. Release de strain e calibração

**[REAL — manifesto textual reaproveitado]** Os 14 eventos preservados têm dois descritores, H1 e L1. O primeiro aponta para O4a_4KHZ_R1; os outros para O4b_4KHZ_R1. Não repetimos a reconciliação GPS dos eventos. O inventário completo está em `DESCRITORES_EXTERNOS_D.json`.

| Release no manifesto | Canal de origem documentado | Escopo |
|---|---|---|
| O4a_4KHZ_R1 | `{ifo}:GDS-CALIB_STRAIN_CLEAN_AR` | Identidade pública do produto bulk |
| O4b_4KHZ_R1 | `{ifo}:DCS-CALIB_STRAIN_CLEAN_AR01` | Identidade pública do produto bulk |

Fontes: [O4a](https://gwosc.org/O4/O4a/), [O4b](https://gwosc.org/O4/O4b/). Os atributos dos arquivos locais continuam não verificados.

**[KNOWN]** AR01 reúne C01 onde disponível e C00 no restante. O período C01 documentado vai de GPS 1409425408 a 1415647232. CLEAN inclui subtração de ruído; isso não autoriza um procedimento novo de remoção de glitches. Não existe o correspondente canal GATED em AR01. Não se pode selecionar um envelope apenas porque ele é rotulado O4b. [Release alternativo O4b](https://gwosc.org/O4/o4b_alternate/).

## 4. Envelopes: o que é exato e o que ainda falta

**[DECLARADO na origem, conferido no JSON textual]** Os três registros Zenodo fixados declaram envelopes entre seus produtos: [17602505](https://zenodo.org/records/17602505), [20348005](https://zenodo.org/records/20348005), [20348006](https://zenodo.org/records/20348006). Os 14 nomes externos, tamanhos, MD5 declarados e URLs de conteúdo foram confrontados com esses JSON. Nenhuma URL de conteúdo foi acessada. MD5 declarado pelo fornecedor não é uma verificação nossa do payload.

**[OPEN]** A descrição geral não fornece o caminho interno exato, o label de análise, a cobertura H1/L1, a época, a grade ou o hash do envelope de cada evento. Todos esses campos permanecem nulos no inventário. Não inventamos um caminho PESummary convencional. Também não abrimos o notebook de exemplo, que pode conter saídas científicas além de instruções de leitura.

**[KNOWN — produto independente]** O [DCC T2500288-v5](https://dcc.ligo-wa.caltech.edu/LIGO-T2500288/public) lista `LIGO_O4a_cal_uncertainty.tgz` e `LIGO_O4b_cal_uncertainty.tgz`. Não foram baixados. Seu [README versionado](https://dcc.ligo-wa.caltech.edu/public/0202/T2500288/005/README.txt) documenta arquivos `calibration_uncertainty_[IFO]_[GPS].txt`, horários, escolhidos pelo GPS mais próximo. As sete colunas são frequência, medianas de magnitude/fase e limites inferiores/superiores de uma sigma; fase em radianos. A magnitude representa `R_true/R_model`, centrada aproximadamente em 1, e não erro fracionário centrado em zero. A faixa declarada é 10–5000 Hz; os erros sistemáticos estimados permanecem sem correção no strain. Isso não especifica covariância completa ou independência gaussiana. Os envelopes preliminares de baixa latência são distintos. O exemplo de link ao registro 16053484 não substitui o 17602505 fixado. Há um erro cronológico na data final escrita em prosa para O4b no README; a unidade não tentou corrigir GPS por essa frase. O padrão de nome não determina sozinho o membro exato de cada evento.

## 5. Duas rotas úteis para a lacuna de calibração

**CAL_A — inventário segregado de cabeçalhos PE.** Numa etapa explicitamente autorizada, obter somente schema/metadados de calibração, vinculados ao label e detector, sem ler posteriors. Vantagem: conserva a proveniência exata do PE fixado. Risco: um leitor genérico PESummary pode carregar arrays científicos; caminhos de grupo não podem ser presumidos. Nesta unidade, até a abertura de cabeçalhos HDF5 está fora do escopo.

**CAL_B — produto horário independente do DCC.** Numa etapa própria, inventariar os arquivos de calibração, comprovar release/hash, detector, época e grade; só depois definir o tratamento dos parâmetros de calibração. Vantagem: separação clara dos posteriors. Limite: ainda exige verificar membros reais e compatibilidade C00/C01. É a rota documentalmente mais simples para isolar o PE, sem garantir que o produto seja idêntico ao usado em cada label publicado. Nenhuma das rotas foi executada ou ratificada aqui.

## 6. A escolha de injeções tem efeito científico

**[KNOWN]** A documentação do O4 informa ausência de injeções CBC/BURST/STOCH/DETCHAR durante os períodos observacionais publicados, mas injeções CW em LIGO durante o run, com intervalos de inatividade. Isso não substitui a conferência dos bits locais. Os nomes de listas Timeline, como NO_CBC_HW, também não devem ser confundidos com o nome de bit NO_CBC_HW_INJ. [Injeções O4](https://gwosc.org/O4/o4_inj/).

**INJ_A, proposta:** exigir os quatro tipos exceto CW; tratar CW explicitamente por política previamente registrada para linhas/contaminação. Não chamar isso ausência de toda injeção e não presumir efeito desprezível.

**INJ_B, proposta:** exigir todos os cinco, incluindo NO_CW_HW_INJ. Pode excluir tempo relevante; não calculamos a fração sobrevivente. A escolha depende da pergunta científica e deve anteceder a inspeção dos resultados.

Nove bits disponíveis não significa exigir todos: a categoria CBC/ringdown e eventual requisito BURST permanecem escolhas do contrato. Não alteramos `required_quality_flags=null`, `required_no_injection_flags=null`, a seleção PSD A/B nem os quatro holds. Os dez eventos sem hold anterior também não se tornam prontos por isso.

## 7. Custódia, alcance e próximo passo

`SOURCE_CAPTURE.json` registra cópias byte a byte de nove fontes textuais e verifica os pins recebidos. A tentativa de capturar corpos HTTP por Python foi recusada pelo ambiente com WinError10013; esse erro ficou registrado. A ferramenta web permitiu a consulta documental. `PUBLIC_DOCUMENTARY_EXCERPTS.json` e `FONTES_QUALIFICADAS.json` preservam URLs, localizadores, trechos curtos e campos factuais. Seus hashes são dos excertos/representações locais — **não dos corpos HTTP originais**. O checksum do servidor permanece desconhecido. A validação offline cruza os descritores e deixa os campos não observados nulos.

**Entregar à ROOT:** revisar o dicionário e a política de injeções; escolher a rota de qualificação dos envelopes; integrar esses recibos ao contrato existente. Não criar uma segunda seleção ou um segundo pipeline. A semântica documentada está resolvida; presença local, alinhamento e cobertura efetiva serão comprovados na etapa autorizada correspondente. Nenhum PSD, strain, NPZ, container PE, posterior ou centro foi lido; não houve fit, abertura de D, alteração de V1, nova chamada a modelos, repetição INIT003 ou liberação de hold.
