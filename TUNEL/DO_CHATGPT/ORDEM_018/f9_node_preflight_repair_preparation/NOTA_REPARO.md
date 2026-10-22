# I02 — preflight das admissões antes de consumir fundo

[REAL documental] Preparação 99e2bfa7-36b8-4e0f-92e7-1a6918e80591. O defeito já registrado no parecer I02 passa a ter um reparo de código concreto: a igualdade prediction_admission_sha256/assembly_admission_sha256 é exigida pelo construtor e novamente por descriptor, chamado antes de qualquer aquisição ou consulta do store pelo callback persistente. A validação posterior do consumidor permanece.

O erro NODE_PREDICTION_ADMISSION encerra o caminho incompatível. A comparação repetida cobre alteração entre construção e próximo callback no regime de objetos confiáveis; não é isolamento contra mutação concorrente ou código hostil. O guard externo continua necessário.

Escolhida alternativa B (comparação interna antecipada) em vez de A (dependência exclusiva da verificação no controlador). Não houve mudança de fórmula, store ou biblioteca numérica. A nova identidade é documental e não concede execução: uma admissão futura deve apontar para ela e para os bytes revisados; autorizações anteriores não são transplantadas.

Verificação desta preparação: AST e hashes, sem importar candidato, inicializar PreparedJoint, abrir matrizes/dados, chamar fundo/solver/WSL ou executar controles. É proposta para revisão independente; não declara teste de runtime, store ou preflight operacional completo. Nenhum AUTH/CLAIM/ROOT_DECISION foi criado.
