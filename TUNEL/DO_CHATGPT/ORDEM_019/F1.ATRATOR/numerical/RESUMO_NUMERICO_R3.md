# F1.ATRATOR — resultados sintéticos do pré-registro R1

Autor: codex-gerente-tgl / atrator_sources. [REAL — ensaio numérico finito]; [DERIVED — fórmulas/cotas analíticas]. O enunciado ontológico segue [ONTO].

Execução R3: EXIT 0. Todos os resultados esperados foram observados. Não houve chamada à Bancada de produção nem leitura de dado observado.

| Face/controle | A1 / A2 / A3 / A4 | dim Fix | erro final n=4096 | maior resíduo algébrico |
|---|---|---:|---:|---:|
| primary_population | PASSA / PASSA / PASSA / PASSA | 1 | 5.3351814e-13 | 4.9960036e-15 |
| primary_density | PASSA / PASSA / PASSA / PASSA | 1 | 9.094947e-13 | 9.4368957e-15 |
| identity_population | PASSA / PASSA / PASSA / FALHA_SEM_HIPOTESE | 2 | 0 | 0 |
| rotated_dephasing | PASSA / PASSA / PASSA / FALHA_SEM_HIPOTESE | 2 | 1.0186598e-12 | 5.0717766e-16 |

β runtime = 0.012031300400803142; λ = 1−2β = 0.9759373991983937. α lido da atribuição não indentada na linha 5557 do módulo embutido no um.py pinado e conferido contra o SEALED_CODATA_ALPHA do wrapper. Não importado nem executado.

## O que passou

- Populações incoerentes: T=|S|², S=[[√(1−β),√β],[−√β,√(1−β)]], R=J/2. Sob contração estrita do complemento, dimensão fixa 1 e estado normalizado (1/2,1/2).
- Canal completo: D∘Ad(S)∘D na base ortonormal de Pauli/Hilbert–Schmidt. R(ρ)=Tr(ρ)I/2. A descoerência completa antes/depois de S é hipótese sintética explícita.
- R comparado independentemente com projetores obtidos por SVD de I−T e eigh de T; idempotência, auto-adjunção, RT=TR=R e letra q(I−T)/q(0) conferidos.
- Potências nos nove n e médias de Cesàro nos seis N fixados antes: fórmulas e cotas conferidas. A média finita não foi obrigada a chegar a 1e−10 de R; a cota O(1/N) é a do pré-registro.
- 256 estados aleatórios de população mais as duas bases; 256 densidades aleatórias mais quatro estados puros explícitos. Positividade, traço e hermiticidade conferidos nas potências. Critérios CP/TP calculados pela matriz de Choi em unidades matriciais, independentemente da representação por Pauli.
- Representação normalizada exp(a(X−I)) do canal de populações, a=−log(1−2β)/2: resíduo 1.1883195e-16. Não identifica por homônimo o boost canônico, nem torna o canal completo singular D∘Ad(S)∘D um GKLS de tempo finito invertível.

## Controles negativos

Identidade populacional e dephasing rotacionado possuem dois estados estacionários distintos, incluídos nos resultados. A1–A3 passam com seus próprios projetores; A4 falha sem a hipótese, como exigido. Não se força R=J/2 no controle degenerado.

A translação afim f(x)=x+1 não possui ponto fixo: x_n=n e média dos primeiros N termos (N−1)/2 divergem. A1 direta e A1 Cesàro FALHAM. Esse controle está expressamente fora da classe linear/CPTP; todo mapa linear fixa zero e todo canal CPTP finito tem estado estacionário.

## Tentativas preservadas e alcance

R1 recusou a extração AST de α no wrapper externo; R2 recusou a terminação CRLF na regex ancorada. Ambas terminaram antes de construir as matrizes. R3 corrigiu somente o leitor (com verificação adicional do valor selado). Pré-registro, fonte, valor de α/β, semente, amostras, tolerâncias e critérios não mudaram. Manifestações de execução foram gravadas antes de cada tentativa, e os logs trazem comando, início, fim, tempo e exit.

Os PASSA são numéricos na face e nos pontos testados. A universalidade condicionada deve ser lida no candidato Lean e em suas hipóteses; nenhuma medição da natureza, sigma observado ou creditação foi produzida. GKLS v384 foi reaproveitado documentalmente, sem repetição da campanha.
