[REAL/DERIVED/INPUT/OPEN] Revisão independente do código do principal para E2/E3, por outro autor que não implementou esses módulos. **REVISÃO COM CORREÇÕES NECESSÁRIAS ANTES DO FREEZE/USO. Não encerra a ORDEM013BIS.** Axiomas N/A — sem Lean.

Escopo: null_runner.py, synthetic_null.py, route_iv_null.py, fetch_registered.py, injection_design.py, remnant_conversion.py e E2_DESIGN_DRAFT_001.json. Para conferir as chamadas, também foram lidos registration_guard.py, strain_io.py, trechos pertinentes de pe_runner.py, o builder do draft e a álgebra E0 importada. Os arquivos do principal não foram alterados. Código/pins E7 permanecem congelados.

Evidência reprodutível: `review_main_fixtures.py` e `MAIN_CODE_REVIEW_FIXTURES.json`, nesta pasta. O SHA256 medido do JSON de evidência é `50f7b878387b52a6d58cecbdfef893f5fdb48083887f9ba2d38b303c39adf6bbf`. O JSON contém os pins completos de todas as fontes. Nenhuma mudou durante as fixtures. Arquivos em edição podem mudar depois: este parecer vale para esses bytes, não é aprovação automática de revisões futuras.

## Achados acionáveis

### P1 — A janela da injeção ainda pode conter o evento astrofísico usado como referência

`bis/e2_code/injection_design.py:23`, especialmente a conferência de identidade de arquivo na linha 40 e a criação do gerador na linha 42. O código exige `noise_kind=REAL_OFFSOURCE`, igualdade entre os paths/hashes rotulados onsource/offsource e que a injeção caiba no segmento. Não verifica que **o segmento de análise** exclui a região em torno de `event_GPS`. A PSD está separada do segmento; isso não torna o segmento automaticamente livre do sinal real.

> [nota operacional do operador — omitida no retrato público]

Correção solicitada ao proprietário: antes do gerador, exigir disjunção entre a janela inteira de análise e o intervalo protegido do evento real, com margem registrada; vincular esse GPS real a metadado pinado, distinguindo-o do GPS sintético da injeção. Manter também a disjunção PSD/análise já existente. Fixtures de borda devem conferir a convenção de intervalos e a janela, não apenas o instante da injeção.

### P2 — Download truncado sem checksum pode receber recibo de sucesso

`bis/e2_code/fetch_registered.py:30–50`. Há teto de bytes, recusa de vazio e verificação de checksum quando fornecido, mas não há igualdade contra tamanho esperado/Content-Length. O loop com read(tamanho) pode chegar a EOF antes do comprimento anunciado sem esse teste explícito. O SHA calculado localmente identifica os bytes recebidos; sozinho não prova completude.

[REAL — HTTP simulado, nenhuma rede] Resposta com `Content-Length: 10`, apenas `b'abc'`, checksum ausente: promoveu 3 bytes ao target e gravou `PUBLIC_BYTES_DOWNLOADED_NOT_SAMPLES_READ`, `provider_checksum_verified=false`. O campo false é honesto, mas não impede que uma transferência incompleta seja tratada como produto disponível.

Correção: registrar tamanho exato e checksum primário quando disponíveis; exigir igualdade ao tamanho declarado antes de promover .partial. Se tamanho/checksum de origem forem desconhecidos, conservar estado explicitamente não validado para consumo científico; não inventar hash esperado. Registrar verificação do tamanho separadamente do SHA local. Preservar a tentativa recusada. Host HTTPS e validação de redirects existentes devem permanecer.

### P2 — Recibo de download dinâmico não fixa a alocação E3.2 que autorizou a receita

`fetch_registered.py:51` e `registration_guard.py:150`. A guarda lê e verifica a alocação testemunhada, o SHA da configuração de jobs e os recibos de licença; acrescenta `_allocation_sha256` à visão derivada. Porém o fetch recebe `reg` original e apenas o mapa recipes; seu recibo grava parent E2 + nome da receita, sem SHA da alocação, configuração ou conteúdo da própria receita. Reutilizar o nome de uma receita em outra versão testemunhada torna o recibo isolado insuficiente para identificar qual autorização estava ativa.

