# Revisão independente I05 — perfis afins condicionais F9

**Nenhum bloqueador material identificado no pacote selado examinado.** [REAL — revisão estática] A derivação e a implementação preservam o alvo de perfil da likelihood nos extras H3/H4/H5, as dependências a987/df482 e os limites declarados de estimativa de engenharia. A conclusão não executa, autoriza ou qualifica numericamente o candidato.

Pedido: 4eea0cfb-0a3e-4b38-abcd-37bddbf5bbe3. Mapa consultado antes: 593. Manifesto: 2.752 bytes, SHA256 3f90b6c2c3b68075141350e3427cf3bb31b326f2ac3e08b2e73009ff330a75e2. O recibo ao lado identifica os bytes finais efetivamente lidos.

## Custódia e método

[REAL] O manifesto, os sete membros e dois backups foram conferidos antes da leitura de conteúdo. O snapshot inicial inclui esses nove arquivos e o manifesto. Foram conferidos também o pedido e dez fontes: oito solicitadas e dois backends herdados. Todos permaneceram iguais na conferência final.

O script independente inspect_static.py fez 85 conferências de pins, AST e interfaces, todas satisfeitas, registrando 22 caminhos na evidência. Isso não é PASS de controles numéricos. Foram lidos integralmente módulo, API, derivação, contrato e empacotador, além de _Curve, o caminho de construção das curvas em df482, PreparedJoint.evaluate_five/admissão e os dois backends relevantes. A revisão anterior dos priors físicos foi consultada como evidência documental, não como substituto da leitura do novo adaptador.

Não foram importados/chamados candidatos, NumPy/SciPy, backend, solver ou provedores; não houve WSL, controles, leitura de observados, AUTH/CLAIM, edição do pacote, memórias ou ledger.

## Álgebra e implementação

[DERIVED — condicional ao mesmo C/X, suporte, medida e θ] Com R=(I−QQᵀ)W do backend existente, r=R(y−μ_ref), w=Rv e t=x−x_ref:

q(x)=‖r−wt‖²=‖r‖²−2Bt+At², A=wᵀw, B=rᵀw.

Para A>0, o mínimo no segmento é x_ref+clip(B/A,[l−x_ref,u−x_ref]). O sinal de B e as desigualdades de fronteira descritos na derivação correspondem a _Curve.peak: comparar B a A(l−x_ref) e A(u−x_ref) antes de dividir é compatível com o vértice restrito. O método herdado tem prior_linear=0 como padrão; affine_profile.py:105 chama peak() sem argumento. Não injeta densidade de prior, largura ou Jacobiano na posição do máximo da likelihood.

| Modelo | Correspondência conferida |
|---|---|
| H1/H2 | Mantêm as médias e os logs pontuais fornecidos por evaluate_five; não recebem parâmetro extra. A norma q é avaliada pelo mesmo residualize. |
| H3 | x=β, limites originais [−0,05;0,05], direção (I_law/ln10)a_h já transformada. Não reaplica o fator cinco. β fixo de H1 continua no pacote original, sem literal novo. |
| H4 | x=δ=−5log10(1+s), direção c_C. A transformação é decrescente: o limite inferior de δ corresponde a s=+0,15. O perfil usa B/A; B−λ é próprio da integração contra o prior transformado e não entra neste adaptador. |
| H5 | x=1/rd, intervalo [1/160;1/130]. A direção é reconstruída pela média BAO de referência vezes rd_ref, apenas nos índices3:16. As outras270 componentes permanecem zero na direção, incluindo as três CMB. Não aplica 1/(30x²) nem modifica r_star. |

A norma é recalculada diretamente no ponto por _q_at_mean, usando residualize do backend; não emprega a subtração potencialmente instável ‖r‖²−B²/A. Nenhuma nova pseudoinversa, SVD, fatoração de C/X, busca em θ ou quadratura foi introduzida.

O perfil log_profile_deta é da integral nuisance já fornecida por a987, com seu prefator e logκ comum omitido. Para C/X/suporte fixos, o prefator é constante no extra, de modo que minimizar q seleciona também seu máximo. Esse campo não é apresentado como evidência integrada nos parâmetros físicos nem como mínimo global.

## Suporte, ramo plano e ponto devolvido

[REAL — implementação] _Curve reaproveita as verificações de suporte da direção e dos dois endpoints. Na geometria afim exata, endpoints e direção no suporte comum mantêm o segmento admissível; os testes concretos continuam usando os cutoffs e tolerâncias herdados. O adaptador não os relaxa, não acrescenta jitter, não corta dimensões nem descarta modelos.

