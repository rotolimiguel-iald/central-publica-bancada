import TGLExt.TheMasterFires
import TGLExt.StrongFrame
import TGLExt.V354RegularLegacyWitness
import TGLExt.PoincareGroup
import TGLExt.ProfileEntropyLimits
import TGLExt.TheImportedEquilibrium

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# OS CONTRATOS DE TIPO DE H2 / H3 / IMPORT-H3, PARAMETRIZADOS PELA REALIZAÇÃO
  [RASCUNHO DE GERÊNCIA — item C01 do mapa de 22/09/2026; frente W2_final, 23/09/2026]

  Segunda versão (após o cético W2, correções C1–C7, e as duas correções de tipagem da frente W5).
  NÃO cunha nome reservado nenhum. NÃO entra em TGL/Audit.lean nem em um.py nesta sessão.
  Pronto para `TGLExt/ContratoQG.lean` na custódia da v370: os imports são os do kernel e o
  namespace já é `TGLExt.ContratoQG`; a transposição é cópia byte a byte para `TGLExt/` (o nome de
  módulo passa de `ContratoQG`, no scratchpad, a `TGLExt.ContratoQG`, sem mudar o conteúdo). Medido:
  no scratchpad o módulo NÃO pode chamar-se `TGLExt.ContratoQG` — o `lean` escolhe a primeira raiz do
  LEAN_PATH que contém a pasta `TGLExt/` e não cai para a seguinte (compile_ContratoQG_try0.txt).
  Nos probes, a única mudança na transposição é a linha `import ContratoQG` → `import TGLExt.ContratoQG`.

  É o TIPO que os três nomes reservados

    TGLExt.qgPrice_H2_smoothModularFourFrame_discharged     : ContratoH2 W₀ R₀
    TGLExt.qgPrice_H3_localHorizonEquilibrium_discharged   : ContratoH3 W₀ R₀
    TGLExt.qgImport_H3_horizonEquilibriumData_produced     : ContratoImportH3 W₀ R₀

  terão de habitar quando alguém os cunhar, no molde de `TGLExt/V350GateContract.lean`
  (`def checkedH2 : ContratoH2 ratifiedWitness.1 ratifiedWitness.2 := qgPrice_H2_...` +
  `#print axioms` no Audit), onde `ratifiedWitness : FullTGLWitness = ⟨W₀, R₀⟩` é o par
  (testemunha, realização) RATIFICADO PELO OPERADOR (a partição M01; cláusula (d)).

## O furo que este arquivo fecha (v103, medido no mapa C01)
  Os leitores `_GRAVITY_PRICE_FLAGS` / `_GRAVITY_IMPORT_FLAGS` do um.py aceitam QUALQUER termo com
  esses nomes e axiomas limpos. `SmoothFrameData` e `HorizonEquilibriumData` são trivialmente
  habitáveis (`theCurvedFrame`, `theHorizon`) — um `True` com o nome certo acenderia a bandeira.

## O que mudou da 1ª versão (a928a853355afc54) — as correções do cético
  C2  O contrato é `ContratoH2 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)`:
      (B1) é sobre `W.net` e o fluxo de `R` (via o implementador `Δit`, abaixo); (B2) é
      `∃ a, W.U a ≠ 1`; (B3) idem; e `dS_eq` de `ContratoH3` é sobre o PERFIL DO ESTADO DE R
      (campo `profile`, amarrado a `W.vac` e ao fluxo de R por `stateIso`), não `mixProfile` por nome.
      A 1ª versão citava `theSpecificAQFTWitness` e `mixProfile` POR NOME dentro do tipo: era
      IsEmpty INCONDICIONAL, e nenhum fornecedor poderia cunhar os nomes reservados sem editar
      WedgeNet.lean. Agora o vazio é TEOREMA SOBRE O PAR LEGADO
      (`contratoH2_empty_on_legacy_realization : IsEmpty (ContratoH2 theSpecificAQFTWitness
      regularModularRealization)`) e o tipo tem alvo habitável em outro par.
  W5(a) `WedgeModularData` NÃO expõe Δ^{it} em vetores (só o fluxo na álgebra, `≃⋆ₐ`). O contrato
      leva o implementador como CAMPO: `Δit : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)`, `Δit t W.vac = W.vac`, e
      `modularFlow t a = Δit t ∘ a ∘ Δit (−t)` (campo `flow_implemented`, escrito com
      `LinearIsometryEquiv.conjStarAlgEquiv`, que é EXATAMENTE a forma do kernel:
      `modularConjugation P t := (modularFlowUnitary P t).conjStarAlgEquiv`, ModularFlowAlgebra.lean:63).
      Na realização legada o implementador existe e a identidade é rfl (`legacy_flow_is_implemented`).
  W5(b) O frame é REGIONAL: `smooth_on`/`det_unit_on` sobre `rightWedge` [REAL — já era assim na 1ª
      versão, linhas 197-198]. Correção D1 do cético de W5, incorporada ao docstring de (C): para o
      frame do jato `E = [ξ_κ | e₁ | e₂ | e₃]` vale det E = κ·x¹ (lema `jetFrame_det`, [DERIVED]):
      invertível em todo x¹ ≠ 0 (em particular em TODA a cunha, onde x¹ > |x⁰|) e degenerado no
      HIPERPLANO x¹ = 0, que contém a aresta — por isso `SmoothFrameData.det_unit` (global,
      ClosureCertificate.lean:101) é o tipo errado, e o contrato pede `∀ x ∈ rightWedge`.
  C4  `kappa_eq_two_pi_temperature` é DEFINICIONAL (T := κ/2π); κ é [INPUT] e NÃO está amarrado ao
      parâmetro KMS de `Δit` nem à rapidez de `boostMat` (ligação [OPEN]).
  C6  `contratoH2_empty_on_legacy_realization` é a CONTRAPARTE EM KERNEL da identificação física
      ABERTA listada em um.py:162032 (`geometric_BW_identification_for_legacy_wedge_data_U_equals_one`):
      com U = 1 a cláusula (B2) falha e o contrato é vazio. Não é a identificação BW em si.