Correção: transportar ao fetch os digests da alocação/configuração e um digest canônico da receita efetivamente usada; incorporá-los ao recibo e revalidar essa cadeia antes da promoção final. Isto é uma lacuna de custódia, não evidência de que houve download indevido. Nenhum download real foi feito nesta revisão.

### P1 para freeze — O draft 001 ainda não satisfaz o contrato do código corrente

Pendências já sinalizadas pelo principal, aqui verificadas sem confundi-las com regressões novas:

- `pe_jobs.GW250114_PILOT` não contém `fixed_deformation_parameters`; `pe_runner.validate_config` retorna `KeyError` na fixture. Também faltam `privacy_mode` e `remnant_conversion_INPUT`. Piloto com as quatro deformações livres deve ter o mapa fixo explicitamente vazio; não completar por default silencioso.
- O draft 001 mantém duração 4 s/start 1420878139. O **builder lido já contém 8 s/start 1420878135**, conforme a correção comunicada pelo principal. Não se pede voltar a mudar o builder: regenerar versão nova de draft e conferir contra o contrato final. O builder lido ainda não incluía os três campos acima.
- O draft possui `extra_code_trees`, enquanto a guarda percorre `extra_code_roots`; este deve conter os produtores extras finalizados, incluindo E7. `own_code_tree_sha256={}` também é placeholder de draft, não cobertura paga.
- A guarda procura `allocation_policy`, ausente no draft. A frase `future_allocation` não fornece path/cap/schema para o carregador E3.2; sem essa ponte ele só vê jobs/downloads iniciais. Isto falha fechado, mas não executa a ampliação prometida.
- Status do draft e seed de cegamento continuam preparatórios. Não trocar o status para REGISTERED sem produzir a testemunha e preencher os pins/compromissos exigidos.

### P1 para admissão cega — Incorporar o censo novo por identidade e pin, sem converter ausência local em certeza universal

O `PUBLICATION_CENSUS.json` medido tem SHA256 `505eb16a608070ab53c50869c89d89000727f49ac156f18b07b75f9bc399a3dd`; confere com FREEZE_RECEIPT. Contagens: **23 examinados; 9 com publicação encontrada; 14 não localizados no escopo; destes 14, quatro com pendência de qualidade e dez sem esse alerta específico**. Não é certificação universal de cegueira.

O draft contém 53 candidatos e ainda não pina PUBLICATION_CENSUS.json. Os nove conhecidos continuam no mapa: GW230601_224134, GW230811_032116, GW230922_020344, GW230922_040658, GW230924_124453, GW230927_043729, GW231108_125142, GW231123_135430 e GW231206_233134. Seus campos de publicação no draft ainda estão pendentes, portanto a guarda atual **não os admite**: não houve vazamento demonstrado, mas a incorporação é obrigatória antes do freeze.

O principal deve unir o censo ao mapa por event ID, marcar os nove como não cegos/excluídos do teste, preservar o escopo e proveniência dos 14 e manter os quatro quality holds. Os outros 30 nomes do draft não foram certificados por esse censo de 23 e continuam pendentes; não reduzir silenciosamente o conjunto nem preencher todos como não publicados. Preservar o pin do censo e os pins de fontes/recibo pertinentes. Nenhuma leitura C1 foi selecionada por este revisor.

## Nulos científicos — verificação favorável com escopo limitado

[REAL] **25 células = 16 matched_projection + 9 rota IV; 25 seeds distintas.** Total programado: 1.609.000.000 draws, **zero executados aqui**. As 16 células são duas populações × quatro leituras com N_alvo finito em E0 × dois modelos sintéticos. Isso não apaga as outras seis leituras da matriz: são nulas/abertas/sub-resolução sem aquele alvo operacional, e não vencedoras/perdedoras selecionadas por dados novos.

