[REAL — T03 registro e controles pagos; nulos da fase P ainda não executados]

Abertura015SHA256: dbd0a307438dda2969a21baf64665d54e8b70fb84c3fe10f8c233ddeac736610
Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

V1.1 registrada com testemunha anterior a qualquer job pesado. RegistroSHA256 96571187bec3c1d7ceb209a5aa0b30f30e2f5719184950cea668363f13794c51. Recibo de conferência 4e777c522e8b09d5ea6109e4a22721da93b0e703fab35adb6a6f92b8eee5a462. 150 controles consolidados, hashes da árvore atual conferidos: candidato, entrada integrada, leitura específica e relógio. A repetição dos31 controles do relógio foi necessária porque a guarda mudou; os demais resultados foram reaproveitados após conferir os respectivos hashes. ResultadoSHA256 702e845ee137ab79d856ed47d18b9fa2b9619dccccdb7d5f82d99579a3e92c80.

A entrada real checked_registration no /opt/lal_env conferiu cadeia, ativação, pinos e runtime e recusou executar pela ausência esperada de PART_015_BUDGET_START.json. Isso é bloqueio deliberado da fase P, não falha do registro. V1 e árvores antigas intactas. R5:1015 retornos finitos na configuração4096/8192; permanece cobertura finita.

PAGO: preparo, estatísticas auxiliares, emenda, testemunha, controles e qualificação source-only. NÃO PAGO nesta entrega:30 células sintéticas, posterior piloto, calibração física E3.3. Machine hours desta fase:0. Nenhuma semente lida e nenhum descegamento. Nulos não medem p físico antes da calibração. A emenda compra condição operacional, não significância experimental.

Reprodução/auditoria: consolidate_guard_probes.py verifica os recibos; register_v1_1.py registra uma única vez e recusa sobrescrita. Para consultar, usar os artefatos entregues, não repetir a publicação. Axiomas:N/A sem Lean. PróximoT05, depoisT06,T11,T12 e alocação; R7 somente antes do primeiro job pesado.
