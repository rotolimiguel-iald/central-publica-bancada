[DERIVED+CAS — confronto adversarial MiMo C6; candidato original preservado]

Abertura SHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

MiMo propôs resíduo −2K H0/3 e alteração do potencial de−2K para−4K/3.
A auditoria diferencia literalmente sua conexão de Christoffel:
sum_i partial_i Gamma^m_ia = −delta_ma em dimensão4, não−2delta_ma/3.
Assim, os dois índices covariantes dão+2K H0, não+4K H0/3.
A diferença é exatamente o resíduo que a resposta afirmava existir.
Também S_00,11=−1/2; o controle que a resposta dizia isolar só o traço
não tem S=0.

Verificamos novamente200equações, agora mantendo x e y arbitrários até
o fim, nas duas pontas e nos100componentes independentes. Todos os
resíduos são zero. O potencial sugerido pelo modelo introduziria
+2K H0/3: falha explícita, não adotada. A densidade não é aferível por
esse teste fora da diagonal; permanece auditada no contato da bancada.
Controles totais:219; CPU32.421875s; comando audit_mimo_parametrix_v2.py, rc0. A primeira auditoria parou numa asserção de denominador: antes de impor w=(x-y)² a expressão tem polo de ordem4, não3. Mantida a tentativa falha; corrigido apenas o multiplicador de teste.

A resposta fica integralmente preservada, estatuto DECLARADO; a correção
é ao lado. Não ajustamos H0,H1, esquema ou operador. Não é loopQ2 completo,
continuação lorentziana nem alteração do gate. Custo MiMo medido no recibo
USD0.25467684; contabilizado uma vez.
