[DERIVED — identidade principal de ghost constante; REAL — CAS exato; OPEN — ghost variável e Q2 finita]
# A7.b — completar todas as polarizações do ghost constante

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T00:11:38.588781+00:00.

O ajuste do representante Z preservou as64 componentes simbólicas da
identidade do bracket já obtida. O sistema combinado tem posto15 em21
coeficientes; seis parâmetros livres foram postos em zero. Isso é escolha
de representante, não unicidade/canonicidade. Os coeficientes e suas bases
estão registrados em constant_ghost_completion/results.json e no script.

Fixados esses coeficientes ANTES do ensaio completo, verificamos

    R1(H,p;0,v) = -K_p Z_new(H,p;0,v) + (p·v) B(E_p H),
    B(A) = -A/6 - I tr(A)/12,
    E_p H = p² Itr(H) - Itr(K_p C_p H).

Aqui K_p v=pv^T+vp^T, C_p H=Hp-p tr(H)/2, Itr(H)=H-I tr(H)/2.
Normalização: R1=G-M/4 após retirar4iκA0, A0=1/(8π²), como nos
vértices anteriores. E é4κ vezes a Hessiana física livre, não a Hessiana
gauge-fixada. O termo B(E) é justamente a contribuição de equação de
movimento permitida pela primitiva de antifields deslocados já construída.

Cobertura:10 polarizações simétricas H ×10 fontes simétricas T ×4 vetores v,
p=e0, momento do ghost zero. 40 componentes não nulas,
400 comparações exatas, zero diferenças. Não se impôs transversalidade a H
nem paralelismo entre p e v. Covariância O(4) e homogeneidade cúbica dos
dois lados estendem o resultado a qualquer p Euclidiano; p=0 segue por
continuidade polinomial. Não se deduz daí uma extensão Lorentziana causal
ou uma escolha do estado físico sem verificar essa ponte.

Com ghost constante, Z_new é

    -v trH p²/8 + v(p·Hp)/12 + (Hv)p²/4
    -(Hp)(p·v)/12 + p trH(p·v)/6 - p(v·Hp)/6.

O ensaio usa o mesmo motor de vértices previamente auditado. As400
comparações verificam a nova decomposição; não constituem400 avaliações
independentes do motor. Não houve compilação Lean nesta etapa.
CPU do ajuste: 8.5s; CPU do ensaio: 77.1875s;
paredes: 8.548890600039158s + 77.72153049998451s. Ambas execuções rc0.

Próximo passo na mesma A7.b: calcular o polinômio principal completo com
momento do ghost não nulo e medir o resíduo da candidata BV. A ação
completa, termos curvos, realidade e anomalia causal finita continuam OPEN.
Nenhum original, kernel ou gate modificado.
