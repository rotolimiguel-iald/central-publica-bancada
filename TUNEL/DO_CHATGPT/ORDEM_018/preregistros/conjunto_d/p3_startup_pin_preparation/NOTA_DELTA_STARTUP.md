# P3 — sucessor imports-only com pin nominal de startup

[INPUT] ROOT autorizou preparar, sem executar, o sucessor isolado da preparação 2bfd4665-a7e7-410a-aeb3-0406f90a596f. A inspeção 4a0d70f2-be3c-4d21-9257-9b0c4d7e537b continua terminal e não pode ser repetida. Esta preparação tem identidade d50bb889-1682-4320-8106-9bdbd8368257, registrada antes do código no mapa677.

[REAL — bytes/AST] O delta de código integral está em DELTA_FONTES.patch. prehook_imports.py ganha somente um ramo de inventário para o arquivo nominal pinado de sitecustomize; qualify_imports.py troca apenas a constante de identidade. O driver empacotado é idêntico ao da preparação anterior. As outras quatro peças e as 12 dependências conservam também seus pins originais: guard, checkpoints, source, validador e launcher não mudaram. Não há novo runner científico.

## Causa e alcance da correção

O diagnóstico stdlib sob nobody/venv, com -I -B, mediu 33 módulos iniciais e quatro entradas sys.path. Entre os módulos:15 sem arquivo,16 sob a stdlib,1 marcador virtual stdin do diagnóstico e somente sitecustomize fora das categorias. Não havia NumPy/Bilby/Dynesty/LAL. A classificação anterior usa caminhos resolvidos: o alias /usr/lib/python3.12/sitecustomize.py é um symlink para /etc/python3.12/sitecustomize.py e, portanto, não satisfaz o ramo de diretório stdlib.

O arquivo de155bytes foi lido/hashado como dado. Seu texto tenta importar apport_python_hook, suprime ImportError e chama install somente no ramo de sucesso. apport_python_hook não constou do snapshot inicial; isso não é atestado geral de indisponibilidade ou ausência de todo efeito. Python pode executar sitecustomize automaticamente ao iniciar; não foi acrescentada importação explícita desse módulo. -I não equivale a -S.

SYSTEM_STARTUP_PIN.json traz hash medido, caminho canônico, alias e origem documental. O novo ramo exige que a única chave dessa classe seja /etc/python3.12/sitecustomize.py, que o nome do módulo corresponda e que o alias resolva ao destino exato. Reusa _module_pin/require_pin para conferir bytes, SHA e __file__/__spec__. Não permite o diretório /etc, outros módulos de startup, troca de conta/permissões ou alteração da política de inicialização. A allowlist científica e o guard continuam intactos.

## Alternativas

A — Pin nominal do arquivo já observado, com alias e conteúdo conferidos. Resolve precisamente a falha de classificação encontrada, conservando a inicialização atual. É a alternativa autorizada para esta preparação.

B — Desativar site por -S e reconstruir explicitamente os caminhos das dependências. Muda a inicialização e pode afetar a descoberta do venv; exigiria outro contrato. Não foi adotada, implementada ou ensaiada.

O inventário de33módulos não é uma prova do fecho de todos os imports científicos posteriores. Um novo arquivo não admitido continua a produzir falha visível; não há fallback nem promoção automática de um caminho visto para caminho autorizado.

## Inspeção futura e limites preservados

COMANDO_CANDIDATO.json contém o comando concreto do mesmo runner imports-only, com nova raiz e placeholder para o hash de uma decisão ROOT futura. Transporte proposto: WSL Ubuntu-24.04, usuário nobody, --exec, três variáveis de thread iguais a1. Não se criou ROOT_DECISION, AUTH, CLAIM, diretório de consumo ou UUID de execução. A autorização anterior não é transferida ao sucessor.

Conservam-se120s nominais totais,110s de trabalho, um filho,8GiB de endereço, CPU100/105s e2MiB por arquivo do filho após admissão. Os recibos são provisórios até exit0 externo e verificação do prazo. A limitação não bloqueante P3PKG-01 permanece: timeout muito precoce pode não registrar o PID do filho. Não foi corrigida para manter o delta restrito; não se promete hard realtime nem contenção de inicializadores nativos/descendentes.

Driver e launcher de PE conservam PREPARATION_ONLY incondicional. A ciência, seus parâmetros, guard e escopo continuam bloqueados. O próximo passo é revisão ROOT deste delta e, somente se houver nova decisão específica, uma inspeção de imports própria. Mesmo eventual êxito dessa inspeção não qualifica waveform, likelihood, PE, recuperação ou cobertura. A qualificação científica permanece uma etapa separada com contrato, identidades e entradas próprias.

FONTES_E_LINHAGEM.json liga os pins da falha e do diagnóstico completo. As conferências desta preparação são AST/bytes; nenhum candidato ou biblioteca científica foi importado, nenhum WSL foi invocado para este sucessor, nenhuma ciência foi executada e nenhum observado foi aberto. O pacote anterior e seus logs/claims permanecem preservados.
