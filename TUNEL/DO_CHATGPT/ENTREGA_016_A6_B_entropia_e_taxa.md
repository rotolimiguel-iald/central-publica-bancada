[REAL — provas Lean compiladas e auditadas no escopo dos enunciados]

# A6 — entropia escalar, exponencial idempotente e taxa espectral

Abertura do operador, SHA256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

| Alvo | Estado | Resultado | Teoremas novos |
|---|---|---|---:|
| B3a | PAGO | Raio em [0,1), antitonia; entropia crescente; déficit não negativo e decrescente | 14 |
| B3b | PAGO sob r>0 | Derivada exata da entropia escalar | 4 |
| B3d | PAGO | Exponencial de idempotente em álgebra de Banach completa | 2 |
| B1b | PAGO sob gap | Decaimento em norma com constante 1 por Parseval | 3 |

B3a usa p∈(0,1), k=|c|²≥0, k<p(1−p), s≥0. Foram provados r(s)=√((2p−1)²+4ke^(−2s)), S(s)=binEntropy((1+r(s))/2) e D(s)=binEntropy(p)−S(s)≥0. S é estritamente crescente quando k>0. A igualdade desse escalar com −Tr(ρ log ρ) pertence ao harness matricial D, ainda pendente.

B3b: S′(s)=(2ke^(−2s)/r(s)) log((1+r(s))/(1−r(s))). O caso r=0 não foi incluído nessa fórmula dividida por r; a monotonicidade B3a o inclui.

B3d: para e²=e, exp(−s(1−e))=e+exp(−s)(1−e). É identidade algébrica para s real; idempotência sozinha não garante que e seja canal completamente positivo, não fixa taxa física nem seleciona um vácuo único.

B1b: ||T_s x−Px||≤exp(−sγ)||x−Px||, s≥0, γ>0, em dimensão finita. A hipótese do gap se refere exatamente aos autovalores de H: cada um é zero ou ≥γ. Ela já implica não negatividade espectral; não foi acrescentada uma segunda hipótese redundante de positividade. Não se afirma igualdade de norma de operador nem existência de modo que atinja γ. Núcleo total e dimensão zero permanecem admitidos.

Auditoria: 23 teoremas novos, quatro fontes finais, cobertura integral; todos os axiomas contidos no trio. Nenhum sorry/axiom novo nas fontes finais. Oito tentativas no total: B3a 1; B3b 3; B3d 2; B1b 2. Falhas preservadas.

Custo de máquina: 128.900510s parede somados, 129.890625s CPU; janela registrada de bancada 0.182222h (não exclusiva; começa na primeira compilação). Estimativas externas explícitas deduplicadas: US$0.2805930732; incompletas, não equivalem à fatura. Nenhuma chamada externa nova nesta implementação.

Não move o gate. Permanece a MEDIDA de empacotamento: provas em módulos companheiros, prefixo V3 da base preservado, monólito final ainda não integrado. A etapa seguinte é B1d (limite forte em dimensão infinita), seguida dos controles C e do harness D.

Manifesto de fontes, logs, comandos, hashes e tempos: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A6_EQUACAO_DA_VERDADE\B_fechamentos\entropy_and_gap_manifest.json
