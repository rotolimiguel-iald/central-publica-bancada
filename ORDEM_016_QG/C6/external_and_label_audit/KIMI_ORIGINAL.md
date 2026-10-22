# ORDEM_016 A-7.b — resposta da bancada (artefato textual)

**Estatuto desta resposta:** `[DECLARADO]` integral, até verificação local. Nenhuma linha abaixo alega execução, compilação, medida ou recibo; tudo é derivação por escrito `[DERIVADO-por-escrito]`, a rodar. Auxiliar estritamente euclidiano em ℝ⁴; **não** se presume continuação lorentziana; nenhum original é alterado; **Q2 não é anunciada completa**; nenhuma definição de `A2` é trocada para obter fechamento; nenhum `W2` calculado é inventado — `W2`, `J2`, `W1`, `J1` permanecem simbólicos e o que se entrega é o **dicionário + o mapa de dependências**. As unidades anteriores (sinais Wick, correntes X/Y, identidade abstrata BV, enumeração de grafos Euler) não são repetidas.

**Lacunas declaradas antes de qualquer fórmula:**
- **GAP-1:** `full_loop_extension_engine.py` e `logarithmic_contact_engine.py` não foram lidos nesta chamada — só o arquivo `localized_source_boundary_engine.py` (sha256 `b9d91842…92410`, lido do contexto, não computado por mim). As convenções internas de `propagator_derivative`, `contact`, `dx`, `Q`, `x`, `z` são inferidas **do uso** `[DECLARADO por uso]`; o dicionário deve ser re-lido contra os módulos reais.
- **GAP-2:** o conteúdo interno de `V2` (quártico) não está no trecho; `Σ^tad` e `I2` ficam simbólicos na estrutura.
- **GAP-3:** os fatores combinatoriais (1/2 bolha, 1/2 tadpole, 1/3! vértice) são convenção a calibrar contra referência φ³/φ⁴ conhecida — verificação local pendente `[ABERTO]`.
- **GAP-4:** a existência de mistura ⟨h b⟩ depende do gauge-fixing efetivo; declarada como ramo condicional.

---

## 1. Convenções fixadas (o que o enunciado mandou fixar)

**(C1 — euclidiano, sem i):** nenhum fator `i` em propagação, vértice ou contato; `q := ∂δ` **sem** `i` (dado); `CE := −4π²` com `Δ f = CE·δ⁴` para `f = 1/z`, `z = x·x`. Toda ocorrência de `Δ` sobre `f` vira `CE·δ`; coeficientes sempre lidos em unidades de `CE`.

**(C2 — funcional gerador):**
```
Z_χ[j; h†,c†] = ∫ DΦ exp{ ħ⁻¹ [ −S_χ + ∫ j·Φ ] },
S_χ = S0 + g χV1 + g² χV2,   χ inerte (limite adiabático só no fim).
```
`j` acopla **só** aos campos propagantes `(h, b, c, b̄)`; `h†, c†` são fundo externo — **não propagam** (dado), portanto pernas `h†/c†` nunca recebem amputação nem Wick.

**(C3 — conectado e contagem de ħ):** `G^c := ħ log Z_χ = Σ_L ħ^L G^c_L`; vértice `1/ħ`, linha interna `ħ`, linha externa para `j` sem `ħ`; em ħg² vivem exatamente: bolha `V1–V1` (I=2, V=2), tadpole `V2` (I=1, V=1), tadpole `V1` (W1, ħg) e os 1PR construídos sobre ele (ħg² via elo extra).

**(C4 — 1PI por Legendre, derivada esquerda):**
```
φ := δG^c/δj ;   Γ[φ] := j·φ − G^c[j] |_{j(φ)} ;
Γ = S_χ + ħ W + O(ħ²),   W = g W1 + g² W2   (dado).
```

**(C5 — Grassmann/sinais):** paridade = gh mod 2: `c, b̄, h†` ímpares; `h, b, c†` pares. Toda reordenação de campos ímpares carrega o sinal da permutação; **cada loop fechado ímpar carrega −1 global** (regra STr). `s0` age como derivada à esquerda de grau 1: `s0(FG) = (s0F)G + (−1)^{|F|} F(s0G)`.

