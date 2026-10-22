# Plano F1b — reprodução histórica conjunta das Fases 4/5

Identidade: chatgpt-codex/ordem-018/derivacoes. [INPUT] Unidade delegada da ORDEM_018 §5, F1(b). [REAL] Entrega de leitura, inventário e contrato; zero ajustes, zero execução/importação de um.py ou motores originais, zero novos downloads e nenhum veredito científico.

## Alcance e separação dos registros

A reprodução independente é viável por código novo na Central, com NumPy/SciPy e leitura das tabelas congeladas. Nesta unidade a autorização é **preparar o plano**, não iniciar fits. A autorização geral F1b permite reproduzir números históricos; a execução futura deve respeitar este contrato, o pré-registro da reprodução e a direção da coordenação. Não abrange composto novo da Fase 9, cinco hipóteses novas, lançamento de provedores, alteração de fonte, livro de testes, kernel ou gate.

A expressão histórica “cego” é um campo do arquivo antigo, não uma propriedade da reprodução atual. Retrodição sem ajuste preserva seu valor de novidade de uso; a reprodução verifica o cálculo. O β fixo vem de α_CODATA2018·√e em runtime; o ramo β livre é um alvo diagnóstico **arquivado**, não ajuste da constante física nem novo concorrente proposto nesta rodada. Face e leitura/projeção permanecem objetos distintos: as opções de leitores nas Fases 4/5 são contratos explícitos, não deduções automáticas de K.

As rotas d1.fase4_desvio_30set e d1.fase5_sh0es_01out foram consultadas antes dos arquivos. A consulta posterior para ordem018/fase45/F1b retornou zero rota homônima. Preservam-se aposentadorias e resultados anteriores.

| Bloco histórico | Conjuntos na verossimilhança | Escada entra no ajuste? | Leituras/alcance |
|---|---|---|---|
| F4 P_dr2_escada | Planck comprimido + DESI DR2 + SH0ES gaussiano | Sim, H0_local | D1b e D1a |
| F4 Q_dr2_escada_pantheon | P + Pantheon só cosmologia | Sim | D1b e D1a; SN mede forma com M perfilado |
| F4 R_dr1_escada | Planck + DESI DR1 + SH0ES gaussiano | Sim | Replicação correlacionada DR1/DR2, nunca somá-las |
| F4 S_dr2_escada_cc | P + CC32 diagonal | Sim | Distâncias locais e relógios acumulados |
| F4 T_dr2_cc | Planck + DESI DR2 + CC32 diagonal | **Não** | Ramo histórico sem escada; não é apenas Planck+BAO |
| F5 P_dr2_sh0es | Planck + DESI DR2 + Pantheon+SH0ES | **Sim, calibradores dentro** | nenhuma, sombra, acumulada; sombra D1a ao lado |
| F5 Q_dr1_sh0es | Planck + DESI DR1 + Pantheon+SH0ES | Sim | sombra e acumulada |
| F5 S_dr2_sh0es_cc | P F5 + CC32 diagonal | Sim | nenhuma, sombra e acumulada |
| F5 V_sh0es_so | Pantheon+SH0ES apenas | Sim | Validação já reproduzida pela coordenação; reutilizar recibo, não repetir |
| F5 zsplit: ajuste do fundo | Planck + DESI DR2, β=0 | **Não** | θ_fundo congelado antes do GLS |
| F5 zsplit: leitura dos resíduos | Pantheon+SH0ES + θ_fundo fixado acima | **Sim no GLS**, não no ajuste de θ_fundo | M e seis deslocamentos; não chamar o GLS completo de “sem escada” |

P_empilhado (F4, modo tgl) fica inventariado como **controle histórico aposentado**, fora do programa de execução proposto. Não reabrir a dupla aplicação de β como teste. Os resultados F4 e F5 compartilham dados: não multiplicar suas evidências entre si nem tratá-los como replicações independentes. Nas próprias famílias históricas, a soma de blocos assume ausência de covariância cruzada entre conjuntos; a presente reprodução não fornece uma covariância cruzada ausente nem certifica a independência dessa aproximação.

## Arquivos e integridade

