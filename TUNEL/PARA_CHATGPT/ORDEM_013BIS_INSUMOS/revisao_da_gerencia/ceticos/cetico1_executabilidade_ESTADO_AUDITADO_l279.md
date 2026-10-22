# CÉTICO 1 — achado «ESTADO_AUDITADO.json sem regra de divergência» (ordem l.279; §6 l.234; PROMPT l.4)

**Veredito: NÃO refutado (refutado=false). Gravidade mantida: IMPORTANTE.** Um exagero do revisor é corrigido ao lado.

## O que foi medido (script, 22/09/2026 12:28 -0300; bancada só leitura)

1. `ESTADO_AUDITADO.json` (scratchpad `bis\ORDEM_013BIS_INSUMOS\`): 34 artefatos; 1º = `STATUS_ORDEM_013.json` (sha16 `0815ce7d607ac49f`, 343.395 B, mtime 22/09 10:04:13); `nota` = «o recibo ... vale para ESTES bytes; toda correcao e adendo ao lado, com hash novo».
2. Conferência dos 34 sha16 contra `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\` **agora**: **0 de 34 divergentes**. Bytes e mtimes idênticos ao JSON.
3. Os três processos vivos escrevem só em `cache\source_evidence\...\{RESULT,AUDIT_RATE,...}.json` — **nenhum toca os 34 artefatos da raiz**. A afirmação do revisor «a divergência é certa já no primeiro turno» é **exagerada**: no instante da conferência inicial (PROMPT l.12: «Comece agora pela verificação dos sha16») não há divergência.
4. **Mas `STATUS_ORDEM_013.json` É vivo por construção**: quem o reescreve são os scripts `record_*.py` da própria bancada (10 arquivos gravam nele: `record_c1_c6_addendum.py`, `record_delivery_bundle.py`, `record_family_mixture_progress.py`, ...), um por turno; prova em disco: `STATUS_ORDEM_013.json.bak_20260922_093802_775542` (341.461 B) e `.bak_20260922_100413_456688` (341.371 B) — duas reescritas só na manhã de 22/09. O mesmo vale para `PROGRESSO.md` (fora do JSON). A primeira `record_*` da bancada sob a 013-bis (F0 pede anexo com hash — e a bancada registra tudo em STATUS) torna o item 1 divergente; qualquer conferência posterior à inicial (ou uma inicial feita DEPOIS de registrar «ordem recebida») diverge.
5. Texto da ordem: `grep` de «divergência» dá só l.155, l.234, l.279, l.284. A l.234 enumera os gatilhos de PARE (ORDEM 013, esta ordem, insumo, pacote v369, fonte congelada) e o caso «fonte VIVA ... registre e siga» — **artefato da própria bancada não está em nenhuma das duas listas**. PROMPT l.4 manda conferir «cada artefato seu contra ESTADO_AUDITADO.json» e a frase seguinte «Se divergir a ordem, um insumo, o pacote v369 ou qualquer fonte congelada: PARE» também não o inclui. Consequência da divergência de artefato próprio: **não escrita em lugar nenhum** (ordem, prompt, `README_INSUMOS.md` l.8, JSON `nota`).
6. `MANIFESTO_INSUMOS.json` **ainda não existe** no scratchpad (será gerado por script na publicação) — logo `ESTADO_AUDITADO.json` ainda pode ser corrigido sem quebrar hash algum.
7. A ORDEM 013 nunca citou `STATUS_ORDEM_013.json` (grep vazio); ele é ferramenta de turno da bancada, não entregável. A 013-bis o cita na l.4 como fonte do `goal_status` — o que justifica hasheá-lo como *estado lido*, não como *bytes sob recibo*.

## Por que o achado fica de pé

- A instrução «confira ... e de cada artefato seu» sem consequência é uma instrução sem saída: as duas leituras possíveis (PARE por analogia com l.234; ou ignorar) são ambas defensáveis pelo texto, e ambas ruins — a primeira gasta o marco MA num `BLOQUEIO_manifesto` por causa de um arquivo que a própria bancada reescreve por rotina; a segunda deixa a gerência auditar MA sem saber se os bytes da §1 ainda são os de disco.
- Há exploração real: a l.53 proíbe corrigir «por cima» na Parte A, e a l.221 proíbe sobrescrever artefato citado sem backup; sem a regra de divergência, uma sobrescrita *com* backup dos C4_*/C5_* auditados passa como «divergência não listada como bloqueio» e o recibo da §1 perde o objeto sem que a ENTREGA o diga.
- Não é gosto: é regra de protocolo ausente num contrato que a ordem declara imutável.

## Correção do exagero do revisor (ao lado)

Trocar «a divergência é certa já no primeiro turno» por «0/34 divergem na conferência inicial (medido 22/09 12:28); `STATUS_ORDEM_013.json` diverge no primeiro `record_*.py` da bancada, e os C4_*/C5_* só divergem se a bancada os tocar por cima». Isto muda a urgência, não a gravidade: a regra ausente continua ausente.

## Correção FINAL (texto exato)

**(a) §6, l.234 — acrescentar, no fim do bullet «Bloqueios», após «... e siga.»:**

> **Artefato SEU contra `ESTADO_AUDITADO.json`: divergência NÃO é bloqueio.** O recibo da §1 vale para os bytes ali listados e só para eles. A ENTREGA do MA traz a tabela `DIVERGENCIAS_ESTADO_AUDITADO` (arquivo; sha16 auditado; sha16 atual; causa ∈ {adendo ao lado / STATUS vivo / sobrescrita — e, se sobrescrita, o caminho do backup de bytes}). Sobrescrever qualquer artefato auditado é violação da regra desta Parte A (correção ao lado, nunca por cima): o original volta do backup e a correção vai para o adendo. `STATUS_ORDEM_013.json` e `PROGRESSO.md` são vivos (reescritos pelos `record_*.py` a cada turno): ficam fora do recibo; registre o par de sha16 e siga.

**(b) §7, l.279 — substituir o parêntese de `ESTADO_AUDITADO.json` por:**

> `ESTADO_AUDITADO.json` (sha16 dos artefatos-chave da bancada no estado auditado — o recibo da §1 vale para esses bytes; a entrada `STATUS_ORDEM_013.json` traz `vivo: true` e vale só como o estado lido às 10:04 de 22/09, fora do recibo; divergência de artefato seu segue a regra da §6)

**(c) Insumo — por script, antes de gerar `MANIFESTO_INSUMOS.json`:** em `ESTADO_AUDITADO.json`, acrescentar `"vivo": true` à entrada `STATUS_ORDEM_013.json` (e nada mais); regenerar o manifesto depois. Não retirar a entrada: a l.4 da ordem cita o `goal_status` lido desse arquivo, e o sha16 é o rastro de qual estado foi lido.

**(d) PROMPT l.4 — após «(o recibo da seção 1 vale para esses bytes)» acrescentar:** «; divergência de artefato seu NÃO é bloqueio — liste-a na ENTREGA do MA com os dois sha16 e a causa; STATUS_ORDEM_013.json é vivo e fica fora do recibo».
