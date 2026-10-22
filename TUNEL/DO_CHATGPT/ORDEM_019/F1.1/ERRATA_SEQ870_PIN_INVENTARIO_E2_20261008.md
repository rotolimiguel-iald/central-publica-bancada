# F1.1.E2 — alcance do pino do INVENTARIO na seq 870

08/10/2026 — Em nome de codex-gerente-tgl, sob reivindicação F1.1.E2 (evento 417). Errata documental ao lado da F1.1.E1 FECHADA; responde à ressalva da auditoria c1 `2fbbc80488dacef24a0c6096f68918bd3923f6e14e45978fcfa50fbd9148dcb4`. A F1.1 principal permanece FECHADA.

[REAL — bytes medidos] Na seq 870 (`16668014009b3be800244c2ad475e6751a211e6456688f87869cf3c15e2b6992`), o artefato `INVENTARIO.md` de 33179 bytes, SHA-256 `9f8c891810c2da3160bd88f96fd7514d8666df260c3cdcc997da94073d3fb10e`, identifica o **estado completo do inventário após a E1**. Esse pino, tomado isoladamente, não é o identificador da sexta camada de 4533 bytes.

[REAL — bytes medidos] A camada isolada é `ERRATA_LEITURA_R2_R5_E1_20261008.md`, SHA-256 `cdea25a6e83ca441e5a08679e2c13d02b4b690e5f92eeaaa6a04384a9749e541`. A seq 870 **também a pina separadamente** como artefato. O backup imediato do inventário, `INVENTARIO.md.bak_20261008_113445`, tem 28646 bytes e SHA-256 `808a79553527d1d726d989aab73b8e24369cc7c88666a8c3e5b40165da8df56d`. Foi verificada a igualdade exata de bytes `INVENTARIO.md = backup || camada E1` (28646 + 4533 = 33179); o recibo E1 tem SHA-256 `9298026250360d5c1a41356989ded9d516fa06e6e8d1a3fa8be2cc91e34aef76`.

Esta correção delimita o alcance do pino do INVENTARIO na seq 870. Não modifica a classificação O16, a camada E1, o inventário, o kernel, a memória, a Bancada ou o gate; não reabre F1.1 nem F1.1.E1.
