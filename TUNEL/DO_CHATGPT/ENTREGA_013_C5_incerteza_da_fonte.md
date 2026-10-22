[REAL — diagnóstico local e integrais verificadas; INPUT nos priors e na transposição física; inferência astrofísica completa OPEN]

# Ordem 013 — incerteza da fonte e limites do resultado com fonte fixa

UTC: 2026-09-22T04:04:14.582949+00:00. Axiomas: N/A — sem Lean. Nenhuma mudança do gate, do um.py ou do C6.

## Resultado e interpretação

A rodada anterior de recuperação IMR fixava massas, spins, fase e inclinação. Esta extensão mede a informação que resta ao acrescentar, à mesma liberdade de amplitudes por detector, o instante do pico e quatro parâmetros intrínsecos: log da massa total, log da razão de massas, deslocamento comum dos spins alinhados e deslocamento oposto dos spins. A inclinação e o céu ainda são fixos. São duas famílias, O4/O5 de referência, quatro leituras observáveis, a=0/1 e uma única fonte representativa.

**Na família Phenom, o ramo B conserva cerca de 0.842% a 2.66% da informação local disponível após ajustar amplitudes, ao liberar também tempo e parâmetros da fonte.** O resultado é estável sob refinamento. Isso mede degenerescência neste modelo; não é exclusão da leitura B e não mede significância de um evento.

Na SEOB, a derivada da razão de massas e a dos spins continuam sensíveis à resolução. As estimativas estão preservadas e marcadas **NUMERICAL_SENSITIVITY_UNRESOLVED**. Não escolhemos o refinamento que produziria um resultado desejado. Passaram 16/32 controles em cada rodada: os 16 da Phenom. Essa contagem não representa uma aprovação física por maioria.

| Família | PSD | a de referência | z local, fonte fixa, SNR40 | z local, fonte livre, SNR40 | Informação restante | Controle |
|---|---|---:|---:|---:|---:|---|
| SEOBNRv4HM | O4 | 0 | 0.416009 | 0.057146 | 1.887% | NUMERICAL_SENSITIVITY_UNRESOLVED |
| SEOBNRv4HM | O4 | 1 | 0.390952 | 0.0492061 | 1.584% | NUMERICAL_SENSITIVITY_UNRESOLVED |
| SEOBNRv4HM | O5 | 0 | 0.417451 | 0.0566804 | 1.844% | NUMERICAL_SENSITIVITY_UNRESOLVED |
| SEOBNRv4HM | O5 | 1 | 0.392498 | 0.048926 | 1.554% | NUMERICAL_SENSITIVITY_UNRESOLVED |
| IMRPhenomXPHM | O4 | 0 | 0.399913 | 0.0438374 | 1.202% | STABLE_LOCAL_DIAGNOSTIC |
| IMRPhenomXPHM | O4 | 1 | 0.377102 | 0.0346032 | 0.842% | STABLE_LOCAL_DIAGNOSTIC |
| IMRPhenomXPHM | O5 | 0 | 0.403772 | 0.0658769 | 2.662% | STABLE_LOCAL_DIAGNOSTIC |
| IMRPhenomXPHM | O5 | 1 | 0.379117 | 0.0427879 | 1.274% | STABLE_LOCAL_DIAGNOSTIC |

O símbolo z nesta tabela é a norma local da derivada projetada, em unidades de ruído ideal, para Δa=1. É um diagnóstico de Fisher. Não é sigma observado nem conversão de fator de Bayes. O SNR é referido ao sinal nominal a=0 neste novo teste; não é exatamente a renormalização de cada injeção da rodada anterior.

## Construção e controle da conta

Escrevendo d=∂h/∂a e A para as colunas de parâmetros indesejados após branqueamento, calculamos d_perp=(I−AA⁺)d e I_a=||d_perp||². Os ranks são conferidos com três tolerâncias. As derivadas intrínsecas vêm de formas IMR novas, geradas por PyCBC/LAL, com o remanescente próprio de cada família; não de uma alteração arbitrária da frequência do QNM.

O pico é o máximo contínuo, por spline, da amplitude do harmônico 22. Todos os harmônicos compartilham esse pico. A janela de dados fica fixa em 10 tM do remanescente nominal enquanto variamos a fonte. Isso evita transformar mudança de janela em informação de massa.

