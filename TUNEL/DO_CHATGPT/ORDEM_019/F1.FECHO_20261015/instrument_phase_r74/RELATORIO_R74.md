# R74 — fase ligada ao gerador, reservatório e leitura

Em nome de codex-gerente-tgl; F1.FECHO_20261015, claim967/escopo973. Reaproveita R57, R62, R64 e R66; não pede nova definição de realização/satisfação ao operador.

## Resultado

[REAL — computação sintética] Uma execução, pré-registro e revisão anteriores ao START: **118/118 verificações PASSA**, EXIT 0, 3.644512 s. Maior resíduo entre verificações de igualdade/positividade: **1.69170915e-11**. Tolerâncias por item no plano (álgebra 1e-11; integração 2e-8). Não é sigma experimental nem medida de aparelho.

[DERIVED — identidade de transporte] O mesmo estado, Hamiltoniano, cinco canais e bombeamento foram transportados por R(t)=exp(i Σχ_j n_j), com a conexão −Σχ̇_j n_j. O salto conjunto conserva suas duas fases e termos cruzados. As duas implementações corretas — portas transformadas com LO original e portas-base com LO transportado — reproduziram o quadro original em médias, segundos momentos, covariâncias e decoder C/B. Os filtros complexos atuam durante a janela; a alternativa algébrica de transportar o filtro consta da derivação, não de um oitavo ramo executado.

O bombeamento coerente R66 satisfaz o transporte: mantendo a porta transformada, α do banho fica fixo; absorvendo a fase na porta-base, α'=exp(iχ_e)α. O sinal operacional z das quadraturas foi passado ao leitor/decoder R57, com reconstrução e releitura idempotente verificadas. Isso não identifica z com G_OH físico sem o contrato próprio.

## Controles que quebram o sinal

| Controle | Diferença máxima em C/B/z | Limiar prévio | Resultado |
|---|---:|---:|---|
| negative_filtered_stale_LO | 0.0155328019 | 1e-07 | DETECTADO |
| negative_filtered_bad_J_phase | 4.25714303e-07 | 1e-07 | DETECTADO |
| negative_filtered_split_bath | 4.16731709e-06 | 1e-07 | DETECTADO |
| negative_filtered_bad_pump | 1.80554807e-05 | 1e-07 | DETECTADO |
| negative_final_phase_only | 0.00152389394 | 1e-07 | DETECTADO |

Além dessas cinco comparações de saída, três controles no gerador detectam as modificações de J, banho e bomba; o sinal rico não nulo é um controle de não vacuidade. Eles integram as 118 verificações, não amostras independentes de evidência empírica.

## Reuso e alcance

[REAL documental] Nós Vivo não indexa esta unidade (recusa preservada); mapa e fontes locais recuperam o mecanismo. A mudança de referência RF/óptica já estava delimitada na R64. O avanço aqui é o consumidor explícito com referências distintas por canal, filtros e banho consistentes.

[DERIVED] A conjugação simultânea conserva comutadores nulos na rede transportada; não afirma igualdade de cada álgebra original com sua conjugada nem fornece nova representação global. Ver PHASE_INSTRUMENT_BRIDGE_R74.md e ESCOPO_CONTATO_R74.txt (contato simetrizado não autoriza medir quadraturas incompatíveis; as portas executadas são independentes).

[OPEN] Identificação e calibração materiais, Γ independente e critérios integrais R4/R5 permanecem abertos. Parâmetros são INPUT adimensional; nenhuma passagem GHz/nm é obtida por renomeação. Nenhum novo Lean, dado observado, um.py, kernel, produção ou gate foi alterado.

Evidências: PLAN_R74.json, PREEXEC_REVIEW_R74.json, FREEZE_R74.json, START_R74.json, RESULT_R74.json, COMMAND_RESULT_R74.json; fontes por hash no plano e SOURCE_PINS_PHASE_INSTRUMENT_R74.json. A revisão final e a memória são recibos posteriores próprios.

