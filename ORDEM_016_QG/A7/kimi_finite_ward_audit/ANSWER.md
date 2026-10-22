# A7.b — Contato Ward/Slavnov FINITO a O(ħ) no setor de dois campos externos (gravidade pura087)

**Estatuto do documento:** [DECLARADO — resultado até revisão local; DERIVED nas contas feitas aqui; REAL apenas onde se cita o registro das fontes]. Nenhuma execução é alegada: o script do §7 é entregável para a bancada. Nada aqui toca kernel, `um.py` ou gate.

**Recortes declarados de entrada:** (i) σ permanece classicamente restrito (não se integra σ nem se chama isso de equivalente); (ii) trabalha-se na região **χ = 1** do gauge de De Donder (`ell = 1/(2κ)`, `C* = −D`) — fora dela o setor longitudinal e seus contatos mudam; (iii) a parte principal é local plana; tudo que depende de curvatura (K, e os setores com propagadores σ não projetados) fica separado e não é computado; (iv) a anomalia completa de todos os produtos (item d da pergunta) **não** é calculada; (v) não se usa H⁴ clássico como coeficiente, não se adota a proposta PM087 anterior, não se alega unicidade por n ≥ 3, e não se finge que o coeficiente logarítmico UV fixa parte finita.

---

## 1. O setor e as identidades BRST exatas

Dados (das fontes `model_inputs/DERIVACAO_OPERADORES.md` e `ghost_bubble`), com `g = ḡ + h` **sem** reescala `h → √κ h`:

- `P h = □h − 2K h + 2K g tr h`, `B = −I_tr/(4κ)`, `H_gf = B·P`, `G_H = G_P·B⁻¹` (inversos conservam B);
- `Q v = □v + 3K v` (ghost), Hessiana Grassmann `[[0,−Q],[Q,0]]`, inversa `[[0,G_Q],[−G_Q,0]]`, contatos `QG_Q = G_QQ = id`;
- `K_gauge v = L_v g`; `C` = De Donder.

**Identidades exatas (não apenas principais)** [DERIVED, verificação algébrica direta]:

```
C ∘ K_gauge = Q        (C_ν(L_v g) = □v_ν + Ric_ν{}^σ v_σ = □v_ν + 3K v_ν;  principal: p² v_ν)
H ∘ K_gauge = 0        (invariância de difeomorfismo, linearizada)
H_gf ∘ K_gauge = ell·C* ∘ Q
```

Disto segue a **identidade de Ward de propagadores** (forma Redell/Fröb):

```
K_gauge ∘ G_Q = ell · G_H ∘ C*      (W1)
ell · C ∘ G_H ∘ C* = id              (W2)
```

e a **condição de ordem zero** do CAS das fontes: endomorfismo `−2K` (sem traço, mult. 9), `+6K` (traço, mult. 1) — que **não** é espectro da EDP nem escolha de estado.

## 2. A identidade de Ward de dois pontos (item a — fora da diagonal)

Com antifields externos, `b` sem laços, a STI a O(ħ), `(S, Γ¹) = 0`, projetada no setor de dois `h` físicos, toma a forma de self-energy:

```
Π ∘ K_gauge = 0      (a self-energy aniquila configurações de gauge pura)      (W3)
```

equivalente a (W1)–(W2) amputadas. As **duas** estruturas transversais possíveis na parte principal plana são `tr(TATB)` e `tr(TA)tr(TB)` com `T = I − ppᵀ/p²`.

**Estado do logarítmico (registro das fontes `metric_bubble_v2`, `ghost_bubble`):** com `A0 = 1/(8π²)`, na base `[trAB·p⁴, trA trB·p⁴, (pAp·trB+pBp·trA)p², pABp·p², pAp·pBp]`,

```
métrica/A0 = [71/60, 27/40, −19/30, −11/5, 26/15]
ghosts /A0 = [1/12, 7/48, −1/8, −1/12, 1/6]
(−m/2 + g)/A0 = [−61/120, −23/120, 23/120, 61/60, −7/10]
```

