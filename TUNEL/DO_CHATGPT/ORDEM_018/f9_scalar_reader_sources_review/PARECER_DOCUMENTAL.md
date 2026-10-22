# Parecer independente — fontes dos cinco leitores escalares

[REAL documental] **PASS_DOCUMENTARY_ONLY.** As transcrições e a descrição D1–D6 são sustentadas pelos cinco resumos HTML locais e pelos documentos congelados examinados. O aceite é de integridade, correspondência e semântica documental. Não constitui admissão estatística, reexecução do composto ou novo veredito.

Manifesto: 3025 B, SHA256 6d6171f4cf9012c03dbaf75878acbe3183c9859d26071301feecf80720524521. Vínculo: 14451 B, SHA256 d37d7507f24bafd6960a7ff6cc5c375dea6d08fcbfadfc9d38ede2f1871b5bb0. Foram conferidas 26 relações de pins, discriminadas em FONTES_E_CONFERENCIAS.json; versões nos próprios HTMLs: SH0ES v3, CCHP v3, SBF v2, masers v2 e TDCOSMO v4. Fontes de proveniência Python foram somente lidas/analisadas por AST, nunca importadas ou executadas.

Os snippets e números de linha são âncoras de localização; isoladamente não demonstrariam todos os componentes nem a interpretação do leitor. A conclusão abaixo usa também a leitura integral de cada resumo arquivado. Datas/URLs de coleta permanecem evidência documental do recibo de origem, sem nova consulta à rede nesta revisão.

| Leitor | Transcrição e erro | Resultado da conferência |
|---|---|---|
| SH0ES R22 | 73,04 ± 1,04 | Resumo inclui sistemáticos, Cefeidas/SN, Gaia EDR3, NGC4258 e LMC; corresponde ao V1 e primário. |
| CCHP | 70,39; erros 1,22, 1,33 e 0,70 | TRGB sozinho; quadratura local 1,935794410571536 coincide com ambos os JSONs. |
| SBF | 73,8; erros 0,7 e 2,3 | Rota TRGB-SBF descrita como independente de Cefeidas/SN Ia e calibrada por NGC4258; quadratura local 2,4041630560342613 coincide. |
| Masers | 73,9 ± 3,0 | Seis galáxias, incluindo NGC4258; incerteza peculiar fixa de 250 km/s e sem correção peculiar no resultado principal escolhido. |
| TDCOSMO | 71,6 +3,9/−3,3 | Oito lentes, restrição de Omega_m por Pantheon+, LambdaCDM plano; média local dos lados = 3,6, armazenada como 3,5999999999999996 em binary64. |

[REAL — aritmética elementar] As três compressões foram conferidas por operações stdlib elementares independentes. Igualdade foi exata com os floats armazenados. Isso não recupera verossimilhanças, correlações, forma das caudas ou independência dos componentes de erro. Os dois casos identidade também coincidem. Nenhum z, evidência, covariância matricial ou composto foi recalculado.

**D1–D4 conferidos.** O rótulo CCHP TRGB+JAGB+Cef é amplo demais para 70,39; cefeida=false já está no V1 e não foi alterado. Em SBF, grupo_SN=true/grupo_4258=false realmente divergem de uma leitura literal da rota descrita. Masers inclui NGC4258 apesar do flag falso. TDCOSMO usa informação Pantheon+ em Omega_m, embora grupo_SN=false; essa dependência é distinta da calibração de luminosidade SN da escada. São razões para revisar a semântica da regra de grupos; os resumos não dão licença para inverter flags ou inventar covariâncias cruzadas.

**D5–D6 conferidos.** preregistro_fase3.py:24–25 e 49–52 documenta as quadraturas/simetrização. rodar_fase9_v1.py:115–116 usa os grupos na covariância desenhada. Nas linhas 64–65, 175 e 177, o runner carrega ALV e usa membership das chaves em lidos para marcar REAL por hash/contar declarados. Esse trecho não verifica os bytes das fontes nem a adequação da covariância. O vínculo documental entregue não deve ser transformado em ALVOS_FASE9_LIDOS.json ou em admissão automática.

[REAL — identidade do registro já aberto] Os cinco IDs são exatamente a família P_primaria do V1; campos H0/sigma coincidem entre vínculo, spec.leitores e resultado. frozen_metadata reproduz o V1 integralmente. O resultado aponta para o hash físico desse V1 e para o mesmo spec_sha256; a serialização canônica declarada foi conferida por hash, sem executar a função de veredito. runner_sha256 coincide com a fonte lida.

O resultado histórico continua TGL_FASE9_RAZAO_DE_HUBBLE_V1__INCONCLUSIVE_SYSTEMATICS__D1B__FUNDO_BG1__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED. Essa frase reporta o JSON já aberto: não resulta de avaliação nova. Seu R1 registra ALVOS ausente e cinco leitores DECLARADO naquela execução; a coleta/documentação posterior não altera retroativamente esse registro. A comparação escalar da gerência não é a comparação conjunta ROOT, e nenhum resultado/admissão foi transferido entre elas.

Não há bloqueador para aceitar esta entrega **como vínculo documental**. Continuam pendentes a interpretação científica dos grupos/dependências, a regra justificada de covariância e a admissão auditada para eventual abertura/execução decidida separadamente. Não é necessário fingir que hashes ou resumos resolvem essas escolhas.

Revisão 8a98bc66-b7a0-457b-8ddf-d145832d418c, UTC 2026-10-06T21:49:28.595586+00:00. Somente a pasta própria f9_scalar_reader_sources_review foi escrita, usando o helper oficial safe_files (backup exato de bytes, temporário verificado, replace e readback). Pacote, fontes, V1, resultado e runner foram reconferidos estáveis ao fechamento. Nenhum ALVOS, AUTH, CLAIM, memória, mapa, ledger ou continuidade foi criado/alterado; zero execução científica, import científico, arrays, catálogos brutos, rede, provedores, d72 ou P3.
