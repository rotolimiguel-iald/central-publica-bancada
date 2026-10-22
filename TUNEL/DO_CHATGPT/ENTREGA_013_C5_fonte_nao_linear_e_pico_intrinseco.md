[REAL — candidatos de fonte física e verificação numérica; DERIVED condicional no limite de poder; marginalização completa OPEN]

# Ordem 013 — fonte não linear, polarização coerente e correção do pico

UTC: 2026-09-22T04:36:38.574849+00:00. Axiomas: N/A — sem Lean. O C6 e o programa canônico permanecem intactos.

## Resultado

Foram feitas 12 buscas com a convenção antiga de pico e 12 numa rodada corrigida, reaproveitando os candidatos anteriores. Três binários alinhados, duas famílias de injeção e duas de recuperação. A injeção tem a=1 no ramo B; a recuperação busca uma fonte GR, a=0, variando massa total, razão de massas, ambos os spins, inclinação, fase e instante do pico. Distância e uma polarização são compartilhadas pela rede.

**As seis recuperações pela própria família admitem candidatos sem dephasing com resíduo de 0.1449 a 0.5979 em unidades da métrica de ruído, para SNR de ringdown 40**, nas PSDs O4/O5 de referência. Verificados com geradores a 16384 e 32768 Hz. A busca é local: um candidato válido dá uma cota superior para o melhor resíduo, mesmo quando o otimizador esgota seu orçamento. Não é garantia de ótimo global, cobertura, posterior ou fator de Bayes.

As trocas de família têm resíduos entre 0.6606 e 4.857. Portanto a incerteza do gerador precisa permanecer no modelo. Não se seleciona apenas o ajuste favorável.

| Candidato | PSD | Resíduo a 16384 Hz | Resíduo a 32768 Hz | Ambos abaixo de um |
|---|---|---:|---:|---|
| reference_IMRPhenomXPHM_to_IMRPhenomXPHM | O4 | 0.144953 | 0.144873 | sim |
| reference_IMRPhenomXPHM_to_IMRPhenomXPHM | O5 | 0.147022 | 0.14695 | sim |
| reference_IMRPhenomXPHM_to_SEOBNRv4HM | O4 | 0.668337 | 0.668495 | sim |
| reference_IMRPhenomXPHM_to_SEOBNRv4HM | O5 | 0.660434 | 0.660626 | sim |
| reference_SEOBNRv4HM_to_IMRPhenomXPHM | O4 | 0.905949 | 0.905899 | sim |
| reference_SEOBNRv4HM_to_IMRPhenomXPHM | O5 | 0.899861 | 0.89981 | sim |
| reference_SEOBNRv4HM_to_SEOBNRv4HM | O4 | 0.317586 | 0.317225 | sim |
| reference_SEOBNRv4HM_to_SEOBNRv4HM | O5 | 0.320533 | 0.319987 | sim |
| source_64_IMRPhenomXPHM_to_IMRPhenomXPHM | O4 | 0.517437 | 0.517421 | sim |
| source_64_IMRPhenomXPHM_to_IMRPhenomXPHM | O5 | 0.512796 | 0.512781 | sim |
| source_64_IMRPhenomXPHM_to_SEOBNRv4HM | O4 | 4.25326 | 4.2621 | não |
| source_64_IMRPhenomXPHM_to_SEOBNRv4HM | O5 | 4.22815 | 4.23706 | não |
| source_64_SEOBNRv4HM_to_IMRPhenomXPHM | O4 | 3.3484 | 3.3504 | não |
| source_64_SEOBNRv4HM_to_IMRPhenomXPHM | O5 | 3.33365 | 3.33568 | não |
| source_64_SEOBNRv4HM_to_SEOBNRv4HM | O4 | 0.563785 | 0.564073 | sim |
| source_64_SEOBNRv4HM_to_SEOBNRv4HM | O5 | 0.559458 | 0.559775 | sim |
| source_90_IMRPhenomXPHM_to_IMRPhenomXPHM | O4 | 0.416988 | 0.416953 | sim |
| source_90_IMRPhenomXPHM_to_IMRPhenomXPHM | O5 | 0.42127 | 0.421241 | sim |
| source_90_IMRPhenomXPHM_to_SEOBNRv4HM | O4 | 2.85584 | 2.85783 | não |
| source_90_IMRPhenomXPHM_to_SEOBNRv4HM | O5 | 2.8844 | 2.88636 | não |
| source_90_SEOBNRv4HM_to_IMRPhenomXPHM | O4 | 4.85355 | 4.85718 | não |
| source_90_SEOBNRv4HM_to_IMRPhenomXPHM | O5 | 4.83488 | 4.83925 | não |
| source_90_SEOBNRv4HM_to_SEOBNRv4HM | O4 | 0.598038 | 0.59792 | sim |
| source_90_SEOBNRv4HM_to_SEOBNRv4HM | O5 | 0.592194 | 0.592087 | sim |

## A falha identificada e corrigida

