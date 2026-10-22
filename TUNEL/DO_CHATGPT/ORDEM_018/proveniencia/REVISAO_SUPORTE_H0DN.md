# Revisão independente — suporte singular e adendo H0DN

[REAL — controles locais sintéticos] **Dois achados P2 de validação da API inicial, resolvidos na nova versão V2 após revisão independente do delta. Nenhum achado bloqueante permanece no recorte sintético revisto.** A fórmula de densidade restrita ao suporte, a convolução gaussiana própria e o sinal/Jacobiano do adendo H0DN conferiram. O código do autor permaneceu read-only nesta revisão. Nenhum dado real, ajuste, execução upstream ou aceitação de V1. A versão inicial e seus achados permanecem como história; a resolução da V2 está registrada ao final, sem apagar resultados anteriores.

## Achados acionáveis na versão inicial

**H0DN-01 — P2: rejeitar tolerâncias não finitas.** Em `singular_gaussian.py:25`, testar apenas `min(...) < 0` não exclui NaN ou infinito. Na cópia byte a byte auditada, C=[[1,1],[1,1]], r=[2,0], `support_tolerance=inf` produz `support_ok=true` e logdensidade finita −1,7655121234846454, embora o resíduo nulo tenha norma sqrt(2). `absolute_cutoff=NaN` ou infinito e `relative_cutoff=inf` também são aceitos: C perde seu posto positivo e vira rank0 no ponto zero. Ação: exigir três escalares finitos e não negativos antes da simetrização/decomposição, preservando os parâmetros congelados válidos. Esses exemplos não afetam retroativamente os18 controles que usaram os defaults finitos.

**H0DN-02 — P2: impedir broadcasting silencioso na marginalização.** Em `gaussian_prior_marginal:69–74`, y=[1], mu=[0,0], C=I2, A=I2, m=[0,0], S=I2 retornam rank2 e logdensidade −3,0310242469692907. Uma única componente de y foi replicada implicitamente, fabricando um resíduo de duas componentes. `SupportGaussian.evaluate` valida só o resultado já expandido e não detecta o erro. Ação: validar explicitamente y/mu:(n,), C:(n,n), A:(n,p), m:(p,), S:(p,p), além de finitude, antes de somas/produtos. O helper não deve transformar um contrato dimensional inválido em evidência finita.

A auditoria preserva os exemplos e a cópia original `covariance_support_under_review.py`, SHA256 `9e5956667b109750c231e5b58ce5776be993a330ceb55bdc53e3010c2e5f5163`. Não alterou nem executou `verify_support.py`; os18 controles anteriores foram conferidos por recibo/código/pins, sem repetição do driver.

## Protocolo e controles independentes

`REVISAO_SUPORTE_H0DN_PROTOCOL.json` foi gravado antes dos controles, seguido de `REVISAO_SUPORTE_H0DN_FREEZE.json` com hashes de protocolo, script e cópia. Foram30 conferências:24 passaram inicialmente,5 rejeições esperadas reproduziram os dois defeitos acima e1 diferença finita do próprio revisor excedeu a tolerância por cancelamento numérico. Esse último caso **não é achado do autor**: derivada central de log10(1+s), h=1e−6, erro5,737e−11; uma emenda pré-fixada preservou o resultado e usou a identidade estável log1p(s)/ln10, mesmo passo e tolerância1e−11. O erro caiu para7,243e−13. `REVISAO_SUPORTE_H0DN_DERIVATIVE_PROTOCOL.json` e `..._DERIVATIVE.json` documentam a correção numérica, sem afrouxar o limite.

Foram lidos18 arquivos na primeira auditoria: protocolos/código/recibos, adendo e documentação, apenas dois arquivos upstream de **código/configuração** e seus pins Git. Não foram lidas as tabelas observacionais. O helper executado é uma cópia auditável nesta pasta, sem carregador de dados, otimização ou comunicação externa; bytecode desabilitado.

## Densidade singular, medida e normalização

