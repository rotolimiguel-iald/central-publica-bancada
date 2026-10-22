# ORDEM018 — H0DN, covariância e identificação do efeito

05/10/2026, hora local. Revisão documental pedida pela coordenação. Sem executar H0DN, ajustar parâmetros, alterar pré-registro ou emitir novo veredito observacional.

## Resultado e alcance

[REAL — inspeção] O H0DN oferece os ingredientes para desenhar um contraste entre um deslocamento universal da escala local e um viés **diferencial** das distâncias obtidas por Cefeidas. A revisão local verificou 24 arquivos públicos contra os blobs do commit registrado em `UPSTREAM_MANIFEST.json`. `STRUCTURE_AUDIT.json` contém os resultados estruturais e as linhas das funções. Isto não é uma reprodução do ajuste publicado.

[DERIVED] O teste deve usar a rede de distâncias e suas dependências. Um único H0 comprimido perde a informação que distingue os métodos. Deslocamento universal com uma escala H0 inteiramente livre é degenerado; uma referência de fundo independente ou outras previsões distintivas são necessárias. A rede e seus componentes não podem ser multiplicados como observações independentes.

[OPEN] A revisão não prova que a lei TGL atua de modo universal sobre todos esses indicadores. Essa correspondência deve vir da previsão canônica de cada observável, incluindo distâncias geométricas e fotométricas, e da seleção congelada. Ela não pode ser escolhida depois de comparar os resultados.

## O que foi conferido no código público

Todos os caminhos abaixo são relativos a `upstream/`, uma cópia para leitura. O manifesto gera os URLs raw com o commit fixado; nenhum código de terceiros foi importado ou executado.

| Referente | Leitura estática |
|---|---|
| `h0_constrainer/configs/config.ini:16` | Configuração baseline: hosts, SNe Ia/Pantheon+, SBF, grupos e megamasers. Filtros excluem JAGB, Miras, b25 e SMC; q0 e j0 são fixados. |
| `h0_constrainer/h0_constrainer/data_loader.py:65` | Identificadores de hospedeira, método, âncora e fonte são preservados. MAS significa método–âncora–fonte; HMS, hospedeira–método–fonte. |
| `h0_constrainer/h0_constrainer/data_loader.py:328` | Linhas de referência são retiradas dos hosts e usadas para as incertezas MAS. Existem fallbacks com avisos; eventual adaptador da bancada deve recusar referências ausentes. |
| `h0_constrainer/h0_constrainer/equations.py:334` | C global nasce na montagem: variâncias dos hosts, componentes compartilhadas de âncora/MAS e termos HMS fora da diagonal. A matriz depende da seleção. |
| `h0_constrainer/h0_constrainer/equations.py:399` | SNe calibradoras ligam magnitude absoluta e distância da hospedeira; linhas do fluxo ligam magnitude absoluta a log10(H0); megamasers têm linhas próprias. |
| `h0_constrainer/h0_constrainer/intercept.py:227` | Covariância fotométrica dividida por 25 para unidades do intercepto, adicionando variância de velocidade. Compressão usa a covariância fora da diagonal por padrão. |
| `h0_constrainer/h0_constrainer/solver.py:85` | Pseudoinversa de C com `atol=1e-10`, `rtol=0`; a matriz normal é invertida por `np.linalg.inv`. Graus de liberdade: rank(C)−npars. |
| `idlcode/mpinv.pro:46` e `idlcode/org_v3p9.pro:2154` | IDL chama pseudoinversa sem tolerância explícita; o default é relativo à maior singularidade, dimensão e precisão de máquina. Não é o mesmo critério numérico do Python. |

[REAL — estrutura dos arquivos] A tabela bruta tem 363 linhas. Aplicando somente os padrões de exclusão baseline e retirando linhas de âncora, restam 272: 112 ceph_hst, 8 ceph_jwst, 26 trgb_jwst e 126 trgb_hst. Há **20 hospedeiras com Cefeidas e TRGB** nessa seleção preliminar. Não é a seleção final: não executamos o casamento com calibradores/grupos (`rung_equalize`). Portanto 272 não é número de observações independentes nem de equações do ajuste publicado.

[REAL — covariância fornecida] `data/sn1a_covar_pp.dat` contém uma matriz 277×277, finita, simétrica na leitura e com diagonal positiva; 76.452 entradas fora da diagonal são não nulas. **É a covariância SN do fluxo, não a covariância da rede inteira.** Não foi calculado espectro, rank ou positividade semidefinida, nem gerada a C global. O cabeçalho dimensional está em notação científica. O parser local foi corrigido para aceitar esse formato, PGC opcional e comentários `#`/`;`; as duas primeiras tentativas pararam antes do recibo.

