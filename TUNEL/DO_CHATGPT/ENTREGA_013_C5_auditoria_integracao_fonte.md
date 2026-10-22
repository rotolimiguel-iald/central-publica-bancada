[REAL — resultados numéricos e auditoria; OPEN — aceitação científica da fonte não linear]

# ORDEM 013 — Auditoria da integração de fonte

2026-09-22T05:23:34.904279+00:00

O piloto de amostragem aninhada terminou com 24267 chamadas e sem atingir a
meta de convergência. ESS das componentes: [1.004503652320579, 20.188395533331473]; componentes
aprovadas no critério de pesos: 0 de 2400.
Esses fatores de Bayes NÃO são uma entrega científica aceita. Dobrar a taxa da forma
de onda passou no controle dos pontos relevantes; a integração estatística falhou.

No oráculo analítico, balancear componentes melhorou os pesos, mas duas sementes ainda
diferiram 0.398763109 em ln B (critério: 0,2). A etiqueta
de consistência ampla do teste não substitui essa exigência. A alternativa de amostragem
independente obteve erro máximo 0.0132514732 em quatro
controles de integrais conhecidas; isso valida seu mecanismo, não o modelo astrofísico.

## Integração independente no problema real

| rodada | propostas | avaliações dentro do prior | conjuntos com precisão mínima |
|---|---:|---:|---:|
| inicial | 4096 | 2303 | 0 / 1200 |
| adaptada | 16384 | 13021 | 0 / 1200 |

A rodada adaptada usou 24 componentes Student-t aprendidas de TODOS os pesos do piloto.
Dez por cento das propostas vêm do prior original completo; pontos fora do cubo têm
integrando zero e continuam no denominador. O prior físico, os parâmetros, o modelo e
os intervalos de ruído não foram reduzidos para conseguir passar. Aprender uma proposta
não é restringir o prior; a integral usa o quociente pela densidade da proposta.

Pior ESS na rodada adaptada: 1.00000004;
maior peso individual: 0.999999981;
maior erro estimado de Monte Carlo em ln B: 0.760440425.
Auditoria aritmética/taxa: PASS_ARITHMETIC_AND_RATE. Critérios completos de precisão:
False. Uma repetição independente da proposta final
e a calibração contínua do parâmetro de dephasing ainda faltam.

Cada conjunto simulado é analisado separadamente. Os 1200 conjuntos reutilizam 50
intervalos pareados por detector; não são eventos independentes. O4/O5 são sensibilidades
de cenário. Não houve leitura nova do evento, alteração da C6, do um.py ou do gate.
SEOBNRv4HM continua na matriz de injeções e controles; sua integração como família de
recuperação ainda está pendente. A confirmação física e qualquer significância nova
permanecem não estabelecidas. N/A — sem Lean.

Falhas operacionais preservadas: ordem de importação do dynesty local no oráculo
balanceado; booleano NumPy não serializável no primeiro registro do oráculo independente.
As cópias de bytes estão ao lado dos scripts corrigidos. Nenhuma delas foi falha de física.

## Reprodução

## Causa numérica localizada e próximo passo

A fase 22 no pico gira 35.7757518 rad na varredura de massa
60–100 massas solares e 12.2003879 rad na varredura
do spin comum −0,25 a 0,25. A fase de referência, portanto, pode criar muitas curvas
estreitas no posterior. Isso é um diagnóstico do gerador, não uma identificação física.
`PEAK_PHASE_COORDINATES.md` deriva uma mudança EXATA de variável que conserva o prior:
fase no pico uniforme em [0,π), somando as duas pré-imagens orbitais com pesos 1/2.
É essencial conservar ambos os ramos e todas as harmônicas, inclusive ímpares. A soma
é invariante à troca de ramo do argumento complexo. Implementação e validação de
quadratura ainda não foram feitas. Essa é a próxima ação justificada pelo diagnóstico;
não repetir as integrações anteriores apenas aumentando o número de amostras.

## Reprodução dos artefatos existentes

Scripts e resultados ficam em `cache/source_evidence`. Scripts create-once recusam
sobrescrever rodadas. Para nova integração usar semente/nome distintos; preservar os
priors e verificar o registro. `audit_importance_source.py <nome_da_rodada>` confere
custódia, somas diretas em precisão estendida e taxa duplicada nos pontos dominantes.
Os cálculos desta entrega terminaram; não retomar as sessões históricas como se estivessem vivas.

## Custódia

