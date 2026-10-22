# R85 — Seleção dinâmica e alcance normal das variações de P

19/10/2026, /root/r69_locality_bridge. Claim996; R16_INTEGRATED_P_H3.
Project/check da referência própria FECHO_MISSION_REFERENCE.json: revisão566,
ready=true. [DERIVED] Demonstração analítica candidata; controle simbólico exato
separado. Nenhum termo Lean novo, hipótese E=0 acrescentada, dado ou β ajustado.

## 1. O que a seleção existente realmente seleciona

| Fonte lida | Enunciado efetivo | Ponte ainda necessária |
|---|---|---|
| TheVerbSelectsTheAction:149–176 | post a é projeção em span(a); select a ψ=〈a,ψ〉a, idempotência | Isso não é δ∫L/δg; a docstring:122–130 separa expressamente os objetos. |
| TransportWitness:57–73 | S3L(v)=〈v,ΣD†D v〉=0 iff cada Dv=0 | Identificar os D e v com uma ação local e suas variações métricas; não fabricar essa identidade. |
| VariationalInhabitant:93–100,136–143 | Se log p_i+h_i=c, a derivada de F(p)=S(p)−Σp_i h_i é zero nas direções Σδp_i=0; recíproca por direções elementares | h é fornecido; não aparecem Ricci, jets de P ou integração no espaço-tempo. |
| DecisionCommutation:172–181,208–230 | Contraste quadrático ½Σβd_i x_i² e fluxo diagonal: gradiente/EDO/Lyapunov | Funcional finito distinto do gravitacional;:54–58 distingue GKLS externo. |
| ModularRemainderAction:17–31,46–53 | Ad_u invisível iff comutação, incluindo corner invariante | 'Action' é ação de automorfismos, não ação lagrangiana. |
| GibbsMatterBridge:28–38,109–122 | Resposta Gibbs é stress nulo; área-matching iff ηRic(ℓ,ℓ)=2πT(ℓ,ℓ) | A hipótese de área não sai da criticidade Gibbs;:125–156 ainda a recebe. |
| SelectedFisherGibbsBridge:41–70,91–114 | Métrica e fonte do mesmo P; conservação sob onda; Einstein sob área | Mesma origem não deriva as equações adicionais. |
| R66 BOSONIC_CONTINUUM:6–15,27–43 | Semigrupo GKLS do aparelho bosônico/OH construído, taxas/gerador declarados | Esse contrato não define um campo SelectedProbabilityData(x) nem sua ação integrada; localização posterior R71 não muda essa distinção. |

O paper unificado:10350–10362,10418–10460 escreve a peça não minimal e a EOM
em Ψ; a identificação operatorial plena é marcada como conjectura nas próprias
linhas10449–10460. Isso é um ponto de partida físico real do acervo, não deve
ser apagado nem confundido com um teorema de seleção variacional de P.
ActionCouplingControls:41–55 já tem o controle dado sem EOM, reaproveitado.
TheAxiomAndTheFalseWitness:59–61 distingue o lock e o atrator GKLS.

### Controle lógico forte, sem substituir a dinâmica da casa

Qualquer P(x)>0 normalizado admite h_i(x)=−log P_i(x). Então log P_i+h_i=0,
e o teorema Gibbs citado vale ponto a ponto. Subtrair a média de h torna o
Hamiltoniano diagonal de traço zero e só muda a constante c. A Hessiana de F
é −Σv_i²/P_i, estritamente negativa nas direções normalizadas não nulas.
Isso inclui o P6 conservado que falha H3 na R84. Construir h DE P não é uma
lei que selecione P; mostra que a propriedade Gibbs, sem origem independente
de h(x) e controle de seus jets, não discrimina as configurações relevantes.
Se h for independente de x e se P forem literalmente seus pesos de Gibbs na
mesma base fixa, P é constante e falha rank4; outra identificação por medidas
ou observáveis variáveis exige sua ponte própria.

Há o mesmo teste puramente algébrico para 'ser atrator GKLS': para qualquer P
fixe ρ_P=diag(P), L_ij=√(γP_i)|i〉〈j|, γ>0. Somando exatamente,
ΣL_ij X L_ij†=γ Tr(X)ρ_P e ΣL_ij†L_ij=γI. Logo

    G_P(X)=γ[Tr(X)ρ_P−X],
    T_t(X)=e^(−γt)X+(1−e^(−γt))Tr(X)ρ_P.

É CPTP e tem único estado estacionário ρ_P, para cada x como parâmetro.
Portanto unicidade/convergência de um GKLS genérico também não implica H3.
Esse reset é CONTRAMODELO LÓGICO, não é o gerador R66 nem foi implantado como
motor. A fórmula foi somada analiticamente; não houve campanha ou dado novo.

## 2. Geometria correta: imersão na esfera e normais

