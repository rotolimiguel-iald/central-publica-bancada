# Alternativas antes do código

[INPUT] Preparação local da ligação somente leitura I02 → ponte I05/I06 V2. Nenhuma execução, dado observado, processo, provedor, decisão ou claim autorizado por este pacote.

A — escolhida: reutilizar DurableStore.lookup e validadores NodeContext/ThetaIntegrator, sobre stores POSIX privados já abertos e documentos originais retidos; registry do processo leitor valida módulos realmente carregados. Não invocar callback de nó, acquire, commit, prepare_joint, solver ou reconstrução. lookup faz fsync de diretório por contrato; não publica arquivos. Leitura sem emulação Windows.

B — reconstruir consumidor/joint e executar DurableNodeCallback para aproveitar cache. Rejeitada: callback pode acquire/recalcular e prepare_joint reabre matrizes; isso excede recuperação somente leitura e introduz repetição indevida. Reimplementar parser de store inteiro seria outra duplicação evitável.

[OPEN] O produtor retém request/decision/coupling, mas não todos os bytes theta_plan/consumer_admission/estrutura referenciada. Entradas originais ausentes recusam; não regenerar. O selo externo ainda exige exit zero do próprio parent: intake precisa de evidência externa independente já verificada, não digest escolhido da carga. Não existe resultado d72 executado por esta preparação.

[DERIVED] Contextos usarão y_native_f64le, C_native_f64le, structure_sha256, references.fixed_affine_support.sha256, configuração do plano e pin da admissão. Suporte é identidade documental de engenharia, não certificado geométrico. Nenhuma abertura/certificação L/U/SF nova.
