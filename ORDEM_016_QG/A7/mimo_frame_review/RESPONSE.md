# Demonstração escrita — A7.b: composição frame↔coordenada nos dois motores

## 1. Derivação de `frame2` a partir de $e_a^i = \delta_a^i + K(Y^2\delta_a^i - Y_a Y_i)/6$

Seja $f_a^i(Y) = \frac{1}{6}(Y^2\delta_a^i - Y_a Y_i)$, de modo que $e_a^i = \delta_a^i + K f_a^i$.

**Primeira derivada:**
$$\frac{\partial f_a^i}{\partial Y_j} = \frac{1}{6}\bigl(2Y_j\,\delta_a^i - \delta_{aj}\,Y_i - Y_a\,\delta_{ij}\bigr)$$

**Segunda derivada (frame2):**
$$\frac{\partial^2 f_a^b}{\partial Y_i\,\partial Y_j} = \frac{1}{6}\bigl(2\delta_{ij}\,\delta_a^b - \delta_{ai}\,\delta_{bj} - \delta_{aj}\,\delta_{bi}\bigr)$$

O código define:
```python
frame2(i,j,a,b) = (2·[i=j]·[a=b] - [a=i]·[b=j] - [a=j]·[b=i]) / 6
```

Estes coincidem termo a termo. $\checkmark$ (em métrica euclidiana $\delta_a^b = \delta_{ab}$).

**Propriedades verificáveis algebricamente:**
- Simetria em $(i,j)$: $\text{frame2}(i,j,a,b) = \text{frame2}(j,i,a,b)$. $\checkmark$
- Simetria em $(a,b)$: $\text{frame2}(i,j,a,b) = \text{frame2}(i,j,b,a)$. $\checkmark$
- Traço: $\sum_a \text{frame2}(i,j,a,a) = \frac{1}{6}(8\delta_{ij} - 2\delta_{ij}) = \delta_{ij}$. $\checkmark$

---

## 2. Primeira derivada do frame em $Y=0$: anula-se

$$\frac{\partial f_a^i}{\partial Y_j}\bigg|_{Y=0} = \frac{1}{6}(0 - 0 - 0) = 0 \qquad \forall\, a,i,j$$

Consequência: em $Y=0$, os termos cruzados (uma derivada no frame, uma no propagador) da regra do produto **somem**. Restam apenas os termos puros de segunda derivada: $\partial^2(\text{frame}\times\text{prop}) = (\partial^2\text{frame})\cdot\text{prop} + \text{frame}\cdot(\partial^2\text{prop})$. Isto justifica que o código só precisa de `frame2` (não de um "frame1").

Além disso, `frame2` **não depende de $Y$** (é constante racional), o que confirma que é o jato de segunda ordem avaliado em qualquer ponto — e em particular em $Y=0$ após o anchoring.

---

## 3. Sinais por tipo de índice

### 3.1 Co-frame (inversa) para índice superior (contravariante)

O inverso de $e_a^i = \delta_a^i + K f_a^i$ é, a primeira ordem:
$$e^a_i = \delta^a_i - K f^a_i$$

Para um vetor contravariante $V^a$ no índice do fantasma em $X$:
$$V^a_{\text{frame}} = e^a_i\, V^i_{\text{coord}} = V^a - K f^a_i\, V^i$$

O código:
```python
f -= F(self.z*[a=c] - self.point[a]*self.point[c], 6) * coord(0,c,b,...)
```
computa $f \mathrel{-}= \frac{X^2\delta_{ac} - X_a X_c}{6}\cdot G_{cb} = f_a^c(X)\cdot G_{cb}$, isto é, **sinal negativo** para índice contravariante superior em $X$. $\checkmark$

### 3.2 Frame para índice covariante (covetor)

Para um covetor $\omega_a$ (derivada externa $\xi$ em $X$, ou índice do fantasma em $Y$):
$$\omega_a^{\text{frame}} = e_a^i\, \omega_i = \omega_a + K f_a^i\, \omega_i$$

O código para $\xi$ em $X$:
```python
f += F(self.z*[xi=c] - self.point[xi]*self.point[c], 6) * coord(0,a,b,c,...)
```
computa $f \mathrel{+}= f_\xi^c(X)\cdot G_{\ldots c}$, isto é, **sinal positivo** para covetor. $\checkmark$