Escreva ψ_i=2√P_i (apenas nesta construção geométrica; NÃO identificar esse
ψ auxiliar com o campo físico Ψ do artigo). Então |ψ|²=4 e
F_ab=〈∂_aψ,∂_bψ〉. Ponha s=P_s=ψ_s²/4, c=ds e q=cᵀF⁻¹c.
Decomponha uma variação admissível em δψ=dψ(X)+N, com
〈N,ψ〉=〈N,∂_aψ〉=0: N é normal à imersão DENTRO da esfera de raio2.
Se II é sua segunda forma fundamental esférica,

    δF=L_XF−2〈N,II_ab〉,
    δc=L_Xc+d(ψ_s N_s/2).

A fórmula normal segue diferenciando 〈N,∂_bψ〉=0. O termo radial da segunda
forma fundamental ambiente não contribui, pois N⊥ψ. Para N=Σf_α N_α,
∂_a f_α não aparece em δF: seu produto com ∂_bψ é zero. É aqui que se obtém
levantamento de CAMPOS, não apenas um rank de jets.

Restrinja agora aos normais N_s=0 COMO CAMPO. Então δs=δc=0 e

    δg=R_c(δF),
    R_c(H)=−H+(2/q²)ccᵀ(uᵀHu),   u=F⁻¹c.

R_c é uma involução: o mapa Π(H)=ccᵀ(uᵀHu)/q² tem Π²=Π, pois uᵀccᵀu=q²;
portanto R_c=−I+2Π e R_c²=I. Assim o único rank adicional exigido para levantar
qualquer H métrico é o mapa normal N↦〈N,II〉 sobre Sym²(R⁴).

Critério suficiente VERIFICÁVEL: em um aberto, escolher dez normais suaves
N_α com N_α,s=0 e a matriz M_(ab),α=〈N_α,II_ab〉 invertível. Dado H compacto,
resolver ponto a ponto

    f=−(1/2)M⁻¹ entries(R_c(H)),   N=Σf_αN_α.

M⁻¹ é suave; f e N têm o mesmo suporte compacto de H; δg=H exatamente, sem
resolver PDE ou perder suporte. Este critério é sobre derivadas de ψ e pode
ser calculado antes de conhecer o Euler métrico; não é a hipótese E=0 renomeada.
Ele não afirma que toda P do acervo o satisfaça. A classe P5 não tem normais.

## 3. Testemunha explícita: P16 com levantamento completo

A estrutura SelectedProbabilityData é genérica em qualquer Fintype, inclusive
Fin16 (SelectedFisherLorentzMetric:243–250). Construímos um representante
matemático admissível, ainda SEM instância Lean compilada.

Em R¹⁵ escolha base ortonormal e_*, e_a (a=0..3), e_ab (0≤a≤b≤3).
Defina q_aa=x_a²/2, q_ab=x_a x_b para a<b e

    v(x)=e_*+Σ_a x_a e_a+Σ_(a≤b) q_ab(x)e_ab,
    η(x)=v(x)/|v(x)|,
    z(x)=1+x_0,       r(x)=√(4−z(x)²).

Escolha O ortogonal com Oe_*=(1,…,1)/√15. Uma construção explícita é
O=I−2wwᵀ/(wᵀw), w=e_*−(1,…,1)/√15 (Householder).
Em um aberto suficientemente pequeno em torno de0, todos os componentes de
Oη são positivos, r>0 e z>0. Defina

    ψ=(z, r Oη),
    P_s=z²/4,   P_j=(4−z²)(Oη)_j²/4  (j=1..15).

Estas fórmulas de P, sem usar r fora do aberto, são suaves globalmente e
normalizadas para todo x; positividade é exigida somente no aberto. Em0,
P=(1/4,1/20,…,1/20). Rank4 do diferencial e relógio não nulo seguem de

    F(0)=diag(13/3,3,3,3),    c(0)=(1/2,0,0,0),
    q(0)=3/52,              g(0)=diag(13/3,−3,−3,−3).

Para construir NORMAIS SUAVES no aberto, seja V a matriz15×5 de colunas
η,∂_0η,…,∂_3η. Seu Gram é invertível perto de0. Ponha

    Q=I−V(VᵀV)⁻¹Vᵀ,
    N_ab(x)=(0, O Q(x)e_ab/r(x)).

Então N_ab⊥ψ e N_ab⊥∂_aψ e sua componente selecionada é zero em todo o
aberto. Em0, η=e_*, ∂_aη=e_a, a componente normal de ∂_a∂_bη é e_ab.
Portanto 〈N_cd,II_ab〉(0)=δ_(ab),(cd). No ordenamento de pares
(00,01,02,03,11,12,13,22,23,33), o mapa coeficientes normais→δg é

    diag(−2,+2,+2,+2,+2,+2,+2,+2,+2,+2),  det=−1024, rank10.

