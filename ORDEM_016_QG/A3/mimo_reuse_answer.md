# Inventário de assinaturas e comparação delimitada — campos geométricos de `ContratoH2` v3.1

## 0. Escopo e método

Comparo os sete campos geométricos de `ContratoH2` (ContratoQG_v31.lean:210–242) com os fornecedores nomeados, distinguindo: (a) fornecimento direto, (b) adaptação simples, (c) impossibilidade provada, (d) ausência. O rascunho `WedgeKillingNormalization_v4` é classificado como redundante / adaptação / não fornecido. Não rederivo geometria lorentziana, não toco campos modulares, BW ou energia positiva.

**Nota de status**: a compilação de `WedgeDraggedFrame_v6` com auditoria de axiomas no trio é **evidência fornecida pela bancada**; não executo ferramentas. `WedgeKillingNormalization_v4` é **rascunho não compilado** — trato suas provas como propostas.

---

## 1. Limitação de `theCurvedFrame` (verificação via `frame_ne_curvedFrame`)

Dois teoremas independentes excluem `theCurvedFrame.E` como candidato ao campo `E` de `ContratoH2`:

| Teorema | Arquivo/linha | Rota | Conclusão |
|---|---|---|---|
| `curvedFrame_not_dragged` | ContratoQG_v31_Teoremas.lean:713–723 | `dragged` | `theCurvedFrame.E` não é arrastado pelo boost (`sinh 1 ≠ 0` em l.723) |
| `curvedFrame_fiducial_not_modular` | ContratoQG_v31_Teoremas.lean:725–739 | `fiducial_is_modular` | a coluna 0 de `theCurvedFrame.E` não é proporcional ao campo de Killing (`profileFn` anula-se em l.738) |
| `frame_ne_curvedFrame_by_drag` | ContratoQG_v31_Teoremas.lean:745–751 | composição | `C.E ≠ theCurvedFrame.E` para todo `ContratoH2` |
| `frame_ne_curvedFrame_by_fiducial` | ContratoQG_v31_Teoremas.lean:753–759 | composição | idem, segunda rota |

**Escopo exato**: isto exclui **apenas** o frame particular `theCurvedFrame` (= `qgStrongCertificate_frame.1` = `existingSmoothFrame`). **Não conclui** que inexista outro frame no acervo. Em particular, `wedgeFrame` (WedgeDraggedFrame_v6.lean:10–11) satisfaz `dragged` e `fiducial_is_modular` (por `wedgeFrame_dragged` l.37–42 e `wedgeFrame_fiducial` l.44–48) e é candidato válido.

**Observação adicional sobre `ConcreteFourFrame`**: `modularFrame = 1` (ConcreteFourFrame.lean:71–75) é **constante**. Um frame constante invertível não pode satisfazer `dragged`, pois `M = boostMat s · M` para todo `s` forçaria `boostMat s = 1`, falso para `s ≠ 0`. Isto é observação algébrica direta, **sem teorema nomeado no acervo** — registro como tal.

---

## 2. Tabela campo / fornecedor / tipo / hipóteses / compatibilidade

Sete campos geométricos de `ContratoH2` (ContratoQG_v31.lean:207–242):

