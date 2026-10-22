[DERIVED — integração por partes; REAL — CAS exato; OPEN — soma de Ward]
# A7.b — derivar antes de ancorar
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T08:20:00.631350+00:00.

Implementado o cálculo de jatos covariantes no extremo Y dos propagadores
bilocais, mantendo todos os índices de derivadas como slots tensoriais.
O ghost tem índice superior em X, com sinal positivo da conexão; os
índices em Y são inferiores. O tensor métrico carrega dois em cada extremo.
O auxiliar w=(X-Y)² só é imposto depois das derivadas e da ancoragem.

Os comutadores [D_i,D_j] no extremo Y foram cotejados com a ação explícita
de R^a_bij/K=delta_ai delta_bj-delta_aj delta_bi:232 identidades simbólicas,
com todos os componentes ghost e os100 componentes simétricos métricos,
para os pares de derivadas(0,1) e(1,3). Isso testa os pares especificados;
não é uma afirmação de execução exaustiva para toda palavra arbitrária.

**Redução que será aplicada aos laços.** Considere a contribuição bilocal,
com o teste em X absorvido nos coeficientes e k=G(c) em Y:

 B[h,k]=int dvolX dvolY [B0^(ab) k_ab+B1^(jab) D_j k_ab],
 B0 e B1 simétricos nos últimos índices a,b.

Para c compacto, a integração por partes dá o coeficiente de c_b:

 W^b=2[-D_a B0^(ab)+D_a D_j B1^(jab)].

Em Y=0 de UMA carta RNC fixa, a primeiraK:

 W^b=2[-partial_a B0^(ab)+partial_a partial_j B1^(jab)]
      +K[8/3 sum_a B1_0^(aab)-2/3 sum_a B1_0^(baa)]+O(K²).

Os coeficientes B são componentes coordenadas ANTES de ancorar. Os termos
adicionais vêm da derivada da conexão na primeira divergência. Escrever
Gamma(0)=0 e descartar suas derivadas apagaria esses termos. A simplificação
usa a conexão RNC da bancada e a simetria a,b; não aplica dY=-dX.

**Controle independente.** Expandiu-se a forma fraca em c_b, partial_i c_b
e partial_i partial_j c_b, mantendo sqrt(g)=1-KY²/2. A derivada de Euler
coordenada foi comparada ao motor de divergências. Os oito coeficientes
(quatro componentes, ordensK0/K1) coincidiram em campos polinomiais racionais.
Suprimir as derivadas da conexão dá resíduos304/3,344/3,128,424/3 nesses
campos: quatro controles negativos. Não foram ajustados coeficientes de laço.

O primeiro checker falhou em rc1 porque extraiu coeff(K,0) de expressão
ainda não expandida; v2 expande antes de extrair. O motor foi preservado,
assim como o log falho. O v2 terminou rc0,240 checks,CPU10.796875s.
O custo da tentativa v1 não foi medido. Fontes e logs no manifesto.

**Limite preciso:** B0/B1 ainda não foram preenchidos pelos vértices Wick
completos. Esta etapa fornece a redução e o motor de derivadas; não fornece
o coeficiente totalQ2. Os contatos do regulador, tadpoles, W e aridades
superiores continuam separados. Próximo: inserir os pares métricos/ghost
no mesmo cálculo, depois comparar com a fonte Einstein na mesma prescrição.

Orquestração: a revisão MiMo0e8fc209 terminou IncompleteRead, sem resultado,
uso/custo desconhecidos; não repetida. A coordenação informou início único
do Kimi96648157 (quartico métrico), sessão28410 de sua propriedade.
Nenhum original, kernel ou gate alterado. A7.b continua ativo no timebox.