Para o par alinhado ±22, h+ é proporcional a (1+cos²i)/2 vezes uma quadratura e h× a cos i vezes a outra. Assim h+²+h×² pode oscilar com a fase quando a fonte é inclinada: seu máximo não é a amplitude intrínseca do modo complexo. No candidato problemático, o pico projetado saltou **2.60065 ms** ao mudar a resolução. O pico intrínseco variou **12.6872 μs** no mesmo diagnóstico.

A rodada nova usa o máximo da amplitude do 22 visto face-on, antes da projeção para a orientação da fonte, e mantém um único instante para todos os harmônicos. Trata-se de uma convenção nova, registrada separadamente: não alteramos o início ou o resultado do C6. A taxa do modelo continua aplicada ao tempo desde o pico declarado; nenhuma identificação física única de início/desenrolamento é inferida disso. O pico e as buscas antigos permanecem como evidência do erro.

## O que o limite gaussiano permite dizer

Para dois templates fixos h0 e h1, branqueados por uma covariância conhecida, r=||h1−h0||. O estatístico S=⟨h1−h0,Y−h0⟩/r tem distribuição N(0,1) sob h0 e N(r,1) sob h1. Um teste que controle o falso alarme do nulo composto GR também precisa controlá-lo no candidato h0 encontrado. No modelo gaussiano, o melhor poder desse par a um limiar unilateral de cinco sigmas é Φ(r−5).

Nos pares da própria família, isso dá cotas de poder entre 6.01547e-07 e 5.36089e-06 em SNR40. **É uma derivação condicional para os templates e ruído gaussiano, não uma medição da cauda do ruído real, nem uma conversão de ln B para sigma.** Uma fonte sem dephasing quase idêntica impede alto poder uniforme nesse cenário; não exclui a TGL nem elimina a necessidade da inferência.

## Likelihood que fica disponível

`coherent_imr_likelihood.py` reaproveita a integral linear existente com somente dois coeficientes comuns de rede: c=A cos(2ψ), d=A sin(2ψ). Eles representam distância e rotação de polarização, em vez de amplitudes independentes para cada modo/detector. O prior isotrópico gaussiano desses coeficientes equivale a ψ uniforme módulo π e p(D)=403²/(s²D³) exp[−403²/(2s²D²)], D em Mpc. É normalizado e marcado INPUT; não é prior uniforme em volume.

A integral de distância/polarização é exata, inclusive determinante; o maior erro contra a covariância completa foi 2.75122147286e-11. **Os sete parâmetros não lineares da fonte ainda não foram integrados.** O código não normaliza a forma de onda a um SNR escolhido dentro da likelihood. O SNR40 é apenas a normalização declarada das injeções de controle.

## Critérios, reprodução e aproveitamento

- **PAGO:** modelos físicos de rede com polarização comum; três fontes; ambas as famílias; resultados negativos incluídos.
- **PAGO:** pico intrínseco corrigido por diagnóstico explícito; nova rodada registrada; hashes e C6 original conferidos.
- **PAGO:** regeneração dos 12 candidatos e projeção QR independente, diferença máxima 8.881784197e-16; controle em 32768 Hz.
- **PAGO:** pacote inglês `cache/C7_COHERENT_SOURCE_REPRODUCTION_v1.zip`, 13662627 bytes; reprodução em pasta nova regenerou os candidatos, com diferença máxima de resíduo 0. O otimizador não foi repetido na reprodução; isso está expresso.
- **NÃO PAGO:** marginalização dos sete parâmetros, distribuição de evidência de fonte completa, calibração de ruído não gaussiano e cobertura sob população de fontes.
- **INALTERADO:** C6 INCONCLUSIVE_SYSTEMATICS, leituras físicas condicionais, escolha de relógio/partição e gate.

Descompactar o pacote e executar `python -B reproduce.py` num Python com PyCBC/LAL/NumPy/SciPy. Versões testadas constam no README e nos recibos. Os arquivos de forma de onda usam dados e geradores públicos; não há programa canônico ou acervo privado no pacote.

Há agora uma likelihood de fonte não linear com distância/polarização comuns integradas exatamente. Falta integrar os sete parâmetros de fonte e medir distribuições O4/O5 e cobertura sob fontes variadas; candidatos de Powell não são posteriores nem fatores de Bayes. Usar o módulo corrigido em cache/nonlinear_intrinsic_peak (ou C7_COHERENT_SOURCE_REPRODUCTION), não a versão histórica de pico projetado.

As buscas são não cegas, partem das fontes simuladas e de candidatos anteriores, e têm orçamentos limitados. Saídas de orçamento não foram renomeadas como sucesso. Nenhum evento real foi relido. As memórias locais receberam backups imediatos de bytes; a gerência mantém a incorporação canônica.

## Custódia lida nesta execução

