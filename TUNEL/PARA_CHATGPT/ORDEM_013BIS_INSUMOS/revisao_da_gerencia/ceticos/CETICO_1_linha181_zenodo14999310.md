# CÉTICO 1 — achado da lente regua_hashes_casa, ORDEM 013-bis linha 181 (§4 E3), «Zenodo 14999310»

## Medição (22/09/2026, por script, só leitura)
- `grep -rl 14999310 bis/ auditoria/` → 4 arquivos: a própria ordem, `bis/parteB_ampliacao.md` (rascunho da ordem), e os dois arquivos da lente revisora (`fontes_dos_numeros.out`, `REVISAO_regua_e_hashes.md`).
- `grep -rl 14999310 bis/medir/` → **0**. `auditoria/` → 0. `RELATORIO_AUDITORIA_AO_OPERADOR_22SET.md` → 0. `PROMPT_CODEX_ORDEM_013BIS.txt` → 0. Bancada `Chatgpt/ORDEM_013_RINGDOWN` (md/json/txt/py) → 0.
- Único registro do fato na medição: `bis/medir/E_instrumento/MEDICAO_E.json:253` `aproximantes_falham_sem_LAL_DATA_PATH: [NRSur7dq4, SEOBNRv5HM_ROM, SEOBNRv5_ROM]`; `SINTESE.md:179` «LAL_DATA_PATH em cache/vendor: não testada». Nenhuma menção a record do Zenodo em E_instrumento.
- **Conclusão da medição: o número foi escrito de memória. O achado está certo na forma.**

## Tentativa de refutação — o número é verdadeiro?
Lido da API pública em 22/09 (`https://zenodo.org/api/records/14999310`): título «LALSuite waveform data», DOI 10.5281/zenodo.14999310, publicado 10/03/2025, 87 arquivos (~18,8 GB). Em `/files`: `NRSur7dq4_v1.0.h5` 17.489.768 B (md5 ec4a0a9c…), `NRSur7dq4Remnant_v1.0.h5` 130.964.640 B, `SEOBNRv5ROM_v1.0.hdf5` 439.382.784 B (md5 d402120d…), `SEOBNRv5HMROM_v1.0.hdf5` 2.196.668.728 B (md5 dc6253d8…). O record existe e contém exatamente os dados dos aproximantes que falham na MEDICAO_E.

**Veredito: refutado = false.** A memória acertou, mas a régua n.2 não é sobre acertar — é sobre não escrever número sem leitura por script. A ordem, imutável depois de publicada, carregaria um número sem fonte na cadeia de medição. Gravidade mantida em IMPORTANTE (número sem fonte; não induz erro de física, não decide nada do operador). A correção proposta pela lente («record a localizar pela API») ficou aquém: o record já foi lido; a correção final registra a fonte, a data, os tamanhos e o que segue não testado.

## Correção FINAL (substituir na linha 181 o parêntese «(LAL_DATA_PATH; dados públicos Zenodo 14999310, instaláveis em pasta própria — não testado)»)
`(LAL_DATA_PATH; os dados dos aproximantes são públicos no Zenodo — record 14999310, «LALSuite waveform data», 87 arquivos, com NRSur7dq4_v1.0.h5 17.489.768 B, SEOBNRv5ROM_v1.0.hdf5 439.382.784 B e SEOBNRv5HMROM_v1.0.hdf5 2.196.668.728 B `[REAL — lido da API zenodo.org/api/records/14999310/files em 22/09; md5 do Zenodo não conferido em disco]`; instaláveis em pasta própria via LAL_DATA_PATH — instalação e carga **não testadas** `[OPEN]`)`
