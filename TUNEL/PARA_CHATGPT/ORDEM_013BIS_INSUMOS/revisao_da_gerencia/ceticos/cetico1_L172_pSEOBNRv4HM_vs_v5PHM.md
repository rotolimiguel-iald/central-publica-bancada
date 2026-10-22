# CÉTICO 1 — achado da lente executabilidade_tunel sobre a ORDEM 013-bis, l.172 (E2.6) e l.182 (E3.1)

**Veredito: refutado=false (o achado está certo). Gravidade mantida: IMPORTANTE.**

## O que medi (só leitura, por script, 22/09/2026)

1. `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_SCHEMA.json` — `grep -o 'pSEOBNR[A-Za-z0-9_]*' | sort | uniq -c`:
   `695 pSEOBNRv5PHM · 4 pSEOBNRv5PHM_QNM22 · 3 pSEOBNRv5PHM_config_complete · 5 pSEOBNRv5PHM_data0_1420878141`. Zero `v4HM`.
   Chaves existentes: `pSEOBNRv5PHM/approximant`, `pSEOBNRv5PHM/config_file/config/waveform_approximant`, `pSEOBNRv5PHM/meta_data/meta_data/approximant`.
2. `C4_CATALOG_SCHEMA.json` (GWTC-5.0 metafiles): `20 pSEOBNRv5PHM`, zero v4HM.
3. `C4_GWTC3_SCHEMA.json`: `18 pSEOBNRv4HM · 360 pSEOBNRv4HM_tgr_20200402_54e79581_usehm`.
4. `C4_220_INITIAL.json` (GW250114, source_sha256 b9971bcd…a627, N = 40776): o `config_text` do prior traz `tilt_1 = Sine`, `tilt_2 = Sine`, `phi_12`, `phi_jl` — prior **precessante** (v5PHM); os quantis publicados batem com a ordem: dtau220 = [−0,10335; −0,01340; +0,08731] ⟹ «−0,013 [−0,103; +0,087]» da l.182 está correto.
5. `auditoria\aud_6.txt:26` [PAGO_VERIFICADO]: «Grupo pSEOBNRv5PHM, N = 40.776»; `aud_6.txt:32`: os 33 do GWTC-5.0 têm grupos `pSEOBNRv5PHM`, `pSEOBNRv5PHM-reweighted` e `pseob-rd`; os 18 do GWTC-3 `<evento>/posterior_samples` (v4HM).
6. `bis\medir\E_instrumento\MEDICAO_E.json:206,222`: `pyseobnr: AUSENTE` nos dois venvs; `:241`: `pyseobnr 0.3.7 disponivel` no PyPI (só leitura). `SINTESE.md:179`: «Instalabilidade de pyseobnr 0.3.7 … não testada».
7. ORDEM 013-bis: `grep -n -i 'v5PHM|pyseobnr'` → **zero ocorrências**. A única menção a v5 é l.181 «NRSur7dq4/SEOBNRv5 falham (LAL_DATA_PATH; … Zenodo 14999310)» — isso é o **SEOBNRv5 ROM do LAL**, não o `pSEOBNRv5PHM` do `pyseobnr`; a ordem conflui os dois.
8. ORDEM 013 §5 l.310 já autoriza «SEOBNRv5/NRSur/qnm só num ambiente NOVO de usuário … nunca em /opt» — logo a **permissão** de instalar existe (herdada pela 013-bis l.236), mas a 013-bis não nomeia `pyseobnr`/`pSEOBNRv5PHM` como a rota que reproduziria o posterior publicado no mesmo modelo.

## Por que o achado não se refuta

- **l.172, trecho «pSEOBNRv4HM_PA … por ser o espaço em que os posteriores publicados vivem (a C4 compara ali)»** — frase falsa para o MODELO: a C4 compara em `pSEOBNRv5PHM` (GW250114 e GWTC-5.0) e em `pSEOBNRv4HM` (GWTC-3). O comum é o PARÂMETRO (δτ fracional do QNM 220, `dtau220`/`DTau220`; prior Uniform(−0,8; 2,0)), não o aproximante. `pSEOBNRv4HM_PA` é spins alinhados (PA = pós-adiabático) `[KNOWN]`; v5PHM é precessante — o prior do release (item 4) exige tilt/phi_jl.
- **l.182 «reproduz o δτ̂₂₂₀ publicado … dentro da sua σ»** — pede reprodução de um posterior v5PHM precessante com um piloto v4HM_PA alinhado sem declarar a diferença de modelo nem mandar casar o config do release (f_low, srate, duração, PSD, marginalizações — todos presentes em `pSEOBNRv5PHM/config_file/config/*`, item 1). Uma falha do critério «dentro da sua σ» fica **inatribuível** (família × wrapper × configuração) — exatamente o tipo de ambiguidade que a bancada pode explorar num item de aceitação (l.185).
- **Alternativa não orçada**: `pyseobnr` 0.3.7 (v5PHM) em venv próprio é instalável (item 6) e a ORDEM 013 §5 já permite; a 013-bis não a nomeia. Não é bloqueante (a permissão herdada existe; o operador pode vetar a convenção, l.172), mas é a diferença entre um piloto que **reproduz no mesmo modelo** e um que **mede uma diferença de família** sem dizer.

