# CÉTICO 2 — achado «seis auditores independentes» (ORDEM 013-bis L9; RELATORIO L3, L5)

**Veredito: REFUTADO (a ordem não muda). Gravidade ajustada: NOTA (opcional).**

## O que foi medido
- L9 da ordem: «O «tudo» é o relatório da **auditoria da gerência** sobre a entrega da ORDEM 013 (seis auditores independentes, só leitura; relatórios integrais em `ORDEM_013BIS_INSUMOS\auditoria_da_gerencia\`)». A mesma frase já nomeia quem auditou: a gerência. A palavra «gerência» aparece 22 vezes na ordem; a §1 (L26) diz «medido pelos seis auditores **da gerência**»; L276 e o README_INSUMOS (monta_insumos_bis.py:129) dizem «os seis relatórios da auditoria da gerência, um por frente»; o cabeçalho de cada cópia (monta_insumos_bis.py:45) diz «Relatório do auditor i da gerência». Não há como a bancada ler «externos».
- RELATORIO L3: «relatório entregue pela **gerência (Claude)** ao operador ... por seis auditores independentes» — o sujeito está na mesma frase. L5: «Seis auditores independentes conferiram a entrega só lendo» — o objeto da independência é a entrega da bancada.
- Os seis aud_*.txt (mesmo scratchpad da sessão 6da8f00d…, todos gravados 22/09 10:42) usam «independente» no sentido técnico e mensurável: código próprio sem importar bancada nem casa (C0C1C2/leaver.py:2 «Auditor's own code, no house/bancada import»; aud_1:3 «Refiz de forma independente»; aud_2:44 «Recomputação com código meu»; aud_4:41 «oráculo independente»; c4/recompute_catalog.py:1 «independent recomputation»). É esse o sentido que a ordem transporta: independência DA BANCADA (recomputação e leitura), não identidade de revisor externo.
- Não há evidência de cruzamento entre relatórios: nenhum aud cita `aud_k` ou «outro auditor»; aud_4:136 diz «C4, que não é desta frente», o que mostra frentes separadas. Mas também NÃO há evidência positiva de que um não viu o outro.

## Por que se refuta
1. A frase não é falsa nem ambígua no contexto: «auditoria da gerência (seis auditores independentes, só leitura)» — o «independentes» qualifica o método (leitura própria, oráculos próprios, sem tocar no cálculo da bancada), que é exatamente o que os seis relatórios documentam e o que a bancada pode reproduzir pelos scripts copiados nos insumos.
2. A correção proposta introduz uma afirmação NÃO MEDIDA: «sem ver os relatórios dos outros». Nada em disco prova isso; escrevê-la na ordem imutável violaria a régua (o número corrige a frase; nada se afirma sem fonte). «Mesma sessão Claude» é [REAL] pelo caminho do scratchpad, mas a ordem já diz «da gerência», que na casa É a sessão Claude.
3. A errata proposta ao RELATORIO reescreveria uma transcrição para corrigir algo que o próprio texto já diz («entregue pela gerência (Claude)»). Errata ao lado só cabe quando há erro; aqui não há.
4. É questão de gosto/precisão de vocabulário, não de física, estatística, régua, hash ou competência do operador. Na dúvida, refutado=true.

## Se a gerência quiser precisar (NOTA, opcional, sem mudar estatuto)
L9, substituir «(seis auditores independentes, só leitura; ...)» por:
«(seis frentes de auditoria da gerência, um agente por frente, cada um com recomputação própria — independente do código da bancada — e só leitura; relatórios integrais em `ORDEM_013BIS_INSUMOS\auditoria_da_gerencia\`)».
RELATORIO: sem errata (a transcrição já diz «gerência (Claude)»).
