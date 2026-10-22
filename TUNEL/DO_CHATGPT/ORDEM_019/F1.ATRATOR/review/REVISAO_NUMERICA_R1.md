# Revisão numérica independente — F1.ATRATOR R3

Autor: atrator_skeptic, sob reivindicação 664 da coordenação. ACOM: project da referência exata da unidade recuperado na revisão 3; transitions centralizadas na coordenação.

**Veredito: PASSA no alcance matemático finito pré-registrado.** Nenhum achado material pendente na rodada numérica. Esta revisão não audita ainda a candidata Lean e não declara creditação física. A cunhagem permanece [ONTO].

## Integridade e cronologia [REAL]

O PREREGISTRO_R1 foi criado às 13:08:19 UTC. As tentativas começaram às 13:11:54 (R1), 13:13:45 (R2) e 13:14:39 (R3). Os 14 arquivos-fonte pinados foram relidos e todos conferem; os pins do programa, scripts, pré-registro, logs, resultado e recibos também conferem. O R3 terminou às 13:14:43 UTC, EXIT 0.

R1 recusou antes da construção de qualquer matriz porque ALPHA_FINE_CODATA_2018 está no módulo embutido, não na AST top-level do wrapper. R2 recusou no mesmo estágio porque o leitor não aceitava CRLF. O diff integral está ao lado: R3 corrige a recuperação da entrada, exige unicidade da linha e confere o literal com SEALED_CODATA_ALPHA da AST externa. Não executa o um.py. Tolerâncias, semente, alvos, matrizes e verificações científicas não mudaram. A igualdade da cauda do código a partir do cálculo de β foi verificada, normalizando somente o nome do arquivo de resultado e os metadados do leitor.

β foi recalculado independentemente em runtime a partir da linha pinada: 0,012031300400803142. Não foi usado β literal como entrada. A reprodução usa unidades de matriz Eij e a forma explícita do canal, sem importar ou executar o runner entregue; o runner usa a base de Pauli. Isto fornece conferência por coordenadas diferentes.

## Resultados por item

| Item | Populações | Matrizes densidade | Alcance |
|---|---|---|---|
| A1 | PASSA | PASSA | Fórmula espectral, potências e cotas; aproximação forte em n=4096 abaixo de 1e−10 |
| A2 | PASSA | PASSA | RT=TR=R por resíduos e derivação |
| A3 | PASSA | PASSA | R²=R, R*=R, projeção espectral/SVD e letra normalizada em A=I−T |
| A4 | PASSA | PASSA | Dimensão fixa 1 sob contração estrita no complemento; estado único após normalização |

A existência não é vazia: p=(1/2,1/2) e ρ=I/2 são estados concretos fixos. O fator transitório é λ=0,9759373991983937, estritamente abaixo de 1. Os canais são compatíveis com CPTP no desenho: a face completa mede/descoerentiza antes e depois da S; o segundo canal é descoerência conjugada por uma unitária. O runner confere Choi, traço, positividade e a reconstrução do superoperador.

## Controles [REAL/DERIVED]

- Identidade de populações: dimensão fixa 2, A1–A3 PASSA com a projeção verdadeira R=I; A4 FALHA_SEM_HIPOTESE, como exigido. Os dois estados e0/e1 exibem a multiplicidade.
- Descoerência rotacionada: dimensão fixa 2, A1–A3 PASSA; A4 FALHA_SEM_HIPOTESE. As duas populações conjugadas por S são fixas.
- Dinâmica afim x↦x+1: uma iteração independente confirma x_n=n e a média dos primeiros N termos=(N−1)/2; ambas divergem. A1 direta e Cesàro FALHAM. O controle pertence declaradamente a outra classe: não é operador linear nem CPTP finito. No runner os rótulos deste controle vêm do argumento analítico explícito; a presente revisão conferiu a recorrência por iteração.

## Precisão que deve acompanhar a conclusão

Os resíduos finais entregues em float64 são 5,3351814e−13 (populações) e 9,0949470e−13 (densidades). São pisos de arredondamento/acumulação. A reprodução em outra base dá resíduos diferentes, também abaixo de 1e−10; igualdade bit a bit entre implementações distintas não é exigida.

Para o canal real exato, a conta com 110 dígitos dá |λ|^4096=4,70275630625964e−44. Não dizer que o resíduo de ponto flutuante mediu essa quantidade. Para Cesàro em N=4096, a distância exata é 0,0101460613926531: o teste conferiu a fórmula e a cota O(1/N), NÃO uma precisão de 1e−10 em relação a R. A convergência universal vem da demonstração, não apenas dos 258 estados de população e 260 densidades amostrados.

A representação T=exp[a(X−I)] foi conferida para populações. Ela não identifica a S angular com a dinâmica dissipativa, nem importa o limite para a órbita angular, nem identifica toda a dinâmica hiperbólica canônica da TGL.

## Ocorrência no próprio auditor

O primeiro script do auditor completou as asserções numéricas, mas falhou no normalizador de metadados do diff: o R1 já possuía alpha_assignment_line, fato não tratado pelo normalizador. O script foi preservado, a falha foi registrada em REPRODUCAO_R1_FALHA_AUDITOR.json e uma R2 corrigiu só esse normalizador. R2 deu EXIT 0 e produziu REPRODUCAO_NUMERICA_R1.json. Nada da entrega foi alterado.

## Fontes e limites

Os hashes medidos estão em REVISAO_NUMERICA_R1.json; a reprodução e o diff estão ao lado. Não houve escrita ou ensaio na Bancada de produção, execução/modificação do um.py, alteração do Nós, dado observado ou gate. O resultado é validade e consistência no modelo finito testado, não uma medida de 5σ nem uma conclusão ontológica universal.
