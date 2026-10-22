[DERIVED condicional; CONJECTURE na ponte Kerr–KMS] 2026-09-22T17:31:19.239311+00:00; adendo a C1_LEITURAS.json, SHA256 333a9d8b7d650affb21e63564a399fa3048e407de71f7b9d57ec4d2cd2e583b3.

# C1 — correções medidas e limites da leitura modular

Nenhuma leitura foi selecionada. O ensaio é NÃO-CEGO quanto aos dados já publicados. A coluna das falas do operador permanece vazia.

As bandeiras de R-A e R-RAIZ-EP4 agora separam P1 (matéria, não excluída) de P2 (modos ópticos independentes por braço, excluída nessa partição). A cota P2 lida do núcleo é τ★/tP ≤ 0.0147282002183. Cota da série mediana, com margem de calibração; sem nível de confiança atribuído.
R-MOD recebe excluded_if_universal=true apenas para a extensão do período KMS local aos relógios terrestres (Unruh-g). Sua sobrevivência requer regra explícita de não universalidade, parte da partição física a cargo do operador.

## Passo 5: coincidência numérica, não identidade

| spin | δτ R-MOD, QNM exato | δτ R-RAIZ-0, QNM exato | R-MOD, controle BCW |
|---:|---:|---:|---:|
| 0 | -0.191788214 | -0.024645032 | -0.190907073 |
| 0.3 | -0.11101134 | -0.0279627916 | -0.111620226 |
| 0.5 | -0.0682042579 | -0.0315727169 | -0.0697627241 |
| 0.6785 | -0.0368350715 | -0.037164631 | -0.0380066766 |
| 0.8 | -0.0193399984 | -0.0445364273 | -0.0190877229 |
| 0.9 | -0.00765432196 | -0.0586305298 | -0.00590758775 |
| 0.95 | -0.00298293719 | -0.0778922357 | -0.00147016206 |

As duas expressões têm dependências distintas em spin. A proximidade perto de 0,68 não fornece uma identidade de operadores nem escolhe uma leitura. O controle BCW é impresso como aproximação; o ramo corrotante usa QNM exato.

## Passo 1: fontes e três rotas para spin não nulo

[KNOWN — seções do integral consultadas] Bisognano–Wichmann 1975: introdução, Teoremas 1–2 e discussão de Tomita–Takesaki (pp. 993, 997–998). O enunciado usa cunhas de Minkowski, vácuo, covariância e hipóteses sobre campos/álgebras. Não estabelece um estado térmico global em Kerr. Em 1976, introdução e Teorema 1 estendem o quadro a campos com spin e explicam a dualidade modificada na presença de férmions; tampouco identificam QNM com oscilador fechado.
[OPEN — integral não lido] Kay–Wald 1991: tentativas na editora e repositório autoral retornaram HTTP 403. Sewell 1982: o DOI forneceu apenas uma página de redirecionamento; a página recebida não contém o artigo. A referência bibliográfica não paga uma leitura integral. O passo fecha como parede de acesso documentada, não como teorema importado verificado nesta rodada.
[CONJECTURE — hipóteses da construção, não cânone] As alternativas são:
1. Restringir a região dentro da superfície em que o gerador corrotante se torna nulo e selecionar modos com ν=ω_R−mΩH>0. No oscilador efetivo escolhido, Z=Σ exp[−(2π/κ)νn] converge. Perde-se a identificação com todo o exterior assintoticamente plano; condições de contorno e existência do estado regional continuam exigências independentes. A positividade de um modo não prova a existência do estado completo.
2. Incluir um modo bosônico com ν<0 mantendo esse mesmo ansatz de Gibbs: os termos da soma geométrica crescem, logo Z diverge; em ν=0 também diverge. Não há estado normalizado desse oscilador. Uma truncagem finita esconderia a obstrução; não a remove no limite. Isso refuta o ansatz, não todos os estados de Kerr.
3. Usar um estado de Unruh para o problema de emissão/colapso. Nessa rota não se pressupõe equilíbrio KMS global do exterior. Perde-se a passagem automática K=(2π/κ)νN+log Z, ds/dt=κ/(2π) para toda a dinâmica; Γ da R-MOD não decorre apenas do nome Unruh. A lei de ruído/readout ainda exige derivação.

## Passos restantes e unidades

