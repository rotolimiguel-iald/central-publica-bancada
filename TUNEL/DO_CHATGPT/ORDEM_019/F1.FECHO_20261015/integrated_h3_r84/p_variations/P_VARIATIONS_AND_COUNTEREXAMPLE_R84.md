# R84 — Variações dos mesmos P: alcance, exemplo positivo e obstrução concreta

Autor: /root/r69_locality_bridge; 19/10/2026. Claim993, R16_INTEGRATED_P_H3.
Referência própria FECHO_MISSION_REFERENCE.json; project/check revisão562, ready=true.
Estatuto: [DERIVED], demonstração analítica candidata; nenhum novo termo Lean ou build.
Os exemplos abaixo são configurações do tipo matemático atual, não soluções físicas
atestadas da TGL nem refutação da teoria. Não usam β, dados observados ou ajuste.

## 1. Reuso e domínio exato

SelectedFisherLorentzMetric.lean:39–43,243–261 define, para probabilidades positivas
normalizadas p_i, diferencial injetiva e relógio c=dp_s não nulo:

    F_ab=Σ_i (∂_a p_i)(∂_b p_i)/p_i,
    q=cᵀF⁻¹c>0,   g=2 ccᵀ/q−F.

SelectedProbabilitySigma.lean:44–51,104–108,132–150 já constrói dos MESMOS P
φ_j=√(p_j/(1−p_s)), Σφ_j²=1, w_j=dφ_j e

    T_ab=c_G Σ_j [∂_aφ_j ∂_bφ_j−(1/2)g_ab g^{cd}∂_cφ_j∂_dφ_j],
    c_G=k_G/(π cosh² k_G),   k_G>0.

c_G é a resposta Gibbs da fonte citada; não é substituído por um parâmetro
escolhido para fazer Einstein valer. Escrevemos C=2π/η para o coeficiente da
conclusão nula (C=8πG somente sob a identificação física/normas correspondentes).
A conservação decorre de □_gφ_j=λ(x)φ_j, pelo teorema nas linhas170–189.
Harea continua hipótese explícita nas linhas191–218.

## 2. Diferencial completo e equação projetada de estacionariedade

Fixe o rótulo s. Tome v_i=δp_i suaves, suporte compacto em U, Σ_i v_i=0.
Sobre esse compacto, positividade/rank/clock são abertos: ε suficientemente
pequeno mantém admissibilidade. As derivadas são

    δF=Σ_i [(dp_i⊗dv_i+dv_i⊗dp_i)/p_i−v_i dp_i⊗dp_i/p_i²],
    δc=dv_s,  u=F⁻¹c,
    δq=2u·δc−uᵀδF u,
    L_P(v):=δg=−δF+(2/q)(δc⊗c+c⊗δc)−(2δq/q²)ccᵀ,
    B_P(v)_j:=δφ_j=(φ_j/2)[v_j/p_j+v_s/(1−p_s)].

São identidades de diferenciação no ramo positivo. Não se variou g mantendo
simultaneamente P fixo. Se uma ação covariante S[g,φ] já tiver primeira variação
integrada, com contorno eliminado legitimamente,

    δS=∫ (E^{ab} δg_ab + Σ_j E_j δφ_j) d⁴x,

E e E_j são densidades de Euler COMPLETAS: incluem acoplamento não minimal e
qualquer termo material da ação escolhida. Então a ação composta S[g(P),φ(P)]
obedece exatamente a δS=∫v·(L_P†E+B_PᵀE_φ).
Uma forma explícita evita esconder a condição no nome 'adjunto'. Ponha

    z=cᵀEc,
    A=−E+(2z/q²)uuᵀ,
    b=(4/q)Ec−(4z/q²)u.

Pois E:δg=A:δF+b·δc, a densidade de Euler por p_i é

    Q_i=−(dp_iᵀ A dp_i)/p_i²
        −∂_a[(2/p_i) A^{ab}∂_b p_i + δ_is b^a] + Z_i,
    Z_j=E_j φ_j/(2p_j)                (j≠s),
    Z_s=Σ_j E_j φ_j/[2(1−p_s)].

Integração por partes usa somente suporte compacto. A conclusão correta é

    Q_i=Q_s para todo i≠s,

ou Q_i=Λ_P(x) comum a todos os rótulos. Isso é estacionariedade sob Σv_i=0.
NÃO é E^{ab}=0. No ramo Gibbs com potenciais p_i em vez de φ_j, substituir
Z_i pelo Euler material correspondente E_i; pesos k_i constantes permanecem
fixos. Se outros campos/boundaries externos variam, suas parcelas têm de entrar.

