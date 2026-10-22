[DERIVED — componente logarítmico local e primitiva; REAL — CAS; OPEN — Q2 completa]
# A7.b — Ward K², tadpole linear e primitiva quadrática
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T05:14:19.990968+00:00.

**Calibração:** jatos covariantes da 1-forma até ordem5 e K², incluindo
coframe e conexão do espaço-forma. A derivada dupla da identidade
clássica E G(c)=0 foi conferida em768 componentes;48 componentes
reproduzem a Ward primeiraK anterior. Duas extrações completam818
controles. Não se impôs zero à Ward de laço.

Retirando i*hbar*A0, A0=1/(8pi²), na base K²[G(v),g(p.v)]:

    H_loop G = [4/3,−20/3]
    E R      = [20/3,8/3]
    soma     = [8,−4].

A fonte já paga é R=G(3Box(v)/8−grad(divv)/4−37Kv/8)+2Kg divv.
Usando E G=0, E R=−4K Hess(divv)+4Kg Box(divv)+12K²g divv.
Essa fórmula e os jatos dão os coeficientes acima sem ajuste.

**Tadpole linear:** contração dos vértices cúbicos com os Green
coincidentes. A densidade é hbar*A0*K²*tau*trh, com tau_métrica=−6,
tau_ghost=0, tau_total=−6. Dez fibras verificam a proporcionalidade
ao traço,31controles. A variação não linear clássica desta densidade,
integrada com suporte compacto, contribui tau*K²[G(v)−g(p.v)].
Logo o resíduo medido DEPOIS dessa parcela é

    R_K2(v)=2K²[G(v)+g(p.v)],

e continua não nulo. A primeiraK permanece

    R_K1(v)=K[−p²G(v)/2+2pp(p.v)−5gp²(p.v)/2].

**Primitiva local desse componente:** na convenção de símbolo covariante
com derivadas simétricas, defina o operador formalmente autoadjunto
deltaH_t. Seu símbolo Kp², na base
[p²trAB,p²trA trB,pAp trB,pBp trA,pABp], tem coeficientes

    [1/2−t/2, 9/4+t/2, −1−t/2, −1−t/2, t].

A contribuição desse operador à Ward K² é[−t−13/3,2t+38/3].
Acrescente o símbolo K², na base[trAB,trA trB],

    [t+7/3,−t−22/3].

Então deltaH_t G(v)=−R_K1(v)−R_K2(v) nas ordens calculadas,
para todo t real.97controles polinomiais, incluindo um momento fora
do eixo usado na determinação dos coeficientes.

O funcional é explícito:

    B_t[h]=(1/2) integral h·deltaH_t h,
    s0 B_t=integral h·deltaH_t G(c).

Autoadjunção usa os coeficientes invariantes paralelos, simetria entre
as fibras, duas derivadas simetrizadas e suporte compacto. Assim, o
componente logarítmico integrado, linear em h e c, aqui MEDIDO admite
essa primitiva relativa ao diferencial livre. Não é uma conclusão sobre
todos os componentes da anomalia não linear nem sobre sua parte finita.

**A liberdade t foi identificada, não escolhida:**

    partial_t deltaH_t = −K E/2.

640 controles, dez fibras e dois momentos, verificam a igualdade nas
duas ordens homogêneas. Ward não determina esse parâmetro porque
E G=0. Isso não classifica as31direções do ajusteA2 anterior e não
demonstra não trivialidade de uma classe na cohomologia BV completa.

**Cutoff e continuação:** para chi inerte e B_chi=1/2 integral chi h·D h,
a polarização fornece s0 B_chi=integral h·(chi D+[D,chi]/2)G(c).
Reutiliza-se a identidade já verificada em finite_cutoff_contact e
finite_cutoff_position; seus testes anteriores são planos e não são
apresentados como novos testes curvos. Aqui D=deltaH_t tem ordem2:
se sua parte diferencial é K C^ij nabla_(i nabla_j),

    [D,chi]T=K C^ij[(nabla_i nabla_j chi)T+2(nabla_i chi)nabla_j T].

O termo K² comuta com chi. Esses contatos precisam entrar; a parte
s1 B_t, de ordem h²c, também não foi apagada. A identificação com a
quebra completa da prescrição temporal ainda exige essa hierarquia.
Nenhum t selecionado, contratermo adotado ou prescrição alterada.

Pacote:1586 controles, CPU13.515625s. Falhas técnicas preservadas:
primeiro avaliador omitiu uma soma em m (NameError, versão v2 ao lado);
primeira invocação da auditoriaEinstein usou Python semSympy (rc1),
seguida pelo runtime simbólico já existente (rc0), sem instalar pacote.
Logs, fontes, predecessores e resultados têm hashes no manifesto.
Gate, kernel e originais intactos. A7.b continua; Q2 completa OPEN.
