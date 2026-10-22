# Integração condicional dos priors físicos — derivação F1(c)

Unidade df482198-56c4-4169-ae5e-3908f5d12f2c. [DERIVED — sob as hipóteses declaradas]
Derivação matemática e candidato estático. Nenhuma integral, vetor, cauda, mínimo, controle ou
dado observado foi avaliado nesta preparação. [REAL] As fontes/pins foram lidos; a interpretação
algébrica abaixo não é evidência de execução.

## 1. Objeto e fontes

five_model_assembly.py, consumidor a987 revisto no mapa563 e linear_gaussian.py fixam o objeto.
A fonte do montador define theta=(H0,omega_b h²,omega_c h²), os mesmos 283 componentes, 63 eta,
T/unidades e priors próprios: beta uniforme em [-0,05;0,05], s em [-0,15;0,15] e rd em
[130,160] Mpc. O contrato numérico F9 §5 confere as densidades 10,10/3,1/30 e a mudança de
variável H4. O theta de fundo é fixo nesta unidade; nenhuma nova previsão cosmológica é
necessária ao variar os três extras. H5 altera apenas o denominador BAO, conservando rstar
CMB e a resposta local; H4 altera apenas c_C delta; H3 altera apenas a resposta local a_h.

A implementação proposta reutiliza o objeto PreparedJoint e a classe Gaussian existentes
por injeção. Não altera suas fontes, não reconstrói C, não usa bloco local isolado e não
escreve outra pseudoinversa/SVD/normalização. O pacote de fundo já calculado é fornecido em
bytes e ligado ao mesmo hash/identidade/theta da montagem.

## 2. Redução afim com C inteira

No suporte transformado fixo, escreva W para o branqueamento de C e Q para a base ortonormal
de WX já construída pelo backend. R=(I-QQ^t)W e K é o logaritmo do prefator completo já
qualificado. Para um parâmetro extra x, uma média afim
mu(x)=mu_ref+v(x-x_ref), t=x-x_ref, b_ref=y-mu_ref, defina

r=R b_ref, w=R v, A=w^t w, B=r^t w, D=r^t r.

Então, sob o mesmo suporte afim, desenho/posto e medida:

q(x)=||r-wt||² = D-2Bt+At²,
log L_eta(x)=K-q(x)/2
           = log L_eta(x_ref)+Bt-At²/2.

O código chama residualize do backend para obter r e w; produtos escalares formam somente
os coeficientes do eixo. Todas as covariâncias cruzadas entram em W/R. Não se substitui C
por uma matriz BAO ou local isolada. O cálculo pontual continua em log_integral do backend,
com todos os prefatores e log(kappa) comum omitido identificado. Mesmo quando prefatores
podem cancelar numa razão futura, eles não são descartados aqui.

Exige-se v dentro do suporte linear, X dentro dele com posto63, e todas as médias na classe
afim comum admitida. Os endpoints do segmento são conferidos no código junto ao vetor
direção; em aritmética exata isso basta por afinidade e convexidade. Os testes float/tolerâncias
do backend são de engenharia, não certificado de suporte. Um zero de densidade devido ao
complemento do suporte comum não é underflow, falha de posto ou evidência de rejeição.

A=0 implica w=0 e B=0 em aritmética exata. O parâmetro extra pode ser totalmente absorvido
pela medida nuisance comum: L_eta fica constante. Como seu prior é próprio e normalizado,
a integral é L_eta(x_ref), sem penalidade artificial de largura e sem acrescentar uma
64ª direção plana. Isso é diferente de uma direção não identificada ENTRE os 63 nuisance,
que já invalidaria a integral plana no backend.

No candidato float, A=0 só toma o ramo plano quando cada componente de w é exatamente zero
no cálculo. A=0 com w não nulo é CURVATURE_UNDERFLOW e falha visível. Um w computado zero
não prova a degenerescência científica exata; a saída diz FLAT_EXTRA_IN_PROJECTED_FLOAT_GEOMETRY.
Não há cutoff novo para chamar A pequeno de zero. A>0 pequeno permanece no ramo geral,
com limitação de precisão declarada.

## 3. H3: beta linear e prior uniforme

A fonte fornece h_local=log10(H0)+(I_law/ln10) beta. Como a_h já está transformado por T,
v3=(I_law/ln10) a_h. Não multiplicar a_h outra vez por cinco. x=beta, com l=-0,05, u=0,05
e largura Delta_beta=0,10; usar como referência o beta do pacote pinado.

Para A>0, completando o quadrado, m=B/A e t_l=l-beta_ref, t_u=u-beta_ref:

J3 = L_ref/Delta_beta * exp(B²/(2A))*sqrt(2pi/A)
     * [Phi(sqrt(A)*(t_u-m)) - Phi(sqrt(A)*(t_l-m))].

