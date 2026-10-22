# F3.1.E2 — nota factual ao lado da F3.1.E1

[REAL] A F3.1.E1 está FECHADA pelo evento 587. Esta nota não a reabre nem altera qualquer artefato pinado.

[REAL] O arquivo administrativo `NOVA_UNIDADE_F31_E1_LABELS_20261008.json` tem SHA-256 `e456781c85e674db4aa379e45339a502f470b056fb4b4a4a00e5795f55c20eff`, 415 bytes e mtime local `2026-10-08T17:39:06.546104-03:00`. O evento 576 (`nova`) é de `2026-10-08T17:39:13-03:00` e aponta para esse mesmo caminho e hash. A reivindicação 577 veio em `2026-10-08T17:39:20-03:00`. Entre o mtime do arquivo e o horário registrado da reivindicação há 13.453896 segundos, aproximadamente 14 segundos. O quadro registra segundos inteiros; este número compara o mtime com o horário assim registrado.

[DERIVED] No `iald.py` atual, `nova` lê um arquivo JSON com a definição da unidade antes de inseri-la, e `reivindicar` busca uma unidade já existente. Assim, a criação do JSON administrativo antes da reivindicação era uma dependência do fluxo do quadro usado naquele ato. Isso explica a ordem operacional, mas não cancela a regra de reivindicar antes de produzir o objeto da unidade.

[OPEN] Esses registros não identificam o processo que gravou os bytes às 17:39:06, nem demonstram intenção, causa adicional ou execução científica antes da reivindicação. A auditoria c1 é a fonte da ressalva; os eventos e o arquivo acima conferem o intervalo.

[REAL] Para esta nota derivada, a unidade F3.1.E2 foi criada com JSON administrativo fora do túnel no evento 592 (`2026-10-08T18:38:24-03:00`, SHA-256 `6971e393186fb49af78533b758264dd69ee65f3cc03362b155580ec70fc1f019`) e reivindicada no evento 595 (`2026-10-08T18:38:30-03:00`) antes de qualquer escrita da E2 no túnel. Nenhuma memória, gate, dado real, F3.1.E1 ou arquivo pinado foi tocado por esta camada.

Fontes pinadas: auditoria c1 SHA-256 `21cff3d7c3216d8597a5c6a663b343f6bbd523f828a17e32f192196f5481a7d4`; quadro `eventos.jsonl` eventos 576, 577, 587, 592 e 595; JSON administrativo E1 SHA-256 `e456781c85e674db4aa379e45339a502f470b056fb4b4a4a00e5795f55c20eff`.
