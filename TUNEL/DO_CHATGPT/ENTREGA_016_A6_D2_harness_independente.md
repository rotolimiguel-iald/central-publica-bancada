[REAL — harness independente executado; DERIVED — identidades exatas dos exemplos]

# A6.D2 — duas verificações independentes na bancada

Abertura SHA256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

Resultado: 44/44 grupos de checks, 9/9 controles negativos, 260 avaliações por aritmética de intervalos e 12 comparações de entropia relativa com logaritmo matricial. Semente 160620260924 pré-registrada antes da geração. A fonte não importa V1 nem lê seus resultados.

No primeiro exemplo racional em dimensão 5, os projetores espectrais foram calculados como polinômios de Lagrange em H, em vez de usar diretamente os vetores para construí-los. O fluxo foi conferido pela EDO, condição inicial, semigrupo, Taylor até ordem 12, preservação da leitura e limite. O segundo exemplo usa matrizes racionais aleatórias; sua inércia (três modos positivos/dois nulos) decorre da congruência com a matriz 3×3 positiva definida, cujos menores principais exatos estão registrados. Esse segundo exemplo confere a projeção da série truncada até ordem 15; não se apresenta essa truncagem como igualdade da exponencial inteira.

Foram verificados dois leitores contínuos, amostragem em tempo positivo, 48 pares racionais (com resultados verdadeiros e falsos), núcleo/complemento, derivadas, perfil e nove controles negativos. O superoperador do qubit é explicitamente uma projeção ortogonal Hilbert–Schmidt, H=id−E=D†D, com exponencial exata E+exp(−s)(id−E).

Entropia: quatro pares (p,|c|²), incluindo p=1/2 e dois casos a 99% da fronteira de positividade, cada um com 65 pontos em s∈[0,10]. mpmath.iv a 60 dígitos confirmou 0<r<1 e limite inferior estritamente positivo da derivada em todos os 260 pontos. O caso de coerência zero é tratado separadamente como estado constante. A grade não prova positividade universal; essa é a proposição escalar Lean já auditada com suas hipóteses.

O logaritmo matricial foi construído por autodecomposição exata SymPy de matrizes hermitianas com coerência complexa; Tr(ρ(logρ−logσ)) foi comparado a S(σ)−S(ρ), cujo S(ρ) foi avaliado com autovalores calculados independentemente por mpmath.eighe. Precisão 50 dígitos, tolerância 10⁻⁴⁰, maior resíduo 6.681911775230489115351341167878704697037992200262622E-51. Não foi reutilizada a fórmula da diferença entrópica para calcular ambos os lados.

Duas execuções preservadas: a primeira já passou; a v2 acrescenta os três checks explícitos de Hilbert–Schmidt/exponencial/entropia cruzada exigidos por B3c. Tempo total 22.228982s parede e 22.187500s CPU. D1 permanece separado, 51/51+9/9. D3 “22/22+5” continua NÃO_VERIFICÁVEL.

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A6_EQUACAO_DA_VERDADE\D_harness\independent_harness_manifest.json`. Não move gate, não mede σ, não altera originais. Próximo: ficha E.
