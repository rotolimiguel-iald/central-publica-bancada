[DERIVED — vértice principal; REAL — CAS exato; OPEN — contribuição quântica completa]
# A7.b — Hessiana e vértice cúbico métricos

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. Data UTC 2026-09-24T22:25:49.596164+00:00.

Usamos g=delta+h com h covariante, Fourier exp(+ipx), contrações euclidianas
do símbolo principal. A ação -sqrt(g)R/(2κ) é escrita em Gamma-Gamma módulo
divergência SOMENTE com cutoff constante. C=div(h)-d tr(h)/2 é linear e a
fixação +C²/(4κ) não acrescenta vértice cúbico. A transferência dos sinais
ao problema Lorentziano e contatos de derivadas do cutoff permanece separada.

O motor metric_principal_vertices.py retorna 16κ vezes a derivada cúbica da
ação, sem divisão adicional por3!. A conferência quadrática recupera
H_gf=p² I_tr/(4κ), inclusive a multiplicidade2 das componentes fora da diagonal.
Oito exemplos da identidade clássica cúbica verificam V3(Kv,H,J)+
V2(L_v H,J)+V2(H,L_v J)=0; quatro são não triviais. Isto é verificação exata
desses exemplos, não certificação automática de toda identidade polinomial.
Também foram conferidas seis permutações de Bose, dez direções de gauge na
Hessiana sem gauge e a família conforme, 16κ V3(I,I,I)=12Σp_i².

Comando Python314 -X utf8 -B A7/metric_vertex_check.py; rc0.
81 verificações e dois controles negativos; wall 0.008968000009190291s,
CPU 0.015625s. Resultados, plano anterior e log no manifesto.
Nenhum dado de curvatura, coeficiente ghost1 ou QME foi certificado aqui.