## Onde inserir cada hipótese — derivação condicional

Escreva o sistema no formato do programa:

\[
y=A x+\epsilon,\qquad \operatorname{Cov}(\epsilon)=C,
\qquad h=\log_{10}H_0.
\]

Na equação dos hosts, um **viés positivo no módulo publicado** das Cefeidas pode ser parametrizado como

\[
E[y_i]=\mu_{g(i)}+c_i\delta_C,
\qquad c_i=1\ \text{nas linhas Cefeida admitidas; }0\text{ nas demais}.
\]

Isto define uma hipótese diferencial, não qualquer possível erro das Cefeidas. Por exemplo, um deslocamento idêntico de zero fotométrico em hospedeiras e âncoras pode cancelar na diferença usada para inferir distância. Tal mecanismo exige outra resposta, calculada antes da compressão. Não substituir todos os mecanismos por uma etiqueta binária.

Para uma mesma hospedeira medida por Cefeidas e TRGB,

\[
E[y_C-y_T]=\delta_C,\qquad
\operatorname{Var}(y_C-y_T)=C_{CC}+C_{TT}-2C_{CT}.
\]

A distância da hospedeira cancela. Esse é o contraste que a média final H0 sozinha não preserva. As 20 coincidências de identificador localizadas são candidatas a esse teste, sujeitas à seleção completa, covariância e consistência dos estimadores.

Para a rota canônica condicional `H_local = K H_background`, com K positivo e comum,

\[
h=\log_{10}b+\log_{10}K.
\]

O termo comum atua nas linhas que contêm h por meio da coluna `A[:,ihub]`. Não se soma a todas as linhas de magnitude do sistema indiscriminadamente. Se b é livre e só há a rede local, mudar K e compensar b mantém h: **a rede local, isolada, não identifica K**. Uma âncora de fundo independente torna essa comparação possível; se essa âncora já incorporou dados locais, é preciso recuperar a likelihood conjunta ou suas dependências.

Num ramo apenas Cefeida, com intercepto SN fixo, aumentar o módulo inferido em dμ reduz M_B em dμ e reduz log10(H0) em 0,2dμ. No modelo acima δ_C é o viés da **medição**: removê-lo reduz μ e aumenta log10(H0) em 0,2δ_C. Fixar o sinal pela definição evita inverter o efeito. Na rede mista a propagação deve ser calculada com A e C; não impor esse fator a todo o resultado agregado.

Uma implementação não precisa criar outra física: precisa transportar a resposta prevista até essas linhas, conservar a tipagem/unidade e mostrar quais contrastes sobrevivem à marginalização dos parâmetros existentes.

## Correção ao lado da revisão anterior: C pode ser singular

