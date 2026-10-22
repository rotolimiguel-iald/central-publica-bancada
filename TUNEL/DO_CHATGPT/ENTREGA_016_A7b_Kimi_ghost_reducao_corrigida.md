[DERIVED — resíduo integrado condicionado; REAL — CAS; OPEN — Q2 causal]
# A7.b — revisão do Kimi: parcela F² e correção mista
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T08:13:48.328167+00:00.

Recebido job `3979f662-13f0-4848-8948-b9dacb8c590e`, Kimi K3 máximo:
318432 tokens entrada/119744 saída,
438176 total. A resposta é preservada integralmente,
com o recibo e SHA. O Kimi entregou uma redução parcial e deixou F²/48
sem reduzir; o total conforme e o limite plano coincidiam com a bancada.

**A concordância desses controles não bastou.** A primeira tentativa local
usou a diferença entre a fórmula completa existente e a parcial do Kimi
para inferir F². Falhou em rc1 no par T=H=e00, ordemK: resíduo3/4.
O script/log v1 permanece. No v2, os coeficientes de F² foram extraídos
diretamente da contração de palavras covariantes, depois conferidos nos55
pares da base simétrica, nas ordens p⁴,Kp²,K² e num controle denso não axial.
O ajuste anterior ao teste é declarado; não é uma avaliação cega.

Com tau=trh, L=divh e Psi=divL, módulo divergências:

 tr(F²)/48 = -(Boxh)²/12+(Boxtau)²/24-Psi Boxtau/8
             -5 L BoxL/24-Psi²/24
             +K[7hBoxh/12+L²/6-7Psi tau/24-3tau Boxtau/32]
             +K²[-2h²/3+tau²/6].

O erro da parcial foi localizado em gamma=tr(B-Boxh)²/8. A forma corrigida é

 gamma = [Psi²+2 LBoxL+(Boxtau)²/4+(Boxh)²
          +K(7L²+9Psi tau-5tau Boxtau/4)]/8.

O modelo escrevera 5Psi tau e -tau Boxtau/4 dentro dos colchetes.
A correção total é K(Psi tau/2-tau Boxtau/8). Ela some para h=f g e
para TT, explicando por que os dois controles do texto não a detectavam.
A nova expressão gamma passou165 controles exatos; a antiga falha em26.

**Derivação algébrica curta.** C=L-gradtau/2, B=gradC. Pela integração
por partes em Ric=3Kg, tr(B²) equivale a
Psi²-Psi Boxtau+(Boxtau)²/4-3KL²-3KPsi tau+3Ktau Boxtau/4.
Usando div(Boxh)=BoxL+5KL-2Kgradtau e div(BoxL)=BoxPsi+3KPsi,
-2tr(B Boxh) equivale a
2LBoxL+Psi Boxtau+10KL²+12KPsi tau-2Ktau Boxtau.
Somando (Boxh)², obtém-se gamma acima. Nenhuma troca de derivadas
por momentos comutativos foi usada no controle curvo.

Também corrigido o sinal impresso da integração por partes:
int L BoxL = -int h^(ab) nabla_a Box nabla^r h_rb.
O sinal positivo do texto deixa diferença-4 num controle plano exato.
A parcela F² contribui nas três ordens; suprimi-la falha em três controles.

Com a correção, a soma reproduz a densidade integrada já registrada em
ghost_curved_hessian/DERIVACAO.md; não altera essa entrega anterior.
O controle conforme de F² dá K f Boxf/8, e o completo permanece
7(Boxf)²/8+19K f Boxf/2, módulo divergências.

O exemplo CE2 do modelo compara E1+E2, não o determinante do produto de
operadores: não demonstra anomalia multiplicativa. A corrente D2 exige
tr(Omega0 hA), não Omega0 tr(hA). São ressalvas de leitura, não novos
teoremas analíticos. As hipóteses do resíduo de calor permanecem explícitas.

Resultado: 337 controles reportados/30 negativos, rc0 nos v2/gamma,
CPU8.4375s; o custo de CPU da tentativa falha não foi medido. O conjunto
não é uma prova de determinantes finitos, identidade pontual, contatos de
cutoff nem Q2 completo. Gate e originais intactos. Próximo: voltar à
integração por partes bilocal, mantendo estas correções como verificação
do setor ghost e sem contaminar o parecer MiMo já em andamento.
