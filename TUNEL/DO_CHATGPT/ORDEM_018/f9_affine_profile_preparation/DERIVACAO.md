# Perfis condicionais dos extras F9

Pedido 4eea0cfb-0a3e-4b38-abcd-37bddbf5bbe3; dependência I05. [DERIVED — condicional ao suporte, desenho, covariância e modelo admitidos] [REAL — preparação estática, sem avaliação numérica].

## Objeto e duas alternativas

Alternativa A, escolhida: eliminar o extra afim por seu vértice restrito, usando a geometria R já construída pelo backend. Em uma futura busca em θ, isso reduz o problema de quatro para três coordenadas sem mudar o domínio físico. A busca em θ NÃO é implementada aqui.

Alternativa B: otimização direta simultânea nas coordenadas físicas originais β, s ou r_d e θ. É a mesma likelihood/domínio se implementada corretamente, mas acrescenta uma busca desnecessária no extra e problemas de convergência/fronteira. Não é fallback deste pacote.

Reaproveitam-se PreparedJoint.evaluate_five do consumidor a987 e _Curve do df482. O df482 constrói curvas dentro de integrate_at_fixed_theta e não possui API para exportá-las. Por isso este adaptador repete somente a montagem dos três argumentos afins, com as mesmas fontes verificadas. Ele não chama a integral dos priors para obter um perfil, não modifica o pacote congelado e não copia residualize, SVD, inversa, suporte ou normalização gaussiana.

## Eliminação algébrica

Fixe θ, C, X, o suporte afim e a medida. O backend existente fornece R=(I−QQᵀ)W. Para μ(x)=μ_ref+v(x−x_ref), defina r=R(y−μ_ref), w=Rv, A=wᵀw, B=rᵀw. Escrevendo t=x−x_ref:

q(x)=‖r−wt‖²=‖r‖²−2Bt+At²; log L_η(x)=K−q(x)/2.

K é constante no extra e vem do mesmo backend. Se A>0, q'(x)=2[A(x−x_ref)−B], q''=2A>0. Portanto, no intervalo fechado [l,u]:

x*=x_ref+clip(B/A,[l−x_ref,u−x_ref]).

Se B≤A(l−x_ref), a derivada é não negativa em todo o segmento e l minimiza. Se B≥A(u−x_ref), u minimiza. No restante, o vértice interior minimiza. O _Curve.peak existente realiza essas comparações antes da divisão para evitar overflow desnecessário quando o vértice está fora do domínio. É chamado SEM deslocamento de prior. A aritmética float desse helper continua sujeita a arredondamentos/underflow de coeficientes e produtos; não vira certificado por expressar uma fórmula analítica.

Se A=0 em aritmética real, w=0 e B=0; todo o intervalo minimiza. No código, _Curve admite esse ramo apenas quando todos os componentes projetados são exatamente zero no float calculado. A=0 com componente não nulo é falha de underflow; A pequeno positivo não é redefinido como zero. O representante escolhido no ramo plano é a referência já fornecida, com o intervalo inteiro registrado como empate na geometria calculada. Isso não prova não identificabilidade física exata.

O perfil é avaliado pela norma do resíduo projetado no ponto factível, não por subtração ‖r‖²−B²/A. O mesmo residualize fornece a projeção; o log da integral nuisance é preservado de evaluate_five nos pontos sem extra/plano e de _Curve.log_likelihood nos pontos selecionados. Uma norma zero de vetor calculado não nulo gera falha explícita, sem fabricar ajuste perfeito.

## H3, H4 e H5

H3: x=β∈[−0,05;0,05], v=(I_law/ln10)a_h. a_h já está na unidade transformada. Não aplicar novamente a escala cinco. O β fixo de H1 continua no pacote do montador, sem literal novo ou reajuste nesta implementação.

H4: x=δ=−5log10(1+s), s∈[−0,15;0,15], v=c_C. A transformação é bijetiva e decrescente; δ_l corresponde a s=+0,15, δ_u a s=−0,15. Logo minimizar sobre s equivale a minimizar sobre esse intervalo de δ. O máximo da likelihood usa B/A. **B−λ, λ=ln10/5, só aparece ao integrar a likelihood contra o prior transformado; não aparece neste perfil.** Maximizar uma densidade posterior após mudança de coordenadas seria outro alvo.

