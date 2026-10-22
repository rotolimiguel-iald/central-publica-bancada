[DERIVED — quociente clássico por ideal diferencial; REAL — CAS e revisão MiMo; OPEN — prescrição causal]
# A7.b — sigma constante: restrição clássica não é integração quântica
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T00:54:15.484764+00:00.

Parecer MiMo job187b509f-0a81-41e3-9f6a-835c870b525c, execução563d3687-6a95-4c39-a22c-f9634343ff8e, lido
integralmente. A distinção entre projetar o setor sigma e integrar suas flutuações
é correta. A alegação adicional de que s agindo em h recebe EOM de xi é incorreta:
sg=Lie_c g; as equações de movimento entram em s dos ANTIFIELDS.

**Prova escrita no modelo fonte, antes de qualquer contração quântica.**
Use coordenadas de alvo xi próximas do valor constante phi0. Seja I o ideal
diferencial gerado por TODOS os jatos de xi e xi^ddagger. No sigma modelo sem
potencial/fonte linear, S_sigma é quadrático nas derivadas de xi, com métrica
do alvo suave. Assim E_xi pertence a I, e o tensor de energia também (na
verdade começa em grau dois em xi e seus jatos). Temos

    s xi=c^mu partial_mu xi ∈ I,
    s xi^ddagger=±E_xi + termos lineares em xi^ddagger e seus jatos ∈ I.

O sinal depende da convenção esquerda/direita do antibracket, irrelevante
para a pertença ao ideal. Como s comuta com o prolongamento por jatos e é
derivação, sI⊂I. Logo ele induz um diferencial no quociente clássico, e seu
quadrado é zero quando o s completo da fonte o é. Na restrição, a ação se
reduz a Einstein–Hilbert mais os acoplamentos BV métricos/ghosts; o termo
sigma na transformação do antifield métrico desaparece e o termo
xi^ddagger Lie_c xi no antifield ghost desaparece. O par não mínimo pode
ser mantido com a gauge de De Donder exclusivamente métrica aqui usada.

Não apagamos os antifields dos campos RETIDOS. O aviso da087, l.11, refere-se
justamente a esses antifields. A alegada tensão interna X4 do parecer não
decorre daquele aviso. Trata-se de QUOCIENTE DE COMPLEXOS, não de afirmar
que I é ideal de Poisson-BV: (xi,xi^ddagger)=1 impede esta última afirmação.
O antibracket do setor retido é definido separadamente sobre seus pares.

**Controle local e alcance.** O CAS usa a carta hemisférica de S3,
G_ij=delta_ij+xi_i xi_j/(1-|xi|²), dimensão espaço-temporal4 e densidade
métrica inversa A^mu nu arbitrária. Deriva Euler a partir da lagrangiana,
confere E_xi(0)=0, T(0)=0 e as três linearizações

    E_i,lin=-c_m[A^mu nu partial_mu partial_nu xi_i
                   +(partial_mu A^mu nu)partial_nu xi_i].

São19checks+2negativos, rc0, CPU9.9375s. Uma fonte J xi
destrói a restrição; apagar SOMENTE os antifields sigma, mantendo xi livre,
também não dá ideal estável. A prova de sI⊂I é o argumento escrito acima,
não uma conclusão universal produzida por esses testes finitos.

As três Hessianas de flutuação NÃO são zero. Portanto fixar o valor de
fundo não apaga os propagadores. Em produtos quânticos, xi(x)⋆xi(y) contém
ħG(x,y): não há transporte automático desse quociente clássico. Um
determinante não trivial também não implica quebra Ward; seria preciso
calcular sua variação na prescrição escolhida.

**Demais correções da revisão.** W5/X6 confundem o H4 do CE quadrático com
o H4 completo: a087 diz explicitamente que NÃO o exaure. R4/W6 transformam
a observação sobre contratermos de0/1/2pernas da072 numa cota universal;
esta não é estabelecida ali, e a filtração quântica já entregue permite
valências maiores. K/Lambda e os operadores da restrição estão em
model_inputs/DERIVACAO_OPERADORES.md; o parecer só recebeu excertos anteriores.
Não declarar novamente inexistente o que a bancada já construiu. O fundo
069 sigma=id continua distinto do espaço-forma087 sigma constante.

Nada aqui fixa a normalização causal completa, integra sigma, move gate ou
modifica um.py. Recuperação da resposta fez zero chamadas novas a provedores.
Uso informado:331360entrada+34313saída=365673tokens; custo estimadoUS$0.17399391.
