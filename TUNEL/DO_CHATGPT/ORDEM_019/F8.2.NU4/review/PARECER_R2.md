# Revisão independente NU4 — R2

**PASS_CONDITIONAL_NUMERICAL_PILOT** — 536/536 verificações. [REAL] Releitura dos 16 recibos, pré-registro, executor e quatro pinos, incluindo bytes do módulo e manifesto instalados. Não foi repetida chamada à Bancada.

[REAL numérico] Decimal de 110 dígitos, pi por Machin e cossenos por série; ΔPee conferido por subtração direta em alta precisão, independente do expm1 operacional. Taxas, lei E⁻², densidades, traço e positividade à tolerância pinada conferem.

| E (MeV) | ΔPee no recibo |
|---:|---:|
| 2 | 1.7880671575146663E-39 |
| 4 | -1.1955678421658232E-40 |
| 8 | 1.0530619494291178E-40 |

[DERIVED condicional] O estado diagonal é exatamente estacionário. O caso coerente tem efeito minúsculo, não zero físico; zero por subtração double é arredondamento. Energia preservada significa Tr(ρH) com H diagonal efetivo fixo, não um tensor gravitacional completo. Usou-se o ℏ da implementação, sem exigir igualdade de últimos dígitos com NU2.

O controle positivo foi escolhido antes para Γ31t=0,1; sua perda31=0,095162581964 e ΔPee=−0,000889064398731 conferem. Verifica a resposta do canal; não estima τ★. Paridade, canal modular e escala β(χ) também conferem e mantêm contratos e relógios distintos.

O relatório PRIMEIROS_RESULTADOS_R1 foi lido integralmente: não foi localizado defeito material de alcance. Este é um piloto condicional τ★=tP, Kfac=1, sem likelihood observada e sem cálculo de significância. Não demonstra fluxo absoluto, luminosidade nem massa de Chandrasekhar; não exclui outros contratos da TGL. A frase «não entregou um sinal de 5sigma» é delimitada logo adiante pela ausência de dados e função de significância, não um teste estatístico com resultado nulo.

Consulta ao Nós: NU4 ausente do grafo; pré-registro e NU2/NU3 reutilizados. Nenhuma escrita em Bancada, quadro ou memória. Identidade conferida por bytes/recibos existentes, sem nova sondagem HTTP.

ERRATA DA REVISÃO, em nome do revisor nu2_skeptic: R1 registrou 532/533 porque a própria sonda comparou o diagnóstico modular com Tr(rho K). A implementação nas linhas 86 e 98-99 define h=sqrt(K) e reporta Tr(rho sqrt(K)). O valor correto desse diagnóstico é 0,344246; 0,388246 pertence a Tr(rho K), também conservado, mas não é o campo emitido. R2 corrige só essa comparação; R1 e seus bytes foram preservados e pinados. Não houve alteração da Bancada nem repetição operacional.

Manifesto: `54fc9e27e4599c49990adb9587a45a8858393f2d8f5d66ec3e022b8140757c1b`.
Resultado: `ec18cfbd5a245d9a10e1bb446f7db86769cadfeca462a0172680047d8cd46482`.
Relatório interpretativo: `da04dc1a53af24bb990dda143dfe93e1b45a226cf5cf7492c456865d1489a851`.
