[REAL — quatro teoremas compilados; A5.b ainda parcial]
# A5.b — Integrais teleológicas e medida de memória
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

`TeleologicalTail_v3.lean` compila rc0 e auditoria PASSA, quatro declarações no trio.
Hipóteses: f contínua; para todo corte x, f e u*f absolutamente integráveis em Ioi(x).
Tail(x)=integral_x^infinito f; WeightedTail(x)=integral_x^infinito (u-x)*f.
Foram provadas as derivadas Tail'=-f e WeightedTail'=-Tail; portanto,
a=-c*WeightedTail e theta=c*Tail satisfazem a'=theta, theta'=-c*f, incluindo c=8*pi*G.
Estas hipóteses não são uma escolha de tensor físico; limites teleológicos e unicidade
continuam pendentes, assim como a conexão x+lambda*n à cauda deslocada.

Fontes/logs/recibos e hashes em `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A5\teleological_partial_manifest.json`.
Falhas 01/02 preservadas: import de derivada de produto ausente; depois elaboração de
termo corrigida com congr_deriv. Fonte v3 SHA256 `886642d13f6bbeaba2cb379aa59d20d2065eb7d3b60ab371bccbf346b7202b60`.

Construção matricial `NullPropagatorGeometry.lean`: tentativa 01 terminou
rc=3221226505, std::bad_alloc, pico 8588427264 bytes,
sob limite de processo 8192 MiB. Não é prova nem refutação. Próximo passo: separar
álgebra matricial leve e ligação ao contrato real, sem duplicar contrato nem relaxar limite.
Máquina total destas quatro tentativas: 58.760109s parede/58.906250s CPU.
Não move gate. Revisões Kimi de contorno e covariância, e MiMo de caudas, preparadas
com os IDs fixos e entregues à fila coordenada quando surgir vaga; nenhuma nova resposta presumida.
