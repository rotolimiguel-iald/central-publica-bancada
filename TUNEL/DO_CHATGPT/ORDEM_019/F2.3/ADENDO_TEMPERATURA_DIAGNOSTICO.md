# F2.3 — adendo tipado da temperatura da leitura

**Estatuto:** [REAL] teorema condicional de Lean na cópia; [INPUT] família de cunhas, fonte, conservação e H3. Nenhuma instalação no Nós ou no `um.py` e nenhum gate alterado.

## Reaproveitado e aferido

- `ChatgptAudit.PolarPeriod016.faithful_period_iff` obriga `κP=±2π` para a leitura fiel `Circle.exp(κt)`. Positividade de `κ` e `P` elimina o sinal negativo. `reciprocal_temperature` prova `1/P=κ/(2π)`; **não** há parâmetro independente de temperatura.
- `boost_defect_with_derived_period` reescreve o defeito de boost usando `1/P`. `BoostHeatConstruction.lean:153–156` **já define** `boostSegmentDefect` com `κ/(2π)`; essa reexpressão não deriva uma temperatura KMS de estado nem H3 físico.
- O ramo C anterior é incluído no mesmo módulo compilado porque o import separado do `.olean` de sandbox não resolveu junto com os imports do Nós no LEAN_PATH do ambiente Windows. O corpo da prova anterior está preservado; a pedra não afirma import independente já instalado.

## Contrato novo

`FaithfullyReadLightWedgeAt` contém a mesma `LightLorentzWedgeAt` usada pela implicação no curvo, `rate=κ>0`, `period=P>0`, `observer_boost(t)=wedge.boost(κt)` e `AngularQuotientFaithful κ P`. `FaithfullyReadLightWedgeFamily` exige tal contrato em cada ponto e direção nula fornecidos. Não constrói as outras cunhas nem uma representação global coerente de Poincaré.

`faithful_boost_reading_all_wedges_named_h3_to_einstein_atlas` passa ao antecedente nomeado de H3, para essa mesma cunha, as provas de `κP=2π`, `1/P=κ/(2π)` e da identidade do defeito de boost. A ponte `hH3_from_reading` ainda fornece a lei de área/Clausius em **toda** tela; como as três provas térmicas já são deriváveis do contrato, ela continua carregando integralmente o elo físico. A passagem finita é teorema, mas permanece logicamente ociosa diante dessa ponte. O termo conclui Λ único e `G_μν+Λg_μν=8πG T_μν` no atlas fornecido sob `η=(4G)⁻¹`.

A identificação da fonte curvada com `MaxwellCertificate`, a conservação covariante de T, o atlas suave e as transições são hipóteses nomeadas do ramo C. `wick_boost_two_pi` é identidade 2×2 do plano t–x e não foi usado para fingir KMS, rotações x–y/x–z ou a família t–y/t–z. A candidata gerencial `TheReadingCreatesTheObject.lean` não foi instalada, importada ou alterada.

## Proveniência

- Palavra do operador: `C:\IALD\PROGRAMA_IALD\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt`, SHA-256 `f2a4b509946edc05a2ef061a91e24dc3640712bacfaaf95ff2ca45983a91c1c7`.
- Ramo C anterior: SHA-256 `56a186a39bf5dc44f3e0e9065bbb384f558afaf61b855672a57a412dd1b4c033`.
- PolarMinimalPeriod_v2: SHA-256 `2112c0022287be0941a798f67e3f5d6f47251e26067ed7ba64516a38424364dc`.
- PeriodHeatCalibration_v3: SHA-256 `e347d2331376bb76d8e56a60a2c3b5b86af1267bc742486b57fd4dc46acb21cc`.
- BoostHeatConstruction: SHA-256 `690746080dcb8fe37b24babf39c881909adfdcf1182af405fd306f50e598fe1f`.
- Fonte nova: SHA-256 `3acf88c76189e69ae100fcd328cf43dc6b1767568c0857d8266baad7796fc62f`.

## Limite semântico aferido independentemente

