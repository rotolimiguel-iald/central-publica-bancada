# F0.3.B2 — revisão independente do motor e correção candidata

[REAL — sondas sintéticas e código] Reivindicação 632. Revisão dos sete módulos, seguida de correções expressamente autorizadas pela coordenação. Os bytes anteriores dos três módulos alterados ficam ao lado (`*.before_r1`). O candidato foi modificado; nenhum original da Bancada ou memória foi tocado.

## Achados e tratamento

1. **Graus de liberdade:** em um modelo sintético de seis observações, três parâmetros livres e uma magnitude perfilada, a saída dizia gl=3; o valor coerente é 2. Agora o retorno subtrai e nomeia `M_supernova` nos dois leitores de supernova.
2. **Combinação de convenções:** o default com fundo contendo β podia ser cobrado junto com transporte local/acumulado, que o próprio contrato descreve como dupla contagem. A validação conjunta atua só no leitor selecionado. TGL/eff + Planck/DESI foi preservado. Pantheon simples recusa uma lei SN que seu código não implementa.
3. **Rótulo:** uma combinação mista era chamada de artigo só por ter beta_no_fundo=nao. Agora artigo exige equivalência integral ao preset; a combinação mista exibe as opções.
4. **Fonte DR1:** os cinco coeficientes tinham citação histórica, mas não pino primário no contrato da função. O recibo agora declara `DECLARADO`, SHA primário nulo e admissão não verificada. Nenhum valor foi alterado nem houve nova admissão.

## Verificação

Estado: `FIXED_CANDIDATE_TESTS_PASS`. Harness original e regressões materiais foram executados em subprocessos novos com `-B`; logs incluem comando, início, fim, segundos e saída. Só foram usados resíduos e centros sintéticos. A extração de arquivos e os pins não equivalem a validação física.

O JSON contém hashes anteriores/atuais, linhas das correções e recibos. A guarda canônica foi simulada pelo harness; a integração com manifesto real fica com a coordenação. Não houve ajuste observado, CAMB novo, abertura de rito nem mudança de gate.