`null_runner.projection_inputs` usa as larguras std(ddof=1) e previsões pontuais E0 pinadas. Não lê HDF5. Composição `arange(N)%K`: ciclos determinísticos da ordem original, diferença máxima de uma ocorrência por classe, sem seleção pela largura. Conferi nos oito cenários gaussianos que N = ceil(N90_mixture_illustration_not_selection) de E0. O programa escreve corretamente que esse N não garante 90% de poder após nuisance. As previsões pontuais E0 não se tornam integração de posterior completo: isso permanece limitação explícita desses controles sintéticos.

`synthetic_null.projected_components`: C=diag(sigma²)+X V Xᵀ, X=[1,sigma], média E1 subtraída no modelo declarado, V local E1 somente INPUT. Woodbury concordou com solução densa determinística 4×4 a **2,220446049250313e-16**. Frações de variância de ruído e nuisance somam um; PSD/simetria/valores finitos têm guardas. Isso é integração gaussiana sob V finita, **não projeção de intercepto com prior impróprio livre**, nem calibração física.

O nulo não gaussiano implementa escala t5 comum ao catálogo no termo de medida, padronizada por sqrt(3/chi²5), mais nuisance gaussiano independente. A soma não é renomeada t5. O controle analítico condiciona corretamente na escala e integra a cauda normal. Não foram executados draws ou quadratura de cauda nesta revisão.

Para tornar mensurável o aviso sobre poder, calculei somente a expressão analítica condicional Φ(sqrt(I)-5) em amplitude 1, com V INPUT. Não é z físico nem resultado de campanha:

| População | Leitura | N fixado | I com nuisance INPUT | Poder gaussiano condicional |
|---|---|---:|---:|---:|
| GWTC5_31 | R-B | 3328 | 0,7373675 | 0,0000172672 |
| GWTC5_31 | R-MOD | 1056 | 2,3751502 | 0,000271246 |
| GWTC5_31 | R-RAIZ-0 | 976 | 1,7521351 | 0,000118312 |
| GWTC5_31 | R-LIN | 263 | 5,5571581 | 0,00411315 |
| GWTC5_33 | R-B | 3447 | 0,7362036 | 0,0000172163 |
| GWTC5_33 | R-MOD | 1082 | 2,3807242 | 0,000273071 |
| GWTC5_33 | R-RAIZ-0 | 1009 | 1,7472530 | 0,000117460 |
| GWTC5_33 | R-LIN | 272 | 5,5402449 | 0,00406975 |

Logo não rotular nenhum desses alvos como N90 calibrado com nuisance. A redação de `not_claimed` e `target_source` já faz a distinção corretamente.

Rota IV: larguras reais congeladas de E0, sigma_sys INPUT=0 conforme desenho; nulo gaussiano heterogêneo, média comum perfilada e variância extra não negativa. A composição aqui é **multinomial por catálogo**, como a álgebra E0 pinada, e não o catálogo balanceado fixo do matched filter. Esta distinção deve sobreviver no relatório. Chunks usam seed+índice; as nove seeds espaçadas de 1000 e os 100 chunks por célula do draft não se sobrepõem. Contagem estritamente LRT>25, guardas de finitude antes de contar, limite de tempo entre chunks. Sem execução da otimização/LRT nesta revisão; sua validação anterior continua uma dependência pinada, não uma prova nova deste revisor.

Intervalos binomiais: cálculo determinístico para cenário hipotético 0/1.000.000 produz UL95 unilateral **2,9957277863525433e-6**, acima da cauda unilateral de 5σ. Não significa que houve zero excedências medidos. O código reporta corretamente intervalo empírico e não certifica 5σ com esse orçamento IV.

## Injeções e PSD — o que está correto

`strain_io.offsource_psd` fixa o fim do bloco PSD em no máximo min(event_GPS−exclusion, segment_start_GPS); portanto o bloco não se sobrepõe ao segmento de análise. A seleção é primeiro bloco válido por flags/finitude, não mínimo de PSD. A separação temporal é compatível com usar o mesmo arquivo longo de ruído em duas janelas distintas. Permanece o achado P1 sobre a janela de análise versus o evento real.

[REAL — fixture de recusa antes do gerador] IMRPhenomXPHM com dtau220=0,01 é recusado. A segunda família só injeta GR e o recibo diz isso; não foi encontrada promoção de envelope para dephasing pSEOB nem alegação de segunda família TGL. Escala de SNR é IMR ótima de rede na PSD/banda, explicitamente distinta de SNR de ringdown. A recuperação de M/chi permanece livre conforme os priors; não há remanescente fixado pela injeção.