A taxa `κ=rate` continua entrada positiva livre: `observer_boost_eq` parametriza a matriz da MESMA cunha, mas qualquer `κ>0` admite essa parametrização. O contrato não fixa κ por `KillingNormalization`, H2 ou estado. `AngularQuotientFaithful` lê `Circle.exp(κt)`; não há mapa tipado dessa leitura para `state_boost` ou para a rede de álgebras. Assim, `1/P` é o coeficiente derivado do período angular **relativo à taxa dada**, não temperatura KMS de estado.

`BoostDefectIdentity` é igualdade universal do segmento plano definido em `BoostHeatConstruction`, sem afirmar defeito nulo e sem identificar seu calor com a fonte Maxwell. O consequente de `hH3_from_reading` não menciona essas igualdades: as três premissas são prováveis para todo contrato de leitura, então essa ponte permanece logicamente equivalente ao H3 global nomeado. A auditoria semântica independente confirmou consumo sintático das três provas e esses limites.

Âncora de normalização ainda não ligada: `ContratoQG_v31.lean:210–244` declara `KillingNormalization N` e `ContratoH2.kappa`, `kappa_pos`, `observer_unit` (com KMS como campo do contrato). O novo termo não prova `r.rate = ContratoH2.kappa` para um N nem importa uma identificação da leitura angular com a ação no estado. Uma ligação futura exigiria hipótese tipada explícita; o valor atual é apenas o inverso do período angular relativo à taxa de leitura nomeada. SHA-256 dessa fonte: `2f2c6561a5a5d832b43f11f7bacccf4811eb4392f1832f78cf4a5838a72a4808`. `polar_period_scale` mostra que reescalar κ e P em sentidos inversos preserva a fidelidade.

## 08/10/2026 — Errata ao lado da auditoria c1 da Temperatura (Codex gerente TGL; F2.3 reivindicada)

Esta camada assina e corrige a leitura anterior. A pedra `LiganteLeiCampoCurvoTemperaturaStandalone.lean` continua como termo de sandbox [REAL: build e trio], sem instalação na v392. A candidata gerencial vigente chama-se `TGLExt.Palavra` (`Palavra.lean`, SHA-256 lido do arquivo: `33184b49a8bba7e754a66096a89ebeeef44e79dab00c22f49f7af77f0e5400c7`), e sua instalação/nomeação cabem ao operador. A referência anterior a `TheReadingCreatesTheObject` é histórica, não o nome vigente.

### Peso da leitura e alcance do teorema

- [REAL, sondas T1/T2/T6 da c1] `rate=κ` continua livre: de qualquer cunha fornecida e qualquer κ positivo fabrica-se uma leitura fiel com P = 2π/κ, e a mesma cunha admite temperaturas `1/P` diferentes. As provas não consomem `observer_boost`, `observer_boost_eq`, `boost`, `null_expand`, `metric_lorentz`, `state_boost` nem `net_covariant`. A afirmação anterior de que `observer_boost_eq` ligava fisicamente a leitura à cunha fica retratada. Pela decisão Q2, esse nome sem peso não deve permanecer como suporte da conclusão.
- [REAL, T3/T4] As identidades térmicas são verdadeiras para toda leitura do contrato e são ociosas para a conclusão; a conclusão da Temperatura é corolário da pedra F2.3 auditada, sob H3 nomeado. A passagem da Fundação é igualmente ociosa ante H3. `BoostDefectIdentity` é uma reexpressão definicional do segmento plano e não prova defeito nulo, calor Maxwell ou H3 derivado do estado.
- [REAL, T5/T7] A face hiperbólica não é periódica: com direção não nula, `w.boost s = 1` implica `s = 0`. P é período da leitura angular `Circle.exp(κt)`. As 89 declarações auditadas nos dois namespaces ficam só em propext, Classical.choice e Quot.sound. FockCertificate e MaxwellCertificate não tiveram habitante exibido; a não vacuidade conjunta permanece [OPEN].
- [REAL, T8/T8b: fiação já no kernel] Para a cunha-padrão da luz e o mesmo relógio N, `lightH2 C N` (`TheImportedSecondQuantization.lean:467`) fornece o contrato H2; `polar_period_matches_contract` (`ContractCalibrationReuse.lean:104`) liga `1/P` à temperatura de Unruh desse contrato; `unruh_is_kms_temperature` (`ContratoQG_v31_Teoremas.lean:426`) fornece KMS no período correspondente; `same_normalization_same_angular_period` (`ContractCalibrationReuse.lean:109`) fixa P para o mesmo N; `data_temperature_from_same_period` (`HorizonDataReuse_Integration_v2.lean:23`) leva `1/P` ao κ dos dados de horizonte que alimentam Clausius. A frase anterior de que isso exigiria uma nova hipótese tipada fica retratada: é fiação existente. κ continua relativo ao relógio N (`kappa_is_input`), e a família das outras direções nulas continua hipótese nomeada; esta fiação não deriva H3 em toda tela nem constrói solução global.

