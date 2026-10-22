[DERIVED — contato suave da fonte, contração geral e companheiro BRST tipado; não é a soma da anomalia quântica]

# O que a referência suave transporta

O vértice de fonte já utilizado permite calcular a contribuição finita
de W_H no ponto de coincidência. Retêm-se as simetrias
W_ab|cd=W_ba|cd=W_ab|dc=W_cd|ab, sem supor isotropia. Esses dados têm 55
componentes independentes. Não se afirma que um tensor arbitrário assim
definido seja o jato de um estado Hadamard admissível.

Ponha S_ar=Σ_m W_am|rm e M_jr=∇_j c_r. Na normalização comum C_E
retirada do cálculo anterior, a fonte tem coeficiente

    R_ab^{jr}=-1/4[δ_jb S_ar+δ_ja S_br
                   +W_aj|br+W_bj|ar-2W_ab|jr].

A fórmula foi comparada diretamente com a contração anterior do vértice
para os 55 elementos da base de W, os dez da fonte simétrica e os 16
coeficientes M_jr. As 8.800 igualdades não pressupõem isotropia.

## Deformação e rotação

Escreva Gc=M+M^T e Ω=(M-M^T)/2. Defina dois mapas na fibra simétrica:

    W_direct(H)_ab=Σ_jr W_ab|jr H_jr,
    W_cross(H)_ab=Σ_jr W_aj|br H_jr,
    L_W(H)=-[SH+HS+2W_cross(H)-2W_direct(H)]/8.

Então o contato inteiro satisfaz

    R_W(M)=L_W(Gc)-[Ω,S]/4.

Essa identidade foi conferida em todos os coeficientes, com W simbólico.
O comutador [Ω,S] é simétrico porque Ω é antissimétrico e S simétrico.
Ele é precisamente a parte rotacional da derivada de Lie de S: no jato
covariantemente constante, L_c S={strain,S}+[Ω,S]. Isso localiza o dado
que se perde quando a referência anisotrópica é tratada como um escalar.
Não prova, por si só, que transformar W resolva a identidade BRST do par
completo de propagadores gauge-fixados.

A fatoração R_W=L_W G para TODOS os primeiros jatos de c existe na fibra
se, e somente se, S é escalar. Com efeito,

    R_ab^{jr}-R_ab^{rj}
      =-[δ_jb S_ar+δ_ja S_br-δ_rb S_aj-δ_ra S_bj]/4.

O mapa do espaço de matrizes simétricas S para esse defeito tem posto9
e núcleo de dimensão1 gerado pela identidade. Isso foi calculado em
aritmética exata. Equivalentemente, uma matriz simétrica que comuta com
todas as rotações é escalar. W inteiro não precisa ser isotrópico: a
condição recai somente sobre seu traço parcial.

Controle negativo: W=H⊗H, H=diag(1,0,0,0), dá S=H. Comparar os jatos
M_10=1 e M_01=1 preserva Gc e muda R_01 em -1/4. A parcela rotacional
de cada decomposição tem magnitude1/8. Não se pode escondê-la ajustando
coeficientes do mesmo Gc.

## Companheiro BRST, com o grau correto

Na família isotrópica do controle anterior,

    W_ab|cd=wI(δ_acδ_bd+δ_adδ_bc)/2+wTδ_abδ_cd,
    L_W(h)=a h+b g trh,
    a=-(wI+wT)/2,   b=-wI/8+wT/4.

Isso reproduz exatamente o contato já calculado. Considere o diferencial
livre s0h=Gc, s0h†=Eh, s0c=0, com h† ímpar e E o operador de Einstein
linearizado. O gerador local

    F_W=∫h†·L_W h

tem número de ghost -1. Sua variação é

    s0F_W=∫(Eh)·L_W h-h†·L_W Gc.

Esse par tem número de ghost ZERO: é uma modificação BRST-exata da ação,
não a anomalia de número de ghost1 e não sua primitiva já calculada.
O termo métrico tem Hessiana N_W=E L_W+L_W E quando E e L_W são
autoadjuntos. Assim, de EG=0 segue

    N_W G=E L_W G=E R_W.

A identidade plana de operadores foi conferida em todos os momentos
e polarizações com wI,wT simbólicos. A versão covariante segue da
identidade de composição sob as mesmas hipóteses tipadas; não foi
usada para alegar que os diagramas suaves efetivos geram esse N_W.
Com W variável, a composição E L_W inclui suas derivadas; não se pode
substituí-la por L_W E. A fórmula simples de fatoração requer a condição
sobre S no domínio em que for aplicada.

No setor anisotrópico, a parcela rotacional continua explícita. O
argumento de fatoração não a remove e não determina seu destino na soma
Ward. Isso é uma obrigação de transporte identificada, não a descoberta
de uma anomalia física não removível.

## Correção verificada ao parecer Kimi

No modelo polinomial bosônico, com α_W=exp(ħW∂²/2), vale

    T_{D+W}(F,G)=α_W T_D(α_W^{-1}F,α_W^{-1}G).

Foram verificadas exatamente todas as potências F=x^m,G=x^n, m,n≤4.
A fórmula do parecer que aplica α_W apenas às entradas, sem inversas
nem transformação da saída, falha já em F=G=x: perde o termo ħW.
O teste é bosônico; não certifica sinais ou fatores do transporte ghost.

Também não basta que um contato seja não nulo para decidir sua classe
de cohomologia. O termo fonte isolado e seu companheiro métrico precisam
ser distinguidos; a construção acima oferece um par exato, sem afirmar
que ele coincida com a soma dos diagramas. Condições de bisolução devem
usar o operador gauge-fixado pertinente: substituir H_gf por E_phys
exige um entrelaçamento demonstrado, que o parecer não forneceu.

Permanecem para o cálculo completo: outros contatos suaves, jatos de W,
compatibilidade BRST do par de referências, diagramas locais restantes,
K², aridades superiores e continuação causal. Nenhuma escolha de estado,
prescrição ou contratermo foi adotada nesta entrega.
