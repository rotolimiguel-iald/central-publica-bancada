[DERIVED — mudança exata de variáveis; REAL — diagnóstico do gerador; OPEN — implementação e teste na inferência]

# A fase no pico e a integração das duas ramificações

O diagnóstico `PEAK_PHASE_DIAGNOSTIC.json` mediu 35,77575177 rad de variação da fase
complexa 22 no pico quando a massa varia de 60 a 100 massas solares, com os demais
parâmetros fixos. Variando o spin comum entre −0,25 e 0,25, a variação foi
12,20038793 rad. Não são evidências de dephasing: são coordenadas da forma de onda GR.
Na variação da fase orbital de referência, a inclinação foi −1,999999990 e o resíduo
da relação linear, 8,73e−9 rad. Isso sustenta testar uma coordenada de fase no pico;
não prova que essa seja a única causa da concentração de pesos.

Sejam η os demais parâmetros, φ a fase orbital atual, uniforme em [0,2π), e
b(η) a fase do modo complexo 22 no pico com φ=0. Defina

    ζ = φ − b(η)/2  (mod π),       0 ≤ ζ < π.

É indispensável conservar as duas pré-imagens:

    φ_j = [ζ + b(η)/2 + jπ] mod 2π,       j=0,1.

Para QUALQUER likelihood periódica L(η,φ), sem aproximação da forma de onda,

    ∫[0,2π) L(η,φ) dφ/(2π)
       = ∫[0,π) {L(η,φ_0)+L(η,φ_1)}/2 · dζ/π.

Prova: para η fixo, a translação conserva a medida uniforme no círculo. Separá-lo
em dois intervalos de comprimento π e traduzir cada um para [0,π) dá exatamente
os dois termos. O jacobiano em φ é 1. A dependência de b em η não altera a prova,
que vale condicionalmente para todo η, preservando também o prior conjunto.

Sob a lei de fase 22 medida, arg(h_22 no pico)=b−2φ, o novo argumento é −2ζ;
as duas pré-imagens coincidem no modo 22. **Não coincidem necessariamente nos
modos ímpares:** estes podem trocar de sinal quando φ muda por π. Por isso os
dois termos precisam ser calculados com a forma de onda COMPLETA. Escolher só
um deles ou descartar modos ímpares mudaria a teoria estatística.

Se o argumento principal b salta em 2π, as duas pré-imagens simplesmente trocam
de rótulo. Sua soma permanece a mesma. Isso evita escolher uma ramificação
arbitrária a partir do modo 22.

Computar a média na escala logarítmica por logsumexp(logL_0,logL_1)−log(2).
A integração analítica de distância/polarização pode ser feita em cada ramo;
a linearidade da integral permite depois somar os ramos. O mesmo procedimento
vale separadamente para cada hipótese a=0/1, conjunto de dados e família.

Próxima implementação: coordenada ζ uniforme em [0,π), soma EXATA de ambos os
ramos e todas as harmônicas, preservando os outros priors. Validar a identidade
por quadratura independente na fase, conferir ambas as famílias e o caso de
modos ímpares, e só então executar novas amostras independentes. Não reutilizar
o nome de uma rodada anterior nem reinterpretar seus resultados como se já
tivessem usado essa transformação.

O diagnóstico e a derivação não movem o gate, não escolhem relógio/partição física
e não transformam os fatores de Bayes ainda imprecisos em resultados aceitos.