## 3. P5: rank de jet 10, mas variações de campos apenas de difeomorfismos

Com exatamente cinco probabilidades, rank(dp)=4 torna P um difeomorfismo local
para um aberto do simplex positivo de dimensão4. O Fisher e o relógio são
pullbacks de tensores fixos no simplex; como as dimensões coincidem, a inversa
e q também comutam com o pullback. Portanto g(P) é o pullback de UMA métrica
fixa no simplex, e φ(P) o pullback de funções fixas.
Para toda v normalizada existe X=(dP)⁻¹v; então

    δg=L_Xg,    δφ_j=X·dφ_j.

No ponto x, impondo X(x)=0 e escolhendo DX(x) livre, δg_ab(x)=
g_cb∂_aX^c+g_ac∂_bX^c realiza QUALQUER tensor simétrico H_ab(x): basta
∂_aX^c=(1/2)g^{cb}H_ab. Assim o mapa de 1-jets é sobrejetivo (rank10).
Isso NÃO torna a aplicação de campos sobrejetiva: todas as variações em um
aberto são derivadas de Lie, com compatibilidades diferenciais.

Consequência material: uma ação difeocovariante integrada somente desses
objetos, sem estrutura externa fixa, é automaticamente estacionária sob essas
variações compactas de P5, pela mudança de variáveis no integral. Equivalente:
a contração de E com L_Xg somada à de E_φ com X·dφ é a identidade de Noether.
Nem E=0 nem E_φ=0 decorrem disso. Portanto 'a ação é estacionária em P5'
isoladamente pode ser uma condição vazia, embora o 1-jet tenha rank10.
Este argumento exige suporte compacto e ação verdadeiramente covariante;
não se aplica a uma lei extra, observador/campo externo fixo ou contorno alterado
sem analisar a contribuição correspondente.

## 4. Família calculável com mesma métrica/fonte e conservação

Seja φ:V⊂R³→S^{m−1} uma imersão suave positiva, h=Σdφ_j², e suponha
Δ_hφ_j=−3φ_j (exemplos explícitos abaixo). Em U=(0,π)×V defina

    p_s=sin²(τ/2),   p_j=cos²(τ/2) φ_j(y)².

As identidades trigonométricas normalizam P em todo R⁴ usando as fórmulas
abaixo; a positividade é necessária apenas em U. dp_s=(sinτ/2)dτ≠0.
Se dP(v)=0, dp_s(v)=0 implica v_τ=0; então φ_j>0 implica dφ_j(v)=0,
e a imersão implica v=0. Logo todas as condições de SelectedProbabilityData
são satisfeitas. Cálculo direto dos produtos diferenciais, Σφdφ=0, dá

    a(τ)=2cos(τ/2),
    F=dτ²+a²h,     g=dτ²−a²h,
    sigmaPotential_j=φ_j,   □_gφ_j=−a⁻²Δ_hφ_j=(3/a²)φ_j.

Portanto heigen e a conservação exigida pelo teorema EXISTENTE valem nessa
família, não são adicionadas sem testemunha. Para v h-unitário e
ℓ=∂_τ+a⁻¹v, g(ℓ,ℓ)=0 e T(ℓ,ℓ)=c_G/a².

