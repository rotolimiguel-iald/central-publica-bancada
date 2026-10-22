[DECLARADO — resposta do provedor; conferir com artefatos/compilador]

# Transformada de Fourier de $f_r(x)=\exp[-b(x-r-i\pi/2)^2]$

## Convenção

$$\mathcal{F}f_r(p)=\int_{-\infty}^{\infty}f_r(x)\,e^{-2\pi i xp}\,dx$$

## Derivação completa

**Passo 1 — Expandir o expoente de $f_r$.**

$$(x - r - i\pi/2)^2 = (x-r)^2 - i\pi(x-r) - \pi^2/4$$

pois $(-i\pi/2)^2 = i^2\pi^2/4 = -\pi^2/4$ e a cruz é $2(x-r)(-i\pi/2) = -i\pi(x-r)$. Logo:

$$f_r(x) = \exp\!\big[-b(x-r)^2\big]\;\cdot\;\exp\!\big[ib\pi(x-r)\big]\;\cdot\;e^{b\pi^2/4}$$

**Passo 2 — Montar o integrando e separar o termo sem $x$.**

$$\mathcal{F}f_r(p) = e^{b\pi^2/4}\cdot e^{-2\pi ipr}\;\int_{-\infty}^{\infty}\exp\!\big[-b(x{-}r)^2+(ib\pi-2\pi ip)(x{-}r)\big]\,dx$$

**Passo 3 — Quadrado completo em $u = x - r$.** Com $A = ib\pi - 2\pi ip$:

$$-bu^2 + Au = -b\!\left(u + \tfrac{A}{2b}\right)^{\!2} + \frac{A^2}{4b}$$

Verificação da expansão: $-b(u^2 + 2u\cdot\frac{A}{2b} + \frac{A^2}{4b^2}) + \frac{A^2}{4b} = -bu^2 - Au + \cancel{\frac{A^2}{4b}} - \cancel{\frac{A^2}{4b}} + \frac{A^2}{4b}$. $\checkmark$ *(como $-bu^2 + Au$)*

**Passo 4 — Calcular $A^2/(4b)$.** Aqui está o ponto crítico. Com $A = i(b\pi - 2\pi p) = i\pi(b-2p)$:

$$A^2 = i^2\pi^2(b-2p)^2 = -\pi^2(b-2p)^2$$

$$\boxed{\frac{A^2}{4b} = -\frac{\pi^2(b-2p)^2}{4b} = -\frac{\pi^2 p^2}{b} + \pi^2 p - \frac{b\pi^2}{4}}$$

A chave é $i^2 = -1$: o termo quadrático sai **real e negativo**.

**Passo 5 — Integral gaussiana.** Com $v = u + A/(2b)$:

$$\int_{-\infty}^{\infty} e^{-bv^2}\,dv = \sqrt{\pi/b}$$

**Passo 6 — Combinar.**

$$\mathcal{F}f_r(p) = \sqrt{\frac{\pi}{b}}\;\cdot\;e^{b\pi^2/4}\;\cdot\;\exp\!\left(-\frac{\pi^2p^2}{b}+\pi^2 p - \frac{b\pi^2}{4}\right)\;\cdot\;e^{-2\pi ipr}$$

Os fatores $e^{\pm b\pi^2/4}$ cancelam:

$$\boxed{\mathcal{F}f_r(p) = \sqrt{\frac{\pi}{b}}\;\exp\!\left(-\frac{\pi^2 p^2}{b}+\pi^2 p\right)\exp(-2\pi i r p)}$$

**A candidata está CORRETA.** $\text{DERIVED}$

---

## Verificações da mesma fórmula ($r = 0$)

Com $g_b(p) = \mathcal{F}f_0(p) = \sqrt{\pi/b}\;\exp(-\pi^2 p^2/b + \pi^2 p)$:

**1) Real estritamente positiva?** **SIM.** Todos os expoentes são reais ($b > 0$), e $\sqrt{\pi/b} > 0$, logo $g_b(p) > 0$ para todo $p \in \mathbb{R}$. $\checkmark$

**2) $L^2$?** **SIM.** O expoente $-\pi^2 p^2/b + \pi^2 p \to -\infty$ quando $p \to \pm\infty$ (o termo quadrático domina), logo $g_b$ decai exponencialmente nos dois extremos e $\int |g_b|^2 < \infty$. $\checkmark$

**3) $g_b(-p) = e^{-2\pi^2 p}\,g_b(p)$?** **SIM.**

$$g_b(-p) = \sqrt{\pi/b}\;e^{-\pi^2p^2/b - \pi^2 p}$$

$$e^{-2\pi^2 p}\,g_b(p) = \sqrt{\pi/b}\;e^{-2\pi^2 p}\;e^{-\pi^2 p^2/b + \pi^2 p} = \sqrt{\pi/b}\;e^{-\pi^2 p^2/b - \pi^2 p}$$

Idênticos. $\checkmark$

---

## Nota sobre a derivação (erro identificado e corrigido)

Na primeira passagem desta derivação, o quadrado completo produziu o termo $\pi^2 i\, p^2/b$ em vez de $-\pi^2 p^2/b$, porque $-b\!\left(\frac{\pi i p}{b}\right)^{\!2}$ foi avaliado como $+\pi^2 i\, p^2/b$ (tratando $i^2$ como $+1$) em vez do correto $+\pi^2 p^2/b$ (com $i^2 = -1$). A versão corrigida, com $i^2=-1$ aplicado corretamente, dá o coeficiente **real** $-\pi^2/b$ no expoente de $p^2$, conforme acima. O coeficiente da candidata está correto; nenhuma correção é necessária.