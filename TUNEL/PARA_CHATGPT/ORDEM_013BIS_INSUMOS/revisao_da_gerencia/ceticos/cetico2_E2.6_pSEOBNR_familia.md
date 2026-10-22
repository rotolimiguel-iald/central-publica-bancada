# CÉTICO 2 — achado «pSEOBNRv4HM_PA não é o espaço dos posteriores publicados» (ORDEM 013-bis l.172 / l.182)

Veredito: **refutado = false**. Gravidade mantida: **IMPORTANTE**.

## O que medi (22/09/2026, bancada só leitura)
- `C4_SCHEMA.json` (GW250114 / GWTC-5.0): `grep -oE 'pSEOBNR[^"]*'` → só `pSEOBNRv5PHM*`; contagem `grep -c pSEOBNRv5` = 705, `pSEOBNRv4` = 0. Chaves `pSEOBNRv5PHM/approximant`, `pSEOBNRv5PHM/version`, `pSEOBNRv5PHM/config_file/config/{waveform_approximant, minimum_frequency, maximum_frequency, sampling_frequency, duration, psd_dict, psd_length, reference_frequency, mode_array, distance_marginalization, phase_marginalization, time_marginalization, calibration_model, likelihood_type}` existem.
- `C4_CATALOG_SCHEMA.json` v5=20/v4=0; `C4_CATALOG_PRIOR_AUDIT.json` v5=78/v4=0; `C4_GWTC3_SCHEMA.json` v5=0/v4=378 (`pSEOBNRv4HM_tgr_20200402_54e79581_usehm`); `C4_GWTC3_220.json` v4=9.
- O número citado na l.182 (−0,013 [−0,103; +0,087]) é `C4_220_INITIAL.json` → `quantiles.dtau220 = [−0,10335; −0,01340; +0,08731]`, N=40776, prior `Uniform(−0,8; 2,0)` em `dtau220`, sobre o posterior **pSEOBNRv5PHM** do release (source_sha256 b9971bcd…). Logo E3.1 manda reproduzir com v4HM_PA um número medido em v5PHM.
- `medir/A_poder_eventos/A_poder_eventos.json:1297` já diz «(pSEOBNRv5PHM / pseob-rd / pSEOBNRv4HM)»; `samples_summary.json` rotula os eventos como `pSEOBNRv5PHM-reweighted`. A gerência sabia o modelo e a ordem não o transportou.
- ORDEM 013 §5 l.308/310: pyseobnr não instalado; instalável em venv de usuário (nunca em /opt) com LAL_DATA_PATH do Zenodo 14999310. `SINTESE.md:179`: instalabilidade «não testada». A ordem 013-bis não menciona `pyseobnr` nem `pSEOBNRv5PHM` uma vez (grep = 0 ocorrências).

## Por que a frase induz erro
A l.172 diz que pSEOBNRv4HM_PA é «o espaço em que os posteriores publicados vivem». Falso para GWTC-5.0/GW250114 (v5PHM, precessante) e verdadeiro só para GWTC-3 (v4HM, spins alinhados). O que é comum é o **parâmetro** (δτ fracional do 220, `dtau220`/`DTau220`), não o modelo. Consequência na l.182: uma diferença piloto×publicado fica inatribuível (família v4HM_PA×v5PHM, wrapper Bilby próprio×config do release, f_low/srate/duração/PSD/marginalizações) — a bancada pode declarar «reproduz» ou «não reproduz» sem que ninguém saiba o que foi comparado. A ordem também não manda ler o `config_file/config` do release, que é o único meio de casar a configuração.

## Por que não é BLOQUEANTE
O parâmetro é o mesmo e comparável; não há número fabricado nem gate movido; a decisão de convenção segue [INPUT] com veto do operador. É frase errada + ambiguidade explorável → IMPORTANTE.

## Correção FINAL (texto para substituir; estilo e estatutos mantidos)
Ver StructuredOutput / abaixo.
