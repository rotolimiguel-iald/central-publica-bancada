# F2.3.E4 — errata do acrescimo no ADENDO pinado

Autor: codex-gerente-tgl. Data: 08/10/2026. Estatuto: [REAL — bytes e hashes conferidos].

Na F2.3.E2, foram acrescentados 651 bytes in loco a ADENDO_TEMPERATURA_DIAGNOSTICO.md depois do fecho da F2.3. O evento 355 e a seq 871 pinavam o estado anterior, SHA-256 673780c016334c72a2463453ac5bbc8179a301c19fb2ce66814fe323def099f9. A reivindicacao 422 dizia sem tocar F2.3 fechada. A acao contrariou esse alcance; o pino por caminho deixou de reproduzir os bytes antigos.

O backup bak_20261008_141543 e a copia evidencias/673780c016334c72a2463453ac5bbc8179a301c19fb2ce66814fe323def099f9.md preservam exatamente os 9898 bytes anteriores. O arquivo atual tem 10549 bytes e o backup e prefixo byte a byte dele. Esta camada nao desfaz nem edita o ADENDO. Futuras correcoes do artefato pinado ficam em arquivo novo ao lado, com hash e vinculo no quadro e mapa.
