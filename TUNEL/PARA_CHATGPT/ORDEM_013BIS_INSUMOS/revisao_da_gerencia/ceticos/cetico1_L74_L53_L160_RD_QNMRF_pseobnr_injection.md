# CÉTICO 1 — achado «RD.tar.gz / QNMRF.tar.gz não estão em disco; pseobnr_injection nunca extraído» (l.74, l.53, l.160)

Veredito: **refutado = false** (o achado está certo em todos os números; gravidade mantida em IMPORTANTE).

## O que a ordem diz (lida com numeração)
- l.53: «Nenhum strain novo é lido. **Tudo o que é número já existe em disco ou se recalcula em segundos.**» (regra geral da Parte A)
- l.74 (F2, Parte A): «`RD.tar.gz` e `QNMRF.tar.gz` listados (`tar -tzf`) com sha256; a pasta `pseobnr_injection/` do 17018009 listada.»
- l.160 (E1.3, Parte B/MB1): «abrir `pseobnr_injection/` do Zenodo 17018009 (listado na ORDEM 013 §1.3, nunca aberto) e o `RD.tar.gz` do 21454847 (segundo método, 6 eventos) … Se não houver injeções utilizáveis: NÃO PAGO, dito.»
- l.235–236 (global): downloads em `cache\` com sha256 no `MANIFESTO_DOWNLOADS.json` + licença por arquivo; «Sem rede: `ENTREGA_013BIS_BLOQUEIO_rede.md` com URLs e tamanhos.»

## Medido em disco (bancada só-leitura, 22/09/2026)
- `cache\public\21454847\`: `pSEOB.tar.gz` (711.331.923 B), `record.json`, `archive_index.json`, `extraction_receipt.json`, `extracted\pSEOB`. **Sem `RD.tar.gz`, sem `QNMRF.tar.gz`.**
- `record.json` (files): pSEOB 711.331.923 · FTI_TIGER 2.192.682 · **QNMRF 1.214.239** · POL 14.199 · README 804 · **RD 415.283.962** (md5 240bae5d…) · RES 91.084. Licença `cc-by-4.0`; publicado 2026-07-22 (anterior ao corte de 22/09 da l.177 — o download não fere a cláusula do registro).
- `cache\MANIFESTO_DOWNLOADS.json` existe (com 8 backups) — a rota de download com manifesto já está montada.
- `cache\public\17018009\archive_index.json`: `pseobnr_injection/` = README.md (26 B), kde_data_injection_no44.dat (50.444 B), kde_data_injection_44.dat (50.500 B), posterior_samples.h5 (64.331.592 B). `extraction_receipt.json`: **0** ocorrências de `pseobnr_injection` → nunca extraído. Licença do record: `mit-license`.
- Extração de leitura (para o scratchpad, `tar --force-local … -O`, 16,6 s): README = «* PESummary samples from: » (26 B, truncado na origem); cada `.dat` = KDE 1-D de **1000 linhas** (x, densidade), x começa em −0,80 → a marginal de δτ̂ de **UMA** injeção, com/sem o 440. **Não há eixo de SNR.** Um `posterior_samples.h5` = um posterior.
- A própria medição da gerência já sabia: `bis\medir\B_catalogos\FRENTE_B_RESULTADO.md` l.11 «`RD.tar.gz` 415.283.962 B (não baixado pela bancada)»; auditor 6 (`auditoria\aud_6.txt` l.64–67, 142) pediu «baixar o RD.tar.gz (ou justificar por escrito)». A ordem incorporou o FIX do auditor em F2 mas manteve a frase da l.53, que o contradiz.

## Por que não refuto
1. l.53 vs l.74 é inconsistência interna medida: listar com sha256 exige o artefato em disco (régua nº 2: hash lido do arquivo, nunca do record — e o record só dá md5). São ~416,5 MB de rede dentro de uma Parte que se declara «tudo em disco». A bancada pode (a) pular F2 citando a l.53 ou (b) baixar em silêncio fora do manifesto. As duas são erros que a ordem induz.
2. `pseobnr_injection/` não pede rede — está no tarball já em disco (1.671.496.586 B) — mas «listada» (l.74) não é «extraída e lida» (l.160); a ordem deve dizer que é extração local.
3. E1.3 já traz o «NÃO PAGO, dito» genérico, mas promete «curva c(SNR) da própria LVK, por injeção». Medido: é UM ponto (uma injeção, duas variantes de modo). Sem a frase, a bancada pode interpolar um ponto e um controle sintético como «curva» — exatamente o preenchimento que a régua proíbe.

Não é BLOQUEANTE: a l.235–236 tornam o item executável (download permitido + bloqueio sem rede). É IMPORTANTE porque a l.53 é falsa como está e a l.160 promete o que o dado não tem.

## Correção FINAL (texto pronto, substituição exata)

**l.53**, trocar «Tudo o que é número já existe em disco ou se recalcula em segundos.» por:
«Tudo o que é número já existe em disco ou se recalcula em segundos — **exceto os dois tarballs de F2 (`RD.tar.gz` 415.283.962 B e `QNMRF.tar.gz` 1.214.239 B do Zenodo 21454847), que NÃO estão em disco e pedem download** (regra da §5: `cache\`, sha256 no `MANIFESTO_DOWNLOADS.json`, licença CC BY 4.0 lida do record).»

**l.74**, trocar «`RD.tar.gz` e `QNMRF.tar.gz` listados (`tar -tzf`) com sha256; a pasta `pseobnr_injection/` do 17018009 listada.» por:
«`RD.tar.gz` e `QNMRF.tar.gz` (21454847) **NÃO estão em disco** `[REAL — cache\public\21454847 tem só pSEOB.tar.gz]`: baixar para `cache\public\21454847\` (md5 do record conferido; sha256 lido do arquivo, no `MANIFESTO_DOWNLOADS.json` com licença CC BY 4.0) e listar (`tar -tzf`); **sem rede → `ENTREGA_013BIS_BLOQUEIO_rede.md` com as duas URLs e tamanhos, e o item fica NÃO PAGO na Parte A, pago em E1.3 (MB1)**. A pasta `pseobnr_injection/` do 17018009 (4 membros: README.md 26 B, kde_data_injection_no44.dat, kde_data_injection_44.dat, posterior_samples.h5 64.331.592 B) **extraída do tarball já em disco, sem rede**, com o `extraction_receipt.json` atualizado ao lado (hoje: 0 ocorrências).»

**l.160**, trocar o item 3 inteiro por:
«3. **A injeção da própria LVK (um ponto, não uma curva):** abrir `pseobnr_injection/` do Zenodo 17018009 (nunca aberto; extração local, sem rede) — é **UMA injeção** `[REAL — README de 26 B truncado; dois KDE 1-D de 1000 pontos em δτ̂, com e sem o 440; um posterior_samples.h5]`: ler onde ela cai em (δf̂, δτ̂) com/sem o 440 e registrar como **um ponto de viés na sua SNR** (dita, lida do posterior). O `RD.tar.gz` do 21454847 (segundo método, 6 eventos; download por §5) entra como controle de método, não como injeção. **A curva c(SNR) da LVK fica NÃO PAGA, dita** — o ponto NÃO se interpola com o controle sintético do item 4; c(SNR) sai só de E3.»