Raiz histórica B = C:\IALD\Bancada_Um.
Raiz selada D = C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\d1_camb\v3.
Todos os caminhos absolutos, tamanhos, hashes e intervalos de funções estão em AUDITORIA_E_CONTRATOS.json, calculados sobre bytes nesta rodada. Os dados pequenos e covariâncias reconstruídas deterministicamente por leitura AST estão em ENTRADAS_HISTORICAS_E_COVARIANCIAS.json. A montagem de covariância não é ajuste nem medição de evidência.

| Artefato-alvo | SHA-256 medido |
|---|---|
| B/investigacao/fase4_desvio_30set/PREREGISTRO_FASE4_DESVIO_20260930.json | 22b4c440d8ad844d7dd4071734d10c2776da3a7e1587709cb10f5e7987f4acf9 |
| B/investigacao/fase4_desvio_30set/RESULTADO_FASE4_DESVIO_20260930.json | 10683b334d28d84acdd8a086fe91fcbeaa46e747b0e3b51dc4192c270d8e6219 |
| B/investigacao/fase5_sh0es_01out/PREREGISTRO_FASE5_SH0ES_20261001.json | f9fbf497c90c0a66730d8d87bc6d0a9eb46478889b80908eedef7cea95c7cc63 |
| B/investigacao/fase5_sh0es_01out/RESULTADO_FASE5_SH0ES_20261001.json | 851d1076b85f12f671bfbe018f67e8291a2c83686bb98fb2251a4ed3c254eca2 |
| D/d1_v3_pipeline.py | 4e8f9dc33e28db79970faed641c55571c38939f6558b25f57ada54a1729b5fea |
| B/tabelas/camb_lcdm_v1.npz | 6bc4dd4a092325007ed05504401d6722d2f849956f3168a72b474786b4ce7363 |

[REAL] Dez cruzamentos de identidade passaram: resultado→pré-registro F4/F5, pipeline→manifesto e resultado selado, tabela→manifesto, cronômetros→resultado F4, Pantheon tabela/cov→resultado F5 e cópias locais→originais. São cruzamentos de bytes, não execução científica. O relatório narrativo F4 atual tem 7682 bytes e hash 8cb9c8b208cd5c32f986ed679bb47edb64c9577550345e586bef0644d74929db; diverge do retrato mais antigo do mapa. Isso não foi tratado como corrupção: os alvos são os JSONs conferidos, não a redação mutável do relatório.

## Dados e covariâncias por bloco

| Bloco | Entrada e seleção | Covariância/normalização | Arquivo/hash ou receita |
|---|---|---|---|
| Planck_comp | (R,l_A,ω_b), média lida de D/_dados_reais | Chen,Huang&Wang2019, 3×3; σ=(.0046,.0895,.00015), ρ_Rl=.46, ρ_Rb=−.66, ρ_lb=−.33 | D/pipeline hash acima; B/bancada/fontes.py::planck_chen2019; PDF apenas hasheado, 09effe1d0d8caa0173bf8c826a621fb3606ab884a4d2931b198212a4f47310b5 |
| DESI_DR1 | 12 observáveis e ordem de DESI_ROWS, valores de _dados_reais | diag(σ²) + cinco correlações DM–DH no mesmo z: .510:−.445, .706:−.420, .930:−.389, 1.317:−.444, 2.330:−.477 | D/pipeline + fontes.py::desi_dr1_covariancia; matriz congelada no JSON de entradas |
| DESI_DR2 | 13 componentes, ordem do arquivo mean | Covariância completa 13×13, nenhuma diagonalização | mean 9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585; cov 252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509 |
| SH0ES_local F4 | Média 73.04, σ1.04, lidos do pipeline | Gaussiana escalar em H0K, variância σ² | Mesmo pipeline selado; não acrescentar este bloco a pantheon_sh0es F5 |
| Pantheon F4 | (zHD>.01) AND IS_CALIBRATOR=0; 1580 linhas históricas | Submatriz STAT+SYS simetrizada; M perfilado; μ=5log10[(1+zHEL)DM(zHD)]+25 | Tabela 1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8; cov abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc |
| Pantheon_SH0ES F5 | (zHD>.01) OR IS_CALIBRATOR=1; 1657 linhas =1580+77; 37 hospedeiras segundo o contador histórico | Mesma matriz original 1701²; submatriz completa preserva correlações calibrador/não calibrador; nos calibradores μ=CEPH_DIST | Mesmos hashes acima; M perfilado no vetor completo |
| CC_Moresco F4/F5 | 32 triplas (z,H,σ) importadas do artigo; ordem preservada | **Diag(σ²), histórica**; não substituir por Fase7 | B/fontes_externas/moresco_2022_cc.json, 530db89807c02723e37335eecc6ea94f5eabff005dc74b82938f21aeb75c1948 |

