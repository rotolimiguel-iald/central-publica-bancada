# R78 — resposta complexa do gerador OH–luz e normalização do radical

Em nome de codex-gerente-tgl, 18/10/2026 (execução 19/10 em UTC). Unidade F1.FECHO_20261015, reivindicação967, escopo981. Componente sintético/documental; R4 e R5 integrais permanecem abertos.

## 1. O que foi efetivamente feito

[REAL — execução numérica] Uma única execução do plano PLAN_R78_R2.json, congelado após revisão independente, com **93 verificações aprovadas e exit0**. Reutilizados por extração AST os dois helpers puros do gerador R66; não executados seus outros ritos nem importados programas canônicos. Beta calculado em runtime por ALPHA_FINE_CODATA_2018*sqrt(e). Corte de ocupação total N<=3, dimensão16; quatro instantes adimensionais0,0.25,0.5,0.75. Tempos, taxas, ganhos e preparações são INPUTs sintéticos. Nenhum dado observado foi aberto e nenhuma medição física foi feita.

O teste calcula a primeira variação da trajetória do gerador completo sob dois probes Hamiltonianos constantes X/P, usando Duhamel em exponencial de bloco. Compara com diferenças centrais em epsilon0.001 e0.0005, mantendo o MESMO estado inicial em cada par. O receptor lê Lout=sqrt(kappa_out)*a_out com LO0 e pi/2. Não há drive coerente direto no banho de saída nesse modelo. É resposta transitória a degrau nos controles: não é varredura espectral, resposta estacionária ou frequência de material medida.

A versão R1 não foi executada. R2 retirou, ANTES do congelamento, a imposição incorreta de nulidade no caso sem semente. Parâmetros/preparações/tolerâncias não mudaram. O critério permite respostas nulas ou não nulas e não exige a fórmula da patente como resposta.

## 2. Resultado numérico

A coluna de resposta é max sobre os quatro tempos e as quatro entradas do Jacobiano real d(QX,QP)/d(x,y), por unidade dos controles Hamiltonianos adimensionais. NÃO é potência transmitida, eficiência, ganho óptico calibrado, probabilidade nem beta medido. O erro FD é desacordo entre dois cálculos do MESMO corte, não cota de erro físico/contínuo.

| Preparação/controle | Máxima resposta | Máximo desacordo Duhamel–FD na saída |
|---|---:|---:|
| seeded_full | 3.26649760023e-07 | 9.08899691621e-14 |
| unseeded_full | 2.54285780351e-09 | 3.13854082561e-16 |
| seeded_blocked | 5.42101086243e-20 | 8.33044570825e-14 |

O ramo semeado contém referência coerente na saída: mede modulação condicional de sinal já presente. O ramo sem semente omite a componente inicial |0,1,0>, mas conserva coerência/preparo na entrada e no OH e a bomba; NÃO é vácuo global nem emissão sem energia. Ambos os estados foram normalizados independentemente e fixados antes de calcular. No ramo sem semente, o cálculo retorna uma primeira variação pequena não nula; sua extrapolação ao espaço completo não foi certificada.

No controle bloqueado, gJC e lambda foram zerados juntos. A resposta marginal da saída cai para resíduo numérico; isso confere a sensibilidade do teste às ligações presentes. Não isola qual ligação é responsável nem prova a realização física da face. A coerência intracavidade a_in†a_out pode variar até no ramo bloqueado por alteração local da entrada: ela NÃO é testemunha suficiente de comunicação nem correlação temporal de detector. Os diagnósticos n_out e a_in†a_out estão no JSON com esse alcance.

O máximo desacordo de estado Duhamel–FD em todos os ramos foi 1.33390933021e-09, dentro da tolerância2e-7. Cada check usa sua tolerância própria; não comparar o máximo agregado com a tolerância algébrica2e-10. Uma rotação errada do LO em0.6rad alterou o sinal semeado e obedeceu à lei de rotação exp(-i phi). Isto verifica dependência da referência de fase no modelo.

## 3. A ponte que agora temos e a que ainda falta

[DERIVED — cálculo no corte] Com u=x+i*y nas coordenadas dos probes e z=(QX+iQP)/sqrt2, a resposta real-linear escreve-se

    delta z(t) = h_plus(t)*u + h_minus(t)*conj(u).
    h_plus=(R_X-i R_P)/2; h_minus=(R_X+i R_P)/2.