κ=√(1−χ²)/[2t_M(1+√(1−χ²))] e ν=ω_R−mΩH têm unidade s⁻¹; −Im ω determina τ_GR separadamente. Passo 2 [DERIVED condicional]: assumindo o oscilador positivo, K=(2π/κ)νN+log Z e ds/dt=κ/(2π), a coerência adjacente do duplo comutador dá Γ=πβν²/κ. Passo 3: o domínio ν>0 é exigido, e o ramo fora dele é recusado. Passo 4: a extensão universal laboratorial foi corrigida acima. Passo 6: estatutos permanecem separados. Nenhuma dessas contas prova a identificação do estado físico do horizonte.
As dimensões foram reconstruídas a partir de G, c, ħ, massa, frequência e energia, com expoentes racionais SI; uma soma de taxa com tempo é recusada como controle negativo. R-PROP é um expoente adimensional de propagação. R-GLOBAL tem taxa relacional nula por hipótese.

## C3.1 — constantes e regressão

LEGACY_V346 preserva G=6,674×10⁻¹¹ e M☉=1,98892×10³⁰ kg: não é o perfil CODATA2018/IAU2015. Comparação abaixo em z=0, para não misturar a diferença de constantes com a convenção de relógio fonte/detector:

| leitura | Γ_legado/Γ_moderno−1 | δτ_legado/δτ_moderno−1 |
|---|---:|---:|
| R-A | -0.000445513678 | -0.000234016627 |
| R-B | -0.000211546556 | 0 |
| R-RAIZ-EP4 | -0.000445513678 | -0.000234016627 |
| R-RAIZ-REST | -0.000679426047 | -0.000467978491 |
| R-LIN | -0.000211546556 | 0 |

Recalculadas 264/264 linhas do CSV, inclusive as 99 linhas pequenas solicitadas. O contador de 132 inclui também as 33 linhas R-GLOBAL de efeito exatamente nulo. Todas as diferenças relativas nas três colunas ficaram abaixo de 10⁻¹²; este é controle de reprodução do módulo, não uma segunda derivação independente de todas as leis.
A regressão v346 compara delta_tau_linear; a expressão de ensemble exata é −x/(1+x). O modo realization continua sem previsão universal: NÃO PAGO como distribuição calibrada de uma pipeline física; requer desenrolamento, estimador, janela e ruído nomeados. Os ensaios condicionais de C2 são separados.

## Evidência e reprodução

- C1_LEITURAS_v3.json: e9fdd97d7429476f3551750b40b2b5d996abe2a8a341472157872687c4a821ea
- C1_NUMERICAL_CONTROLS_v2.json: a5c943922993fdef3d09a8b898feb4210586e360121c32da4857ddd644e3edec
- C1_PRIMARY_RETRIEVALS.json: b22f77abeb19f8f0ea761259cf5019507bdc8cbf5ab81c9c88302ab8dcb98c3e
- bisognano_wichmann_1975.pdf: 874b39772c21e8773fc509601bcacc72eeb602117eea14da23ca7c46849712dc; https://denebola.if.usp.br/~jbarata/leituras-recomendadas/BisognanoWichmann-01-DualityConditionHermitianScalarField_985_1_online.pdf
- bisognano_wichmann_1976.pdf: 6d26912502b0da846b6aae380121583ed1adb859dde3f3289fa5d44df4ba8048; https://denebola.if.usp.br/~jbarata/leituras-recomendadas/BisognanoWichmann-02-DualityConditionQuantumFields_303_1_online.pdf
- sewell_1982_publisher.html: 37d4d38b2de397c16de3158503017bffdf23c2a56f5a332b9a1341f1f5eb5fd5; https://doi.org/10.1016/0003-4916(82)90285-8

Comando do cálculo: `/opt/lal_env/bin/python -B refeito/measure_c1_013bis_v2.py` a partir da bancada WSL. O script recusa sobrescrever resultado existente; para nova auditoria, executar uma cópia numa pasta própria com seus insumos.
Axiomas: N/A — sem Lean. A fonte canônica não foi executada nem editada. Não foram feitas PE, calibração pesada ou seleção de partição. A falha inicial de token da guarda P2 permanece em bis/C1_FAILED_P2_TOKEN_PREFIX.txt e no código .failed_P2_TOKEN_PREFIX.
Abertura do operador: SHA256 0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0.
