# ORDEM018 F1/F9 — projeto linear V01 e medida nuisance comum

Unidade **ec4872ec-82f0-4236-a76c-1e10f89aefe5**. Preparação documental independente solicitada pela coordenação. [REAL] identificadores, código pinado e aritmética exata de coeficientes; [DERIVED] provas condicionais de suporte/integração; [OPEN] contrato científico e abertura. Nenhum centro novo foi convertido, nem y/C observados montados, nem ajuste, S, g, H0, ln B, upstream, dados D ou modelo remoto executado.

**Resultado:** a montagem comum possui **267 equações, 63 nuisance η e h como 64º parâmetro**. A coluna a_h tem sete entradas unitárias; c_C tem 119. As duplicações por âncora impõem **72 vínculos determinísticos independentes**, explicitados por linha no JSON. X, a_h e c_C respeitam esses vínculos. A integral nuisance pode ser especificada exatamente; nenhuma dessas afirmações calcula a evidência ou a potência do teste.

## 1. Fonte e notação

Fontes congeladas: `../UPSTREAM_MANIFEST.json`, `../jagb_extension/SOURCES.json`, `../jagb_extension/MANIFESTO_ENTREGA.json` e `../jagb_extension/SELECTION_V01_IDENTIFIERS.json`. O código upstream não foi importado. O leitor independente em `derive_identifier_design.py` produz somente chaves e coeficientes racionais, nunca o vetor de medidas. A nova especificação está em `ESPECIFICACAO_LINEAR.json`; cada linha mantém o localizador original.

O upstream chama a matriz de coeficientes A e o vetor de parâmetros X. Para compatibilidade com a proposta F9 da coordenação, adotamos aqui:

**y = Xη + a_h h + c_C δ_C + ε,   A_up = [X | a_h].**

h = log10[H0/(km s⁻¹ Mpc⁻¹)]. δ_C tem unidade magnitude e sinal positivo quando a distância publicada por Cefeidas está enviesada para cima. A coluna diferencial é uma hipótese sobre a média, não um novo erro comum a adicionar automaticamente a C.

A forma de η é:

η = (μ_1,…,μ_59, μ_Fornax, μ_Virgo, M_B, M110_offset).

Há 53 hospedeiras com medições diretas, mas **59 parâmetros de hospedeira** na rede inteira. As seis adicionais entram pelos grupos/calibradores: IC2006, N1344, N1374, N1375, N4458 e N4489. Não confundir a contagem anterior de 53 hospedeiras medidas diretamente com o número de colunas do modelo.

Os parâmetros de geometria da âncora e de erros MAS/HMS já marginalizados em C não reaparecem como nuisance livres com o mesmo prior. M110_offset é o deslocamento SBF da definição upstream, não uma substituição silenciosa por uma magnitude absoluta com outra origem.

## 2. Receita exata das linhas

As colunas de hospedeiras seguem a ordenação lexical de `uniquify`; os grupos seguem sua primeira ocorrência (Fornax, Virgo); depois M_B, M110_offset, h. A ordenação upstream das linhas é a tabela abaixo. No intercâmbio, usar **chaves e row_id**, não confiar em índices memorizados.

| Família | Linhas | Xη | a_h | c_C | y, apenas definição simbólica |
|---|---:|---|---:|---:|---|
| Distâncias estelares | 178 | μ_host | 0 | 1 se método começa por ceph; 0 nos demais | distância publicada da respectiva linha |
| Relações de grupo | 13 | μ_host − μ_group | 0 | 0 | 0, com dispersão de grupo |
| Calibradores SN Ia | 55 | μ_host + M_B | 0 | 0 | magnitude SN padronizada |
| Calibradores SBF | 14 | μ_host + M110_offset | 0 | 0 | m110 − M110 da tabela |
| Intercepto SN no fluxo | 1 | −M_B/5 | 1 | 0 | α_SN + 5 |
| Intercepto SBF no fluxo | 1 | −M110_offset/5 | 1 | 0 | α_SBF + 5 |
| Megamasers do fluxo | 5 | 0 | 1 | 0 | logh_value transformado conforme upstream |

Fontes: `equations.py:148–296` (parâmetros), `334–344` (estelares), `380–413` (grupo/SN), `448–461` (SBF), `519–527` e `619–627` (interceptos), `630–643` (masers); arquivos em `../upstream/h0_constrainer/h0_constrainer/`. A referência exata dos trechos está pinada nos manifestos.

