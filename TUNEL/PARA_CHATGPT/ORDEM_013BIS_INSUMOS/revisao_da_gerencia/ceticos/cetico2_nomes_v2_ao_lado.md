# CÉTICO 2 — achado «artefatos v2 ao lado sem nome fixado» (ORDEM 013-bis l.62, l.63, l.88, l.113)

**Veredito: refutado = false. Gravidade mantida: IMPORTANTE.**

## O que medi (22/09/2026, só leitura na pasta da bancada)

1. A ordem, l.53: «correção ao lado, nunca por cima (adendo datado, com hash novo; a versão anterior fica, **com backup de bytes**)». A frase «com backup de bytes» é a mesma linguagem da régua 6 do `TUNEL_PROTOCOLO.md` (l.71): «Backup de bytes antes de tocar arquivo próprio já entregue; `temp → confere → substitui`». A régua do túnel prescreve **substituição no lugar com .bak** — o oposto de «ao lado». A ordem não dá nome ao arquivo v2 em nenhuma das três ocorrências (l.62 «arquivo novo, versão 2»; l.63 «v2 ao lado»; l.88 «v2 ao lado»), nem em §6 l.235 («os adendos da Parte A ao lado dos originais»).
2. A prática já instalada da bancada é exatamente a que o achado teme. Na pasta `ORDEM_013_RINGDOWN\` há 15 arquivos `*.bak_20260921_*` de sobrescrita no lugar, entre eles **`C5_FISHER.json.bak_20260921_200857_779037`** (262.865 bytes, sha16 `b9837d5ead8b0500`) ao lado do `C5_FISHER.json` atual (264.414 bytes, sha16 `71189d65f52d3530`): o C5_FISHER **já foi regravado por cima uma vez**, com backup. Sem nome fixado, a leitura natural da bancada para «C5_FISHER.json v2 ao lado» é repetir o gesto — e a ENTREGA dirá «ao lado» apontando um `.bak`.
3. F8 (l.113) lista como critério de término só `ENTREGA_013_M1…M6`, `ENTREGA_013_ERRATA_contrato`, as 8 fichas e `PORTAO_DO_PODER_013.json`. Os três JSON v2 (C0, C1, C5), `C0_ADENDO_FRASES_PUBLICAS.md`, `C2_ADENDO_OBSERVAVEL.md`, os dois `C4_ADENDO_*.md`, `C6_ADENDO_REALIZADO.json` e `C5_ANEXO_PROCESSOS_ENCERRADOS.json` ficam fora do término: a bancada pode declarar MA sem eles e estar formalmente em dia com l.113.
4. Os hashes v1 lidos hoje (referência para o recibo da gerência; a v1 vinculante é a que existir ao abrir a ordem):
   - `C0_AUDITORIA.json` 24.269 bytes, sha16 `f0009e1194282434`
   - `C1_LEITURAS.json` 29.800 bytes, sha16 `333a9d8b7d650aff`
   - `C5_FISHER.json` 264.414 bytes, sha16 `71189d65f52d3530`

Nenhum auditor (aud_1..6) fixou nome; aud_1 l.99/166 só diz «regenerar C0_AUDITORIA ... com erratas ao lado». Logo a lacuna é da ordem, não herdada.

## Por que não é gosto

Um nome de arquivo é o que o script de auditoria da gerência abre; sem ele, a conferência «v1 intacta (sha) + v2 com supersedes» não é automatizável e a bancada tem duas leituras legítimas do mesmo comando (novo arquivo × substituir-com-.bak). Isso é «ambiguidade que a bancada pode explorar» = IMPORTANTE. Não é BLOQUEANTE: a ordem é executável e não induz erro de física.

## Correção FINAL (texto exato)

**(1) Substituir a l.53 por:**

> Regra geral da Parte A: **correção ao lado, nunca por cima**. Versão nova de um artefato já entregue = **arquivo novo `<nome>_v2.<ext>` na mesma pasta** (ex.: `C0_AUDITORIA_v2.json`), com os campos `supersedes` (o nome da v1) e `supersedes_sha256` (lido por script); **a v1 fica intacta, byte a byte** — o seu sha256 vai na ENTREGA e a gerência o confere. Sobrescrever a v1 e guardar `.bak` **não é ao lado** (a régua 6 do túnel, `temp → confere → substitui`, vale só para arquivo ainda NÃO citado em entrega; todo artefato citado em ENTREGA ou nesta ordem é imutável). Adendos em Markdown levam data e o sha256 do arquivo que corrigem na 1ª linha. **Nenhum job novo de calibração** nesta parte. Nenhum strain novo é lido. Tudo o que é número já existe em disco ou se recalcula em segundos.

**(2) Na l.62, trocar** «regeneração de `C0_AUDITORIA.json` **ao lado** (arquivo novo, versão 2, com `supersedes` e o sha da v1)» **por** «**`C0_AUDITORIA_v2.json`** (regra da l.53; `C0_AUDITORIA.json` intacto)».

**(3) Na l.63, trocar** «`C1_LEITURAS.json` v2 ao lado:» **por** «**`C1_LEITURAS_v2.json`** (regra da l.53; `C1_LEITURAS.json` intacto):».

**(4) Na l.88, trocar** «`C5_FISHER.json` v2 ao lado:» **por** «**`C5_FISHER_v2.json`** (regra da l.53; `C5_FISHER.json` intacto — o `.bak_20260921_200857` existente mostra que ele já foi regravado por cima uma vez; não se repete):».

**(5) Substituir a primeira frase da l.113 (F8) por:**

> A Parte A termina quando existirem `ENTREGA_013_M1 … M6`, `ENTREGA_013_ERRATA_contrato`, as 8 fichas `REAPROVEITAMENTO_C0…C7.md`, `PORTAO_DO_PODER_013.json` **e os adendos nomeados: `C5_ANEXO_PROCESSOS_ENCERRADOS.json`, `C0_ADENDO_FRASES_PUBLICAS.md`, `C0_AUDITORIA_v2.json`, `C1_LEITURAS_v2.json`, `C2_ADENDO_OBSERVAVEL.md`, `C4_ADENDO_DTAU_POSITIVO.md`, `C4_ADENDO_GWTC3_18_vs_10.md`, `C5_FISHER_v2.json`, `C6_ADENDO_REALIZADO.json` — cada um com sha256 na ENTREGA do marco correspondente e as v1 com o sha256 de antes da ordem conferido igual**, cada uma com o contrato do túnel, e a bancada **PARA** e espera o recibo da gerência.

(O resto de F8 fica como está.)
