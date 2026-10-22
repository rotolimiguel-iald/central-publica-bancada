# CÉTICO 2 — achado E7 (ordem l.207): «numpy puro» vs posteriores pSEOB em HDF5

**Veredito: refutado=false (achado confirmado; a correção proposta pelo revisor está ERRADA num ponto e foi refeita).** Gravidade: IMPORTANTE (mantida).

## Medido
- ORDEM 013-bis l.207: «`tgl_ringdown_ampliacao.py` (numpy puro; β em runtime; lê o registro E2, os posteriores pSEOB e o nuisance E1 …)».
- ORDEM 013 l.81 e l.224: fonte primária = `gw250114_pseobnr/posterior_samples.h5`; l.312: «Sem WSL: … Python 3.14; **sem h5py**. Para a C4, crie `.venv` + `pip install h5py`».
- Bancada (só leitura): `python -c "import h5py"` no Windows → `ModuleNotFoundError`; `.venv` NÃO existe em `ORDEM_013_RINGDOWN`. Os leitores da bancada (`posterior_220_readout.py`, `gwtc3_posterior_readout.py`, `catalog_220_readout.py`) importam `h5py` e `scipy.stats.gaussian_kde` — não são numpy puro.
- `um.py` l.201922: «tgl_pycbc_env tem gwpy/gwosc/h5py» — h5py só no ambiente WSL; o canônico não o tem no Windows.
- **Ponto que derruba a correção do revisor:** `C4_CATALOG_220.json` (673.228 B; 33 rows; N_posterior_draws 608.681) guarda por evento SÓ `quantiles` de 3 valores (ex.: GW150914_095045, N=17032, df220 = [-0,0515, 0,0192, 0,1189]) — zero amostras, zero `.h5` referenciado. A ordem exige (l.168 E2.2, l.195 E5.1, l.158 E3) «posteriores completos … nunca sobre medianas». Um JSON «no esquema do C4_CATALOG_220.json» entregaria quantis e violaria E2/E5. O esquema tem de carregar AMOSTRAS.

## Conclusão
A inconsistência é real e executável nos dois sentidos (ou o módulo não é numpy puro, ou não lê os posteriores). A separação extrator(h5py, WSL/.venv) → JSON de amostras → módulo numpy puro resolve; o JSON precisa ser de amostras (thinning só declarado, com semente e N por evento), com sha256 dos .h5 e do próprio JSON, e recusa fail-closed.
