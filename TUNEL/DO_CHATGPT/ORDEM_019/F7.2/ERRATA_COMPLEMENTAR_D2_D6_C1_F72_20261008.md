# F7.2 — complemento aditivo D2–D6 da c1

[REAL documental, 08/10/2026] O Nós vivo (`consultar.py --unidade F7.2`) localiza a tabela por canal, o canal de neutrinos de junho (`n = −2`) e a v369 de relógios. A auditoria c1 `AUDITORIA_F7_2_C1_a91f9500.md` conferiu os 17 pinos da camada anterior e classificou D2 e D3 como feitos, D4 como apenas textual, D5 como parcial e D6 como pendente. Este complemento mantém os originais pinados.

## D2 — V2 já corrigida ao lado

[REAL] A leitura vigente do `V2_STAGING/README_V2_STAGING.md`, de `V2_STAGING/STAGING_RECEIPT_V2_ERRATA_AO_LADO_20261008.json` e de `V2_STAGING/ERRATA_CABECALHO_TABELA_V2_20261008.md` corrige o estado histórico «implantação pendente»: a V2 foi instalada em disco sem ato prévio e ratificada a posteriori pela c1. A tabela V2 e o recibo V2 originais seguem pinados. O MCP não foi recarregado.

## D3 — âncora da Eq. (6)

[KNOWN — Beccaria–Ternes, arXiv:2606.13362v1] A Eq. (6) está em §III.B, p. 3 do PDF. A Eq. (13) está em §IV.B, p. 5, e a Tabela I na p. 7. A numeração «§IV.2» na LITERATURA é a da versão HTML e se refere à seção dos resultados, não à Eq. (6). `V3_STAGING/ERRATA_TABELA_V3_ANCORA_E_ESTADO_20261008.md` e `ERRATA_ANCORAS_JUNO_REF72_E_ESTADO_F72_20261008.md` já trazem essa leitura. A tabela V3 e a cópia na Bancada mantêm os bytes `sha256=b97f24ae225901dbb4d0c1f430f9dd4ce4bba17015e7249f407af23110d05bfb`.

## D4 — referência [72] sob custódia

[REAL — custódia local; KNOWN — conteúdo da fonte] O PDF do artigo JUNO cita na referência [72], p. 10, Esteban, Gago, Gonzalez-Garcia e Zapata, *Exploring neutrino loss with diffuse astrophysical neutrino fluxes*, arXiv:2605.13955. O PDF público v1 do arXiv, submetido em 13/05/2026, foi guardado em `fontes_literatura_r1/` com `sha256=cc86bd94a0474166e99a9a3c6f440e33eb72b90fc98eb7b26e0e8120a3feca33`; o recibo é `REF72_CUSTODY_F72_20261008.json`. A Tabela I, p. 8, trata da atenuação de fluxo em IceCube HESE sob escolhas de fonte e energia. Esse `γ₀` de perda de neutrinos não é o `γ₂₁ = γ₃₁` de dephasing sem perda da linha JUNO. Não se infere limite de `τ★` da TGL; `τ★_limite = null` [OPEN].

## D5 — tabela V3 e manifesto em staging

[REAL] Onde a tabela V3 herdou «esta tabela V2 foi preparada em sandbox», leia-se: **a tabela V3 foi preparada em staging; as 26 fontes foram copiadas para a Bancada e ratificadas a posteriori pela c1; o canal V3 segue sem instalação e sem recarga do MCP**. O alvo pinado e esta correção estão ligados por `V3_STAGING/MANIFESTO_ERRATA_TABELA_V3_D5_20261008.json`, que permanece em staging. A ratificação consta em `RECIBO_RATIFICACAO_COPIA_R8_C1_20261008.json`, `sha256=47be5f09e983dd091cb4782e458101d553d2e54125ba75ec1fbcb47405b45044`. A cópia R8 foi aditiva e inerte na aferição c1; isso não autoriza nova gravação na Bancada.

## D6 — autoria da mensagem

[REAL documental] No parágrafo «Anomalia de referência» de `LITERATURA_POS_JUNHO_F7_2_20261008.md` e de sua cópia V3, onde se lê «mensagem do operador», leia-se **despacho da gerência c1 ao Codex**. A indicação do caminho `AUDITORIA_F7_2_C1_20261007.md` veio da c1; o relatório efetivamente lido tem sufixo `aed6e453`. Não atribuir ao operador o texto da gerência.

## Estado operacional e escrituração

[REAL — decisão c1] A frase da camada anterior de que a ratificação da cópia R8 «segue pendente» foi superada pelo evento 313 e pelo recibo c1 acima. Vale esta errata para `V2_STAGING/README_V2_STAGING.md`, `V2_STAGING/STAGING_RECEIPT_V2_ERRATA_AO_LADO_20261008.json`, `ERRATA_TABELA_V3_ESTADO_20261008.md`, `ERRATA_ANCORAS_JUNO_REF72_E_ESTADO_F72_20261008.md` e o registro histórico do mapa seq 850. O mapa e as superfícies de memória requerem lançamento próprio ao lado pela gerência da unidade; este arquivo não os altera.

[REAL — limite] Esta camada só cria arquivos no túnel. A tabela V3 pinada, a cópia na Bancada, os módulos, o MCP, `um.py`, os scripts de junho e o gate não foram alterados. Os resultados de modelos externos não são confirmação física.
