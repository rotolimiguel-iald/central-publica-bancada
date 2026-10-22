# F9 — próximo controle somente por erros e projeto linear

[DERIVED condicional / PLANO NÃO EXECUTADO] Este controle antecede qualquer leitura de centros para veredito. Usa somente identificadores, coeficientes das equações e erros/covariâncias documentados. Não calcula ajuste, intercepto observado, H0 observado ou evidência. A família PSD estelar já foi qualificada; a matriz completa da rede depende da especificação linear e dos blocos de erro não estelares em preparação.

Duas alternativas: (A) reconstrução completa por erros primitivos/jacobianos físicos, com orçamentos publicados suficientes; (B) construção fiel ao modelo upstream e à família residual PSD explicitamente limitada, preservando as hipóteses de fatoração do upstream. B permite o diagnóstico de identificabilidade; seu resultado é condicional, não uma medição das correlações ausentes.

## Projeto e suporte comum

Escrever y = X eta + a_h h + c_C delta_C + epsilon. A especificação da gerente determina todas as chaves e coeficientes; não alinhar por posições adivinhadas. Fixar a ordem e a escala das linhas antes de construir o suporte. As linhas em log10(H0) podem ser multiplicadas por5 para trabalhar em magnitudes, desde que y, X, respostas e C sejam transformados juntos. Essa transformação é fixa/comum aos modelos; a medida e o jacobiano são registrados. Nenhum rank é escolhido para melhorar um ajuste.

Com decomposição do suporte C=U Lambda U^T, W=Lambda^(-1/2)U^T e núcleo N, conferir N^T X=N^T a_h=N^T c_C=0 na tolerância fixada e nos vínculos combinatórios exatos. O teste futuro dos centros exigirá ainda N^T y=0; o controle por erros não pode declarar isso verificado. Caso falhe, nenhum uso de C+ elimina a inconsistência.

## Eliminação dos nuisance sem centros

Defina Xw=W X e Aw=W[a_h,c_C]. QR/SVD rank-revealing fornece base Q para col(Xw), com rank de X conferido e tolerâncias documentadas. O projeto das respostas após nuisance é T=(I−QQ^T)Aw. F=T^T T é informação condicional em h,delta_C; seus elementos e determinante testam a separação das duas direções. Não é S/g do ajuste observado, pois não usa y. Reportar autovalores, singular values e dependência da escala de unidades, sem converter em detecção.

Se F é positiva definida, a covariância de um estimador linear ideal condicionado ao contrato é F^(-1). A resposta puramente universal a uma correção Delta_h depois de permitir delta_C arbitrário tem separação gaussiana ideal |Delta_h|*sqrt(F_hh−F_hC^2/F_CC); isso não inclui ainda incerteza do fundo, priors finitos de delta_C, não linearidade cosmológica ou ausência de componentes de covariância. Não divulgar esse número como poder do teste completo nem como exclusão observada. Sem uma definição de Delta_h e fundo congelada, este passo permanece simbólico.

## Medida nuisance para a futura comparação

Com X inteiramente no suporte, rank pleno, domínio eta=R^p e a mesma medida plana em todos os rivais, a integração exata multiplica a likelihood perfilada por (2pi)^(p/2)/sqrt(det(Xw^T Xw)). C e X variam entre cenários de sensibilidade, mas ficam comuns às cinco hipóteses dentro de cada cenário. O fator arbitrário da medida plana pode cancelar em cada razão entre modelos; não autoriza evidências absolutas nem uma média entre cenários sem prior. A regra deverá constar expressamente do V1.

Alternativa própria: prior gaussiano eta~N(m,Sigma) com fontes e escala justificadas antes de centros; marginalizar por C+X Sigma X^T, sem duplicar erros já marginalizados. Prior uniforme finito exige volume e probabilidade de truncamento, não apenas perfil. Nenhuma largura é ajustada ao resultado. A opção de medida ainda será consolidada com o parecer da gerente.

## Saída limitada e portas restantes

O primeiro controle completo deve registrar fontes/pins, projeto, unidades, ranks, erros de vínculos, custo e falhas. Não há autorização neste plano para um novo composto. Depois vêm cinco modelos de média, fundo/escala acústica, priors próprios dos parâmetros físicos livres, qualificação das compressões e função de veredito. A decisão de abertura continua a do §6 da ORDEM018, após V1 concreto por hash.