A nota anterior `../covariance_identifiability/REVISAO_LOCAL.md` tratou explicitamente C definida positiva. O H0DN exige a extensão semidefinida. O artigo explica a redundância das equações e o uso de pseudoinversa; também descreve a compressão do fluxo em interceptos e suas hipóteses cosmográficas. Isso apoia a leitura do código, não substitui a validação numérica de uma extensão TGL. Fonte: [H0DN, apêndice B](https://arxiv.org/html/2510.23823v1).

[DERIVED — álgebra] Se C=U₊Λ₊U₊ᵀ e N contém uma base do núcleo, a likelihood gaussiana degenerada requer

\[
N^T(y-Ax-R\eta)=0,
\qquad
\chi^2=(y-Ax-R\eta)^T C^+(y-Ax-R\eta).
\]

A segunda expressão sozinha não impõe a primeira. Exemplo exato: C=[[1,1],[1,1]] representa a duplicação da mesma medida. Para y=(a,a), a média proposta (m+δ,m−δ) tem custo pela pseudoinversa **independente de δ**, embora a relação determinística exija δ=0. Logo não se deve declarar uma nova direção de sinal invisível/inócua apenas porque a pseudoinversa a anulou.

Se a rede é construída como y=Bz a partir das medidas elementares, uma resposta física r nessas medidas deve chegar como Br. Isso preserva automaticamente as mesmas relações lineares. Esta é a forma segura de estender hipóteses sem criar sinal artificial nas equações redundantes.

Para as direções que respeitam o suporte, tome W=Λ₊^(-1/2)U₊ᵀ, Z=W A_nuis e P=ZZ⁺. Então a informação sobre duas respostas R=[r_U,r_C], após perfil dos nuisance, é

\[
F_R=R^T W^T(I-P)W R.
\]

Separação local de dois parâmetros exige rank(F_R)=2. Se h está livre em `A_nuis`, r_U=A[:,ihub] já está no espaço removido: não há informação adicional sobre um deslocamento universal. Incluir o bloco de fundo muda o problema e pode quebrar essa degenerescência. O critério deve ser aplicado ao sistema conjunto especificado, não a um slogan sobre independência.

[OPEN — validação da futura extensão] Guardar suporte, escala das unidades, espectro/rank de C e do desenho branqueado. Comparar os critérios IDL/Python sem escolher a tolerância pelo resultado. `rank(C)−npars` pressupõe identificabilidade de todas as colunas; com colunas novas, verificar o rank efetivo. Não foi demonstrado aqui defeito no resultado publicado: essas exigências são para estender o modelo sem resultados silenciosamente inválidos.

## Integração útil à bancada

1. Manter residentes os identificadores, A, C, decomposição do suporte e as respostas previstas; derivados devem carregar o hash da seleção e das fontes.
2. Na navegação, ligar método → âncora → hospedeira → calibrador → fluxo; mostrar contrastes Cefeida–TRGB, componentes comuns e o que a marginalização absorve.
3. Seleção de cenário troca a previsão, não altera os dados. Se muda a seleção ou a cosmografia, recompor os blocos que dependem dela e invalidar os derivados afetados.
4. O intercepto comprimido serve para o modelo em que sua resposta é a direção comum. Uma previsão TGL que altera a forma em redshift ou a relação entre distância luminosa e angular requer retornar aos dados do fluxo. Não aplicar uma correção pós-compressão e chamá-la automaticamente de teste integral.
5. O fator constante descartado pela compressão cancela em razões somente sob o mesmo modelo de dados/seleção/covariância. Comparações que os alteram devem conservar normalizações e termos apropriados.
6. Registrar IDs de origem e sobreposição. H0DN, SH0ES, CCHP e variantes da mesma rede são vistas relacionadas; dependência não vira independência por terem nomes diferentes.

Esta seção é desenho de integração. Nenhuma API, interface ou serviço residente foi modificado nesta revisão.

## ACT DR6 e CMB-S4 — atualização documental

[KNOWN — publicado, não reproduzido] No [ACT DR6 v2](https://arxiv.org/html/2503.14454v2), a combinação P-ACT-LB reúne Planck+ACT, lenteamento CMB e BAO DESI Year-1. Os resultados para N_eff dependem do conjunto/modelo:

| Conjunto | N_eff, 68% | Referência |
|---|---|---|
| P-ACT-LB | 2,86±0,13 | Eq.30 |
| P-ACT-LB-D | 2,87±0,13 | Eq.43; acrescenta deutério observado |
| P-ACT-LB-D-He | 2,89±0,11 | Eq.44; acrescenta deutério e hélio observados |
| P-ACT-LB com Yp também livre | 3,14±0,25 | Eq.46; outra extensão |
| P-ACT-LB_DR2 | 2,92±0,12 | Apêndice I; DESI DR2 substitui Year-1 |

Consistência BBN como relação teórica não é o mesmo que incorporar abundâncias observadas. As Eq.43–44 usam PRyMordial e incertezas teóricas/observacionais. Estes resultados compartilham dados: não multiplicá-los entre si, nem adicionar BBN novamente ao caso D-He. Também não tratar a restrição marginal publicada como likelihood TGL sem verificar a correspondência do modelo.

[KNOWN — estado institucional] O [site oficial CMB-S4](https://cmb-s4.org/) informa retirada de apoio DOE/NSF em 09/07/2025 e encerramento organizado do projeto. Projeções antigas não representam um cronograma operacional garantido.

Nenhum poder, fit, Bayes factor, significância ou veredito novo foi calculado nesta revisão. A projeção F0 da coordenação continua condicional às suas hipóteses; este relatório não a promove a resultado observado.

## Entrega e decisão seguinte

**Aproveitar a rede H0DN como estrutura de teste, mantendo a inspeção por método e o suporte da covariância.** Para executar a comparação ainda é necessário unificar e ratificar o V1 já em preparação, especificando a resposta TGL, o rival diferencial, a âncora de fundo e as dependências. Isso é fixar o teste observacional; não exige criar outra camada de teoremas nem desconsidera retrodições sem ajuste.

Artefatos desta unidade: `UPSTREAM_MANIFEST.json`, `UPSTREAM_TREE.json`, `STRUCTURE_AUDIT.json`, `fetch_sources.py`, `audit_structure.py`. Cópia selecionada para revisão, não instalação completa executável do H0DN. Originais, kernel, gate e pré-registros preservados.
