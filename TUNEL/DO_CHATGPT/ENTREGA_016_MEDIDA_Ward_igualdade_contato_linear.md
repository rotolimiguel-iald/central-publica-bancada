[INPUT/ONTO — correspondência do operador; DERIVED+CAS — contato principal; A7.b integral OPEN]

Fala do operador, verbatim: «Identidade de ward é o operador de “=“».
Registro de bancada, sem alteração do Atlas, do kernel ou do programa terminal.

Na leitura proposta, Ward realiza o critério de compatibilidade entre transformação
e leitura. A expressão tipada atualmente usada é shat0 T1(F)=T1(s0F+A1(F)).
Os mapas shat0 e T1 fazem operações distintas; a igualdade relaciona seus resultados.
A correção A1 não se torna nula pela nomenclatura, nem uma classe não trivial foi
demonstrada apenas por haver representante não zero. Não foi criado operador novo.

Ligação concreta aos contatos existentes: a normalização de uma entrada linear
deve usar a distribuição de Green inteira. No controle euclidiano principal,
o fluxo pela esfera S3_r dá (2pi²r³)(-2/r³)=-4pi²=CE. Logo
Delta(1/r²)=CE delta, embora a expressão pontual seja zero fora da origem.
O motor já calcula C_w=(R(D_w f)-D_w R(f))/CE. Assim
D_w R(f)=R(D_w f)-CE C_w; para w=(i,j), C_ij=-delta_ij/4.
A parcela acrescentada à extensão da derivada pontual é -pi² delta_ij delta.
Sua soma é exatamente CE delta. O controle sem contato perde a fonte inteira.

Verificadas também as composições até três derivadas:
C_(w,i)(f)=C_i(D_w f)+q_i C_w(f), em todos os índices ordenados ensaiados.
Isso conecta os contatos à normalização diferencial de uma linha, preservando
a prescrição R já registrada. Não é a soma da Ward com duas interações.
Com uma entrada linear, há no máximo uma contração cruzada; a extensão de um
produto com duas linhas não precisa ser recalculada para esta verificação.
A compatibilidade global dos produtos compostos, porém, não segue dessa contagem.

[KNOWN] Fröb, arXiv1803.10235v3, equações158 e Teorema9, permite impor a
concordância perturbativa linear por renormalização. Sua prova, eq174–180,
identifica a diferença local a remover; não afirma que qualquer prescrição radial
prévia já satisfaça todas as condições. Fonte lida nesta rodada:
https://arxiv.org/pdf/1803.10235v3 .

Ainda preservar: o resto suave curvo do Green, a mesma representação de Wick,
as duas inserções A1 e a normalização dos operadores compostos. O cálculo
presente não apaga A1=(i hbar)alpha int chi div(c), nem determina alpha físico.
Resultado: 104 controles exatos, CPU 0.171875s, rc0.
Próximo ramo do mesmo A7.b: montagem de duas entradas, incluindo esses contatos
e os termos de cutoff. Q2 completa continua OPEN. Nenhuma chamada externa nova.
Abertura SHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
