[REAL — ficha C7; reprodução numérica separada de calibração física]

# Reaproveitamento C7

Existiam os sete pacotes C7_* originais, reproduce_c6.py e reproduce.py, seus MANIFEST.json::files/shipped_files e os resultados congelados. São reusados sem refazer ciência: cálculos originais em reproduction/ ou reproduce_legacy.py, resultados C4/C6, insumos mínimos per_series[2] com origem e hash. Os wrappers e provas abaixo são novos porque os originais permitiam conflito de saída, resultado não finito, criação interna ou vazamento de temporário.

Novo: pacote principal v3_3; suplementos POSTERIOR/GWTC3/INJECTION v3_2 e IMR/COHERENT/NATIVE v3; bundle único v3_1; guardas de finitude, escopo por leitura, proveniência/licenças, fixture e unidades, output externo e finally. Os scripts e linhas de origem estão no manifesto/árvores congeladas; a tabela reading_scope.json contém dez leituras e seis conjuntos. O construtor é refeito/build_final_bundle_v3_1_013bis.py::main; verificadores são verify_delivery.py e reproduce_c6.py::main.

PAGO: identidade de bytes em extração limpa, 75 resultados C6 reproduzidos, diferença zero, negativas e downgrade testados. NÃO PAGO: calibração de forma de onda, observável de realização única, mapeamento Kerr/laboratório, pasta profunda (aviso MAX_PATH usado conforme F6), nova reprodução científica de todos os suplementos. Esses limites são explícitos nos READMEs. Nenhuma campanha C5 reaberta. As versões defeituosas permanecem ao lado.

Reprodução: conferir o bundle com python -B verify_delivery.py; os comandos completos de replay estão no README e em bis/C7_V3_2_CLEAN_VALIDATION.json. Usar caminhos externos a TODA a entrega, não só ao subpacote. A guarda de cada wrapper protege seu subpacote; proteção automática do diretório-pai inteiro não foi demonstrada. Axiomas: N/A — sem Lean.

Âncoras medidas nos arquivos existentes (arquivo:linha):
- `C7_INDEPENDENT/reproduce_c6.py:25`; SHA256 `916b812ed3b359c42a5929ca7355083ed8229fc563b715ac8b7827753204cc72`.
- `C7_POSTERIOR_REPRODUCTION/reproduce.py:111`; SHA256 `7cb02c6749342c48cfc7df47976247b0baed52f52b9aa6ec195d5bec5b8b18e0`.
- `C7_GWTC3_REPRODUCTION/reproduce.py:113`; SHA256 `710624fc1fee81ec462ea0e7ae95db6f33fe391caf1e7bf6a23c9b5712a14bf6`.
- `C7_INJECTION_REPRODUCTION/reproduce.py:111`; SHA256 `0e6ac6e02af3d098219a58fa928051f7f93454b89b5e97d698fb74a72c848169`.

Abertura: [ENTREGA_013BIS_ABERTURA_operador.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md>) SHA256 `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`
Pacote: [TGL_RINGDOWN_DELIVERY_v3_1.zip](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/TGL_RINGDOWN_DELIVERY_v3_1.zip>) SHA256 `67af7fdd0ff3ed07d20b70702467eab9a97e3d0bd843a93aa08c703cb0ccf20f`
