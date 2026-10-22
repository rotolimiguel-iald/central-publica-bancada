[REAL — conferência local do parecer; DECLARADO — texto externo; DERIVED — correções]
# A7.b — revisão Kimi métrica aproveitada com correções
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:52:46.462755+00:00.
Job2177daf6-29db-4d0c-940a-63d4c582fa04; execução2b2ea20e-990e-4410-ae1d-e9bf1a630e05.
Resposta inteira lida: received_reviews/2177daf6-29db-4d0c-940a-63d4c582fa04.md,
SHA256 `1a63814dceb77980ffc4a55980f2c65f37fa631e8c0144f506114508e8a7e42a`.

O parecer oferece derivação útil da contração transposta, aritmética dos cinco
coeficientes, identidade longitudinal principal e expressão em Ric/R. Esses
resultados já tinham CAS local; não são novas provas apenas por concordância.

Correções verificadas nesta rodada:

1. O contraexemplo E01/E01 em p=e0 alegado como -61/240 vale **zero**.
E01=K_p(e1) é longitudinal. E11/E11 vale -7/10, como o parecer diz.
2. Nossa frase antiga "dez contrações duplas de base" era imprecisa. O código
metric_bubble_check_v2.py:111–117 testa os dez pares não ordenados de QUATRO
imagens K_p(e_nu), não os dez elementos gerais da fibra simétrica. A correção
de redação fica ao lado, com a fonte anterior preservada.
3. Cancelamento determina somente a razão dos pesos, não sinal global nem
normalização. Além disso, os pesos da Hessiana de Gamma não são os mesmos
do próprio Tr log: delta²Trlog=-Tr(G deltaQ G deltaQ) para Q linear. Assim,
Gamma=(hbar/2)Trlog H-hbar Trlog Q dá a Hessiana -métrica/2+ghost, exatamente
a convenção da fonte. A afirmação F=-Gamma/hbar no parecer confunde a ação
com seu segundo diferencial. O teste escalar exato confirma os dois sinais;
fases Lorentz completas continuam separadas como antes.
4. A seção9 troca sbarc para+b, enquanto BV069:79,96 fixa **-b**. Também
escreve sh=L_c h como se fosse a linearização; ela inclui K_gauge c.
5. Pedir F_K(K_pv,H)=0 isoladamente não é a identidade curva completa.
O setor h*c e os comutadores entre ordens contribuem. O termo fonte já
medido K_gauge(Fv)+2K g divv, cuja imagem por E é não nula, ilustra a
omissão sem exigir recalcular o laço plano.

15 checks novos,rc0,CPU 0.046875s; nenhuma bolha antiga
recalculada. Parecer e fontes originais intactos. Essas correções não anulam
o cancelamento principal calculado nem fecham Q2. Custo Kimi não informado
pelo recibo, portanto não registrado como zero. Uso318260entrada/34621saída,
310528cache/352881total, recuperado da execução, sem nova chamada.
