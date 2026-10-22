[REAL — controles compilados e mutações detectadas; nenhum resultado físico inferido]

# A6.C — controles das hipóteses e do auditor

Abertura SHA256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

C1 PAGO: 9 grupos, 27 theorem/lemma locais compilados com rc0 e auditados no trio. C2 PAGO: oito mutações geradas por substituição exata, hashes conferidos com a referência, compiladas e recusadas pelo auditor.

| Controle | Hipótese/objeto | Resultado |
|---|---|---|
| C1.1 | Projeção oblíqua | P²=P e HP=0, mas PH≠0 e P exp(−sH)≠P para s>0. |
| C1.2 | Gerador não autoadjunto | P ortogonal seleciona ker H; H nilpotente não simétrico e PH≠0. |
| C1.3 | Sem positividade | H=−I: sem limite zero; diag(3,−3): produto contínuo conservado sem fatoração. |
| C1.4 | Leitor descontínuo | Indicador da segunda coordenada é conservado, não fatora e não é contínuo. |
| C1.5 | Leitor constante | Conservação para qualquer fluxo e falha de distinção de identidades. |
| C1.6 | Fora dos bits | truthValue(2,0)=−3 não pertence a {0,1}. |
| C1.7 | Poda incompatível | Reuso do controle H=0, H′=I: a leitura anterior não é conservada. |
| C1.8 | Penalidade assinada | id†id−id†id=0 tem núcleo total; interseção dos núcleos é zero. |
| C1.9 | Qubit inválido | Traço 1, determinante −11/100 e testemunha quadrática negativa: não PosSemidef. |

| Mutação | rc Lean | Auditor | Detectada |
|---|---:|---|---|
| M1 | 1 | FALHA | True |
| M2 | 1 | FALHA | True |
| M3 | 1 | FALHA | True |
| M4 | 1 | FALHA | True |
| M5 | 1 | FALHA | True |
| M6 | 0 | FALHA | True |
| M7a | 0 | FALHA | True |
| M7b | 0 | FALHA | True |

M1–M5 falham na compilação. M6, M7a e M7b compilam, mas são recusados por sorry, axioma novo e cobertura ausente, respectivamente. Esses arquivos intencionalmente inválidos ficam apenas como controles, separados das fontes aprovadas.

Cinco tentativas dos controles preservadas: três da base e duas do complemento. A última correção do complemento explicita a ordem parcial complexa para que a desigualdade 1/5≤0 produza a contradição. Todos os enunciados aprovados foram relidos; fluxos exponenciais estão vinculados às matrizes geradoras.

Máquina: 357.652019s de parede somados por processo, 357.187500s CPU. Processos paralelos impedem interpretar a soma como duração cronológica. Nenhuma escrita detectada no kernel.

Escopo: auditoria das fontes e dos logs locais; não substitui auditoria transitiva completa dos imports. Originais, um.py e gate não alterados. Próximo ramo: D1/D2. Integração monolítica continua pendente.

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A6_EQUACAO_DA_VERDADE\C_controles\controls_manifest.json`.