Em t=0.75, no ramo semeado:

    h_plus = -2.1552150964576032e-7 - 2.125764790838723e-7 i
    h_minus = -1.5454750739349352e-8 + 1.1992601049625585e-8 i.

Os números são transcritos de RESULT_R78.json. h_minus não nulo descreve estas coordenadas de CONTROLE HAMILTONIANO. Antes de identificar a amplitude óptica física com u, é necessário derivar sua convenção de acoplamento, fase e normalização. Por isso esta decomposição não é prova de canal óptico conjugado nem refutação, sozinha, de M=g_OH*S_beta. O experimento não construiu a matriz de espalhamento óptica completa de todos os portos e polarizações.

Agora há uma ligação executável entre gerador e observável de amplitude/fase, condicional ao modelo e preparo. [OPEN] Restam a conversão de drive físico para os probes, o mapa de superfície/espelhamento OH para esse gerador, a identificação das taxas/ganhos e a comparação com a lei de transmissão da patente. O nome OH no modelo não substitui a derivação material. Não repetir o leitor/decoder R57, o mecanismo de releitura R73 ou o enquadramento de fase R74.

## 4. Normalizações reaproveitadas

[REAL documental] NORMALIZACOES_R78.md recupera F0, rho0, energia–frequência, dimensões da câmara e frequência OH, com arquivos/linhas/hashes. Essas escalas EXISTEM. Nos intervalos examinados, não foi localizada a identificação que determina o prefator superficial e as taxas do MESMO gerador. Não é alegação de ausência em todo o acervo.

[DERIVED — exemplo dimensional, não lei física] Para densidade de energia rho, pode-se escrever Sigma_S=(hbar/A0)*sqrt(|rho|/rho0), com rho0>0 e A0>0. O coeficiente C=hbar/(A0*sqrt(rho0)) tem a unidade que falta para converter sqrt(densidade de energia) em ação/área. A mudança rho0'=s*rho0, A0'=A0/sqrt(s) preserva C; isso é invariância da referência, não determinação de A0 ou rho0. Módulo/raiz não reconstroem fase e sinal. A área macroscópica do cubo não foi identificada automaticamente com área efetiva do acoplamento.

A frequência OH pode definir uma unidade temporal; todos os coeficientes do gerador devem ser convertidos juntos. Isso não fixa taxa de relaxação, potência limiar ou Gamma independente. A identificação tau_star=t_P encontrada na fonte permanece CONJECTURE, como nela declarada.

## 5. Limites e próximo avanço

- PASS é consistência numérica do componente: não confirmação física ou 5sigma.
- O corte3 não recebeu nova cota contínua para estes probes/derivadas; a cota R75 da bomba não é transferida por nome.
- Tolerâncias e diferenças finitas não são enclausuramentos rigorosos. Mesmo resposta não nula não fornece SNR experimental.
- O termo de ruído de contato registrado é apenas uma parcela da covariância do receptor; não é variância total nem amostra medida.
- Identificar a face material e as normalizações exige consumir as equações existentes de modos, suporte espacial e acoplamento; fontes adicionais devem ser consultadas antes de construir o que faltar.
- Antes de nova campanha, derivar a conversão entre drive óptico e controles X/P e estabelecer o alcance de corte necessário. Não selecionar estados/janelas depois de ver estes números para alegar teste decisivo.
- Canonico um.py, Nós, Bancada, dados observados e gate intactos. Nenhum provedor ou build Lean novo.

## 6. Custódia

Resultado: RESULT_R78.json, SHA256 `205c81426062112d7356ddc5d915abb2b212fdc6612fac4e61066dfc7bfd731b`.
Freeze: FREEZE_R78.json, SHA256 `414970ced99829e1158669048a501559bb804f4faad6590f952349c305477e10`.
Execução: 2026-10-19T00:23:26.324902+00:00 a 2026-10-19T00:23:27.190846+00:00, 0.865328400s; COMMAND_RESULT_R78.json registra o comando literal.

PREEXEC_REVIEW_R78.json e revisão final acompanham esta entrega. SOURCE_PINS_NORMALIZACOES_R78.json conserva cobertura e excertos; normalizações não foram usadas para fabricar parâmetros físicos nesta execução.