## Conversão de remanescente — duas linhas finitas, nenhuma waveform

[REAL] `remnant_conversion.derive` foi executada em **duas** linhas sintéticas com o LAL instalado e Planck18 instalado. A interface retornou status/fração/spin; o código verifica status=0, 0<fraction<=1 e |af|<1, produz Mfdet=fraction*(m1+m2) em massas solares detector e conserva ordem/contagem. O caso (m1,m2,chi1,chi2,dL)=(30,5,−0,9,−0,9,800) manteve **af=−0,23050186436685438**, sem drop. Isso requer domínio QNM posterior explícito; não autoriza extrapolação BCW.

| Linha sintética | Mfdet | af | z sob Planck18 INPUT |
|---|---:|---:|---:|
| (40,30,0,2,−0,1,400 Mpc) | 66,5647448952548 | 0,7067859620958441 | 0,08491816070057145 |
| (30,5,−0,9,−0,9,800 Mpc) | 34,636010119925395 | −0,23050186436685438 | 0,1616798608183367 |

Arquivo `/opt/lal_env/lib/python3.12/site-packages/astropy/cosmology/data/Planck18.ecsv`: SHA256 **cb54925ee712fb46f9b820d6057a4cdc0c34414a4b4e3ca5c76aba98baa5e59d**. Parâmetros usados: H0=67,66; Om0=0,30966; Tcmb0=2,7255; Neff=3,046; m_nu=[0,0,0,06] eV; Ob0=0,04897. Código Astropy/cosmology aparece no manifesto de runtime inspecionado. O código local e a execução sustentam esta conferência; não alego ter refeito a consulta web que o principal realizou.

[OPEN — integração, não falha do cálculo] A versão de pe_runner.py pinada nesta revisão ainda escreve remnant_status/redshift_status OPEN e não chama derive; o principal informou integração pendente. E2 precisa incluir os parâmetros e pin acima, depois a revisão deve conferir o caminho integrado. O esquema publicado E7 não foi alterado.

[P2 — consistência de nomenclatura/configuração] O SHA do ECSV é conferido, mas o código **não compara** `cosmology_parameters` ao conteúdo do ECSV; poderia chamar outra combinação numérica de Planck18_external_INPUT. Os valores da fixture coincidem com o objeto instalado. Ao congelar, validar essa igualdade por código/controle pinado, ou nomear qualquer variante como variante INPUT, em vez de inferir igualdade a partir do hash de um arquivo apenas lido para SHA.

## Pins principais e reprodução

| Artefato | SHA256 do estado testado |
|---|---|
| null_runner.py | 2aa0c1f2e57d35c1baaffda1ed8b4f055c6481e4d912208aff959579ace33a6a |
| synthetic_null.py | be0fa6d4b678993edcbc7dec15f311950c51e466020dc99c5d0f043763eb65f1 |
| route_iv_null.py | dfcf9491ab98f9d32aae119177f53a3622289593c19c528e50cd091ebd7000cd |
| fetch_registered.py | d56ba5f49e449a9efa3d12fec8e3e989b6b5bf57abef6e579abb00877f271c4b |
| injection_design.py | 6c512a0911fe6aa5b9c106239e63fdf41d94c33af49200127aeb5843cfee3e8d |
| remnant_conversion.py | 641451837ba636cd05eea34bdcc439917a20877d6a9f2d132cca8b32d48fff3f |
| E2_DESIGN_DRAFT_001.json | be65bbacadaec7808075fdb8c0e42159ed3ea35018b95e6ae6d281097621013a |

Comando efetivamente usado: `/opt/lal_env/bin/python -B /mnt/c/IALD/Central\ de\ Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/review_main_fixtures.py`. A fixture cria seu JSON com modo exclusivo: para repetir após mudanças, versionar o script/resultado, preservando a tentativa anterior. Não rodar os main() dos produtores para reproduzir esta revisão.

> [nota operacional do operador — omitida no retrato público]