a_h tem entradas 1 somente nas duas linhas de intercepto e nas cinco de masers; todas as outras 260 entradas são zero. c_C tem 111 entradas Cefeida HST/R22 mais oito Cefeida JWST/SH0ES: **119**, coincidindo com o candidato anterior. As outras 148 linhas têm zero. Deslocar a coluna SN/SBF ou todas as distâncias porque Cefeidas calibram parte da rede seria duplicar o efeito: a ligação ocorre através dos mesmos μ_host e M_B no ajuste conjunto.

Masers admitidos: UGC_3789, NGC_6264, NGC_6323, NGC_5765b, CGCG_074-064. N4258 é âncora, não sexto maser de fluxo. V01 não inclui Coma/FP, EPM, SN II ou TF. Esses setores não ganham colunas por estarem disponíveis em outras variantes.

### Interceptos não são nuisance extras

α_SN e α_SBF são resumos dos respectivos dados de fluxo, com suas covariâncias; não são parâmetros adicionais de η nesta montagem. Não incluir simultaneamente a linha comprimida e todas as medidas que a produziram como evidências separadas. A constante residual da compressão pode cancelar numa razão apenas se independer de todos os parâmetros/modelos comparados; caso contrário precisa acompanhar a likelihood completa.

A configuração pinada fixa q0=−0,55 e j0=1, usados na redução SN/masers. A coordenação precisa manter essa transformação cinemática comum no recorte proposto, com seu alcance declarado, ou reconstruir a descrição não comprimida se permitir que a expansão altere esses termos. Não recalcular y de modo dependente de θ mantendo uma normalização antiga. Nenhum intercepto ou transformação de maser foi calculado aqui.

## 3. Vínculos determinísticos das cópias por âncora

Nas 178 linhas estelares há 104 chaves HMS e **11 MAS ativos**. Existem 14 linhas de referência na seleção, mas três não são utilizadas por qualquer equação estelar admitida: ceph_jwst/N4258/CCHP, trgb_hst/N4258/A21 e trgb_hst/N4258/A22. Uma referência disponível não cria um parâmetro ou um dado a mais. Essa distinção é especialmente útil ao materializar a família de covariâncias previamente proposta.

Cada linha é uma aresta entre um nó HMS e um nó MAS. Os componentes ativos são nove combinações método/fonte. O único componente com ciclos é Cefeida HST/R22: **37 hospedeiras × 3 âncoras = 111 arestas**. Sua matriz de incidência tem posto 37+3−1=39; dimensão de ciclos 111−39=72. Os outros 67 registros têm um MAS por componente e não acrescentam ciclos. Resultado combinado: posto de incidência estelar 106, nulidade à esquerda 72. Trata-se de contagem combinatória exata, não de SVD da covariância observada.

Fixe uma hospedeira H* e uma âncora A* no componente R22. Para cada uma das outras 36 hospedeiras H e cada uma das outras duas âncoras A:

**y_(H,A) − y_(H,A*) − y_(H*,A) + y_(H*,A*) = 0.**

Isto decorre de cada linha compartilhar o erro de hospedeira HMS e a referência MAS/âncora. Cada erro primitivo cancela nessa combinação. Há 36×2=72 equações independentes; a aresta (H,A) fora da árvore aparece com coeficiente 1 somente no seu ciclo fundamental.

Exemplo de row_ids, sem valores: `host_data.dat:L171 − L130 − L145 + L104 = 0`, no ciclo M1337/M101 e MW/LMC. Os 72 ciclos, seus sinais e identificadores estão em `ESPECIFICACAO_LINEAR.json:deterministic_cycles`.

**Duas cópias por âncora não são medidas idênticas.** y_(H,A)−y_(H,A*) pode ser não zero: é o contraste compartilhado entre calibrações. O que é determinístico é que o mesmo contraste vale para outra hospedeira sob a construção de erro. Não apagar todas as diferenças por âncora; não tratar as 111 linhas como 111 medidas independentes.

### O que foi e não foi verificado

O script verificou com inteiros/racionais que cada ciclo anula separadamente as incidências HMS, MAS e âncora, e também **LX=0, La_h=0, Lc_C=0**. L denota a matriz cujas linhas são os ciclos. Nenhum centro foi lido para verificar **Ly=0**. Essa será uma condição de compatibilidade dos dados quando houver abertura.

