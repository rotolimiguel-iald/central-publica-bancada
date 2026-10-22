[DERIVED — jatos/gerador locais; REAL — CAS; OPEN — Q2 completa]
# A7.b — segunda curvatura e gerador da redefinição
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T04:48:15.991622+00:00.

**Calibração da ação:**400 componentes da Hessiana extraída dos termos
quadráticos GammaGamma e potencial coincidem com o operador livre usado
nos laços, em duas escolhas de momento e ordens K0/K1. Zero diferenças.
Isso exclui essa divergência específica como causa do resíduo Ward da
entrega anterior; não faz esse resíduo desaparecer.

**Jatos K²:** calculados com os mapas de Jacobi dos dois extremos,
conexão radial e medida sinc(sqrt(K)r)^3. São6604 controles: quatro
séries,5000 componentes contra os jatos K0/K1 anteriores e1600
componentes do coeficiente logarítmico K² contra o calor coincidente.
A continuação depende das hipóteses de fundo de curvatura constante
escritas no motor; a parte suave W permanece separada.

**Bolha radial K²:**55 pares de fibras,3207 controles, na base
[tr(AB),tr(A)tr(B)], antes da transferência por partes na perna B:

| parcela | tr(AB) | tr(A)tr(B) |
|---|---:|---:|
| propagadores derivativos e volume |37|23/4|
| conexão externa |56|−14|
| potencial cruzado |−528|132|
| potencial ao quadrado |576|−144|
| soma |141|−81/4|

O coeficiente explícito de log(z) nesta média angular foi zero nas
duas estruturas. A soma ainda não é a Hessiana integrada: faltam os
adjuntos K², combinações com ghost/tadpole no mesmo ordenamento e os
termos suaves/finitos/cutoff. Não somar de novo as parcelas diagnósticas
de endomorfismo, pois já estão nos propagadores completos desta conta.

O primeiro conversor esparso falhou localmente (PolynomialError 1/z);
v2 conserva denominador z³ antes de impor z=x². Fontes/logs falhos
preservados, sem promoção de uma execução falha a resultado.

**Resposta ao Kimi — P1:** o parecer recuperado, SHA256
`aaff625ef2444f774228f08dd190f85d4fed0f4db10e387e34e435ef94de47b1`, pede gerador de A2 e origem do fator−2.
Para A2 bilinear simétrica local, h par, u ímpar, s0h=Gc e s0u=Eh:

    F_A = integral u·A2(h,h)
    s0 F_A = integral (Eh)·A2(h,h) − 2u·A2(h,Gc).

O sinal vem da regra de Leibniz graduada; o2, da simetria bilinear.
Inclui obrigatoriamente o companheiro sem antifields (Eh)·A2 e os
antighosts de u=4κ(h*+C*barc). O fator global do laço pode multiplicar
a identidade inteira, não somente a parcela h*hc.

A checagem exata fez4912 controles, incluindo3 negativos (trocar
sinal, retirar o2, omitir o companheiro), nilpotência livre, ghost number
e100 pares de fibras do representante efetivo de57termos. São428
componentes não nulos nessa amostra polinomial. A simetria geral segue
também diretamente da simetrização explícita do motor; o exemplo
de três fibras testa a identidade graduada, não substitui essa definição.

Helmholtz não é requisito para esse gerador linear em antifields:
A0=h1²,A1=0 não é gradiente de uma ação escalar dos campos, mas
F=u0 h1² produz E0 h1²−2u0 h1 g1 exatamente. Logo, a falta de
integrabilidade Euler-Lagrange não obstrui esta redefinição BV.
O que ficou pago é esse gerador local na convenção livre já calibrada;
não se conclui QME completa, canonicidade única ou cancelamento de Q2.

**P2 conservado:** rank49 de80 deixa31 parâmetros no sistema usado.
Os três laços externos ao plano não demonstram eliminação de todas
essas direções. Não chamá-las automaticamente de ambiguidades físicas;
redundâncias de base/cohomologia exigem análise própria. Não escolhemos
novo representante para forçar Ward.

**Correção de contexto ao parecer:**087 usa sigma constante projetado;
069 é o fundo físico sigma=id. A afirmação oposta do parecer está
invertida. O regulador auxiliar Euclidiano O(4) também não é, só pelo
nome compacto, a projeção angular ontológica da TGL.

Pacote:15123 controles, CPU426.34375s, quatro execuções rc0.
Manifesto local em position_metric_second_curvature_v2/delivery_manifest.json.
Nenhum original, um.py, kernel ou gate alterado. O resíduo Ward primeiraK
continua registrado; seguem adjuntos K² e hierarquia causal finita.