## A amarração: A MESMA REALIZAÇÃO, agora como PARÂMETRO
  Para o par legado (o que hoje paga H1/A2) os nomes curtos da secção 0 são, POR rfl/teorema, os
  objetos de `regularModularRealization` sobre `theSpecificAQFTWitness`
  (`sameFlow_is_the_regular_modular_flow`, `sameVacuum_is_the_regular_vacuum`,
  `sameNet_is_the_wedge_algebra`, `legacy_flow_is_implemented`). Para QUALQUER par (W, R) o
  contrato exige que rede, vácuo, fluxo, estado e cunha sejam os de (W, R) — pelos campos, não por nome.

## Estatutos
  [DERIVED]  os lemas de sanidade, as exclusões aritméticas e as paredes (provados aqui, sem sorry);
  [KNOWN]    Bisognano–Wichmann (Δ^{it} = U(Λ(−2πt))), Unruh (T = κ/2π), Bekenstein–Hawking (S = A/4G),
             Jacobson 1995 — entram como CLÁUSULAS EXIGIDAS, nunca como teoremas daqui;
  [INPUT]    κ, G, a tela S, o horizonte esticado ε, o segmento λ₀, o tensor de matéria, o perfil
             perturbado, o andar N — e o PAR (W₀, R₀) ratificado (partição do operador);
  [OPEN]     a identificação da rede da TGL com uma rede física (M01); a ligação κ ↔ parâmetro KMS
             de Δit; o limite N → ∞ da entropia da torre.

  β jamais literal. Sem sorry, sem axiom. Nada aqui move o gate — torna estritamente mais difícil movê-lo.
-/

namespace TGLExt.ContratoQG

open TGL.SpecificAQFT TGL.ModularRealization ChatgptAudit TGLExt.V350Continuous
open TGLV354.TraceCompletion ChatgptAudit.Response028
open MeasureTheory Matrix

noncomputable section

/-! ## 0. O PAR LEGADO — nomes curtos que são, por prova, os objetos da realização regular -/

/-- Ad(Δ^{it}) da torre no perfil `mixProfile`: o fluxo modular da realização regular. -/
abbrev sameFlow (t : ℝ) : WCLM ≃⋆ₐ[ℂ] WCLM := modularConjugation mixProfile t

/-- a rede da realização regular. -/
abbrev sameNet (O : Set (Fin 4 → ℝ)) : VonNeumannAlgebra WH := theSpecificAQFTWitness.net O

/-- o vácuo da realização regular. -/
abbrev sameVacuum : WH := hOmega mixProfile

/-- [DERIVED] o fluxo deste arquivo É o `modularFlow` da camada 1A de `regularModularRealization`
    (por rfl: `regularModularRealization.modular = towerWedgeData`, `towerWedgeData.modularFlow =
    factorFlow mixProfile`, `factorFlow P t a = ⟨modularConjugation P t a, _⟩`). -/
theorem sameFlow_is_the_regular_modular_flow (t : ℝ)
    (a : (regularModularRealization.modular.wedgeAlgebra).toStarSubalgebra) :
    ((regularModularRealization.modular.modularFlow t) a).val = sameFlow t a.val := rfl

/-- [DERIVED] ★ (W5(a), na realização legada) o fluxo da camada 1A É implementado em vetores pelo
    unitário `modularFlowUnitary mixProfile t : WH ≃ₗᵢ[ℂ] WH` do kernel, via `conjStarAlgEquiv` — por rfl
    (`modularConjugation P t := (modularFlowUnitary P t).conjStarAlgEquiv`). É a forma do campo
    `ContratoH2.flow_implemented`, instanciada no par legado. -/
theorem legacy_flow_is_implemented (t : ℝ)
    (a : (regularModularRealization.modular.wedgeAlgebra).toStarSubalgebra) :
    ((regularModularRealization.modular.modularFlow t) a).val
      = (modularFlowUnitary mixProfile t).conjStarAlgEquiv a.val := rfl

/-- [DERIVED] o vácuo deste arquivo É o vácuo da testemunha (por rfl). -/
theorem sameVacuum_is_the_regular_vacuum : theSpecificAQFTWitness.vac = sameVacuum := rfl

/-- [DERIVED] a álgebra da cunha da rede É o fator da torre (teorema `wedgeNet_M`), e é a
    `wedgeAlgebra` da realização regular (campo `wedgeAlgebra_eq`). -/
theorem sameNet_is_the_wedge_algebra :
    sameNet rightWedge = regularModularRealization.modular.wedgeAlgebra :=
  regularModularRealization.modular.wedgeAlgebra_eq.symm

/-- [REAL — lido da definição] as translações da realização LEGADA são triviais: `U := fun _ => 1`. -/
theorem legacy_translations_trivial (a : Fin 4 → ℝ) : theSpecificAQFTWitness.U a = 1 := rfl

/-! ## 1. A ação geométrica do fluxo: o boost da cunha e o seu campo de Killing -/

