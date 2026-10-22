# Revisão local de empacotamento — adjudicada

[REAL — inspeção estática; nenhuma compilação ou chamada remota]

Arquivos examinados (SHA256 lido dos bytes):

- `assemble_package.py` — `8dd3443f68dd622a6c2694c1dc8911cbb6900b105e69d2ebd057c9e7c2cdd6d6`
- `PROPOSTA_RUNTIME.py` — `484fa0930e1b1c9c2f3dc6149e2b07d8e7df7a8cb12d3f8004db3a277021fd65`
- `reproduzir.py` — `8f34028c426946c03a1ede696a6d1b181933ae487d38d7c41b92e5bdd7831c83`
- `lean/ContratoQG_v32_Proposta.lean` — `3ab863dddd41f7583156ab6d9335c04cec3d431c6c182a58c224ddd9646ca4a4`
- `SOURCE_PLAN.json` — `3ff559e8ddc373f0597a073123ed4863dee6d070ba9d10d73fef51fd0110a445`
- `SUPPLEMENTAL_PLAN.json` — `5c063d1e56bdf840504d268c81d8ac7455d02d52cf887138a928e8b14f753db5`
- `compile_batch.py` — `a45544f6d7fed81c1dcf3e1b807a829a279e53ba357c44f6772aa0b105fb8d40`
- `finish_compilation.py` — `35be7f4b6739550c766d910acfb68d5df1ed19c3a23f3a8c51e73018c1cdcf38`
- `../../ORDEM_016_QG/D6/ContentContractProposal.lean` — `85c83f1a2e3af8f934665d75fbdc18decb4f72b5989fa6d791863afc18366770`
- `lean/PhotonContractTheorems_v2.lean` — `4f6d5cd3d0d64045832f59ec3c71c81e5b1b713df4cd17ef96e59211d5f0fd44`

## Achados ativos

### F1 · MEDIUM · Ramo de falha da proposta P3 pode ser anunciado como compilado

compile_batch inclui ContratoQG_v32_Proposta; finish_compilation importa no joint apenas estados rc0. Se a proposta tiver rc≠0, assemble ainda monta índice que anuncia lean/ContratoQG_v32_Proposta.lean, sem assert de presença. Se rc0, este achado não se aplica.

Impacto: Pacote parcial pode declarar P3 compilado quando o módulo foi excluído por falha.

Correção proposta: Exigir explicitamente módulo e rc0 no joint antes de anunciar a proposta, ou emitir MEDIDA e retirar a afirmação no índice.

### F3 · HIGH · Adulteração de evidência histórica não bloqueia assemble/seal

P8_COPIAS registra unchanged=sha(dest)==previously_indexed_sha256, porém não exige true. Um relatório alterado após o índice é copiado, e seal() apenas calcula hashes do pacote atual. No instante desta revisão, as fontes P8 e apoio conferem; o defeito é no caminho de recusa futura.

Impacto: Pacote pode ser selado com fonte histórica divergente de hash previamente indexado.

Correção proposta: Comparar hash atual com row.sha256 antes de copiar e falhar visivelmente na divergência; verificar unchanged em seal.

### F5 · MEDIUM · Runtime não cruza rc/axiomas declarados com o conteúdo dos recibos

O leitor confere SHA dos arquivos contra P2 e PRONTO, mas usa unit.rc e unit.axioms do próprio P2 sem comparar rc, source_sha256 e log_sha256 no JSON do recibo nem BENCH_DECL do log. Controles sintéticos atuais mutam bytes de arquivos, não inconsistências entre metadados internamente pinados.

Impacto: Um pacote incorretamente montado pode retornar BENCH_ARTIFACT_CHECKED para metadados rc/axiomas contraditórios ao recibo/log.

Correção proposta: Parsear recibo e linhas BENCH_DECL e exigir equivalência integral aos campos da unidade antes de all_verified.

### F6 · MEDIUM · Reprodução não exige pin externo de PRONTO

O script lê PRONTO.json do próprio pacote, verifica seus arquivos contra a mesma lista e só registra o SHA ao final; não recebe hash esperado independente. Um pacote e PRONTO reescritos em conjunto passam esse controle autorreferente.

Impacto: P7 demonstra consistência interna, mas não custódia contra o selo que a gerência recebeu.

Correção proposta: Aceitar --expected-ready-sha obrigatório e comparar antes de copiar/compilar; manter falha fechada.

## Adjudicações

- A1 — CORRIGIDO NA REVISÃO: Módulo entra em compile_batch.py:17 e, com rc0, em finish_compilation.py:26. Resta só o ramo de falha descrito em F1.
- A2 — RETIRADO COMO DEFEITO: D6.same_horizon_by_content_from_realizations deriva a conjugação dos dois fluxos a partir dos realizadores; PhotonContractTheorems_v2.lean:681 demonstra Δit_determined para W/R/N fixos. O contrato deve documentar a projeção e não sugerir que κ/frame decorrem apenas do reconhecimento.
- A3 — REBAIXADO A FRAGILIDADE: Embora assemble_package.py:107 extraia imports só do SOURCE_PLAN, comparação estática atual das importações TGL/TGLExt nos módulos primários e suplementares achou zero imports faltantes. A extração é frágil ante nova fonte, mas não há omissão atual medida.

Esta revisão não executou o lote Lean ativo, não certifica P2/P3/P5 e não move o gate.
