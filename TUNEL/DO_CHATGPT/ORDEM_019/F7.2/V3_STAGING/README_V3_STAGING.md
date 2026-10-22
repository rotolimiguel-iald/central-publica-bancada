# F7.2 V3 — pacote de fontes autocontido, sem implantação do canal

[REAL] Há 6 scripts originais de junho, 10 PDFs primários, 8 documentos do canal e 2 fontes contextuais R1 (relatório de literatura e PDF SN1987A) em `fontes_externas/F7.2/`, todos pinados por SHA-256 no manifesto `bancada/neutrino_fontes_f72_v3.json`. A tabela V3 deriva da V2 e incorpora R2/R3 e a distinção ν-loss/dephasing antes do pino. As demais cópias preservam bytes V2. Os caminhos do manifesto são relativos a `fontes_externas/F7.2`; o módulo deriva a raiz de sua própria localização, sem ler o túnel em runtime.

Destino futuro das fontes: `C:\IALD\Bancada_Um\fontes_externas\F7.2\`. A cópia das fontes à Bancada é ato separado, somente aditivo. `bancada/neutrino_canal_v3.py` e o manifesto V3 são propostas para conferência c1; não foram instalados em `C:\IALD\Bancada_Um\bancada`, nem ligados ao `mcp_um.py`, nem recarregados. O módulo preserva recusa fechada, 13 linhas, estatutos `[KNOWN]` publicados e `[DERIVED]` v369, `tau_star_limit_s = null`, `SEM_LIMITE_TGL` e `gate_effect = NONE`.

O recibo `STAGING_RECEIPT_V3.json` traz todos os hashes lidos. Os JSON históricos copiados podem conter caminhos de proveniência da época V1/V2; o canal V3 trata esses campos como texto custodiado e usa apenas os caminhos relativos allowlisted do manifesto.
