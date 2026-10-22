[REAL — energia positiva analítica e covariância do boost orbital compiladas]

# ORDEM 016 — A3.2–A3.3 e teste de vácuo A3.5

UTC 2026-09-24T16:47:46.628335+00:00; ABERTURA sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

**A3.2 PAGO para as translações construídas.** Para a no `forwardCone`
do contrato e todo vetor ψ do espaço orbital L², foi construída
F(z)=∫ exp(i z a·p) dμψ(p), com dμψ=‖ψ(p)‖² dμ(p).
A finitude dessa medida foi provada a partir de ψ∈L². O pareamento
(+---) é não negativo no cone futuro; isso foi demonstrado, não assumido
como campo de estrutura. F é holomorfa para Im z>0, contínua até a borda,
limitada por μψ(Ω), e F(t)=⟨ψ,U(ta)ψ⟩. O lema
`orbital_positive_energy_v31_shape` usa exatamente `forwardCone`,
`upperHalf` e a conclusão analítica do contrato v3.1. Não exige momento
de energia finito: no interior, a derivada tem majorante 1/δ.

**A3.3 PAGO no componente cinemático do boost.** A mudança de rapidez
é ligada à `TGLExt.boostMat` existente por igualdade de coordenadas.
O grupo orbital tem identidade, composição, inversa, norma preservada
e continuidade forte na topologia real. Foi empacotado como equivalência
isométrica complexa, com a igualdade de operadores no tipo do contrato:

    B_s.conjStarAlgEquiv(U(a)) = U(wedgeBoostMap(s,a)).

No raio nulo, a mesma matriz dá B_s U(r n) B_(-s)=U(r exp(s) n).
O sinal vem do transporte pelo boost inverso; não foi trocado por
convenção informal. Isto não identifica ainda B com o grupo modular
de uma álgebra regional, nem deriva o 2π de BW por uma nova definição.

**A3.5 — teste de vácuo:** todo vetor orbital fixo por todos os boosts
é zero; portanto não existe vácuo normalizado com essa invariância no
espaço de uma partícula. É o resultado que exige a etapa de Fock.
Precisão lógica: NÃO foi demonstrado que a implicação `null_ergodic`
isolada seja falsa; ela pode ser satisfeita sem um vácuo físico. O que
não se pode fornecer aqui é o conjunto de condições com vácuo normalizado
e invariância por boosts. Não foi fabricado habitante do tipo reservado.

**Escopo dos três ramos:** energia e translações escalares valem nas
órbitas sem massa e massiva; os lemas permitem fibras complexas. Usar
duas componentes não constrói por si o cociclo físico das helicidades
±1. Essa realização continua aberta; seu controle normativo condicional
está na entrega anterior e permanece com esse estatuto.

**Verificação:** 42 declarações auditadas em 7 fontes finais;
13 compilações preservadas, máximo quatro versões compiladas
por módulo. rc0 final, cobertura integral de axiomas, somente o trio,
nenhuma admissão e kernel sem arquivos novos/modificados em cada rodada.
Máquina: 331.747650s parede / 234.187500s CPU; intervalo desde primeira
compilação desta entrega: 0.326322h. Fontes, comandos, logs,
hashes e tentativas em `A3/energy_covariance_manifest.json`.

**Reutilização:** operadores de translação, equivalência L², jacobiano,
ausência de autovetores e a matriz da casa foram importados e ligados.
As duas conferências independentes da coordenadora sobre as entregas
anteriores foram vinculadas por hash no manifesto; eram revisões de
fontes/logs/custódia, sem recompilação, e não se estendem automaticamente
à presente entrega.

**Ainda não pago:** realização física completa das helicidades, rede
local AQFT, identificação modular BW e segunda quantização. Esta entrega
reduz essas pendências pela construção dos operadores e da condição
analítica; não altera `um.py`, originais, kernel, gate ou confirmação física.

Sem nova chamada externa. Estimativas deduplicadas conhecidas: US$
0.1939854588; 3 jobs sem custo informado
permanecem desconhecidos. Não é total faturado. As duas unidades MiMo/Kimi
aguardam a confirmação específica de egress já pedida pela coordenação.
Nenhuma chamada foi repetida nem despachada por outra rota.
