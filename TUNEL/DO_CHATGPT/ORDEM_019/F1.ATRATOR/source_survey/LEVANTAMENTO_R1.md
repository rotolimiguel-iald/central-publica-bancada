# F1.ATRATOR — levantamento antes da construção

Autor: codex-gerente-tgl / subagente atrator_sources. [DERIVED — leitura documental]. Fontes, linhas completas e SHA-256 medidos estão em FONTES_R1.json. Nenhum experimento foi executado neste levantamento.

## O que já existe e deve ser reaproveitado

1. **S de fronteira:** SMatrix.lean:40–47 e 66–69 define S(θ)=[[cos θ,sin θ],[-sin θ,cos θ]]. Linhas 100–113 provam unitariedade; 234–256 dão reflexão −sin θ, peso sin²θ e conservação da soma dos pesos. O inventário da Bancada (INVENTARIO_KERNEL_CADEIA_BETA_20260928.md:49–52,62–64) localiza a ligação β↔reflexão e diz onde α_CODATA√e é calculado em runtime. ProgrammerRule.lean:45–58 chama ℂ² de estado do canal de espelhamento, mas a dinâmica ali é rotação unitária.
2. **Semigrupo dissipativo no referencial S:** GlobalLiftLadder.lean:173–215 define Ad(S†)∘D_t∘Ad(S), prova a lei de semigrupo e convergência à esperança diagonal conjugada. Esse espaço fixo tem duas direções na face 2×2: serve como controle sem unicidade; não fornece A4. A docstring 190–192 diferencia-o de D_t∘Ad(S), que sozinho não é aquela família de semigrupo.
3. **Projeção e letra:** ExactWitness.lean:80–84 identifica o operador auto-adjunto que pousa e fixa K com K.starProjection; 107–126 identifica P_ker A=q(A)/q(0) sob a hipótese aniquiladora Xq, q(0)≠0 e coeficientes reais. WordExistence.lean:167–173 e 219–226 constrói essa palavra na face finita auto-adjunta com núcleo não trivial. InfiniteWord.lean:140–149 tem a projeção por cálculo funcional sob zero isolado no espectro. Para o novo T discreto, o operador a usar nesta ligação é A=I−T, cujo núcleo é Fix(T), preservando a tipagem.
4. **PALAVRA e releitura:** work/leitura_cria_o_objeto_07out/Palavra.lean:14–20 registra a cunhagem do polinômio normalizado como LETRA. Linhas 99–108 compõem primeira leitura e releitura com o teorema existente. TheObserverReadsTheAngle.lean:108–116 dá P₊(P₊Oθ)=P₊Oθ, por idempotência. Não afirma que o ângulo evolui para limite. PALAVRA está como candidato no work; não foi encontrado TGLExt/Palavra.lean no kernel canônico lido. Mapa seq750 registra nome e instalação para v392; isso não é instalação comprovada.
5. **Fluxo do lock mínimo:** TheAxiomAndTheFalseWitness.lean:104–164 já define F(t)=P+exp(−t)(I−P), prova semigrupo, fixa P, converge a P e identifica a exponencial. Mapa seq349 corrige a leitura da seq344: a exponencial já é termo. A ligação geral desse lock com um gerador GKLS físico continua hipótese separada.
6. **GKLS v384:** o V1 da Bancada:76–88 já exige unicidade por espectro, mede toda a grade e inclui dephasing degenerado como controle N1. O worker:208–226 chama UNIQUE quando há exatamente um autovalor dentro do limiar zero e todos os outros têm parte real negativa separada por gap. O resultado original foi apenas lido: T2 672/672 únicos; T4 21100/21100; D128 n0=1 UNIQUE. N1 tem n0=14,22,38,70 para d=8,16,32,64, n_c=3. Reusar mapas 294,295,338,345, sem repetir a campanha.

## Canal novo mínimo e hipóteses nomeadas

**Primário proposto:** medir populações incoerentes e repreparar entre passos, T_pop=|S|²=[[1−β,β],[β,1−β]], β calculado em runtime; R_pop=J/2. A passagem de amplitude unitária a população é uma hipótese instrumental sintética explícita, não inferência de dissipação de S. O canal de matrizes correspondente é D∘Ad(S)∘D, distinto da família sFrame. Nomear a contração estrita no complemento do modo de massa conservada e fixar normalização μ=1; a unicidade de um estado normalizado não diz que o subespaço linear de pontos fixos contém um único vetor (ele contém os múltiplos do modo estacionário).

**Regimes:** θ fixa a amplitude de leitura. Nenhum limite θ→∞ é pedido. A contração do canal de populações e a parametrização dissipativa do complemento pertencem ao sistema aberto; não identificar por nome com o boost hiperbólico de outro tipo sem um lema.

**A4:** não-comutatividade isolada dos saltos não é hipótese suficiente em dimensão arbitrária: pode sobrar um setor espectador. Usar contração estrita do complemento/hipótese ergódica nomeada. v384 sustenta unicidade medida nas instâncias construídas, não um teorema para qualquer família de saltos não comutantes.

**Controle sem ponto fixo:** um mapa linear tem sempre zero fixo e um canal finito CPTP tem ao menos um estado estacionário. Uma dinâmica sem nenhum ponto fixo deve ser declarada fora dessa classe (por exemplo, translação afim não compacta). Um ciclo não convergente pode ter média de Cesàro convergente, logo não o chamar de falsificador da alternativa Cesàro sem testar a alternativa escolhida.

## Lacuna que esta unidade pode preencher

Compor A1–A4 em uma interface explícita Hilbert/face finita, ligar R à starProjection de Fix(T) e à letra normalizada, medir os controles sob tolerâncias prévias e produzir candidato Lean em sandbox. As fontes já dão os blocos; o levantamento não certifica a nova pedra nem a execução do teste. A cunhagem singularidade/leitura é [ONTO]; o teste mede validade matemática na face indicada.