/-- a ação geométrica do boost no plano (0,1) da cunha `rightWedge` (rapidez `s`);
    reutiliza `TGLExt.boostMat` (PoincareGroup.lean), que é o boost NESSE plano. -/
def wedgeBoostMap (s : ℝ) (x : Fin 4 → ℝ) : Fin 4 → ℝ := (boostMat s).mulVec x

/-- o campo de Killing do boost, normalizado por κ (a gravidade superficial do observador de
    Rindler): ξ_κ(x) = κ·(x¹, x⁰, 0, 0). Anula-se exatamente na aresta {x⁰ = x¹ = 0}. -/
def killingField (κ : ℝ) (x : Fin 4 → ℝ) : Fin 4 → ℝ := κ • ![x 1, x 0, 0, 0]

theorem wedgeBoostMap_apply0 (s : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s x 0 = Real.cosh s * x 0 + Real.sinh s * x 1 := by
  simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

theorem wedgeBoostMap_apply1 (s : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s x 1 = Real.sinh s * x 0 + Real.cosh s * x 1 := by
  simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

/-- [DERIVED] ★ o boost preserva a MESMA cunha (a cunha é o domínio do seu próprio fluxo modular). -/
theorem wedgeBoostMap_mem_rightWedge (s : ℝ) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    wedgeBoostMap s x ∈ rightWedge := by
  have hx' : |x 0| < x 1 := hx
  obtain ⟨h1, h2⟩ := abs_lt.mp hx'
  have hd : 0 < x 1 - x 0 := by linarith
  have hs : 0 < x 1 + x 0 := by linarith
  have e1 : Real.cosh s - Real.sinh s = Real.exp (-s) := Real.cosh_sub_sinh s
  have e2 : Real.cosh s + Real.sinh s = Real.exp s := Real.cosh_add_sinh s
  have p1 : 0 < (Real.cosh s - Real.sinh s) * (x 1 - x 0) := by
    rw [e1]; exact mul_pos (Real.exp_pos _) hd
  have p2 : 0 < (Real.cosh s + Real.sinh s) * (x 1 + x 0) := by
    rw [e2]; exact mul_pos (Real.exp_pos _) hs
  show |wedgeBoostMap s x 0| < wedgeBoostMap s x 1
  rw [wedgeBoostMap_apply0, wedgeBoostMap_apply1, abs_lt]
  constructor <;> nlinarith

/-- [DERIVED] a aresta é fixa pelo boost: o horizonte é de Killing para o MESMO fluxo. -/
theorem wedgeBoostMap_fixes_edge (s : ℝ) {x : Fin 4 → ℝ} (h0 : x 0 = 0) (h1 : x 1 = 0) :
    wedgeBoostMap s x = x := by
  funext i
  fin_cases i <;> simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four, h0, h1]

/-- [DERIVED] o campo de Killing anula-se na aresta (o ponto onde o frame NÃO pode ser o gerador cru:
    por isso a cláusula do jato é o ARRASTO pelo 1-jato, não "coluna = gerador"). -/
theorem killingField_vanishes_on_edge (κ : ℝ) {x : Fin 4 → ℝ} (h0 : x 0 = 0) (h1 : x 1 = 0) :
    killingField κ x = 0 := by
  funext i
  fin_cases i <;> simp [killingField, h0, h1]

/-- [DERIVED] o determinante do boost é unidade — lido da condição de Lorentz `boostMat_isLorentz`
    (det B · det η · det B = det η, com det η = −1 ≠ 0), sem expandir o 4×4. -/
theorem boostMat_det_isUnit (s : ℝ) : IsUnit (boostMat s).det := by
  have h := congrArg Matrix.det (boostMat_isLorentz s)
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose] at h
  have hη : eta4.det ≠ 0 := by
    unfold eta4
    rw [Matrix.det_diagonal, Fin.prod_univ_four]
    norm_num [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
      Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail]
  have hsq : (boostMat s).det * (boostMat s).det = 1 := by
    have h' : ((boostMat s).det * (boostMat s).det - 1) * eta4.det = 0 := by
      linear_combination h
    rcases mul_eq_zero.mp h' with h1 | h1
    · linarith
    · exact absurd h1 hη
  refine isUnit_iff_ne_zero.mpr ?_
  intro h0
  rw [h0, mul_zero] at hsq
  exact zero_ne_one hsq

/-- o FRAME DO JATO de W5: colunas [ξ_κ(x) | e₁ | e₂ | e₃] (o gerador cru na coluna 0, a base
    canônica nas outras). NÃO é candidato a habitante de (D) — as colunas 1–3 não são arrastadas pelo
    boost; serve SÓ para medir em kernel o determinante que decide o TIPO do frame (regional). -/