**Resíduo setorial da WTI logarítmica** [DERIVED aqui, por substituição algébrica de `A = K_p(v)` nas cinco estruturas]:

```
F_m(K_p(v), B) = (1/6) p⁴(pᵀBv) + (1/12) p⁴(p·v) trB
F_g(K_p(v), B) = (1/12) p⁴(pᵀBv) + (1/24) p⁴(p·v) trB
```

— as peças isoladas **não** são transversais; a combinação cancela na razão exata **2:1** nas duas estruturas, e a terceira combinação `(2c₃+c₄+2c₅)` já é zero em cada setor. (W3) vale para a parte logarítmica; é isto que a prescrição R pode quebrar por contatos.

## 3. A prescrição R e a Tabela de contatos (item b)

Prescrição fixada (não reauditada aqui): `R(u) = FP_a[(1−a) μ_R^{2a} z^a u]`, `z = x² − i0`, `+−−−`, `C := 4iπ²`, `□(1/z) = Cδ`. Propriedades usadas: `R(pu) = pR(u)` (multiplicativa), `R(∂u) ≠ ∂R(u)`, e as fórmulas da fonte `tensor_extension/DERIVACAO_TENSORIAL.md`.

**Tabela T — contatos por kernel (parte principal plana; `r_n = −1/[4^{n−1}(n−1)!(n−2)!]`, `Res U_n = C r_n □^{n−2}δ`):**

| # | objeto | identidade | contato (vs. regra formal) | valor |
|---|---|---|---|---|
| T1 | `1/z` | `R(1/z) = 1/z`, `□(1/z) = Cδ` | primitivo (Schwinger) | `Cδ = 4iπ²δ = iδ/(2A0)` |
| T2 | `□R_n` | `□R_n = 4n(n−1)R_{n+1} − 4(2n−1)Res U_{n+1}` | `−4(2n−1)Res U_{n+1}` | n=2: `+(3C/8)□δ`; n=3: `+(5C/192)□²δ`; n=4: `+(7C/9216)□³δ` |
| T3 | `R_n − D_n` | `R_n = D_n + (H_{n−1}+H_{n−2}−1)Res U_n` | resíduo de normalização | n=2: `0`; n=3: `−(3C/64)□δ`; n=4: `−(7C/2304)□²δ` |
| T4 | `R_{μν}` (posto 2) | `R_{μν} = (1/8)∂_μ∂_ν(1/z) + (1/4)η_{μν}R_2 − (C/32)η_{μν}δ` | **contato do traço** `−(C/32)η_{μν}δ` | omiti-lo ⟹ erro `+(C/8)δ` no traço `η^{μν}R_{μν} = R_2` |
| T5 | `∂_μ∂_ν(1/z)` | `= 8R_{μν} − 2η_{μν}R_2 + (C/4)η_{μν}δ` | contato de reescrita | `+(C/4)η_{μν}δ = iπ² η_{μν}δ`; traço: `Cδ = Cδ` ✓ |
| T6 | `[∂_μ, R](U_n)` | `= 2(c_{−1} − c_{−2})` | comutação derivada–R | potência pura: `−4(n−1)C r_{n+1} ∂_μ□^{n−2}δ` → n=2: `(C/8)∂_μδ`; n=3: `(C/96)∂_μ□δ`; n=4: `(C/3072)∂_μ□²δ` |
| T7 | `z R_n = R_{n−1}` | exato (multiplicativo) | nenhum | verificado n=3: `zR_3 = R_2` via `z□δ = 8δ` |
| T8 | EOM-linear (Fröb 158) | `T_{n+1}(F^n,h(Ht)) − T_n(F^n)⋆h(Ht) = iħn T_n(F^{n−1},δ_tF)` | contato EOM/antifield | não é licença para apagar `δ_tF` |

