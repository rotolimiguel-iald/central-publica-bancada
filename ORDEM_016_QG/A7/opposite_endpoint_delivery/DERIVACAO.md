[DERIVED — controles exatos da corrente no extremoX; identidade geral/Q2 OPEN]

A montagem anterior incluía correntes emY e tinha resíduo-14928/117649 no
controle h11,c0,x=(1,2,-1,1),lambda=e0-e1,eta=e0, jatos exponenciais completos.
Construímos as duas inserções que faltavam nessa distribuição de pernas:
corrente métrica h_X h_X c_X e corrente b_X h_X c_X, contra Vghost_Y.
O h externo fica emX; o c externo fica emY. Não é uma troca dos rótulos
do cálculo antigo: o ghost da corrente agora contrai com barc_Y.

Convenções fixadas antes da execução:
Cmetric_real=+dchiX.Jraw/(16kappa); GD=-4kappa S f;
Gbh=-G^T(d)f; <c_X barc_Y>=f. O1/2 da Hessiana é cancelado pelas
duas escolhas do h externo. A adjunção dos jatos externos é
prod_i[-(d_i+lambda_i)] prod_j[d_j-eta_j]. Retidos h'' e todos
os fatores de Leibniz; nenhuma normalização escolhida para zerar resíduo.

Resultados exatos no controle não trivial:
* corrente métrica emX:15194/117649;
* corrente mista emX:-38/16807;
* soma:-14928/117649+15194/117649-38/16807=0.
Os dois controles com lambda0 também permanecem zero.
Há350 termos métricos e132 mistos após agregação;46 termos métricos
contêm segunda derivada EXTERNA de h, omitida por um leitor limitado a h,h'.

83 verificações:75 identidades do operador adjunto até
h''/c',6 avaliações por dois métodos (Leibniz em linhas versus derivar
produto explícito),2 controles de dchiX0. CPU5.484375s,rc0.
Isso demonstra os valores e a consistência da adjunção nesses controles;
não prova cancelamento em todos os tensores/pontos, nem extensão diagonal,
curvatura, parte suave, ordens superiores ou QME completa. Gate inalterado.
Próximo: variar componentes/pontos e calcular os contatos da montagem completa.

Orquestração: novas unidades Kimi bd8796b3 e MiMo24ad1812 aceitas em staging
pela coordenação única, após FIFO existente; ambas prévias selecionam o
provedor exigido. Staging não é execução. Kimi218c concluiu; resposta integral
preservada em kimi_smooth_twojet_review, ainda DECLARADO, sem auditoria local.
Consumo desse resultado registrado uma vez no ledger; custo de assinatura
desconhecido, não zero. Custo monetário conhecido parcial recontadoUS$1.4569561218.

Comando:A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/opposite_endpoint_current_check.py.
Log:C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A7\opposite_endpoint_current_run.log;sha256=82b13a1644a595be63484b4a6e38c0658827a6166b39b4213102cf0589b07623.
Abertura sha256:216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
