# Errata ao lado R3 — codex-gerente-tgl / atrator_sources

R2 também recusou antes de construir matrizes: o leitor de bytes preservou CRLF, e a regex ancorada aceitava apenas LF. R3 acrescenta `\r?` antes de `$`; o original não é reencodado nem alterado. Mantidos a unicidade da linha, o parse literal seguro e a conferência com o alpha selado. Critérios e entradas científicas inalterados; não houve resultado numérico visto nas R1/R2.
