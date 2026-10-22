[REAL — duas falhas locais distintas, preservadas e diagnosticadas]
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
v1, comando symbolic_runtime/Scripts/python.exe -X utf8 -B A7/finite_antifield_contact_check.py,
rc1: bool*Symbol recusado pelo Sympy. LogSHA256 `5f82b5592311e9f6c9eec62489f152214cda1b017e69c235a8770d869d5808bb`.
v2 substituiu deltas booleanos por inteiros. Passou a parte euclidiana e
falhou no teste Lorentziano: faltavam g_ii g_jj g_kk e g_ww dos numeradores
de derivadas de z. Não era falha da identidade física nem licença para
eliminar o controle Lorentziano. LogSHA256 `786022762c378311f9c6d52d902041e1ffafea31edf3a8ae9c63c5c5949e20cd`.
v3 restaura esses fatores, sem mudar a fórmula alvo/coeficientes de entrada;
rc0,138checks,CPU2.625s. LogSHA256 `7b2188ac08842a7726b5b8fd484709ec980899526aca50b95350d2c5e0e8a190`.
Cada tentativa tem script/preregistro próprio. Próximo passo: contatos
com cutoff/curvatura e hierarquia causal. Zero novas chamadas de modelos.