| # | Campo | Fornecedor principal | Tipo / Assinatura do fornecedor | Hipóteses do fornecedor | Compatibilidade com `ContratoH2` | Grau |
|---|---|---|---|---|---|---|
| 1 | `kappa_pos : 0 < kappa` (l.211) | `refRadius_pos` + def. κ | `refRadius_pos (N) : 0 < refRadius N` (Teoremas:441–447) | `N : KillingNormalization` (não requer `ContratoH2`) | Com κ := `1 / refRadius N`: `one_div_pos.mpr (refRadius_pos N)` | **Direta** |
| 2 | `observer_unit : minkowskiSq (killingField κ N.point) = 1` (l.232) | `observer_unit_of_index` | `minkowskiSq (killingField (1/refRadius N') N'.point) = 1` (Teoremas:474–484) | `N' : KillingNormalization` (não requer `ContratoH2`) | Com κ := `1 / refRadius N`, `N' := N`: idêntico | **Direta** |
| 3 | `E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ` (l.234) | `wedgeFrame` | `wedgeFrame (x) : Matrix (Fin 4) (Fin 4) ℝ` (WDF_v6:10–11) | Nenhuma (def. total) | Tipo idêntico | **Direta** |
| 4 | `smooth_on` (l.235) | `wedgeFrame_smooth` | `ContDiff ℝ (⊤:ℕ∞) (fun x => wedgeFrame x i j)` (WDF_v6:13–18) | `i j : Fin 4` | ContDiff → ContDiffOn via `.contDiffOn`; restr. a `rightWedge` | **Adaptação** (1-linha) |
| 5 | `det_unit_on` (l.236) | `wedgeFrame_det_unit` | `IsUnit (wedgeFrame x).det` (WDF_v6:34–35) | `hx : x ∈ rightWedge` | Hipótese idêntica ao campo; tipo idêntico | **Direta** |
| 6 | `dragged` (l.238–239) | `wedgeFrame_dragged` | `wedgeFrame (wedgeBoostMap s x) = boostMat s * wedgeFrame x` (WDF_v6:37–42) | Nenhuma (vale ∀ x) | **Mais forte** que o exigido (o campo pede `x ∈ rightWedge`); enfraquecer = descartar hipótese | **Direta** (enfraquecimento) |
| 7 | `fiducial_is_modular` (l.241–242) | `wedgeFrame_fiducial` | `∃ c, 0 < c ∧ (fun i => wedgeFrame x i 0) = c • killingField k x` (WDF_v6:44–48) | `hk : 0 < k`, x arbitrário | Instanciar `k := 1/refRadius N` (= κ), `hk := kappa_pos`; campo pede só x ∈ rightWedge (fornecedor é ∀ x) | **Adaptação** (instanciação) |

### Cobertura por arquivo

| Arquivo | `kappa_pos` | `observer_unit` | `E` | `smooth_on` | `det_unit_on` | `dragged` | `fiducial_is_modular` |
|---|---|---|---|---|---|---|---|
| **StrongFrame** (`theCurvedFrame`) | — | — | `theCurvedFrame.E` (mas excluído) | ✓ (adaptação) | ✓ (adaptação) | ✗ impossível (l.713) | ✗ impossível (l.725) |
| **ConcreteFourFrame** (`modularFrame`) | — | — | `modularFrame = 1` (constante) | ✓ (constante) | ✓ | ✗ impossível (algébrico) | ✗ impossível (col. 0 constante ≠ K(x)) |
| **StrongAssembly** (`qgStrongCertificate_frame`) | — | — | = `theCurvedFrame.E` (l.143–145) | ✓ | ✓ | ✗ | ✗ |
| **ConexoesExistentes** | — | — | = `theCurvedFrame.E` (l.12) | ✓ | ✓ | ✗ | ✗ |
| **WedgeDraggedFrame_v6** (`wedgeFrame`) | — | — | `wedgeFrame` (l.10–11) | ✓ (l.13) | ✓ (l.34) | ✓ (l.37) | ✓ (l.44) |
| **ContratoQG_Teoremas** (normalização) | `refRadius_pos` (l.441) | `observer_unit_of_index` (l.474) | — | — | — | — | — |

**Resumo**: os campos geométricos do frame (`E`, `smooth_on`, `det_unit_on`, `dragged`, `fiducial_is_modular`) são fornecidos **integralmente** por `WedgeDraggedFrame_v6`. Os campos de normalização (`kappa_pos`, `observer_unit`) são fornecidos por `ContratoQG_v31_Teoremas` (lema `refRadius_pos` e `observer_unit_of_index`). Os demais arquivos (`theCurvedFrame`, `modularFrame`, `ConexoesExistentes`) fornecem apenas `smooth_on` e `det_unit_on`, e são **excluídos** para `dragged`/`fiducial_is_modular`.