É integral do likelihood contra o prior 10 d beta, não valor no melhor beta.
A densidade uniforme foi mantida; não há troca para prior gaussiano nem corte em ±n sigma.
A=0 segue o ramo constante acima.

A expressão com exp(B²/(2A)) e diferença de Phi explica a matemática; ela NÃO é a sequência
float implementada. Dois CDFs comuns podem arredondar ao mesmo número nas caudas e fabricar
massa zero, enquanto o prefator pode transbordar e sua combinação ser finita.

## 4. H4: s uniforme, delta e Jacobiano

Defina lambda=ln10/5 e delta=-5log10(1+s)=-ln(1+s)/lambda.
A inversa é s=exp(-lambda delta)-1 e |ds/d delta|=lambda exp(-lambda delta).
A orientação se inverte:

delta_l=-5log10(1+0,15), delta_u=-5log10(1-0,15),
pi_delta(delta) = lambda/0,30 * exp(-lambda delta).

A normalização é exata:
integral(delta_l,delta_u) pi_delta d delta
= [exp(-lambda delta_l)-exp(-lambda delta_u)]/0,30
= [(1+0,15)-(1-0,15)]/0,30 = 1.

A média é mu_ref+c_C(delta-delta_ref), portanto v4=c_C, sem novo termo no fundo.
Com t=delta-delta_ref:

L_eta(delta) pi_delta(delta)
= L_ref * lambda/0,30 * exp(-lambda delta_ref)
  * exp[(B-lambda)t - A t²/2].

Para A>0, a mesma janela gaussiana usa B_eff=B-lambda, mas o fator
lambda/0,30 * exp(-lambda delta_ref) permanece fora. Completando o quadrado:

J4 = L_ref * lambda/0,30 * exp(-lambda delta_ref)
     * exp[(B-lambda)²/(2A)] * sqrt(2pi/A)
     * [Phi(sqrt(A)*(t_u-(B-lambda)/A))
        - Phi(sqrt(A)*(t_l-(B-lambda)/A))].

Não é correto adotar prior uniforme em delta, omitir o fator exponencial ou trocar somente
B por B-lambda e esquecer a normalização/Jacobiano. Para A=0 com w=B=0, a integral do prior
normalizado devolve L_ref. O candidato usa esse ramo por identidade de normalização,
sem calcular diferenças de exponenciais quase canceladas.

## 5. Janela estável ancorada, comum a H3/H4

Seja ell(x)=log L_eta(x)+k x+c, com k=0,c=-ln Delta_beta para H3 e
k=-lambda,c=ln(lambda/0,30) para H4. Escolha o máximo RESTRITO deste integrando:

x_p=x_ref+clip((B+k)/A,[l-x_ref,u-x_ref]).

O código decide primeiro as fronteiras por comparar B+k com A(l-x_ref), A(u-x_ref);
só divide por A quando a solução está dentro. Isso evita overflow desnecessário do vértice
externo. Avalia log L_eta(x_p) diretamente pelo backend, sem D-B²/A, e define

h=B+k-A(x_p-x_ref),
J = exp[log L_eta(x_p)+k x_p+c] *
    W(A,h,l-x_p,u-x_p),

W(A,h,L,U)=integral_L^U exp(h z-Az²/2) dz > 0.

Essa é a função especial injetada log_exp_quad_interval. Para A>0 sua forma completada é

log W = h²/(2A)+0,5 ln(2pi/A)
        + log[Phi(sqrt(A)U-h/sqrt(A)) - Phi(sqrt(A)L-h/sqrt(A))].

A função deve avaliar o CONJUNTO em log-domain com precisão declarada; não basta devolver a
subtração de CDFs float. Em cauda direita, a diferença de survival functions evita 1-1; em
cauda esquerda, usar log-CDF; logdiffexp pode usar log(-expm1(delta_log)). Ainda assim,
completamento e log-cauda podem cancelar, ou endpoints normalizados podem coalescer por
arredondamento. A implementação da função especial deve lidar com isso por formulação
escalada/erfcx, expansão controlada, precisão maior ou integração escalada do mesmo alvo,
sem chamar massa positiva de zero. Método/erro são reportados. Esse serviço é uma dependência
explícita, não implementada/importada/qualificada automaticamente aqui.

Os argumentos são ancorados com zero dentro do intervalo e máximo restrito do integrando.
Na matemática exata h z-Az²/2<=0 ali. Isso reduz a necessidade de exponenciais enormes.
O log da janela de intervalo finito não vazio deve ser finito; -inf/NaN do serviço é falha,
não likelihood zero. Erros de backend/coeficientes/reconstrução e do modelo teórico permanecem
separados do erro local da função especial. A ausência de cota uniforme não impede uma
estimativa ENGINEERING_ONLY honesta, nem permite rotulá-la certificada.

