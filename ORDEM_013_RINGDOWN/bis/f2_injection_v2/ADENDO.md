[REAL operacional — correção R1 sob Python otimizado; sem nova ciência]

# F2 injeção — adendo de robustez v2

Os resultados reutilizáveis em E1 são os originais auditados em `bis/f2_injection/`, com parecer `bis/F2_INJECTION_INDEPENDENT_REVIEW.md`. Esta v2 não substitui, reemite ou recalcula esses resultados. A aprovação descritiva não cobre lnB, curva c(SNR) ou cobertura frequentista. Na tabela original, suporte local usa KDE das 20.000 linhas, enquanto conteúdo em GR usa treino 16.000/consulta 4.000.

Quatro scripts copiados ao lado. Todas as guardas assert foram convertidas em if com exceção explícita (ValueError; FileExistsError para destino). A publicação final usa os.link(temp,destino), que recusa destino existente inclusive na corrida após a primeira checagem. Os bytes temporários continuam conferidos explicitamente. Sem fallback para replace; filesystem sem hardlink resulta em falha visível. Temporário próprio é removido ao encerrar a tentativa de publicação. Nenhum arquivo preexistente é removido. Caminhos internos de produtos foram apontados para f2_injection_v2. A transformação AST preserva os cálculos; formatação/comentários de código são normalizados. Não há outputs científicos nesta pasta.

Teste executado: Python 3.14 com -B -O, somente AST extraída das funções de escrita/publicação e das guardas de pin/destino, em filesystem mock em memória. Os quatro scripts geradores NÃO foram executados/importados. 12 casos negativos passaram: destino existente, pin de fonte incompatível e destino criado concorrentemente na publicação final, por script. Os blocos mock também foram compilados optimize=2. Os nove arquivos originais (quatro scripts e cinco produtos) permaneceram com os hashes anteriores. Não houve acesso HDF5, posterior ou strain.

Comando executado:
`C:\Python314\python.exe -B -O "C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\f2_injection_v2\test_guards_mock.py"`

O próprio teste grava recibo exclusivo e recusa sobrescrevê-lo numa repetição; para repetir, usar cópia isolada autorizada. Tempo de parede retornado pela ferramenta para esse comando: 1,4506248 s (inclui inicialização Python), sem campanha científica. O relógio contínuo da Parte B continua governado pelo recibo do operador; não foi alterado.

PAGO: robustez das guardas nos casos mock testados sob -O; integridade dos originais. NÃO PAGO: reprodução científica v2, teste integrado HDF5, certificação de hardlinks em todos os filesystems ou novo aceite científico. Não foi criado resultado de injeção v2. Axiomas N/A; teoremas 0.

Arquivos escritos nesta correção:
- inspect_injection.py
- diagnose_injection.py
- check_contract.py
- write_report.py
- MANIFEST.json
- test_guards_mock.py
- GUARD_TEST_RESULTS.json
- ADENDO.md
- RECEIPT.json

Os hashes das quatro fontes/copias estão em MANIFEST.json; RECEIPT.json registra os demais bytes produzidos. Nenhuma entrega formal ou memória foi alterada.
