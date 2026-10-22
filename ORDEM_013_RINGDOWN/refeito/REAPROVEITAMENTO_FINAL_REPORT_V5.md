# Aproveitamento — gerador documental final v5

[INPUT — achados consolidados de R, encaminhados pelo principal] Sucessor mínimo da v4: acrescentar os custos B1 e explicitar o prazo efetivo da reserva de finalização. Autoria W; o texto real será revisto por R. Não executar o gerador nesta implementação.

Preservados a v4, seu manifesto e os drafts anteriores. Herdadas as correções OPEN versus zero de R-GLOBAL, os custos B2 pinados, a validação de integridade/closure, o anexo E6 e estatutos/limites E7.

`load_b1_costs` confere primeiro o hash da entrega B1 no manifesto B1. Extrai os pins dos dois recibos da lista de arquivos daquela entrega, confere seus bytes e copia `/wall_seconds` e `/cpu_seconds` quando existente. O ajuste e a revisão direta permanecem linhas distintas. CPU ausente na revisão é OPEN, não zero; nenhuma dessas linhas é acrescentada ao ledger contínuo. Sem novo ajuste, KDE, MC ou leitura de amostras.

Ao lado do saldo nominal das 40 h, imprime o valor real de `ORCAMENTO_40H.json /wall_accounting/finalization_stop_utc`, esclarecendo que saldo nominal não é nova alocação de PE/injeções nem extensão da reserva. A checagem de prazo já existente foi mantida.

CLI igual à v4. Destino padrão sucessor: `bis/final_report_v5_001`, sem `--replay`; mesmos nomes de arquivos de draft e manifesto dentro dele, publicação exclusiva. Nenhum draft é criado durante o preparo. Fonte, ficha, checks e preservação estão pinados em `FINAL_REPORT_V5_IMPLEMENTATION_MANIFEST.json`. N/A — sem Lean.
