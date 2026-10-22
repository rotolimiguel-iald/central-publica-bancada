# CÉTICO 1 — achado «seis auditores independentes» (ORDEM 013-bis L9; RELATORIO L3, L5)

## Medido (22/09/2026)
- L9 da ordem: «(seis auditores independentes, só leitura; relatórios integrais em ...)». Contexto da mesma frase: «relatório da auditoria da gerência». L26: «medido pelos seis auditores da gerência».
- aud_1..6.txt: seis arquivos gravados no mesmo minuto (10:42, mesma pasta de scratchpad da sessão 6da8f00d-...); 4 dos 6 citam o id da sessão no próprio texto (aud_3, 4, 5, 6); aud_1 e aud_2 citam a mesma pasta `...\scratchpad\ordem013\auditoria\`.
- monta_insumos_bis.py:45 rotula cada um como «Relatório do auditor i da gerência» e nomeia a frente única de cada um.
- Remissões cruzadas entre relatórios (grep `aud_[1-6]|outro auditor|outros auditores`): ZERO — coerente com «um por frente, sem ver os outros», mas isso é indício, não prova.
- «independente» aparece nos relatórios no sentido de RECÁLCULO independente da bancada (aud_1:3, aud_2:44 «código meu»), não de revisor independente do modelo/orquestrador.

## Veredito
Refutado = NÃO. O que é medido: seis frentes, seis agentes da mesma sessão Claude (mesmo modelo, mesmo orquestrador), cada um só leitura, cada um refazendo por script próprio, sem remissão a outro relatório. O que L9 sugere sem qualificar: revisores distintos, com erro descorrelacionado. Para a bancada (ChatGPT/Codex) isso é peso probatório declarado sem medida; erro correlacionado de modelo é exatamente o que «independentes» esconde. Gravidade mantida em IMPORTANTE (limite inferior da faixa: o contexto «da gerência» já exclui «externos»; não muda física nem número).

Ressalva à correção proposta pelo revisor: «sem ver os relatórios dos outros» não está medido (só a ausência de remissão cruzada). A correção final abaixo diz o que se mede.

## Correção FINAL — L9 (substituir o parêntese)
«(seis frentes de auditoria da gerência: seis agentes da mesma sessão Claude, um por frente, cada um só leitura, refazendo os números por script próprio e sem remissão aos demais relatórios — independentes da bancada, não do modelo; relatórios integrais em `ORDEM_013BIS_INSUMOS\auditoria_da_gerencia\`)»

## Correção FINAL — insumo RELATORIO (errata ao lado, linha nova logo abaixo da L3; L3 e L5 ficam como estão)
«> Errata da gerência (22/09/2026, ao lado): onde este relatório diz “seis auditores independentes”, leia-se “seis frentes de auditoria por seis agentes da mesma sessão Claude, só leitura, um por frente, com recálculo próprio — independentes da bancada, não do modelo”.»