### 3.3 Índice do fantasma inferior em $Y$ (covetor)

Corrigido por `frame2(i,j,b,c)` com sinal **positivo** na função `framed`:
```python
f += frame2(i,j,b,c) * coord(0,a,c,xi,yi,())
```
Isto é $\partial^2 e_b^c/\partial Y_i\partial Y_j \cdot G_{ac}$, transformação de covetor. $\checkmark$

### 3.4 Índice de $D_j h$ (derivada do vértice)

O índice derivada $k$ do vértice é covetor (direção de derivação), logo transforma com o **frame** (sinal positivo):
$$\partial'_k = e_k^l\, \partial_l \implies \frac{\partial^2 \partial'_k}{\partial Y_i\partial Y_j}\bigg|_{Y=0} = D_{kl}\,\partial_l$$

No `d2vertex`: $\sum_l D[l][k]\cdot V_l(h) = \sum_l D_{lk}\cdot V_l(h)$, sinal **positivo**. $\checkmark$

### 3.5 Verificação de simetria de $D$ no produto

Como $\text{frame2}(i,j,l,k) = \text{frame2}(i,j,k,l)$ (verificado acima pela simetria em $(a,b)$), temos $D[l][k] = D[k][l]$, o que torna a contração independente da ordem dos índices. $\checkmark$

---

## 4. Derivação de `d2vertex` a partir do frame

O vértice $V$ recebe um tensor simétrico $h_{ab}$ (índices de frame) e produz um covetor $V_k(h)$ (índice de derivação). Na formulação em frames:

$$V'_k = e_k^l\, V_l\!\bigl(e^{\mathsf T} h\, e\bigr)$$

onde $(e^{\mathsf T} h\, e)_{uv} = e_u^r\, e_v^s\, h_{rs}$ é o tensor transformado.

### Segunda derivada em $Y=0$

Usando $\partial e = 0$ em $Y=0$ (item 2):

$$\frac{\partial^2 V'_k}{\partial Y_i\partial Y_j}\bigg|_{Y=0} = \underbrace{\frac{\partial^2 e_k^l}{\partial Y_i\partial Y_j}\, V_l(h)}_{\text{correção no índice derivada}} + \underbrace{\delta_k^l\, \frac{\partial^2 V_l(h')}{\partial Y_i\partial Y_j}}_{\text{correção no tensor}}$$

