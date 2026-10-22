[DERIVED — contração geral da fonte suave e companheiro BRST; Q2 completa OPEN]

Data 2026-09-25T10:17:56.475589+00:00. Abertura SHA256 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

O contato suave da fonte foi estendido do controle isotrópico para todos
os 55 componentes algébricos de W_ab|cd no ponto de coincidência.
A contração original do vértice foi conferida em 8.800 coeficientes.
Com S_ar=sum_m W_am|rm, M_jr=grad_j c_r e Omega=(M-M^T)/2, obteve-se

    R_W(M)=L_W(M+M^T)-[Omega,S]/4,
    L_W(H)=-(SH+HS+2W_cross(H)-2W_direct(H))/8.

O contato fatora pelo gerador de gauge simétrico em toda a fibra se,
e somente se, S é escalar. O mapa do defeito tem posto9 e núcleo
gerado pela identidade. Não se exige que W inteiro seja isotrópico.
O termo restante é a parte rotacional da variação da referência.
Isso identifica uma obrigação de transporte, não uma anomalia física.

No caso isotrópico, L_W=aI+b g tr, com a=-(wI+wT)/2 e
b=-wI/8+wT/4, reproduz o resultado anterior. O gerador de ghost-1
F_W=integral hdagger.L_W h fornece o par de ação de ghost0

    s0F_W=integral(Eh).L_W h-hdagger.L_W Gc.

A Hessiana companheira N_W=E L_W+L_W E satisfaz N_W G=E R_W no
recorte testado. É uma construção explícita de companhia BRST para
essa fonte; não foi identificada com a soma dos diagramas suaves.
Não deve ser confundida com a anomalia de ghost1.

## Auditoria do Kimi

A chamada smooth_reference_ward_transport foi recebida e lida. Sua
fórmula com alpha_W somente nas entradas perde hbar*W já para dois
funcionais lineares. A conjugação correta, no modelo bosônico testado,
é alpha_W T_D(alpha_W^-1 F,alpha_W^-1 G). Ela passou em todas as
potências de0a4. Os sinais ghost não foram certificados por esse teste.
Também não se troca o operador gauge-fixado por E_phys sem o elo próprio.

Total local: 9546 verificações, CPU1.53125s; rc0 nos dois scripts.
Controles negativos: perda de hbar*W; diferença-1/4 entre jatos com
o mesmo Gc; omitir a parcela rotacional perde-1/8 no exemplo dado.
Referência/estado físico não foram escolhidos; nenhum W arbitrário foi
declarado bisolução física. Fontes e logs: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A7\smooth_rotation_delivery\manifest.json.

Próximo passo: confrontar esse companheiro com bolhas mistas singular/suave
e com o transporte completo dos jatos. Persistem W geral, outros locais,
K², aridades e continuação lorentziana. Originais, kernel e gate intactos.
