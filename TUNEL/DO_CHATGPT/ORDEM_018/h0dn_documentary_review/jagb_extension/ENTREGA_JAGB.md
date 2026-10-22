# ORDEM018 — inclusão de JAGB e resposta diferencial das Cefeidas

05/10/2026. [REAL documental + DERIVED condicional]. Unidade independente solicitada pela coordenação, sem chamadas remotas, ajuste, leitura numérica de centros para inferência ou execução de código upstream.

## Peça encontrada

**JAGB já está implementado na variante pública V01 do H0DN.** Ela acrescenta 12 registros de distância em 11 hospedeiras que também têm Cefeidas e TRGB. Não acrescenta uma nova amostra SN independente. V01 é o nome da variante do H0DN; não confundir com V1, o pré-registro do nosso teste ainda em preparação.

O commit é o mesmo da revisão anterior, conferido nos manifestos locais. Sete arquivos públicos adicionais foram baixados e verificados por blob Git; 31 fontes locais foram conferidas no total. Os arquivos originais não foram editados. `map_jagb_metadata.py` é uma implementação própria dos filtros e cruzamentos de **identificadores**, não executa funções do H0DN e não converte módulos/magnitudes observados em números.

## Arquivos e entrada pelas equações

| Referente no repositório | Papel confirmado |
|---|---|
| `h0_constrainer/configs/variants.ini:6` | V01 substitui `host_exclude_list` por `*mira*, SMC, b25`, retirando apenas a exclusão JAGB. |
| `h0_constrainer/configs/base_variants_config.ini:6` | Herda `host_data.dat`, SNe calibradoras/fluxo, covariância SN, SBF, grupos e megamasers. |
| `h0_constrainer/configs/config.ini:198` | Exemplo equivalente de inclusão JAGB. |
| `idlcode/vars.pro:68` | Variante V01 também explícita no código IDL; usa as mesmas fontes baseline e exclusões. |
| `data/host_data.dat:315` | Referência `jagb_jwst,N4258,CCHP` e sete hospedeiras nas linhas 316–322. |
| `data/host_data.dat:327` | Referência `jagb_jwst,N4258,SH0ES` e cinco hospedeiras nas linhas 328–332. |
| `data/host_data_nomet.dat` | Contém as mesmas chaves de identidade JAGB; é alternativa de tabela, não evidência adicional. Não foi avaliada igualdade dos valores. |
| `data/sn1a_calib.dat` | Liga as hospedeiras às magnitudes SN. Uma mesma linha SN não se duplica por existir mais de um indicador estelar. |
| `data/sn1a_hf_pp.dat` e `data/sn1a_covar_pp.dat` | Fluxo SN comum e sua covariância, usados pelo intercepto comum. |
| `data/anchors.dat`, `groups.dat`, `sbf_calib.dat`, `sbf_hf.dat`, `megamaser.dat` | Âncoras e demais ligações da seleção herdada; preservadas na comparação V00/V01. |

JAGB entra pela equação genérica `mu_host = valor publicado` em `equations.py:334`, não por uma nova equação H0 privativa. O mesmo `mu_host` entra em `M_B + mu_host = magnitude_SN` (`:399`). O intercepto comum conecta `log10(H0) - 0.2 M_B` ao fluxo (`:519`). Filtros e cruzamentos estão em `main.py:348`, `data_loader.py:713`, `:768` e `:825`; referências MAS são separadas em `data_loader.py:328`.

