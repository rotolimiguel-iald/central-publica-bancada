[REAL] Auditoria independente do banco sintético T10-C, 27/09/2026.

Fonte: `ORDEM_013_RINGDOWN/bis/015/t10/T10_C_BANK_AUDIT.json`, SHA-256 `182bc480299ed40c786a2905e6dbadab728709b399909173adbaa1b0ceabcc2a`. Manifesto do banco: `T10_C_BANK_RESULT_v4.json`, SHA-256 `05eb55665a1f8134bc88ca4a6361dd198e28b0c8db4ed0d52fe5396352c04216`.

Foram conferidos 10/10 arquivos, em cinco SNR-alvo (19,1; 17; 15; 13; 12) e duas famílias (SEOBNRv4HM, IMRPhenomXPHM). Cada sinal somado ao ruído fecha numericamente com o strain armazenado, com erro máximo entre 1,88×10⁻³⁷ e 1,50×10⁻³⁶. A geração foi LAL direta. A comparação no primeiro bin com os controles anteriores de C5 via PyCBC deixou resíduo relativo de forma de onda 0,00685594 (EOB) e 0,02322631 (XPHM). Assim, **não se reivindica equivalência exata** entre as duas interfaces; a diferença é um sistemático de implementação a carregar numa eventual recuperação.

O banco contém dez injeções sintéticas, sem recuperação PE. Não fornece dispersão de injeções, σ(c), significância conjunta, evidência da natureza ou movimento de gate. O observável que permanece aberto é uma recuperação de δf̂/δτ sob as duas famílias e ruído qualificado. O T10-A existente é 220 apenas; T10-A′ é posto espectral, sem posterior multimodo. O T10-B encontrou covariância H1 acima do limiar pré-registrado; a regularização posterior é `[INPUT]`, não qualificação automática do ruído real.

Reprodução: `python ORDEM_013_RINGDOWN/bis/015/t10/audit_t10_c_bank.py` a partir da raiz `Chatgpt` (lê o banco existente; nenhum `um.py`). A cadeia de hash dos arquivos individuais está no JSON da auditoria.
