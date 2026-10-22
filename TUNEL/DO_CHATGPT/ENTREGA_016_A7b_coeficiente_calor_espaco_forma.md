[DERIVED — coeficiente local de calor no fundo fixo; REAL — CAS exato; OPEN — variações curvas e anomalia]
# A7.b — contribuição livre de curvatura K²

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T23:23:17.580934+00:00.

Calculamos o símbolo de calor Riemanniano auxiliar D=-(∇²+E) associado aos
operadores mínimos já extraídos no espaço-forma4D da087, Λ=3K, sigma projetado.
E_m h=-2Kh+2Kg trh, E_g v=3Kv. Sob esta continuação local, H_E=(I_tr/4κ)D_m
e Q_E=-D_g. O cálculo abaixo é dos dois operadores D; não escolhe estado
Euclidiano/Lorentziano, não integra modos zero nem define a fase do determinante
da Hessiana métrica indefinida. K não é o gerador modular nem um dado observado.

## Derivação radial, sem importar a fórmula universal de a4

Em coordenadas geodésicas, f(r)=sin(sqrt(K)r)/sqrt(K) e o Laplaciano escalar
radial é ∂r²+3(f'/f)∂r. Inserir (4πt)^-2 exp(-r²/4t)Σt^j u_j na equação
do calor dá a recorrência de transporte. Para u_j=u0 a_j:

    u0=(r/f)^(3/2)=1+Kr²/4+19K²r4/480+…,
    r a_j'+j a_j=u0^-1 Δ(u0 a_(j-1)).

Segue a1=2K-K²r²/60+…; u1=2K+29K²r²/60+…;
u2(0)=Δu1(0)/2=29K²/15. O CAS deriva a recorrência da EDP antes de usá-la.

Na trivialização ortonormal por transporte radial, x·A=0 e trA=0.
A_mu=(1/2)x^nu Ω_nu,mu+O(x²). Na contribuição ao TRAÇO de u2, os termos
lineares em A/derivadas têm traço zero; A·∂u0=0; a parte quadrática dá
tr u1_conn=trΣA_mu²/3 e tr u2_conn=ΔtrΣA_mu²/6=trΣΩ_mu,nu²/12.
Correções da métrica a A² começam na ordem r4. Esse argumento é para o
traço diagonal nesta conexão métrica paralela, não uma fórmula matricial
completa para qualquer conexão. E é paralelo; o fator exp(tE) produz
2K trE+(1/2)trE². Sua compatibilidade com a conexão foi checada.

Logo, na convenção K_D(t;x,x)~(4πt)^-2[I+t a2+t² a4+…],

    tr a4 = rank*29K²/15 + 2K trE + trE²/2 + trΩ²/12.

## Valores medidos

| fibra | trE | trE² | trΩ² | tr a4 |
|---|---:|---:|---:|---:|
| S²T* | -12K |72K²|-144K²|58K²/3|
| T* ghost |12K|36K²|-24K²|716K²/15|

Assim o peso de determinantes Γ1=(1/2)TrlogD_m-TrlogD_g dá

    (1/2)tr a4_m - tr a4_g = -571K²/15.

O peso de rank é1; o de a2 é-16K. A conexão contribui-4K² ao peso de a4;
trocar os tensores por escalares apagaria exatamente essa contribuição.
O coeficiente do calor não é, por si, um coeficiente de anomalia BRST.

rc0,29checks,3controles negativos; CPU 0.453125s, wall
0.4538417999865487s. Conferidos trΩ² anteriores, fator espectral exp(tE),
signos, rank e pesos. Preservados código/plano/resultado/log no manifesto.

Este é um dado local SEM pernas externas no fundo on-shell fixado. Não
podemos diferenciar a família minimal on-shell para inventar a Hessiana
da ação efetiva em gauge de fundo fixo: termos proporcionais às equações
de fundo e vértices de curvatura ainda precisam entrar. Não demonstra
renormalizabilidade UV, não paga Q2 e não move o gate.
