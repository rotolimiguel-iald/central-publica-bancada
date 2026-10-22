# ORDEM018 F1 — covariâncias residuais concretas em H0DN V01

Request: `54feb986-d927-4ff9-aa69-3c07680ee78b`. Estatuto: **[REAL] revisão documental e erros; [DERIVED] família PSD; [OPEN] escolha do contrato científico.** Esta unidade não calculou S, g, H0, ln B nem um novo veredito. Não executou H0DN nem chamou modelos remotos. V01 é a seleção upstream; não é o pré-registro V1 da bancada.

**Conclusão operacional:** a rede já representa âncora, referência estelar por método e repetição do mesmo indicador por diferentes âncoras. O que falta qualificar não é a independência de todos os erros imagináveis: são dependências residuais delimitadas entre as referências estelares de N4258 e entre medições das mesmas hospedeiras. Há uma alternativa executável por sensibilidade, abaixo, sem inventar uma matriz medida nem somar erros duas vezes.

## 1. Evidência existente e seleção preservada

Reutilizado integralmente `../SELECTION_V01_IDENTIFIERS.json`: 178 equações de hospedeiras, 14 referências MAS; 12 registros JAGB em 11 hospedeiras, todas com Cepheids e TRGB; 13 identificadores de SNe compartilhados, nenhum acrescentado à lista de calibradores por introduzir JAGB. N5643 tem JAGB de duas fontes. As linhas SN existentes continuam uma vez cada; um resultado agregado de H0 por método não vira observação adicional.

`ERROR_COMPONENTS.json` acrescenta somente erros e identificadores, com as linhas originais. A auditoria leu 104 grupos HMS distintos; todos os erros dentro de cada HMS são exatamente iguais nesta seleção. Nenhuma referência MAS ausente. Nenhum valor central foi convertido em número pelo script. Artigos completos contêm resultados e algumas tabelas foram vistas na leitura: isto **não é um estudo cego**; a família abaixo não foi ajustada nem comparada aos centros.

### O que o código já representa

Fontes de código: `../../upstream/h0_constrainer/h0_constrainer/equations.py:334–376`; definições em `data_loader.py:328–400,450–505`.

| Termo | Chave exata | Tratamento existente |
|---|---|---|
| Distância geométrica | mesma âncora | acrescenta a mesma variância a todo par, inclusive diagonal |
| Referência estelar MAS | método + âncora + fonte | compartilha o erro daquela referência entre todas as hospedeiras que a usam |
| Medição estelar HMS | hospedeira + método + fonte | compartilha a medição repetida sob âncoras distintas; diagonal já contém esse erro |
| Distância da hospedeira | parâmetro comum | une métodos na mesma distância; não é uma covariância de erro adicional |
| SN e intercepto de fluxo | equações já existentes | não se multiplicam pelo número de indicadores estelares |

