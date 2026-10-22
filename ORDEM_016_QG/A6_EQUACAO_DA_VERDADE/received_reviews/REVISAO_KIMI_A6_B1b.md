[REAL — comparação com prova compilada existente; DECLARADO — esqueleto do Kimi]
# Revisão local Kimi A6.B1b

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T22:51:36.330146+00:00.
Resposta integral lida: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A6_EQUACAO_DA_VERDADE\received_reviews\46bc7f7d-0b2c-4238-892e-e9280a95cfd3.md`, SHA256 `8841fb4a03519a1173aa8c3ce2700778c653d4afd15d2726c177db35d24db17a`.
Execução única `81989b2b-358b-4902-bd17-c5cbfc9ab870`; uso informado no recibo, sem nova chamada.

O argumento por base ortonormal e Parseval preserva a constante1 e coincide
com finite_gap_norm_rate em FiniteGapRate_v2.lean. Ali o gap pertence aos mesmos
eigenvalues da base; projeta fora o kernel, inclui H=0/dimensão0, e exige s>=0,
γ>0. A positividade extra do parecer é redundante com a hipótese do gap.
Igualdade de norma para todos s requer gap atingido e complemento não nulo;
em s=0 isolado ela não identifica o gap. O fluxo dissipativo não é modular unitário.

Recibo local existente rc0; fonte `6e8b6225c9e9e56a4ecedc38337f48da365cc09a0422390227ee23fb020a754f`, log `f5e8a9b3c537cbb4fd985ca955f6cced76373a02d99c8421efc434394fead677`, auditoria3/3,
somente propext/Classical.choice/Quot.sound, zero sorry. Conferidos em disco,
sem nova compilação nesta rodada. Reutilizar essa prova, não criar novo módulo.

O esqueleto Kimi não está compilado, lista APIs candidatas e tem sorry explícito
na extensão opcional. No ramo hF1, após reescrever b_i=0, h1 fica0=1; o uso
one_ne_zero h1 tem orientação incorreta. A contradição seria zero_ne_one h1,
ou one_ne_zero h1.symm. Não transplantei esse código nem substituí a prova pronta.
Parecer útil como conferência independente escrita, não certificado de kernel.
