[DERIVED — contraexemplo integrado ao parecer; reutilização de provas anteriores]

O parecer DeepSeek7df6c82e foi lido integralmente. Para N formalmente
autoadjunto e chi fixo, a primeira variação correta de

    Bchi=-C_E/2 integral chi h.Nh

é -C_E integral delta_h.Mchi h, onde

    Mchi=(chi N+N chi)/2=chi N+[N,chi]/2.

A passagem do parecer integral chi h.N(delta_h) = integral chi delta_h.Nh
omite N agindo em chi. A antiadjunticidade de [N,chi] implica somente
integral h.[N,chi]h=0 para o mesmo argumento real. Não implica
integral delta_h.[N,chi]h=0.

Controle integrado independente: N=d^4, h=chi=(1-x²)^6 e delta_h=x²h
em [-1,1], prolongados por zero. As funções têm regularidade C5 nas
pontas; os termos de fronteira pertinentes são nulos. Dividindo por C_E:

    variação direta = 352187318272/38569325025;
    fórmula correta = 352187318272/38569325025;
    fórmula do parecer = 8589934592/7713865005;
    diferença = 103079215104/12856441675.

No mesmo controle, integral h.[N,chi]h=0. Isso isola o erro de inferência,
sem negar a propriedade antiadjunta. Foram41 controles, CPU0.34375s.

Não é necessário construir outro operador: fourth_order_cutoff_bridge já
continha Mchi e528 verificações. Seus hashes e os insumos foram conferidos,
sem executar os testes novamente. Para a completude curva, usar as palavras
inteiramente simetrizadas daquele artefato; as expressões ordenadas O3/O4
do parecer não podem ser identificadas com elas por comutação presumida.
O teste h01=constante também não verifica sozinho um operador diferencial.

Na descida, A1=-s0B e s0A2+s1A1=0 dão s0(A2+s1B)=0, assumindo
{s0,s1}=0. Acrescentar A1 não invalida a identidade total, mas mistura
aridades. A liberdade A2->A2+Z, s0Z=0, não torna automaticamente a classe
cohomológica independente da escolha: ela muda por [Z], que só é zero se
Z for exato. Nenhuma nulidade dessa classe foi demonstrada pelo parecer.

Reconciliação de Fourier: o parecer Kimi usa exp(-ipx), enquanto a perna
móvel do par usa exp(+ipx). As provas já existentes mostram respectivamente
C_E*(-i)^m e C_E*i^m. O gerador de grau espacial j tem grau de momento
n-2o+j, portanto i^(m-j)*i^(n-2o+j)/i=(-1)^order. As134 combinações
já testadas do par foram recuperadas e seus hashes conferidos, sem nova
execução. A discrepância ímpar não requer mudar os coeficientes do par.

Essa reconciliação fecha a pendência de convenção reaberta na auditoria
Fourier anterior; não fecha a soma quântica integral. Nenhum original,
prescrição, kernel ou gate foi alterado. Q2 completa continua OPEN.