**(C6 — antibracket):**
```
(F,G) = ∫ Σ_Φ [ (δ^R F/δΦ)(δ^L G/δΦ*) − (δ^R F/δΦ*)(δ^L G/δΦ) ],
gh(F,G) = gh F + gh G + 1,
```
com a relação esquerda/direita declarada `δ^R F/δΦ = (−1)^{|Φ|(|F|+1)} δ^L F/δΦ`. Um sinal errado aqui é **detectável**: quebra o fecho WZ do §7.

**(C7 — fatoriais de vértice):** monômio `h³` de `V1` escrito **com** `1/3!`; monômios mistos (`χ b̄ C(L_c h)`, `χ h† L_c h`, `χ c† c·∂c`) **sem** fatorial; regra de vértice = derivada funcional total do coeficiente (kernel totalmente simetrizado). Fatores de simetria de grafo: **bolha de duas linhas entre vértices distintos: 1/2**; **tadpole num vértice: 1/2**. Calibração contra φ³/φ⁴ = pendência GAP-3.

**(C8 — normalização da inserção):** `[I]` é normalizada por `N_I: [I]_{árvore} ≡ I` (coeficiente 1); a parte 1-loop `J` usa **a mesma prescrição R** do lado dos T-produtos; qualquer contratermo finito adicional é **mudança de esquema**, registrada no ledger, nunca introduzida para fechar conta.

---

## 2. A cadeia de funcionais até ħg² — conectado → 1PI, com os sinais

**Setor livre:** `S0` quadrático em `(h,b,c,b̄)` + `h†·Gc` (`Gc_{μν} = ∂_μ c_ν + ∂_ν c_μ`). Propagador `D` = blocos `⟨hh⟩`, `⟨c b̄⟩` (e `⟨h b⟩` **se** o gauge misturar — GAP-4). Identidade-chave do lado BV: `s0 h† = δS0/δh =: E(h)` — o operador `einstein` do engine `[DECLARADO por uso]`.

**Conectado em ħg², setor quadrático externo:**
```
G^c_{1,2}|quad = (g²/2) ∫_{x,y} χχ ⟨T V1(x) V1(y)⟩_{2 linhas}
               + g²   ∫_x     χ  ⟨T V2(x)⟩_{tadpole}
               + L_1PR ,
```
**Ledger 1PR** (registrado, e **excluído** de `W2` pela Legendre):
- **L1:** `[tadpole V1](x) · D^{hh}(x,y) · [V1 árvore, 2 pernas h externas](y)` — setor `(h,h)`;
- **L2:** idem com o tadpole fantasma (valor com sinal −);
- **L3:** `[tadpole V1](x) · D^{hh}(x,y) · [χ h† L_c h: perna h no elo](y)` — setor externo `(h†, c)` em ħg²: **existe e alimenta a Ward no setor antifield**;
- **L4:** análogo no vértice `χ c† c·dc` — setor `(c†, c)`.
(Ordem g³ ou superior está fora. `⟨c h⟩ = 0` elimina os elos fantasmas alternativos.)

**Legendre no setor quadrático (o sinal, derivado):** se
`G^c|quad = (1/2) jDj + (ħg²/2) j D Σ^c D j` (`Σ^c` = kernel conectado amputado), então `φ = Dj + ħg² DΣ^cDj`, `j = Kφ − ħg² Σ^c φ` (`K := D⁻¹`), e
```
Γ|quad = (1/2) φKφ − (ħg²/2) φ Σ^c φ   ⟹   W2|quad = −(1/2) φ Σ^c φ .
```
**O 1PI é MENOS o amputado conectado** nesta convenção — consistente com `Γ1 = +(1/2) STr log`: a bolha direta entra com `+` do `STr log` e a mesma conta vem com `−` do lado conectado; as duas rotas fecham, e é isso que “preservar sinais” significa aqui.

**Os dois ingredientes de Σ^c:**
```
Σ^bolha_{ab}(x,y) = (1/2) V1_{,ace}(x) V1_{,bdf}(y) · K^{cd,ef}(x,y) · σ(cd,ef),
   K^{cd,ef} := R[ D^{cd}(x,y) D^{ef}(x,y) ]   (colocação de derivadas preservada, §6),
   σ = −1 se o par interno forma o loop c–b̄ (ímpar), +1 caso contrário;
Σ^tad_{ab}(x,y)  = (1/2) V2_{,ab cd}(x) · T^{cd}(x) · δ(x−y),
   T^{cd}(x) := R[ D^{cd} ](x,x)   (nunca “f(0)”; a coincidência é objeto de R).
```

---