| Arquivo | SHA-256 |
|---|---|
| `coherent_imr_model.py` | `3ee4c88b7c719f3a67f41dda4e67462cbb576ea8fcf191d8abe5480aba3f3d38` |
| `coherent_imr_likelihood.py` | `883613f37e7861c95ec43790c18ce7e790f7c708de776a75cb5496bc5fb3d74e` |
| `nonlinear_coherent_recovery.py` | `f426318a1f4cd2502cd71bed20377fa710fa78bd51425d8496059f294999d64a` |
| `validate_coherent_model.py` | `7c46f0c5ebef98dd936c9a4706815a7ffe867435a8c2cb22e826de143677a89e` |
| `validate_coherent_likelihood.py` | `375c839ef517c94db9f67a5548ac4f95573db877bc269636e1c764bd77e624dc` |
| `REGISTRO_C5_NONLINEAR_COHERENT.json` | `af458f8d7f283652fafea35c0fd1d31eb3578da31b9791c059448869f956203a` |
| `C5_COHERENT_MODEL_VALIDATION.json` | `646ac965b17089596e238af16af747919d4b2e1c5c391130b83ab9bd6eb62f1a` |
| `C5_COHERENT_LIKELIHOOD_VALIDATION.json` | `8fd147497ac2100e95da95aaa3328068aa22df590469dd8008fc0ed5a355368d` |
| `C5_NONLINEAR_COHERENT.json` | `ceeb3fda937f0d2b4b0dd4922868c81d72adff94775bf4f091400e2a72879ab3` |
| `C5_COHERENT_PEAK_DIAGNOSTIC.json` | `6a56b29f75bf1388d09c46c61fbfa9d361649a71ed8833e102844bfbfc22b8a2` |
| `diagnose_coherent_peak.py` | `55993e9eb781e142c7ebc2e0e9f1315b48014f14235613d962b959b8c5af20df` |
| `prepare_intrinsic_peak_run.py` | `2343c8199acaf3442717ed682eae1307d9b1c09bab7f1d4e228afa6e9cc4145d` |
| `verify_nonlinear_coherent.py` | `99e15f571626c28ab3ea32bfc1783414c3a8f9958d722f80b691f651b23dd107` |
| `build_coherent_source_package.py` | `24b1df2a9db1d258b40cb0976fa95174bcbbefcb35ccaf0176a3884f55a5d249` |
| `C7_COHERENT_SOURCE_PACKAGE.json` | `7b8a50c120c2533cdbc62be960fdeb8dee76a84bf621a33a261f6102072264ca` |
| `C7_COHERENT_SOURCE_REPLAY_VALIDATION.json` | `b6ed52324d189e52c9838fcbf0b4f74f1c1259f49bed44181d5f801acbee248b` |
| `C5_NONLINEAR_SOURCE_SUMMARY.json` | `e51a7faeda45d16f674986a1d5fdf55ac5da885d2d6fa67212ef586b92157b27` |
| `record_nonlinear_coherent.py` | `33b455a061013345665d18aa98210a1487dbc56ddd3d6a4a1ef839ae028d36aa` |
| `cache/C7_COHERENT_SOURCE_REPRODUCTION_v1.zip` | `19be994825bb76618dcfd1edcf3a819141a66a07999dc1324b41d1f7fb8efc3e` |
| `cache/nonlinear_intrinsic_peak/REGISTRO_C5_NONLINEAR_COHERENT.json` | `81f223445b02c1c313a8efe939b72cb7a6696adaaf80baa166b913555ff1a27c` |
| `cache/nonlinear_intrinsic_peak/C5_NONLINEAR_COHERENT.json` | `ded69e9a63371a6cfb2ed83beaaa653741d2177b9c43ddc2309cd7365be5a426` |
| `cache/nonlinear_intrinsic_peak/C5_NONLINEAR_COHERENT_VALIDATION.json` | `dbcc05451b948c77a3e495b353405ac77c91003b7811396a6ddb1b0f447fb28d` |
| `cache/nonlinear_intrinsic_peak/C5_COHERENT_MODEL_VALIDATION.json` | `11c2f0fa1a8a3d7f30c6dbb3819b67c48865fe7e8fd7a970abc2f2a2930e6ee8` |
| `cache/nonlinear_intrinsic_peak/C5_COHERENT_LIKELIHOOD_VALIDATION.json` | `cc292f917d0cba3be45df414ecb581eb51a547ae97f11a1684a138db025efc1a` |
| `cache/nonlinear_intrinsic_peak/PEAK_CORRECTION_PROVENANCE.json` | `13d603832d634774182c056a60ac29e821e172ebe402b76093a1f811650be78b` |
| `cache/nonlinear_intrinsic_peak/coherent_imr_model.py` | `4d9e568816c3b47e8e59b2401334a1a66541247fa80ed36495949aa4f5bca497` |
| `cache/nonlinear_intrinsic_peak/nonlinear_coherent_recovery.py` | `8c05dfa7d5e71fb17634ce4514290710a5208c1486472034e368161f8fb4dfa4` |
| `cache/MANIFESTO_DOWNLOADS.json` | `07c45d18d92ca3541625d76548eb0e1ff29ed82d34ed1388a4118fd39ed9efd7` |
