[REAL/DERIVED — revisão local; parecer MiMo aceito parcialmente]

Lida a resposta integral. A fórmula P-Q=E_X(chiX K)-C_E(chiX U),
com U=chiY C-(dchiY)B, coincide com a derivação local anterior.
Também coincidem os coeficientes do contato Y, normalizados por CE=-4pi²:
(-1/16,1/6,0). As tabelas de primeira/segunda derivada sem log conferem
com o motor de contatos existente. Não foi calculada uma nova Q2 aqui.

ERRO na seção6 e no resumo8 do parecer: a igualdade
chiX(X) partial^nu delta(X-Y)=chiX(Y) partial^nu delta(X-Y)
é FALSA em geral, inclusive depois de todas as derivações. Suporte na
diagonal não apaga a sensibilidade de derivadas de delta aos jatos.
A regra correta é
f(X) partial_x^nu delta(x)=sum_{alpha<=nu} (-1)^|alpha|
 binom(nu,alpha) (partial^alpha f)(Y) partial_x^(nu-alpha) delta(x).
Contraexemplo mínimo: x delta'(x)=-delta(x), enquanto x(0)delta'=0.
Para f=1+x e teste phi=1+2x+3x²+... perto de0, as respostas são -3 e-2.
Os cinco controles conservam uma função bump idêntica a1 perto do suporte;
não dependem de testes não compactos. A simplificação só vale quando os
jatos adicionais relevantes se anulam, não por ser a etapa final.

A receita de resíduos simples conferida não deve ser estendida
automaticamente a amplitudes logarítmicas com polos duplos: nesses casos
é preciso conservar os fatores do esquema e todas as ordens de Laurent.
Essa ampliação não foi usada na aprovação parcial. O próprio parecer
não executou C_E aplicado à fonte componente a componente; a bancada já
tem esse cálculo anterior. Não refazê-lo nem promover esta revisão a
validação de todos os laços ou de uma prescrição causal completa.
