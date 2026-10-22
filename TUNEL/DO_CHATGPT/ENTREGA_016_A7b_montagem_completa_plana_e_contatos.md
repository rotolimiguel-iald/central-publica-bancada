[DERIVED — montagem plana e contatos medidos; Q2 completa OPEN]

Oito controles previamente registrados, com h diagonal/não diagonal, c0..c3,
pontos não axiais e jatos exponenciais de ambos os cutoffs, cancelam exatamente
após incluir correntes emX eY. Os pesos vêm da ação/Wick e não foram ajustados.
Isso amplia a evidência; oito controles não são prova de uma identidade universal.

Na prescrição radial já fixada, R=FP[(1-a)mu^(2a)z^a], foram calculados os
contatos da correnteX com os mesmos jatos externos atéh''. Quatro polinômios
(dois tensores, dois ghosts, dois diagramas) coincidem entre tabela de C_D e
diferenciação direta do regulador. Esta segunda rota conserva apenas a parcela
linear ema PORQUE aqui os kernels são racionais com polos simples; não se
exporta essa simplificação aos logaritmos.

No controle h11,c0,q=(1,2,-1,1), a montagem de todos esses contatos dá,
para(lambda,eta)=(0,0),(0,e0),(e0-e1,e0), respectivamente:
5341/1920,48317/7680,75977/3840, em unidades deC_E=-4pi².
Os números antigos avaliados emq=(2,1,0,0) não eram o mesmo controle.
Nenhum contato não nulo foi removido por ajuste ou chamado de anomalia irremovível.

Foram calculadas as40 componentes h_A c_r paralambda=e0-e1,eta=e0 e,
separadamente, as40 com os cutoffs trocados. No primeiro conjunto, a parte
homogênea de grau5 emq recupera EXATAMENTE os três coeficientes anteriores:
a=-139/1920,b=217/960,c=99/1280 na base
delta_ab q_r q4, q_a q_b q_r q2,(delta_ar q_b+delta_br q_a)q4.
Componentes externas não diagonais recebem o peso2 da contração tensorial.
A variação BRST dessa parte é zero por igualdade polinomial nas16 entradas.
Isso reencontra a primitiva plana já existente, sem criar novo teorema por nome.

O representante localizado completo tem defeito de adjunto graduado no setor
h/c isolado. Antes da polarização, a entrada01 emq0 é697/1920; a matriz do
defeito é antiautoadjunta com o peso exp((lambda+eta)X), conferido exatamente.
Testou-se então a polarização par FIXA (A(lambda,eta)+A(eta,lambda))/2;
resultado: fechado nesse setor=False,
entradas não nulas=16,
entrada01 emq0=8293/3840.
Não se escolheu sinal conforme o resultado. A próxima análise deve identificar
os termos de descida/correntes/normalização ainda necessários ANTES de atribuir
classe de cohomologia à quebra. Não se promove esse setor a Q2 completa.
Curvatura do espaço-forma, partes suaves/tadpoles, outras aridades e realização
causal/lorentziana continuam com seus escopos registrados, não presumidos pagos.

Falha operacional preservada: metric_current_insertion_engine_v2 usava int0
na soma vazia e falhava em.subs quandoeta0. V3 muda somente paraInteger(0).
Nenhum coeficiente físico mudou; comando/log falho e sucessor estão no manifesto.
O primeiro testeMiMo parou no desacordo real de resíduo;v2 preserva o desacordo
em resultado estruturado e lista os coeficientes divergentes, sem corrigi-los
para concordar com o modelo.

1136 verificações algébricas/auditorias, além dos8 controles e80 componentes
de contato calculadas;CPU medida dos scripts concluídos=550.140625s. As contagens
incluem verificações de contraexemplos: não significam que todo parecer passou.
Custo externo conhecido parcialUS$1.7035941618, estimado/não fatura; assinatura Kimi
sem custo alocado. Originais,um.py,kernel e gate inalterados.
Abertura sha256:216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
