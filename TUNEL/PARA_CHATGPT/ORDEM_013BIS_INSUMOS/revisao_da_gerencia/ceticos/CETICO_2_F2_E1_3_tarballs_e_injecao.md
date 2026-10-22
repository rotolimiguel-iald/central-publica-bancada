# CÉTICO 2 — achado «RD.tar.gz / QNMRF.tar.gz não em disco; pseobnr_injection não extraída» (ORDEM 013-bis l.53, l.74, l.160)

Data: 22/09/2026. Lente: cético (tentativa de refutação). Veredito: **NÃO REFUTADO** — gravidade **IMPORTANTE** mantida.

## O que a ordem diz (lido com numeração)

- l.53: «**Nenhum job novo de calibração** nesta parte. Nenhum strain novo é lido. Tudo o que é número já existe em disco ou se recalcula em segundos.»
- l.74 (F2): «`RD.tar.gz` e `QNMRF.tar.gz` listados (`tar -tzf`) com sha256; a pasta `pseobnr_injection/` do 17018009 listada.»
- l.160 (E1.3): «abrir `pseobnr_injection/` do Zenodo 17018009 (listado na ORDEM 013 §1.3, nunca aberto) e o `RD.tar.gz` do 21454847 (segundo método, 6 eventos) […] Se não houver injeções utilizáveis: NÃO PAGO, dito.»

## Medido por script (bancada só-leitura; nada escrito lá)

1. `cache\public\21454847\`: contém **só** `pSEOB.tar.gz` (711.331.923 B; sha16 `ee1d64487597132f`), `record.json`, `archive_index.json`, `extraction_receipt.json`. `ls | grep -c "RD.tar.gz\|QNMRF"` = **0**. O `record.json` lista 7 arquivos: pSEOB 711.331.923 B; FTI_TIGER 2.192.682; **QNMRF 1.214.239**; POL 14.199; README 804; **RD 415.283.962**; RES 91.084 (md5 no record). ⇒ `tar -tzf` de RD/QNMRF exige **download** (≈ 0,42 GB), o que contradiz a l.53 literalmente.
2. `cache\public\17018009\archive_index.json` (3.712 membros; sha256 do tarball `18d740c8…`): `pseobnr_injection/` tem 4 membros regulares — `README.md` **26 B**, `kde_data_injection_no44.dat` 50.444 B, `kde_data_injection_44.dat` 50.500 B, `posterior_samples.h5` 64.331.592 B. `grep -c pseobnr_injection extraction_receipt.json` = **0** nas três pastas (17018009, 17461225, 21454847); `find -iname "*pseobnr_injection*"` na pasta da bancada = vazio ⇒ **não extraída**. Extração é local (tarball já em disco, sem rede).
3. Conteúdo (extraído para o meu scratchpad, `cet2_injecao\`): README = `* PESummary samples from: ` (26 B, truncado na fonte — nada diz). Os dois `.dat` são KDEs 1-D em grade de 1000 pontos: `44`: x ∈ [−0,8; 0,8], moda 0,380, ∫ = 1,000; `no44`: x ∈ [−0,8; 1,0], moda −0,007, ∫ = 1,001. Ou seja: **UMA injeção**, recuperada com e sem o modo 44 — um ponto (SNR fixo), não uma curva c(SNR).

## Tentativa de refutação e por que falha

- «A l.235/236 já permite downloads em `cache\` e prevê `ENTREGA_013BIS_BLOQUEIO_rede.md`» — verdade, mas é regra geral da ordem; a **l.53 é regra específica da Parte A** e afirma que tudo já está em disco. A bancada, lendo a Parte A, tem duas frases contraditórias sobre o mesmo item; a ambiguidade é explorável (pular F2 «porque a Parte A não baixa», ou baixar e ferir a l.53). Não refuta.
- «E1.3 já tem o escape "NÃO PAGO, dito"» — tem, mas a frase «curva c(SNR) da própria LVK» sugere que existe uma curva a ler; o que existe é um ponto. A ordem deve dizer que é um ponto, para que o «NÃO PAGO» da curva não apague o ponto que existe (viés a SNR do GW250114 com/sem 44 — é dado útil para E4/440).
- A ORDEM 013 l.299–302 já dizia «pSEOB 0,71 GB + RD 0,42 GB» e «baixar de zenodo.org é permitido e necessário»; a bancada baixou só o pSEOB (FRENTE_B_RESULTADO.md l.11: «RD.tar.gz … não baixado pela bancada»). A gerência sabia disso ao escrever a 013-bis e mesmo assim escreveu a l.53 — inconsistência interna, não questão de gosto.

## Gravidade

IMPORTANTE (inconsistência interna + item de Parte A inexecutável sem rede; não é erro de física nem fabricação). Não BLOQUEANTE: a ordem tem o escape de rede (l.236) e o «NÃO PAGO» (l.160); o dano é a bancada explorar a ambiguidade.

## Correção FINAL (texto exato)

- **l.53**, substituir a última frase por: «Tudo o que é número já existe em disco ou se recalcula em segundos — **exceto os dois tarballs de F2 (`RD.tar.gz` 415.283.962 B e `QNMRF.tar.gz` 1.214.239 B do 21454847, tamanhos lidos do `record.json`), que NÃO estão em disco e pedem download novo em `cache\`**.»
- **l.74**, substituir o trecho «`RD.tar.gz` e `QNMRF.tar.gz` listados (`tar -tzf`) com sha256; a pasta `pseobnr_injection/` do 17018009 listada.» por: «`RD.tar.gz` (415.283.962 B) e `QNMRF.tar.gz` (1.214.239 B) do 21454847 **não estão em disco** `[REAL — só `pSEOB.tar.gz` em `cache\public\21454847\`]`: baixar para `cache\` (sha256 + md5 conferido com o `record.json` + licença CC BY 4.0 no `MANIFESTO_DOWNLOADS.json`) e listar (`tar -tzf`); sem rede → `ENTREGA_013BIS_BLOQUEIO_rede.md` e o item fica NÃO PAGO na Parte A, pago em MB1. A pasta `pseobnr_injection/` do 17018009 (4 membros: `README.md` 26 B, `kde_data_injection_no44.dat`, `kde_data_injection_44.dat`, `posterior_samples.h5` 64.331.592 B) **está no tarball em disco e nunca foi extraída** (0 ocorrências no `extraction_receipt.json`): extrair para `cache\public\17018009\extracted\`, sem rede, e listar com sha256.»
- **l.160**, substituir por: «**A curva c(SNR) da própria LVK, por injeção:** abrir `pseobnr_injection/` do Zenodo 17018009 (listado na ORDEM 013 §1.3, nunca extraído) — **é UMA injeção** (um `posterior_samples.h5` + dois KDEs 1-D de 1000 pontos, com e sem o modo 44) `[REAL — lido do índice do tarball]`, logo um **ponto** de viés ao SNR do GW250114, não uma curva; registrar o ponto (com e sem 44) e dizer **NÃO PAGO para a curva** — e o `RD.tar.gz` do 21454847 (segundo método, 6 eventos; download de F2): o que há de injeção, o que dá para ler de viés versus SNR sem PE nova. Se não houver injeções utilizáveis além desse ponto: NÃO PAGO, dito.»

Arquivos: este registro e `cet2_injecao\` (README + 2 .dat extraídos; o .h5 não foi extraído).
