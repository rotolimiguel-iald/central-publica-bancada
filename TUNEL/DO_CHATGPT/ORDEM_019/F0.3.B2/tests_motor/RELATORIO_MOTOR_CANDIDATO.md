# F0.3.B2 — motor candidato, revisão das ressalvas B1

Autor: codex-gerente-tgl / nu2_theory_sources. Reivindicação 632. [REAL — código candidato e controles sintéticos] Consulta Nós Vivo: F0.3.B2 ainda ausente do grafo; fallback F0.3 reutiliza a memória/custódia v391. Fonte de trabalho: relatório R2 da F0.3.B1 e os sete módulos copiados pelo coordenador. Nenhum original da Bancada, memória ou quadro foi escrito por esta subunidade.

## Entrega

- O default é TGL/eff; selado, corrigido e artigo permanecem escolhas explícitas. As curvas recebem as mesmas opções da predição, incluindo beta_no_fundo. São curvas geométricas BAO: R e leis SN/CC não são seus eixos.
- Motor e fachada recusam conjuntos vazios, desconhecidos, duplicados ou sobrepostos: DR1/DR2 e qualquer par no grupo Pantheon/Pantheon+SH0ES/SH0ES/SH0ES_local. Sem conjuntos, usa planck_comp+desi_dr1. Esta recusa conservadora não afirma que as demais fontes sejam independentes; uma likelihood conjunta exige contrato próprio.
- Entradas numéricas devem ser finitas e não booleanas; quantidades inteiras e flags são tipadas. NaN de chi2/resíduo dentro do suporte é falha. Fora dele, a proposta de MCMC recebe -inf, rejeição normal explícita.
- Motor.limites é a interseção instrumental da tabela com limites_declarados. Motor.suporte e todas as operações devolvem os dois, intervalos abertos, prior_amplo_coberto=false e evidencia_prior_amplo_autorizada=false. Ajuste restrito e posterior uniforme nessa interseção são diagnósticos, sem instituir um prior científico novo. A amostragem inicial e as derivadas centrais do ajuste respeitam esse suporte.
- A cauda do posterior não produz p/z frequentista; significancia é null na amostragem, e o livro registra p_local null. A cauda empírica zero não é probabilidade zero. Šidák tem p_sidak_exploratorio/z_sidak_exploratorio; p_global/z_global são null e global_certificado=false. Wilks e JtJ permanecem aproximações locais declaradas, sem calibração nova.
- Toda operação Evidencia confere require_current antes e depois; o assíncrono confere no início e no fim. A identidade do primeiro recibo fica vinculada à instância. Mudança de manifesto/programa/selo exige recarga. canonical_guard é injeção no construtor para testes; o padrão usa a guarda real e root do motor.
- Fontes passam por read_checked, que lê uma vez, verifica o pin do manifesto canônico e entrega os mesmos bytes ao parser. alpha delega read_alpha, mantendo igualdade histórica do pipeline como controle numérico, sem certificação de física. NPZ e manifesto, JSON, textos e PDF Chen são obrigatórios/pinados. O pin é custódia, não admissão científica.
- Cache Pantheon só é usado com pin externo e cache_sha256 interno coerente com a fonte. Cache legado sem esse campo é ignorado; a fonte pinada é parseada em RAM. A carga não cria/sobrescreve caches. A docstring antiga que dizia STAT+SYS desligada foi corrigida no candidato.
- O teste encontrou também conexões SQLite não fechadas: Livro._con agora encerra a conexão em finally, além de concluir a transação.

## Interfaces para integração

Evidencia(motor, livro, canonical_guard=None); _curvas(th, opcoes=None). Motor.limites_declarados, Motor.limites (efetivos), Motor.suporte. TabelaCAMB.suporte/proveniencia. fontes.read_checked/json_checked. Guarda externa canônica: read_alpha e verify_source_bytes. Os clientes devem aceitar significancia=null no posterior e p_global/z_global=null nas aproximações locais. A fonte/default de modo deve ser tgl na UI e nas chamadas que não pedem reprodução histórica.

## Verificação

17 testes sintéticos passam, EXIT 0. Log TEST_RUN_R2.log traz comando, início/fim, segundos e saída integral. Inclui curva artigo igual ao ΛCDM de referência para c=0; curva TGL diferente, seleção adversarial, finitude/bool, identidade alterada antes do assíncrono, ajuste quadrático sintético no suporte, interpolação de tabela sintética/pin errado, cache legado sem escrita, cadeia gaussiana sintética e ausência de p frequentista no posterior. Não houve instanciação de Motor real, fit observado, leitura de arrays observados, CAMB novo, chamada a provedor, nova significância ou escrita na Bancada. A primeira rodada passou 16 testes e falhou só na limpeza SQLite; FIRST_RUN_SUMMARY registra a causa e a correção. -B evitou pycache.

O teste não certifica precisão cosmológica dos modos, calibração de 5 sigma, convergência de qualquer cadeia real nem implantação. A auditoria/instalação e o manifesto final são da coordenação. Não foi medido poder e nenhum gate mudou.
