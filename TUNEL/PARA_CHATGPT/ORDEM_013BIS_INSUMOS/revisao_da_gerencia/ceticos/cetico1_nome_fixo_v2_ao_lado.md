# CÉTICO 1 — achado «v2 ao lado sem nome fixado» (ORDEM 013-bis l.62, l.63, l.88, l.113)

**Veredito: NÃO refutado. Gravidade mantida: IMPORTANTE.**

## O que a ordem diz (lido com numeração)
- l.53: «correção ao lado, nunca por cima (adendo datado, com hash novo; a versão anterior fica, com backup de bytes)».
- l.62: «regeneração de `C0_AUDITORIA.json` **ao lado** (arquivo novo, versão 2, com `supersedes` e o sha da v1)».
- l.63: «`C1_LEITURAS.json` v2 ao lado».
- l.88: «`C5_FISHER.json` v2 ao lado».
- l.67: «toda correção acima é adendo datado ao lado (v1 intacta, backup de bytes)».
- l.113 (F8): lista só `ENTREGA_013_M1 … M6`, `ENTREGA_013_ERRATA_contrato`, as 8 fichas e `PORTAO_DO_PODER_013.json`. Nenhum dos três v2 nem os adendos C4/C5/C6 entram no critério de término.
- l.235: «os adendos da Parte A ao lado dos originais» — sem nome.
- `TUNEL_PROTOCOLO.md`: grep por `supersede|_v2|versão|ao lado|nome fixo` devolve ZERO linhas — não há convenção de nome herdada do protocolo.

## O número que prova o risco (medido, só leitura, em `Chatgpt\ORDEM_013_RINGDOWN\`)
A bancada JÁ pratica «sobrescrever com backup» nos exatos arquivos que a ordem manda versionar ao lado:

| arquivo vivo | sha16 vivo | backup ao lado | sha16 do backup |
|---|---|---|---|
| `C5_FISHER.json` | `71189d65f52d3530` | `C5_FISHER.json.bak_20260921_200857_779037` | `b9837d5ead8b0500` |
| `C0_C3_checks.json` | `0592189981243c50` | `C0_C3_checks.json.bak_20260921_200857_809588` | `929b9306f92f32f0` |
| `C1_TABLES.json` | `bf5ac0d2dad2322a` | `C1_TABLES.json.bak_20260921_204634_110078` | `c84c2544bdc14f6d` |

Os hashes diferem: o arquivo de nome canônico foi **substituído** e a versão anterior sobrevive só como `.bak_<timestamp>`. Esse padrão satisfaz literalmente a l.53 («a versão anterior fica, com backup de bytes») e contradiz a l.67 («v1 intacta») — a ordem tem duas frases que a bancada pode ler de dois modos, e o modo que ela já usa é o que quebra a auditoria por nome (o sha da v1 citado nas ENTREGAs de 21/09 deixaria de bater com `C5_FISHER.json`). Além disso não há nenhum `*_v2*` nem `*supersed*` na pasta hoje: o nome é inteiramente livre.

## Por que IMPORTANTE e não BLOQUEANTE
A ordem é executável e não induz erro de física; o defeito é ambiguidade explorável + critério de término (F8) incompleto. Corrigível com uma frase na regra geral e uma lista em F8.

## Correção FINAL (texto exato)
**l.53, substituir por:**
Regra geral da Parte A: **correção ao lado, nunca por cima**. Versão nova de artefato já citado por sha = **arquivo novo `<nome>_v2.<ext>` na mesma pasta** (JSON: campos `supersedes` = nome da v1 e `supersedes_sha16`; `.md`: as duas linhas no cabeçalho), **a v1 intacta byte a byte — o sha da v1 conferido na ENTREGA. Sobrescrever o nome canônico com `.bak_*` ao lado NÃO é «ao lado»: é por cima** (é o padrão de 21/09 em `C5_FISHER.json`, `C0_C3_checks.json`, `C1_TABLES.json`, cujos `.bak_` já diferem do vivo). Adendos = `<alvo>_ADENDO_<assunto>.<ext>`, datados, com hash. **Nenhum job novo de calibração** nesta parte. Nenhum strain novo é lido. Tudo o que é número já existe em disco ou se recalcula em segundos.

**l.62:** «regeneração de `C0_AUDITORIA.json` **ao lado** (arquivo novo, versão 2, ...)» → «`C0_AUDITORIA_v2.json` **ao lado** (com `supersedes` e `supersedes_sha16` da v1)».
**l.63:** «`C1_LEITURAS.json` v2 ao lado:» → «`C1_LEITURAS_v2.json` ao lado:».
**l.88:** «`C5_FISHER.json` v2 ao lado:» → «`C5_FISHER_v2.json` ao lado:».

**l.113 (F8), substituir a primeira frase por:**
A Parte A termina quando existirem `ENTREGA_013_M1 … M6`, `ENTREGA_013_ERRATA_contrato`, as 8 fichas `REAPROVEITAMENTO_C0 … C7.md`, `PORTAO_DO_PODER_013.json`, `C5_ANEXO_PROCESSOS_ENCERRADOS.json`, `C0_AUDITORIA_v2.json`, `C0_ADENDO_FRASES_PUBLICAS.md`, `C1_LEITURAS_v2.json`, `C2_ADENDO_OBSERVAVEL.md`, `C4_ADENDO_DTAU_POSITIVO.md`, `C4_ADENDO_GWTC3_18_vs_10.md`, `C5_FISHER_v2.json`, `C6_ADENDO_REALIZADO.json` — cada um com sha256 na entrega que o cita, **com os originais v1 de nome canônico intactos (sha conferido)** — e a bancada **PARA** e espera o recibo da gerência.
