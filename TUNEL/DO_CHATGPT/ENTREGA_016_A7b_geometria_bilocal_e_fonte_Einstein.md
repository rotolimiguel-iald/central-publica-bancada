[DERIVED — componentes escritos; REAL — CAS exato; OPEN — Q2 completo]
# A7.b — fonte Einstein e geometria de dois extremos
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T08:06:17.454748+00:00.

O operador E foi aplicado ao teste tensorial completo em RNC, antes da
extensão, com levantamento de índices e densidade. Foram conferidos os
campos do teste, o limite plano e um controle não axial. O argumento de
auto-adjunção formal usa testes compactos; a extração do símbolo bulk não
elimina por decreto os termos do corte.

Na base [p² Tpv, (pTp)(pv), p² trT(pv)], as colunas (1,L,L²) da fonte
adjunta primeiraK são:
[["55/108", "7/36", "0"], ["-47/36", "-1/4", "0"], ["599/432", "5/36", "0"]]
Fatores comuns C_E, i e K retirados. Isso mede R(E T,c), não a quebra Q2.

Os dois cálculos longos dos pares terminaram rc0, sem reinício:
- Taylor covariante ordenado (sessão93180): 3559.875s CPU.
- Teste em X e ghost em Y (sessão65231): 968.28125s CPU.
Seus coeficientes curvos diferem. Ambos passaram os respectivos controles
plano/não axial; isso não prova equivalência das duas montagens a uma mesma
distribuição de Ward. Somá-los à fonte sem derivar a integração por partes
bilocal não é autorizado pelo cálculo. Logs não nulos isolados não
estabelecem uma classe de anomalia quântica.

A identidade BRST livre dos propagadores foi conferida em coordenadas e
nas matrizes dos pares. Os jatos mistos métricos e fantasmas também foram
cotejados: o ghost superior tem sinal de conexão diferente do inferior.
Há verificações simbólicas e avaliações racionais específicas; o total
abaixo não significa igual número de teoremas independentes.

O motor bilocal mantém X e Y em UMA carta RNC antes de derivar:
 d1=-(X²Y²-(X.Y)²)/3,
 P1=((X²-Y²)I-XXᵀ+YYᵀ)/6+(XYᵀ-YXᵀ)/2.
A primeira expressão vem da energia da geodésica a primeiraK; a segunda,
da integral da conexão no segmento. A correção da trajetória contribui
em ordem superior. Inversa, isometria, transporte e recuperação dos jatos
da fonte passaram em1178 verificações. O teste v1 falhou porque comparou
expressões antes de impor o auxiliar z=X². O v2 só impõe essa restrição
DEPOIS das derivadas; o motor não foi alterado. O mesmo ocorreu no teste
ghost misto: v1 preservado, v2 registra256 identidades após a restrição.

Um controle concreto mostra por que ancorar cedo demais perde informação:
 (dYi dYj d1)|Y=0 = -2/3 (X² delta_ij-XiXj),
apesar de d1 e sua primeira derivada sumirem em Y=0. Para os completamentos
rho²=w+K d1 e w=(X-Y)² da MESMA prescrição ancorada, e para
u=w^-2 log(mu²w)^ell, ell=0,1, a diferença entre as segundas derivadas dos
reguladores estendidos produz -K*pi²*delta_ij*delta4(X)/2 a primeiraK.
Derivação: resíduo radial, área2pi² de S3 e <ni nj>=delta_ij/4; o fator
(1-a) é conservado inclusive no polo duplo do log. Testes que descartam
o termo falham em8 controles negativos. Esse é um exemplo escalar da
diferença entre completamentos; não seleciona uma nova prescrição física
nem fornece sozinho o comutador bitensorial geral.

Novas revisões aceitas pela coordenação: Kimi/divergência do par em Y;
Kimi/contatos do regulador em Y; MiMo/transporte bilocal independente;
DeepSeek/implementação da fonte Einstein. Mesma memória canônica, prévias
com executor correto, IDs persistidos e uma chamada por unidade. Estão em
STAGING, ainda sem job_id nesta entrega. Nenhum resultado esperado novo
foi inserido nos prompts de revisão, preservando a independência.

Total dos grupos: 5526 verificações reportadas, 8 negativos,
4563.640625s CPU (inclui os dois processos iniciados antes desta entrega).
Todos os dez comandos finais terminaram rc0 no Python simbólico de A4.
Custos das falhas preparatórias não medidos não entram como zero; v1/logs
continuam preservados. Nenhum original, kernel ou gate foi alterado.
Próximo: montar as derivadas Y dos kernels/vértices/medidas antes de Y=0,
transportar os contatos na mesma prescrição e então fazer a soma de Ward.
A7.b segue dentro do timebox; A7.c/d, A8 e ParteB continuam obrigatórios.
