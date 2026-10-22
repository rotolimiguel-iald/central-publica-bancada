# R90 — ACOM v18 recuperado: representação efetiva e alcance do elo

Autor /root/r69_locality_bridge. [REAL — recuperação e leitura de arquivos; DERIVED — análise de tipos/operações]. Missão própria project/check revisão577, ready. Nenhum código científico foi importado ou executado; benchmarks são registros anteriores lidos, não reproduzidos.

## 1. Caminho de recuperação que resolve a remissão

Os lotes P2_imac_acom_039 a042 fornecidos pela gerência indexam18 documentos, de ACOM trinity e Unified até v13. Todos os18 corpus textuais indicados existem e foram consultados por padrões focais; nenhum retornou v18/Dirac/triplo espectral/Nicolai/flutuação interna. A inspeção do diretório científico correspondente confirmou essa família de versões. Não se tratou arquivo ausente como texto vazio: a verificação final de existência está na cobertura pinada.

A busca por CAMINHOS v18 no índice encontrou P3_iald_raiz_117.json:92,123,138,153, apontando os resultados do ACOM em C:\IALD\projetos_pyhton\acom. A listagem apenas desse diretório revelou os fontes reais:
- acom_v18_dirac.py;
- acom_v18_graviton.py;
- acom_v17_vs_v18_comparison.py;
- tgl_quantizer_v2_2_spectral.py e iald_spectral_v1.py como vizinhos científicos pertinentes.

Isto corrige ao lado a limitação de recuperação R88 ('v18 não localizado naquela consulta; v17 público localizado'). A fonte v18 EXISTE; não há justificativa para continuar procurando essa versão por ausência presumida. Não se refez nenhuma das69 extrações R67.

## 2. As equações realmente implementadas

| Fonte:linhas | Operação encontrada | Estatuto e alcance |
|---|---|---|
| acom_v18_dirac.py:16–37 | Cabeçalho declara D√e, álgebra Aα e triplo (Aα,L²(Σ),D√e); preserva g=√|L| e4 estados | [DECLARADO na origem] interpretação do algoritmo como triplo; a leitura abaixo verifica o corpo do código. |
| :173–202 | angular_bits, alpha_bits_fraction e grade senoidal; repartição de bits denominada interpretação fatorada | [REAL fonte] configuração de quantização. Não confundir a fração de bits configurável com acoplamento físico derivado. |
| :204–212,281–324 | ψ=2·1_(L<0)+1_(ΔL>0), ΔL_j=L_j−L_(j−1); g_j=√(|L_j|+ε); θ_j=arcsin(clamp(g_j/(gmax+ε))) | [REAL fonte] classificação de4 estados por sinais e transformação de um vetor de dados achatado. O rótulo 'derivada temporal' não inclui aqui passo físico de tempo ou carta de espaço-tempo. |
| :252–278 | Q=round[(θ/(π/2)+ε)^(1/(1+β))·(2^b−1)], com clamp; inversa usa potência1+β | [REAL fonte] quantização não linear e não injetiva para resolução finita. |
| :419–445 | reconstrói θ, g=gmax sinθ e L′=sign(ψ)g² | [REAL fonte] realização concreta da dobra/reconstrução, com erro de quantização; não declara igualdade irrestrita L′=L. |
| :361–376 | razão de contagens 'beta_emergent'; variância angular; custo em nats; tetelestai_simple compara variância aβ e tetelestai_form aα | [REAL fonte] diagnósticos algorítmicos. Não são Euler de S_total nem comprovação de conservação de stress. |
| acom_v18_graviton.py:182–244 | θ(S)=arcsin√(α√S), clipping de g/cosθ, amplitudes sin(g_normθ), reconstrução quadrática | [REAL fonte] outro algoritmo da mesma família, explicitamente dependente da entropia dos dados. Não substituir silenciosamente β canônico por esse parâmetro adaptativo. |
| tgl_quantizer_v2_2_spectral.py:32–45,228–284,339–347 | Aα observa/classifica; D√e=quantização de |w|; faixas por máscara usam round e poda de vácuo; w′=sign(ψ)|w|_q | [REAL fonte] a própria docstring define o chamado Dirac como quantizador, sem necessidade de adivinhar seu significado. |