[DERIVED, verificado em sintéticos] Para C=U+ Λ+ U+ᵀ, com posto r, a expressão é

`log p = -1/2 [r log(2π) + Σ log λ+ + ||Λ+^(-1/2) U+ᵀ residual||²]`,

aceita somente quando `Nᵀ residual=0` sob a tolerância numérica declarada. Ela é densidade relativa à medida euclidiana r-dimensional no **suporte afim** da distribuição. A guarda do núcleo impede que um custo de pseudoinversa finito esconda um resíduo impossível. No caso rank0, logdensidade0 no ponto admissível é a convenção de massa Dirac unitária; não é uma densidade contínua normalizada no espaço ambiente.

A verificação independente usou `B=[[1,0],[0,1],[2,-1]]`, `S=[[2,.3],[.3,.7]]`, `z=[.4,-.2]` (notação Python). O custo em Bz coincide com zᵀS⁻¹z. A normalização respeita `pdet(B S Bᵀ)=det(S) det(BᵀB)`, logo a logdensidade redundante difere da elementar por `−log sqrt(det(BᵀB))`. Também houve comparação direta com Cholesky de uma C definida positiva. Portanto duplicar linhas não cria precisão e pode mudar a densidade absoluta por mudança de medida, mesmo quando a razão entre hipóteses permanece igual.

Comparações entre modelos exigem suporte afim/medida de referência compatíveis e modelo de observações comum. Igualdade de dimensão, sozinha, é insuficiente. Subespaços distintos de igual dimensão também exigem cuidado. Quando B, seleção, covariância ou suporte dependem da hipótese, não se pode cancelar uma normalização apenas porque cancelava no exemplo fixo. O texto do autor já restringe as razões ao mesmo espaço e vínculos; o adendo deve conservar essa restrição.

[OPEN numérico] Os cortes1e−12 e1e−10 são escolhas dos exemplos adimensionais, não tolerâncias aprovadas para magnitudes/logaritmos ou toda a rede H0DN. Autovalor pequeno descartado e autovalor negativo dentro da tolerância são tratados como zero; isso é aproximação declarada, não demonstração de vínculo exato. O helper de marginalização inicial usa os defaults internos e não oferece argumento para transportar outra política numérica: uma futura integração precisa de uma política única fixada para todas as covariâncias e seus suportes. O retorno numérico com tolerância no núcleo também não deve ser interpretado como densidade normalizada num tubo do espaço ambiente.

## Prior gaussiano próprio

[DERIVED] Sob `y=mu+A x+epsilon`, x~N(m,S), epsilon~N(0,C), **independentes**, a distribuição marginal é N(mu+A m, C+A S Aᵀ). Isso inclui a normalização completa e pode ampliar o suporte. Não equivale a minimizar chi² nem a integrar com prior plano impróprio. Se a nuisance já integra C ou está correlacionada com epsilon, é necessário reconstruir o modelo conjunto; adicionar A S Aᵀ outra vez duplicaria sua contribuição.

Conferi o caso escalar não trivial A=2 por quadratura normalizada independente; conferi expansão de suporte para C=diag(1,0), A=(0,2), S=0,25, cuja covariância marginal é I2. S=0 foi conferida como probabilidade Dirac própria, não como prior impróprio. A aritmética coincide. A expressão não implementa evidências dos cinco modelos sob priors uniformes compactos e não decide comparabilidade de suportes entre modelos.

## Adendo H0DN: resposta e prior

[REAL documental] Os hashes e blobs Git dos arquivos upstream arquivados `equations.py` e `configs/config.ini` coincidem com o manifesto da revisão anterior. Em `equations.py:522` e nas demais linhas do fluxo, `coeffs[ieq,ihub]=1` acompanha `h−0,2 M0=ab+5`; h é log10(H0). A alteração universal atua pela coluna `A[:,ihub]`, não por somar o mesmo número a todas as observações. No modelo condicionado proposto, `h=log10(b)+log10(K)`. Se b/h é nuisance inteiramente livre e só existe a rede local, K é degenerado com essa escala; um fundo independente ou informação adicional específica é necessário.

