[REAL — fechamento documental independente de C7-R4; sem nova execução científica]

# C7 v3_3 — fechamento de R4

Data UTC: 2026-09-22T18:51:18.150914+00:00.

**C7-R4 fechado na v3_3.** As 78 atribuições agora cobrem exatamente os arquivos esperados, sem duplicatas, com SHA256 calculado dos bytes finais; README e OVERVIEW conferem. SHIPPED_ATTRIBUTIONS não se auto-hasheia: sua identidade é coberta pelo manifesto externo. C7-R1–R3 permanecem fechados pelo parecer v3_2, com os mesmos bytes executáveis. Este fechamento não quita os achados separados dos wrappers dos suplementos.

Conferi 79/79 arquivos do manifesto por tamanho/hash e todos os membros/bytes do ZIP. Versus v3_2, a única alteração entre os arquivos embarcados listados no manifesto é `provenance/SHIPPED_ATTRIBUTIONS.json`; o próprio MANIFEST também muda, como esperado. Todos os outros 78 arquivos, incluindo executáveis, ciência congelada, evidência e textos, são byte a byte idênticos. A v3_2 permanece íntegra.

O builder conclui os textos antes das atribuições e aplica guardas explícitas antes da escrita do pacote. Controle independente do bloco real por AST sob optimize=1: íntegro passa; ausência, duplicação, linha extra, hash incorreto e README alterado após o hash são recusados (cinco negativas). Não executei o builder nem a C6.

O recibo documental aponta corretamente para o replay v3_2 já conferido, com SHA256 correto e identidade dos arquivos de execução. Isso transporta a evidência daquela execução sobre os mesmos bytes; não é uma execução nova na v3_3. As unidades frescas informadas no recibo são [DECLARADO — registro do construtor]; esta revisão acrescenta verificação independente dos bytes e das guardas documentais. `temporary_removed=true` do controle documental não traz o caminho temporário: sua ausência física não foi reconstatada por este parecer. A remoção dos temporários do replay v3_2 já foi conferida no parecer anterior.

Persistem os estatutos científicos e as limitações dos relatórios anteriores; licença não foi reinterpretada como autorização geral do código, nem PASS numérico como confirmação física. Sem PE/C5/campanhas, memória/canônico ou edição de produção.

Controle: `bis/c1_review/c7_v3_3_documentary_checks.py`; resultados em `c7_v3_3_documentary_results.json`.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
| `refeito/build_independent_v3_3_013bis.py` | `d3889d9da68a7e33d767137714ad639210fb8ebd2d564fc46c6040be4ca1b5bb` |
| `C7_INDEPENDENT_v3_3/MANIFEST.json` | `859f59a4258215f6dd2e467087fbab4cb09b33c1522c5424d8575c6a439f616b` |
| `cache/C7_INDEPENDENT_v3_3.zip` | `bf10adf6a8479ca9e299f86bdf2c791ffd02843f0d5e9df08ac466464005f72a` |
| `C7_INDEPENDENT_v3_3/provenance/SHIPPED_ATTRIBUTIONS.json` | `44ac110b48e3081e55e3eb77d375c0aede80cb349859e979b657c09a4e17bafd` |
| `bis/C7_V3_3_DOCUMENTARY_VALIDATION.json` | `e57039af2d4746ffd4f8e19dd909fd2fa15a8ca6c8939e26f6088aaa5a9cb3de` |
| `bis/c1_review/c7_v3_3_documentary_checks.py` | `5ec6eb298e93e0af37af05dbfb188b1400f71cad0633c4e6924704369a8c7d98` |
| `bis/c1_review/c7_v3_3_documentary_results.json` | `e5d99c7e176fe39b8434920309702b3d91293297b5df769e0cd809d9ca694d4c` |