O operador implementado dirac_operate não é linear: mesmo mantendo máscara, bits e extremos fixos, round com níveis finitos é constante por intervalos e muda por saltos; em domínio que atravesse um limiar não preserva superposição. O corpo ainda faz os extremos dependerem dos dados, reforçando que não é um operador linear fixo em um Hilbert especificado. Essa constatação analítica de estrutura não é teste de desempenho nem refutação da ontologia do algoritmo. O algoritmo pode materializar uma leitura operacional; não fornece, apenas por seu nome, o D autoadjunto de um triplo de Connes ou a representação de 1-formas a[D,b].

## 3. O que os recibos antigos efetivamente medem

acom_v18_dirac_benchmark_20260304_194912.json registra7 conjuntos, compressão, correlação, PSNR e throughput; hardware CPU, torch2.10.0+cpu. A comparação v17/v18 das19:50 registra os mesmos tipos de métricas e explicita quantização uniforme versus bifatorada. acom_v18_results.json é GRAVITON, com11 conjuntos e métricas de compressão/reconstrução. Não transferimos o nome, a versão ou os resultados entre DIRAC e GRAVITON. Nenhum desses recibos foi apresentado como teste novo, cálculo de espectro de Dirac, equação gravitacional ou medida física.

## 4. Resíduo que a recuperação não pode esconder

O achado positivo é o mapa explícito dado→(sinais,ângulo,níveis)→dado reconstruído, com o D√e operacional definido. Isso sustenta a existência do programa citado e permite reaproveitar sua leitura de contorno. No corpo desses fontes e nos trechos lidos não há mapa do estado discreto ψ para Ψ_μ(x), campos de conexão ou variação da ação EH+ξR|Ψ|²−(dΨ_μ)²/4. Também não aparece igualdade entre o custo/variância do quantizador e S_total, nem um termo que consuma o resíduo ACTION_EOM_RESIDUAL_R89.md.

A métrica do espaço de dados declarada no cabeçalho e g_j=√|L_j| são objetos de tipos diferentes de g_μν(P) e da fonte Hilbert de R83–R89. A ligação teria de transportar a representação, domínio e derivadas; não pode ser feita equiparando as letras g,ψ ouD. A regra de satisfação do autor continua orientando essa ligação. Sua implementação de quantização não autoriza trocar a primeira variação da ação por erro de reconstrução sem uma identidade demonstrada.

## 5. Cobertura auditável e encerramento do levantamento dirigido

Escopo:4 lotes P2 (18 corpus), índice P3_iald_raiz_117, listagem de2 diretórios científicos decorrentes dos caminhos, leitura focal dos2 fontes v18, do quantizador spectral v2.2, cabeçalho/busca de iald_spectral_v1 e v19, e3 recibos pertinentes. A pesquisa lexical não é ausência universal no computador. As ocorrências 'Euler' nas constantes e 'action' dentro de 'fraction' foram excluídas da conclusão: os padrões de cobertura usam limites de palavra. A leitura do código foi estática; não se acessaram pesos, arquivos confidenciais, e-mails ou dados dos exemplos, não se extraíram DOCX novamente e não se chamou provedor.

Resultado: remissão v18 RECUPERADA; mapa algorítmico CONCRETO; identidade com diferencial/ação completa NÃO LOCALIZADA NESTE RECORTE. O R16 não é fechado por essa recuperação. O próximo passo deve consumir fonte concreta dessa identidade ou registrar o resíduo técnico já delimitado; não repetir a busca desta versão nem fazer outra pergunta abstrata de definição.
