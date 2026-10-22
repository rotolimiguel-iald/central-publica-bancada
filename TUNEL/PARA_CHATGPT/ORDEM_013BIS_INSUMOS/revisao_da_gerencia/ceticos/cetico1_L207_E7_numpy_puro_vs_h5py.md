# CÉTICO 1 — achado «E7: numpy puro × posteriores HDF5» (ORDEM 013-bis, l.207)

**Veredito: NÃO REFUTADO (refutado=false). Gravidade mantida: IMPORTANTE. A correção proposta pelo revisor está CERTA no diagnóstico e ERRADA no remédio (o esquema do `C4_CATALOG_220.json` não serve) — correção final abaixo.**

## O que foi medido (22/09/2026, só leitura na bancada)

1. **A linha.** `ORDEM_013BIS…md:207`: «`tgl_ringdown_ampliacao.py` (numpy puro; β em runtime; lê o registro E2, **os posteriores pSEOB** e o nuisance E1 …)». E2.2 (l.169) fixa o observável «sobre os **posteriores completos** pSEOB»; E5.1 (l.195) diz «nunca sobre medianas».
2. **Os posteriores são HDF5.** Na bancada: `ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles\*.h5` (lidos por `catalog_220_readout.py:57-58` com `h5py.File(path)['<label>']['posterior_samples']`) e `cache\public\17018009\...\gw250114_pseobnr\posterior_samples.h5`; `find -iname "*.h5" -o -iname "*.hdf5"` na pasta = **114 arquivos**.
3. **O Python do Windows não tem h5py** `[REAL]`: `python -c "import h5py"` → `ModuleNotFoundError` em `3.14.3 (MSC v.1944 64 bit)`. Igual ao dito na ORDEM 013 l.312 («Python 3.14; **sem h5py**»); h5py 3.16.0 só em `/opt/lal_env` (ORDEM 013 l.307).
4. **O `um.py` não importa h5py** `[REAL]`: `grep -i h5py um.py` (203.166 linhas) só acerta dentro de blobs base64; zero `import h5py`, zero `posterior_samples`. Um módulo que «lê os posteriores pSEOB» direto do `.h5` não entra no canônico como numpy puro.
5. **O esquema do `C4_CATALOG_220.json` NÃO carrega os posteriores completos** `[REAL — lido por script]`: 673.228 bytes, `rows[33]` com `quantiles.{spin,mass_detector,redshift,df220,dtau220}` de **3 valores cada** (ex.: GW150914 dtau220 = [−0,181; 0,101; 0,453]), `N` por evento (17.032), `N_posterior_draws` total 608.681, `GR_HPD_content` — e nada de amostras. Usá-lo como fonte do módulo violaria E2.2 e E5.1 (medianas/quantis em vez do posterior). A parte «no esquema do `C4_CATALOG_220.json`» da correção proposta pelo revisor **cai**.

## Por que não refuta
A inconsistência é real e a ordem fica imutável: a bancada ou entrega um módulo com `import h5py` (o um.py herda uma dependência que a régua «numpy puro» do canônico não tem) ou entrega um «numpy puro» que não lê o dado (E7 vazio). O revisor acertou; só o remédio precisa ser corrigido (amostras completas, não quantis; `.npz` é legível por numpy puro e evita um JSON de ~6×10⁵ linhas × 5 colunas, mas o JSON também serve — a ordem deixa a bancada escolher entre os dois, ambos hasheados).

## Correção FINAL (substituir a l.207 inteira)

### E7 — O MÓDULO PARA O um.py (a gerência incorpora)
Em duas peças, porque **o Python do Windows do `um.py` não tem h5py e o `um.py` não o importa** `[REAL — medido em 22/09]`: (i) **`bis\extrai_posteriores_pseob.py`** (roda em `/opt/lal_env` no WSL ou no `.venv` da ORDEM 013 §5 — nunca no Python do sistema) lê os `.h5` pSEOB (metafiles GWTC-5.0/GWTC-3; GW250114) e grava **`POSTERIORES_PSEOB_<catálogo>.npz`** (ou `.json`, dito) com as **amostras completas** por evento — `domega220`, `dtau220`, `dtau440` (onde existe), massa e spin do remanescente, redshift, os limites do prior uniforme — **nunca só quantis** (o `C4_CATALOG_220.json` traz só q05/q50/q95 e não serve de fonte: E2.2/E5.1), com o sha256 de cada `.h5` de origem e do próprio extrato num `MANIFESTO_POSTERIORES_<catálogo>.json`; (ii) **`tgl_ringdown_ampliacao.py`** (numpy puro; β em runtime; lê **só** o extrato (i), o registro E2 e o `NUISANCE_V1.json`; emite o veredito da matriz; **recusa rodar** sem o hash do registro ou se algum sha256 do manifesto não bater), com testes de unidade e a ficha de aproveitamento. **Um rito novo entra no `um.py` pela gerência**, depois da auditoria; a bancada não toca no canônico. Até o GWTC-6, o rito emite **`AWAITING_DATA`** com o N_alvo e o gate impressos.
- **Aceitação:** o módulo (ii) importa apenas numpy/json/hashlib (a guarda de E2 cobre também (i)); o extrato de um catálogo já público (calibração, NÃO-CEGO) reproduz os quantis do `C4_CATALOG_220.json` por evento (diferença dita); nenhum posterior publicado depois do hash do registro E2 é extraído antes do recibo do registro.

## Fontes
- `…\bis\ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md` l.169, l.195, l.207.
- `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013_confrontacao_do_ringdown.md` l.307, l.312.
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\catalog_220_readout.py` l.15, l.44, l.57-58; `C4_CATALOG_220.json` (estrutura lida por script).
- `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` (grep h5py: zero importações).