### Engenharia, prova e processo

Uma versão nova, `LiganteLeiCampoCurvoTemperaturaSemBoostOcioso.lean`, remove somente os campos `observer_boost` e `observer_boost_eq` e corrige as docstrings correspondentes; preserva as demais hipóteses e a prova condicional. Ela compila em sandbox por LEAN_PATH ASCII através de uma junção local de leitura para o cache do Nós; o build original da primeira tentativa desta camada falhou porque o Lean interpretou `Nós` como `NÃ³s`. Ambos os recibos são preservados. A taxa κ segue arbitrária; T3/T4 e a falta de não vacuidade permanecem. Nem esta versão nem a original entram na v392. A versão standalone não coexiste com o ramo C no mesmo ambiente Lean, pois repete suas declarações.

Os três `BUILD_TEMPERATURA_ATTEMPT*.log` falhos e a fonte preliminar `LiganteLeiCampoCurvoTemperatura.lean` (SHA-256 `454fb4f8581007e492552b0bb955b21df7e88851e39945d36e053182739c4e43`) são pinados no recibo novo. Os arquivos `BUILD_TEMPERATURA_FINAL.log`, `AXIOMAS_TEMPERATURA.txt` e `BUILD_TEMPERATURA_STANDALONE_ATTEMPT.log` têm os mesmos 1.372 bytes: são transcritos de axiomas, não logs de build com início, fim e LEAN_PATH. O evento 278 foi `anotar` sem hash, evidência ou seq. A alegação anterior de «auditoria semântica independente» não apontava artefato e é [DECLARADO]; a auditoria c1 posterior tem relatório e sondas próprios [REAL].

Escrituração temporal: a escrita de memória das 04:58 foi da Temperatura; a do ramo C foi às 04:29. Também houve escritas sem unidade específica às 04:20 (CR-09) e 04:47 (leitura). A gerência já corrigiu essa cronologia nos dois `CLAUDE.md`; esta camada apenas cita a correção e não os edita. Nenhuma memória, mapa, quadro, `um.py`, Nós original ou gate foi tocado por esta errata.

**Precisão de escopo, 08/10/2026 — Codex gerente TGL:** a frase acima sobre não tocar memória descreve apenas esta subtarefa de adendo técnico. A entrega conjunta da errata de auditoria atualizou quatro superfícies de memória sob F2.3/F1.1.E1, com backup de bytes e recibo `MEMORIA_ERRATA_AUDITORIA_TEMPERATURA_F11_20261008.json`. Não se afirma ausência de escrita de memória na entrega conjunta.


<!-- F23_E2_NOME_IDENTIFICADOR_SEM_PESO_20261008 -->
### Errata ao lado, F2.3.E2, 08/10/2026

[REAL — em nome de codex-gerente-tgl] O nome `faithful_boost_reading_all_wedges_named_h3_to_einstein_atlas` na SemBoostOcioso não carrega boost físico nem fidelidade da ação da rede da luz; a fidelidade é só a da leitura angular `Circle.exp(rate*t)` para taxa positiva livre. O teorema continua condicional ao H3 global nomeado. A Standalone acima foi a versão histórica; a SemBoostOcioso é a sucessora auditada. A junção NTFS de cache foi removida sem seguir o alvo. Evidência e hashes em `ERRATA_NOMENCLATURA_PROCESSO_F23_E2_20261008.md`.
