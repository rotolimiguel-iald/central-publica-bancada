[DERIVED — contato da ação métrica; REAL — CAS; KNOWN — normalização linear; OPEN — anomalia]
# A7.b — normalização linear e contato com cutoff na ação Einstein–Hilbert

Abertura sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

## 1. Parte da prescrição fixada antes da conta

Adota-se a condição de normalização para inserções lineares da equação158 de
Fröb, arXiv1803.10235v3. O Teorema9, pp40–43, prova que a liberdade finita pode
implementá-la. A indução envolve número total de campos e aridade; não basta
zerar um coeficiente isolado. O Teorema8 usa essa condição para uma inserção
inteiramente dependente de antifields. Ele não elimina vértices mistos.
Os Teoremas3/6/7 e a prova9 foram conferidos no PDF; isso corrige ao lado a
limitação do HTML registrada em model_inputs/DERIVACAO_OPERADORES.md.
Fonte: https://arxiv.org/pdf/1803.10235v3 .

Essa escolha é parcial: fixa inserções lineares relativamente aos produtos
inferiores. Ainda não fixa todas as extensões não lineares, os termos finitos
compatíveis com o contrato072, nem calcula a quebra Ward.

No setor bosônico métrico, chamando H a Hessiana e t um teste tensorial compacto,
a identidade de Green converte essa normalização no contato

    T_(n+1)(F^n,h(Ht)) − T_n(F^n) ⋆ h(Ht)
      = i ħ n T_n(F^(n−1), δ_t F).

Mantém-se o primeiro termo off-shell: não aplicar a equação de campo dentro de T
e apagar o lado direito. A verificação abaixo calcula δ_t F numa família métrica
concreta; não calcula coeficientes quânticos das extensões.

## 2. Família que preserva a variável de perturbação

Tome h=u gbar, gnew=(1+u)gbar, e cutoff χ; Rbar=12K, Λ=3K.
Esta é uma restrição da ação Einstein–Hilbert a métricas, não um modelo quântico
escalar nem uma substituição do propagador tensorial. A variável é linear em h.

Derivação geométrica: para gnew=e^(2φ)gbar, a diferença de conexões é
C^a_bc=δ^a_b φ_c+δ^a_c φ_b−gbar_bc φ^a. Contraindo a diferença de Ricci,
o termo derivativo é −6□φ e o quadrático é −6(∇φ)^2. O CAS confere ambos
com índices Lorentzianos. Substituindo φ=log(1+u)/2 e a densidade (1+u)^2,
a lagrangiana puxada para essa família, por volume de fundo, fica

    Lχ = −χ/(2κ) [(1+u)Rbar −3□u
                  +3(∇u)^2/(2(1+u)) −2Λ(1+u)^2].

O Euler–Lagrange exato, sem descartar derivadas de χ, é

    Eχ = 1/(2κ) [−χ Rbar +4Λχ(1+u)
          +3χ□u/(1+u) −3χ(∇u)^2/(2(1+u)^2)
          +3∇χ·∇u/(1+u) +3□χ].

Em u=0 on-shell: Eχ=3□χ/(2κ); o cutoff impede confundir a equação localizada
com a equação de fundo sem cutoff. A contribuição tem suporte onde χ varia.

Subtraindo graus0,1,2 na MESMA variável linear u, a interação restrita é

    Vχ = 3χ/(4κ) [u/(1+u)] (∇u)^2,
    δVχ/δu = −3/(4κ) [χ(∇u)^2/(1+u)^2
                         +2χu□u/(1+u) +2u∇χ·∇u/(1+u)].

Logo há contato de gradiente do cutoff na interação, enquanto □χ pertence
à parte linear removida. Para o teste t gbar, δ_t V=∫t(δVχ/δu) μbar.
O setor cosmológico nessa família tem apenas graus até2, pois o determinante
é (1+u)^4. Isso não anula vértices cosmológicos de grau7/8 noutras direções;
a família de posto1 da conta de filtração é diferente da família de traço.

## 3. Resultado, correção de escopo e próximo elo

Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/linear_contact_check_v2.py`.
rc0 observado; 15 identidades e 4 controles negativos passam;
wall 1.642552400007844s, CPU 1.640625s, Sympy 1.14.0.
Os vértices3–8 dão exatamente os contatos2–7. O teste recusa perda do cutoff,
troca de sinal cinético e confusão entre contato livre e interagente.
Resultado estruturado direto; não houve captura independente de stdout.

A conta anterior linear_contact_check.py também passou (13/5), mas usa
gnew=e^(2φ)gbar e subtrai o Taylor quadrático em φ. Isso muda a separação
livre/interação. É verificação auxiliar preservada, não a interação original
em h. A versão v2 é a referência para essa separação na família h=u gbar.

Não foram incluídas as polarizações métricas restantes, gauge, ghosts e
antifields nos contatos calculados. Nenhuma alteração de medida funcional
foi deduzida da mudança de coordenada, nenhum laço foi avaliado.
Falta completar a prescrição não linear e extrair a primeira quebra quântica
de ghost1/forma4. A normalização parcial não é uma prova de QME.
Sem novo Lean, mudança de original, gate ou confirmação física.