Fontes DR2: C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais\desi_gaussian_bao_ALL_GCcomb_{mean,cov}.txt.
Pantheon original: C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat e C:\IALD\projetos_pyhton\acom\tgl_data_cache\pantheon_covariance.dat.
Cópias autorizadas idênticas: ../reproducao_fase5/Pantheon+SH0ES.dat e pantheon_covariance.dat.
Covariâncias Planck/DR1/CC montadas e dados pequenos: JSON de entradas, SHA-256 f2521084b5b5eaffde38646b8f082bc523eb9360713b824c13f90153f831ebf3. A proveniência histórica atribui Chen, DESI e Moresco às fontes citadas; a presente tarefa não refez auditoria bibliográfica nem leu o PDF.

A docstring de fontes.py ainda fala em Pantheon diagonal/não ligado, mas o ramo efetivo Motor._prepara→PantheonCov e o resultado F5 guardam a matriz completa. O plano segue o caminho de execução explícito, registrando a legenda obsoleta como tal.

## Matemática que a reprodução deverá implementar

[DERIVED — álgebra do contrato histórico, não nova incidência física]

No modo artigo, β_fundo=0 e c=0. Com h=H0/100:
Ωm=(ωb+ωc+0.06/93.14)/h²;
Ωr=4.4814e−7·(2.7255)^4·[1+3.046·(7/8)·(4/11)^(4/3)]/h²;
ΩΛ=1−Ωm−Ωr;
E²(z)=Ωr(1+z)^4+Ωm(1+z)^3+ΩΛ.

O integrador histórico usa essa aproximação de radiação com N_eff inteiro e contribuição massiva em matéria. A razão sobre CAMB corrige os observáveis acústicos no ramo artigo, mas não autoriza substituir silenciosamente E(z) na lei por outra física. Reprodução e auditoria posterior desse aproximante são coisas distintas.

D_M=(c_luz/H0)∫0^z du/E(u); D_H=c_luz/[H0E(z)]; D_V=[z D_M² D_H]^(1/3). BAO divide pelo r_drag interpolado de CAMB. R=√Ωm H0 D_M*/c_luz e l_A=πD_M*/r_*.

Como os dois fundos são iguais no modo artigo, as razões TGL/ΛCDM de r_*, r_drag e D_M* são 1. Assim Planck usa D_M*, r_* e z_* da tabela CAMB sem precisar rodar CAMB novamente. O z_* **da lei** é outro papel: fixo em 1089.95 conforme os dois pré-registros; não trocar pela saída variável de CAMB nem pelo fiducial 1089 usado em outra unidade F0.

I_D1b(z)=(2/3)ln E(z); I_D1a(z)=ln(1+z).
K_*=exp[β I(z_*fixo)]; A(z)=exp{β[I(z_*fixo)−I(z)]}.
SH0ES_local prediz H0K_*.
CC acumulado prediz H0E(z)A(z); CC nenhuma prediz H0E(z).

SNe:
- nenhuma: DM histórico acima;
- sombra: DM/K_*;
- acumulada: (c_luz/H0)∫du/[E(u)A(u)], com A=1 acima de z_* no algoritmo histórico;
- Pantheon só cosmologia da F4 usa sempre DM sem lei_sn, conforme motor.py:215;
- calibradores F5 substituem μ cosmológico por CEPH_DIST antes do perfil de M.

