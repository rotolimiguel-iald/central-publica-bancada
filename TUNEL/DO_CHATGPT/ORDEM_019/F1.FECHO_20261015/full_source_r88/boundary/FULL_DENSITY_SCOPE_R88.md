# R88 — variação local completa e corolário integral

[REAL — sandbox] Primeira tentativa: EXIT 0 em 74.155908 s, cinco teoremas e três definições, apenas propext/Classical.choice/Quot.sound, zero marcadores incompletos e zero avisos. Fontes verdes anteriores importadas por bytes, sem recompilação; nenhuma execução após o verde.

O fator geral F(t,x) entra na R83 com c0=0 e xi=1. A densidade é v(g+t h) F(t,x) R(g+t h). Sua derivada é v/2 tr(hq) F₀ R + v dF R − v F₀ Σ_ij HⁱʲRic_ij + ∂_a(vBᵃ) + v[H:Hess(F₀)−tr(qh)q:Hess(F₀)], onde q=g⁻¹, H=q h q, W=divH−grad tr(qh) e B=F₀W−H dF₀+tr(qh)grad(F₀). dF é a derivada do parâmetro t; as parciais espaciais de F₀ são objetos distintos. Todas as parcelas δv, δq, δF e δRic estão presentes, incluindo RδF.

A identificação do componente de Ricci usa unicidade da derivada entre metric_ricci_first_variation e a pedra Hessian; não assume a fórmula de Euler–Lagrange. O teorema local compõe essa igualdade com o produto HasDerivAt já provado na R83, sem reconstruir bibliotecas.

O corolário integral aplica literalmente integrated_gravitational_first_variation da R84 e troca seu integrando derivado pela igualdade quase em toda parte já demonstrada. Exige suporte da medida na região aberta, regularidade/simetria/invertibilidade do campo, derivadas temporal e espaciais do fator, regularidade local explícita de C, mensurabilidade, integrabilidade e majorante Lipschitz uniforme integrável. Conclui integrabilidade da derivada completa e HasDerivAt do integral da densidade. A divergência permanece dentro do integrando; não se presume fluxo zero nem se descarta a fronteira.

[OPEN] Não constrói F a partir de Ψ/P nem o conjunto admissível de variações; não impõe ou deriva estacionariedade, não acrescenta fonte física completa e não conclui H3/Einstein para a TGL inteira. Fixar a ação e a fonte da mesma construção permanece tarefa material própria. Nenhuma memória, produção, kernel original ou gate foi alterado.

Declarações: full_local_density_first_variation na linha 90; full_integrated_density_first_variation na linha 105. Pinos/linhas/logs reais em FULL_DENSITY_DELIVERY_R88.json.