Notas honestas: (i) em T6, para kernels **com log** (os `D_n`), `c_{−2} ≠ 0` — os `c_{−2}` não estão computados nas fontes (a continuação meromorfa é insumo que elas declaram não construir); fica na lacuna L2. (ii) A recorrência T2 é consistente com `□D_{n−1} = 4(n−1)(n−2)D_n` graças à identidade harmônica exata `(n−1)(n−2)(H_{n−3} − H_{n−1}) = −(2n−3)`, válida para todo n [DERIVED, conferida no script]. (iii) Regra usada: `x_μ□^mδ = −2m ∂_μ□^{m−1}δ`.

## 4. A quebra Ward finita: montagem e a lacuna nomeada

Com `R`, a prova formal de (W3) falha exatamente onde usa: (α) `□G = Cδ` (T1) nos cancelamentos `q²/(q²)` — os "tadpoles de contato"; (β) derivadas passando por `R` (T6); (γ) reescritas de tensores homogêneos (T5) e o traço (T4); (δ) o contato EOM-linear (T8), que é o setor antifield da STI. A quebra finita é, portanto,

```
𝔚_R(A,B) := Π_R(K_gauge·, B) = ħ A0 · κ⁰ { w_m·[CT_□+CT_∂+CT_tr]_m + w_g·[idem]_g }  +  2iħ T_2(F, δ_tF)
```

com `w_m = −1/2`, `w_g = +1` (ponderação `(ħ/2)Tr log H − ħ Tr log Q`, fases Wick separadas, conforme o registro das fontes). **Sobre κ:** na expansão sem reescala, vértices `∝ κ⁻¹` e propagadores `∝ κ` ⇒ a bolha é `κ⁰` na parte principal (ressalva: a normalização absoluta depende do `V3` da fonte066, não incluído nos trechos; como `κ` é real não nulo e entra polinomialmente, a WTI se decompõe por grau de `κ` e cada grau fecha separadamente; os contatos da Tabela T são propriedades de kernel, κ-independentes, e entram com o κ do seu diagrama).

**Lacuna L1 (contração necessária, expressão verificável):** os valores de `[CT_*]` exigem as **η-traçadas dos vértices nos pares de linha interna**. Concretamente, na notação das fontes (`N_m = Tr(S0 W_A S0 W_Bᵀ)/16`, `W_A = 16κ V3`):

```
CT_m(A,B) = (C/64) · Σ_linhas λ=(i,k),(j,l) η^{iλ kλ} [W_A W_Bᵀ-traçada em λ com S0 na outra linha]
```

e, para o ghost, a traçada **é computável já** [DERIVED, conferível no script]:

```
η^{νρ} V_νρ(H,p,k) = −[ (p·H·r) + (r·k) trH + (k·H·r) − (r·p) trH/2 − (r·H·k) ],   r = k + p
```

**Lacuna L2:** as extensões de posto 4 (`x_μx_νx_ρx_σ/z⁶`, `x²/z⁵`) e seus contatos de traço, e os `c_{−2}` logarítmicos de T6 — sem elas e sem o `V3` explícito, o **coeficiente numérico total** de `𝔚_R` não fecha. O que fecha sem elas está nos §§2, 3, 5, 6.

## 5. A liberdade local D2 (item c): o que restaura e o que deixa de restaurar

Base de contratermos na ordem 2, **ghost 0, forma 4** (a quebra teria ghost 1/forma 4; um eventual gerador canônico BV, ghost −1, existe sse a quebra for exata):

```
ΔS_D2 = ∫ μ_g [ α₁ (R¹)² + α₂ Ric¹:Ric¹ + α₄ K R¹ + α₅ K² ]  +  gauge (C_νC^ν)  +  EOM (h*·(local)·h)
```

(com `Riem¹² = 2Ric¹² − (R¹)²/3 + t.d.` em 4D — Gauss–Bonnet linearizado é derivada total).

**Mapa para a função de dois pontos** [DERIVED, com as projeções T; conferido no script]:

```
Ric¹(A):Ric¹(B) = (p²)²/4 · [ tr(TATB) + tr(TA)tr(TB) ]
R¹(A) R¹(B)     = (p²)² · tr(TA)tr(TB)
R¹(A) = p² tr(TA)
```