Com erros MAS/HMS positivos e o bloco estelar baseline, os ciclos caracterizam exatamente seu núcleo. Os erros ativos positivos e a igualdade dos erros dentro de cada HMS foram conferidos nos metadados da unidade anterior. A família PSD interior preserva esse núcleo quando seus fatores de correlação são definidos positivos. Isso não certifica o suporte dos demais blocos nem valida os dados reais.

Arredondamentos publicados ou outras transformações podem tornar Ly diferente de zero. A política de precisão deve ser congelada antes de observar o efeito: reconstrução de primitivas, erro de quantização justificado ou outra especificação explícita. Não apagar resíduos no núcleo pela pseudoinversa nem acrescentar jitter para fazer passar um resultado.

## 4. Posto das colunas e condição para a integral nuisance

X tem **posto de coluna 63**, demonstrável sem pesos nem centros. Se Xv=0, as linhas de hospedeiras medidas fixam v_μ=0. Cada grupo está ligado a uma dessas hospedeiras, portanto seus v_μgroup=0; os links fixam também as seis hospedeiras adicionais. As linhas de calibradores então dão v_MB=v_M110offset=0.

a_h não pertence ao espaço de colunas de X: nas cinco linhas de masers X=0 e a_h=1. Logo [X,a_h] tem posto 64.

c_C não pertence ao espaço de colunas de [X,a_h]: há duas linhas da mesma hospedeira, uma Cefeida e outra TRGB, com X idêntico e a_h=0, mas c_C=1 e 0. Testemunha em M101: `host_data.dat:L10` e `L247`. Logo o projeto aumentado tem posto 65. **Identificabilidade algébrica não é sensibilidade estatística ou evidência física.**

No bloco estelar, X e c_C pertencem à imagem da incidência HMS, pois seus valores dependem da hospedeira/método e não mudam nas cópias de âncora; a_h é zero. Portanto estão no suporte baseline estelar. Se os demais blocos forem não degenerados, as três colunas/matrizes estão no suporte completo. Caso contrário, aplicar o guard de suporte já existente a todos os blocos. Não foi criado outro guard nesta unidade.

Assim, o projeto conhecido não obriga a introduzir nuisance fora do suporte para resolver as duplicações estelares. O problema de NᵀX≠0 da nota geral não ocorre nesses 72 vínculos. Essa conclusão continua condicional ao tratamento dos outros blocos e à covariância efetivamente escolhida.

## 5. As mesmas colunas nas cinco hipóteses

Escreva ℐ(θ)=(2/3)ln E_LCDM(z*;θ) e h_bg=log10[H0_bg/(km s⁻¹ Mpc⁻¹)]. O valor beta_TGL é calculado como ALPHA_FINE_CODATA_2018×sqrt(e), nunca estimado pelas médias locais nesta hipótese.

| Modelo da proposta F9 | h inserido nas sete linhas a_h | δ_C inserido nas 119 linhas c_C |
|---|---|---|
| TGL fixa, mapa R-A | h_bg + ℐ beta_TGL/ln10 | 0 |
| LCDM referência | h_bg | 0 |
| Beta livre diagnóstico | h_bg + ℐ beta/ln10 | 0 |
| Viés diferencial Cefeida | h_bg | parâmetro próprio δ_C |
| H5 opção A, ainda condicional | h_bg | 0 |

H5 A muda a régua BAO r_drag no bloco de fundo; não altera X, a_h ou c_C da rede, nem é por isso um modelo EDE. Outras escolhas H5 exigem seu contrato específico. Todas as cinco conservam os mesmos 63 nuisance, dados, unidades e regra de medida. h não é integrado novamente como um parâmetro local livre independente de θ: isso cortaria a ligação ao fundo que a comparação quer testar. Pode ser representado por uma delta de Dirac em h−h_model(θ) com a medida dh apropriada.

O vínculo universal local R-A é uma hipótese de correspondência física, não um teorema produzido pela incidência. Beta livre, δ_C ou r_drag são parâmetros particulares de modelos, com priors próprios e normalizados; **não** pertencem ao fator plano comum dos 63 nuisance.

## 6. Duas medidas nuisance bem definidas