| arquivo relativo à bancada | SHA256 medido |
|---|---|
| `cache/source_evidence/source_evidence.py` | `0590f8e15bd508e525d2911fc570615671fdcdbc328399f4d7d8cb05d9816f7a` |
| `cache/source_evidence/importance_source_evidence.py` | `4671a7c402349e65f9c570527cd81a9f9a8608489a39f789e3288760ca654990` |
| `cache/source_evidence/validate_balanced_mixture.py` | `52982057783c0a717e65d540067a59505f05455b410937579f32f62e52f77578` |
| `cache/source_evidence/validate_importance_mixture.py` | `b81c4f354e390b3984c13f9e89ab7f33d016de20c4af36081547e995400bbd76` |
| `cache/source_evidence/refine_importance_proposal.py` | `510f1d5861314fe791dd1f9ae8257598f751acb55512965c2d2fd86afb7d2129` |
| `cache/source_evidence/audit_importance_source.py` | `643b54166cfcc6f6bcda56f9c2aa04efc350d7465a8322d55674cf1921696db2` |
| `cache/source_evidence/analyze_source_evidence.py` | `6723ed2ff58e409c7b47ed54e91929291f1f4d68879a842d658e4b8340aab12c` |
| `cache/source_evidence/BALANCED_ORACLE.json` | `44df2c65009e9dae001fb9b4cfcc46855d9e1e035bcc78bb36c2b4465d8802dc` |
| `cache/source_evidence/IMPORTANCE_ORACLE.json` | `ea907680a91a2238ee13e394f3cfe3add43e3eac22f17ff9321691ada31fb386` |
| `cache/source_evidence/validate_balanced_mixture.py.import_order_failed_bytes` | `5886bd625838d6b0325ca17998a4aa926e88f3e5ac2f5015f7cc17cb25e3a199` |
| `cache/source_evidence/validate_importance_mixture.py.numpy_bool_failed_bytes` | `db826f2981565726541088cefac98466cbb0ab166f37fc1b95fb3ae46e94c4e0` |
| `cache/source_evidence/REGISTRATION.json` | `cfde6683725ae3613cca2f3b46f55b7fd3ca9b0aac4443e297bb72cc7d2b7e6e` |
| `cache/source_evidence/runs/IMRPhenomXPHM_adapted_130701/IMPORTANCE_PROPOSAL.json` | `35b718570705bbbd78865d07913933116ff80efa8b41a32e4109fda12859098f` |
| `cache/source_evidence/diagnose_peak_phase.py` | `2bab71e781e00415a3f84f96bbbe4fa249b98d8a5d0bfbc0f250734509769602` |
| `cache/source_evidence/PEAK_PHASE_DIAGNOSTIC.json` | `a306a23c96d43d9c0badec6fd170b2474aabfacedc065757263220908cde6788` |
| `cache/source_evidence/PEAK_PHASE_COORDINATES.md` | `13809c80d2515421b5f3c447596a3fc7c887e53c28e8471bb07d6d7688b0aecd` |
| `cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/RESULT.json` | `3f015cbd503dcf16e75797dcb9072588608689bfd84696f3ffbddea6e0aa00dd` |
| `cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/AUDIT.json` | `fb4a420bd9fc1dd4e7694afc89c1d871f14dcc497e005014e59ac27d82958a23` |
| `cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/samples.npz` | `b250011235394741bb0c52c6241fd901ed5a3ed0eadc8fd8ab9c9dcd3531a361` |
| `cache/source_evidence/runs/IMRPhenomXPHM_seed130522_nlive256/IMPORTANCE_PROPOSAL.json` | `4f3c2b885d8b41a2a648d70fe5072fbbe756004f1df80b3ffa81d35f8d5904f5` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_seed130522_nlive256_seed130701_N4096/RESULT.json` | `55791e8658ea2fd519b1da722c189ba864b52b8b758cf88aba2ee1d1a26ba87c` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_seed130522_nlive256_seed130701_N4096/RESULT_ARRAYS.npz` | `db085326c9ab220b987f3c27e6f1e26fb335d8dfff69bd0611be0d2a229b76ce` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_seed130522_nlive256_seed130701_N4096/START.json` | `b4bf2033bfa6fcb507ce75c26cd38f3d7613c235e1f41f354357895c1a3085c3` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/RESULT.json` | `8b198ff8a8822427601a0882757021ed0dc41f62492b36a801ee4d5148039a85` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/RESULT_ARRAYS.npz` | `4002a5182e3e7259deac745c28b76d72c5822e7274a79db98500f35059be39db` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/AUDIT.json` | `af6124acb779b40d71861015c44e5cd70b8f4db2034bab59ce5fd6ce6ede722f` |
| `cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/START.json` | `6e3ac0f1f9fd4d28c0761e8ba9940e33cedf572ab0f5aabebcb4776dcbec3963` |
| `record_source_evidence_audit.py` | `0201643bf53b4d05f1fa53c67a19f08654129a1102f86b8abe3ca4add1c48bda` |