Com r=m_b−μ, Mhat=(1ᵀC⁻¹r)/(1ᵀC⁻¹1) e χ²prof=rᵀC⁻¹r−(1ᵀC⁻¹r)²/(1ᵀC⁻¹1). Implementar por Cholesky/soluções lineares; evitar construir inversa explicitamente. A simetrização C←(C+Cᵀ)/2 do histórico deve ser preservada e registrada. M é perfilado, não amostrado com um prior finito. Os lnZ arquivados omitem constantes de normalização da gaussiana e usam exp(−χ²prof/2); são comparáveis por diferenças **dentro da mesma família/likelihood**, não evidências absolutas entre famílias de dimensões diferentes.

## Funções, snapshots e implementação independente

| Fonte (sob B) | Funções/trechos a espelhar conceitualmente | Código novo proposto |
|---|---|---|
| bancada/fontes.py:51–117,126–136,163–193 | extração AST de α/dados/LIMITES; Planck e DR1 corrigidos | loader local que verifica pins e não importa originais |
| bancada/camb_tabela.py:17–69 | TabelaCAMB, _pesos, __call__; Lagrange separável com seis nós (grau5) | interpolador NumPy independente sobre NPZ congelado |
| bancada/fundo_gpu.py:26–28,106–156 | Ωr, fundo, DM, DM_com_boost, Ez | E analítico e quadratura Gauss–Legendre convergente; ramo histórico separado caso necessário para localizar erro numérico |
| bancada/motor.py:147–238 | _obs_bao, _predizer_bloco, _r_planck, _r_dr1, _r_cc | previsões/likelihoods independentes, apenas modo artigo |
| bancada/pantheon_cov.py:49–102 | seleção, mu, M_hat, chi2_prof, residuos_brancos | Cholesky e perfil analítico novo |
| bancada/evidencia.py:91–137,156–173 | _ajuste, comparar | ajuste novo com restrições históricas e cálculo explícito de JᵀJ |
| ferramentas/evidencia_bayes.py:26–120 | _grade, evidencia, comparar_evidencias | quadratura histórica independente + relatório de estabilidade, sem reutilizar a função original |
| bancada/amostrador.py | stretch Goodman–Weare, a=2; τ por janela Sokal | opcional posterior independente, sem promessa de mesmos números de RNG |
| investigacao/fase4_desvio_30set/rodar_fase4.py:78–128 | bloco, ciclos de núcleos e posterior | relatório de reprodução F4, sem acesso de escrita ao livro |
| investigacao/fase5_sh0es_01out/rodar_fase5.py:76–100,137–192 | bloco, ciclos de leituras, zsplit e posterior | relatório de reprodução F5 |

Todos os hashes dos arquivos acima e os intervalos AST constam da auditoria. Foram localizados os backups motor.py.bak_20261001_123905_sh0es (estado anterior a SH0ES, pertinente à F4) e motor.py.bak_20261001_163715_cccov (anterior a CCcov, pertinente à F5), mais fontes/fundo/evidencia/Pantheon correspondentes. Os diffs de bytes/texto ficam na auditoria. Não há nos JSONs F4/F5 um manifesto completo do hash do motor executado: o nome/datamento de backup é evidência de linhagem, não prova de identidade de execução. A reprodução deverá privilegiar contratos + alvos + snapshots e declarar essa lacuna. Nunca executar backups.

O histórico integra em ln a: grade20001, Simpson cumulativo e interpolação cúbica, intervalo [−ln(1+1e8), ln(1e3)]. A proposta independente usa integrais diretas e comparação de convergência (ex.: GL64/128) para não transportar automaticamente o erro de implementação. Preservar a mesma função E, tabela CAMB e máscara de validade; diferenças de quadratura aparecem no orçamento numérico. Se for necessário reproduzir o último dígito do algoritmo antigo, oferecer ramo explicitamente “fidelidade numérica histórica”, separado do integrador independente.

## Parâmetros, priors e suporte efetivo

