[DERIVED — cálculo local auxiliar e auditoria; Q2 curvo OPEN]

# Resto de Euler do parametrix no espaço-forma

Reutilizados os coeficientes de calor e a conexão radial já calculados.
Em dimensão4 euclidiana, z=r², L=∇²+K E, na normalização singular1/z:

 Hsing=U0/z-U1 log(z/ell²)/4+U2 z log(z/ell²)/16.
 [L Hsing]=3 U2/4.

O coeficiente U2 já inclui K². A recorrência de transporte cancela o log;
o termo quadrático da conexão cancela a dependência direcional restante.
O controle que omite a conexão falha. Resultados dos blocos mínimos:

 [L Hsing]_metric=K²(-21 P_TL/20+479 P_tr/20),
 [L Hsing]_ghost=179 K² Id4/20.

Controle escalar radial independente com potencial E dimensional:
 [L Hsing]_scalar=3E²/8+3EK/2+29K²/20.

São 14 verificações, CPU0.28125s.
O traço ponderado métrica/2-ghost é -571K²/20; NÃO é A1 nem A2.
O sinal inverte ao usar D=-L. Para Hsing+W ser bisolução, a parte suave
deve satisfazer [L W]=-3U2/4 nessa separação. Isso é condição necessária;
nenhum W, estado, propagador não minimal22x22 ou continuação lorentziana
foi construído. Não se impôs uma escolha suave para cancelar a anomalia.

O resultado localiza por que a normalização plana anterior não se transfere
automaticamente ao fundo curvo: o argumento de comutação Wick-BV usava PH=0.
O próximo alvo é o defeito de aridade1 em termos de PH e QH, sem substituir
esse defeito por um traço de calor. Nova unidade MiMo87d preparada para isso.

# Auditoria DeepSeek6309 — aceitação parcial e correção explícita

Resposta original preservada integralmente como DECLARADO. Os passos1–3
conservam corretamente a multiplicidade de h_ii e o sinal:
 -(∂i+lambda_i)R(F)=R(-(∂i+lambda_i)F)+C_i(F).

Os passos6–7 são recusados. Não se somam operadores ∂+lambda e -∂+eta
antes de aplicá-los aos kernels trocados, que incluem índices transpostos,
cutoffs permutados e x invertido. A frase de que R comuta com derivadas
contradiz o C_i não nulo definido no próprio pedido. L_i F=0 tampouco
é equivalente a L·∂F=0.

Defina B_(ghost,r) pela soma real -(∂i+lambda_i)F_(ij),r, contando duas
vezes quando i=j. A condição de cancelamento da parte bilocal é

 B(lambda,eta;x)-B(eta,lambda;-x)^T=0 fora da diagonal,

com a compatibilidade da extensão explicitamente conservada. Ela precisa
ser verificada nos kernels; não é uma condição escalar L·∂F=0.
Contraexemplo: apenas F_(00),0=z^-2 não nulo dá
16x0/z³+2(eta0-lambda0)/z². Mesmo L=0 não remove a derivada.
Mais diretamente, F=1, lambda0=1, eta0=0 tem L·∂F=0, mas descendente=-2
fora da diagonal. Marcadores são jatos locais; não se assume integração
global convergente dos exponenciais. O adjunto local é D*=-D-L.
Também C0(∂0(1/z))/CE=-1/4: omitir a passagem da derivada por R perde contato.
São 6 controles adicionais, CPU0.1875s.

O passo10 também extrapola: igualdade de descendentes não prova trivialidade
BRST do funcional bilocal, nem identifica a classe de anomalia. A diferença
pode ser fechada sem ser exata. Conservamos a distinção entre contatos
medidos, inserção J2 e mapa A2, bem como a dependência de A1 ainda aberta.
A auditoria não modifica as16 componentes previamente calculadas, que já
verificavam os dois kernels e o contato C_i separadamente.

Nenhum original, kernel ou gate alterado. Abertura SHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