[DERIVED condicional] `E[y_C]=mu_host+delta_C` define viés **diferencial positivo no módulo publicado**, preservando a possibilidade de cancelamento de um zero fotométrico comum a hosts e âncoras. No caso puramente Cefeida com interceptos/geometria fixos, o módulo aparente maior reduz M e reduz h em delta_C/5; removê-lo faz a correção oposta. Assim o deslocamento **aparente** satisfaz `1+s=H_aparente/b=10^(−delta_C/5)`, ou `delta_C=−5 log10(1+s)`. Não é uma resposta universal automática da rede mista.

Para s uniforme em [−0,15;0,15], o suporte ordenado de delta é [−0,30348920176805827;0,3529053714285364] mag. O Jacobiano é `|ds/delta|=(ln10/5) 10^(−delta/5)`. Logo `pi(delta)=ln10/[5*(0,30)] * 10^(−delta/5)` dentro desse intervalo e zero fora. Os endpoints, a inversa, a monotonicidade e a integral unitária foram conferidos. Um prior uniforme em delta seria outro prior; mesmo endpoints não o tornam equivalente. Exige s>−1. Estes cálculos são de transporte de parâmetro, não ajuste a centro observado.

[REAL documental/OPEN seleção] `configs/config.ini:37` contém `host_exclude_list = *jagb*, *mira*, b25, SMC`: o baseline arquivado exclui JAGB. O adendo corretamente registra que esse baseline sozinho não cumpre TRGB/JAGB da F1. Uma extensão precisa fixar fontes/seleção/âncoras e covariâncias compartilhadas; não multiplicar estimativas comprimidas correlacionadas. O JSON permanece `PROPOSED_NOT_RATIFIED`; esta revisão não aprova V1 ou autoriza composto.

## Identidades e alcance

As fontes e hashes integrais estão em `REVISAO_SUPORTE_H0DN.json`; os snapshots do adendo preservam a versão examinada. A revisão usa resultados puramente sintéticos, sem catálogo/centro novo, sem rodar upstream, sem mudar as cinco hipóteses, kernel ou gate. A correção de API pode ser qualificada pelo delta e novas regressões, preservando as evidências históricas, sem repetir fits ou os ritos.

## Resolução ao lado — V2, 06/10/2026 UTC

[REAL — revisão independente do delta] **H0DN-01 e H0DN-02 resolvidos em `singular_gaussian_v2.py`.** O autor criou versão nova, sem modificar a biblioteca original. A validação agora exige escalares finitos/não negativos; checa os limiares derivados para overflow; faz a simetrização sem somar dois valores grandes antes da divisão; verifica exatamente as seis formas e sua finitude antes de operações que poderiam fazer broadcasting. As fórmulas de densidade/convolução e os defaults científicos não foram alterados.

O pacote V2 tem37 regressões registradas, com código/protocolo pinados no FREEZE_V2 antes da execução. A revisão independente qualificou somente o delta:16 conferências passaram, incluindo os cinco contraexemplos agora rejeitados, a expansão de suporte por prior próprio e a normalização absoluta sob mapa redundante. Biblioteca, protocolo, freeze, RESULT18 e manifesto da primeira versão continuam com os mesmos bytes/hashes. Nenhum driver de teste do autor ou upstream foi executado pelo revisor; usou-se uma segunda cópia byte a byte nesta pasta.

V2 SHA256 lido: `98264bdd57aaad0904bd342631fd3c147fa19f90e8922f0ad6b15ac1b3b93374` (4953 bytes). Evidência: `REVISAO_SUPORTE_H0DN_V2_PROTOCOL.json`, `review_support_h0dn_v2.py`, `REVISAO_SUPORTE_H0DN_V2.json`. A aprovação restringe-se ao protótipo sintético. Política numérica H0DN real, montagem/seleção, nuisance compartilhadas, medida comum e evidências das cinco hipóteses permanecem OPEN; adendo H0DN continua proposta, sem ratificação de V1.
