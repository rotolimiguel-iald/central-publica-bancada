[DERIVED — identidade graduada de jatos módulo divergência; OPEN — incorporação BV gauge-fixada completa]
# A7.b — candidata quadrática em antifields

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T23:50:59.983542+00:00.

Se u_A é ímpar, gh(u_A)=-1, c^μ é ímpar, gh(c)=1, E_A é par e
δu_A=E_A, δc=δE=0, tome B_AB constante e simétrica e

    Ψ_B = (1/2) u_A B_AB c^μ ∂_μ u_B,
    J^μ = u_A B_AB c^μ E_B.

A regra de Leibniz GRADUADA dá a identidade local

    δΨ_B+(1/2)∂_μ J^μ
       = u_A B_AB[c^μ∂_μ E_B+(1/2)(∂_μ c^μ)E_B].

A prova escrita é trocar E_A c ∂u_B por -∂u_A c E_B usando simetria
de B e paridades; a derivada de J fornece os dois termos restantes.
O CAS realizou essa operação numa álgebra exterior com dois índices de
fibra genéricos e B00,B01,B11 independentes. A prova por índices vale
para qualquer número de fibras e soma de μ. Conferiu δ²Ψ=0, gh/paridade,
divergência nãozero antes do quociente e três negativos: sinal da divergência,
omissão dos termos cruzados de fibra e B antissimétrica.

Para ghost constante, o membro direito é u B(c·∂)E. A escolha

    B(A)=-A/6-I trA/12

reproduz a forma TRANSVERSAL do resíduo medida na outra entrega, na
normalização ali especificada. É uma candidata local, não a declaração
de que o contratermo completo da ação foi construído.

Cuidados que ficam como equações a resolver: a069 fixa o diferencial
dos antifields pela ação gauge-fixada; δh* inclui Hh+C*b e sua convenção
de sinal, não só E(h). H contém o fator1/(4κ). É necessário encaixar
normalização, sinal, b e outros antifields no gerador completo. Fourier
também repõe i. Para cutoff χ, a integração por partes conserva um termo
proporcional a ∂χ: não o eliminamos. Nada aqui calcula A(e^V) finita,
componentes curvas ou o vértice h*hc inteiro.

Script antifield_quadratic_primitive_check.py: rc0,5checks+3negativos,
CPU0.046875s.
O termo aparece como resposta ao contraexemplo, não como escolha de
coeficientes para forçar QME. Q2finitaOPEN; nenhum kernel/gate alterado.
