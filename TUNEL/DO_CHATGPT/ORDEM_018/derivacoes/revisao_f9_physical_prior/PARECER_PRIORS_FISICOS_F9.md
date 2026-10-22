# Revisão independente — priors físicos condicionais F9

**[REAL — revisão estática] Nenhum bloqueador material identificado no pacote df482198-56c4-4169-ae5e-3908f5d12f2c dentro do escopo declarado.** A derivação e o código preservam os priors e as normalizações dos três parâmetros extras. O pacote pode seguir à decisão concreta de integração de engenharia de ROOT. Este parecer não executa nem autoriza o candidato, não libera observados e não atribui precisão certificada.

A entrega569 foi consultada antes do exame; início registrado na seq.571. O manifesto da origem foi preservado como cópia de bytes e novamente conferido no fechamento. Contagens e hashes efetivamente lidos estão em RECIBO_REVISAO_ESTATICA.json.

## Correspondência algébrica

[DERIVED — condicional ao mesmo suporte/C/X/medida] O backend existente fornece R=(I−QQᵀ)W. Para μ(x)=μ_ref+v(x−x_ref), r=R(y−μ_ref), w=Rv, A=wᵀw e B=rᵀw, a variação da log-likelihood é B(x−x_ref)−A(x−x_ref)²/2. O candidato obtém r e w com residualize do backend pinado, sem montar outra pseudoinversa, SVD ou matriz por blocos. Assim, as covariâncias cruzadas e a integração das 63 nuisances permanecem no contexto comum. A normalização é obtida por log_integral, não descartada.

**H3.** A direção é v₃=(I_law/ln10)a_h, com a_h já transformado. O intervalo continua β∈[−0,05;0,05], densidade 10. O código passa k=0 e c=−ln(0,10) à janela analítica. Não duplica a conversão por cinco, não troca o prior por gaussiano e não trunca a caixa em torno de um ajuste.

**H4.** Com λ=ln10/5 e δ=−ln(1+s)/λ, s=exp(−λδ)−1 e |ds/dδ|=λ exp(−λδ). A transformação é decrescente: δ_l corresponde a s=+0,15 e δ_u a s=−0,15. O prior é λ exp(−λδ)/0,30; sua massa é [(1+0,15)−(1−0,15)]/0,30=1. A implementação usa v₄=c_C, k=−λ e c=ln(λ/0,30). O termo exponencial depende da coordenada absoluta δ, não apenas do deslocamento em relação à referência; o fator k·peak na soma final mantém essa diferença. Nenhum fator de Jacobiano ou de largura foi perdido.

Para H3/H4, o máximo restrito do **integrando com prior** é x_p=x_ref+clip((B+k)/A,[l−x_ref,u−x_ref]). A comparação com A(l−x_ref), A(u−x_ref) ocorre antes da divisão; o código avalia a log-likelihood no ponto pela classe existente. Com h=B+k−A(x_p−x_ref), retorna log L(x_p)+kx_p+c+log∫exp(hz−Az²/2)dz sobre [l−x_p,u−x_p]. Isso é a mesma integral deslocada e ancorada, sem a sequência float instável exp(B²/2A) vezes subtração de CDFs ordinárias.

A fórmula documental do mínimo da likelihood permanece separada: usa B/A, não (B−λ)/A. O pacote não implementa nem executa um novo ajuste global por causa desse adendo.

**H5.** Mantido θ, somente as 13 componentes BAO variam como D_j(θ)/r_d. Em q=1/r_d, a direção tem D_j nos índices3:16 e zero nas demais 270 componentes; os extremos são 1/160 e 1/130. A densidade é 1/(30q²), cuja integral vale1. A reconstrução da direção como média BAO pinada vezes r_d,ref é algébrica; seu arredondamento float permanece explicitamente não certificado.

Na mudança q=q_l+Δq·u, o fator de escala é L(q_p)Δq/(30q_l²), enquanto o callback é [L(q)/L(q_p)](q_l/q)². O produto recupera exatamente L(q)dq/(30q²). q_p maximiza a likelihood, não necessariamente o integrando completo; isso basta para a majorante matemática f_scaled≤1, pois q_l/q≤1. Nenhum prior uniforme em q foi substituído pelo prior uniforme original em r_d. Os endpoints do callback são tratados diretamente para evitar deriva da soma na fronteira.

## Degenerescência, suporte e falhas

O construtor _Curve passa a direção por residualize e confere o suporte afim dos dois endpoints. Na geometria exata, afinidade e convexidade transportam essas condições para todo o segmento; os testes usados aqui são os float/tolerâncias existentes, sem certificado exato ou reparo por jitter. A condição de posto63 das nuisances não é relaxada.

