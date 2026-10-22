# F8.2.NU3 — parecer independente do módulo numérico candidato

**Autor:** `nu2_skeptic`, pesquisador documental; código candidato escrito por outra mão. **Unidade:** F8.2.NU3, reivindicação 633. **Veredito:** PASS no escopo matemático e sintético abaixo.

## Objeto pinado

- Candidata: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\candidate\bancada\neutrino_contract.py`.
- SHA-256: `eca873551583f13b5aa8974d27fe7f989450b876b207945e718ca415c527a91f`.
- Contrato de referência: `archive_contracts/CONTRACTS_API_R2.json`.
- Resultado: `tests/CANDIDATE_TEST_RESULT_R2.json`: **64 PASS, 0 FAIL**, exit 0.
- Verificação adicional do domínio de escala: `tests/BETA_SCALE_DOMAIN_RESULT_R1.json`, **4 verificações, 0 falhas**.

## O que foi conferido

[REAL computacional] O canal D[X⊗I] coincide com a solução analítica e com integração RK4 independente do gerador. Conserva traço, positividade (tolerância numérica), carga e composição de semigrupo. `expm1` preserva a probabilidade positiva para tempo adimensional minúsculo.

[REAL computacional; DERIVED condicional] O propagador físico coincide com integração RK4 do GKSL escrito por produtos matriciais, incluindo termo unitário. Foram conferidos: fator 1/2, conversão ℏ, textura vinculada dos três pares, n=−2 com entradas fixas, invariância ao deslocamento escalar de H, conservação de energia para H fixo, estado diagonal estacionário, τ★=0 e Kfac=0 como evolução unitária. A perda de coerência planckiana permanece positiva no diagnóstico `expm1`, mesmo quando o estado arredondado já não resolve o desvio.

[REAL computacional] O canal modular usa diferenças de raízes, não diferenças de k nem de energia. A família β(χ) é separada do coeficiente β0 da propagação. As saídas dizem tempo físico não identificado ou realização condicional, e conservam `nature_sigma=null`, `data_opened=false`, `gate_effect=NONE`.

[REAL computacional] NaN, infinitos, booleanos, texto em campo numérico, entradas negativas, energia zero, matrizes inválidas e alteração da identidade canônica durante a chamada foram recusados. O ataque de overflow produz aviso NumPy e depois ValueError; não houve sucesso falso.

## Achado corrigido

A versão anterior retornava zero quando exp(−χ/2) sofria underflow. A candidata pinada agora recusa χ=1500 e χ=10³⁰⁰ explicitamente com `BETA_SCALE_UNDERFLOW`; χ=100 e 1000 permanecem positivos. Kfac=0 passou a ser admitido como limite de canal nulo, como a fórmula permite. A R1 dos testes e a primeira candidata referida no resultado foram preservadas.

## Alcance do PASS

`require_current` foi substituído apenas no processo de testes por um recibo artificial; `finite_number` é a função real da candidata. Isso evita ler ou executar um.py, servidor, lake e Bench original. Portanto este parecer **não certifica o manifesto de implantação, a identidade do processo vivo, o transporte MCP/HTTP ou permissões de gravação**. Esses itens pertencem à revisão operacional da raiz.

O PASS é da implementação dos três modelos condicionais e da função de escala. Não atesta uma taxa de produção estelar, transporte em matéria, mapa físico de χ(E), ajuste de dados ou poder experimental. O módulo não identifica operadores de espaços distintos e não substitui β0 por β(E). Sua implementação é fiel aos contratos recuperados dentro desse recorte. Nenhuma alteração na candidata foi feita pelo revisor.
