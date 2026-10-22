[INPUT/ONTO] Resposta limitada a Q2/C6, sem completar Q2, sem escolher partição, sem inferir assinatura física e sem misturar R_bal com Rraw. H0 e H1 custodiados não são reajustados. Os resultados escalar `CE*K/4` e vetor `7 CE*K δ_ab δ_cd/16` não são usados como ajuste do tensor métrico.

Não alcanço a fórmula tensorial fechada de

\[
CE\,K\,\delta\; T_{ab,cd,ef,gh}
\]

para o contato local densitizado de

\[
\mathcal E_x\bigl(H_{ab,cd}\bigr)\,H_{ef,gh}
\]

com o operador candidato

\[
\mathcal E=\sqrt g\,(\operatorname{roughBox}-2K\,\mathrm{Id}+2K\,g\,\mathrm{tr})
\]

e com o algoritmo `pair_delta` exatamente como fornecido. A etapa que impede é estrutural, não numérica:

1. `pair_delta` é um contrato **escalar**. Ele recebe listas `(coeficiente, perfil)` e palavras de derivadas `(lado, índice)`, aplica `jet`, escolhe `E.correction` ou `smooth_correction`, e devolve um escalar via `multiply(c*d,value)`. Ele não possui camada de índices tensoriais, contração métrica, nem produto tensorial de coeficientes.

2. A expansão métrica fornecida em `bilocal_first_curvature_engine.py` define `metric(o,a,b,c,e)` até primeira ordem em \(K\), mas isso não é ainda uma lista compatível com `pair_delta` do tipo
   \[
   H_{ab,cd}=\sum_r U^{(r)}_{ab,cd}\,f_r(w)+O(K^2).
   \]
   Faltam as listas explícitas \(U^{(r)}_{ab,cd}\) e as palavras de derivadas correspondentes ao operador de Euler métrico.

3. O operador `roughBox` métrico tem termos de conexão. Em RNC, esses termos são lineares em \(x\) no ponto de contato e contribuem para o coeficiente de \(\delta\) quando multiplicados por derivadas de \(1/w\). Eles **não** são palavras de derivadas parciais puras; precisam ser inseridos como coeficientes polinomiais extras. Esse módulo de conexão métrica não está nos trechos carregados.

4. O termo \(2K\,g\,\mathrm{tr}\) contrai o primeiro par de índices:
   \[
   H^m{}_{m,cd}=g^{mn}H_{mn,cd}.
   \]
   Isso acopla \(S_{ab,cd}\) e \(g_{ab}g_{cd}\) e exige uma contração de traço sobre a primeira linha que o `pair_delta` escalar não implementa.

5. Não há, nos trechos carregados, o código do caso vetor7 nem o módulo de Euler métrico que poderia calibrar a base tensorial. Portanto não posso inferir os coeficientes \( \alpha,\beta,\gamma,\delta \) da decomposição

\[
T_{ab,cd,ef,gh}
=
\alpha\,S_{ab,cd}S_{ef,gh}
+\beta\,S_{ab,cd}\,g_{ef}g_{gh}
+\gamma\,g_{ab}g_{cd}\,S_{ef,gh}
+\delta\,g_{ab}g_{cd}g_{ef}g_{gh}
\]

sem inventar resultado.

A redução formal que seria usada, se os módulos faltantes existissem, é:

\[
\langle \mathcal E_x H_{ab,cd}\,H_{ef,gh}\rangle_{\rm loc}
=
\sum_{r,s,w}
U^{(r)}_{ab,cd}V^{(s)}_{ef,gh}\,
\bigl\langle (C_w f_r)\,\partial_w\,g_s\bigr\rangle_{\texttt{pair\_delta}}
\,\delta(x),
\]

com \(C_w\) contendo densidade \(\sqrt g\), conexão e traço, e o coeficiente `CE*K*δ` sendo a parte linear em \(K\) dessa soma. Como \(C_w\), \(U^{(r)}\) e \(V^{(s)}\) não estão explicitados nos trechos fornecidos para o caso métrico, a fórmula fechada permanece inalcançável nesta chamada.

Conclusão: a pendência exata é a implementação/execução do **Euler métrico covariante com conexão e traço** acoplado ao `pair_delta`. Não afirmo que zerojet é loopQ2, não substituo o cálculo por ausência de anomalia 4D, e mantenho a ação apenas sobre a primeira linha.