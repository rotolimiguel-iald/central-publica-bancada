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

[REAL — coeficientes principais exatos; MEDIDA — cancelamento pretendido não obtido; OPEN — Ward completa]
# A7.b — bolha métrica e diferença longitudinal medida

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. Data UTC 2026-09-24T22:25:49.596164+00:00.

Prescrição anterior ao cálculo: mesmo extrator radial log Λ_UV, denominadores
q²(q+p)², símbolo principal euclidiano. W_A=16κ V3(A,p,E_i,q,E_j,-p-q).
Na base simétrica de dez componentes, S0 é a inversa da forma I_tr: bloco
diagonal I4-ones4/2, seis entradas1/2 fora dele. Logo G_h=4κ S0/q² e
N_m=Tr(S0 W_A S0 W_B)/16. W é reconstruído por quinze avaliações inteiras
de um polinômio quadrático; uma avaliação fora dos nós confere cada matriz.

Na ordem trAB*p4, trA*trB*p4, (pAp*trB+pBp*trA)*p2, pABp*p2, pAp*pBp,
os coeficientes sobre A0=1/(8π²) foram:

    métrica: ['53/30', '23/60', '-3/10', '-101/30', '31/15']
    ghosts:  ['1/12', '7/48', '-1/8', '-1/12', '1/6']
    -métrica/2+ghosts: ['-4/5', '-11/240', '1/40', '8/5', '-13/15']

A combinação é a hipótese de normalização da Hessiana derivada formalmente de
Gamma1=(ħ/2)Trlog H-ħTrlog Q, antes da fase Lorentz. Não foi ajustada após o teste.
Para p=e0, A=B=E00, a peça métrica vale A0/4 e a ghost A0/16: a soma vale
-ħ A0/16. Usando K(e0)=2E00, a contração dupla vale -ħ A0/4; as outras nove
contrações de base são zero. Portanto o critério pretendido de cancelamento
duplo NÃO foi satisfeito por esta soma. Não é legítimo declarar anomalia:
faltam conferir identidade adequada, normalizações, termos/inserções BV e
contatos da prescrição. O resultado não contém cálculo de ghost1/forma4.

Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/metric_bubble_check.py;
rc0 significa que o cálculo e seus 65 checks terminaram, NÃO que o cancelamento
passou. Foram conferidos 55 pares tensoriais e dez interpolações fora dos nós.
Wall 7.56341830000747s, CPU 7.515625s.

Correção ao lado: o negativo wrong_relative_determinant_sign testa apenas
não nulidade, que também ocorre com o sinal proposto; não discrimina o erro.
O outro negativo apenas impede apagar a peça métrica não nula. Não anunciar
dois detectores de erro físico independentes. Errata preservada no manifesto.

Próximo passo: verificação independente do vértice/integração e da identidade
longitudinal com fontes BV; só então combinar curvatura, cutoff e normalizações
finitas. O Kimi recebeu uma unidade preparada especificamente para a identidade
e fatores, anterior a este resultado, sem ajustar seu payload depois da medida.
Nenhuma mudança no um.py, kernel, gate ou no modelo físico canônico.
