[REAL — higiene e integridade documental; limitações explícitas]

Abertura015SHA256: dbd0a307438dda2969a21baf64665d54e8b70fb84c3fe10f8c233ddeac736610
Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

As três pastas EXATAS da T13 foram removidas pela identidade criadora; o junction e o symlink foram desvinculados sem seguir destinos e sem takeown. Journal: bis/015/t13/WINDOWS_CLEANUP.json e WSL_UNLINK.json. Nenhuma ampliação de caminho. A pasta 214951 é distinta da 214938 autorizada e permanece fora do escopo; a nova auditoria a registra como ilegível no sandbox e excluída da custódia por caminho: ['C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e2_publication_census\\CUSTODY_TRANSFER_FIXTURE_20260922T214951\\cache\\E2_PRIVATE'].

Semente REAL: cache/E2_PRIVATE/BLIND_SEED_V1.bin; o caminho bis/cache da ordem não existe. O sandbox não conseguiu stat antes/depois das remoções Windows. No WSL, antes/depois da desvinculação, 32 bytes e mtime_ns 1790113483194878000 idênticos. Nunca se leu conteúdo. A limitação do primeiro intervalo permanece; não declarar uma conferência completa que não ocorreu.

Novo harness t13_acl_fixture_harness.ps1: finally cobre a criação e falha da fixture. Cópia pinada do helper cria/verifica ACL nativa; falha injetada rc1; finally executou e removeu a fixture. O reparador foi copiado sem executar o main real; limpeza após transferência entre identidades não foi reencenada. Cinco wrappers de reprodução já tinham finally, conferidos por AST e hash em EXISTING_FINALLY.json; não criamos versões redundantes nem reabrimos campanhas.

final_integrity_015_v2.py acrescenta onerror. A primeira execução no sandbox falhou ao hashear um.py; tentativa preservada. A repetição somente de leitura no host conferiu 217 insumos,31 fontes,47 entregas A: quatro diferenças canônicas contra o retrato antigo, zero diferença nos insumos/entregas A e zero arquivo excedente. A v3 conserva erros individuais de leitura e registra a pasta ilegível 214951; seu estatuto NÃO é PASS. Recibos: FINAL_INTEGRITY_015_20260926T102556230095Z.json e FINAL_INTEGRITY_015_v3_20260926T102634778604Z.json. As diferenças não foram corrigidas sobrescrevendo fontes.

Inventário sem conteúdo nem remoção: guard_7h3lo515=10928466 B; native_package_tamper=204170 B; delivery_fresh=39606661 B; delivery_v2_fresh=120653732 B. O primeiro levantamento Windows ficou parcial por caminhos longos; o WSL mediu os quatro sem erros. Papéis inferidos pelos nomes históricos; apagabilidade não demonstrada, mantidos para auditoria de referências.

Intervalo documentado desde o primeiro script: 0.1137h; comandos leves, pesada0h, chamadas externas0. T13 aceita como MEDIDA de higiene com limites nomeados. Próximo ramo: T03, preparação da V1.1 sem iniciar relógioR7 nem dados cegos.