Foram geradas 68 formas por rodada: nominal e diferenças centrais, mais controles de resolução. A segunda rodada divide os passos por quatro; a terceira dobra as taxas de geração para 16384/32768 Hz. As duas anteriores, seus registros e resultados continuam intactos. Total 204 formas de controle, não 204 eventos físicos independentes.

## Distribuições de razão de Bayes: escopo estritamente afim

Cada rodada também calcula 288 distribuições de ln B, com 206 intervalos de ruído por célula, usando os mesmos intervalos externos 50:256 já conhecidos. São reutilizados entre cenários e rodadas. A integral é a de um modelo afim h=h_a+J_a·u, com prior gaussiano normalizado em u. Assim C_a=I+J_a Σ J_aᵀ e log Z_a=−(r_aᵀC_a⁻¹r_a+log det C_a)/2, fora a constante comum.

Os três priors da fonte são: fixo, σ=0,002 e σ=0,02 em cada uma das quatro coordenadas declaradas. Eles são **INPUT diagnóstico**, centrados na fonte simulada. Não são informação do evento nem derivação da TGL. As amplitudes têm prior próprio, idêntico em definição entre hipóteses; a integração inclui o determinante. Também calculamos média e variância analíticas para ruído gaussiano ideal no centro do prior, mantendo-as separadas do ruído empírico.

Esses resultados não substituem uma integral sobre formas de onda não lineares. Uma média positiva sob a=0, que continua possível por efeito do prior, não é detecção. Os números completos de ambos a=0/1 estão no resumo JSON, sem selecionar somente a hipótese favorável.

## Critérios e evidências

- **PAGO:** registro e hashes antes de cada rodada; parâmetros físicos e regras de aceitação declarados; nenhum novo strain do evento lido.
- **PAGO:** integral afim conferida por Cholesky da covariância completa, independente da implementação SVD de produção: 648 comparações, maior diferença de ln B=2.06739514397e-10.
- **PAGO no escopo local:** convergência das derivadas e informação projetada na Phenom, nas quatro leituras/duas PSDs/duas amplitudes.
- **NÃO PAGO:** convergência da SEOB pelo critério pré-fixado; derivadas sensíveis preservadas como tal.
- **NÃO PAGO:** cobertura/viés sob variação não linear de fontes, marginalização astrofísica completa e rede com polarizações coerentes. As 12 amplitudes independentes por detector são uma flexibilidade fenomenológica, não uma inferência física de orientação.
- **INALTERADO:** C6, seus hashes, o veredito INCONCLUSIVE_SYSTEMATICS, as leituras físicas abertas e os pacotes anteriores.

## Próximo passo e aproveitamento

O diagnóstico local da fonte está calculado, mas não substitui marginalização não linear. Phenom mantém só 0,8–2,7% da informação local do ramo B depois dos parâmetros livres testados. A família SEOB falha nos controles de derivada mesmo com refinamento; avançar com avaliação não linear/coerente de fonte, sem trocar isso por mais rodadas de Fisher ou aceitar números instáveis.

Reaproveitados PSDs, ruído externo, QNMs, leis condicionais e geradores já instalados. Nada foi instalado em /opt. Para reproduzir o cálculo de uma rodada já gerada, entrar em sua pasta e executar `python -B analyze_source_tangents.py` seguido de `python -B verify_source_tangents.py` **em uma cópia nova com as saídas removidas da cópia**, preservando as entradas/registro; os scripts recusam sobrescrever resultados. A análise exige NumPy/SciPy; gerar fontes exige PyCBC/LAL. `verify_source_tangents_extended.py` confere as três rodadas sem repetir a geração. A geração usa só fontes públicas e o ruído derivado já custodiado. Não se entrega um novo ZIP duplicando os pacotes anteriores nesta etapa diagnóstica.

As falhas desta rodada são os controles numéricos da SEOB, registrados nos três resultados; as execuções terminaram com código zero. Não há processo em curso. STATUS, PROGRESSO e manifesto foram atualizados com backup imediato de bytes. Memórias canônicas são somente leitura nesta ordem.