Por continuidade, um aberto menor mantém detM≠0. O critério da seção2 dá
levantamento de TODO campo métrico simétrico compacto nesse aberto.

Não paramos no vetor tangente: dado o N obtido, escreva v₀=ψ_rest/r=Oη e
δv=N_rest/r, com 〈v₀,δv〉=0. A curva efetiva

    ψ_ε=(z, r (v₀+εδv)/|v₀+εδv|),    P_i,ε=ψ_i,ε²/4

preserva z e a normalização, tem derivada N e mantém positividade/rank/clock
para |ε| suficientemente pequeno sobre o suporte compacto. Fora do suporte
P_ε=P; a extensão global normalizada é assim preservada. É uma curva
admissível do MESMO tipo e não uma variação independente de g introduzida à mão.

Controle separado, pré-pinando script/plano: SymPy1.14 calculou as derivadas
exatas de ψ em0, F/g, matriz II, rank/determinante e involução. Uma execução,
exit0 em aproximadamente3,59s, nenhuma aritmética de ponto flutuante nos
cálculos. Evidências EXACT_RANK_*.json/log. O controle não prova por si só
continuidade/levantamento de campos; esses passos foram demonstrados acima.

## 4. A matéria muda — e por que fixá-la impediria o teste nulo

Na testemunha, φ_j=√(P_j/(1−P_s))=(Oη)_j. Nos levantamentos normais,
δφ_j=N_rest,j/r, em geral NÃO ZERO. Consequentemente, o critério de rank não
permite eliminar a parcela ΣE_φ δφ da variação da ação composta.
Uma via suficiente, depois da identificação correta da ação, é uma equação
material independente que torne E_φ radial: E_φ,j=λφ_j. Então Σφδφ=0 elimina
a parcela material em todas essas curvas normalizadas; estacionariedade
verdadeira da ação composta e rank acima implicam E_g=0 pelo lema fundamental.
Isso usa uma equação material verificável (a heigen sigma é candidata para uma
ação sigma identificada), não acrescenta Einstein como hipótese. A seleção
existente da seção1 ainda NÃO forneceu essa estacionariedade gravitacional.
Acoplamento não minimal/outros campos pedem o Euler COMPLETO, não somente um
termo cinético escolhido. Em particular, não se identifica Ψ físico com φ.

A alternativa 'fixar φ e variar livremente a métrica' é impossível aqui, de
forma geral, não apenas no exemplo warped. Ponha h=Σdφ_j², s=P_s. Então

    F=ds⊗ds/[s(1−s)]+4(1−s)h.

Se δφ=0, a normalização força δP_j=−P_j δs/(1−s) e δh=0. Em D=ker ds,

    δg|_(D×D)=4δs h|_(D×D).                            (†)

Com efeito, a restrição de δ(ccᵀ/q) é zero, assim como a parte de δF que tem
um fator ds. h|D é positiva definida; D é espacial, pois g⁻¹(ds,ds)=q>0.
Um teste métrico H=ζ k♭⊗k♭ com k não nulo e nulo tem, onde ζ≠0, rank1
quando restrito a D: k♭|D não pode ser zero, pois isso tornaria k♭ proporcional
ao covetor timelike ds. Já (†) tem rank3 quando δs≠0 e rank0 se δs=0.
Logo NENHUM teste nulo desse tipo, não zero, tem levantamento com δφ=0.
Fixar φ é mais forte que fixar T; não se transfere essa impossibilidade a
outras condições materiais sem examinar suas equações.

## 5. Avanço entregue e lacuna residual exata

[DERIVED] O obstáculo genérico 'variações P não alcançam métricas' foi
substituído por condição calculável e testemunha P16 que efetivamente alcança
campos compactos; para P5 permanecem as restrições da R84. A matéria do mesmo P
foi mantida na cadeia. [OPEN] Falta uma lei física independente que selecione
uma P apropriada e produza estacionariedade da AÇÃO COMPLETA, incluindo o Euler
material, ou uma ponte demonstrada entre os funcionais existentes e essa ação.
Gibbs/lock/atração não foram descartados: seus enunciados foram delimitados.
Não existe nesta nota uma inferência de rank10 para H3 sem os passos restantes.

Cobertura: os módulos expressamente pedidos, suas remissões TransportWitness/
DecisionCommutation/TheAxiomAndTheFalseWitness, Selected* e R66 já pinada,
mais linhas10319–10460 do paper unificado. Busca focal; nenhuma afirmação de
inexistência em todo o PC. A primeira tentativa de nome de pasta R66 falhou e
foi resolvida por rg --files para reservoir_bridge_r66. Sem novas chamadas de
IA, integração em produção, memória, missão, quadro ou gate.