Seja r o posto de C efetiva, U uma base ortonormal de seu suporte e N de seu núcleo; estes objetos não foram calculados numericamente aqui. Fixe coordenadas de dados e unidades comuns, e escreva b=y−a_h h−c_C δ_C. A densidade gaussiana, sobre o suporte afim comum, é

L(b|η,C) = (2π)^(−r/2) pdet(C)^(−1/2) exp[−(b−Xη)ᵀ C⁺(b−Xη)/2],

com Nᵀ(b−Xη)=0. Uma base de ciclos L não é ortonormal e **não substitui** U ou o jacobiano da medida; ela fornece restrições exatas.

### A. Prior próprio comum — evidências normalizadas

Escolher uma densidade π_η(η), integral 1, mesma origem/unidades e mesmo significado físico nos cinco modelos. Não ajustar sua localização/largura com os mesmos centros locais antes da comparação.

Opção gaussiana: η~N(m_η,V_η), V_η definida positiva e independente do ruído. A integração dá exatamente

**y | h,δ_C ~ N(Xm_η+a_h h+c_C δ_C, C+XV_ηXᵀ).**

Manter a normalização, o posto e o suporte dessa convolução. No caso aqui qualificado em que X está no suporte de C, ela não expande esse suporte; na nota geral, se X estiver fora, pode expandi-lo. Esse é um prior de distâncias/magnitudes físicas, distinto dos erros de âncora/MAS/HMS já presentes em C.

Opção uniforme em uma caixa/ domínio finito Ω de volume VΩ: π_η=1Ω/VΩ. Supondo X no suporte, F=XᵀC⁺X invertível e compatibilidade do núcleo, seja η_hat=F⁻¹XᵀC⁺b. A integral equivale à expressão plana abaixo multiplicada por **Pr[N(η_hat,F⁻¹)∈Ω]/VΩ**. O volume comum pode cancelar na razão, mas a probabilidade de truncamento geralmente não. Limites e caudas são decisões do contrato, não inferíveis da matriz de desenho.

### B. Mesma medida plana — razão relativa, não evidência absoluta

Use dη nas mesmas 63 coordenadas em todos os modelos, ou κ dη com a mesma constante arbitrária κ. Requer domínio R^63, integral finita, posto completo de X no suporte, suporte de dados comum e transformações de coordenadas com seus jacobianos preservados.

Defina F=XᵀC⁺X e P=C⁺−C⁺XF⁻¹XᵀC⁺. Então

**L_plana(h,δ_C;C) = (2π)^(−(r−63)/2) [pdet(C) det(F)]^(−1/2) exp[−bᵀPb/2]**,

no suporte compatível. Esta identidade foi derivada completando o quadrado em η; não foi avaliada em dados. A integral com κ dη é κ L_plana. O mesmo κ cancela em Z_i/Z_j se as demais integrais com priors próprios forem finitas e não nulas. Z_i isolado continua dependente da constante arbitrária: não chamá-lo de evidência absoluta.

**Condições precisas de cancelamento:**

1. Mesma dimensão e mesmo espaço físico η em todos os modelos. Remover um nuisance apenas num rival ou torná-lo não identificado invalida cancelamento automático; não usar infinito/infinito.
2. Mesma medida sobre os mesmos dados. Cortes diferentes, suporte afim diferente ou outra compressão exigem reconciliação explícita, não apenas pdet.
3. X e C fixos, iguais e independentes de parâmetros/modelo tornam pdet(C), det(F) e potências de 2π fatores comuns que podem sair das integrais e cancelar. Com C dependente de λ ou θ, esses fatores devem permanecer **dentro** de cada integral, ainda que a função seja a mesma nos modelos. Uma função comum dentro de integrais ponderadas diferentemente não cancela em geral.
4. A constante arbitrária κ é diferente desses fatores calculáveis: ela cancela globalmente se realmente for uma única constante comum. Mudanças η=T(θ,modelo)ζ introduzem |det T|; se esse jacobiano varia, não pode ser descartado como κ comum.
5. Limites finitos tornam o prior próprio: conservar probabilidade de cauda/truncamento. Declarar uma caixa “larga” não prova que a correção seja igual nos modelos.
6. Beta livre, δ_C e r_drag precisam de seus próprios priors normalizados. Não cancelar o volume de um parâmetro que só existe num dos rivais.

