# CÉTICO 2 — achado «ESTADO_AUDITADO.json sem regra de divergência» (ordem l.279 / §6 l.234 / PROMPT item 2)

Medido em 22/09/2026 12:28, bancada SÓ LEITURA (`C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`).

## O que o achado afirma × o que o número diz

1. «a divergência é certa já no primeiro turno» — **REFUTADO em parte.** Script sobre os 34 artefatos de `ESTADO_AUDITADO.json`: **0/34 divergentes às 12:28** (bytes e sha16 iguais). O PROMPT (l.12) manda «Comece agora pela verificação dos sha16» ANTES de F0 — a primeira conferência passa. A divergência só nasce DEPOIS que a bancada grava.
2. «vários C5_*» divergem por processo vivo — **REFUTADO.** Os três jobs vivos (`ps` no WSL: 1261 run_real_phase_importance ×4; 1413 SEOBNRv4HM ×2; 1449 IMRPhenomXPHM ×12) rodam de `cache\source_evidence\` e escrevem só `REGISTRATION/START/PROGRESS/EVALUATIONS_COMPLETE/RESULT/PROPOSAL*.json` nessa subpasta — **nenhum dos 34**. Os C5_* só mudam se a bancada os sobrescrever, o que a ordem já proíbe (l.53 «correção ao lado, nunca por cima»; l.221 backup de bytes; F-alvos pedem «v2 ao lado»).
3. `STATUS_ORDEM_013.json` é vivo — **CONFIRMADO.** 26 scripts `record_*.py` da bancada o reescrevem (com `.bak_` — 41 backups só hoje, 5 entre 08:43 e 10:04). A ordem o cita (l.4) mas NUNCA manda atualizá-lo e não o distingue dos outros 33 no JSON (campos: arquivo, bytes, sha16, mtime — sem `vivo`). A nota do JSON diz «toda correcao e adendo ao lado, com hash novo», o que é inexecutável para um ledger de status.
4. Ambiguidade — **CONFIRMADA.** PROMPT l.4 encadeia «cada artefato seu contra ESTADO_AUDITADO.json» → «Se divergir ... qualquer fonte congelada: PARE». «Fonte congelada» não é definido; §7 só define «fonte VIVA» (l.234). O JSON chama os bytes auditados de estado ao qual «o recibo vale» — leitura «congelado» é plausível. Consequência de uma leitura errada: BLOQUEIO espúrio ao primeiro `record_*.py` (a Parte A para até resposta da gerência). A leitura oposta (ignorar) não causa dano — o recibo cobre os bytes auditados e os backups existem.

## Veredito

refutado = **false** no núcleo (ausência de regra + STATUS vivo listado sem marca), com as duas evidências do revisor corrigidas (não é «certa no primeiro turno»; não há C5_* vivo). Gravidade mantida **IMPORTANTE** pelo custo assimétrico: uma linha na ordem evita um turno perdido da bancada; a ordem é imutável depois de publicada.

## Correção FINAL (texto exato)

(a) §6, l.234 — acrescentar ao fim do item «Bloqueios», na mesma linha:
`Artefato SEU listado em ESTADO_AUDITADO.json que divergir NÃO é bloqueio: o recibo da §1 vale para os bytes auditados; a ENTREGA do marco lista cada divergente com os dois sha16 e a causa (adendo ao lado / backup / STATUS). STATUS_ORDEM_013.json é vivo por construção (26 record_*.py o reescrevem com .bak_) e fica fora do recibo.`

(b) `ORDEM_013BIS_INSUMOS\ESTADO_AUDITADO.json` — na entrada `STATUS_ORDEM_013.json`, acrescentar `"vivo": true` (não retirar: o sha16 0815ce7d607ac49f documenta o estado que a §1 leu). Como o JSON entra no MANIFESTO_INSUMOS.json, regenerar o manifesto por script depois (l.281: «não se lista a si mesmo»).

(c) PROMPT l.4 — após «(o recibo da seção 1 vale para esses bytes)» inserir: «; divergência de artefato SEU não é bloqueio — só se registra».
