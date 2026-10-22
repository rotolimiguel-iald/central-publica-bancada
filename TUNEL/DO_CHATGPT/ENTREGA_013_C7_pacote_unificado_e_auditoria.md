[REAL — reprodução e custódia verificadas; predições DERIVED/INPUT/CONJECTURE; interpretação NÃO-CEGA]

# Ordem 013 — pacote unificado e auditoria de cobertura

UTC: 2026-09-22T03:00:40.904623+00:00. Axiomas: N/A — sem Lean novo.

## Critérios pagos

- **PAGO:** GWTC-3 recalculado em pasta limpa, com nova extração dos 18 HDF5 do ZIP público já conferido. 6598 campos numéricos coincidiram exatamente; identidades, seleção e vereditos também. A seleção de dez eventos foi novamente extraída da Tabela 13 e das exclusões do artigo.
- **PAGO:** oito controles adversariais recusaram arquivo adulterado, caminhos inválidos, identidade, veredito, contagem e medida alterados.
- **PAGO:** quatro pacotes prévios reunidos em `cache/TGL_RINGDOWN_DELIVERY_v1.zip` (10583656 bytes; 183 entradas). Extração nova validou 182 arquivos do manifesto. Os bytes das entregas anteriores foram preservados.
- **PAGO:** `C7_DELIVERY_OVERVIEW.md`, resumo científico em inglês com as quatro respostas, taxas por leitura, exemplo de distribuição de ln B, dados reais, comandos de reprodução e limitações.
- **PAGO:** `C7_REQUIREMENTS_AUDIT.json/.md`, inspeção de 14 grupos de requisitos e 51 artefatos com hashes. Separação explícita entre cálculo concluído e critério científico reprovado.

## Critérios não pagos e escopo

- **NÃO PAGO — aceitação científica C5:** nenhum grupo FULL_IMR testado passa conjuntamente os critérios de viés/cobertura nas duas famílias e nas duas amplitudes injetadas. Não é consertado por escolher só células favoráveis.
- **PARCIAL — comparação externa C6:** oito posteriores pyRing comparados, mas não reprodução idêntica de modelos/priors; não há produto 10,5 tM no release inspecionado. O próprio C6 foi integralmente reproduzido.
- **ABERTO por escopo:** identificação física de partição, relógio e desenrolamento; a bancada não fez essa escolha. A realização finita condicional não demonstra um estado global de Kerr.
- **PENDENTE de revisão final:** conferir cada exigência granular contra a matriz consolidada, especialmente colunas C1 e alcance de validação externa. O objetivo permanece ativo; não se declara integralmente concluído.

## Resultado que pode ser comunicado

No ramo B, no GW250114 de referência: Gamma ≈ 4,95 s⁻¹, Gamma/omega ≈ 0,00316 e delta_tau ≈ −0,01985, sob o relógio de massa assumido. A medida primária de strain dá ln B ≈ −0,002595. Os catálogos corrente e GWTC-3 dão −1,80828 e −0,820834 em seus respectivos recortes. Não multiplicar esses resultados: há dados sobrepostos. Os vereditos continuam INCONCLUSIVE_SYSTEMATICS; nenhum desses números é sigma.

## Reprodução

Descompactar `TGL_RINGDOWN_DELIVERY_v1.zip`, ler `README.md` e executar `python verify_delivery.py`. Cada uma das quatro subpastas tem manifesto e instruções próprias. Para o GWTC-3: `python reproduce.py full --archive-cache /path/to/public` ou `--download`; o teste desta rodada usou o ZIP local verificado, não repetiu a transferência.

## Aproveitamento e memória

Reaproveitados os três scripts científicos GWTC-3 sem alteração. Acrescentados um leitor de ZIP com hash/CRC, comparação exata de identidades e empacotamento. Nenhuma função nova em um.py, nenhuma fonte canônica modificada. O registro C6 e seus insumos continuam íntegros. STATUS, PROGRESSO e manifesto local recebem backups imediatos byte a byte.
Notas antigas de pendência foram corrigidas por adendo e índice: a recuperação de trajetórias, os posteriores, as injeções, o strain e o GWTC-3 já têm execução e reprodução. Não é necessário refazê-los. Falhas de acesso WSL, codificação de saída e tabela Markdown estão preservadas no STATUS; não alteraram resultados científicos.

## Custódia medida

| Artefato | SHA-256 |
|---|---|
| `package_reproduce_gwtc3.py` | `710624fc1fee81ec462ea0e7ae95db6f33fe391caf1e7bf6a23c9b5712a14bf6` |
| `build_gwtc3_reproduction.py` | `b4ad14233f9cf912bc92317765f3d62d06b542d4a0d3a337d3e3ab04f771ea18` |
| `verify_gwtc3_reproduction.py` | `5910ad8cb99ab56766d3daa4622603abf78e9bfba57b50f79f862237756a987e` |
| `C7_GWTC3_REPRODUCTION/MANIFEST.json` | `77f9f8883837fcc34899f962991560a92b19e9a9e1fefa9804f7c1f9eada99b5` |
| `C7_GWTC3_REPRODUCTION_VALIDATION.json` | `900df79b4aa68bd80cb0b555d823c739e3beb726de2aa844dbf0deb0c0f8299e` |
| `cache/C7_GWTC3_REPRODUCTION_v1.zip` | `8b0c8fcffa7ce36616c7dab39b963c1f343c9e770c620471f0ddc46aabe70407` |
| `build_delivery_audit.py` | `3d75364fce3a7cbe40280a7cec95035639da1794ebb2812ca037bec1f1833a62` |
| `C7_REQUIREMENTS_AUDIT.json` | `f84ac921fad188b21ae0c8a9b65b4295740196d9341efaf04b5d42e93071b591` |
| `C7_REQUIREMENTS_AUDIT.md` | `9646a2f0bbd25dac918e9962d692708db32c7b279633635003dbbe2d6ce078e8` |
| `C7_DELIVERY_OVERVIEW.md` | `218a3de59715c9b1c610a1fd6e59143fe347eaf088cac5b3b1cfbc5ae7f48066` |
| `build_delivery_bundle.py` | `0c66c23cc304edbe266bc1e8193d53be1f892a0ada76e606faf498e9e76f5ae4` |
| `C7_DELIVERY_BUNDLE_VALIDATION.json` | `f557751d3f9a82bce3f70eeab551771aa9849e71f3b79035ee0dae3bed53952b` |
| `cache/TGL_RINGDOWN_DELIVERY_v1.zip` | `45c561e1bde379d577b55abc7684b5fdce33ab1008d6b1eba1e092f147eb4cf0` |
| `cache/MANIFESTO_DOWNLOADS.json` | `de12d0611043dfd2d0d6d9db1bbedf3d8e2cd54c23bdb10e466b60ec5efc80d0` |
