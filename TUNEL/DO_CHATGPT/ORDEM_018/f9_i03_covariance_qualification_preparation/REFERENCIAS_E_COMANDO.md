# I03 — montagem da covariância e passagem ao consumidor

Pedido b89a3fc5-244f-4c72-8f59-7b2ecc74c62b. Unidade27c6d5e9-df9f-4566-bd5d-4857683936d8, I03_COVARIANCE_CONSUMER_JOIN. [REAL documental] Identidade persistida antes do código; início no mapa648. Preparação local apenas, sem importar/executar candidato, NumPy ou bibliotecas nativas; sem solver, WSL, observados, provedor, AUTH/CLAIM/ROOT_DECISION. Memórias globais e decisão ficam com ROOT.

## Lacuna real e alternativas

I03 f200dee1 teve aceite estático609/611. Sua implementação ainda não foi consumida numericamente. A unidade755c qualificou consumer/prior com covariâncias feitas diretamente pelo harness; não chamou JointCovarianceBuilder e não construiu o bloco estelar com seus72vínculos. Esse é o recorte novo. Não repetimos755c, os controles estelares históricos ou campanhas de600cenários.

**Alternativa A, escolhida:** dois rótulos representativos e quatro recusas. O builder original monta nove blocos,36cruzes explícitas e o estelar pela primitiva já existente. Uma referência independente calcula cada entrada por pares de identificadores e frações exatas. Só depois se liga C nativa ao consumidor e backend já qualificados. Não há novo solver gaussiano de produção.

**Alternativa B:** campanha completa dos600rótulos, ambos tratamentos SBF, controle de família e integração física. Tem escopo/custo maiores, mistura escolhas O01/O02 e não é necessária para verificar a montagem que falta agora. Fica fora. Uma matriz final já pronta, diretamente injetada no consumidor, repetiria a junção anterior e não exercitaria I03; foi descartada como resposta à presente solicitação.

## Reuso, ambiente e fontes

As fontes de joint_covariance.py, METADATA_ESTRUTURA_FAMILIA.json, consumidor, backend e support são pinadas por bytes. A função **block_correlation** é extraída por AST da definição original em qualify_stellar_family.py: mesmo corpo e localizadores de linha, com np explicitamente vinculado ao runtime. Não se importa o antigo módulo/harness, não se roda seu main, não se altera sys.path por ele nem se importa audit_inputs. O recibo identifica essa projeção AST; não a apresenta como execução integral daquele arquivo.

De755c reutilizam-se somente structure_from_documents, make_packet e seus auxiliares de serialização, com fonte pinada. Seu run e seus cinco casos não são chamados. O fundo e as médias continuam fixtures declarados: não são saídas novas do assembler/CAMB. Acrescenta-se uma origem afim sintética igual a todos os modelos. β_TGL continua calculado por α do layout vezes√e. Nenhum domínio de prior é alterado; priors e integral theta não são executados nesta unidade.

O runtime é o Windows do bundle Codex já usado em755c: Python com ABI3.12, NumPy2.3.5. Rechecagem atual dos bytes dos arquivos do inventário anterior, sem nova carga de biblioteca. O inventário registra também o recibo da execução finita anterior; aquele sucesso não antecipa o resultado do novo candidato. Demais fontes herdadas, incluindo orçamentos de erro, são apenas conferidas por hash — seus valores não são lidos/parseados como insumo científico. DLLs do Windows e estado global do loader não têm fechamento completo certificado. Não há install, repin de provedor ou fallback WSL.

## Dois rótulos e construção independente

Rótulos já presentes na metadata:

- STELLAR_0_000__SBF_UPSTREAM_M_ONLY: all_same e u=v=p=q=0.
- STELLAR_1_055__SBF_UPSTREAM_M_ONLY: cepheid_opposite e u=v=p=q=1/4.

Os mesmos sigma sintéticos são usados em ambos: âncora1/4, MAS1/2, HMS1 (mag). D0=0 é INPUT explícito do fixture. Há14chaves MAS,104HMS e4âncoras na fonte, preservadas mesmo quando alguma incidência é inativa. Não se utilizam os erros observacionais das fontes históricas.

