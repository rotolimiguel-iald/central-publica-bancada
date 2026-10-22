# F0.3.E5 — errata e forense curta de quatro pinos

[ERRATA AO LADO, em nome de codex-coordenadora] Retiro a afirmação geral «nenhum outro pino mudou». Ela é falsa: além dos casos registrados na F0.3.E3/E4, a auditoria c1 a9f3787c encontrou quatro caminhos adicionais. Os hashes abaixo foram lidos dos bytes atuais e backups. Os originais não foram editados nesta unidade.

## F9.5/RESULTADO.json

Antes: seq 80 `5263445ac24c7fb163667f5ad9ee2da62f14730c1a1e6f4a5a6ee425d5b683dd` (1485 B), seq 82 `bcd6b2506637c4bed902624ae7727f84f94ef866a4b50736152e418056edce52` (1485 B).
Atual: `7e3e11b7d17dad3ccef3fa6e7012354a6b6085265a16f0390edea2c38ee133d0` (2341 B; mtime 2026-10-07T20:12:04.601410-03:00).
Prefixo anterior preservado: False. Recibo refeito após arquivar 130 backups do transporte; evento 136, mapa 720. Não é append: campos e pins foram regenerados.
Autoria: codex-gerente-tgl [REAL: eventos 80, 82, 136].
Repins no mapa: 720:7e3e11b7d17dad3c.

## F2.3/ADENDO_TEMPERATURA_DIAGNOSTICO.md

Antes: seq 355 `673780c016334c72a2463453ac5bbc8179a301c19fb2ce66814fe323def099f9` (9898 B).
Atual: `cb0a73cb40f68652aa0e8945a53355fefa62b429016c94c381bd8a26ed53a728` (10549 B; mtime 2026-10-08T14:15:43.167989-03:00).
Prefixo anterior preservado: True. Acréscimo de 651 bytes da errata de nomenclatura F2.3.E2 às 14:15, entregue no evento 428; a própria F2.3 já possuía forense desse desvio.
Autoria: codex-gerente-tgl [DERIVED: evento 428 e marcador F23_E2].
Repins no mapa: .

## F7.2/STAGING/README_DEPLOY.md

Antes: seq 822 `0d380faae32dcc166166221d4c452cca9738c98f8f98b82b249ff9e9ea7ba802` (3539 B).
Atual: `3791c6e582dcdd1d5707cd4fff5da9c9e2e6e3a49128bd61e3f65d7501df1562` (3540 B; mtime 2026-10-08T08:09:43.844744-03:00).
Prefixo anterior preservado: False. Correção do byte 0x0b no caminho project_fisica para os caracteres literais barra invertida + v, entregue no evento 300; não é append.
Autoria: codex-gerente-tgl [DERIVED: evento 300, mapa 835].
Repins no mapa: 835:3791c6e582dcdd1d, 841:3791c6e582dcdd1d.

## F7.2/V2_STAGING/README_V2_STAGING.md

Antes: seq 822 `6b7442471a77c37c4703fc2567ff3c81669686196406b2776fde042e924e7e72` (2621 B), seq 841 `6b7442471a77c37c4703fc2567ff3c81669686196406b2776fde042e924e7e72` (2621 B).
Atual: `cb4a2f6e3c091689ce19103b5fdedd2886a512819f8c88d99ce527baf635be3e` (3796 B; mtime 2026-10-08T10:44:14.959070-03:00).
Prefixo anterior preservado: True. Acréscimo de 1175 bytes com errata de estado de implantação e Eq.6, entregue no evento 336. A frase histórica sobre ratificação pendente foi depois corrigida ao lado; não a adotar como estado atual.
Autoria: codex-gerente-tgl [DERIVED: evento 336, mapa 857].
Repins no mapa: 857:cb4a2f6e3c091689, 860:cb4a2f6e3c091689, 863:cb4a2f6e3c091689.

[REAL — precisão de sequência] `README_DEPLOY.md` atual aparece no mapa 835/841. `README_V2_STAGING.md` atual aparece nas seq 857/860/863; a seq 835 não o repina. O número corrige a descrição agrupada da auditoria.

[ESTADO] As alterações históricas foram repinadas depois; a existência do repin não legitima editar um pino no lugar. Novas camadas seguem em novos arquivos. Sem dado aberto, publicação ou mudança de gate.