H5: x=1/r_d∈[1/160;1/130], com v_j=D_j(θ) nas 13 linhas BAO e zero nas demais 270. O vetor é reconstruído como média BAO de referência vezes r_d,ref, exatamente como no df482. r_d=1/x é bijetivo e decrescente, logo o mínimo de likelihood é transportado sem fator de Jacobiano. O fator 1/(30x²) é da integral do prior, não do perfil. Não confundir x=1/r_d deste código com a coordenada documental alternativa r_d/r_d,CAMB: o domínio físico é o mesmo.

H1/H2 não têm extra. Mantêm a média e o log L_η fornecidos pelo consumidor, com q avaliado pela mesma norma projetada. Não se cria um ajuste extra para esses modelos.

## Ponto físico efetivamente avaliado

No float, inverter uma transformação e voltar pode deslocar a coordenada por arredondamento. O candidato separa affine_candidate (vértice escolhido) de affine_evaluated (coordenada obtida do parâmetro físico devolvido), registrando roundtrip_shift. A norma e a log-likelihood usam a segunda. Assim, o ponto apresentado como factível é o ponto efetivamente lido na curva.

Em H4, expm1 evita cancelamento desnecessário próximo de s=0. Endpoints transformados são ligados diretamente aos endpoints físicos opostos; a referência preserva sua representação original. Em H5, o recíproco devolve r_d e é reaplicado para obter x efetivo. Pontos fora dos domínios ou não finitos são falhas, sem clipping silencioso da inversa. Isso mantém um testemunho factível de engenharia; não constitui uma cota superior certificada de q sem erro de avaliação controlado.

## Suporte, normalização e certificados

As 283 linhas, as 63 nuisances, C inteira e blocos cruzados, a origem afim, T e κdη pertencem ao PreparedJoint fixo. O pacote inteiro passa por evaluate_five antes da preparação das curvas. _Curve confere a direção e os endpoints no suporte comum, com as tolerâncias existentes. Uma inconsistência de suporte durante a avaliação aborta a coleção, não remove o rival.

O complemento legítimo do suporte afim tem log L=−inf, conforme o consumidor. Nesse ramo, o perfil não fornece q finito nem um minimizador factível, e mantém o diagnóstico. Nenhuma exceção vira densidade zero. A propagação desse diagnóstico continua condicional à geometria/tolerâncias admitidas; não é rejeição física certificada.

O prior físico não é aplicado; suas coordenadas/limites são conferidos como metadados. A densidade base 50/3 tampouco é aplicada ou integrada. O prefator K e a omissão explícita de logκ permanecem na saída. Nenhuma evidência, razão de Bayes ou sigma é produzida.

O módulo só calcula estimativas condicionais em um θ. q_feasible_estimate não é L global, U certificado, g_i ou mínimo em toda a caixa de θ. Cada modelo mantém certificados condicionais UNAVAILABLE e mínimo global NOT_SEARCHED, com números None. O resultado não aceita uma flag certificadora do chamador: certificados externos precisam de seu próprio verificador e vínculo de alvo/cenário/dados/θ/domínio/erro conforme INTERFACE_CERTIFICADOS_F9.json. Não se preenche L=0 como certificado automático sem essa admissão, embora q≥0 seja a identidade algébrica pertinente.

## Estatuto da entrega

Somente leitura de fontes, derivação, AST e hashes. Nenhum candidato, backend, NumPy/SciPy foi importado; nenhuma norma, coeficiente, perfil, controle ou observação foi calculado. Não há solver, WSL, provedor, instalação, launcher, AUTH/CLAIM ou nova campanha. ENGINEERING_ONLY, UNBOUNDED_THEORY_ERROR e MM CONDITIONAL_UNRATIFIED permanecem. Qualificação numérica e revisão independente não são simuladas por esta preparação.
