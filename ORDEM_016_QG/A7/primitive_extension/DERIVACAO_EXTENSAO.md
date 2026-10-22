[DERIVED — extensão primitiva; REAL — CAS algébrico; OPEN — produtos completos e anomalia]
# A7.b — primeira extensão não linear com normalização explícita

Abertura sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

## Convenção fixada antes do cálculo

Assinatura +---, z=x²−i0, □=∂t²−∑∂i². μ_R>0 é uma escala de referência fixa,
mantida simbólica; não é ajustada após observar Ward. Para a distribuição z^−2
fora da origem, escolhe-se

    R2 = −(1/4) □ [log(μ_R² z)/z],

sem adicionar termo delta finito. O kernel log(z)/z tem grau de escala2,
portanto sua extensão à origem é única; a derivada é distribucional. A
escolha é Lorentz-covariante. O CAS verifica a identidade radial longe da
origem: □F(z)=4z F''(z)+8F'(z). Não verifica frente de onda nem existência
distribucional por amostragem numérica.

[KNOWN] Hollands, §3.4, eq223–227, constrói a extensão pelo termo finito de
uma família meromorfa. O texto omite fatores numéricos no exemplo; os nossos
coeficientes são calculados na convenção acima. No fim de §3.3, T10/T11 ainda
exigem ajustes da extensão. Portanto essa conta não certifica todos os produtos.
https://arxiv.org/html/0705.3340v4

## Derivação dos coeficientes e do contato de escala

A identidade radial fornece, antes de tomar a parte finita,

    U_a = (μ_R²)^a z^(−2+a)
        = □[(μ_R²)^a z^(−1+a)]/[4a(a−1)].

O kernel dentro de □ tem expansão

    −1/(4a z) − [1+log(μ_R²z)]/(4z) + O(a).

Logo a parte finita analítica e a escolha diferencial são diferentes:

    FP U_a = R2 − (1/4)□(1/z).

O contato pode ser normalizado sem importar o prefator suprimido da fonte.
Fixe a transformada inversa com exp(−ipx)/(2π)^4. O inverso de □ tem
transformada −1/(p²+i0), de modo que □G0=δ0. O contorno em p0 no ponto
t=0 dá i/(2|p|); a transformada espacial de 1/(2|p|) é 1/(4π²r²).
A expressão Lorentz-invariante correspondente é G0=−i/(4π²z). Assim

    □(1/z) = 4iπ² δ0,
    Res_(a=0) U_a = −iπ² δ0,
    FP U_a = R2 − iπ² δ0,
    μ_R dR2/dμ_R = −2iπ² δ0.

A identidade de contorno/boundary value é uma derivação escrita; o CAS usa
esse contato como entrada analítica e verifica os coeficientes resultantes.
Para o quadrado do inverso principal G0, sem os fatores Wick iħ nem pesos
dos vértices, isso dá

    μ_R d[R(G0²)]/dμ_R = i/(8π²) δ0.

É um contato de ESCALA do kernel primitivo, não uma anomalia Ward/BRST.
Curvatura, tensor B^−1, ghosts e todos os vértices ainda entram na contração
real da teoria. Este G0 é o inverso principal plano usado na expansão local;
não substitui o Green exato do fundo curvo.

Para n>=3, a mesma escolha se prolonga por

    Rn = □R_(n−1)/[4(n−1)(n−2)]
       = −□^(n−1)[log(μ_R²z)/z]/[4^(n−1)(n−1)!(n−2)!].

O CAS verifica n=2,...,5. Isso é uma família radial, não autorização para
renormalizar todo produto tensorial escolhendo decomposições arbitrárias:
as identidades entre decomposições, diagonais parciais e T10/T11 ainda precisam
ser conciliadas. A condição linear de Fröb já fixada permanece exigida.

## Verificação e alcance

Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/primitive_extension_check.py`.
rc0 observado; 11 checks e 3 negativos passam, Sympy 1.14.0.
wall 0.18896810000296682s; CPU 0.171875s. Resultado estruturado direto;
sem arquivo stdout independente. Plano anterior à execução; manifesto com hashes.
Não houve CAS de distribuições, renormalização de todos os grafos, coeficiente
Ward completo, novo Lean ou alteração do gate. Próximo trabalho: extensão
tensorial compatível com os contatos e a hierarquia, antes da soma da quebra.