A=0 é aceito como curva plana somente quando todos os componentes de w são zero no cálculo. A=0 com componente projetado não nulo gera CURVATURE_UNDERFLOW; A pequeno positivo continua no ramo geral. Se w=0, B=0 e a integral contra qualquer um dos três priors próprios normalizados devolve L_ref. Não se introduz uma penalidade de largura ou uma 64ª nuisance plana. O rótulo FLAT_EXTRA_IN_PROJECTED_FLOAT_GEOMETRY não afirma degenerescência científica exata.

O único retorno −inf decorre do complemento do suporte afim comum já diagnosticado pelo consumidor. Não é substituto de falha de cálculo. A validade dessa propagação continua condicionada à geometria admitida; os testes float próximos do limiar não viram prova de nulidade exata. O próprio contrato conserva essa ressalva.

A janela finita e positiva deve devolver log finito; NaN/−inf é recusado. H5 exige área estritamente positiva. Underflow de nós é contado e rotulado, sem inferir massa exatamente zero ou limite do resto. Qualquer erro do callback fica retido e invalida o retorno, mesmo se o serviço de quadratura tentar capturá-lo. A contagem retornada deve coincidir com as chamadas efetivas, que têm teto imposto no wrapper. Não há retry/fallback, corte/renormalização de região ou omissão de modelo; a coleção só retorna depois de completar os cinco ramos.

## API, dependências e consumidor a987

O código importa apenas math. NumPy, PreparedJoint e os serviços são recebidos do chamador. O uso de campos privados do consumidor é declarado como acoplamento ao pin específico, não como uma interface privada universal. A chamada inicial evaluate_five reaproveita a conferência da família, 283/63, estrutura, suporte, prefator e identidade. O pacote de fundo adicional tem o mesmo hash e identidade da montagem; θ é comparado com o fundo e com todos os modelos. A redução dos extras não chama CAMB, assemble_five ou outro solver.

O módulo exige os priors e coordenadas exatos do montador. H1/H2 permanecem pontuais; H3/H4/H5 integram apenas seu parâmetro extra. A densidade base50/3 em θ não é aplicada nem integrada. As saídas são integrais **condicionais**; não são evidências em θ, logZ ou Bayes factors.

As funções log_exp_quad_interval e positive_quad_1d são dependências explícitas ainda não implementadas/qualificadas por esta entrega. O contrato exige alvo, ID/pin, método, contagem, convergência e erro local estimado ou UNASSESSED. O código retém esse recibo sem transformar uma meta passada como argumento em garantia alcançada. A janela tem seu número declarado de avaliações conferido após o retorno; o respeito interno ao serviço e sua identidade carregada pertencem à qualificação externa do chamador. No callback de H5, a contagem é efetivamente observada pelo adaptador.

Esse limite de confiança já está escrito: nomes, flags e hashes declarados não autenticam objetos Python arbitrários nem liberam dados. Uma futura integração terá de fornecer os serviços concretos previstos pela própria API; não proponho outra campanha, instalação ou certificado uniforme como condição artificial para estimativas ENGINEERING_ONLY. Erros locais dos serviços não abrangem erros do backend, de A/B, da reconstrução BAO ou do fundo. A saída diz isso expressamente.

κdη, a medida de dados transformada e a normalização do consumidor permanecem comuns. MM segue CONDITIONAL_UNRATIFIED, e UNBOUNDED_THEORY_ERROR é preservado. Nenhuma covariância MM ou lei condicional baseada nos valores medidos é ratificada por esta implementação.

## Alternativas e alcance do aceite

Foram confrontadas as alternativas previamente documentadas: janela analítica estável em H3/H4 com quadratura positiva1D em H5, escolhida; e quadratura direta nas coordenadas originais β/s/r_d, que preservaria os priors mas demandaria mais avaliações condicionais. A segunda não é fallback automático autorizado por uma falha da primeira. A subtração ingênua de duas CDFs float permanece rejeitada como solução geral de caudas.

[REAL — atividade do revisor] Somente leitura, AST, pins e comparação documental/algébrica. Zero importações candidatas, NumPy/SciPy/backend, controles, solver, WSL, observados ou rede. Não foram calculados A/B, integrais, caudas, mínimos ou previsões; nenhuma AUTH/CLAIM foi criada. Fontes, pacotes consumidos, memórias compartilhadas e ledger não foram alterados. O resultado teórico c435 pertence ao trabalho separado de ROOT e não foi usado como likelihood nesta revisão.