def jetFrame (κ : ℝ) (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![κ * x 1, 0, 0, 0;
     κ * x 0, 1, 0, 0;
     0,       0, 1, 0;
     0,       0, 0, 1]

/-- [DERIVED] ★ (D1 do cético de W5, agora em kernel) det E = κ·x¹ para o frame do jato: invertível em
    todo x¹ ≠ 0 (em particular em TODA a cunha, onde x¹ > |x⁰| ≥ 0) e degenerado no HIPERPLANO x¹ = 0,
    que contém a aresta. Por isso `det_unit` GLOBAL (`SmoothFrameData`) é o tipo errado e o contrato
    pede `det_unit_on : ∀ x ∈ rightWedge`. -/
theorem jetFrame_det (κ : ℝ) (x : Fin 4 → ℝ) : (jetFrame κ x).det = κ * x 1 := by
  simp [jetFrame, Matrix.det_succ_row_zero, Fin.sum_univ_succ]

/-- [DERIVED] na cunha, com κ > 0, o frame do jato é inversível (o x¹ > |x⁰| ≥ 0 da cunha). -/
theorem jetFrame_det_isUnit_on_wedge {κ : ℝ} (hκ : 0 < κ) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    IsUnit (jetFrame κ x).det := by
  rw [jetFrame_det]
  have hx' : |x 0| < x 1 := hx
  have h1 : 0 < x 1 := lt_of_le_of_lt (abs_nonneg _) hx'
  exact isUnit_iff_ne_zero.mpr (mul_pos hκ h1).ne'

/-- [DERIVED] no hiperplano x¹ = 0 (que contém a aresta) o frame do jato DEGENERA. -/
theorem jetFrame_det_zero_on_hyperplane (κ : ℝ) {x : Fin 4 → ℝ} (h1 : x 1 = 0) :
    (jetFrame κ x).det = 0 := by
  rw [jetFrame_det, h1, mul_zero]

/-! ## 2. CONTRATO H2 — o four-frame suave como JATO da ação geométrica do fluxo de (W, R) -/

/-- **ContratoH2 W R** — o tipo que `qgPrice_H2_smoothModularFourFrame_discharged` terá de habitar,
    no par (W₀, R₀) RATIFICADO pelo operador.

    (A) NORMALIZAÇÃO [INPUT]: κ > 0, a gravidade superficial do campo de Killing ξ_κ; T := κ/2π é a
        temperatura de Unruh POR DEFINIÇÃO (`unruhTemperature`). κ NÃO está amarrado, neste tipo, ao
        parâmetro KMS de `Δit` nem à rapidez de `boostMat` — ligação [OPEN] (C4).
    (Δ) O IMPLEMENTADOR [W5(a)]: `WedgeModularData` só expõe o fluxo na álgebra; o contrato exige o
        unitário `Δit t` em vetores que o implementa (`flow_implemented`), fixa o vácuo (`Δit_vac`) e
        é o mesmo objeto de que (B1)/(B3) falam. No par legado é `modularFlowUnitary mixProfile`
        (`legacy_flow_is_implemented`, rfl).
    (S) O ESTADO: o estado de R lido como PERFIL da torre (`profile`), com a identificação isométrica
        `stateIso` que leva `hOmega profile` em `W.vac` E entrelaça o fluxo da torre com `Δit`
        (`state_flow`) — é este perfil que `ContratoH3.dS_eq` usa (C2), não `mixProfile` por nome.
    (B) BISOGNANO–WICHMANN EM (W, R) [KNOWN como exigência]: Ad(Δit t) sobre `W.net` é GEOMÉTRICO —
        leva a álgebra da região O na da região boostada Λ(−2πt)·O, para toda região (B1); as
        translações de W são não-triviais (B2); e satisfazem a relação de Poincaré com Δit (B3).
        O par legado tem U = 1 e NÃO paga (B2): `contratoH2_empty_on_legacy_realization`.
    (C) O FRAME NO HORIZONTE DE RINDLER LOCAL — REGIONAL [W5(b)]: campo E sobre a cunha, C^∞ NA
        CUNHA, det inversível NA CUNHA. O tipo global (`SmoothFrameData.det_unit : ∀ x`) é o errado:
        o frame do jato tem det = κ·x¹ (`jetFrame_det`), inversível em todo x¹ ≠ 0 e degenerado no
        hiperplano x¹ = 0 (que contém a aresta) — D1 do cético de W5, [DERIVED] aqui.
    (D) O JATO: o frame é ARRASTADO pelo 1-jato da ação geométrica do fluxo:
        E(Λ_s x) = DΛ_s(x)·E(x) = boostMat s · E(x).  `theCurvedFrame` viola isto por aritmética
        (`curvedFrame_not_dragged`, entrada (1,0)).
    (E) A FIDUCIAL É O TEMPO MODULAR (o Nome, v96 suavizado): a coluna 0 de E(x) é um múltiplo
        POSITIVO de ξ_κ(x). `theCurvedFrame` viola isto por aritmética (`curvedFrame_fiducial_not_modular`). -/
structure ContratoH2 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W) where
  /-- (A) a normalização do campo de Killing [INPUT]. -/
  kappa : ℝ
  kappa_pos : 0 < kappa
  /-- (Δ) o implementador do fluxo de R em vetores: Δ^{it} como isometria unitária de W.H. -/
  Δit : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)
  /-- (Δ) Δ^{it} fixa o vácuo de W. -/
  Δit_vac : ∀ t : ℝ, Δit t W.vac = W.vac
  /-- (Δ) o fluxo da camada 1A de R É Ad(Δ^{it}): modularFlow t a = Δit t ∘ a ∘ Δit (−t). -/
  flow_implemented : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
    ((R.modular.modularFlow t) a).val = (Δit t).conjStarAlgEquiv a.val
  /-- (S) o estado de R como perfil da torre. -/
  profile : SiteProfile
  /-- (S) a identificação isométrica da torre do perfil com W.H … -/
  stateIso : TowerHilbert profile ≃ₗᵢ[ℂ] W.H
  /-- (S) … que leva o vácuo da torre no vácuo de W … -/
  state_is_vac : stateIso (hOmega profile) = W.vac
  /-- (S) … e entrelaça o fluxo modular da torre com o implementador de R. -/
  state_flow : ∀ (t : ℝ) (x : TowerHilbert profile),
    stateIso (modularFlowUnitary profile t x) = Δit t (stateIso x)
  /-- (B1) BW geométrico de Ad(Δ^{it}) sobre a rede de W: Ad(Δit t) net(O) ⊆ net(Λ(−2πt) O). -/
  bw_covariance : ∀ (t : ℝ) (O : Set (Fin 4 → ℝ)) (T : W.H →L[ℂ] W.H),
    T ∈ W.net O → (Δit t).conjStarAlgEquiv T ∈ W.net (wedgeBoostMap (-(2 * Real.pi * t)) '' O)
  /-- (B2) as translações de W são não-triviais (uma rede física translada). -/
  translations_nontrivial : ∃ a : Fin 4 → ℝ, W.U a ≠ 1
  /-- (B3) a relação de Poincaré entre Δ^{it} e as translações de W: Δ^{it} U(a) Δ^{−it} = U(Λ(−2πt) a). -/
  poincare_relation : ∀ (t : ℝ) (a : Fin 4 → ℝ),
    (Δit t).conjStarAlgEquiv (W.U a) = W.U (wedgeBoostMap (-(2 * Real.pi * t)) a)
  /-- (C) o campo de frames, REGIONAL. -/
  E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  smooth_on : ∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => E x i j) rightWedge
  det_unit_on : ∀ x ∈ rightWedge, IsUnit (E x).det
  /-- (D) o jato: arrasto pelo diferencial da ação geométrica do fluxo. -/
  dragged : ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
    E (wedgeBoostMap s x) = boostMat s * E x
  /-- (E) a fiducial é a direção do tempo modular, positivamente. -/
  fiducial_is_modular : ∀ x ∈ rightWedge,
    ∃ c : ℝ, 0 < c ∧ (fun i => E x i 0) = c • killingField kappa x

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- a temperatura de Unruh em tempo de Killing, POR DEFINIÇÃO: T := κ/2π. -/
def unruhTemperature (C : ContratoH2 W R) : ℝ := C.kappa / (2 * Real.pi)