Para linhas i,j, a referência calcula diretamente

    Cstar_ij = (1/16)·[anchor_i=anchor_j]
              + (1/4)·Rm(MAS_i,MAS_j) + Rh(HMS_i,HMS_j).

Cada Rm/Rh é definido pelos deltas de identidade e pelos produtos de sinais de pares na mesma partição, com pesos racionais fixos. **Não chama block_correlation, nem constrói A/B/H para multiplicá-los como o candidato.** A referência usa a fórmula escalar por pares; o candidato usa incidências, matrizes de correlação e produtos NumPy. Compartilham a especificação, não o algoritmo de montagem. Os valores são frações diádicas; o critério congelado é igualdade exata f64 das283×283entradas, não tolerância relaxada após observar resultado.

Blocos nativos fora do estelar são diagonais explícitos: PLANCK diag(2,1,1), DESI/GROUP/SN_CAL/SBF_CAL identidades; SN_HF1/16dex²; SBF_HF1/8dex²; cinco MM com variâncias(i+1)/64dex². MM usa a receita condicional diagonal admitida pela interface e referências D=10,v=700,U=700 exclusivamente sintéticas. Não se recalcula ou ratifica a lei dos erros MM.

Todas as36cruzes são fornecidas com IDs, coordenadas, hashes e política de zero. Duas são não nulas e fixas entre os rótulos:

    C[PLANCK_0,STELLAR_j] = S0[0,j]/8,
    C[PLANCK_0,SN_HF] = 1/64,

com S0 a referência estelar baseline. As transpostas devem aparecer na parte inferior. Os34outros pares são zeros explícitos. Nenhum termo cruzado com MM é autorizado pela receita candidata.

## PSD e suporte — prova do fixture, não da covariância da natureza

[DERIVED, sob a especificação acima] Nas duas escolhas, os blocos primitivos têm parte identidade positiva; no rótulo interior Rm,Rh≥I/2. Portanto S≥S0/2, com mesmo núcleo. A cruz v=S0e0/8 está no suporte e satisfaz

    vᵀS⁺v ≤ 2·S0[0,0]/64,   S0[0,0]=21/16.

A cruz com SN_HF consome (1/64)²/(1/16)=1/256 do complemento de Schur. A soma é menor que a variância2 de PLANCK_0; portanto os demais105graus permanecem positivos e o suporte total tem dimensão105+rank(S0).

O harness verifica o posto do grafo por eliminação racional esparsa nas colunas da incidência. Exige106, conforme a identidade estrutural documentada, e verifica exatamente que X_estelar,a_h,c_C pertencem a esse espaço. Assim o posto esperado conjunto é211 e as72restrições estelares são preservadas. **A eliminação não foi executada na preparação**; divergência é falha, não licença para adaptar o posto de admissão ao resultado do NumPy. O backend existente confrontará essa expectativa na execução eventual.

A origem o tem componentes não nulas na primeira linha estelar e no intercepto SN_HF, e é somada às médias dos cinco modelos. y=μ_H2+Xη+(1/4)e_PLANCK_1, com η racional fixa. PLANCK_1 é independente e tem variância1. Portanto, após eliminar η,

    logL_H2 − log_prefactor = −1/32.

Esse pequeno contraste quadrático é uma referência analítica própria. **O log_prefactor continua vindo do backend qualificado anteriormente:** não se alega novo oráculo independente de normalização absoluta nesta unidade. Outros quatro modelos precisam devolver valores finitos no suporte comum. Não se calculam evidência global, lnB ou sigma.

## Passagem ao consumidor e identidade da admissão

A saída C_native do builder, com seus próprios bytes e IDs, entra diretamente em prepare_joint. O harness confere hashes do registro e de C; equality dos bindings, resposta/estrutura e medida comum; copia para a admissão o hash exato de C retornado. y/origem são convertidos para coordenadas nativas por T⁻¹; X e médias já estão no sistema final. O consumidor é o único a aplicar Ty,TCTᵀ,Torigem, inclusive nas cruzes mag×dex/dimensionless×dex.

