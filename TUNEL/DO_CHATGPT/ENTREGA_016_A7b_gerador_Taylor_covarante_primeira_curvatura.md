[DERIVED — gerador exato em K1; REAL — CAS; OPEN — amplitude integrada]
# A7.b — soma dos jatos, preservando a ordem
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T07:11:27.051220+00:00.

No mesmo campo radial v_a(x)=[delta_a^b-K(z delta_a^b-x_a x^b)/6]
v_b exp(p.x)+O(K²), derivamos uma expressão fechada para

    sum_n D_y D_x^n D_i G(v)/n! = exp(p.x) (P0+P1+P2) +O(K²),

onde Pj é homogêneo de grau j em x. D_y/D_i são mantidos quando o vértice
os exige. p é formal REAL nesta fórmula; as fases i são restauradas por
grau homogêneo antes da integração. Não identificamos boost com rotação.

**Derivação para todo n.** Em K1, a expansão de uma palavra de derivadas
recebe: (a) a segunda derivada do coframe, escolhendo dois lugares;
(b) uma derivada de Gamma atuando no índice final, escolhendo dois lugares;
(c) uma derivada de Gamma atuando em outro índice de derivada, escolhendo
três lugares ordenados. Os demais lugares dão fatores p. Ao selecionar k
lugares do bloco radial de tamanho n, a multiplicidade é binomial(n,k).
Dividir por n! e somar n dá exp(p.x)/k!. O termo de grau3 é zero porque
d_x Gamma(x,x)=0 na carta normal do espaço-forma. Assim restam graus0..2;
não é ajuste de uma série truncada nem hipótese de momento comutante.

Conferência: palavras ordenadas com comprimentos1,3,5 contra a recursão
covariante anterior; gerador contra palavras até comprimento radial8,
dez fibras, duas escolhas de p/v e quatro disposições de índices dos
vértices. 1728 controles, rc0, CPU5.265625s.

**Integração necessária:** os primeiros termos curvos têm grau angular
até6. Sua projeção harmônica exige momentos até12. A regra anterior, grau8,
não pode ser reutilizada como prova dessa integração. Construímos uma regra
exata por nove órbitas de vetores inteiros, 432 nós, pesos
racionais (alguns negativos). Todos os 1820 monômios até grau12
foram conferidos; simetrias de sinal verificadas para os ímpares.
CPU0.046875s, rc0. Os pesos não são probabilidades.

Uma execução separada está usando estes objetos e multiplicadores de
Laurent que preservam l>m. Seus resultados não integram esta entrega:
curved_pair_fourier_check.py, sessão própria93180, ainda não terminal
na última consulta. Nenhuma amplitude completa ou Q2 é declarada paga.
