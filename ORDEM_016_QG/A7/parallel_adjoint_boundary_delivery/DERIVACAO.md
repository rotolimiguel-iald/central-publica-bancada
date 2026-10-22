[REAL — respostas recebidas e verificações locais; conclusões científicas com escopo limitado]

MiMo24ad e DeepSeek70e9 concluíram; recibos e respostas integrais preservados
na bancada e lançados UMA vez por execution_task_id no LEDGER_016.jsonl.

MiMo derivou o mesmo adjunto existente:
 A(I,J)=(-1)^|I|(d+lambda)^I(d-eta)^J.
Sua resposta mantém o sinal cX-barcY positivo, o sinal bX-hY negativo e a
multiplicidade2 dos termos de Leibniz para derivadas iguais. Nove controles
locais passaram, com produtos polinomiais não constantes, derivadas repetidas
e mistas e controles negativos de sinal/omissão. Não criamos outro motor.
Nas linhas de teste da resposta, o símbolo de adjunto precisa ser conservado:
derivada original e derivada adjunta não são literalmente o mesmo operador.

DeepSeek identificou corretamente W20/W02/W11 antes da integração por partes
e a representação com jatos até primeira ordem depois de mover a divergência
para o cutoff. Corrigimos a afirmação de que os jatos de segunda ordem estão
inteiramente numa superfície física: eles se reorganizam em derivadas do
cutoff mesmo quando o fluxo de superfície é zero. Controle com
chi=t²(1-t)²,B=t² em[0,1]: superfície0 e ambas integrais=-1/30.

No controle tensorial já especificado, b4=(15/4,9/8,-3/4,-15/8),
Q=(2,2,2,5). Os dois fatores i da divergência Fourier dão
Vraw_boundary=16 Q.b4=-18, logo o contato normalizado raw/16=-9/8.
Com momento total zero, Vraw_boundary=0 exatamente. O perfil com superfície
física não nula proposto na resposta muda o problema e não é o controle
Fourier pedido. Também se preserva a separação: metric_quartic_vertices
calcula GammaGamma; o termo EH completo exige somar o motor de fronteira.
Nove controles locais passaram. O resultado prévio de1321 controles continua
sendo a evidência mais ampla; não foi reexecutado nem substituído.

Nesta entrega: 18 controles novos, CPU 0.09375s, rc0.
MiMo:356076tokens,419.479s,estimativaUSD0.1652913.
DeepSeek:268952tokens,171.033s,estimativa superiorUSD0.113241636.
Valores lidos dos recibos; não equivalem à fatura.

O coordenador preencheu as duas vagas: Kimi e710b704 no job
d41046ee-a069-4545-a6ba-9c322662af46; MiMo a369dc3e no job
5286ee12-8b8c-44d2-8af3-8dcd5562fe17. Ambos awaiting_dispatch na observação
recebida, não execução presumida. Kimi51c064fb continua próximo em staging.
Mantidos o prazo A7.b20:32UTC, cinco admitidos, uma execução por fornecedor
e três globais. Nenhum prompt independente foi contaminado pelos resultados.

Reprodução: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/audit_mimo_adjoint_deepseek_boundary.py. O script é de intake único;
uma repetição deve preservar recibos e não duplicar custos. Artefatos e log
estão custodiados no manifesto. Originais, kernel e gate intactos; Q2 OPEN.
Abertura sha256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
