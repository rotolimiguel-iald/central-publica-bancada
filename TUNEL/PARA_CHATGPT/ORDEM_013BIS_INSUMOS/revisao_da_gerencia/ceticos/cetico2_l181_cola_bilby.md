# CÉTICO 2 — achado executabilidade_tunel sobre l.181 / l.236 (a «cola» bilby e «nenhum tem tudo») — 22/09/2026

**Veredito: refutado = false. Gravidade mantida: IMPORTANTE.**

## Medido por script (WSL, 22/09/2026; /opt só lido; OMP_NUM_THREADS=1)
- `/opt/lal_env`: lalsimulation 6.2.1, bilby 2.8.2, dynesty 3.1.0, gwpy 4.0.2, h5py 3.16.0, lalinference 4.1.10, numpy 2.5.3, scipy 1.18.1; AUSENTES: pycbc, pesummary, pyseobnr. `hasattr(ls,"pSEOBNRv4HM_PA")` True; Insert DTau220/DTau440/DOmega220 True.
- `/opt/pycbc_env`: lalsimulation 6.2.1 (pSEOBNRv4HM_PA True), pycbc 2.11.0, h5py 3.16.0; AUSENTES: bilby, dynesty, gwpy.
- `bilby.gw.source` contém `lal_waveform_dictionary` (True); `bilby.gw.waveform_generator` contém `time_domain_source_model` (True — a frase da ordem não é falsa, é desnecessária).
- Teste do modelo de fonte DE FÁBRICA `bilby.gw.source.lal_binary_black_hole` com `waveform_approximant="pSEOBNRv4HM_PA"` e `lal_waveform_dictionary` com DTau220 (m1=40, m2=30, d=400 Mpc, f_min=20 Hz, grade 0–2048 Hz a 0,25 Hz): roda sem erro; 0,137–0,148 s por forma; |Δh+|/max|h+| = 1,28×10⁻³ para DTau220=−0,02 e 3,50×10⁻² para DTau220=+0,5 (a deformação chega ao h(f) de bilby). Readback do LALDict: −0,02.

## Por que o achado se sustenta
1. l.181 e l.236 dizem «nenhum ambiente tem tudo»; para o que E3.1 pede (PE IMR bilby+dynesty, PSD off-source, pSEOBNRv4HM_PA com DTau220/DTau440) o `/opt/lal_env` TEM tudo. O que falta a ele (pycbc, pesummary, pyseobnr) não entra em E3.1. A frase, lida por bancada que já reabriu ciclos (l.36), sustenta «venv próprio» ou `ENTREGA_013BIS_BLOQUEIO` sem necessidade.
2. «wrapper Bilby `time_domain_source_model`» aponta a rota errada: a rota de fábrica (`_base_lal_cbc_fd_waveform` → SimInspiralFD, que condiciona aproximantes TD) já aceita o LALDict. A cola real é um source model FD de ~15 linhas que insere o DTau220 (e DTau440) amostrados no dicionário a cada chamada.
3. Lacuna de validação: E3.1 (l.182) e a aceitação (l.186) só exigem «reproduz o δτ̂₂₂₀ publicado dentro da sua σ». Sem injeção-recuperação de DTau220 conhecido ANTES do dado real, «não reproduz o publicado» não distingue bug do wrapper de diferença de PE — a bancada entregaria uma «parede» falsa (ou um PAGO falso por coincidência). A régua «existir ≠ ser aplicado» pede a prova do instrumento antes do dado.

## Não é BLOQUEANTE porque
a ordem é executável como está, não fabrica número, não decide o que é do operador. É ambiguidade explorável + critério de aceitação incompleto → IMPORTANTE.

## Ressalva à correção proposta pelo revisor
Uma PE completa por injeção custa o mesmo que o piloto (81–542 CPU-h estimados, l.182). A validação do wrapper não precisa disso: basta (a) teste de forma de onda a custo zero (saída do source model = chamada direta a SimInspiralFD com o mesmo LALDict, resíduo impresso; monotonia em DTau220) e (b) injeção-recuperação REDUZIDA (nlive baixo e/ou (M, χ) fixos nos valores injetados) em ruído gaussiano da PSD off-source. A correção final abaixo incorpora isso.
