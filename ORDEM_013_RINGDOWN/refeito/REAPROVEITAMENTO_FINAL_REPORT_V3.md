# Aproveitamento — gerador documental final v3

[INPUT — ordem do operador] Implementar as cinco correções da revisão de completude, em arquivo novo; v2 preservada. A autoria desta v3 é de W. R revisará independentemente o texto real. Esta ficha não é aprovação desse texto nem uma nova autorização de execução.

Reutilizado: `prepare_final_report_v2_013bis.py`, fonte SHA256 `d02181a35ad208260354f0b5b3fba96f72d0fb39412df51478e3cd1453fbcc50`, com a estrutura por alvo F0–F8/E0–E7/TESTE, escopos de parede, separação de contabilidade contínua e publicação exclusiva. Os bytes v2 foram preservados; os pins medidos da implementação constam de `FINAL_REPORT_V3_IMPLEMENTATION_MANIFEST.json`.

Novo na v3:

1. `validate_integrity`: lê o status e cada par esperado/medido, recusa diferenças, confere cobertura contra o inventário baseline pinado e o manifesto entregue da Parte A. Transporta integralmente as exceções de metadados. Não abre arquivos canônicos externos para refazer a auditoria.
2. `verify_extra`: confere SHA256 e tamanho de cada artefato documental do closure; verifica status/checks do closure e revalida arquivos documentais antes de gravar. O JSON de amostras e HDF não são abertos. Um payload listado precisa de pin e tamanho idênticos no recibo de execução E7; o relatório distingue explicitamente esse transporte de pin de um rehash local. Os arrays não são insumos deste gerador.
3. `documentary_sections`: anexo explícito E6 Markdown/JSON, revisão independente vinculada e sinóptico de três rotas × dez leituras × seis grupos. Contagens são cobertura documental, sem recomputar z, N90, densidade, posterior, taxa, Fisher ou MC. Estatutos vêm das células E6 ancoradas em C1, cruzados com E7. Estados/motivos OPEN e ambas as variantes são copiados do resultado compacto E7; nenhum substituto BCW ou modelo físico é criado.
4. Custos: transcrição dos campos observados Kerr, diagnóstico Welch, piloto falho, diagnóstico nativo e execução E7. CPU/parede/soma de filhos ficam separados; não se somam ao ledger contínuo. As cinco alternativas preservam estimativas null como OPEN e alocação zero como decisão. O total não é apresentado como inventário perfeito de custos isolados.
5. Comando de replay concreto no relatório, usando os argumentos efetivos e novo diretório. Esta ficha e todas as fontes documentais consumidas entram no mapa de hashes.

CLI: preservados `--e6-result`, `--e7-review`, `--integrity-receipt`, `--extra-manifest`. Adicionados `--e6-review` (padrão: revisão 002 aprovada), `--output-dir` (padrão: `bis`, nomes de saída iguais aos da v2), `--replay` (somente destino novo e isolado dentro do pacote; não publica e não reabre o orçamento). O modo normal respeita tanto 40 h quanto `finalization_stop_utc` da alocação. Replay documental posterior pode conferir fontes imutáveis sem criar consumo científico; carimbo e intervalo serão do replay, expressamente identificados, não reprodução byte a byte.

Saídas, somente quando o principal executar: `FINAL_REVIEW_DRAFT.md` e `FINAL_REVIEW_DRAFT_MANIFEST.json`. Nunca substitui destino existente. Nenhuma entrega final no túnel é escrita pelo gerador. O publicador v2 permanece separado e exige o parecer independente do draft exato.

Não feito nesta implementação: execução do gerador, publicação de draft, rerun E6/E7, leitura do posterior de 92 MB/HDF, nova ciência, alteração de v2, produtores congelados ou vereditos. Verificação somente sintática/AST e fixtures de metadados artificiais de funções isoladas. Falhas, se ocorrerem, devem permanecer nos recibos próprios. N/A — sem Lean.
