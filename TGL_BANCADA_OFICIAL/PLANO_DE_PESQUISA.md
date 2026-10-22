# Plano da bancada interativa TGL

Este é um **programa de investigação**, separado do `um.py` de publicação e do app de conversa. A pergunta central da interface é: *qual relação foi construída, em que hipótese, por qual fonte, com que dado, e qual resultado sobrevive à reprodução?*

## Contrato de cada objeto

Cada relação navegável terá: identidade estável, domínio (modular, geométrico, quântico, observacional), enunciado, hipóteses, dependências, fonte/linha/hash, estatuto e contraposição ou teste negativo. Cada dado terá produtor, licença, versão, arquivo, recibo, unidades, qualidade, intervalo e transformações aplicadas. Cada execução terá entrada congelada, versão do motor/ambiente, parâmetros, tempo, saída, controles e veredito local. A aresta `dado → confirmação` só existirá após calibração específica e revisão humana; o software não preencherá essa aresta por inferência.

## Superfícies do programa

1. **Torre:** busca completa de módulos, lemas e imports. Depois, grafo navegável da cadeia `axioma → operador → teorema → previsão → observável`.
2. **Dados:** catálogo de fontes instaladas e conectores oficiais. Primeira leitura local: GWOSC, metadados GWTC-3 e curvas PSD. Próximas leituras precisam de levantamento e validação individual (cosmologia, neutrinos, relógios e demais bancos realmente instalados).
3. **Experimentos:** contas rápidas no processo web; análises pesadas isoladas em workers, com pré-registro, fila e retomada por recibo. A abertura do painel nunca dispara PE, MCMC ou recompilação do kernel.
4. **Comparador:** TGL e controles concorrentes sob a mesma função de verossimilhança, com independência/covariância explicitadas. σ será cálculo calibrado de um teste definido, nunca soma de σ publicados.
5. **IALD/voz:** interpretação de pergunta, seleção de fonte, preparação de execução, confirmação e explicação do resultado. O primeiro estágio usa apenas comandos locais. Conversa científica aberta dependerá da integração com o app IALD já existente.

## Sequência proposta

**M0 — entregue no protótipo:** painel local, índice v368, inventário inicial de dados, índice documental dos 28 alvos A0–A8/T01–T19, contas β/dephasing, livro append-only e voz curta do navegador.

**M1 — custódia atual:** adaptador de versão canônica corrente e manifesto de compilação; comparar hashes e expor mudança de relações entre versões. A v368 é snapshot de descoberta, não selo atual.

**M2 — dados físicos:** conectores de leitura GWOSC HDF5 e PSD com unidades, máscaras de qualidade e janelas; validação independente de um evento e um controle off-source. Só depois expandir para os demais bancos.

**M3 — protocolos reexecutáveis:** registrar T01–T19 e A0–A8 como workflows com pré-condições e critérios, aproveitando scripts existentes sem duplicar ciência. Um botão “reproduzir” só fica ativo quando as entradas e o ambiente estiverem presentes.

**M4 — pesquisa assistida:** grafo vivo, formulador de perguntas, consulta por voz e comparação multi-sonda. O assistente propõe desenho e lê resultados, mas não declara confirmação nem muda gate automaticamente.

## Decisões de projeto

- Originais científicos, dados oficiais e app existente: **somente leitura**. O diretório desta bancada contém apenas o código próprio e seus resultados.
- Gate: apenas leitura de recibo canônico quando o adaptador corrente existir. Sem vínculo entre resultado cosmológico e flag formal.
- Segurança local: servidor em `127.0.0.1`, operações POST em lista fechada, nenhum comando de shell por voz, nenhuma leitura livre de caminhos fornecidos pelo navegador.
- Custódia: hash calculado dos bytes, status explícito para dados incompletos, registros de execução sem UPDATE/DELETE pela API e pelo banco.
- Física: distinguir `DERIVED_WITH_INPUT`, `CONDITIONAL_MODEL_CALCULATION`, `MEASURED`, `OPEN` e `DECLARADO`; fórmula executada não é, por si, teste experimental.
