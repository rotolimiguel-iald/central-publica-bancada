[REAL — inventário e auditoria executados; DERIVED — cobertura combinatória delimitada]
# A7.b — incidências decoradas corrigidas
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T01:34:38.127358+00:00.

O novo enumerador inclui a cor de cada vértice, o tipo e a orientação das
linhas no certificado canônico. Os originais e os defeitos da resposta
Kimi ficam preservados. Não se promove a crítica não reproduzida dos
índices móveis a fato: os 2.187 controles anteriores não a confirmaram.

Para grafos conexos de um laço I=V, E=sum(v_i-2); com v_i>=3 e E<=6,
V<=6 e v_i<=8. As partições produzem 29 famílias. Geram-se todos os
multigrafos com esses graus, todas as cores admissíveis e todas as linhas
H-H ou C->CB que respeitam os slots. Quocientar em etapas preserva as
órbitas, pois cada etapa subsequente percorre todas as decorações.

Resultado: **6842 tipos de ação**, por E=1..6:
{"1": 2, "2": 11, "3": 41, "4": 206, "5": 1016, "6": 5566}. Inclui tadpoles e grafos
conexos redutíveis; não se impôs 1PI. Assinaturas METRIC=H^v,
GHOST=(CB,C,H),HDAG=(h†,C,H),CDAG=(c†,C,C), estas três cúbicas.
Pernas externas não são numeradas, e derivadas/tensores dos vértices não
são decompostos em diagramas individuais. Isso delimita o significado
de tipo; não é contagem de termos da amplitude.

Auditoria sem importar o motor: 6842 registros revalidados,
sem duplicatas, com todos os automorfismos de vértices conferidos por
permutações que preservam as cores. Oráculo por emparelhamentos de
meias-arestas reproduz E=1,2,3: 2,11,41 tipos, respectivamente a partir
de 4,69,1900 emparelhamentos rotulados. Três controles negativos;
o motor tem outros cinco. CPU motor 3.390625s,
auditoria 0.75s; ambos rc0.

Todos os tipos têm ghost0. **Não há inserção Ward/EOM/cutoff definida
por essa enumeração**. Seu catálogo continua pendente: não basta mudar
o número de ghost de um registro. Pesos de amplitude permanecem null;
automorfismo combinatório não foi usado como peso de Feynman.
O resultado organiza o cálculo; não determina a anomalia nem move gate.

Reprodução: Python314 -X utf8 -B incidence_decorated_run.py e
incidence_decorated_audit.py, com destinos novos (artefatos existentes
são protegidos). Fontes, entradas e logs têm hashes nos manifestos.
