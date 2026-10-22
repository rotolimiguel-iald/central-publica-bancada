[REAL — A-0 concluído com MEDIDAS de orquestração e upload]

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

- A-0.1 PAGO: falas verbatim preservadas.
- A-0.2 PAGO: ordens 016 (774 linhas) e 015 (441 linhas) lidas integralmente; manifesto 016: 397/397 registros conferidos. Fontes: 74 coincidências, 3 registros divergentes referentes a duas fontes vivas, 9 excluídos expressamente. As duas fontes vivas são acréscimos puros, verificação por hash do prefixo antigo.
- A-0.3 PAGO: nove blocos do core/selo concordam com ESTADO_QG_v370; nenhum programa original executado.
- A-0.4 PAGO: 149 âncoras com hashes coincidentes; 136 localizações exatas e 13 rótulos anotados/docstrings conferidos na linha. A busca lexical inicial não retirava as anotações: resultado preservado e revisão ao lado. Não é recompilação das 149 declarações.
- A-0.5 MEDIDA: MCP ausente (recibo 1d0e8630d0ddb5a5fe5c4c977100ba9eb5430d946d639740f21b32f880f3eb76); ledger iniciado vazio e mantido. Upload integral não confirmado: tentativa bloqueou ferramenta por 5040,8872 s, excedendo teto de 1 h dentro da chamada; três itens v370 sem estado final confirmado. Zero chamadas LLM externas; custo US$ 0.
- A-0.6 PAGO: Lean 4.31.0, rc 0; sete consultas de axiomas aprovadas; zero arquivos canônicos mais novos, zero erros de varredura. Parede 219.391 s; CPU usuário 10.421875 s e kernel 24.250000 s; pico de memória comprometida do processo 8327561216 B (métrica Windows, não RSS). Limite de 8 GiB e 900 s no Job.
- Recuo A-0.6b não necessário.

Tempo decorrido desde abertura: 1.736511 h (inclui chamada bloqueante de upload; não equivale a atenção ativa). Máquina pesada Parte B: 0 h. Primeira compilação leve: 0.060942 h. Descoberta inicial lake sem pin iniciou download de outra versão; interrompida, rc 1; compilação paga usou executável 4.31.0 instalado e versão fixada.

Não move a fronteira da QG. Nenhum termo H2/H3 ou setor interagente construído nesta etapa. Próximo: A-1.a reprodução v3/v3.1. Parte B: abertura e manifesto 2638/2638 preparados durante espera; sem R7, V1.1 ou job pesado.

Reprodução: python -B compile_isolated.py <kernel canônico> <cópia AxiomasContorno.lean> <rótulo inédito>. O recibo contém a lista exata de argumentos lake env lean; saída somente fora do kernel.

Artefatos (SHA256 lidos):
- A0/sources_audit.json: cf4e3bcdca7bda6dc309081de1982db6a9490d9f2a854f7c2d6ff212b1a97b92
- A0/core_audit.json: a10e9ab09ff12ebd3c225df116db452f95dba2ace0e40417261a80ebb0bb5b9f
- A0/anchors_audit.json: 6b8648215c10f6ac1eba7d8c5c39c22395a8ff73be8577d0c2c76b8a5841a30a
- A0/anchors_annotation_review.json: 6ffe3595ee565afadda3896ce95c0dc35e416febf03d763076305463705a2a9c
- A0/live_sources_append_check.json: 792d6803635aae7f50395222db34ec465135b56b4d43b8ae33a1d22a843e081f
- A0/package_audit.json: efc579aa9b011a3de7c6b48840af72d86bca46c1314d47b785bac340f437d120
- A0/upload_attempt.json: 97b52e23b1b63a221e8227bf07c3f87e50315b1982d58635b7b4c05fb7109e97
- A0/canonical_smoke_01.json: 8357e7e05ab63048514ac0851705bccc9f4179b082a33021df77e4903230665c
- A0/canonical_smoke_01.log: 5a82aa33711ea309be869f5da85a4e75920fc8277d86c38c33687ee475c406b6
- A0/canonical_axioms_audit.json: bdda84e8b8fe936496f0272b2f92003d7c6e8ac90060119392015a05fcdcaf08
- A0/environment_discovery_incident.json: 2d0a4a95c14a51ef6c74ebdb06de204d3e49483ee56d1f93f97cd02c869acf7c
- A0/audit_inputs.py: 1584fed61bb0c3cdfafc0012c41e32cd48aa7208110cb58ce2a7b035aa9d6026
- A0/compile_isolated.py: 5f9ccb50a59535cb475f1815b5b2ffadf73928ca33305865b95933b84545ea69