[KNOWN — proveniência publicada] O artigo distingue JAGB/SH0ES (JWST GO-1685 e GO-2785) e JAGB/CCHP (GO-1995), com procedimentos estatísticos diferentes. Ambos se ancoram em NGC 4258. A variante V01 inclui JAGB fora do baseline. Fonte: [H0DN, seções V e A.2.4](https://arxiv.org/html/2510.23823v1). Os rótulos/linhas do arquivo foram conferidos; não se atestou nesta unidade que todos os valores correspondem a eventuais versões posteriores dos artigos de origem.

## Seleção ampliada reconstruída por nomes

Os filtros configurados, a seleção de grupos e o casamento host/calibrador foram reimplementados somente com nomes. A comparação abaixo não é uma execução do solver.

| Elemento | V00 | V01 com JAGB |
|---|---:|---:|
| Linhas de distância das hospedeiras | 166 | 178 |
| Linhas de referência estelar para MAS | 12 | 14 |
| Hospedeiras distintas nessas linhas | 53 | 53 |
| Linhas de SNe calibradoras | 55 | 55 |
| Linhas de calibradores SBF | 14 | 14 |
| Ligações de grupo | 13 | 13 |

As 55 linhas SN, 14 SBF e 13 de grupos são exatamente as mesmas seleções de identificadores nas duas variantes. As 12 linhas JAGB se dividem em sete CCHP e cinco SH0ES; N5643 aparece nas duas fontes. Todas as 11 hospedeiras abaixo têm medidas Cefeida e TRGB admitidas no mesmo cruzamento.

| Hospedeira | JAGB | SNe compartilhadas no arquivo de calibradores |
|---|---|---|
| M101 | CCHP | 2011fe |
| N1365 | CCHP | 2012fr |
| N1448 | SH0ES | 2001el; 2021pit |
| N1559 | SH0ES | 2005df |
| N2442 | CCHP | 2015F |
| N3447 | SH0ES | 2012ht |
| N4536 | CCHP | 1981B |
| N4639 | CCHP | 1990N |
| N5584 | SH0ES | 2007af |
| N5643 | CCHP e SH0ES | 2013aa; 2017cbv |
| N7250 | CCHP | 2013dy |

São **13 identificadores SN compartilhados**, não 13 SNe novas. `SELECTION_V01_IDENTIFIERS.json` conserva, para cada host, todas as linhas Cefeida/TRGB/JAGB, instrumento, fonte, âncora, SN e linha do arquivo. A nomenclatura original foi preservada; não houve união aproximada de nomes.

Todas as linhas JAGB usam N4258. Os ramos Cefeida presentes incluem também LMC/MW; isso não torna as estimativas finais independentes, pois compartilham hospedeiras, SNe e o parâmetro comum. O fluxo SN tem 277 linhas e 238 nomes distintos. Nenhum desses nomes coincide com os calibradores nesta comparação literal, mas esse teste de nomes não elimina sistemáticas compartilhadas ou a necessidade da matriz fornecida. Linhas repetidas do fluxo não foram deduplicadas.

## Mapa de covariância: o que existe e o que não está quantificado

Para o bloco de hosts, a leitura de `equations.py:334–376` dá a estrutura abaixo, com os rótulos preservados:

\[
C_{ij}=\delta_{ij}s_i^2
 +[a_i=a_j]\,s_{a_i}^2
 +[MAS_i=MAS_j]\,s_{MAS_i}^2
 +(1-\delta_{ij})[HMS_i=HMS_j]\,s_{HMS_i}^2.
\]

MAS=(método,âncora,fonte); HMS=(hospedeira,método,fonte). A expressão descreve os termos implementados nesse bloco, não uma afirmação de completude de todas as sistemáticas físicas. O ramo HMS usa a regra de `data_loader.py:493`, inclusive o aviso quando erros da mesma chave diferem.

| Relação | Tratamento no código | Implicação para JAGB |
|---|---|---|
| Âncora N4258 comum | Termo comum entre todas as linhas da mesma âncora | Cruza JAGB, TRGB e Cefeidas, inclusive fontes diferentes. Não adicionar novamente a mesma incerteza como prior e covariância. |
| Mesmo MAS | Termo comum dentro de método–âncora–fonte | CCHP/JAGB e SH0ES/JAGB têm referências próprias; não são o mesmo MAS. |
| Mesmo HMS | Termos fora da diagonal para medidas com a mesma chave | Mudança de método ou fonte muda HMS; esse mecanismo não quantifica sozinho a covariância residual entre métodos/fontes. |
| Mesma hospedeira | Mesmo parâmetro de distância | Correlação pela inferência conjunta; não é autorização para acrescentar uma covariância arbitrária. |
| Mesma SN e mesmo fluxo | Mesma linha de calibrador e mesmo intercepto | Fan-out da informação para vários métodos, sem replicação da likelihood SN. |
| Residual entre métodos/fontes além desses termos | Nenhuma matriz específica identificada nos arquivos/trechos inspecionados | **Não quantificado; não comprovadamente zero.** |

A distância geométrica de N4258 entra uma vez como âncora compartilhada. Ela não é uma medida adicional de H0: a linha de NGC_4258 no arquivo de megamasers do fluxo está comentada. Não somar âncora, resultado da rede e resultados de seus ramos como três evidências independentes.

**Pendência para nosso teste:** explicitar a covariância residual relevante à comparação Cefeida–TRGB–JAGB. Recuperar os termos das fontes ou pré-especificar uma família semidefinida de sensibilidade às correlações não quantificadas. Usar zero apenas por ausência de arquivo não é uma solução. Também não se exige demonstrar independência de toda sistemática imaginável: o mapa identifica as dependências concretas e o alcance do modelo publicado.

## Propagação do viés Cefeida no modelo comum

[DERIVED, C fixa e parâmetros identificáveis no suporte] Defina o rival diferencial por

\[
y=A x+c_C\delta_C+\epsilon,
\qquad \operatorname{Cov}(\epsilon)=C.
\]

δ_C positivo significa módulo Cefeida publicado alto. A coluna c_C vale 1 nas linhas de hosts Cefeida e 0 nas outras linhas; não muda diretamente JAGB, TRGB, âncoras geométricas, SN ou fluxo. Esta definição é um viés **diferencial nas distâncias inferidas**, não um deslocamento fotométrico idêntico de âncoras e hospedeiras, que pode cancelar.

`CEPHEID_RESPONSE_CANDIDATE.json` fornece essa coluna candidata por `row_id`: 119 entradas 1 entre as 178 linhas de host e zeros nas restantes. Todas as equações não-host recebem zero antes da propagação. Não usar a posição da linha sem confirmar o manifesto de seleção.

Com W=C⁺, S=AᵀWA e g=AᵀWc_C:

\[
\hat x(\delta_C)=S^{-1}A^TW(y-c_C\delta_C),
\qquad
\frac{\partial\hat x}{\partial\delta_C}=-S^{-1}g.
\]

Logo, para h=log10(H0),

\[
\Delta h=-e_h^TS^{-1}g\,\delta_C,
\qquad
\frac{H_0(\delta_C)}{H_0(0)}=10^{\Delta h}.
\]

A influência chega ao H0 por todos os parâmetros comuns e pesos correlacionados. Não se aplica um deslocamento uniforme ao H0DN final como se fosse o rival Cefeida. Neste recorte, calcular a resposta matricial não requer observar y; porém **não calculamos S, g ou esse coeficiente nesta unidade**, porque a C conjunta ainda deve ser qualificada.

Se δ_C for estimado conjuntamente, a informação perfilada é

\[
I_C=c_C^TWc_C-g^TS^{-1}g.
\]

I_C>0 é a condição local de identificabilidade sob essas hipóteses. C singular exige ainda consistência do suporte: Nᵀ(y−Ax−c_Cδ_C)=0. Não basta a pseudoinversa. Em vez de inventar resposta nas equações redundantes, derivá-la das medidas elementares e de sua transformação para a rede. Incerteza gaussiana marginalizada em δ_C e prior explícito da mesma incerteza são alternativas de representação, não termos a adicionar duas vezes.

O deslocamento universal permanece outra hipótese: se H0 é livre, ele pode absorver uma mudança comum de escala. Para testar `H_local=K H_background`, ligar a rede à referência de fundo autorizada, com dependências explícitas. JAGB ajuda a contrastar métodos; não resolve essa degenerescência global apenas pelo nome do indicador.

## Entrega para a coordenação

Seleção ampliada preparada como **candidata documental V01**, não como ratificação do pré-registro V1. Entregues nomes/linhas, âncora, fontes, SNe compartilhadas, mapa dos termos de covariância implementados e coluna candidata de resposta. Chamadas remotas permanecem suspensas; nenhuma unidade pendente foi repetida.

Arquivos: `SOURCES.json`, `SELECTION_V01_IDENTIFIERS.json`, `CEPHEID_RESPONSE_CANDIDATE.json`, `map_jagb_metadata.py`, este relatório e `MANIFESTO_ENTREGA.json`. O teste ainda depende da qualificação do suporte/covariância, da correspondência física da previsão fixa e da ratificação do contrato existente. Nenhum ajuste, centro inferido, significância, evidência Bayesiana, veredito, gate ou original foi alterado.