/-- [DERIVED trivial — definicional: T := κ/2π] κ = 2π·T. κ é [INPUT] e NÃO está amarrado ao parâmetro
    KMS de `Δit` nem à rapidez de `boostMat` (ligação [OPEN]) — C4 do cético. -/
theorem kappa_eq_two_pi_temperature (C : ContratoH2 W R) :
    C.kappa = 2 * Real.pi * C.unruhTemperature := by
  unfold unruhTemperature
  field_simp

/-- [DERIVED] ★ o contrato ALIMENTA a face finita de H2 (v66/v74): em cada ponto da cunha, o frame do
    contrato dá coframe dual e métrica soldada lorentziana — o consumidor `four_frame_gives_lorentz_metric`
    aceita o termo. -/
theorem feeds_finite_face (C : ContratoH2 W R) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    (C.E x)⁻¹ * C.E x = 1 ∧ LorentzByCongruence (solderMetric4 (C.E x)⁻¹) :=
  four_frame_gives_lorentz_metric (C.E x) (C.det_unit_on x hx)

/-- [DERIVED] ★ o arrasto propaga a inversibilidade ao longo da órbita (consistência de (C) com (D)). -/
theorem det_unit_along_orbit (C : ContratoH2 W R) (s : ℝ) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    IsUnit (C.E (wedgeBoostMap s x)).det := by
  rw [C.dragged s x hx, Matrix.det_mul]
  exact (boostMat_det_isUnit s).mul (C.det_unit_on x hx)

/-- [DERIVED] o vácuo de W É a imagem do vácuo da torre do perfil do estado, e é fixo por Δ^{it}
    (consistência de (S) com (Δ)). -/
theorem state_vac_fixed (C : ContratoH2 W R) (t : ℝ) :
    C.Δit t (C.stateIso (hOmega C.profile)) = C.stateIso (hOmega C.profile) := by
  rw [C.state_is_vac, C.Δit_vac]

end ContratoH2

/-- [DERIVED] ★★ A PAREDE GERAL: em qualquer par (W, R) cujas translações são triviais, o contrato H2
    é VAZIO — (B2) não tem testemunha. -/
theorem contratoH2_empty_of_trivial_translations (W : TGLSpecificAQFTWitness)
    (R : TGLModularRealization W) (hU : ∀ a : Fin 4 → ℝ, W.U a = 1) :
    IsEmpty (ContratoH2 W R) :=
  ⟨fun C => by
    obtain ⟨a, ha⟩ := C.translations_nontrivial
    exact ha (hU a)⟩

/-- [DERIVED] ★★ A PAREDE MEDIDA, no PAR LEGADO: sobre `theSpecificAQFTWitness` (U = 1) com
    `regularModularRealization`, o contrato H2 é VAZIO, por teorema. É a contraparte em kernel da
    identificação física ABERTA listada em um.py:162032
    (`geometric_BW_identification_for_legacy_wedge_data_U_equals_one`): com U = 1 a cláusula (B2)
    falha e o contrato é vazio. Não é a identificação BW em si (C6). Pagar H2 exige ANTES a
    partição M01 — outro par (W₀, R₀), ratificado pelo operador. -/
theorem contratoH2_empty_on_legacy_realization :
    IsEmpty (ContratoH2 theSpecificAQFTWitness regularModularRealization) :=
  contratoH2_empty_of_trivial_translations _ _ legacy_translations_trivial

