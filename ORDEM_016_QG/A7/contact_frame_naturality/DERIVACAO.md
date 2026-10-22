[DERIVED — ponte local de frame, naturalidade dos núcleos e localização da primitiva, até O(K); Q2 completa OPEN]

# Da distribuição local à leitura covariante

Os cálculos se referem ao espaço-forma euclidiano auxiliar 4D, com Ric=3Kg.
K é curvatura constante. Não foi selecionado um horizonte físico ou estado W.

## Transporte dos dois extremos

A transvecção de eixo i em coordenadas normais tem expansão

    k_i^a(X)=δ_i^a-(K/3)(X²δ_i^a-X^aX_i)+O(K²).

A equação de Killing foi verificada para cada componente da métrica nos
dois extremos. Aplicando a derivada de Lie simultânea em X e Y, antes de
ancorar Y=0, os propagadores declarados obedecem

    (L_k^X+L_k^Y)G_ghost=0+O(K²),
    (L_k^X+L_k^Y)G_metric=0+O(K²).

Para o ghost, o índice superior X recebe -∂k e o inferior Y recebe +∂k.
Para o propagador métrico, os quatro índices inferiores recebem +∂k.
O teste cobre todos os componentes e os quatro geradores, sem amostragem
de posições: X e Y são simbólicos e só ao final w=(X-Y)² é imposto.

A correção da distância é

    ρ²=w-(K/3)(X²Y²-(X·Y)²)+O(K²).

Sua derivada de Lie conjunta anula-se à mesma ordem. A de w sozinho não.
O resíduo explícito de cada eixo foi conservado em results.json. Logo,
regularizar por ρ^(2a), com μ constante, respeita essas isometrias até O(K).
Usar w^a em um único chart fixo não tem essa propriedade. Isso não seleciona
um regulador por decreto: registra uma diferença estrutural entre as duas
completações que já foram medidas separadamente.

## Frame e jatos simétricos

A co-base radial paralela é

    e_a^r=δ_a^r-(K/6)(X²δ_a^r-X_aX^r)+O(K²).

Foram verificadas X^i∂_i e_a^r-X^iΓ^r_ia=O(K²) e Γ^a_ijX^iX^j=0.
Assim, na curva exp_Y(tv), derivar componentes em frame paralelo equivale
a derivar covariantemente ao longo de v. Polarizar em v dá

    ∂_(i1...in) h_frame(Y)=∇_(i1...in)h(Y)

no ponto de origem, com as fibras identificadas pelo frame. Isso vale
também para o produto tensorial que representa h_ab. Não exige que os
jatos ordenados comutem: os comutadores continuam necessários quando
se compõe a Hessiana com o gerador de gauge.

## Sinal do contato

Na convenção medida, a densidade de volume em X já entrou na extração
do resíduo. Portanto ∂_X^nδ age sobre o teste h_frame com (-1)^n.
Após a integração em Y, a integração por partes que põe as derivadas
em c fornece outro (-1)^n. Para n=5 ou3, o produto dos sinais é positivo.
A transposição das fibras deve acompanhar essa operação.

Com coeficientes geométricos paralelos e as palavras completamente
simetrizadas, reverter uma palavra sob adjunção preserva a média das
palavras. Daí o operador sobre c possui os mesmos coeficientes da
tabela normal, na convenção de completação declarada. O teste de símbolos
confere os dois sinais em todos os componentes; omitir uma transposição
produz o contraexemplo registrado.

Para o regulador geodésico, os ingredientes bilocais agora têm sua
naturalidade explícita verificada. A aplicação desse argumento à soma
inteira ainda pressupõe que os vértices e a integração foram montados
tensorialmente como declarado nos motores anteriores. Não se usa esta
checagem isolada para certificar novamente toda a montagem de diagramas.
Para o regulador coordenado, persiste a ressalva de naturalidade global.

## Adjunção e corte de quarta ordem

Escreva a Hessiana como

    N=C^{ijkl}∇_(ijkl)+K D^{ij}∇_(ij),

com os índices de fibra suprimidos. C e D são paralelos, reais, simétricos
nos índices de derivada e sob troca das duas fibras. A última propriedade
foi conferida nos dez elementos de base de tensores simétricos, com todos
os momentos simbólicos e b,c,t livres. A reversão das palavras dá N*=N.

Uma corrente de Green que torna a integração por partes explícita é

    J^i(X,Y)=C^{ijkl}[X·∇_jklY-(∇_jX)·∇_klY
                         +(∇_jkX)·∇_lY-(∇_jklX)·Y]
              +K D^{ij}[X·∇_jY-(∇_jX)·Y].

As contrações com C e D incluem os índices de fibra. Sua divergência
é X·NY-(NX)·Y: os termos intermediários cancelam por renomeação dos
índices simétricos, sem supor derivadas covariantes comutativas.

Para Bχ=-C_E/2∫χ h·Nh e sχ=0, a primeira variação é governada por

    Mχ=(χN+Nχ)/2=χN+[N,χ]/2.

Para qualquer palavra I, a identidade de Leibniz ordenada é

    [∇_I,χ]h = Σ_{S não vazio} (∇_{I|S}χ)(∇_{I|S^c}h),

onde subsequências preservam a ordem dos índices. As conexões sobre os
índices derivados são incluídas. O CAS compara essa soma à derivação
direta de χh em coordenadas normais, com χ de grau4 e h tensorial de
grau4. As 528 verificações incluem a transposição completa dos coeficientes.
Não são apenas verificações de símbolos planos.

Consequentemente, no recorte NG=A_cov+O(K²),

    s0Bχ=-C_E∫h·[χA_cov c+[N,χ]Gc/2]+O(K²).

Na forma integrada contra c, aparece ainda a ação de G* sobre χ; ela
não deve ser descartada. Há até quatro derivadas do corte na forma acima
e até cinco após aplicar G*. A localização é BRST-exata como variação
dessa Bχ; isso não prova que todo o contato quântico localizado seja
essa variação. Essa comparação exige os demais diagramas.

O mesmo Mχ entra em s1Bχ com δh=L_c h. A combinação da próxima ordem
continua A2+s1B, não A2-s1B. Não foi calculada A2 nesta entrega, nem
escolhida uma primitiva cúbica. O resultado não cobre W geral, K²,
ou a continuação causal lorentziana.