| Parâmetro | Limite/prior histórico | Tratamento |
|---|---|---|
| H0 | U[50,90] | livre em LCDM/TGL/livre |
| ωb=ombh2 | U[.015,.030] | livre |
| ωc=omch2 | U[.08,.18] | livre |
| β LCDM | δ(0) | fixo |
| β TGL | δ(α_CODATA2018√e) | fixo em runtime |
| β diagnóstico livre | U[−.05,.05] | somente reprodução do ramo arquivado |
| c | fixo0 nas famílias propostas | não abrir dimensão extra |
| M | perfil analítico | não inventar prior finito |

[REAL — leitura e aritmética da grade] A tabela declara H0=[58,78] com11 nós, ωb=[.020,.025] com21, ωc=[.100,.140] com21. TabelaCAMB só aceita posições de índice1 até n−2: **H0∈[60,76], ωb∈[.02025,.02475], ωc∈[.102,.138]**. Fora daí likelihood zero (χ² infinito), embora o volume de normalização da evidência seja o dos limites amplos acima. Preservar essa convenção ao reproduzir; renormalizar o prior para o interior alteraria o contrato. O teste histórico de proximidade de borda usa 0.5% da largura dos **limites do pipeline**, não das bordas internas da tabela; convém registrar ambos na auditoria futura sem mudar retroativamente sua regra.

Ajuste histórico: fiducial (67.5,.02237,.1200,0,0); escalas (1,.0005,.005,.005,.005); least_squares TRF, tolerâncias1e−12, máximo200 avaliações, diferenças centrais com passo1e−3 nas coordenadas escaladas, limites escalados multiplicados por.999. Covariância=(JᵀJ)⁻¹ nas unidades físicas, sem reescala por χ²/gl. A sequência comparar inicia TGL e livre do melhor ponto LCDM; a função de evidência chama seus ajustes sem esse x0. Registrar ambas as sequências para explicar qualquer mínimo divergente.

## Estatísticas e chaves-alvo

AUDITORIA_E_CONTRATOS.json::target_contracts contém cada família, leitura, caminho JSON exato e lista de chaves existentes. Não precisamos inventar alvos a partir da prosa.

1. Todas as famílias propostas: χ² LCDM/TGL/livre, decomposição por bloco, θhat, H0_local, K, Mhat quando aplicável, limites, σ_JtJ; δhat=βhat−β_TGL, zδ=δhat/σβ, zperfil=√max(χ²TGL−χ²livre,0).
2. F4: pull SH0ES=(H0_local−73.04)/1.04; ganho de lei sign(χ²LCDM−χ²TGL)√|Δχ²|; custo por nat βhat I(z*)/ln(1+z*). F5: a mesma raiz com sinal é z_tensao **do ajuste conjunto com escada dentro**, não uma previsão de H0 feita sem a escada.
3. Evidência F4: D1b em P/Q/R/S/T e D1a somente P. F5: sombra/acumulada D1b em P/Q/S; nenhuma e sombra_d1a sem evidência. Comparar lnZ e lnB TGL/LCDM, livre/LCDM, TGL/livre e Savage–Dickey; F5 diferença sombra/acumulada dentro de P ou S.
4. Quadratura histórica: grade cartesiana centrada em θhat±6σJtJ, recortada ao prior; β livre cobre o intervalo completo; n=25 e35. **Soma retangular com pesos constantes Δθ**, não trapézio: logsumexp(−χ²/2)+ΣlogΔθ−logVprior. O resultado publicado guarda n25 e |n35−n25|. Nós fora do suporte são descartados. Laplace arquivado usa apenas as variâncias diagonais, não det da covariância completa. SD usa interpolação linear da marginal da grade n25. Essas escolhas têm de ser identificadas antes de qualquer comparação.
5. Posteriores: F4 P/T D1b; F5 P/S sombra; 256walkers,3000passos,burn600,seed42, stretch a2; mediana,16/84%, frações β≥β_TGL e β>0, τ e Nefetivo. Igual seed em bibliotecas diferentes não implica cadeia idêntica; a comparação será por erro MonteCarlo, não bytes. Posterior é etapa opcional separada da reprodução determinística.
6. zsplit: θ_fundo LCDM de Planck+DR2. Matriz A com coluna1 e seis colunas −1 para não calibradores nos bins (.01,.05],(.05,.15],(.15,.30],(.30,.60],(.60,1],(1,2.3]; y=m_b−μnenhuma. Est=(AᵀC⁻¹A)⁻¹AᵀC⁻¹y; cov_s mesma inversa; testar deslocamentos antigos zero,5log10K, e média **aritmética** por bin da diferença μnenhuma−μacumulada. Estimar s comum, σ, χ²constância/gl5 e χ²hipóteses/gl6. Trata-se de GLS condicional a θ_fundo: a incerteza de θ_fundo não é propagada no runner. Não chamar isso marginalização conjunta completa.
7. Leitura nenhuma F5: como β não entra no fundo nem em SN/CC, seu Jacobiano é nulo para esses conjuntos. βlivre ali não está identificado; preservar nulls/falhas de σ em vez de fabricar uma estimativa.
8. Multiplicidade: não escrever no livro SQLite vivo. Reutilizar contagens históricas em significancia_livro se for preciso conferir a aritmética Šidák. Uma reprodução não cria nova família científica e não deve aumentar a penalização histórica. Os gl do runner geral subtraem apenas os parâmetros explícitos e não o M perfilado; documentar a convenção arquivada sem corrigi-la silenciosamente. Não emitir as strings de veredito como novo resultado.

