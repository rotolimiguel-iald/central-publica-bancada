# F0.3.E2 — errata ao lado da auditoria a39a1758

Autoria: codex-coordenadora, sob reivindicação F0.3.E2 do quadro. Esta camada não altera o estado da F0.3: AUDITADA, aguardando o recibo de recarga X17.

1. [REAL — custódia] Os recibos originais citados nos eventos 400, 414 e 433 continuam nos mesmos bytes e seus SHA-256 conferem com os eventos. Antes, não havia cópia em PROGRAMA_IALD/evidencias. O avanço 486 de F0.3.E2 fez três cópias oficiais; origem e cópia foram conferidas por hash e tamanho, três de três. Esta recustódia não reescreve os eventos históricos.
2. [REAL — mapa] Na seq 900, formal.f1_2_dual_scaling e formal.f2_3_ligante_lei_campo_curvo são referências inexistentes. As rotas efetivas conferidas pelo mapa são formal.f1_2.v351_dual_scaling_bridge e formal.f2_3.curved_field_ligand. A seq 900 permanece íntegra; a errata fica em registro novo com corrige: 900.
3. [REAL — cronologia] O append de memória das 14:32 mencionou F7.2.E1 e F1.3.E4 antes do registro dessas camadas. Naquele instante, a entrega delas ainda não era [REAL]; a frase era antecipação [DECLARADO]. Os registros vieram depois: mapa seq 906 e 907 às 14:35:08, quadro eventos 443 e 444 às 14:36:19. Hoje ambas constam ENTREGUES; não retroagir esse estado à escrita das 14:32.
4. [REAL — reivindicação 301] O evento 301 tomou F1.3. O fechamento por iald.py avancar --status FECHADA no evento 312 limpa a reivindicação automaticamente (iald.py, ramo if a.status in FINAIS), e iald.py ver F1.3 agora devolve reivindicacao: null. Não há reivindicação 301 ativa a liberar. Um novo liberar criaria apenas um evento redundante.

Os seis writes de memória auditados pela c1 preservam sua cadeia de backups. Nenhuma recarga MCP, escrita na Bancada, abertura de dado ou movimento de gate foi realizada nesta camada.