donde `−61/30 Ric¹:Ric¹ + 19/60 R¹R¹ = (p²)²[−61/120 tr(TATB) − 23/120 tr(TA)tr(TB)]` — exatamente a forma T da combinação `−m/2+g`. Os termos `K R¹`, `K²` cobrem as estruturas com menos `p` (setor de curvatura, aqui separado e não computado); `C_νC^ν` só toca o setor longitudinal (W2); os termos EOM cobrem T8 por redefinição de campo.

**Veredito sobre a restauração (na ordem retida):**

1. **Restaurado já (sem dado novo):** a parte **não-local/logarítmica** de (W3) — cancela na combinação 2:1 (§2). A liberdade covariante D2 não precisa mexer nela.
2. **Restaurável por D2 na parte computada:** todos os contatos da Tabela T são **locais** (`□^mδ`, `∂□^mδ`, `ηδ`), logo polinômios locais em momentum — e o espaço desses polinômios (graus ≤ 4, Lorentz-pares) é **exatamente** o span de D2 acima. O contato do traço (T4) e os contatos `[∂,R]` (T6) são, por construção, **escolhas de extensão**: movê-los é mover-se dentro de D2 — não são, isoladamente, quebra física. O contato EOM (T8) é absorvido pelo setor antifield de D2.
3. **Ponto que decide (e que falta):** se os contatos totais, após as contrações L1–L2, forem **covariantes** (caem em `{Ric¹², (R¹)², KR¹, K²}`) ou **s-exatos** (gauge/EOM), a identidade linearizada é restaurada por escolha de D2, com ambiguidade residual = renormalização finita covariante legítima (não anomalia). **Critério verificável:** a quebra é restaurada sse a contração produzir apenas as estruturas `(p²)² tr(TATB)`, `(p²)² tr(TA)tr(TB)` e as K-subordinadas — o que o script testa como sistema linear, dados os coeficientes.
4. **O que NÃO se afirma:** que a restauração está fechada (depende de L1–L2); que algum log UV fixou parte finita; que há unicidade por n ≥ 3; e qualquer coisa sobre a anomalia completa (item d — fora de escopo). Se L1–L2 produzissem estrutura local **fora** da base, seria candidato local a anomalia — os dados disponíveis não a indicam (todos os contatos são `η,□,x` sobre `δ`, que estão na base).

## 6. Wess–Zumino na ordem retida

A condição de consistência é `s 𝔚 = 0` com `s² = 0` na ordem retida (`s h = L_c ḡ`, ordem `c¹h²`). Na base: os geradores covariantes são **Ward-neutros** na ordem retida —

```
Ric¹(K_p(v)) = 0,   R¹(K_p(v)) = 0        (WZ-2pt)
```

[DERIVED; conferido no script com componentes exatas] — e os termos EOM/gauge são s-exatos por construção. Logo `s 𝔚 = 0` na ordem retida, na parte computada. Isto **não** é prova em todas as valências.

## 7. Entregável computacional (a bancada executa; nada se afirma executado)

`a7b_ward_contacts_check.py` — Sympy puro, sem rede. Confere coeficientes, recorrências, traços, a aritmética da bolha, o mapa D2 e (WZ-2pt); **não** prova identidades distribucionais. **Controle obrigatório incluído:** a omissão do contato do traço tensorial, cujo erro deve ser exatamente `+(C/8)δ`.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# A7.b — conferencia algebrica dos coeficientes e contatos Ward (2 pontos, parte principal plana).
# ESCOPO: aritmetica e identidades algebricas; NENHUMA identidade distribucional e provada aqui.
# Convencao: C = 4 i pi^2, Box(1/z) = C delta, z = x^2 - i0, assinatura +---.
# Saida 0 sse nenhum FAIL. Uso: python a7b_ward_contacts_check.py
import sys
from sympy import Rational, symbols, simplify, factorial, I, pi, Matrix, zeros

