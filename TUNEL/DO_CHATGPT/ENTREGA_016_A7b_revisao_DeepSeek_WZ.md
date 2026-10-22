[DERIVED — consistência WZ com convenções explícitas; REAL — contraexemplos CAS; OPEN — coeficiente causal]
# A7.b — revisão dos sinais do parecer DeepSeek
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T00:58:19.280623+00:00.
Resposta jobb6d4bbc6-7bd5-4f73-ae34-4f5738376b06, execução122380b3-f573-4d60-95a1-7dfde9a12bf1, lida integralmente.

**1. O bracket é ímpar.** Para paridades de Grassmann epsilon,

    (F,G)=-(-1)^((epsilon_F+1)(epsilon_G+1))(G,F).

O expoente epsilon_F epsilon_G do parecer é o de um bracket PAR, portanto
incompatível com a definição canônica impressa. Em particular, uma ação par
pode ter (S,S) não nulo. O CAS implementa derivadas esquerda/direita numa
álgebra exterior, sem redefinir a convenção para salvar a resposta.

**2. Jacobi usa a ação inteira.** A identidade é (S,(S,S))=0 para S par.
Não vale (S0,(S,S))=0 para qualquer S. Contraexemplo exato: x par, theta,c,d
ímpares, somente (x,theta)=1; S=theta(xc+d), S0=x. Então

    (S0,S0)=0, (S,S)=2theta c d,
    (S,(S,S))=0, (S0,(S,S))=2c d≠0.

Pode-se atribuir gh(x)=0,gh(theta)=-1,gh(c)=gh(d)=1, conservando gh(S)=0.
É contraexemplo algébrico à frase universal, não uma ação física alternativa.

**3. O sinal do antighost não foi reproduzido.** Na fórmula de bracket
impressa pelo provedor, com (barc,barc^ddagger)=1 e s=(S,·), o termo
-barc^ddagger b gera +b. Não gera -b. A fonte069 especifica o bracket
compatível com suas convenções; o parecer não pode simultaneamente adotar
uma fórmula incompatível e anunciar compatibilidade. É necessário ajustar
a convenção de pares/antifields, sem alterar silenciosamente a ação fonte.
Mudar apenas uma declaração separada de s, mantendo S e bracket intactos,
NÃO muda (S,S). O controle correto detecta desacordo entre s e (S,·), não
um valor novo da equação mestra calculada com entradas idênticas.

**4. Wess–Zumino corrigida, com seu alcance.** Seja S_cl a ação BV CLÁSSICA
COMPLETA (incluindo interação) que satisfaz CME no domínio considerado.
Se Gamma=S_cl+hbar Gamma1+... e a quebra do funcional de Slavnov começa
em hbar, Jacobi expandida nessa ordem dá (S_cl,A1)=0, após conservar os
contatos requeridos pela Ward. Para a formulação causal, usa-se a Ward e
nilpotência com as hipóteses dos Teoremas3/6/7 de Fröb já consultados;
essa expressão simplificada não elimina os contatos da QME.

Não substituir S_cl por sua parte LIVRE S0 em todas as valências. Se
s=s0+s1+... e a=Σa_E, a equação na valência E contém Σ_j s_j a_(E-j).
Somente no primeiro grau adequado a condição pode reduzir-se a s0a_E=0.
Se o cutoff produz um defeito clássico, incluí-lo no complexo estendido
ou declarar o recorte chi=1; não presumir CME global por omissão de dchi.

Adotando a graduação TOTAL em que s d_H+d_H s=0, a consistência local é

    s a_4^1+d_H b_3^2=0.

Índice superior é ghost; inferior é grau de forma. Para Gamma→Gamma+hbar B,
com densidade B_4^0, o representante muda por

    a' = a+s B_4^0+d_H eta_3^1,   b'=b+s eta_3^1.

Esses sinais preservam WZ pela anticomutação indicada. Se a=s B+d eta,
a remoção usa a MUDANÇA com sinais opostos. Na convenção de coeficientes
onde s comuta com d, a descida muda de sinais; não misturar as duas tabelas.
Com cutoff, integral chi d eta = -integral dchi wedge eta para suporte
compacto. A contribuição de borda deve ser mantida.

WZ é linear: (a,b) e (-a,-b) passam juntos. Não detecta sozinho o sinal de
um coeficiente físico. Já a não exatidão de um cociclo DADO é questão de
cohomologia e pode ser provada sem grafos; os grafos/prescrição determinam
qual cociclo efetivamente ocorre. A separação anterior do parecer confundia
essas duas tarefas. Os limites clássicos de valência também não autorizam
truncar antes das contrações, conforme a medida quantum_filtration já entregue.

CAS: 583 identidades, incluindo brackets canônicos, antissimetria
e Jacobi em uma base finita, e3controles negativos; rc0,CPU0.09375s.
Os contraexemplos são exatos. A validade geral de Jacobi é a identidade
algébrica padrão, não inferência por amostragem desses testes. Nenhum
coeficiente quântico foi fabricado; os erros do parecer não invalidam por
si a construção da fonte. Kernel, originais e gate intactos.

Uso informado:232032entrada+26790saída=258822tokens,225280cache;
custo estimadoUS$0.03552528. Recuperar/revisar não fez nova chamada remota.