**Termo tensorial:** $h' = e^{\mathsf T} h\, e$, logo em $Y=0$:
$$\frac{\partial^2 h'_{uv}}{\partial Y_i\partial Y_j} = D_{ur}\, h_{rv} + h_{ur}\, D_{vr} = (Dh + hD^{\mathsf T})_{uv}$$

Definindo $\text{changed} = Dh + hD^{\mathsf T}$, e se $V_l$ é linear em $h$: $V_l(h') = V_l(\text{changed})$.

**Termo do índice derivada:** $\dfrac{\partial^2 e_k^l}{\partial Y_i\partial Y_j} = D_{kl}$ (frame, sinal positivo — covetor).

**Resultado:**
$$\boxed{\;d^2V_k = V_k(\text{changed}) + \sum_l D_{lk}\, V_l(h)\;}$$

Que coincide exatamente com o código:
```python
out = G.vertex(changed)[1][k]
return lincomb((F(1),out), *[(D[l][k], G.vertex(h)[1][l]) for l in range(4)])
```

$\checkmark$ — derivado do frame, não por concordância com o código.

---

## 5. Multiplicidade: divisão por 2 para $a \neq b$

`tensor(a,b)` produz $h_{ij} = \delta_{ia}\delta_{jb} + \delta_{ib}\delta_{ja}$, que para $a \neq b$ tem **duas** entradas não-nulas ($(a,b)$ e $(b,a)$), ambas iguais a 1. Para $a = b$, uma entrada de valor 2.

A função `multiplicity(a,b) = 2` se $a \neq b$, `1` se $a = b$, e o fator $2/m$ no Ward dá:
- $a = b$: $2/1 = 2$ (um único componente diagonal)
- $a \neq b$: $2/2 = 1$ (evita dupla contagem do par simétrico)

A normalização do tensor simétrico é consistente: o "peso" de cada componente independente no somatório $\sum_a$ é uniforme. A verificação racional é que o traço do tensor reproduz a contagem correta:

$$\sum_{ij} h_{ij}^2 = \begin{cases} 4 & a = b \\ 2 & a \neq b \end{cases}$$

e $h_{aa}/1 = 2$, $h_{ab}/2 = 1$ para $a \neq b$ — pesos comparáveis. $\checkmark$

**Item de implementação (soma vazia em `frob`):** se `frob` calcula $\sum_{ij} A_{ij} B_{ij}$ sobre matrizes `empty`, a soma vazia deve retornar `Fraction(0)` (identidade aditiva de $\mathbb{Q}$), **não** `float(0.0)`. Uma saída float não certifica igualdade racional: `Fraction(0) != 0.0` em tipo, e um valor residual tipo $10^{-17}$ flutuante pode parecer zero sem sê-lo em $\mathbb{Q}$. Recomenda-se que `frob` sobre `empty` devolva `F()` explicitamente e que comparações de anulação usem `== F(0)`.

---

## 6. Confronto com integração por partes em coordenadas ($\sqrt{g} = 1 - KY^2/2$)

### Métrica a partir do co-frame

O co-frame é $e^a_i = \delta^a_i - K f^a_i$, e a métrica $g_{ij} = \sum_a e^a_i\, e^a_j$:

$$g_{ij} = \delta_{ij} - K\frac{Y^2\delta_{ij} - Y_i Y_j}{3} + O(K^2)$$

$$\det g = 1 - K Y^2 \implies \sqrt{g} = 1 - \frac{KY^2}{2} \quad \checkmark$$

### Divergência covariante

$$\nabla_\mu V^\mu = \partial_\mu V^\mu + \frac{\partial_\mu \sqrt{g}}{\sqrt{g}}\, V^\mu = \partial_\mu V^\mu - KY_\mu V^\mu$$

Em $Y=0$: $\sqrt{g}=1$, $\Gamma = 0$, e o termo de conexão explícito $-KY_\mu$ **anula-se**. A curvatura ($\partial\Gamma \propto R$) sobrevive — e é exatamente o que `frame2` captura.

### Confronto

| Fonte de correção em $O(K)$ | Coordenadas | Frames |
|---|---|---|
| Conexão $\Gamma$ | $-KY_\mu$ (anula em $Y=0$) | ausente (anula em $Y=0$) |
| Curvatura $\partial\Gamma$ | termos $\partial_a \gamma^j_{jr}$ em `coordinate_yward` | `frame2` em `framed` + `d2vertex` |
| Medida $\sqrt{g}$ | $1 - KY^2/2$ (anula em $Y=0$) | absorvida no frame |

As duas formulações são **complementares**, não aditivas: cada uma captura a mesma física (curvatura) na sua base. $\checkmark$

---

## 7. Status da conexão no Ward quando `d2vertex` é incluído

**Resposta: AUSENTE como termo explícito, COMPLETA via `frame2`, NÃO DUPLICADA.**

Raciocínio:

1. **Ausente como termo explícito:** Em coordenadas normais ($Y = 0$), $\Gamma^i_{jk}(0) = 0$. O termo de conexão $-KY_\mu$ da integração por partes também se anula. Nenhum termo $\Gamma$ explícito é necessário no Ward em frames.

2. **Completa via `frame2`:** A curvatura ($\partial\Gamma \neq 0$ em $Y = 0$) é capturada integralmente pelas correções de segundo jato:
   - No **propagador**: `framed` adiciona `frame2(i,j,b,c)` e `frame2(i,j,yi,c)` quando `len(word)==2`.
   - No **vértice**: `d2vertex` adiciona $D\cdot h + h\cdot D^{\mathsf T}$ (tensor) e $D_{lk}\cdot V_l$ (índice derivada).
   
   Juntas, cobrem todos os termos de $\partial^2(\text{frame}\times\text{prop}\times\text{vértice})$ em $Y=0$ (os termos cruzados com $\partial\text{frame}$ somem pelo item 2).

3. **Não duplicada:** Os termos $\gamma$ de `coordinate_yward` (derivadas da conexão em coordenadas) e os `frame2` de `framed`/`d2vertex` (curvatura em frames) representam a **mesma física em bases distintas**. No código, os motores ghost/metric usam exclusivamente a formulação em frames (sem termos $\gamma$); `coordinate_yward` é um módulo separado em coordenadas. **Não há sobreposição** na implementação.

⚠ **Alerta de duplicação potencial:** Se alguém incluísse simultaneamente os termos $\gamma$ de `coordinate_yward` **e** os `frame2`/`d2vertex` no mesmo cálculo, a curvatura seria contada em dobro. A separação atual dos motores evita isso.

---

## 8. Menor identidade racional que detecta sinal errado

**Identidade:** Para todo $a \in \{0,1,2,3\}$:
$$\sum_{j=0}^{3} \text{frame2}(a,j,j,a) = -\frac{1}{2}$$

**Cálculo explícito:**
$$\text{frame2}(a,j,j,a) = \frac{2\delta_{aj}\delta_{ja} - \delta_{ja}\delta_{aj} - \delta_{jj}\delta_{aa}}{6} = \frac{\delta_{aj} - 1}{6}$$

$$\sum_j \frac{\delta_{aj} - 1}{6} = \frac{1 - 4}{6} = -\frac{3}{6} = -\frac{1}{2}$$

Se `frame2` tiver sinal trocado ($D \to -D$): $\sum_j (-\text{frame2}(a,j,j,a)) = +\frac{1}{2}$.

**Consequência no Ward:** Este somatório alimenta a correção do índice derivada em `d2vertex`:
$$\sum_j \sum_l D_{lj}\, V_l(h) = \sum_l \Bigl(\sum_j D_{lj}\Bigr) V_l(h) = \sum_l \Bigl(-\frac{\delta_{al}}{2}\Bigr) V_l(h) = -\frac{V_a(h)}{2}$$

Com sinal errado: $+\frac{V_a(h)}{2}$. O Ward não se anula. A identidade $-\frac{1}{2}$ (racional exata) é o detector mínimo.

**Implementação:** Verificar `sum(frame2(a,j,j,a) for j in range(4)) == F(-1,2)` com `Fraction`, não `float`. $\checkmark$

---

## 9. Resumo das auditorias

| Item | Veredicto | Fundamento |
|---|---|---|
| `frame2` | **Correto** | $\partial^2 f_a^b/\partial Y_i\partial Y_j$ coincide termo a termo |
| Sinal índice sup. ghost em $X$ | **Correto (−)** | Co-frame: $e^a_i = \delta^a_i - Kf^a_i$ |
| Segundo jato do frame em $Y$ | **Correto** | Constante; 1ª derivada anula em $Y=0$ |
| Índice campo externo ($c_b$ em $Y$) | **Correto (+)** | Covetor: frame $e_b^j$ |
| Índice de $D_j h$ (derivada vértice) | **Correto (+)** | Covetor: frame $e_k^l$ |
| Divisão por 2 ($a \neq b$) | **Correto** | Contagem simétrica consistente |
| `d2vertex = V(changed) + Σ D·V` | **Correto** | Derivado de $V'_k = e_k^l V_l(e^{\mathsf T}he)$ |
| $\sqrt{g} = 1 - KY^2/2$ | **Consistente** | $g = \delta - K(Y^2\delta - YY)/3$ |
| Conexão no Ward (com `d2vertex`) | **Ausente + completa, não duplicada** | $\Gamma(0)=0$; `frame2` cobre $\partial\Gamma$ |
| Soma vazia em `frob` | **Item de implementação** | Deve retornar `Fraction(0)`, não `float(0.0)` |

**Conclusão:** A passagem coordenadas↔frames **preserva sinais e multiplicidades** na divergência implementada nos dois motores, para as verificações derivadas acima. O resultado é **DECLARADO** até revisão local independente. Nenhum código, kernel, gate ou prescrição foi alterado. PROVADA ≠ CONFIRMADA.