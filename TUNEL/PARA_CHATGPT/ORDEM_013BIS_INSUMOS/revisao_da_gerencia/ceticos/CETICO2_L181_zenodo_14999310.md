# CÉTICO 2 — achado I6 (regua_e_hashes), ORDEM 013-bis L181, «Zenodo 14999310»

## Medição (22/09/2026)
- `grep -rn 14999310` em `bis/medir`, `bis/*.md`, `auditoria/`: 0 fontes (só a ordem, `parteB_ampliacao.md` e os arquivos do próprio revisor).
- `Grep 14999310` em `Chatgpt\ORDEM_013_RINGDOWN` (*.md/json/txt/py/yaml/cfg/sh): 0 arquivos.
- `MEDICAO_E.json:253-256` lista só `aproximantes_falham_sem_LAL_DATA_PATH: [NRSur7dq4, SEOBNRv5HM_ROM, SEOBNRv5_ROM]`; `SINTESE.md:179`: «Instalabilidade de ... LAL_DATA_PATH em cache/vendor: nao testada». Nenhum record.
- **Conclusão 1:** o número foi escrito sem fonte na medição → o achado procede (régua n.2).
- API Zenodo, por script (`zenodo_14999310_api.json`, `zenodo_14999310_files.json`): record 14999310 = **«LALSuite waveform data»**, DOI 10.5281/zenodo.14999310, 85 arquivos, 21,19 GB; contém `NRSur7dq4_v1.0.h5` (17.489.768 B, md5 ec4a0a9c…), `SEOBNRv5ROM_v1.0.hdf5` (439.382.784 B, md5 d402120d…), `SEOBNRv5HMROM_v1.0.hdf5` (2.196.668.728 B, md5 dc6253d8…). A busca `"LAL_DATA_PATH"` na API devolve só este record.
- **Conclusão 2:** o número está CERTO e cobre exatamente os três aproximantes que falham. O defeito é de proveniência/estatuto, não de valor. A correção do revisor («record a localizar pela API») ficou obsoleta: já localizado e medido.

## Veredito
refutado = false (o achado «sem fonte» é provado); gravidade IMPORTANTE mantida (número sem fonte numa ordem imutável); correção FINAL = manter o número com proveniência e estatuto.
