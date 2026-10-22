# Revisão independente da integração motor–montagem F9

[REAL — revisão estática] Preparação f07e4aba-e976-4d78-be1c-449968d4a305; execução apenas proposta ffd6ccba-cd70-4747-aceb-a10003dfb7f4. **Nenhum bloqueador concreto identificado na matemática/configuração e na ligação prediction_worker → packet → assemble_five.** A conclusão permite a decisão de ROOT sobre a chamada teórica única; não é autorização nem resultado de execução.

Escopo: configuração, worker, cópias do motor/montador, admissão e fontes estruturais pinadas. Supervisor, limpeza e qualificação operacional/native ficam na revisão de proveniência. Leitura/AST/metadados apenas; não importei candidatos, CAMB, NumPy ou Fraction, não iniciei WSL, não executei controle e não abri centros observados. Mapa antes552. O recibo compara o manifesto de fonte no início e no encerramento; o aceite vale somente para esse snapshot.

## Configuração efetiva e ponto novo

EFFECTIVE_CONFIGURATION conserva o fundo plano padrão, neutrinos térmicos, RECFAST/BBN, prior e referência térmica do protocolo de origem. As diferenças são explicitamente nova identidade, um ponto, um perfil, orçamento e grade. O pacote mantém PROTOCOL_ORIGIN byte a byte e identifica separadamente o hash da configuração efetiva; não apresenta a grade nova como se fosse o piloto histórico.

A grade é **0;0,295;0,510;0,706;0,934;1,321;1,484;2,33**. Zero ocupa o índice0 exigido por background_controls.py182–184 para H(0)/H0 e distâncias nulas; os sete outros pontos são os metadados exatos do layout3+13, sem vizinho/interpolação nova. Os13 componentes BAO mantêm a ordem original, inclusive DH antes de DM em2,33. Não se confundem os oito pontos de avaliação do fundo com as13 componentes.

A seleção é documentada em prepare_integration.py59–65: quantis independentes (1/3,1/2,2/3) nos priors H0[50,90],ombh2[0,015;0,030],omch2[0,08;0,18]. Isso dá o ponto representado em binário no JSON (H0=190/3,ombh2=0,0225,omch2=11/75), sem consulta a estimativa observada. A lista difere dos cinco thetas do protocolo antigo; combinar um novo ponto com reference não repete os dez slots antigos. O código de preparação e o diff documental foram lidos, não executados.

O perfil único é reference: AccuracyBoost2 e tolerância da integral de distância1e−7. Não ocorre comparação baseline/reference nesta unidade. O limiar relativo1e−5 herdado permanece metadado do protocolo; não pode ser relatado como controle de convergência novo. Os controles internos de finitude, positividade, H(0), distâncias nulas e monotonicidade pertencem à chamada existente.

## Uso real do motor e vínculo da admissão

worker.py148–184 importa o CAMB no futuro processo, carrega a cópia intacta do motor, cerca camb.get_background com contador exclusivo e chama **engine.prediction_worker(effective, id, 'reference')** uma vez. Não chama validate, run_controls, main ou execute_worker_once do piloto antigo. O caminho prediction_worker130–186 contém a avaliação CAMB, distâncias e quantidades térmicas reais; não é uma resposta fabricada ou uma substituição por constantes.

Os contadores tentada/retornada precisam ambos ser1 antes de emitir o fundo utilizável. Uma exceção mantém falha; não há nova chamada ou troca por vetor zero. A unidade nova tem suas próprias identidades e claims externos previstos; os slots antigos não são reabertos. O circuito operacional completo é responsabilidade da revisão separada, sem inferir aqui execução.

ASSEMBLY_ADMISSION é pinada em CONTRATO_WSL; contém os mesmos SOURCE_PINS do montador, hash do layout, configuração efetiva e inventário de runtime. O worker confere local_pins antes de lê-la e passa seus bytes e hash ao montador. Assim, nesta integração, o hash da admissão não é obtido do próprio packet não confiável: é vinculado ao contrato exterior.

O worker emite BACKGROUND_RESULT, depois ENGINE_EXECUTION_RECEIPT ligado ao SHA dos bytes do resultado, request/nonce/processo/configuração/runtime e contadores. O packet liga esses hashes, theta, z_lei e unidades. assemble_five compara fontes/configuração/runtime/theta/resultado, exige sucesso de engenharia e conserva a proveniência no retorno. Não depende só de um rótulo de sucesso. Fonte: worker.py164–185; five_model_assembly.py180–232.

