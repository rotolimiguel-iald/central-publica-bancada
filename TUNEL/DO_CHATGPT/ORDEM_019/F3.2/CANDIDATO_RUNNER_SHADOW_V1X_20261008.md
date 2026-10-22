# F3.2 — vínculo V1.x e runner sintético, candidatos

[REAL — inspeção local] O Nós vivo mostrou a F3.2 `AUDITADA`, o vínculo R1 e o
verificador `f9_reader_gate.py` já entregues. A auditoria c1 em
`C:\IALD\PROGRAMA_IALD\auditorias\F3.1_F3.2\AUDITORIA_F3_1_F3_2_C1_20261007.md`
aprovou o componente com ressalvas. Os seis testes originais são **um caso
válido e cinco recusas**. O código original e seu `RESULTADO.json` ficaram
inalterados como evidências históricas.

## O que o candidato implementa

`f9_reader_gate_v1x_candidate.py` reaproveita a leitura de bytes, pin SHA-256,
resolução de caminho e `_reconstruct_sigma` do gate entregue. Ele exige um
**novo** vínculo V1.x pinado, um spec V1.x distinto do V1 histórico, os cinco
IDs completos, todos os bytes de fonte, e janelas literais para `H0` e para
cada componente publicado de σ. Uma âncora genérica não passa. As
compressões locais `identity`, `quadrature` e `arithmetic_mean` mantêm os
componentes; a média assimétrica conserva os lados `plus` e `minus` no recibo.
Chave ou tipo de esquema faltante produz `ReaderGateError`, uma recusa tipada.
O retorno continua `REAL_DOCUMENTARY_HASH_ONLY`, com admissão estatística e
covariância cruzada `OPEN`.

`f9_shadow_runner_candidate.py` só aceita caso, vínculo, spec e fontes sob
uma raiz de fixture explicitamente marcada `synthetic_fixture=true`, todos
pinados. Calcula **somente** a fórmula de poder do V1 nas duas pontas σ
sintéticas e imprime o recibo em stdout. Não possui entrada de dado real,
verossimilhança, composto, veredito, escrita de saída nem rotina que crie
`ALVOS_FASE9_LIDOS.json`. O contrato sintético exige
`mu_do_rito: q→0 (Thomson; Teorema da Escala)` e declara a semântica do
executor indicada na auditoria: fundo marginalizado; perfil de −2 ln L de
`z_delta` com log-det; quadratura ln B com n mínimo 100; `z_disc` como forma
quadrática; σβ como média dos lados. Essas cinco operações **não são
executadas** neste preflight. O nome final do token continua reservado ao
operador (D-J).

## Limites e etapas seguintes

[OPEN] O vínculo real V1.x não existe ainda. A semântica decisória da V2, a
admissão D-H, NAT-22 e F3.4 aguardam os atos competentes. Quando a gerência
estabelecer a semântica, o novo vínculo terá de pinar o spec V1.x e as fontes,
inclusive o PDF do L4 se os cinco masers forem decisórios. A assimetria
`+3,1/−3,0` deve sobreviver no vínculo; a compressão local não recupera a
verossimilhança original nem prova independência (achado D5 da seq 696).
Os centros físicos, seus dados, o mapa TGL do observável e o composto não
foram examinados por este runner. Um resultado documental não autoriza a
legenda `[REAL por hash]` de um leitor no teste físico sem a admissão D-H
(achado D6 da seq 696). Iniciar a Fase 9 não é abrir F3.3.

[REAL — teste local] `python -B -m unittest -v test_f9_shadow_candidate`:
12 de 12 passaram, **um caso sintético válido e onze recusas**. O log é
`TESTE_SHADOW_V1X_20261008.log`. Nenhum gate, spec, fonte canônica, `um.py`
ou veredito foi alterado. `NOT_FALSIFIED` nunca é creditação.
