[DECLARADO — resposta do provedor; conferir com artefatos/compilador]

### Relatório de Conferência Aritmética e Textual (IALD)

**Estatuto da operação:** Conferência formal, aritmética e textual restrita exclusivamente ao vetor JSON do inventário fornecido na requisição (ORDEM 016, A2.3.a). Não houve execução de código, compilação de arquivos Lean, prova independente ou acesso ao sistema de arquivos local. Os hashes, medições e compilações são dados da bancada `[INPUT / DECLARADO]`.

---

### 1. Tabela de Conferência do Inventário Fornecido

Fonte declarada: `core_transport_axioms.json` (SHA256: `fcdd62f6ba504ca9f31889e894aadf7fe6b0ce69803d4dcfd1d2fe5791868578`).

| Arquivo | Teoremas (`theorems`) | Impressos (`printed`) | Faltantes (`missing`) | Proibidos (`forbidden`) | Externos (`outside`) | Erros (`errors`) | Sorry (`sorry`) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `LightRayVerticalDecay_v4.lean` | 6 | 6 | `[]` (0) | `[]` (0) | `{}` (0) | 0 | `false` | PASSA |
| `LightRayBoundaryBalance_v3.lean` | 4 | 4 | `[]` (0) | `[]` (0) | `{}` (0) | 0 | `false` | PASSA |
| `LightRayFourierBoundary_v2.lean` | 3 | 3 | `[]` (0) | `[]` (0) | `{}` (0) | 0 | `false` | PASSA |
| `LightRayCoreMembership.lean` | 3 | 3 | `[]` (0) | `[]` (0) | `{}` (0) | 0 | `false` | PASSA |
| `LightRayCoreExtension_v2.lean` | 4 | 4 | `[]` (0) | `[]` (0) | `{}` (0) | 0 | `false` | PASSA |

---

### 2. Totais do Lote

* **Total de teoremas (`theorems`):** $6 + 4 + 3 + 3 + 4 = \mathbf{20}$
* **Total impresso (`printed`):** $6 + 4 + 3 + 3 + 4 = \mathbf{20}$
* **Campos `missing`:** Vazios (`[]`) em todas as 5 entradas (0 ocorrências).
* **Campos `forbidden`:** Vazios (`[]`) em todas as 5 entradas (0 ocorrências).
* **Campos `outside`:** Vazios (`{}`) em todas as 5 entradas (0 ocorrências).
* **Total de erros (`errors`):** $0 + 0 + 0 + 0 + 0 = \mathbf{0}$
* **Ocorrência de `sorry`:** `false` em todas as 5 entradas (nenhum `sorry` registrado).
* **Status geral do lote:** Todos os 5 itens com valor `"PASSA"`.

---

### 3. Divergências Encontradas

* **Divergências aritméticas:** Nenhuma. A contagem de teoremas declarados coincide estritamente com a de impressos ($20 = 20$).
* **Divergências estruturais:** Nenhuma. Não há violações registradas nos campos de integridade (`missing`, `forbidden`, `outside`, `errors`, `sorry`).

---

### 4. Julgamento da Frase

> **Frase analisada:**  
> *"20 declarações conferidas neste lote, todas cobertas; densidade permanece como hipótese"*

* **Veredito:** **CONCORDA PLENAMENTE COM OS DADOS.**
  1. *«20 declarações conferidas neste lote, todas cobertas»*: É aritmeticamente exato. Há 20 teoremas contabilizados e 20 impressos, sem discrepâncias, erros ou elementos em falta (`missing = []`).
  2. *«densidade permanece como hipótese»*: Concorda com a informação contextual declarada na ordem `[INPUT]`, que especifica que o último teorema do lote (`halfline_isotony_of_gaussian_density`) mantém `hdensity` como hipótese explícita, preservando o estatuto de hipótese e não de fechamento irrestrito.
