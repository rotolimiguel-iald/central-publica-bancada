# ORDEM_016_INSUMOS — o que há aqui e como ler

[REAL — pasta montada por script pela gerência em 23/09/2026; sha16 de cada arquivo em `MANIFESTO_INSUMOS.json`, gerado na montagem; conferir por script antes de usar. Nada se executa aqui dentro: copie para a sua pasta, troque os caminhos absolutos da sessão da gerência (os `…\scratchpad\…` citados dentro dos arquivos são efêmeros) e rode a cópia.]

**Ordem de leitura sugerida:** a ORDEM 016 inteira → a ORDEM 015 inteira (a Parte B) → `PROTOCOLO_ANTI_PAREDE.md` → `ESTADO_QG_v370.json` → `JA_EM_KERNEL.json` → `TETOS_PARTE_A.json` → a pasta do alvo em que estiver.

- `PROMPT_CODEX_ORDEM_016.txt` — o prompt fixo da missão (o operador o cola no Codex), byte a byte.
- `ORDEM_OPERADOR_VERBATIM_23SET_QG.md` — as falas do operador de 23/09 que regem esta ordem, verbatim.
- `PROTOCOLO_ANTI_PAREDE.md` — a regra vinculante (cópia de bytes do insumo da 015; nesta ordem a nota chama-se `ENTREGA_016_MEDIDA_<slug>.md`).
- `ESTADO_QG_v370.json` — a fronteira da QG lida do core v370 por script (remaining, identificações físicas, bandeiras gpf_/gpi_/qgf_, gate, selos, leitura da Testemunha).
- `JA_EM_KERNEL.json` — as âncoras «já em kernel — não refazer» (grep por script, arquivo:linha e sha16 do arquivo) e o pré-resolvido pela gerência nestes insumos.
- `TETOS_PARTE_A.json` — os tetos de horas de bancada por ramo (números da gerência [INPUT]) e as somas por alvo e total (por script).
- `ESTADO_RINGDOWN_LEITURAS.json` — as leituras do ringdown (registro V1 + C1_LEITURAS_v4), os N₉₀, o fator de Bonferroni e as identidades [DERIVED] do A-4k.6.
- `FONTES_DA_CASA.json` — as 34 fontes da 015 re-hasheadas + as fontes novas da 016 (sha16, bytes, sha256, mtime).
- `A0_JULGAMENTO_QG\` — o julgamento «a resposta à 015 resolve a QG?» (NAO_RESOLVE), os fatos e o core lidos, o relatório do juiz. **ERRATA AO LADO (gerência):** o «não começar agora (Q2/UV, transformada limitada)» e o «depois da 014» do julgamento ficam superados pela direção do operador de 23/09 («remonte a ordem toda»); na ORDEM 016 esses itens são o A-7 e o A-2.5, com teto.
- `A1_CONTRATO_V3\` — o contrato de tipo v3 e v3.1 de H2/H3 (os `.lean`, os logs, os manifestos, a mutação, os céticos das duas rodadas) e `RELATORIO_FINAL_DO_FLUXO_V31.json`. Sem `.olean` (dependem do caminho; o olean não é critério) e sem as corridas de mutação (regeneráveis pelos harness incluídos).
- `A2_W5_ANEXOS\` — os anexos Lean da frente W5 (a ponte do jato, o dente de fidelidade, a parede espectral, o brinquedo), a ponte do homônimo `boost4 = boostMat` do cético final, as sondas da frente W2 e `CETICO_FINAL_W5.json` (os defeitos E7–E10).
- `A2_A3_RETA_DE_LUZ\` — o julgamento da forma carregada da luz (a localização modular, as referências conferidas, os alvos A-2/A-3 com tetos), os `.lean` da reta de luz e os manifestos (os preprints não vêm: baixe pelo identificador e confira o sha256 em `MANIFESTO_FONTES_LITERATURA.json`).
- `A4_CIRCULO_KMS\` — o excerto do julgamento do Torus (só a ponte do círculo KMS; o setor neural omitido por ordem do operador) e a checagem sympy de Wick e da regularidade cônica.
- `A6_EQUACAO_DA_VERDADE\` — a receita do A-6 (o ADENDO 001, nunca publicado: leia com a tabela de correspondência da §5.A-6 da ordem), a pedra `V3_pre_resolucao_lean\TheEquationOfTruth.lean`, as medidas do redator (o auditor v2, as mutações C2, a variante só-Mathlib), a verificação independente V1, as âncoras V2, o verbatim do canal e a recompilação do cético (`CETICO_RECOMPILACAO\`).
- `PACOTE_FISICA_v370\` — o pacote para o projeto Física do operador (cópias de bytes do cânone v370 e dos artigos públicos), com `MANIFESTO_LOCAL.json`, `00_LEIA_PRIMEIRO_TGL_v370.md` e a `VARREDURA.json` da gerência. **A bancada só faz o upload** (salvo veto do operador); o conteúdo não vai a nenhum outro provedor.
- `SANEADOS.json` — o excerto e a exceção declarada (o pacote canônico; o prompt fixo não tem mais termo restrito desde a rodada de 23/09 ~23h33); `NAO_COPIADOS.json` — o que não veio, e por quê.
- `MANIFESTO_INSUMOS.json` — sha16 de cada arquivo desta pasta e da própria ordem; não se lista a si mesmo.