São conferidos o hash da C transformada, y/origem recuperados, posto211, nuisance63 e identidade da admissão efetivamente armazenada. I03 não lê ou autentica por si só os documentos referenciados e não recebe a admissão do consumidor: o harness faz a ligação explícita para este teste. **Isso não prova que o controlador de produção já valida todos esses vínculos automaticamente.** Controller39f88 e reparoI02_99e2 têm revisão própria, não duplicada aqui.

## Seis casos

| Caso | Objeto efetivamente exercitado | Aceite |
|---|---|---|
| V01 | Montagem baseline e passagem ao consumidor | Todas as entradas iguais à referência; C sem escrita, hashes corretos, rank211, transformação única, cinco modelos finitos e contraste H2=−1/32 |
| V02 | Montagem1/4 com sinal Cefeida oposto | Mesmo contrato, referência diferente; mesmas entradas comuns/medida/resposta |
| V03 | Omissão de uma das36cruzes | SCHEMA_ERROR antes da montagem estelar |
| V04 | Cruz PLANCK–MM não nula | OPEN_MODEL_COMPONENT; não aproximar a zero |
| V05 | Hash da C na admissão difere dos bytes retornados | PIN_ERROR antes de criar backend |
| V06 | Cruz PLANCK_1–DESI_0=2 com ambas diagonais1 | Builder mantém a matriz; consumidor recusa BACKEND_PREPARATION_FAILED com causa Indefinite covariance |

V06 contém o bloco[[1,2],[2,1]], cuja direção(1,−1) tem forma quadrática negativa. Ele verifica que blocos válidos não bastam para PSD conjunta e que a validação permanece no backend, conforme a divisão original de responsabilidades. Erro não vira probabilidade zero ou modelo descartado.

## Orçamento, comando e consumo

Um construtor I03; cinco build_case;16chamadas à primitiva; quatro tentativas prepare_joint; três construtores backend; duas evaluate_five. Dois oráculos estelares de178²pares,63368pares ao todo. A eliminação racional tem vértices/linhas fixos e limite8192bits conferido. Nenhum serviço de prior, integração theta ou cenário adicional. Dimensões fixas283×283 e283×63; não se guardam600matrizes.

Tolerância do contraste H2:2e−7 absoluta, congelada. Igualdade de matrizes é exata para os fixtures diádicos; transformação de y usa1e−12, origem igualdade exata. São controles finitos de engenharia, não certificado uniforme/intervalar.

Um filho Windows oculto, shell=false, sem processo científico subordinado. Prazo nominal120s; validação pré-claim≤15s; prazo cooperativo80s; espera90s; recolhimento5s. Streams até128KiB como critério de aceite. Variáveis de ambiente pedem uma thread BLAS/OMP, sem alegar controle de JobObject. Não há hardcapRAM/disco ou garantia de tempo real.

O driver é derivado do supervisor755c por substituições textuais conferidas e troca apenas de worker; o driver anterior não roda. Exige decisão ROOT futura com hash real do manifesto, revisão independente e scope SIX_SYNTHETIC_COVARIANCE_JOIN_CASES_ONLY. Há claim exclusivo antes do filho e marca exclusiva do worker. Claim/output parcial ou existente impede repetição; não há retry/fallback. PASS interno é provisório até terminal, ausência de falha e exit0 externo.

Comando futuro, **não executado**:

```powershell
& 'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -I -S -B -X utf8 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_i03_covariance_qualification_preparation\driver.py' --decision-sha256 '<SHA_REAL_DA_FUTURA_ROOT_DECISION.json>'
```

Não cobre600cenários, receita SBF alternativa, covariance real, MM/O01/O02, controlador/guard/FS/P3, assembler/solver, priors/theta, Q01 inteiro, Q02/Q03 ou V1 físico. Mantidas as aberturas§6, D8/D5b/E3, d3/C6 e demais suspensões. Sem nova chamada remota diante da divergência de geração; não repinar/reabrir a unidade Claude. A errata P4/P5 permanece aplicável; nenhuma estatística histórica é somada ou misturada neste pacote.