---

## 3. Classificação de `WedgeKillingNormalization_v4` (rascunho não compilado)

Cada declaração do rascunho (WedgeKillingNormalization_v4.lean:10–63), comparada com o já existente:

| Declaração (rascunho) | Linha | Classificação | Justificativa |
|---|---|---|---|
| `referenceRate` | l.10–11 | **Redundante** | É definicionalmente `1 / refRadius N`. O contrato já tem `refRadius` (Teoremas:439) e `kappa_eq_inv_radius` (Teoremas:458). |
| `reference_radius_positive` | l.13–18 | **Redundante** | Idêntico a `refRadius_pos` (Teoremas:441–447). Mesma prova (abs_lt + nlinarith). |
| `referenceRate_positive` | l.20–21 | **Redundante** | Decorre de `refRadius_pos` via `one_div_pos.mpr`. Mesmo conteúdo que `kappa_pos` para κ = 1/refRadius. |
| `referenceRate_unit` | l.23–30 | **Redundante** | Idêntico a `observer_unit_of_index` (Teoremas:474–484). Mesmo enunciado, mesma rota de prova. |
| `wedge_boost_hasDerivAt` | l.32–49 | **Novo** (não fornecido) | Prova que `HasDerivAt (fun t => wedgeBoostMap (k*t) x) (killingField k (wedgeBoostMap (k*s) x)) s`. Nenhum arquivo comparado contém este resultado. **Não é necessário** para os 7 campos geométricos (eles são identidades algébricas, não diferenciais), mas é genuinamente novo e útil para a relação infinitesimal boost↔Killing. |
| `geometric_fields_for_reference` | l.52–63 | **Bundle redundante** | Empacota os 4 itens redundantes + 3 adaptações de `WedgeDraggedFrame_v6`. Todos os componentes estão disponíveis em fornecedores existentes. Como pacote conveniente, é composição trivial; como teorema novo, não é. |

### Resumo quantitativo

| Classe | Itens | Linhas do rascunho |
|---|---|---|
| Redundante | 4 (`referenceRate`, `reference_radius_positive`, `referenceRate_positive`, `referenceRate_unit`) | l.10–30 |
| Novo (não fornecido) | 1 (`wedge_boost_hasDerivAt`) | l.32–49 |
| Bundle redundante | 1 (`geometric_fields_for_reference`) | l.52–63 |
| Adaptações embutidas no bundle | 3 (ContDiffOn, restrição, instanciação) | (dentro de l.52–63) |

---

## 4. Não circularidade

**Crucial**: distinguir lemas que **construem** `ContratoH2` dos que o **consomem**.

| Lema | Requer `ContratoH2`? | Usável para construir? |
|---|---|---|
| `refRadius_pos` (Teoremas:441) | Não (só `KillingNormalization`) | **Sim** |
| `observer_unit_of_index` (Teoremas:474) | Não (só `KillingNormalization`) | **Sim** |
| `wedgeFrame_smooth` (WDF_v6:13) | Não | **Sim** |
| `wedgeFrame_det_unit` (WDF_v6:34) | Não | **Sim** |
| `wedgeFrame_dragged` (WDF_v6:37) | Não | **Sim** |
| `wedgeFrame_fiducial` (WDF_v6:44) | Não | **Sim** |
| `kappa_mul_radius` (Teoremas:449) | **Sim** | Não (circular) |
| `kappa_eq_inv_radius` (Teoremas:458) | **Sim** | Não (circular) |
| `kappa_fixed` (Teoremas:466) | **Sim** | Não (circular) |
| `reindex` (Teoremas:487) | **Sim** | Não (circular) |
| `feeds_finite_face` (Teoremas:702) | **Sim** | Não (circular) |
| `det_unit_along_orbit` (Teoremas:706) | **Sim** | Não (circular) |

A composição proposta abaixo usa **apenas** lemas não circulares.

---