## Matemática e identidades H1–H5

O motor calcula E_lei com H_CAMB(z_lei)/H0, I=(2/3)lnE_lei, R com Omega_m0 e D_M(zstar), e lA=pi D_M(zstar)/rstar. Usa os mesmos parâmetros para H e distâncias, DH=c/H e DV=(z DM² DH)^(1/3). zstar e zdrag são saídas térmicas; **z_lei1089,95 é INPUT fixo separado**. As distâncias BAO usam rdrag, não rstar.

As cinco hipóteses compartilham theta apenas nesta avaliação, permitindo uma chamada comum de fundo; não impõem melhores ajustes iguais em análise futura. H1 calcula beta em runtime a partir do alpha com proveniência no layout, multiplicado por sqrt(e). H3 recebe beta=0,025; H4 recebe s=0,075; H5 recebe rd=137,5Mpc, todos nos priors existentes e preparados como frações explícitas, sem ajuste nesta unidade.

| Modelo | resposta local h | deslocamento Cefeida | BAO |
|---|---|---|---|
| H1_TGL | log10H0+I beta_TGL/ln10 | zero | rdrag CAMB |
| H2_LCDM | log10H0 | zero | rdrag CAMB |
| H3_beta_free | log10H0+I beta/ln10 | zero | rdrag CAMB |
| H4_Cepheid | log10H0 | −5log10(1+s), aplicado por c_C | rdrag CAMB |
| H5_rd_free | log10H0 | zero | rd livre |

H5 mantém R/lA/rstar CMB do fundo padrão e não recebe resposta TGL local. A tabela H5_BAO_only produzida pelo motor em130/145/160 é metadado teórico herdado; a montagem usa seu próprio rd137,5 em distâncias do mesmo fundo, sem solver adicional. H4 altera somente o vetor c_C da especificação; não soma um deslocamento às267 linhas indistintamente.

O montador conserva a densidade comum50/3 e densidades extras1,1,10,10/3,1/30 nas coordenadas originais. Portanto o prior de H4 continua uniforme ems e o de H5 emrd; não é implicitamente trocado por prior uniforme emdelta_C ouq. Esta unidade não integra esses priors.

## Forma, unidades e métricas

O retorno separa cinco médias de283linhas de uma matriz nuisance comum com63colunas:16linhas de fundo seguidas pelas267locais. O desenho original tem178host,13group,55SN_calibrator,14SBF_calibrator,1SN_HF,1SBF_HF e5megamaser. As sete linhas dex recebem fator5 em X,a_h,c_C e média; as demais preservam magnitudes. O consumidor futuro deve aplicar Ty e TCTᵀ aos observados/covariância; nenhum deles entra nesta unidade e nenhum rank é recalculado.

BACKGROUND_RESULT registra parâmetros completos CAMB, tempo do bloco de previsão e pico RSS do processo Linux. O tempo próprio do motor começa depois de runtime_check e antes da construção CAMBparams; não é tempo exclusivo de solver nativo nem latência total do supervisor. ENGINE_EXECUTION_RECEIPT/CASE_RESULT acrescentam o tempo desde a entrada do trabalho do filho, contadores e hashes. Pico RSS é métrica observada futura, não limite de memória. Não há medida de CPU separada prevista e não a atribuo ao pacote.

ENGINEERING_ONLY, certified=false, uniform_error_bound=null e numerical_certificate=null permanecem explícitos; chi²,p,sigma,lnB ficamnull. Ausência de cota uniforme não impede esta avaliação de engenharia. Não se exige uma certificação global de CAMB para a chamada proposta; tampouco o futuro sucesso pontual proveria essa certificação.

## Conclusão delimitada

O caminho escolhido reutiliza avaliação existente + montador puro, preservando os hashes das fontes. A alternativa de colocar novo solver dentro do montador não é necessária e duplicaria uma responsabilidade já resolvida. Não há achado nesta revisão que justifique campanha adicional de controles.

[OPEN] Recebimento efetivo das bibliotecas, retorno numérico, transporte/cleanup e custo pertencem à única execução futura condicionada à decisão de ROOT e à revisão operacional. [REAL] Esta revisão cria somente seus próprios arquivos; pacote do autor, autorizações, claims, memórias e ledger permanecem intactos.
