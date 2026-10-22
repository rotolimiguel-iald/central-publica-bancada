# R76 — alternativa de fotocontagem de janela curta (ao lado)

**[DERIVED — analítica, não executada, NOT_LEAN]** r69_locality_bridge, 18/10/2026, a pedido da coordenação. Esta nota não acrescenta testes nem muda as features da campanha R76. O critério de não identificabilidade da nota principal refere-se à lista de leituras escolhida, não a todos os instrumentos possíveis.

## 1. Instrumento nomeado e identidade exata no modelo finito

Reaproveite as portas de vácuo independentes `L_j=√κ_j a_j` do contrato R64, agora com detecção ideal de fótons, sem oscilador local na porta contada e sem campo coerente incidente nessa porta. O banho coerente que implementa a bomba OH da R66 é outro canal. Fotocontagem é um instrumento alternativo à homodinagem; não é declarada já implementada no consumidor R76.

No corte finito, escreva `J_j(X)=L_j X L_j†`, `ρ(t)=exp(tG)ρ₀`. A hierarquia de primeiro momento da contagem é `dot u=G u+J_jρ`, `u(0)=0`. Ela se obtém derivando em z=0 o gerador inclinado `G_z=G+(exp z−1)J_j`. Como Tr(GX)=0,

`m_j(T)=Tr u(T)=∫₀ᵀ Tr(ρ(t)L_j†L_j)dt=κ_j∫₀ᵀ<n_j(t)>dt`.

Nos cortes totais R66, `a_j^m=P_m a_j P_m` satisfaz `(a_j^m)†a_j^m=n_j|P_m`: o abaixador não precisa de estado acima do corte. Assim a igualdade acima usa precisamente o número comprimido, sem trocar pela compressão do quadrado de uma quadratura. κ_j>0 e a eficiência/ganho da contagem precisam ser calibrados independentemente; se κ_j=0, esta inversão não existe.

## 2. Erro de janela, provado sem tomografia

No mesmo modelo finito e gerador independente do tempo, a dual é unital positiva e contrativa em norma de operador sobre os hermitianos. Logo

`|<n_j(t)>−<n_j(0)>| = |∫₀ᵗ Tr[ρ(s)G†(n_j)]ds| ≤ t ||G†(n_j)||op`.

Integrando uma vez mais,

`|m_j(T)/(κ_j T)−<n_j(0)>| ≤ (T/2)||G†(n_j)||op`.

Portanto o limite T→0 identifica a ocupação inicial pela derivada média da contagem. Para janela finita e erro simultâneo δm_j na média estimada, somam-se `δm_j/(κ_j T)` e o erro de janela; erros de κ, eficiência e modelo entram separadamente, por limites certificados. Diminuir T reduz o viés de evolução mas amplia o erro dividido por T; o limite analítico não garante sensibilidade estatística finita. A soma dos dois portos fornece uma testemunha de N_b e pode alimentar a desigualdade `p₀≥1−<N_b>` da R72, quando seu limite superior é informativo. Ela não mede automaticamente a ocupação OH.

## 3. Alcance bosônico e física

A identidade integral também vale em uma realização de contagem ilimitada que satisfaça as hipóteses de domínio e integrabilidade correspondentes. Esta nota NÃO constrói essa realização nem a deduz da mera existência dos momentos homódinos R75. No Fock inteiro, `||G†n_j||op` pode ser infinito; é necessária cota uniforme de expectativas `|Trρ(s)G†n_j|`, ou estimativa por momentos, para obter um erro útil de janela. Não se transfere o bound finito mantendo sua constante sem justificativa.

A calibração física dos portos, do relógio e da eficiência permanece requisito. O argumento só mostra que uma lista insuficiente de filtros homódinos não prova impossibilidade de outras leituras. Nenhum Γ, β, energia em joules ou parâmetro do aparelho foi estimado aqui; nenhum estado observado foi aberto.