HMS/MAS incluem instrumento no nome do método. Logo `ceph_hst` e `ceph_jwst`, ou fontes CCHP e SH0ES, são grupos distintos. A matriz de fluxo SN fornecida não é a matriz estelar inteira. O modelo documental da rede explicita a decomposição dos erros originais em hospedeira, referência na âncora e distância geométrica; não se deve adicionar o erro total de um artigo a esses componentes de novo. [H0DN, §II.1 e B.3.2](https://arxiv.org/html/2510.23823v1) — cópia `sources/h0dn.txt:374–385,1939–1954`.

N4258 geométrico: **0,032 mag**, `anchors.dat:2`. Referências JAGB CCHP e SH0ES: **0,05 mag cada**, `host_data.dat:315,327`. Estes três erros têm papéis diferentes. Na comparação entre métodos ancorados em N4258, a distância geométrica comum cancela; os erros das referências estelares não cancelam automaticamente. A comparação publicada explicita sua hipótese de erros não correlacionados, admite uma covariância para sistemáticas relativas e apresenta orçamentos ilustrativos, não uma matriz cruzada medida para esta seleção. [Riess et al., §II.2](https://arxiv.org/html/2408.11770v2) — `sources/method_comparison.txt:138–145`.

## 2. Dependências concretas, limites e números publicados

**CCHP JAGB.** Há termos de modo, suavização, convergência radial, abertura e extinção; N4258 possui ainda calibração fotométrica. A Tabela 3 mostra 0,03 mag na coluna de abertura, enquanto §III.6.2 e a Tabela 5 usam 0,02 mag: não resolvi essa diferença escolhendo um valor. A suavização de N4258 tem erro publicado de 0,05 mag. Esses orçamentos não fornecem coeficientes cruzados Cepheids×TRGB×JAGB. Preservam-se os erros de V01 até uma reconciliação componente a componente. [Lee et al., Tabelas 3/5 e §III.6–7](https://arxiv.org/html/2408.03474v2) — `sources/jagb_cchp.txt:561–617`; Tabela 3 na mesma cópia.

**SH0ES JAGB.** A distância usa variantes estatísticas e erros de extinção/referência; o erro geométrico de 0,032 mag é excluído das tabelas de distância para ser adicionado uma vez. A estimativa de 0,06 mag por variação intrínseca/metodológica não é um coeficiente de correlação e não autoriza acrescentar automaticamente 0,06 mag ao MAS de V01. N5643 tem campos comuns entre GO-1685 e GO-1995; o Apêndice A encontra 857 estrelas correspondentes numa comparação. Isso torna a dependência concreta, mas não publica a covariância das duas estimativas finais de V01. A compilação ampliada do artigo também não substitui os 12 registros escolhidos. [Li et al., §III–IV e Apêndice A](https://arxiv.org/html/2502.05259v2) — `sources/jagb_sh0es.txt:384–397,615,785–789`.

**Combinação CCHP revisada.** A versão consultada adiou a combinação dos três métodos, combinou TRGB/JAGB por hospedeira e preservou o erro geométrico comum. A covariância do ajuste de SNe descrita no texto não é a matriz estelar residual procurada. [Freedman et al., Apêndice B](https://arxiv.org/html/2408.06153v3) — `sources/cchp_overview.txt:1387–1392`.

| Origem residual delimitada | O que se compartilha | Já no modelo? | O que não está numericamente identificado |
|---|---|---|---|
| N4258 geométrico | mesma distância maser | sim, âncora | nada a acrescentar aqui |
| N4258, mesmo método/fonte | mesma estimativa estelar de referência | sim, MAS | partição física fina de seu orçamento |
| N4258, métodos/fonte diferentes | calibração, extinção e seleção de campos possivelmente comuns | distância geométrica sim; referência cruzada não | covariâncias residuais dessas referências |
| Mesma hospedeira em âncoras diferentes | mesma medição estelar | sim, HMS | nada a duplicar |
| Mesma hospedeira entre métodos/fontes | extinção, calibração/ambiente e, onde documentado, imagem/catálogo comum | parâmetro de distância sim; erro cruzado não | fração e sinal do erro diferencial comum |
| N5643 JAGB CCHP/SH0ES | campos/estrelas parcialmente comuns, filtros e procedimentos diferentes | âncora sim; fontes separadas | covariância das estimativas finais, não a correlação das estrelas no diagrama cor–magnitude |
| SN da mesma hospedeira | mesmo calibrador secundário | sim, equação comum | não contar novamente um H0 agregado |

O mesmo software ou a mesma galáxia não implica correlação unitária. Populações estelares diferentes também não demonstram correlação zero de calibração. Os termos acima justificam uma revisão limitada; não se propõe uma lista infinita de falhas hipotéticas. Dentro dos cinco artigos arquivados e dos arquivos V01 examinados, **não foi localizada uma matriz numérica residual conjunta das três classes**, além da construção âncora/MAS/HMS. É um limite desta revisão, não uma afirmação sobre toda a literatura.

## 3. As 11 hospedeiras: onde aplicar o bloco local

| Hospedeira | Fonte JAGB | Erro HMS JAGB em V01 (mag) | SNe compartilhadas |
|---|---|---|---|
| M101 | CCHP | 0,045 | 2011fe |
| N1365 | CCHP | 0,039 | 2012fr |
| N1448 | SH0ES | 0,04 | 2001el, 2021pit |
| N1559 | SH0ES | 0,04 | 2005df |
| N2442 | CCHP | 0,044 | 2015F |
| N3447 | SH0ES | 0,07 | 2012ht |
| N4536 | CCHP | 0,034 | 1981B |
| N4639 | CCHP | 0,039 | 1990N |
| N5584 | SH0ES | 0,04 | 2007af |
| N5643 | CCHP / SH0ES | 0,038 / 0,04 | 2013aa, 2017cbv |
| N7250 | CCHP | 0,043 | 2013dy |

Identidades, demais métodos e linhas: `ERROR_COMPONENTS.json`, campos `eleven_host_method_rows`, `jagb_host_errors` e `mas_reference_errors`. A tabela usa somente os erros de `host_data.dat`, não médias reestimadas nem os erros totais de uma compilação posterior.

## 4. Duas alternativas justificadas

**Alternativa A — reconstrução por componentes comuns.** Obter os catálogos/campos e os orçamentos de calibração correspondentes aos registros efetivamente usados. Reamostrar conjuntamente as estrelas/imagens comuns, com uma única perturbação por calibração/extinção compartilhada; recalcular ambos os estimadores em cada realização. Variantes metodológicas precisam de regra prévia de combinação; não são amostras independentes. N4258 tem uma só perturbação geométrica, separada das medições estelares. Conservar o pareamento de campos e estrelas em N5643 e as mesmas linhas SN. A covariância resultante tem a forma J V Jᵀ, V PSD, com derivadas e fontes registradas.

Vantagem: identifica uma covariância vinculada ao processo de medição. Limite: os erros agregados disponíveis não determinam sozinhos V nem todas as derivadas; não basta reamostrar distâncias publicadas como independentes. Esta alternativa não foi executada nem é condição para começar uma análise de sensibilidade honesta.

**Alternativa B — envelope PSD pré-especificado, preservando as marginais publicadas.** Manter âncora e erros V01; variar somente a alocação de frações dos erros MAS/HMS a modos compartilhados explicitamente delimitados. A família abaixo produz matrizes válidas e contém o modelo publicado como referência. Relatar o intervalo de conclusões e eventual mudança de decisão, nunca escolher a correlação que maximiza a preferência por TGL. São escolhas de sensibilidade instrumental/estatística, não parâmetros novos da física nem medições de correlação.

Recomendação para a F1: **B permite avançar agora**, com contrato declarado; A é a melhoria posterior quando os componentes necessários estiverem acessíveis. Se o resultado depender de uma faixa ainda não sustentada, a dependência deve ficar no resultado, sem veto genérico a investigar.

## 5. Família candidata PSD — derivação própria

Seja i uma equação estelar, sᵢ seu erro de hospedeira; a, m, h são os desvios padrão de âncora, MAS e HMS. A, B e H são matrizes indicadoras: uma entrada 1 por linha para a respectiva chave. Dₘ e Dₕ são diagonais dos desvios MAS e HMS.

No código, para i≠j:

C₀ᵢⱼ = 1[âncoraᵢ=âncoraⱼ] a² + 1[MASᵢ=MASⱼ] m² + 1[HMSᵢ=HMSⱼ] h²;

C₀ᵢᵢ = sᵢ² + aᵢ² + mᵢ².

Defina D₀ᵢᵢ = sᵢ² − h(HMSᵢ)². Então exatamente:

C₀ = D₀ + A diag(a²) Aᵀ + B Dₘ² Bᵀ + H Dₕ² Hᵀ.

A auditoria de erros, sem construir C, encontrou igualdade exata dentro de todos os 104 HMS: **D₀=0 nesta seleção**. No caso geral deve ser não negativo; erro negativo exige revisão, não clipping silencioso.

A família é:

**C(θ) = D₀ + A diag(a²) Aᵀ + B Dₘ Rₘ(θ) Dₘ Bᵀ + H Dₕ Rₕ(θ) Dₕ Hᵀ.**

Rₘ e Rₕ são matrizes de correlação PSD com diagonal 1. Os outros blocos da rede permanecem como especificados no contrato, sem duplicações. Esta expressão cobre o bloco estelar, não presume uma matriz nova para SN ou para o fundo cosmológico.

**Prova.** Para qualquer vetor x, cada termo quadrático é não negativo: por exemplo, (DₘBᵀx)ᵀ Rₘ (DₘBᵀx)≥0. A soma é PSD. Como cada linha escolhe uma única chave MAS/HMS e diag R=1, todas as variâncias individuais permanecem sᵢ²+aᵢ²+mᵢ². Equações repetindo o mesmo HMS continuam usando o mesmo erro primitivo. Rₘ=Rₕ=I recupera C₀. Isso prova admissibilidade algébrica, não a veracidade física de uma correlação escolhida.

### Parametrização concreta sem pares incompatíveis

Para um conjunto G de chaves primitivas, E_G(ε) tem bloco εεᵀ em G (cada ε=±1), identidade fora de G e zeros entre os dois; portanto é PSD e tem diagonal 1. Vários conjuntos disjuntos podem formar uma única matriz de blocos E. Propõe-se:

Rₘ = (1−u−v)I + u E_ref + v E_J;
Rₕ = (1−p−q)I + p E_host + q E_5643.

- E_ref: dois grupos disjuntos, referências **JWST CCHP** e **JWST SH0ES** em N4258, cada um reunindo Cepheids/TRGB/JAGB presentes. Representa sensibilidade à calibração/campos da mesma campanha; não afirma que todas as estrelas sejam comuns. Os demais MAS continuam com identidade neste componente.
- E_J: par das referências JAGB CCHP/SH0ES em N4258. Representa a incerteza residual na ligação entre as duas estimativas da mesma população de referência.
- E_host: um bloco para cada uma das 11 hospedeiras, com suas chaves HMS Cepheids/TRGB/JAGB; não correlaciona hospedeiras distintas por esse termo. É um envelope para o componente local comum; não identifica extinção, população ou imagem como um único mecanismo físico.
- E_5643: apenas o par HMS JAGB de N5643, motivado pelo cruzamento documentado de campos/estrelas.

u,v,p,q≥0; u+v≤1 e p+q≤1. As frações repartem orçamentos existentes; não adicionam uma segunda variância. A correlação de um par será a soma dos componentes aos quais ambos pertencem, com seus sinais; pares não podem receber ρ livre ignorando a PSD global.

**Grade candidata, ainda não ratificada:** cada parâmetro em {0, 1/4, 1/2, 3/4}, com u+v≤3/4 e p+q≤3/4. Sinais: três cenários determinísticos em todos os blocos — (a) todos positivos; (b) Cepheids com sinal oposto a TRGB/JAGB; (c) JAGB SH0ES com sinal oposto aos demais. Esses extremos assinados não são hipóteses físicas favorecidas nem uma cobertura exaustiva de toda matriz PSD. Não se selecionam usando resíduos observados. Usar toda a grade congelada, ou reduzi-la antes do ajuste e justificar a redução por custo/desenho, nunca por resultado.

**Suporte.** Nessa grade Rₘ,Rₕ≥I/4. Logo o núcleo de C(θ) coincide com o núcleo de C₀: ambos são a interseção dos núcleos dos mesmos fatores positivos. Isso evita que a exploração interior crie um suporte observacional diferente. Os extremos u+v=1 ou p+q=1 podem reduzir o posto; servem como diagnóstico separado, não entram automaticamente numa comparação de evidências sobre medidas de suporte diferentes. O guard de suporte já construído pela coordenação continua necessário para os modelos de média.

### Escala dos coeficientes, sem escolher correlações

Somente para o subcaso com dois pares JAGB correlacionados:

- duas hospedeiras distintas, uma JAGB CCHP e outra SH0ES: contribuição da âncora e referência = **0,001024 + 0,0025 ρₘ mag²**;
- duas estimativas JAGB em N5643: acrescenta **0,00152 ρₕ mag²**.

São produtos dos erros lidos, registrados por `audit_errors.py`; não são covariâncias medidas. Não se extraiu ρ dos centros.

### Limite físico importante

A família conserva a separação primitiva MAS/HMS do upstream. Uma sistemática que afeta simultaneamente a hospedeira e a referência pode exigir covariância **entre** esses blocos. Seu efeito em distância relativa é proporcional à diferença das respostas, J_host−J_anchor; um zero point idêntico pode cancelar. Nesse caso adota-se a alternativa A com esse jacobiano e realoca-se o orçamento existente. Somar um zero point positivo a todas as distâncias ou declarar que ele não cancela seria outra hipótese, não consequência desta família. A falta dessa decomposição fina limita o alcance do envelope, sem obrigar supor todas as correlações imagináveis.

## 6. O que a coordenação precisa congelar

1. A seleção V01 e as equações SN compartilhadas já documentadas.
2. Alternativa A ou B; em B, os grupos, sinais e grade (ou outra parametrização PSD explicitamente motivada).
3. Regra de relato em toda a grade e critério de robustez; não otimizar/marginalizar pesos sem um prior científico declarado.
4. Modelo de média físico separado desses parâmetros de sensibilidade; preservar os cinco rivais e as suas normalizações no contrato da coordenação.
5. Tratamento das normalizações e suporte já construído; nada nesta entrega substitui o guard existente.

Não é preciso produzir uma nova função de física ou exigir uma independência absoluta dos três indicadores. É preciso escolher e registrar o tratamento desses componentes concretos. Nenhum resultado 5σ surge desta revisão documental.

## 7. Custódia e reprodução

`PRIMARY_SOURCES.json` contém URLs versionadas, SHA256 e caminhos dos cinco HTMLs públicos; cada TXT derivado tem hash próprio e linhas locais, diferentes das linhas da ferramenta web. `ERROR_COMPONENTS.json` contém erros/identificadores e produtos exatos Decimal. `CONTRATO_PSD_CANDIDATO.json` explicita parâmetros e limites, sem estimativas. `MANIFESTO_ENTREGA.json` sela os derivados e aponta para os manifestos anteriores.

Scripts próprios: `archive_primary.py` (GET público, arquivo íntegro) e `audit_errors.py` (somente erros/identificadores). Não executam/importam H0DN. O bloqueio da âncora do executor MiMo permanece preservado; nenhuma nova submissão remota foi feita. Originais, kernel, gate e os seis artefatos da entrega JAGB anterior permanecem intactos.