[DERIVED — contato de extensão dos pares planos localizados; Q2 OPEN]

Prescrição mantida: R=FP_a[(1-a)mu^(2a)z^a(.)], z=(X-Y)^2,
CE=-4pi². Q_i denota derivada de delta, não momento de Fourier.
Os kernels foram contraídos a partir dos vértices completos EH e ghost,
incluindo suas correntes de fronteira. Não se reconstruiu o par a partir
da identidade de Ward reduzida.

Para cada monômio x^p/z^n usa-se C_D=R D-D R e a regra de Leibniz:
C_D(x^p/z^n)=sum_{I subset D} (partial_I x^p) C_{D\I}(z^-n).
Multiplicar x_i sobre derivadas de delta equivale a -partial_{Q_i}.
O operador de adjunção tem, em Y, -(eta_a-d_a) para h e
(eta_a-d_a)(eta_j-d_j) para partial_j h. Em X, multiplica-se por
-(lambda_i+d_i) quando a perna externa é partial_i h.
O contato P-Q, com P=O R(F) e Q=R(O F), é -C_O(F).
Conserva-se a multiplicidade simétrica 2/m_ar e a orientação do laço
ghost (segundo vértice transposto), além da divisão16 do par métrico.
Por fim chiX é removido à diagonal pela substituição Q -> Q-lambda.
Conservar apenas chiX(Y) omitiria derivadas de delta já verificadas.

Foram usados jatos exponenciais locais: chiX=e^(lambda.X),chiY=e^(eta.Y).
Um cutoff compacto pode coincidir com esses jatos na região do teste.
Três configurações: (lambda,eta)=(0,0),(0,e0),(e0-e1,e0).
Isso não constitui verificação de lambda,eta arbitrários.

Primeira etapa:85 verificações, incluindo contrações cruas no ponto
(1,2,-1,1) contra os motores localizados numéricos existentes. Segunda:
177 verificações; todas as10 polarizações simétricas,4 componentes ghost,
3 configurações:120 polinômios. O reuso dos resultados11,0 anteriores
é explícito; não se conta reexecução que não ocorreu.

Para h11,c0, em Q=(2,1,0,0), (ghost-metric/2)/CE dá respectivamente
153/64,21259/1920,-7351/640. Polinômios completos nos JSONs.
No caso constante, a fonte previamente calculada tem coeficientes
(-3/32,0,3/32) na base invariante de posto3/grau5. Sua soma aos pares
reproduz (-139/1920,99/1280,217/960) em TODAS as40 componentes.
Essa recuperação verifica normalizações/sinais sem apagar os contatos.

Limite: são contatos de extensão dos pares singulares planos. Ainda
faltam na montagem atual os termos da fonte correspondentes à fronteira
ghost pré-integração, inserções da corrente clássica, partes suaves,
curvatura, aridades superiores e continuação causal. Um contato não
nulo do par não é, sozinho, uma anomalia obstrutiva. Q2 completo não foi
calculado. Os testes CAS não foram apresentados como compilação Lean.
