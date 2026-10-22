[DERIVED — inserção Euler condicionada à normalização; Q2 completa OPEN]

No auxiliar plano e na prescrição radial existente, a linha do Euler completo
obedece P_hh N_hh+P_hb N_bh=box I10 como identidade polinomial, para qualquer
kernel escalar. O termo de b é necessário: omiti-lo deixa uma matriz não nula.
Isso explica por que substituir E_h por apenas a Hessiana EH seria incorreto.

Para precisar a normalização de inserções, mantivemos o MESMO produto
z^(a-2)=f_a g_a, com f_a=z^(tau*a-1),g_a=z^((1-tau)*a-1), z>0.
tau é uma alocação diagnóstica do regulador, não parâmetro da TGL nem escolha
de estado. Ele não foi ajustado ao resíduo. Dividindo contatos por CE=-4pi²,
o polo simples da prescrição já existente fornece:

 FP[(1-a)(box f_a)g_a] = tau*q²/8;
 FP[(1-a)f_a(box g_a)] = (1-tau)*q²/8.

Aqui box f_a=4*tau*a*(tau*a-1)z^(tau*a-2), e o resíduo normalizado de
z^(a-3) é -q²/32. Só o coeficiente linear ema contribui nestes termos.
Para derivada em uma linha: (box f_a)d_j g_a dá tau*q_j*q²/24;
(d_j box f_a)g_a dá tau*q_j*q²/12. A soma é a derivada do primeiro contato.

Não se alterou a extensão do produto ordinário. A correção dos gradientes
cruzados na regra de Leibniz é q²/4; somada aos contatos Euler q²/8 dá
3q²/8, exatamente -C_box(z^-2) do motor radial existente. O total independe
de tau. Este cálculo mostra uma liberdade na normalização da inserção
diferenciada antes da multiplicação; não estabelece qual normalização de
produtos temporais satisfaz todas as identidades BV. Não se definiu delta*f
por multiplicação de distribuições nem se adotou f(0)=0.

A contagem de campos distingue corrente e vértice de anticampo. A corrente
hdagger*c*c não tem bubble de DUAS linhas com barc*h*c, pois hdagger não
contrai. Após s0hdagger=E_h, existem dois emparelhamentos com duas linhas,
deixando dois ghosts externos; h e b devem compor a linha Euler completa.
Já o VÉRTICE hdagger*h*c admite duas linhas, deixando hdagger e c externos.
Logo não se pode excluir todo o setor de anticampo pela contagem da corrente.

Foi calculado também o contato ORDENADO I_E,X Vghost,Y, onde
I_E=sum_A E_A[G,chiX]w_A e Vghost mantém a forma anterior à IBP como origem
dos sinais. Ambos os emparelhamentos de w=c.dc foram retidos, com sinais-,+.
Para lambda=e0-e1,eta=e0, foram852 termos; ordem de cutoffs trocada,532.
As16 entradas B_ur(D) e a parte B-B^dagger estão nos resultados. O adjunto
ponderado usa B^dagger=B^T(-D-lambda-eta). No controle q=0, a entrada01 é
-187*tau/192. Este é um candidato explícito na família declarada, SEM fator
global Ward/ação efetiva, SEM soma automática dos cutoffs e SEM seleção de
tau. Portanto não foi somado ao resíduo anterior para anunciar cancelamento.
A necessidade seguinte é derivar a normalização EOM compatível e o peso
global da descida, incluindo o setor de fontes e a identidade inhomogênea.

Recebido e auditado MiMo6307. Sua proposta de cancelamento é refutada pela
regra da cadeia (d_X f(Y-X)=d_X f(X-Y)), pelo cálculo exterior(-,+), pelo
vértice Lie_c h que foi indevidamente reduzido ah, e pelo controle pedido:
2357/117649+314/117649=2671/117649, não zero. A resposta e o recibo foram
preservados; nenhum engine foi alterado para acomodá-la. Uso medido365857
tokens; custo estimadoUSD0.17379642, não fatura; ledger uma única vez.

297controles locais,CPU4.203125s, quatro comandos rc0 com logs custodiados.
Alcance: contatos racionais auxiliares e diagnóstico de normalização.
Q2 integral, normalização lorentziana e gate permanecem sem fechamento novo.
Abertura sha256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