## 3. Quando a bolha já é 1PI — e quando tadpole/amputação alteram o dicionário

- **Bolha V1–V1 (duas linhas, dois vértices distintos):** já é 1PI — nenhum corte de uma linha desconecta. Entra em `W2` **após amputação das pernas externas apenas**; a Legendre não toca nas linhas internas.
- **Tadpole V2 (auto-loop):** 1PI como grafo; entra em `W2`; seu kernel coincidente é `T^{cd}(x) = R[D^{cd}](x,x)`, não um número.
- **Tadpole V1 (uma perna externa):** **não** entra em `W2` — é `W1` (ħg). Em `G^c` ele aparece pendurado por um elo a um vértice árvore: isso é 1PR, **consumido pela Legendre**. **Mas re-entra em `A2` via `(V1, W1)`** (§5): o tadpole sai do dicionário da ação efetiva e volta pelo bracket — é exatamente o ponto do enunciado, agora formalizado. Quem o descartar “porque é 1PR” perde um termo da anomalia; quem o mantiver em `W2` conta duas vezes.
- **Amputação:** só age em perna propagante externa. Na **projeção externa h,c**: a perna de vértice tipo `b̄` lê-se como `c` externo via inversão do propagador fantasma `⟨c b̄⟩`; perna tipo `h` lê-se como `h`; pernas `h†/c†`: amputação = identidade. A projeção `Π_{h,c}` em si só é aplicada **depois** da forma normal (§7).

---

## 4. A inserção composta `[I]` até ħg²

```
I = (S,S)/2 = g I1 + g² I2,   I1 = s0 V1,   I2 = s0 V2 + (V1,V1)/2   (gh +1).
[I]·Γ = I(φ) + ħ J(φ) + O(ħ²),   J = g J1 + g² J2   (dado).
```
Com cutoff `χ` não-constante, `I1 ≠ 0` em geral (termos `∂χ`): **`J1` não é zerado por presunção** (ordem do enunciado respeitada). No setor quadrático externo:
```
J1 = T^{ren}(I1)                      (tadpole da inserção cúbica; 1 perna externa),
J2|quad = −(1/2) φ Σ^{I2} φ,   Σ^{I2}_{ab} = (1/2) (I2)_{,ab cd} T^{cd} δ(x−y)
```
— mesmo `T^{cd}`, mesma prescrição, mesmo sinal de Legendre. A parte árvore `I2` **não** entra em `A2`: cancela contra `(1/2)(S,S)|_{g²}` na QME. Distinção obrigatória no mapa: **tadpole de `V2` (loop de propagador) ≠ tadpole da inserção `I2` (loop sobre o vértice de inserção)** — podem cair nos mesmos monômios externos; são nós distintos.

---

## 5. Lado BV: `s0`, o bracket com sinal, `A1`, `A2`

```
s0 W_k = ∫ [ (Gc) δW_k/δh + (δS0/δc) δW_k/δc† + E(h) δW_k/δh† + (−b) δW_k/δb̄ ]
```
(derivadas esquerdas; `s0 c = s0 b = 0`, dados).

**Conteúdo de W1:** tadpole do vértice `h³` (perna externa `h`) **mais** tadpole do vértice `χ b̄ C(L_c h)` com a contração `⟨c b̄⟩` interna (perna externa `h`, sinal −). Os vértices `h†`- e `c†`- não geram tadpole (`⟨h c⟩ = ⟨c c⟩ = 0`). Logo `W1 = W1(h)` — **independente de Φ***.

**Consequência com o sinal exposto:** `(V1, W1)` não zera por Φ*-independência — zera só a **metade** do bracket:
```
(V1, W1) = − ∫ Σ_Φ (δ^R V1/δΦ*)(δ^L W1/δΦ)
         = − ∫ χ (L_c h)_{μν} · δW1/δh_{μν}
```
(usa `δV1/δh† = χ L_c h`; o termo `δV1/δc† = χ c·∂c` morre porque `δW1/δc = 0`). Leitura: **a variação de calibre não-linear do tadpole**, com o menos herdado de (C6). É o termo que o lado de correntes tem de reproduzir — não é ajustável.

```
A1 := s0 W1 − J1 ;   A2 := s0 W2 + (V1, W1) − J2   (dado; intocado).
```
`A1` é o **contato de não-comutação de R com s0 no loop de um vértice**: se a extensão comutasse com `s0`, `J1 = s0 W1` e `A1 = 0`; o que sobra é medida, não zero presumido.

