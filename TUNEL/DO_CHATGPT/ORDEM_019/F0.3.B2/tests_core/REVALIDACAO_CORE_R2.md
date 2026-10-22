# F0.3.B2 — revalidação independente das correções centrais

[REAL — controles sintéticos] 31 testes aprovados, EXIT 0. Fontes conferidas por hash antes/depois, sem mudança durante a execução. O recibo CORE_RECEIPT_R2.json contém comando, início, fim, tempo, pinos e hash do log. Esta revisão não editou candidate.

Cobertura: programa/selo/código/fontes/manifesto adulterados; versão divergente apesar do pin; fonte desconhecida e bytes alterados; exigência dos cinco módulos mandatórios; geração do manifesto em source_bytes; raiz padrão; rejeição de NaN/Inf/booleanos; HTTP com opções/flags inválidas, Content-Length inválido ou corpo curto, timeout; atividade de carga e requisição síncrona; limpeza do contador após exceção; quiesce e recusa da execução de rito GW; recusa de escape textual da pasta UI; nova verificação canônica ao entregar resposta; leitor GW com fs inválido, forma/dtype inválidos, NaN/Inf, grade irregular e deriva temporal acumulada.

A primeira execução encontrou duas falhas novas (28/30): deriva acumulada no grid GW e corpo HTTP curto contendo JSON completo. A coordenação corrigiu ambos. Acrescentado teste de timeout, a segunda execução ficou 31/31. FIRST_RUN_SUMMARY.json preserva a ocorrência. A correção da grade foi testada com GPS sintético da ordem de 1e9 s.

Os testes importam o servidor sem iniciar Motor; simulam a leitura de alpha ao importar GW. Nenhuma porta foi aberta, nenhum dado observado foi lido, nenhum ajuste físico foi rodado e nenhum arquivo da Bancada instalada foi escrito. Suíte: C:\Python314\python.exe -B -X utf8 tests_core\run_core_suite.py <rótulo_novo>; o rótulo gera artefatos novos. Executar como processo separado, conforme o comando pinado.

Alcance: verifica as recusas e a integração em cenários sintéticos delimitados; não certifica um resultado cosmológico, precisão de um pipeline observado, admissão científica de fontes ou significância de 5 sigma. Nenhum gate mudou. Implantação e manifesto final pertencem à coordenação.
