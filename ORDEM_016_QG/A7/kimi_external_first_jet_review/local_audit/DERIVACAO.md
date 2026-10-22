[DERIVED — auditoria algébrica exata; resposta externa parcialmente aceita, Q2 OPEN]

O parecer Kimi foi lido integralmente. Seus40 canais ghost de primeira derivada
coincidem exatamente com G.vertex(BASIS[k])[1][rho] já existente. Portanto não
criamos novo motor para esse conteúdo. A dimensão do primeiro jato é10+40=50.
A montagem localizada posterior já usa esses slots; a extensão proposta responde
a um retrato anterior do motor bilocal, não a uma ausência em todas as rotas.

As listas A/B/M de tensores têm postos3/7/6; com simetria algébrica adicional de
troca de pares,5. Enumeramos todas as partições de índices livres em pares delta
e singles r (4 padrões de posto3,10 de posto4), simetrizamos e verificamos
SIMBOLICAMENTE cada identidade de expansão em todos os componentes. A solução
numérica exata num ponto fornece coeficientes candidatos; a igualdade polinomial
posterior é que comprova o span. O posto nesse ponto comprova independência;
rotação e escala estendem a independência aos r!=0 para coeficientes radiais.
O alcance é o ansatz construído de delta/r. Não invocamos literatura não lida
como prova de cobertura de todo tensor admissível. Auto-adjunção formal de um
operador diferencial não substitui conferir a simetria algébrica de pares.

Correções ao lado do parecer recebido:
1. G.vertex(T10) levanta IndexError: a API pede16 entradas da matriz4x4.
   LABELS é a parametrização de10 componentes, BASIS efetua a expansão correta.
2. Controle C3 do parecer é falso: para val(T01)=1, esquerda1, direita2.
   Dividir o teste em metades e simultaneamente mudar m de2 para1 duplica o peso.
3. Em x=X-Y, derivada emY é partial_Y z=-2x; o sinal positivo do §4.1 é o deX.
4. T_X independe deY em frame fixo. A proibição de qualquer transporte é excessiva:
   um caminho escolhido dá transporte definido; em vizinhança normal convexa,
   pode-se escolher a geodésica única. Mudança de frame é permitida quando o
   tensor dual e as conexões acompanham a transformação. O teste exato mostra
   tr(P^-1 T P P^-1 O P)=tr(TO), mas mudar sóT altera o par por -3t²-12t.
5. Ric=3Kg não fixa o segundo jato de um TESTE h arbitrário: em fundo plano,
   h11=Y0² tem h=Dh=0 na origem e partial00 h11=2. Uma extensão especial do teste
   deve ser declarada; não se transfere a equação do fundo ao teste.

O parecer distingue declaração e execução, o que foi preservado. Foram
128 verificações CAS exatas, rc0, CPU0.84375s.
Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/audit_kimi_external_first_jet.py.
Nenhuma alteração dos engines, nenhum ajuste de coeficientes, nenhum gate movido.
Não calcula Q2, termos suaves, curvatura completa nem extensão lorentziana.
O consumo desse Kimi já estava no LEDGER: não registramos outra chamada.

Abertura sha256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
