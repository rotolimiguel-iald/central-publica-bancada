[REAL — A4k.1–A4k.3 compilados no escopo geométrico e de composição]

# ORDEM 016 — Wick, período e calibração

UTC 2026-09-24T17:14:59.498343+00:00; ABERTURA sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

**A4k.1 PAGO.** A complexificação está ligada entrada a entrada ao boost real
existente. Para W=diag(1,-i), foi provado W⁻¹ B(iφ) W=exp(φGrot)=Smat(φ),
Smat(2π)=I e os lemas explícitos genK=Grot e complexificação(rotGen)=Grot.
Cada exponencial agora está ligada ao objeto existente; nenhum homônimo foi
substituído sem prova. O regime hiperbólico continua distinto da leitura circular.

**A4k.2 PAGO para o critério de quociente pedido.** Construímos o setóide
t~u sse t=u+nP, n inteiro, seu quociente efetivo e a projeção
polarPoint(r,κ,t)=r exp(iκt). Para r>0 e κ≠0, existe mapa F do quociente
para o plano complexo, injetivo e coincidente com essa projeção, SE E SOMENTE SE
κP=2π ou κP=-2π. A prova usa a periodicidade provada de Circle.exp e força
os números de voltas inversos a serem unidades inteiras, ±1. Não assume o
valor do período na definição da condição geométrica.

Para κ>0 e P>0, resulta P=2π/κ e 1/P=κ/(2π). Essa razão foi ligada à
função efetiva boostSegmentDefect: o coeficiente antes escrito como rate/(2π)
pode ser reescrito como 1/P sob o critério demonstrado. Não foi declarado um
teorema de regularidade de uma métrica arbitrária no vértice; o alcance é
exatamente a descida injetiva da projeção polar. A leitura T=1/P ainda depende
da identificação KMS do estado/região, separada em A4k.4.

**A4k.3 PAGO como calibração.** (κ,P)→(cκ,P/c) conserva a condição circular
para c≠0; a temperatura recíproca escala por c e κ/T permanece 2π.
O balanço quadrático do boost existente é equivalente antes/depois da escala,
por reutilização de boost_segment_quadratic_balance_iff. Do contrato v3.1,
foram reaproveitados sem alterar os corpos os teoremas κ=1/ρ(N), κ fixo dado N
e reindexação para qualquer N', condicionados a um habitante H2. Dois lemas
novos ligam o período angular a unruhTemperature e mostram igualdade de
períodos para o mesmo N. Nenhum habitante H2 foi criado por essa composição.

**Verificação:** 41 declarações auditadas em 6 fontes finais;
11 compilações preservadas, no máximo três por módulo. rc0,
somente axiomas permitidos, sem admissão nem escrita no kernel. Máquina
0.060636 h parede / 0.059852 h CPU; intervalo de bancada desde
primeira compilação 0.270704 h. A extração de calibração reutiliza
10 declarações, incluindo definições; não são anunciadas como
novos teoremas. Fontes, hashes, comandos, logs, falhas e origem do trecho
constam de `A4/wick_period_calibration_manifest.json`.

**Próximo:** A4k.4 (KMS de faixa), A4k.5 opcional e A4k.6 (dez leituras).
O período geométrico não determina sozinho um estado KMS, uma rede ou τ★ do
remanescente. A entrega completa A4_circulo_KMS ainda não foi emitida;
nenhuma PE cega da Parte B foi aberta aqui. Gate e originais intactos.

Orquestração: confirmação específica e delegação permanente recebidas;
primeira execução MiMo confirmada running, quatro unidades seguintes na fila.
Sem repetição. Estimativas já recebidas somam US$ 0.1939854588;
3 unidades anteriores sem custo informado e a execução viva ainda não
medida. Não é total faturado nem alegação de consumo zero.