F = []
def check(name, cond):
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond: F.append(name)

# ---------- base
C  = 4*I*pi**2
A0 = 1/(8*pi**2)
check("C*A0 = i/2", simplify(C*A0 - I/2) == 0)

# ---------- r_n, Res U_n, R_n - D_n ; recorrencia Box (T2, T3)
def Hn(j): return sum(Rational(1,k) for k in range(1, j+1))
def r(n):  return -1/(4**(n-1)*factorial(n-1)*factorial(n-2))
def resU(n): return C*r(n)
def RmD(n):  return (Hn(n-1)+Hn(n-2)-1)*resU(n)

check("T3: R_2 - D_2 = 0", simplify(RmD(2)) == 0)
check("T3: R_3 - D_3 = -(3C/64)", simplify(RmD(3) + Rational(3,64)*C) == 0)
check("T3: r_{n-1} = 4(n-1)(n-2) r_n (recorrencia D sem contato)",
      all(simplify(r(n-1) - 4*(n-1)*(n-2)*r(n)) == 0 for n in range(3,8)))
check("T2: identidade harmonica da recorrencia Box, n=3..7",
      all(simplify((n-1)*(n-2)*(Hn(n-3)-Hn(n-1)) + (2*n-3)) == 0 for n in range(3,8)))

# ---------- z R_3 = R_2 (T7), via zD_3 = D_2 + (3C/8)d e z Box d = 8 d
D2, D3, d0 = symbols('D2 D3 d0')
zR3 = (D3 + Rational(3,8)*C*d0) - Rational(3,64)*C*(8*d0)
check("T7: z R_3 = R_2 (= D_2)", simplify(zR3 - D2) == 0)

# ---------- tensor de posto 2 (T4) e CONTROLE DO TRACO
eta, R2s, d2 = symbols('eta R2 d2')
Rmn = Rational(1,8)*d2 + Rational(1,4)*eta*R2s - Rational(1,32)*eta*C*d0
tr_com = Rational(1,8)*C*d0 + Rational(1,4)*4*R2s - Rational(1,32)*4*C*d0
check("T4: traco eta^{mn} R_{mn} = R_2", simplify(tr_com - R2s) == 0)
tr_sem = Rational(1,8)*C*d0 + Rational(1,4)*4*R2s
check("CONTROLE (obrigatorio): sem o contato do traco, o erro e' exatamente +(C/8) delta",
      simplify(tr_sem - R2s - Rational(1,8)*C*d0) == 0)
check("T4<=>T5: d2(1/z) = 8 R_mn - 2 eta R_2 + (C/4) eta delta",
      simplify(8*Rmn - 2*eta*R2s + Rational(1,4)*eta*C*d0 - d2) == 0)

# ---------- [d_mu, R](U_n) (T6, potencias puras): -4(n-1) C r_{n+1} d_mu Box^{n-2} delta
def cont_dR(n): return -4*(n-1)*C*r(n+1)
check("T6: [d,R](U_2) = (C/8) d delta",        simplify(cont_dR(2) - C*Rational(1,8))    == 0)
check("T6: [d,R](U_3) = (C/96) d Box delta",   simplify(cont_dR(3) - C*Rational(1,96))   == 0)
check("T6: [d,R](U_4) = (C/3072) d Box^2 delta", simplify(cont_dR(4) - C*Rational(1,3072)) == 0)

# ---------- bolha: coeficientes e transversalidade (sec. 2)
cm = [Rational(71,60), Rational(27,40), -Rational(19,30), -Rational(11,5), Rational(26,15)]
cg = [Rational(1,12), Rational(7,48), -Rational(1,8),  -Rational(1,12), Rational(1,6)]
comb = [-cm[i]/2 + cg[i] for i in range(5)]
alvo = [Rational(-61,120), Rational(-23,120), Rational(23,120), Rational(61,60), Rational(-7,10)]
check("-m/2 + g = coeficientes registrados", all(simplify(comb[i]-alvo[i])==0 for i in range(5)))

