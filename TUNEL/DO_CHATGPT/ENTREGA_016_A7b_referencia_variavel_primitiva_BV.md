[DERIVED — primitiva BV do contato relativo suave variável; Q2 completa OPEN]

2026-09-25T10:46:27.499868+00:00. Abertura SHA256 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

O vértice da fonte agora inclui os primeiros jatos suaves antes omitidos:
além de R_W∂c, há A_Wc. Na família isotrópica dependente de (X+Y)/2:

    A_Ic=-g c·∂wI/2; A_Tc=+g c·∂wT/4;
    A_Gc=-(c⊗∂wG+∂wG⊗c)/16.

A bolha foi calculada antes de mover derivadas pela referência. O tensor
métrico I contém96 componentes com parte antissimétrica nos índices de
derivada, invisível no símbolo de w constante. Com w=x1 e h00=x0, omitir
essa parte perde1/8 na saída01. Conservá-la fornece a Hessiana real
N_w=-div(w T grad), com pesos de fibra explícitos. O ghost é zero nesse
contato; a fonte ghost variável não é omitida.

A ligação usa o antifield já existente no BRST:

    B_W=-C_E integral(1/2 h.N_w h+hdagger.R_W c),
    s0B_W=-C_E integral h.(N_wG+E R_W)c.

Isso dispensa fatorar toda R_W por G. As correntes de integração por
partes foram escritas e verificadas localmente; nenhum termo de corte
foi declarado zero. No caso constante, B_W e a primitiva métrica anterior
diferem por -C_E s0 integral hdagger.L_W h, ligando as duas construções.

Controle: w=x0³-3x0x1², c=e0 dá Gc=0, mas E R_Ic=diag(6,-6,0,0).
Portanto uma primitiva apenas métrica perde o termo; a BV o produz.
Não se promoveu esse jato formal a estado físico/BRST-compatível.

Evidência: 11928 verificações, CPU11.671875s, três comandos rc0.
Nota completa: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A7\smooth_variable_bv\DERIVACAO.md.
Manifesto: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A7\variable_smooth_delivery\manifest.json, SHA256 57598eedb8dbb753d8acb84362393efcbf0b10f8e36b9664e9eae9b97257966c.

Alcance: contato relativo de duas pontas, plano auxiliar, família suave
isotrópica dependente do centro; fórmulas da fonte admitem jatos gerais.
Restam curvatura, referência admissível geral, outros locais/aridades,
continuação causal e Q2 completa. Não adotado contratermo; gate intacto.
Próximo: verificar o transporte da referência e combinar com os termos
curvos já medidos, preservando a revisão independente em andamento.
