[OPEN — roteiro local a formalizar; não é declaração de compilação nem resultado do MiMo]

Continuação exata de A2.3.a, após core_transport_manifest.json. Não criar nova rota fora da árvore.

Para b>0 fixo, f_r(x)=exp(-b(x-r-iπ/2)^2). A fórmula a conferir em Lean com fourier_gaussian_pi' e a translação já disponível é
F f_r(p)=g_b(p) exp(-2πirp), g_b(p)=sqrt(π/b) exp(-π²p²/b+π²p).
g_b é estritamente positiva, real e L²; c=2π² dá g_b(-p)=exp(-cp)g_b(p).

Se h pertence ao K já construído e é ortogonal REAL a todos os f_r, H=Fh satisfaz H(p)=exp(cp) conj(H(-p)) quase sempre. A passagem de pertença a esta identidade deve usar continuous_standard_fixed_iff e continuous_tomita_apply_ae, não um K redefinido.

Definir q(p)=conj(H(p))*g_b(p). q é L¹ por Cauchy–Schwarz. Ortogonalidade real dá Re(Fq(r))=0 para todo r. Seja qsharp(p)=conj(q(-p)); é L¹ por reflexão/conjugação e F(qsharp)(r)=conj(Fq(r)). Logo F(q+qsharp)=0. V350FourierUniqueness.fourier_integral_ae_injective fornece q+qsharp=0 quase sempre.

As duas relações de reflexão acima dão qsharp(p)=exp(-2cp)q(p); assim (1+exp(-2cp))q(p)=0. O fator é positivo, g_b também: H=0 e h=0. Não exigir integrabilidade isolada de exp(-2cp); o produto qsharp é integrável pela reflexão.

Fecho final: L=closure(span_real{f_r}) está contido em K pela pertença já compilada e pelo fechamento de K. No Hilbert REAL, para h em K, h-proj_L(h) pertence a K e ao ortogonal de L, portanto é zero pelo argumento anterior. Concluir K⊆L e fornecer hdensity a halfline_isotony_of_gaussian_density.

Obrigações ainda não compiladas: fórmula gaussiana e sua positividade/L²; conjugação-reflexão Fourier e integrabilidade do produto; transferência das relações ae; ligação da ortogonalidade real à integral; argumento de projeção fechada. Reutilizar fontes nomeadas, não pressupor densidade nem meia-inclusão. Este roteiro é da bancada local; a chamada MiMo terminou IncompleteRead sem resultado recuperável.