## 6. H5: q=1/rd, prior e quadratura 1D

No theta fixo, as 13 médias BAO são D_j(theta)/rd, e as demais 270 componentes não variam
com rd. Em q=1/rd, a média é afim e v5 tem D_j nas posições BAO3..15 (indexação0) e zero
nas demais. q_l=1/160, q_u=1/130, q_ref=1/rd_ref.

O prior continua uniforme em rd, não em q:
pi_q(q)=1/(30 q²), q em [q_l,q_u].
A massa integral é (1/q_l-1/q_u)/30=(160-130)/30=1.

J5 = integral(q_l,q_u) L_eta(q)/(30 q²) dq.

Não se aplica uma janela gaussiana pura e se descarta q^-2. Uma alternativa equivalente
seria quadratura em rd com densidade1/30 e média D/rd; a preparação escolhe q para reutilizar
o eixo afim. O código recupera v5 a partir da média BAO já pinada multiplicada por rd_ref.
Essa igualdade é algébrica; sua reconstrução float tem arredondamento não certificado,
explicitamente incluído nas limitações de engenharia. Não há nova chamada CAMB por extra.

Para o serviço de quadratura positiva, q=q_l+Delta_q u, u em [0,1]. Seja q_p o máximo
restrito da likelihood, sem prior. Defina

log_anchor=log L_eta(q_p)+ln(Delta_q/30)-2ln q_l,
f_scaled(u)=exp[log L_eta(q)-log L_eta(q_p)+2ln(q_l/q)].

Então J5=exp(log_anchor)*integral_0^1 f_scaled(u)du. A densidade em q e a transformação
de intervalo foram transportadas integralmente. No cálculo exato f_scaled<=1, e a
log-likelihood de cada nó vem do MESMO backend/C/X. A API impõe um teto explícito às
avaliações do callback e exige recibo de contagem/método/erro do integrador injetado.
O limite de tempo operacional pertence ao executor futuro, não é prometido por esta
função pura.

Nós que underflowem para zero são contados; isso não prova massa zero da região nem fornece
cota sobre massa não amostrada. Área retornada zero em um integral matematicamente positivo
é falha QUADRATURE_ZERO_OR_UNDERFLOW, não conclusão científica. Um recibo de erro estimado
de quadratura ordinária não é certificado de resto ou cobertura. Uma falha do callback é
latched mesmo se o serviço a capturar; não há retry/fallback automático, omissão de massa
ou renormalização da parte disponível.

## 7. Mínimo condicional da mesma likelihood — fórmula, sem execução

O mínimo de q ao longo de cada eixo afim, para A>0, é em

x_L=x_ref+clip(B/A,[l-x_ref,u-x_ref]),
q_min=||r-w(x_L-x_ref)||².

A forma D-2B t+A t² é equivalente; avaliar a norma residual evita subtração ruim de D-B²/A.
A=0 com w=0 dá mínimo plano D em todo intervalo. Isso é o perfil condicional no theta fixo,
não um mínimo global em theta e não a integral do prior.

H3 usa x=beta. H4 usa x=delta com os extremos transformados; por monotonicidade pode voltar
a s=exp(-lambda delta)-1. H5 usa q e pode voltar a rd=1/q. Em H4, B-lambda pertence
EXCLUSIVAMENTE ao integrando do prior, nunca a esse mínimo da likelihood. Em H5, o fator
q^-2 também não altera o ponto que minimiza q_L: ele pesa a integral, não o perfil.
Não foi implementada/rodada rotina nova de ajuste por causa deste adendo; a fórmula permite
reutilização documental posterior.

## 8. Normalização, família e escopo

Os cinco resultados são médias condicionais sobre priors físicos extras próprios:
H1/H2 conservam o valor pontual, H3/H4/H5 integram somente seu extra. O prior base
uniforme em theta, densidade50/3, fica como metadado NÃO aplicado/NÃO integrado.
Ainda falta integrar esse theta para obter a integral relativa inteira; esta unidade
não calcula evidência, razão de Bayes, mínimo global, p, sigma, calibração ou veredito.

κ d_eta é a mesma medida comum, com logκ omitido como no consumidor. Toda normalização
Gaussian é retida. Usar C completa e o mesmo suporte evita supor independência para fazer
a redução 1D. Não altera os modelos/priors, MM condicional não ratificado, V1, abertura
observada ou estatuto UNBOUNDED_THEORY_ERROR. Erro de engenharia não vira massa zero nem
remove rival; a função só devolve a coleção completa após concluir os cinco ramos.

A documentação distingue prova algébrica condicional, código escrito e execução futura.
Nenhuma das referências ou flags injetadas é certificado físico ou autorização por si.
