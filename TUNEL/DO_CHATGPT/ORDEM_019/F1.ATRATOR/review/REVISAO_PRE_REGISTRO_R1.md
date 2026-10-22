# Revisão independente ANTES dos ensaios — F1.ATRATOR

Autor: subagente atrator_skeptic, sob a reivindicação 664 da coordenação. Estatuto: [DERIVED — revisão matemática da proposta; números ainda NÃO executados]. Protocolo ACOM: README/SESSION_MEMORY lidos e project da referência própria da F1.ATRATOR recuperado na revisão 1. Transitions centralizadas pela coordenação.

## Veredito de desenho

**APROVÁVEL COM AS PRECISÕES ABAIXO**, antes de pré-registrar e rodar. O objeto finito proposto suporta A1–A4. A cunhagem permanece [ONTO]; o ensaio mede somente o canal e as hipóteses nomeadas.

1. **Definir o canal dissipativo.** S é unitária/ortogonal e sua iteração coerente não converge. T=|S|² atua nas populações quando a descoerência completa D intervém em cada passo: C=D∘Ad_S∘D. Esta operação precisa estar no contrato. Ela não pode ser silenciosamente atribuída à S angular. O canal de populações é a face dissipativa do modelo sintético; não se deriva dele a dinâmica hiperbólica canônica sem uma ponte específica.
2. **A1: distinguir limite e teste finito.** Para T=[[1−β,β],[β,1−β]], λ=1−2β e R=(1/2)ones, T^n=R+λ^n(I−R). Sob 0<β<1, |λ|<1. Isso prova a convergência para todo vetor, e a amostra numérica verifica a implementação. Uma grade finita que passa não prova sozinha o quantificador universal. Os vetores de base devem fazer parte dos testes para controlar a matriz inteira.
3. **Cesàro tem outra velocidade.** Com média n=0,…,N−1, C_N=R+[(1−λ^N)/(N(1−λ))](I−R). A tolerância absoluta de 1e−10 em N=4096 é inadequada como critério de convergência de Cesàro, que só cai O(1/N). Pré-fixar confronto com a fórmula/cota, ou manter convergência direta como A1 primária e Cesàro como conferência. Não escolher outro critério depois de ver o resultado.
4. **A2/A3: operador e projeção bem tipados.** RT=TR=R, R²=R, R*=R e ran R=ker(I−T) são suficientes no modelo simétrico. Para Hilbert geral, a prova precisa hipóteses adequadas (por exemplo T contração, teorema ergódico médio); um canal GKLS genérico não unital não tem necessariamente projeção ortogonal no produto de Hilbert–Schmidt. Não transferir esta igualdade sem hipótese.
5. **LETRA e PALAVRA.** Em WordExistence, a fonte usa A auto-adjunto, minpoly(A)=Xq, q(0)≠0. Aqui tomar A=I−T, q(X)=X−2β: q(A)/q(0)=R. Equivalentemente R=(T−λI)/(2β). q aniquila o complemento transitório; Xq aniquila A. O polinômio mínimo inteiro de T avaliado em T dá zero, não R. Nomear a letra conforme a cunhagem sem confundir com a candidata PALAVRA. `observing_adds_nothing` exprime projPlus·(projPlus·angFamily θ)=projPlus·angFamily θ; é o mesmo padrão de idempotência, não um teorema que identifique projPlus angular e R de populações.
6. **A4: hipótese não circular.** Nomear a contração estrita no complemento de span(1,1), com constante |λ|<1. Não se pode exigir contração estrita no espaço inteiro, pois há vetor fixo não zero. A conclusão linear é dim Fix(T)=1; unicidade do estado vale após normalização sum p=1. Sem a normalização há infinitos múltiplos do vetor fixo.
7. **Saltos não comutantes não bastam em geral.** Dois operadores que não comutam podem ser simultaneamente blocais em H=H_a⊕H_b e conservar os dois blocos, dando vários estados fixos. Reaproveitar o resultado v384 no alcance efetivamente testado, sem promover não comutatividade isolada a teorema global. Hipótese suficiente pode ser irredutibilidade/comutante escalar com as condições do gerador, ou a contração no complementar que a proposta já usa.
8. **Controles e vocabulário.** T=I tem dim Fix=2: A4 sem hipótese falha como esperado, enquanto A1–A3 podem passar com R=I. Se se mantiver o antigo R=(1/2)ones, dizer que A1/A3 também falham por projeção mal escolhida; preferível recalcular a projeção verdadeira em cada controle. Um dephasing quântico puro com duas populações fixas é outro controle válido, já antecipado no mapa. O controle x↦x+1 em ℝ não tem ponto fixo, nem média de Cesàro convergente, mas é afim e não é canal CPTP finito. Todo operador linear fixa 0; todo canal CPTP finito tem ao menos um estado fixo. Declarar a mudança de classe evita uma impossibilidade no enunciado do controle.
9. **A rotação angular pode ter Cesàro convergente.** Uma rotação não trivial não converge diretamente, mas as médias podem tender ao vetor zero; não chamá-la controle de falha do enunciado disjuntivo “direto OU Cesàro”. Uma troca de duas populações é controle de periodicidade direta e sucesso de Cesàro, se desejado.
10. **Tolerâncias e SVD.** Fixar tolerâncias absoluta/relativa, valores limiares e política para singular values próximos ao limiar (AMBÍGUO/refusa) antes da rodada. Para a face 2D o gap analítico 2β está longe da fronteira, mas isso deve ser uma consequência. Fixar seed, estados, N e dtype; registrar matrizes e resíduos. Toda conclusão PASSA/FALHA deve dizer se é matemática, numérica no desenho ou controle esperado.

## Reaproveitamento confirmado no mapa

O mapa já avisa que o dephasing de um salto Hermitiano deixa toda a diagonal fixa; não reconstruir “atrator único” sobre esse caso. A v384/v385 possui ensaio do atrator único com cinco saltos (672 pontos e stress), cujo estatuto é numérico na grade; reutilizar a fonte em vez de afirmar um teorema geral só pelo nome.

## Fontes abertas

- WordExistence.lean: docstring e `annihilating_word_exists`; padrão Xq e q(0)≠0, não q(A)=0.
- TheObserverReadsTheAngle.lean: `observing_adds_nothing`, identidade angular específica.
- MAPA_LEVANTAMENTO.json: dephasing, ensaio v384/v385 e advertências de não refazer.

Hashes dos arquivos efetivamente lidos no recibo ao lado. Não foi rodado teste numérico, compilador ou provedor nesta revisão. Não houve mudança no Nós, Bancada ou gate.