/-- [DERIVED] ★ a cláusula (d) lida em kernel: se a ratificação escolher o PAR LEGADO
    (`regularFullWitness`), ela ratifica um alvo VAZIO por teorema. A cláusula tem de escolher OUTRO par. -/
theorem ratifying_the_legacy_pair_ratifies_the_void (F : FullTGLWitness)
    (h : F = regularFullWitness) : IsEmpty (ContratoH2 F.1 F.2) := by
  subst h
  exact contratoH2_empty_on_legacy_realization

/-! ## 3. As EXCLUSÕES ARITMÉTICAS de `theCurvedFrame` (o habitante genérico de v104) -/

/-- [DERIVED] ★★ `theCurvedFrame` NÃO é arrastado pelo boost: na entrada (1,0), com x = (0,1,0,0) ∈ cunha
    e s = 1, o lado esquerdo é 0 (diagonal) e o direito é sinh 1 ≠ 0. Pura aritmética. -/
theorem curvedFrame_not_dragged :
    ¬ ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
        theCurvedFrame.E (wedgeBoostMap s x) = boostMat s * theCurvedFrame.E x := by
  intro h
  have hx : (![0, 1, 0, 0] : Fin 4 → ℝ) ∈ rightWedge := by
    show |(![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp
  have h10 := congrFun (congrFun (h 1 _ hx) 1) 0
  rw [curvedFrame_E_apply, curvedFrame_E_apply] at h10
  simp [Matrix.mul_apply, boostMat, Fin.sum_univ_four, profileFn] at h10
  exact (Real.sinh_pos_iff.mpr one_pos).ne' h10.symm

/-- [DERIVED] ★★ a fiducial de `theCurvedFrame` NÃO é a direção modular: em x = (1/2, 1, 0, 0) ∈ cunha,
    a coluna 0 é (5/4, 0, 0, 0) e ξ_κ(x) = κ·(1, 1/2, 0, 0); a componente 1 força c·κ = 0 e a
    componente 0 força c·κ = 5/4. Pura aritmética, para todo κ. -/
theorem curvedFrame_fiducial_not_modular (κ : ℝ) :
    ¬ ∀ x ∈ rightWedge, ∃ c : ℝ, 0 < c ∧
        (fun i => theCurvedFrame.E x i 0) = c • killingField κ x := by
  intro h
  have hx : (![1/2, 1, 0, 0] : Fin 4 → ℝ) ∈ rightWedge := by
    show |(![(1/2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(1/2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp; norm_num
  obtain ⟨c, hc, hE⟩ := h _ hx
  have h0 := congrFun hE 0
  have h1 := congrFun hE 1
  simp [curvedFrame_E_apply, killingField, profileFn] at h0 h1
  rcases h1 with h1 | h1
  · exact hc.ne' h1
  · rw [h1, mul_zero] at h0
    norm_num at h0

/-! ## 4. CONTRATO H3 — o equilíbrio de horizonte local NO MESMO horizonte, com os números CALCULADOS -/

section H3Geometry

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- o ponto do horizonte esticado: x = (λ, ε + λ, y², y³). Para ε > 0 e λ > −ε/2 está NA cunha
    (onde o frame do contrato é suave): a família λ ↦ (λ, ε+λ) é a translação NULA da tela esticada
    ao longo do gerador k = (1,1,0,0) do horizonte da MESMA cunha. -/
def horizonPoint (ε l : ℝ) (y : Fin 2 → ℝ) : Fin 4 → ℝ := ![l, ε + l, y 0, y 1]

theorem horizonPoint_mem_rightWedge {ε l : ℝ} (hε : 0 < ε) (hl : -ε / 2 < l) (y : Fin 2 → ℝ) :
    horizonPoint ε l y ∈ rightWedge := by
  show |(![l, ε + l, y 0, y 1] : Fin 4 → ℝ) 0| < (![l, ε + l, y 0, y 1] : Fin 4 → ℝ) 1
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
  rw [abs_lt]
  constructor <;> linarith

/-- o gerador nulo do horizonte futuro da cunha: k = (1, 1, 0, 0). -/
def nullGenerator : Fin 4 → ℝ := ![1, 1, 0, 0]

/-- o bloco (2,3) de uma métrica: a métrica induzida na tela. -/
def screenBlock (g : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![g 2 2, g 2 3; g 3 2, g 3 3]

/-- a métrica soldada DO MESMO FRAME (v66/v74: g = eᵀ η e, e = E⁻¹). -/
def inducedMetric (C : ContratoH2 W R) (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  solderMetric4 (C.E x)⁻¹

/-- a ÁREA da tela S ⊆ aresta, transladada nulamente por λ sobre o horizonte esticado ε, medida
    pela métrica induzida DO MESMO FRAME: A(λ) = ∫_S √|det g_⊥(λ, ε+λ, y)| dy. -/
def screenArea (C : ContratoH2 W R) (S : Set (Fin 2 → ℝ)) (ε l : ℝ) : ℝ :=
  ∫ y in S, Real.sqrt |(screenBlock (inducedMetric C (horizonPoint ε l y))).det|

/-- a VARIAÇÃO DE ÁREA ao longo do gerador nulo: δA = dA/dλ |_{λ=0}. -/
def areaVariation (C : ContratoH2 W R) (S : Set (Fin 2 → ℝ)) (ε : ℝ) : ℝ :=
  deriv (fun l => screenArea C S ε l) 0

/-- o pareamento T(u, v) = uᵀ T v. -/
def pairing (A : Matrix (Fin 4) (Fin 4) ℝ) (u v : Fin 4 → ℝ) : ℝ := dotProduct u (A.mulVec v)

/-- o CALOR através do segmento [λ₀, 0] do horizonte da MESMA cunha, com o MESMO campo de Killing
    ξ_κ (Jacobson: δQ = ∫ T_ab ξ^a k^b dλ dA; ξ_κ ≈ κλ k perto da aresta). -/
def horizonHeat (C : ContratoH2 W R) (S : Set (Fin 2 → ℝ)) (ε l₀ : ℝ)
    (T : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) : ℝ :=
  ∫ l in l₀..(0:ℝ), ∫ y in S,
    pairing (T (horizonPoint ε l y)) (killingField C.kappa (horizonPoint ε l y)) nullGenerator

end H3Geometry

/-- **ContratoH3 W R** — o tipo que `qgPrice_H3_localHorizonEquilibrium_discharged` terá de habitar.
    Os cinco números de `HorizonEquilibriumData` deixam de ser LIVRES: κ é o κ do MESMO fluxo (H2);
    dA é a variação de área da tela da MESMA cunha na métrica DO MESMO frame; dS é a variação de
    entropia DO MESMO estado (o perfil `H2.profile` do estado de R, andar N) sob a perturbação; dQ é
    o calor do MESMO campo de Killing através do MESMO horizonte. Bekenstein–Hawking e Clausius são
    exigidas ENTRE os números calculados. `dA_ne` proíbe o balanço vazio 0 = 0. -/
structure ContratoH3 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W) where
  /-- o MESMO horizonte: o contrato H2 (fluxo, rede, estado, cunha, κ) sobre o MESMO par (W, R). -/
  H2 : ContratoH2 W R
  /-- G [INPUT] — a TGL prevê β, não G. -/
  G : ℝ
  G_pos : 0 < G
  /-- a tela: pedaço mensurável da aresta da MESMA cunha, de área positiva e finita [INPUT]. -/
  screen : Set (Fin 2 → ℝ)
  screen_measurable : MeasurableSet screen
  screen_pos : 0 < volume screen
  screen_finite : volume screen < ⊤
  /-- o horizonte esticado e o segmento nulo [INPUT]; o segmento vive NA cunha. -/
  eps : ℝ
  eps_pos : 0 < eps
  lam0 : ℝ
  lam0_neg : lam0 < 0
  lam0_in_wedge : -eps / 2 < lam0
  /-- a matéria [INPUT] e a perturbação do MESMO estado [INPUT]. -/
  matter : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  perturbed : SiteProfile
  level : ℕ
  /-- δA CALCULADO da MESMA cunha e do MESMO frame; e não-degenerado. -/
  dA : ℝ
  dA_eq : dA = areaVariation H2 screen eps
  dA_ne : dA ≠ 0
  /-- δS CALCULADO do MESMO estado: S(torre, andar N, perturbado) − S(torre, andar N, H2.profile). -/
  dS : ℝ
  dS_eq : dS = prefixEntropyIncrement H2.profile perturbed level
  /-- δQ CALCULADO do MESMO campo de Killing através do MESMO horizonte. -/
  dQ : ℝ
  dQ_eq : dQ = horizonHeat H2 screen eps lam0 matter
  /-- Bekenstein–Hawking entre os números calculados [KNOWN como exigência]. -/
  area_entropy : dS = dA / (4 * G)
  /-- Clausius com a temperatura de Unruh do MESMO fluxo [KNOWN como exigência]. -/
  clausius : dQ = (H2.kappa / (2 * Real.pi)) * dS

namespace ContratoH3

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- a PROJEÇÃO no tipo legado: todo contrato H3 É um `HorizonEquilibriumData` (o consumidor do
    teorema mestre), com κ := o κ do MESMO fluxo. -/
def toHorizonData (C : ContratoH3 W R) : HorizonEquilibriumData where
  kappa := C.H2.kappa
  G := C.G
  G_pos := C.G_pos
  dA := C.dA
  dS := C.dS
  dQ := C.dQ
  area_entropy := C.area_entropy
  clausius := C.clausius

/-- [DERIVED] o κ projetado é o do MESMO fluxo (por rfl) — não um número solto. -/
theorem toHorizonData_kappa (C : ContratoH3 W R) : C.toHorizonData.kappa = C.H2.kappa := rfl

/-- [DERIVED] o horizonte esticado do contrato vive NA cunha, onde o frame é suave. -/
theorem segment_in_wedge (C : ContratoH3 W R) {l : ℝ} (hl : C.lam0 ≤ l) (hl0 : l ≤ 0)
    (y : Fin 2 → ℝ) : horizonPoint C.eps l y ∈ rightWedge :=
  horizonPoint_mem_rightWedge C.eps_pos (lt_of_lt_of_le C.lam0_in_wedge hl) y

/-- [DERIVED] ★★ o contrato ALIMENTA o teorema mestre completo (v74): com um H1 qualquer e um ponto
    da cunha, a PÊNTADA conclui em termos do contrato — o tipo é consumível por
    `emergence_master_full_triad`, sem homônimo. -/
theorem feeds_the_master (C : ContratoH3 W R)
    {L : Type} [Lattice L] [BoundedOrder L] {T : SubadditiveTraceData L}
    (S : SusyRelativeData L T) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    (0 < T.tau S.ker ∧ T.tau S.ker < ⊤) ∧
      T.tau S.ker / T.tau S.ker = 1 ∧
      ((C.H2.E x)⁻¹ * C.H2.E x = 1 ∧ LorentzByCongruence (solderMetric4 (C.H2.E x)⁻¹)) ∧
      C.toHorizonData.dQ = C.toHorizonData.kappa * C.toHorizonData.dA
        / (8 * Real.pi * C.toHorizonData.G) :=
  emergence_master_full_triad S (C.H2.E x) (C.H2.det_unit_on x hx) C.toHorizonData

/-- [DERIVED] o 8πG de Clausius vale NO contrato com os números calculados. -/
theorem einstein_coefficient (C : ContratoH3 W R) :
    C.dQ = C.H2.kappa * C.dA / (8 * Real.pi * C.G) := by
  rw [C.clausius, C.area_entropy]
  exact einstein_coefficient_from_clausius C.H2.kappa C.dA C.G C.G_pos.ne'

end ContratoH3

/-- [DERIVED] ★★ no PAR LEGADO o contrato H3 também é VAZIO (herda a parede de H2). -/
theorem contratoH3_empty_on_legacy_realization :
    IsEmpty (ContratoH3 theSpecificAQFTWitness regularModularRealization) :=
  ⟨fun C => contratoH2_empty_on_legacy_realization.false C.H2⟩

/-- [DERIVED] ★ `theHorizon` (κ=1, G=1, δA=1) NÃO é a projeção de contrato algum no par legado: todo
    `ContratoH3` tem dA CALCULADO da MESMA cunha e exige um `ContratoH2` — e não há nenhum ali.
    (A exclusão de `theHorizon` é ESTRUTURAL — pela amarração —, não aritmética sobre os cinco
    números: cinco números soltos sempre podem ser realizados por algum horizonte em algum lugar.) -/
theorem theHorizon_is_not_a_contract_projection :
    ¬ ∃ C : ContratoH3 theSpecificAQFTWitness regularModularRealization,
        C.toHorizonData = theHorizon := by
  rintro ⟨C, _⟩
  exact contratoH3_empty_on_legacy_realization.false C

/-! ## 5. CONTRATO IMPORT-H3 — a ponte que PRODUZ H3 de H2 no MESMO horizonte, no MESMO par -/

/-- **ContratoImportH3 W R** — o tipo que `qgImport_H3_horizonEquilibriumData_produced` terá de habitar:
    uma função que, de cada contrato H2 em (W, R), PRODUZ um contrato H3 SOBRE O MESMO H2 (Jacobson
    1995 + BW + Unruh + Bekenstein–Hawking, importados). Substitui o homônimo `EquilibriumInput` (v253).
    ⚠ FURO 1 do cético (C1): quando `ContratoH2 W R` é vazio por teorema (o par legado), este tipo é
    habitável EX FALSO com axiomas limpos (`ProbeVacuousImportH3.lean`). Por isso o leitor exige
    (i) que essa sonda REPROVE e (ii) `gpi_H3 := gpi_H3 ∧ gpf_H2` — um import só vale com um H2 real. -/
structure ContratoImportH3 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W) where
  produce : ContratoH2 W R → ContratoH3 W R
  same_horizon : ∀ h2 : ContratoH2 W R, (produce h2).H2 = h2

/-- [DERIVED] ★★ com o import tipado, `the_trio_is_a_pair` instancia-se COM OS TIPOS: o teorema mestre
    sobre (H1, Nonempty ContratoH2, Nonempty ContratoH3) reduz-se a (H1, Nonempty ContratoH2).
    A dívida continua sendo DUAS: a H2, e a aplicabilidade do import AO MESMO horizonte (o campo
    `same_horizon`) — exatamente a errata C02. -/
theorem import_makes_the_trio_a_pair {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    (I : ContratoImportH3 W R) {H1 P : Prop}
    (master : H1 ∧ Nonempty (ContratoH2 W R) ∧ Nonempty (ContratoH3 W R) → P) :
    H1 ∧ Nonempty (ContratoH2 W R) → P :=
  the_trio_is_a_pair master (fun h => ⟨I.produce h.some⟩)

/-- [DERIVED] a honestidade herdada: o import sozinho não conclui nada sem a H2 — e no par legado a H2
    é vazia, logo o consequente do import nunca é alcançado por ele. -/
theorem import_reaches_nothing_on_legacy
    (I : ContratoImportH3 theSpecificAQFTWitness regularModularRealization) :
    ¬ Nonempty (ContratoH2 theSpecificAQFTWitness regularModularRealization) :=
  fun h => contratoH2_empty_on_legacy_realization.false h.some

/-! ## 6. Os `#print axioms` que o Audit passará a exigir (o molde de V350GateContract) -/

#print axioms sameFlow_is_the_regular_modular_flow
#print axioms legacy_flow_is_implemented
#print axioms sameNet_is_the_wedge_algebra
#print axioms wedgeBoostMap_mem_rightWedge
#print axioms jetFrame_det
#print axioms ContratoH2.feeds_finite_face
#print axioms ContratoH2.det_unit_along_orbit
#print axioms contratoH2_empty_of_trivial_translations
#print axioms contratoH2_empty_on_legacy_realization
#print axioms ratifying_the_legacy_pair_ratifies_the_void
#print axioms curvedFrame_not_dragged
#print axioms curvedFrame_fiducial_not_modular
#print axioms ContratoH3.feeds_the_master
#print axioms ContratoH3.einstein_coefficient
#print axioms theHorizon_is_not_a_contract_projection
#print axioms import_makes_the_trio_a_pair

end

end TGLExt.ContratoQG
