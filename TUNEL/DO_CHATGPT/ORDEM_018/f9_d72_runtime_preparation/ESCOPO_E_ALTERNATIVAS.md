# Inventário atual de runtime d72 — preparação documental

[INPUT] Escopo delegado por ROOT: inspeção local de identidade, metadados e bytes de módulos/bibliotecas, sem importação científica, execução, instalação, dados, unidade científica ou autorização. O d72 selado permanece intacto. A leitura dos dados de teste e tabelas foi excluída: apenas stat nesses itens.

Alternativas antes do coletor: (A) reler arquivos via UNC Windows, suficiente para bytes, insuficiente para UID efetivo, sys.version, /proc e statvfs POSIX; (B) executar apenas coletor stdlib isolado no WSL existente, com --user nobody explícito, -I -S -B, ler metadados/bytes e devolver JSON por stdout. Selecionada B com autorização adicional ROOT recebida nesta subtarefa. UID padrão root e UID técnico nobody são identidades distintas; nobody não é declarado runtime qualificado. Não criar conta nem escrever no Linux.

O coletor somente admite uma lista conhecida de árvores Python e bibliotecas do inventário histórico como rotas; cada hash é calculado agora. O histórico não fornece os hashes atuais. Symlinks são registrados e o hash do alvo regular canônico é medido com O_NOFOLLOW; aliases não são silenciosamente promovidos a caminhos finais compatíveis. Não há imports candidatos, NumPy, SciPy, CAMB ou bilby. /proc/self/maps pertence apenas ao coletor stdlib, não à futura cadeia científica. Não usar ldd, pois uma inspeção ELF não precisa executar o binário alvo.

Os campos que dependem da importação real permanecerão OPEN; nenhum documento deste diretório será um F9_CURRENT_POSIX_RUNTIME_INVENTORY_V1 admissível. Recursos livres são retrato instantâneo, não reserva nem custo da ciência. Não afrouxar família/prior/contratos. Não editar memórias/ledger.