## Custódia lida nesta execução

| Arquivo | SHA-256 |
|---|---|
| `REGISTRO_C5_SOURCE_TANGENTS.json` | `fb8a5728d8a1c0652e2f0ec7c38b1982c60e1c1bf51338dba84978d42e285eba` |
| `C5_SOURCE_TANGENTS_INPUTS.json` | `228a66d054e2e24726ab8edd030757e4649c44bec9f1a5c229d3edfa9df84853` |
| `C5_SOURCE_TANGENTS.json` | `2a5d4f63d26839ceab195b82e57fe08850d1b63405334f140da83c84723d4610` |
| `C5_SOURCE_TANGENTS_VALIDATION.json` | `e97a01c7943702c22ec16d1ddd3158b633edc5c3553142c5d36af17f93292bd2` |
| `cache/source_tangents_refinement/REGISTRO_C5_SOURCE_TANGENTS.json` | `704589ad5e13592fd18342db92c35b9bda6c6052e371d7348943027fec5b9d6f` |
| `cache/source_tangents_refinement/C5_SOURCE_TANGENTS_INPUTS.json` | `c33f91f1e5e489c400d437cef1fe75f679b79f564ab461e1adfc24829eec406e` |
| `cache/source_tangents_refinement/C5_SOURCE_TANGENTS.json` | `6b503e6b157e4a8d824ed4669d353efe0b1ade4317b37172259cc2fbc6674f22` |
| `cache/source_tangents_refinement/C5_SOURCE_TANGENTS_VALIDATION.json` | `4acf43f9c5438f90c86f6ac76b0524cc62e4d3e65f8371d2e1a6232d87511f4a` |
| `cache/source_tangents_highrate/REGISTRO_C5_SOURCE_TANGENTS.json` | `a658d193051cedaf6da2273bae70127fdb36757d28d2ddb515b45e342004f800` |
| `cache/source_tangents_highrate/C5_SOURCE_TANGENTS_INPUTS.json` | `bdce3d3b7ab07711aed46491e3b2ead0bb725ddee78bee9f51061438a9d15be5` |
| `cache/source_tangents_highrate/C5_SOURCE_TANGENTS.json` | `5effc64bf2dcb648145a1b002c62c6da027e6f685eeb68c7a56fd64d59eb9380` |
| `cache/source_tangents_highrate/C5_SOURCE_TANGENTS_VALIDATION.json` | `1e129e553bd02d4db0e140807e379ff24f101ca2715e1c5ecc0e3c9bef409214` |
| `prepare_source_tangents.py` | `54a823eb4ec3ade6c1bdbdd10a471d1b0594da40adff8229a13b3e183517535e` |
| `analyze_source_tangents.py` | `3b7b425e3f81f38b5c2cb5cafe182bf38daa46c89ef99cf1cd7c7b5647b5b77f` |
| `verify_source_tangents.py` | `59a868489a50fd6a57f0af4b3ffc0c1846a00ca12369a286f17e882f9b3d1944` |
| `refine_source_tangents.py` | `1d4ed9e22727b10872e3a2014b0c3dc74c919a9e141e17bea99933fca57f5d8f` |
| `refine_source_tangents_highrate.py` | `c7145796539b5410c5d81eec1614140a7e368a952bdb0b6014c9c47e811ec5a9` |
| `verify_source_tangents_extended.py` | `cdb7a9d38780fddffe52d0d6a4fa5dbf16e88fd9db2b615738a5552a9ce3e07b` |
| `C5_SOURCE_TANGENTS_EXTENDED_VALIDATION.json` | `c87363d62ddf2553f01716095859e89b5aa27144d9e224c007ec27812407781f` |
| `C5_SOURCE_UNCERTAINTY_SUMMARY.json` | `45e0d7aa63c591b29c4ad1cea9b4da8d3e16c77f2821df7f8ef5e93e1fd894f9` |
| `record_source_tangents.py` | `80d451503505d157c9af0a2058fbd78dc88fa2748c2a7752232283c72539fe86` |
| `cache/MANIFESTO_DOWNLOADS.json` | `6dd8ed1504bc0d18927a611fcf4ea6640740e7a8e16a642cc4e47d21a51a8d84` |
