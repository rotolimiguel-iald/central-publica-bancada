# EXCERTO — o julgamento do Torus: a ponte do círculo KMS (A-4 da ORDEM 016)

> [REAL — excerto montado por script a partir do julgamento da gerência de 23/09/2026 (sha16 do original 54aedf5eba78a5a3, 20568 B, fica com a gerência). Linhas copiadas sem alteração; «[…]» marca o que foi omitido.]
> **Omitido por ordem do operador:** o setor neural do artigo (estudo de pesos de modelo de linguagem; ilustração, não prova, na régua da casa) e o seu controle de circularidade — «o controle neural não precisa entrar no artigo» (verbatim, 23/09) — NÃO entram nesta ordem. O artigo original fica em `C:\IALD\Artigo\Torus\` e se cita só por caminho e sha16 (FONTES_DA_CASA.json).

**Pergunta do operador (verbatim, 23/09):** «É interessante porque eu também vejo que o
fechamento que buscamos para a QG está no meu artigo sobre o torus e a borda de wigner. Será
que faz sentido?»

[…]

## 0. O que conferi por conta própria (juiz)

| item | valor | como |
|---|---|---|
| core v370 `um_absoluto.json` | sha256 `d5fa9e29a6230746…`, 23/09 17:37 | lido por script |
| `remaining` | H2_smooth_modular_four_frame_and_geometric_identification · H3_area_heat_equilibrium_on_the_same_physical_horizon · interacting_quantum_state_BRST_QME_anomalies_and_UV_scope | lido |
| `physical_identifications_open` | microscopic_origin_of_Hmin_and_standard_bounded_transform · geometric_BW_identification_for_legacy_wedge_data_U_equals_one | lido |
| gpf_H2 / gpf_H3 / gpi_H3 | False / False / False | lido |
| `BoostHeatConstruction.lean:153` | «The normalization rate/(2*pi) is inherited, not derived as a temperature.» | grep |
| `BoostHeatConstruction.lean:183` `boost_segment_quadratic_balance_iff` | com `rate ≠ 0`: balanço ⟺ `eta*(a+c) = 2*Real.pi*mass`. O `rate` **sai** da condição | leitura |
| `ContinuousModularZero.lean:151` | `qKappa κ = Real.tanh (κ/2)`; α = sech(κ/2) | leitura |
| `Grot` (SMatrix:40, ℂ), `rotGen` (GeometryFluctuation:124, ℝ), `genK` (TheAngleIsTheProjection:76, ℂ) | três cópias de `!![0,1;-1,0]`; nenhum lema de Wick (`cosh_mul_I`/`sinh_mul_I`: 0 ocorrências em TGLExt) | grep |
| ponte de Wick (sympy, F3) | W⁻¹·boost(iφ)·W = rotação(φ); Rot(2π) = 1; período liso 2π/κ ⟹ T = κ/2π; E/T invariante sob ξ → cξ | saída `wick_kms_check_saida.txt` |

---


[…] (§1–§3: o setor neural — omitido)

## 4. A PONTE LEGÍTIMA, e em que forma exata

Existe uma ponte legítima. Ela **não passa pelos dados do artigo**; passa pela **palavra do
título**, o *tau do torus*, lido no sentido [KNOWN] que o artigo não usa, e ela respeita a Regra
dos Dois Regimes do operador.

**A forma exata** `[KNOWN — Bisognano–Wichmann 1975/76, Unruh 1976, Gibbons–Hawking 1977, Sewell 1982; reproduzido em sympy, não em kernel]`:

1. A **FACE** é o boost: direção hiperbólica, rapidez η, gerador K, fluxo Δ^{it}. É ela que **é**
   e que tem limite.
2. A continuação analítica η → iφ (t = −i·t_E) leva o boost à **rotação**:
   W⁻¹·boost(iφ)·W = exp(φ·[[0,1],[−1,0]]). O círculo euclidiano é **a continuação compacta da
   face hiperbólica**. É a LEITURA da face, não uma segunda face.
3. A órbita compacta fecha em 2π (Rot(2π) = 1). A ausência de singularidade cônica obriga o
   período em τ a ser 2π/κ; logo **T = κ/2π**, com β_KMS = 2π em rapidez (BW).
4. **O que a leitura faz e o que não faz.** Ela *não cria o limite*: o ângulo não sai do espaço, e
   isso a régua proíbe. Ela **fixa a unidade** do parâmetro da face: o 2π que o kernel hoje herda
   (`BoostHeatConstruction.lean:153`). **Não fixa κ**, que é normalização.

Em palavras do operador: **o toro, no sentido certo, é a leitura do fecho, não o fecho.** O
círculo KMS é o ângulo que se lê da face hiperbólica. Ele converte «2π herdado» em «2π
derivado», e isso é tudo o que um círculo pode dar.

**Duas notas de apoio, com estatuto:**

- `[DERIVED aqui — aritmética; identificação física OPEN]` θ_M = arcsin√β = **gd(κ_β/2)**, com
  κ_β = 2·artanh√β = 0,22026. A função de Gudermann é exatamente o mapa hiperbólico → circular
  (tanh(κ/2) = sin θ). No kernel, `qKappa κ = tanh(κ/2)` (ContinuousModularZero:151). Então
  θ_M é a leitura angular do ponto κ_β da variável espectral de log Δ, onde q² = β.
  - **Mas esse κ é espectral e adimensional** (E_Killing/T). **Não é** a gravidade de superfície.
    É uma definição, não a identificação de um horizonte.
  - É a Regra dos Dois Regimes vista num número só, e nada mais.
- `[KNOWN; relevância CONJECTURE; custo ALTO]` O lugar da literatura em que um toro de fato
  encontra a gravidade quântica é o toro de fronteira do BTZ euclidiano / CFT₂:
  - o parâmetro modular é τ = iβ_KMS/L;
  - a transformação S (τ → −1/τ) troca AdS₃ térmico e BTZ;
  - a fórmula de Cardy dá S = A/4G (Strominger 1998), uma ponte do tipo H3.
  - Mas isso é 2+1D, e não é o «τ = Matriz» do artigo.


[…] (§5: o controle neural — omitido)

## 6. Homônimos (régua 3: ditos em voz alta)

| palavra | no artigo | no canônico/kernel |
|---|---|---|
| **τ** («o Tau do Torus») | não é definido; existe só no título | τ★ ≈ t_Planck; τ = traço de Breuer; e o τ modular da CFT₂ [KNOWN], que o artigo não usa |
| **κ / K** | K = matriz Key da atenção; não há κ | K = gerador modular; κ = variável espectral de log Δ (ContinuousModularZero); κ = gravidade de superfície (T = κ/2π); κ_QED; κ de lente |
| **KMS** | glosa sem construção | `gibbs_kms` algébrico (FiniteTomita:179); o KMS de faixa **não existe** (mathlib StandardSubspace: TODO) |
| **`Grot` / `rotGen` / `genK`** | não aparecem | três cópias de !![0,1;−1,0] sem lema entre elas; a dívida que a régua nomeia |

[…]

## 7. O que entra na ORDEM 016

Todos os itens abaixo são **kernel ou controle**, e **nenhum** acende gpf_H2, gpf_H3 ou gpi_H3.
Nada move o gate.

| item | alvo | estatuto-alvo | custo |
|---|---|---|---|
| **A-4κ.1: lema de Wick** | Em kernel: W⁻¹·boostℂ(I·φ)·W = exp(φ•!![0,1;−1,0]) (via `Complex.cosh_mul_I`/`sinh_mul_I`) e Rot(2π) = 1, mais **um lema ligando cada homônimo** (`Grot`, `rotGen`, `genK`) a essa rotação | PROVADA (identidade algébrica, `#print axioms` ⊆ {propext, choice, quot}); paga a dívida de homônimos da Regra dos Dois Regimes | baixo (horas) |
| **A-4κ.2: regularidade cônica ⟹ 2π** | (r,τ) ↦ (r cos κτ, r sin κτ) desce a ℝ/Pℤ e é injetiva perto de 0 ⟺ κP = ±2π. Isso **deriva** o `rate/(2π)` que `BoostHeatConstruction.lean:153` declara herdado | [KNOWN] formalizado; converte «herdado» em «derivado» | médio (1–2 dias) |
| **A-4κ.3: retipagem de κ** | Corolário de escala: o balanço é invariante sob rate → c·rate (já implícito em `boost_segment_quadratic_balance_iff`). O contrato passa de «κ INPUT livre» para «κ = normalização (gauge); κ/T = 2π» | [REAL-kernel], já quase presente | muito baixo |
| **A-4κ.4: KMS de faixa analítica** | KMS do grupo de boosts em rapidez com β_R = 2π | [OPEN]: fica **nomeado, não prometido**; bloqueado pelo TODO da mathlib StandardSubspace | alto |
| **A-4κ.5 (opcional): lema de Gudermann** | tanh(κ/2) = sin θ ⟺ θ = gd(κ/2), ligando `qKappa` a θ_M | definição/aritmética, **com o aviso de homônimo** (κ espectral ≠ κ de horizonte) | baixo |

**O que não entra:** nenhum número dos pesos do Qwen vai para H2, H3, o setor interagente ou as
duas identificações físicas.


[…] (as linhas «Parte B: controle neural» e «Fora da 016» e a §8 — omitidas)