Pode-se estudar sensibilidade com uma sequência comum de caixas crescentes; a razão plana é o limite quando as massas condicionais nas caixas tendem a 1 e a passagem do limite pelas integrais externas é justificada. Esta unidade não verificou convergência de caudas.

Uniforme em distância D não é uniforme em módulo μ: D/Mpc=10^((μ−25)/5) e dD/dμ=(ln10/5)D. Similarmente, o prior candidato uniforme em s, com δ_C=−5log10(1+s), induz π(δ_C) proporcional a (ln10/5)10^(−δ_C/5) no intervalo transformado. Esses jacobianos não desaparecem por mudar o nome do parâmetro. Nenhum desses priors foi escolhido aqui.

### Composição com o fundo

Em qualquer alternativa, a comparação completa usa

Z_j = ∫ L_bg,j(d_bg|θ_j) L_local,marg[y|h_j(θ_j),δ_j,C] π_j(θ_j,δ_j,…) dθ_j dδ_j … .

A fatoração pressupõe o tratamento autorizado das dependências entre blocos. Não retirar L_bg só porque parte da expressão é comum: o vínculo h_j é diferente. Se λ for sensibilidade, comparar em cada ponto congelado e relatar robustez; se for integrado como nuisance, declarar um prior próprio sobre a família e manter determinantes/normalizações dentro da integral. Nenhuma das opções autoriza escolher o λ que mais favorece um modelo.

## 7. Contrato de implementação, sem novo motor

O JSON fornece a lista ordenada de colunas, os 267 registros esparsos de coeficientes e os 72 ciclos. A implementação futura deve:

1. Carregar as mesmas chaves/linhas já pinadas; não recriar seleção nem acrescentar catálogos.
2. Materializar X, a_h e c_C da especificação e conferir dimensões e índices; transportar todos pela mesma transformação de dados B, se houver redução de linhas.
3. Antes da likelihood, verificar os vínculos nos valores efetivamente abertos e executar o guard de suporte existente. A redução deve preservar o jacobiano de medida; não tratar uma seleção arbitrária de linhas como base ortonormal.
4. Escolher a alternativa de medida dos 63 nuisance e seus parâmetros/domínio; manter essa escolha nos cinco modelos. Não adicionar âncora/MAS/HMS outra vez.
5. Manter os fatores da compressão, do suporte, dos priors e dos jacobianos necessários à comparação normalizada. Separar sensibilidade de covariância dos parâmetros físicos dos modelos.

O roteiro fecha o **projeto linear e suas condições de medida**. Não decide H5, prior físico, família residual ratificada ou abertura V1. Não reproduz o guard nem cria uma nova camada de funções de física.

## 8. Custódia e falha preservada

A primeira validação parou porque o SHA de `FASE9_V1_CANDIDATE.json` já não coincidia com o pin herdado em `F9_ASSEMBLY_MANIFEST.json`. O texto da montagem F9 confere seu próprio hash. `VALIDACAO_INICIAL.json` preserva a falha; `INPUTS_PINADOS.json` registra os hashes esperado/atual da dependência e o fato de que seu conteúdo **não** foi usado. Nenhum repin do V1 foi feito. A coordenação foi avisada.

A especificação depende dos identificadores upstream e do texto F9 conferido, não de uma ratificação inferida desse manifesto. Arquivos desta unidade são novos; artefatos anteriores, originais, provedores suspensos, kernel e gate permanecem intactos. `MANIFESTO_ENTREGA.json` sela os produtos e as fontes efetivamente consumidas.

<!-- F9_SNAPSHOT_RESOLVED_EC4872EC -->
## Adendo de custódia — snapshot resolvido pela coordenação

[REAL] O proprietário identificou a evolução posterior do candidato V1 e apontou o manifesto F9 para o backup imediato que conserva exatamente o hash da versão usada na revisão. Esta unidade verificou o hash desse snapshot e o da nota: a dependência histórica está resolvida, sem repinar o conteúdo novo e sem repetir o estudo. O manifesto inicial foi recuperado por hash e ambos os manifestos foram copiados em `source_snapshots/`; `RESOLUCAO_CUSTODIA_F9.json` mantém os caminhos e hashes. A falha inicial permanece registrada como história, não como bloqueio atual. Esta resolução não ratifica o V1 evoluído.

