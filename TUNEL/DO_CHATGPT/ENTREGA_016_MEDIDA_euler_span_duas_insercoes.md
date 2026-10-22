[DERIVED — não pertencimento ao span de duas inserções; Q2 completa OPEN]

Hipótese examinada: a diferença de consistência do representante h,c seria
cancelável apenas por um peso global/alocação do regulador nos dois kernels
Euler ordenados já calculados. Nenhum coeficiente foi escolhido por ajuste.
Com lambda=(1,-1,0,0),eta=(1,0,0,0), extraímos572 linhas de coeficientes
polinomiais das16 componentes. Os dois geradores D_X,D_Y têm posto2; ao
adicionar a diferença medida F, o posto sobe a3. O resultado vale tanto
para F ordenado quanto para sua polarização dos dois cutoffs.

Uma testemunha exata usa a entrada00 e os monômios q0^5,q0^4q1,q0^3q1²:

                 D_X       D_Y         F
 q0^5            47/240    47/240     -3259/960
 q0^4q1           1/12        0          -1/2
 q0^3q1²         13/24      13/24      -541/96

O determinante é -847/13824, não zero. A polarização muda o terceiro
coeficiente da segunda linha para217/192 e conserva esse determinante.
Logo nenhum par de constantes a,b satisfaz F+a D_X+b D_Y=0.
É uma afirmação sobre os kernels que efetivamente calculamos, não sobre
todas as normalizações possíveis de inserções compostas. Não se atribui
classe de obstrução BV a esse resultado. O tau permanece não escolhido.

Há também uma separação de ordens útil, sob hipóteses explícitas: se W1
é o tadpole LOCAL de um único vértice cúbico, é linear nos campos; se A1
e J1 são os correspondentes termos locais de número de ghost1, são
lineares em c após integrar por partes. Escreva W1=int h_ab F_ab e
A1=int c_a f_a, J1=int c_a j_a, com coeficientes independentes dos ghosts.
Na projeção de dois ghosts e nenhum campo par, (W1,I1) vem de
delta I1/delta hdagger=-[G,chi](c.dc); (V1,A1) e (V1,J1) vêm do
vértice cdagger chi(c.dc). Cada expressão tem no máximo UMA derivada
sobre um ghost; a adjunção ponderada não aumenta essa ordem. Assim
esses três termos locais de primeira ordem NÃO alteram o menor de grau5
acima. Isto não supõe W1=0, nem cobre W1 não local, nem elimina J2 completo.

O alvo seguinte é a normalização diferencial completa das inserções e dos
termos de descida de J2, inclusive o vínculo entre o representante calculado
e a anomalia A2. Não basta reescalar os dois Euler kernels ou declarar
tadpoles nulos. A identidade inhomogênea permanece a referência escrita:
s0 A2+(V1,A1)+(W1,I1)+s0 J2+(V1,J1)=0.

Auditoria independente Kimi ee44: suas cinco famílias de J_b coincidem
com current_terms nos16 pares(mu,r); o toy -18/2401*gQ*gD confere.
Porém, a convolução com o adjunto formal impõe gD*ell=-2gQ, não+2gQ.
O inverso já verificado usa gD=-4kappa,ell=1/(2kappa),gQ=1 nas unidades
do kernel comum. O b_column já traz os dois deltas: no controle diagonal
ele vale-4/49, contra-2/49 se se retiver só a fibra de traço invertido.
Logo o termo de traço não está ausente do motor. Não o somar novamente.
Substituir dc por eta*c é avaliação especial do campo externo, não o
adjunto(d-eta) do diagrama; o motor conserva esse adjunto. Sua escala v3
é+1/4 por contração ordenada, derivada antes, não a escala/16 do antigo
motor métrico citado pelo parecer. Nenhuma alteração do engine foi feita.

Sete verificações do span,30 da auditoria; CPU total1.390625s,rc0.
Kimi ee44:370528tokens,1011.191s; assinatura sem custo por chamada informado.
Recibo já lançado uma única vez. Provas/checagens anteriores não recontadas.
Comandos: python A7/euler_descendant_span_diagnostic.py e
python A7/audit_kimi_mixed_current_normalization.py (runtime SymPy de A4,
-X utf8 -B; intake é único, não repetir custos). Logs e hashes no manifesto.

Estado coordenado15:46:11UTC: MiMoa369 e Kimi5e1 RUNNING no worker91153;
Kimi51c admitido no job039cab4b-a3a1-4cad-8d8c-349a55d705b3 após e710.
Mantidos cinco admitidos, FIFO e prazo20:32UTC. Originais/kernel/gate intactos.
Abertura sha256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