def F5(c, A, B, p):
    trA, trB, trAB = A.trace(), B.trace(), (A*B).trace()
    p2  = (p.T*p)[0]
    pAp = (p.T*A*p)[0]; pBp = (p.T*B*p)[0]; pABp = (p.T*A*B*p)[0]
    return (c[0]*trAB*p2**2 + c[1]*trA*trB*p2**2
            + c[2]*(pAp*trB + pBp*trA)*p2 + c[3]*pABp*p2 + c[4]*pAp*pBp)
def Kg(p, v): return p*v.T + v*p.T

p = Matrix([1, 2, -1, 1]); v = Matrix([2, 0, 1, -1]); K = Kg(p, v)
bs = symbols('b0:10'); idx = [(0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]
B  = Matrix(4, 4, lambda i,j: bs[idx.index((min(i,j),max(i,j)))])
p2 = (p.T*p)[0]; pv = (p.T*v)[0]; pBv = (p.T*B*v)[0]; trB = B.trace()
check("residuo setorial metrica: F_m(K,B) = (1/6)p^4 pBv + (1/12)p^4 (p.v) trB",
      simplify(F5(cm, K, B, p) - (Rational(1,6)*p2**2*pBv + Rational(1,12)*p2**2*pv*trB)) == 0)
check("residuo setorial ghost:   F_g(K,B) = (1/12)p^4 pBv + (1/24)p^4 (p.v) trB",
      simplify(F5(cg, K, B, p) - (Rational(1,12)*p2**2*pBv + Rational(1,24)*p2**2*pv*trB)) == 0)
H = Matrix(4, 4, lambda i,j: Rational((i+2*j) % 5 - 1, (i+j) % 3 + 2))
H = H + H.T
check("WTI logaritmica: F_{-m/2+g}(K_p(v), H) = 0 (fora de no)",
      simplify(F5(comb, K, H, p)) == 0)
check("CONTROLE: peca metrica isolada NAO e' transversal", simplify(F5(cm, K, H, p)) != 0)
check("CONTROLE: sinal ghost trocado destroi o cancelamento",
      simplify(sum((-cm[i]/2 - cg[i]) for i in range(5))) != 0)

# ---------- mapa D2 (sec. 5) e WZ-2pt (sec. 6)
def Ric1(A, p):
    pA = A*p; p2 = (p.T*p)[0]
    return Rational(1,2)*(p2*A + p*(p.T)*A.trace() - p*pA.T - pA*p.T)
def R1(A, p): return (p.T*p)[0]*A.trace() - (p.T*A*p)[0]
check("WZ-2pt: Ric^1(K_p(v)) = 0", Ric1(K, p) == zeros(4))
check("WZ-2pt: R^1(K_p(v)) = 0",   simplify(R1(K, p)) == 0)
A2 = Matrix(4, 4, lambda i,j: Rational((i+3*j) % 4 - 1, (2*i+j) % 3 + 2)); A2 = A2 + A2.T
B2 = Matrix(4, 4, lambda i,j: Rational((2*i+j) % 5 - 2, (i+2*j) % 4 + 1)); B2 = B2 + B2.T
T  = Matrix.eye(4) - p*p.T/(p.T*p)[0]
X1 = (T*A2*T*B2).trace(); X2 = (T*A2).trace()*(T*B2).trace(); p4 = (p.T*p)[0]**2
check("Ric^1:Ric^1 = (p2^2/4)(X1+X2)",
      simplify(((Ric1(A2,p)*Ric1(B2,p)).trace() if hasattr((Ric1(A2,p)*Ric1(B2,p)),'trace') else (Ric1(A2,p)*Ric1(B2,p)).trace()) - p4/4*(X1+X2)) == 0)
check("R^1 R^1 = p2^2 X2", simplify(R1(A2,p)*R1(B2,p) - p4*X2) == 0)
check("-61/30 Ric:Ric + 19/60 RR = p4[-61/120 X1 - 23/120 X2]",
      simplify(-Rational(61,30)*(p4/4*(X1+X2)) + Rational(19,60)*p4*X2
               - p4*(-Rational(61,120)*X1 - Rational(23,120)*X2)) == 0)

# ---------- vertice ghost e sua eta-tracada (lacuna L1: peca ja computavel)
def Vghost(H, p, k):
    r = k + p; Hr = H*r; Hk = H*k
    return -Matrix(4, 4, lambda nu, rho:
        p[rho]*Hr[nu] + (r.T*k)[0]*H[rho,nu] + k[nu]*Hr[rho]
        - r[nu]*p[rho]*H.trace()/2 - r[nu]*Hk[rho])
k = Matrix([0, 1, -1, 2]); Hg = Matrix(4, 4, lambda i,j: Rational((i+j) % 3, (i+2*j) % 4 + 2)); Hg = Hg + Hg.T
V = Vghost(Hg, p, k); r = k + p
etaV = -((p.T*Hg*r)[0] + (r.T*k)[0]*Hg.trace() + (k.T*Hg*r)[0] - (r.T*p)[0]*Hg.trace()/2 - (r.T*Hg*k)[0])
check("eta^{nu rho} V_{nu rho} = formula fechada", simplify(sum(V[nu,nu] for nu in range(4)) - etaV) == 0)
q = p
Cnu = [ -((q.T*q)[0]*v[nu] + (q.T*v)[0]*q[nu] - q[nu]*(q.T*v)[0]) for nu in range(4) ]
check("C(L_v g) e' proporcional a p^2 v (sem termos (p.v)p; sinal = convencao i^2)",
      all(simplify(Cnu[nu] + (q.T*q)[0]*v[nu]) == 0 for nu in range(4)))

print()
print("TABELA (resumo): traco T4 = -C/32 eta d ; omissao = +C/8 d ; T5 = +C/4 eta d ;")
print("[d,R](U_2) = C/8 d_mu d ; [d,R](U_3) = C/96 d_mu Box d ; Box R_2 = 8R_3 + 3C/8 Box d.")
sys.exit(1 if F else 0)
```

## 8. Delimitação exata do que falta

1. **L1 — vértice métrico `V3` (fonte066, não nos trechos) e a contração dos contatos:** necessária para o coeficiente total de `𝔚_R`. Expressão verificável: `CT_m` do §4 (duas linhas internas, `η` no par de cada linha, `S0` na outra), mais a traçada ghost já fornecida.
2. **L2 — extensões de posto 4 e `c_{−2}` logarítmicos:** `R` de `x⁴/z⁶`, `x²/z⁵` com seus contatos de traço, e os polos duplos de T6 para kernels com log.
3. **Setor de curvatura (K, Λ = 3K):** separado, não computado — inclui as estruturas `K R¹`, `K²` de D2 e os propagadores com `−2K/+6K`.
4. **Fases Wick globais** da combinação `−m/2+g` (o registro das fontes as mantém separadas; aqui herdou-se a ponderação).
5. **χ ≠ 1:** não coberto.
6. **Anomalia completa (todas as valências):** fora de escopo desta unidade, por enunciado.

**Síntese em uma frase:** na ordem retida, a identidade de Ward de dois pontos é formalmente válida fora da diagonal (o logarítmico cancela 2:1, com resíduos setoriais `(1/6, 1/12)` e `(1/12, 1/24)`); a prescrição R injeta contatos **todos locais** (Tabela T: `Cδ`, `(C/8)∂δ`, `−(C/32)ηδ`, `(C/4)ηδ`, `+2iħ T_2(F, δ_tF)`, …), que pertencem à liberdade D2; D2 os restaura na parte computada, com Wess–Zumino fechada na ordem retida (`Ric¹(K) = R¹(K) = 0`); a restauração completa fica condicionada, com nome e endereço, às contrações L1–L2 — e **omitir o contato do traço tensorial custa exatamente `+(C/8)δ`**, como o controle registra.