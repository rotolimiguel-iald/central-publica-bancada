[DERIVED+CAS — correção de representação; jatos e gráfico escalar até primeira curvatura. Q2 OPEN]

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

A extensão R_bal usa linhas radiais identificadas e palavras de derivação.
Expandir a derivada de uma linha em polinômios vezes outro perfil ANTES
da extensão perde essa identificação. A tabela tensor_yjets inicial
passava controles de covariância, mas falhou no confronto com o contato
plano congelado: diferença não nula −Q0 Q²/384 no controle0101.
Ela permanece preservada como DIFFERENT_EXTENSION_NOT_ADOPTED.
O zerojet tensorial anterior não muda. Nenhuma nova prescrição foi escolhida.

labelled_bilocal_jet_engine conserva os três dados (coeficiente, perfil,
palavra radial). Seus4264controles incluem4200igualdades fora da diagonal
e64contatos escalares planos conhecidos. A tabela v2 tem57blocos,
representa570000pares e passa11400controles de forma+200regressões zerojet.
A auditoria adicional passou82200controles, incluindo2400comutadores e
48comutadores de curvatura não nulos. Permutações/reflexões não constituem,
sozinhas, prova de covariância sob toda mudança de coordenadas.

O gráfico real escalar Euler(X)×vértice métrico(Y), três sabores, dá
K CE [143/1536 δab Qr Q² −13/1536(δar Qb+δbr Qa)Q² −23/256 QaQbQr].
São coeficientes de derivadas COORDENADAS de delta, com duplicidade2
nos componentes a≠b. Seus272controles recuperam o contato principal.
A leitura adicional no fantasma contravariante transportado paralelamente
usa P1=(|x|²I−xxᵀ)/6; não pode omitir seus jatos. Resultado e controles
por dualidade distributiva estão em scalar_parallel/results.json.
Não chamamos essa leitura de operador covariante completo.

Kimi: mapa estrutural parcialmente útil; auditoria elementar detectou
sinal de bolha, omissão da bolha I1–V1 em J2 e conversão incorreta de
derivada direita do antifield ímpar. Não adotamos o dicionário numérico.
DeepSeek: não entregou o tensor solicitado. A lacuna de implementação
indicada já foi resolvida na medição local zerojet, não há confirmação
numérica independente nessa resposta. Recibos integrais preservados.

Todos os comandos Python desta correção terminaram rc0; tentativas
anteriores falhas foram mantidas. CPU/custos e hashes nos manifestos.
Não houve alteração de original, kernel, Atlas ou gate. Faltam montagem
temporal completa, setores restantes, K² e confronto da classe local
no problema integral. C6 continua ACTIVE dentro do teto original.