A=0 só é admitido pela dependência pinada quando todos os componentes de w calculados são zero. A=0 com componente não nulo é erro de underflow; A positivo pequeno não é redefinido como zero. Nesse ramo, B=0 é exigido. O adaptador usa a referência, registra todo o intervalo como plano na geometria float e preserva o log pontual. O rótulo não demonstra degenerescência ou não identificabilidade física exata.

Na norma do resíduo, um resultado zero com vetor projetado calculado não nulo provoca erro. Não há captura de exceção que transforme falha do backend/domínio/suporte em densidade zero. O único −inf devolvido é o ramo fora do suporte afim comum já diagnosticado pelo consumidor; ali q e parâmetros factíveis ficam indisponíveis. Essa propagação permanece condicional à geometria e às tolerâncias herdadas, sem certificado de nulidade exata na fronteira.

H4 usa expm1 na inversa e log1p na recomposição; liga explicitamente os endpoints físicos e transformados e preserva a referência. H5 usa o recíproco, com endpoints físicos originais. _physical_point recusa não finitos ou pontos fora do domínio, sem clipping silencioso da inversa.

O código distingue affine_candidate de affine_evaluated. Calcula norma e log na coordenada recomposta do parâmetro físico devolvido e registra roundtrip_shift. Assim, não apresenta o candidato de vértice antes do arredondamento como se fosse o ponto físico efetivamente avaliado. Ainda existem erros float de coeficientes, reconstrução BAO, inversão e backend; o próprio pacote os declara sem enclosure.

## Acoplamento, identidade e falhas

[REAL — fonte/AST] O adaptador importa apenas math. Os módulos existentes são injetados; PreparedJoint e _Curve são usados nos seus pins específicos, não como interfaces privadas genéricas de qualquer versão.

As identidades de pedido a9874f79-9d71-48f5-824c-d51d6d819534 e df482198-56c4-4169-ae5e-3908f5d12f2c correspondem às fontes lidas. Os dicionários de pins herdados coincidem: df482 aponta para o mesmo consumidor; a987 aponta para os mesmos backends linear_gaussian e singular_gaussian_v2. MODELS, limites e assinatura também conferem.

Há um ponto de chamada a joint.evaluate_five e três construções p._Curve. A chamada inicial conserva a admissão da família inteira, 283 linhas/63 nuisances, desenho/respostas, transformação e normalização. O fundo deve ter o mesmo hash e identidade da montagem; θ coincide com o fundo e com os cinco modelos e permanece na caixa original. Priors são comparados como metadados, não aplicados. O contexto completo do backend preserva blocos cruzados; nenhuma redução por bloco foi acrescentada.

A referência caller_verification_reference verifica formato, não autenticidade de objetos Python arbitrários. A identificação real dos módulos/contexto carregados e sua preservação são obrigações externas já explícitas. Essa fronteira de confiança não foi promovida a prova por flags.

Não há try/except de fallback ou busca iterativa. Falha aborta a coleção; os cinco modelos só são devolvidos após conclusão do caminho inteiro. Não são criados launcher, autorização, claim ou repetição de unidade consumida. O gravador externo ainda deverá representar −inf com seu estatuto, pois esse valor Python não é número JSON estrito.

## Estatuto e alcance do aceite

[REAL — saídas conferidas] Cada modelo conserva conditional_minimum=UNAVAILABLE e global_theta_minimum=NOT_SEARCHED, com lower/upper/certificate indisponíveis e verified=false. A API não aceita nem implementa verificação de certificados. q_feasible_estimate é um valor calculado num ponto factível do modelo representado; não é U certificado, mínimo global g_i ou limite inferior L.

Permanecem ENGINEERING_ONLY, a certificação UNBOUNDED_THEORY_ERROR herdada e MM CONDITIONAL_UNRATIFIED. Os campos global_minima, relative_evidence, lnB, p, sigma e verdict são None; priors físicos não aplicados e busca global não realizada. A igualdade θ entre os modelos nesta chamada representa uma avaliação condicional comum, não a imposição de um único ótimo para os cinco modelos em uma busca futura.

O pacote fornece a operação delimitada I05. Não demonstra precisão, desempenho, cobertura global ou adequação física; tampouco tais certificados são artificialmente exigidos para reconhecer sua utilidade como preparação de estimativas de engenharia. A alternativa de otimizar diretamente todos os extras/θ não é fallback autorizado ou implementado.

**Conclusão restrita:** o pacote está apto à decisão de integração da ROOT dentro desse alcance. Nenhuma correção material foi identificada e nenhuma nova campanha é proposta. Qualquer execução futura precisa de sua unidade e evidência próprias; este parecer não a realiza nem a autoriza.
