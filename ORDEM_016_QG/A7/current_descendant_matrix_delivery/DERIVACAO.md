# A7.b — descida distribucional da corrente: matriz completa no recorte medido

[REAL — cálculo simbólico exato; DERIVED — interpretação restrita; Q2 integral OPEN]

As 16 componentes de dois ghosts do resíduo anteriormente medido coincidem
exatamente com a descida distribucional da corrente já construída. Nenhum
coeficiente foi ajustado e nenhuma normalização nova foi escolhida.

Escopo: espaço plano regularizado, lambda=(1,-1,0,0), eta=(1,0,0,0), ambas
as orientações, 40 componentes h/c por orientação. Foram reutilizados oito
núcleos e calculados outros 72. O resto bilocal antissimetrizado é zero nas
16 componentes como expressão racional em x; a diferença entre o resíduo
local anterior e o descendente é zero nos 16 polinômios completos em D.
Não se trata de igualdade apenas no momento zero.

A operação relevante é C_i(F)=R(d_i F)-d_i R(F). Portanto
-(d_i+lambda_i)R(F)=R(-(d_i+lambda_i)F)+C_i(F).
Variar apenas o contato local da corrente omitia essa última parcela.
Mantidos Ymetric/2+Ymixed+Yghost+Xmetric+Xmixed, os fatores da base simétrica,
q->q-lambda, q->D+lambda+eta e a adjunção ponderada D->-D-L.

Auditoria por segunda fórmula: C_i(F)/CE=-2 Res[x_i F/z]/CE, derivada do
regulador analítico. Ela usa os núcleos racionais salvos e a rotina de resíduo,
sem chamar contact() nem recalcular os loops. Reproduz as 16 componentes.
Omitir o contato ou inverter seu sinal deixa diferenças nas 16 componentes.
No controle00 em D=0: omissão=-2743/3840; sinal invertido=-2743/1920.
Esta auditoria usa uma rota algébrica independente, mas compartilha a rotina
básica de resíduos; não equivale a revisão externa de todo o cálculo.

Matriz: 97 verificações, CPU 590.34375s, session19789 rc0.
Auditoria: 34 verificações, CPU 5.9375s, rc0.
Total desta entrega: 131 verificações, CPU 596.28125s.
Comandos: runtime SymPy A4, -X utf8 -B, current_distributional_descendant_matrix.py
e audit_current_descendant_matrix.py. Códigos de saída observados nas ferramentas;
sem captura independente de stdout em arquivo. JSONs e manifestos preservados.

Consequência: o resíduo isolado desse recorte não pode ser tratado como
obstrução homogênea sem incluir a inserção de corrente. Continua pendente
identificar integralmente as inserções da identidade quântica, tratar as
hipóteses de ordem um e estender o resultado para cutoffs gerais/curvatura.
Não foi estabelecido Q2 integral, nem anulação de classe de cohomologia.
O resultado não move o gate e não altera originais científicos/kernel.

A nota FR0B_CONSISTENCIA_LOCALIZADA_ORDEM2.md registra separadamente a condição
localizada da fonte primária e a expansão de ordem dois; não substitui a
identificação dos núcleos da bancada com suas inserções.

Orquestração: Kimi/MiMo prioritários na fila única. DeepSeek6309f0bf aceito
em STAGING_PRIORITY_CAPACITY, sem job nem execução, conforme mensagem oficial
da coordenação. Não duplicar unidades em andamento. Prazo A7.b20:32UTC.

Abertura SHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
