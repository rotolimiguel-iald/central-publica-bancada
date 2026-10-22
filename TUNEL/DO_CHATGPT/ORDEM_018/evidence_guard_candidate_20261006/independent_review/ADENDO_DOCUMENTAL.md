# Adendo final — documentação e contagem de pins

**PASS_STATIC_REVIEW_ONLY mantido.** O delta documental foi recebido durante o fechamento do parecer anterior; este adendo corrige ao lado o retrato textual anterior, sem alterar o selo ou os achados iniciais.

[REAL — bytes conferidos] SOURCE_PINS.json contém **6 fontes originais e 8 candidatos: 14 relações**, todas conferidas. O texto anterior dizia dez, contagem do primeiro candidato; EVIDENCIAS_FINAIS.json e o manifesto anterior já continham as quatorze relações efetivamente medidas. A expressão textual anterior fica corrigida por este adendo.

As pendências documentais do item 2 do parecer anterior estão encerradas no candidato final: `candidate/ui/index.html:87` distingue cauda local e ilustração de Šidák da significância global indisponível; `candidate/README.md` preserva integralmente o texto histórico e acrescenta adendo explícito que o supera no escopo da preparação, sem alegar instalação; o header de `candidate/mcp_um.py:6` já diz diagnóstico/indisponibilidade. Os diffs foram lidos, não executados.

A lógica de evidencia.py, evidence_checks.py, regua.py e app.js permaneceu byte idêntica ao selo independente anterior. O __init__ continua marcado apenas para staging; instalar o novo helper é necessário, sobrescrever __init__ não está incluído. Roteiros históricos permanecem não migrados e não devem ser usados com a nova saída sem adequação; o README agora registra essa limitação.

EG-01 e EG-02 permanecem resolvidos. Os 19 testes Python, 11 casos do renderizador e sintaxe JavaScript continuam exclusivamente atribuídos ao recibo ROOT TEST_ATTEMPT_02; não os repeti. Nenhuma importação/execução de candidato, ciência, dados observados, WSL, HTTP, provedor ou modificação de produção foi feita pelo revisor. Este conjunto encerra a revisão estática do candidato, sem autorizar implantação ou validar significância científica.
