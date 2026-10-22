[DERIVED — naturalidade bilocal e localização da primitiva até O(K); Q2 completa OPEN]

Data 2026-09-25T10:07:55.566470+00:00. Abertura SHA256 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

Os dois propagadores singulares e a distância geodésica passam no teste
de derivada de Lie simultânea nos extremos X/Y, para todas as componentes
e quatro transvecções do espaço-forma auxiliar. A verificação conserva
X e Y simbólicos. A distância coordenada w não passa: seus quatro
resíduos estão registrados. Não se escolheu regulador pelo resultado.

O transporte radial do frame e a regra de duas integrações por partes
justificam a leitura local por jatos completamente simétricos, com sinal
positivo no operador sobre c para as ordens ímpares3/5. O teste não
certifica novamente todos os vértices/diagramas; essa aplicação continua
ligada à montagem tensorial declarada no cálculo anterior. A completação
coordenada preserva sua ressalva de naturalidade global.

A localização da nova Hessiana de quarta ordem exige

    M_chi=(chi*N+N*chi)/2=chi*N+[N,chi]/2.

A derivação covariante direta de chi*h coincide com a soma de todos os
subconjuntos ordenados de derivadas, incluindo conexões nos índices
derivados. Os coeficientes paralelos foram conferidos sob transposição
das dez fibras simétricas, com b,c,t e momentos simbólicos. Omitir o
comutador ou duplicar sua metade produz resíduos explícitos.

A demonstração escrita inclui a corrente de Green da quarta ordem e
s0 B_chi=-C_E integral h[chi*A_cov c+[N,chi]Gc/2]+O(K²). Ao transferir
também G para o outro lado, suas derivadas de chi devem ser conservadas.
BRST-exatidão dessa variação não identifica sozinha todo o contato
quântico localizado. Nenhum contratermo foi adotado.

## Evidência e próximo passo

- Naturalidade/frame/sinais: 1496 verificações,
  CPU 6.5s, oito controles negativos.
- Corte/adjunção: 528 verificações,
  CPU 2.78125s, quatro pares de resíduos.
- Total desta entrega: 2024 verificações; CPU 9.28125s. Ambos os comandos
  com A4/symbolic_runtime/Scripts/python.exe -X utf8 -B terminaram rc0.

Fontes, scripts, logs e demonstração: manifesto em C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A7\contact_frame_cutoff_delivery\manifest.json.
Ainda faltam os outros diagramas locais, W geral, K², aridades superiores
e valores de contorno lorentzianos. Próximo trabalho: essas parcelas e
a comparação das revisões independentes pendentes, dentro do A7.b.
O turno anterior foi PROGRESS (resultado local e staging custodiados).
Nenhum processo próprio continua vivo; nenhuma nova chamada externa
foi iniciada neste turno. Originais, kernel e gate permanecem intactos.