## 5. Plano mínimo de composição

Para `N : KillingNormalization` arbitrário admissível, os sete campos geométricos são montados assim:

**Passo 1 — Normalização de κ** (não circular):
- Definir `κ := 1 / refRadius N` (equivalente a `referenceRate N`)
- `kappa_pos := one_div_pos.mpr (refRadius_pos N)` — fornece campo 1
- `observer_unit := observer_unit_of_index N` — fornece campo 2

**Passo 2 — Frame** (não circular, tudo de `WedgeDraggedFrame_v6`):
- `E := wedgeFrame` — fornece campo 3
- `smooth_on := fun i j => (wedgeFrame_smooth i j).contDiffOn` — fornece campo 4 (adaptação: `ContDiff` → `ContDiffOn`)
- `det_unit_on := wedgeFrame_det_unit` — fornece campo 5 (direta)
- `dragged := fun s x _ => wedgeFrame_dragged s x` — fornece campo 6 (enfraquecimento: descarta `hx`)
- `fiducial_is_modular := fun x _ => wedgeFrame_fiducial κ kappa_pos x` — fornece campo 7 (instanciação de `k`)

**Nenhuma prova nova é necessária** para os sete campos. O único resultado genuinamente novo do rascunho (`wedge_boost_hasDerivAt`) não é requisito destes campos.

### Proposta textual de código (apenas a cola)

```lean
-- Todos os sete campos, montados de fornecedores existentes.
-- Para N : KillingNormalization arbitrário:
def geometricFields (N : KillingNormalization) where
  kappa     := 1 / refRadius N
  kappa_pos := one_div_pos.mpr (refRadius_pos N)           -- Teoremas:441
  observer_unit := observer_unit_of_index N                -- Teoremas:474
  E         := wedgeFrame                                  -- WDF_v6:10
  smooth_on := fun i j => (wedgeFrame_smooth i j).contDiffOn  -- WDF_v6:13 + adaptação
  det_unit_on := wedgeFrame_det_unit                       -- WDF_v6:34 (direta)
  dragged   := fun s x _ => wedgeFrame_dragged s x         -- WDF_v6:37 (enfraquecimento)
  fiducial_is_modular := fun x _ =>
    wedgeFrame_fiducial _ (one_div_pos.mpr (refRadius_pos N)) x  -- WDF_v6:44 (instanciação)
```

Isto **não** constrói `ContratoH2` completo (faltam os campos modulares `Δit`, `flow_implemented`, `kms`, `boost`, `bw`, `translations_continuous`, `translations_faithful`, `positive_energy`, `null_ergodic` — fora do escopo desta unidade). Fornece **apenas** os sete campos geométricos.

---

## 6. Síntese

| Pergunta | Resposta |
|---|---|
| Quais provas do rascunho são redundantes? | `referenceRate`, `reference_radius_positive`, `referenceRate_positive`, `referenceRate_unit` (4 de 6 declarações) — idênticas a `refRadius`/`refRadius_pos`/`observer_unit_of_index` do contrato |
| Quais são simples adaptações? | A cola para `smooth_on` (ContDiff → ContDiffOn), a restrição de `dragged`, e a instanciação de `fiducial_is_modular` — todas 1-linha |
| Qual parte não é fornecida? | `wedge_boost_hasDerivAt` (relação diferencial boost↔Killing) — novo, mas **não necessário** para os 7 campos geométricos |
| O frame `theCurvedFrame` serve? | **Não** — excluído por dois teoremas independentes (`frame_ne_curvedFrame_by_drag`/`_by_fiducial`). Mas isto **não** exclui outros frames. |
| Outro frame serve? | **Sim** — `wedgeFrame` (WedgeDraggedFrame_v6) fornece todos os 5 campos de frame. |
| Há circularidade? | **Não** — todos os fornecedores usados são não circulares (não requerem `ContratoH2`). |

Nenhuma bandeira, gate ou escolha física é alterada. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED ≠ CONFIRMED.