---

## 6. Lado correntes (engine): kernel → funcional local

**Leitura do engine fornecido** `[DECLARADO por uso; GAP-1]`: `source_coefficients(u,v,r,η) → (A, B_j)` (estruturas de contração da fonte, com `dχ·b̄` restaurado pela troca da derivada única na linha Y interna); `source_reduced = A + Σ_j (dx_j B_j − η_j B_j)`; `einstein(h,d)` = E-L linearizado (`E(h)` do §2); `einstein_contact(h,λ)` = o mesmo com `dd(f,i,j) = contact(f,(i,j)) + λ_i contact(f,(j,)) + λ_j contact(f,(i,))`; `source_extension(r,λ,η) = expand(−ec + eY)`, com o shift `Q → Q − λ` e `E` agindo **como multiplicação por `Q`** após o shift (não `Q+λ`).

**Dicionário de saída → funcional local:**
1. **`Q` ↦ derivada na perna externa `h`**: monômio em `Q^α` lê-se como `∂^α h` (sinal por IBP na ordem fixada abaixo);
2. **contatos**: cada `c_α q^α` (`q = ∂δ`, sem i) integrado contra campos externos ↦ `c_α (−1)^{|α|} ∂^α` aplicado na estrutura externa do vértice do lado do `q`; **tabela CE**: `Δf ↦ CE·δ`; `(∂f)²`, `(∂²f)·f`, etc. ↦ **somente via R**; **`δ·f` proibido sem extensão definida** (ordem do enunciado); `δ·δ`: marcado `[ABERTO]` (singularidade acima desta ordem ou prescrição estendida a declarar);
3. **`λ`**: após o shift do engine, o representante local é a parte **λ-independente**; o resto vai ao **ledger λ** (dependência de prescrição; os termos `λ_i λ_j` de ordem zero comutam — docstring do engine);
4. **`η`**: jatos do cutoff Y; limite inerte `η → 0` **no fim**; termos η-dependentes ao ledger até lá.

**Os três kernels nomeados** (a distinção que o enunciado exige preservar): para cada par de linhas com derivadas `D^α, D^β`,
```
K1 = R[ (D^α D^{cd}) (D^β D^{ef}) ]        (R sobre o produto das derivadas)
K2 = [D^α R D^{cd}] · [D^β R D^{ef}]       (produto dos diferenciados estendidos, quando existir)
K3 = D^α D^β R[ D^{cd} D^{ef} ]            (derivadas fora)
```
com `K3 − K1 = C_{D^αD^β}(D^{cd}D^{ef})` (pela definição dada de `C_D`) e `K1 − K2` = contato de não-fatoração da extensão — **objeto próprio, não assumido zero**; se `D^α R D^{cd}` não existir isoladamente, `K2` é substituído pelo FP declarado e marcado. **Um regularizador de par** (um único `z^a` na distância relativa) regula `K1/K3` simetricamente e **não decide** `K1` vs `K2`, nem a aplicação do Euler a **uma só linha**: a aplicação assimétrica (Ward/Euler num vértice só) é um nó independente — é o nó de prescrição compartilhada **P0** do §8.

---

## 7. A identificação sem assumi-la

1. **Base de forma normal `{M_k}`**: construída a gh +1, nos setores `(c × ∂…∂h)`, `(h† × c,h)`, `(c† × c,c)`, `(b̄ × …)`; **truncamento em ordem de derivadas declarado** (hipótese H-trunc; a identificação vale dentro dele).
2. **Redutores**: IBP com ordem fixada (derivadas à direita sobre `h`, `c` ímpar mais à esquerda, sinal por transposição); Euler/E-L por campo; quociente por `s0`-exatos `A ~ A + s0B`. A comparação é feita **antes e depois** do quociente (duas linhas na matriz), para nenhuma discrepância se esconder dentro de um `s0B`.
3. **Projeção `Π_{h,c}`**: zerar `Φ*, b̄, b` **após** a redução. Os setores antifield ficam como **linhas de checagem**: a informação de Ward mora neles; projetar cedo destrói o teste.
4. **Matriz de comparação**: `Δ_k := a_k^{BV} − a_k^{curr}` sobre todos os setores. Desfechos:
   - **(i)** `Δ = 0` em todo setor: identificação verificada nesta ordem/setor — status que **só quem rodar** pode declarar; aqui permanece `[DECLARADO]`;
   - **(ii)** `Δ = s0 B + ∂Θ`: mesma classe, representantes distintos — registrar `B, Θ`;
   - **(iii)** `Δ` não `s0`-exato: discrepância genuína. Árbitros: **(a)** estabilidade de esquema `R ↔ R′` (trocar o fator `(1−a)`/escala `μ` por outra prescrição admissível: conteúdo físico move-se junto nos dois lados só por `s0`-exatos; discrepância estável é anomalia ou bug, não esquema) e **(b)** o **fecho WZ**: a identidade de Jacobi já escrita, `s0A2 + (V1,A1) + (W1,I1) + s0J2 + (V1,J1) = 0`, **avaliada com os objetos computados** (não re-enunciada como argumento): o lado que falha o fecho é o lado inconsistente. É assim que a identidade dada vira **detector**, sem repeti-la como conclusão.