## Obstáculos, alternativas e MEDIDA futura

| Obstáculo | Alternativa A | Alternativa B | MEDIDA antes de concluir |
|---|---|---|---|
| Motor mudou depois da rodada e não foi pinado integralmente nos resultados | Reconstituir equações dos snapshots e contratos | Usar equações atuais só onde diff demonstra equivalência do ramo | Comparar χ² por bloco em θ arquivado antes de otimizar; registrar diferenças e fonte, sem presumir identidade |
| CAMB e prior com suportes diferentes | Usar NPZ congelado com interpolação independente de grau5 e máscara histórica | Regerar CAMB com versão/configuração exatas, em etapa separada posteriormente autorizada | Hash da tabela e resíduos nos400 pontos de teste do NPZ; jamais baixar tabela nova para “fazer bater” |
| Quadratura/integração podem deslocar último dígito | Integrador direto convergente | Ramo independente de fidelidade aos nós históricos | Orçamento de erro por bloco antes de fits; critérios numéricos devem ser fixados por hash antes da execução |
| CC antiga diagonal versus covariância posterior F7 | Reproduzir diagonal exatamente, com limitação explícita | Abrir posteriormente unidade de robustez F7 com contrato próprio | Não trocar dados/covariância durante F4/5; diferenças de ciência ficam fora desta reprodução |
| Família com SH0ES não é fundo sem escada | Usar T F4 ou θ_fundo zsplit como alvos sem escada existentes | Relatar P/Q/S como ajuste conjunto, sem convertê-los em predição externa | Conferir conjuntos de entrada no recibo por família; proibir soma de F4/F5 ou DR1/DR2 |
| Relatório narrativo F4 mudou | Ancorar números nos JSONs cujo hash confere | Examinar adendo/backup para história textual se necessário | Divergência de relatório fica registrada; não transfere defeito aos JSONs sem evidência |

Sequência proposta, ainda não executada: congelar protocolo de reprodução com tolerâncias numéricas; verificar somente identidade/seleções/dimensões; validar interpolação nos pontos de teste congelados e likelihood em θ arquivado; reproduzir primeiro P F4 e P F5 determinísticos; expandir para Q/R/S/T e leituras já arquivadas conforme o mesmo contrato; só então evidência25/35 e eventual posterior. Um resultado que não bate é discrepância localizada, nunca motivo para ajustar a teoria ao alvo. Novos dados, novo prior, nova física de fundo ou uma estatística de discriminação inédita exigem outro contrato.

[REAL] Nesta entrega houve apenas inventário de41 arquivos, leitura AST e montagem determinística das covariâncias históricas. O leitor AST falhou inicialmente por uma expressão aritmética dentro de uma lista; corrigiu-se apenas o leitor novo com backup imediato, antes de qualquer JSON de saída existir. A repetição foi do inventário local, sem chamadas remotas ou cálculo científico repetido. Nenhuma conclusão sobre natureza ou gate decorre deste plano.