## Por que não sobe a BLOQUEANTE
A ordem não fabrica número (os quantis conferem), não decide partição, e o E3.1 já manda imprimir «diferença contra o publicado». O erro é de frase e de atribuição — a bancada executa, mas o resultado do piloto sai com uma comparação mal tipada. IMPORTANTE.

## Correção FINAL (texto pronto; substituir em l.172 e em l.182; acréscimo a l.181)

**l.172 (E2.6), substituir o item 6 inteiro por:**
6. **Convenção única de deformação pós-pico [INPUT]:** a gerência propõe como padrão **o δτ fracional do QNM 220 na família pSEOB (`dtau220`/`DTau220`, e `DTau440` para o 440; prior Uniform(−0,8; 2,0) como no release)** — é o **parâmetro** em que os posteriores publicados vivem e em que a C4 compara (GW250114 e GWTC-5.0: grupo `pSEOBNRv5PHM`, precessante `[REAL — C4_SCHEMA.json, aud_6]`; GWTC-3: `pSEOBNRv4HM` `[REAL — C4_GWTC3_SCHEMA.json]`). **O modelo do piloto é `pSEOBNRv4HM_PA` (spins alinhados) por ser o que o lalsimulation 6.2.1 instalado traz; `pSEOBNRv5PHM` via `pyseobnr` 0.3.7 em venv próprio (ORDEM 013 §5; nunca em /opt) é a alternativa que reproduz o publicado no MESMO modelo — a orçar em E3.2, instalabilidade não testada `[OPEN]`.** As alternativas de convenção (C7_NATIVE: envoltória 22/44; C5: overtones compartilham Γ₂₂₀) ficam registradas com o mapa TGL → δτ̂₂₂₀ de `tgl_ringdown_prediction.py` e a diferença entre convenções impressa. **O operador pode vetar a escolha ao abrir a ordem.**

**l.181 (E3, cabeçalho), substituir «NRSur7dq4/SEOBNRv5 falham (LAL_DATA_PATH; dados públicos Zenodo 14999310, instaláveis em pasta própria — não testado)» por:**
«NRSur7dq4 e o SEOBNRv5 ROM do LAL falham (LAL_DATA_PATH; dados públicos Zenodo 14999310, instaláveis em pasta própria — não testado); o `pSEOBNRv5PHM` do release é outro pacote (`pyseobnr` 0.3.7, ausente nos dois venvs, disponível no PyPI `[REAL — MEDICAO_E.json]`), instalável só em venv próprio (ORDEM 013 §5)»

**l.182 (E3.1), substituir «e reproduz o δτ̂₂₂₀ publicado (−0,013 [−0,103; +0,087]) dentro da sua σ.» por:**
«e compara com o δτ̂₂₂₀ publicado do grupo `pSEOBNRv5PHM` (−0,013 [−0,103; +0,087], sha b9971bcd…a627): **antes de rodar, ler o config do release (`pSEOBNRv5PHM/config_file/config`, com sha) e casar f_low, taxa de amostragem, duração do segmento, PSD/janela, prior de `dtau220` (Uniform(−0,8; 2,0)) e marginalizações; a única diferença declarada é o modelo (v4HM_PA alinhado × v5PHM precessante) — e a diferença contra o publicado é reportada como tal, com a σ do publicado ao lado; «dentro da sua σ» é leitura, não critério de reprovação do piloto**. Se `pyseobnr` for instalado (E3.2), repetir o piloto no mesmo modelo e aí sim exigir reprodução dentro da σ.»

**l.185 (Aceitação E3.1), acrescentar:** «config do release lido e casado (hash); diferença de modelo declarada.»