---

## 8. Mapa de dependências (aplicável aos kernels dados)

```
P0  prescrição compartilhada: R(t) = FP_{a=0}[(1−a) μ^{2a} z^a t]; C_D(t) = R(Dt) − DR(t);
    regra do par vs linha-única (K1/K2/K3); N_I ([I]_árvore ≡ I).   ← nó raiz: se P0 difere
    entre os lados, a comparação é vazia por construção.
L0  kernels dados: f = 1/z; CE = −4π²; q := ∂δ; tabela Δf ↦ CEδ; proibições δ·f, δ·δ[ABERTO].
    [fonte: full_loop_extension_engine / logarithmic_contact_engine — GAP-1]
L1  setor livre: D = (S0'')⁻¹ nos blocos ⟨hh⟩, ⟨c b̄⟩ [, ⟨h b⟩ se GAP-4]; E(h) = einstein.
L2  T-produtos ħg²: K^{cd,ef} (bolha), T^{cd} (tadpole), C_D por kernel;
    derivados de: propagator_derivative, contact, dx, Q, x, z.
L3  funcionais: W1(h) [2 peças, sinal fantasma]; W2 = −(1/2)φΣφ, Σ = Σ^bolha + Σ^tad;
    ledger L1–L4 (1PR, fora de W2); J1 = T^{ren}(I1); J2 = −(1/2)φΣ^{I2}φ.
L4  álgebra BV: s0-rules (dados); (V1,W1) = −∫ χ (L_c h) δW1/δh;
    A1 = s0W1 − J1; A2 = s0W2 + (V1,W1) − J2 (intocado); WZ como teste.
L5  engine/correntes: source_coefficients → source_reduced → einstein_contact/einstein →
    source_extension; mapa Q↦∂h; q^α↦(−∂)^α externo; ledgers λ, η.
L6  forma normal + identificação: base {M_k}; IBP/Euler; quociente s0; Π_{h,c} tardia;
    matriz Δ_k; desfechos (i)/(ii)/(iii); discriminante R↔R′.
```
**Arestas críticas:** `W2 ← L2 + L1 + V1'''/V2''''`; `J2 ← I2 + T^{cd}`; `(V1,W1) ← W1 + pernas antifield de V1`; `L5` e `L3/L4` compartilham **apenas** `P0` e `L0` — nunca o resultado um do outro (é assim que a identificação não é assumida); `A2^{BV}` e `A2^{curr}` convergem só em `L6`.

---

## 9. Hipóteses, limites e o que esta resposta não é

**Hipóteses declaradas:** euclidiano ℝ⁴ (sem continuação presumida); χ inerte com limite adiabático ao fim; propagação sem massa com IR não endereçado `[ABERTO]`; base local truncada (H-trunc); gauge-fixing setorial como dado; o loop `h†-h-c` com `b̄-h-c` **já está no motor de fonte existente** — aqui reconhecido como conteúdo de `L5`, não apresentado como grafo novo.

**Esta resposta não é:** execução, compilação ou medida; não altera originais; não anuncia Q2 completa; não move nenhum gate; não troca `A2`; não inventa `W2` calculado; não ajusta coeficiente para cancelar resíduo conhecido; não usa concordância de modelos como prova. O passo que ela habilita é local: implementar `L3/L4` e o redutor de `L6`, ler `A2^{curr}` de `source_extension` via o dicionário do §6, e emitir a matriz `Δ_k` — cujo veredito, qualquer que seja, entra por medida, nunca por declaração.