Verificação de sinal de Ricci pelas definições do kernel:
CurvatureJetAlgebra:27–29 é ∂_iΓ_j−∂_jΓ_i+[Γ_i,Γ_j];
MetricCurvatureSymmetries:31–32 contrai R^a{}_{baj}.
Aqui Γ⁰_ij=aa' h_ij, Γⁱ_0j=(a'/a)δⁱ_j, Γⁱ_jk=Γ(h)ⁱ_jk; daí

    Ric_00=−3a''/a,
    Ric_ij=Ric(h)_ij+(aa''+2a'²)h_ij,
    Ric(ℓ,ℓ)=[Ric(h)(v,v)+2(a'²−aa'')]/a²
             =[Ric(h)(v,v)+2]/a².

A última igualdade usa a'=−sin(τ/2), a''=−a/4, portanto a'²−aa''=1.
Assim o residual nulo EXATO da mesma configuração é

    H3_defect(ℓ)=[Ric(h)(v,v)+2−C c_G]/a².                 (★)

### 4a. Rota positiva específica — esfera, cinco probabilidades

Escolha φ=(cosχ₁, sinχ₁cosχ₂, sinχ₁sinχ₂cosχ₃,
           sinχ₁sinχ₂sinχ₃), χ_i∈(0,π/2).
Então h é o S³ unitário, Ric(h)=2h, Δ_hφ_j=−3φ_j. Logo a construção P5
produz a igualdade nula de H3 para TODAS as direções precisamente quando
C c_G=4. Nessa normalização matemática, o cálculo completo dá
G+C_Λ g=C T com C_Λ=3/4 quando C c_G=4. Não se trata de Λ físico medido:
Fisher/raio2 e coordenadas são as unidades do exemplo. A relação C c_G=4
precisa vir da identificação admitida; escolher k_G para satisfazê-la seria
impor o coeficiente, não derivá-lo. A existência dessa rota positiva é mantida.

### 4b. Contraexemplo único — seis probabilidades, fonte conservada

Escolha φ em S⁴, com θ,χ,ψ∈(0,π/2):

    φ=(cosθ/√3, sinθ/√3,
       √(2/3) sinχcosψ, √(2/3) sinχsinψ, √(2/3) cosχ).

É o produto S¹(1/√3)×S²(√(2/3)) no S⁴. A norma é1, todos componentes são
positivos, e h=(1/3)dθ²+(2/3)(dχ²+sin²χ dψ²) tem rank3. O Laplaciano
no círculo tem autovalor −1/(1/3)=−3; nas coordenadas da esfera tem
−2/(2/3)=−3. Logo TODAS as φ_j satisfazem a mesma heigen acima.
Mas Ric(h)(v,v) vale0 na direção unitária do círculo e3/2 na da esfera.
Por (★), as duas direções nulas exigiriam simultaneamente

    C c_G=2    e    C c_G=7/2,

impossível, mesmo se C fosse escolhido livremente. Uma parcela Λg não altera
nenhuma dessas contrações. Não se apelou a uma fonte independente de P.

Ponto concreto τ=π/2, θ=χ=ψ=π/4:

    P=(1/2,1/12,1/12,1/12,1/12,1/6),
    g=diag(1,−2/3,−4/3,−2/3),
    Ric=diag(3/4,1/6,4/3,2/3),
    T/c_G=diag(3/4,−1/6,−1/3,−1/6),
    ℓ_c=(1,√(3/2),0,0), ℓ_s=(1,0,√3/2,0).

As contrações exatas são: g(ℓ_c,ℓ_c)=g(ℓ_s,ℓ_s)=0;
Ric(ℓ_c,ℓ_c)=1, Ric(ℓ_s,ℓ_s)=7/4;
T(ℓ_c,ℓ_c)=T(ℓ_s,ℓ_s)=c_G/2.
O pequeno controle racional anexo confere esta álgebra no ponto; NÃO substitui
a demonstração diferencial acima e não é campanha de dados nem prova Lean.

## 5. Resultado útil e próximo contrato

[DERIVED] O mapa P→(g,T) existente é concreto, e há famílias em que a igualdade
nula deriva geometricamente sob coeficiente identificado. [DERIVED] O mesmo
tipo permite fonte conservada sem H3, de modo que origem comum+heigen não
substitui a lei dinâmica. Estacionariedade composta só fornece Q_i comum;
a classe P5 mostra por que rank local de jets não resolve sua integrabilidade.

Para avançar sem trocar a meta: identificar a ação/fonte não minimal COMPLETA
no mesmo registro e a dinâmica que selecione P; provar que a equação projetada
(e eventuais equações dos outros campos) elimina o residual métrico, ou então
caracterizar explicitamente a subclasse geométrica e seu coeficiente derivado.
Nenhuma conclusão daqui diz que a TGL física admite os exemplos como soluções;
eles isolam exatamente a hipótese que os tipos atuais ainda não carregam.

Cobertura da recuperação: leitura direta dos módulos Selected*, Fisher,
FiniteCoherentSources, convenção de curvatura, R83 e busca dirigida de nomes
SelectedProbabilityData/selectedMetric/selectedSigmaRecord nos módulos
*Variat*.lean e *Action*.lean. O grep dirigido não encontrou essa ponte nesses
nomes. VariationalInhabitant:15–24 trata criticalidade de Gibbs/energia livre;
VariationalFlow:28–30,47–53 trata fluxo e sua derivada; não são variação métrica.
TheSameBetaReadsFourFaces:20–42 tipa a EOM como INPUT;
ActionCouplingControls:41–55 fornece contra-modelo algébrico do dado sem EOM.
Esses conteúdos foram reaproveitados, não declarados inexistentes. Não houve
varredura de todo PC. Duas tentativas iniciais de nomes de arquivo (singular/
ProbabilityFisherField) falharam visivelmente e foram resolvidas por rg para
FiniteCoherentSources/FisherInformationTensor. SHA/trechos estão no manifesto.
