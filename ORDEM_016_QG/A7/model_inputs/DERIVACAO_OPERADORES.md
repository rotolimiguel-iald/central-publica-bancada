[DERIVED — especialização algébrica; REAL — CAS exato dos operadores de entrada]

# A7.b — modelo mínimo e dados livres conferidos

## 1. O modelo fixado pela087

Usamos um aberto Lorentziano orientado e globalmente hiperbólico de um espaço-forma4D.
A convenção desta conta é R_abcd=K(g_ac g_bd−g_ad g_bc), K>0; portanto Ric=3K g,
R=12K. κ é real não nulo. A ação restrita é S_EH=−(2κ)⁻¹∫μ_g(R−2Λ).
O requisito on-shell fixa Λ=3K: G+Λg=(Λ−3K)g. Isso é condição do modelo de teste,
não identificação de Λ com um dado observacional ou com a Λ=3/4 do outro fundo.

O setor087 projeta sigma constante ao complexo métrico mínimo. A restrição clássica
φ(x)=φ0 dá ∂φ=0, T_sigma=0 e equação sigma satisfeita para qualquer métrica. Ela é
preservada por difeomorfismos, sφ=c·∂φ=0. Portanto o setor restrito é consistente
classicamente. Não se conclui equivalência com integrar os campos sigma no funcional
quântico da teoria completa.

Um fundo φ0 constante, SEM a projeção, admite ξ em T_φ0 S³, com três componentes.
Em coordenadas normais do alvo, a parte quadrática é

    S_sigma,2 = (c_m/2)∫μ_g g^{μν} δ_ij ∂μ ξ^i ∂ν ξ^j.

O CAS confere essa Hessiana numa carta explícita (sqrt(1−t²|ξ|²),tξ), que tem a mesma
derivada tangente e Hessiana de ação on-shell da carta exponencial nessa ordem. Não
se identifica essa carta com Exp em ordens superiores. A Hessiana temporal é c_m I3.
Assim, manter o fundo constante não apaga três propagadores. Um determinante de
matéria eventualmente obtido integrando-os não é, em geral, uma constante métrica;
essa integração não foi feita aqui.

## 2. Hessiana métrica e ghosts

Seja I_tr h=h−g tr(h)/2; I_tr²=id em4D. De Donder Cν(h)=∇μ(I_tr h)μν.
A fonte066 dá H_gf=(2κ)⁻¹[−□I_tr h/2+L_R h+Λh], com C*=−D,
ell=1/(2κ), e H_gf=H+ell C*C. Nas convenções acima,

    R_μρνσ h^{ρσ}=K(g_μν tr h−h_μν),
    L_R h=−2K h+(K/2)g tr h,
    B=−I_tr/(4κ),
    P=B⁻¹H_gf: P h=□h−2K h+2K g tr h,
    Q=CK: Qv=□v+3Kv.

Aqui o K da curvatura não é o mapa de gauge K_gauge(v)=L_v g nem o gerador modular.
O CAS calcula o endomorfismo de ordem zero sobre as dez componentes: −2K no setor
sem traço (multiplicidade9), +6K no setor de traço (multiplicidade1). Isto NÃO é o
espectro global da EDP, não escolhe estado e não prova estabilidade/positividade.
Os inversos de H_gf devem conservar B: G_H=G_P B⁻¹.

Em símbolos principais, com p covetor arbitrário, C(K_gauge v)=p²v,
δG_pr(K_gauge v)=0 e o termo de gauge cancela a parte não mínima. O CAS verifica
essas identidades como polinômios, sem impor p²≠0. A Ward diferencial com curvatura
é a identidade escrita da fonte; não foi substituída por essa verificação principal.

Na ordem(c,barc), Hessiana Grassmann e inverso são respectivamente
[[0,−Q],[Q,0]] e [[0,G_Q],[−G_Q,0]]. A multiplicação formal preserva os contatos
QG_Q=G_QQ=id. O teste matricial não constrói G_Q nem uma extensão renormalizada.
Antifields continuam fontes externas sem propagadores; auxiliar b não ganha laços.

## 3. O contrato do cálculo que ainda falta fixar

A7.b exige uma prescrição temporal antes do coeficiente de quebra, não apenas esses
operadores livres. A escolha de referência Hadamard/Wick, extensões às diagonais,
escala e termos locais finitos, junto de T10/T11 e contatos, ainda deve ser registrada.
Somente então se pode extrair a primeira ordem em ħ, ghost1/forma4, e conferir
sa_N+d_H b_N=0 no complexo correspondente. Nenhum coeficiente de anomalia foi
calculado nesta etapa. A existência de H4(s) clássico não fornece tal coeficiente.

[KNOWN — leitura primária delimitada] Hollands, §§3.4–3.6 e Teorema2, fornece exemplos
de extensão analítica e descreve a liberdade por uma hierarquia local D_n; não fixa
uma escolha única para este teste gravitacional. Seu exemplo escalar tem fatores
numéricos suprimidos, portanto não será copiado como coeficiente gravitacional.
Fonte: https://arxiv.org/html/0705.3340v4 (lido24/09/2026).
O HTML de Fröb1803.10235v3 consultado está truncado no início da seção2: os
Teoremas3/6/7 não foram verificados nessa consulta e permanecem remissões das fontes
locais, não uma nova leitura primária completa.

Não houve alteração de um.py/kernel/gate, prova Lean nova ou transporte ao fundo
físico sigma=id. Estes dados preparam a prescrição; não satisfazem sozinhos A7.b.
