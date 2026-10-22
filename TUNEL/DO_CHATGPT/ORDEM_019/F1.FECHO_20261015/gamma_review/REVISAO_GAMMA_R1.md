# Revisão independente — elevação exponencial e Sexp

[REAL] **PASSA COM ESCOPO DE OPERADORES CONSTRUÍDOS**, sem achado material. Claim 845.

| Fonte | EXIT | Segundos | #print axioms | .olean idêntico |
|---|---:|---:|---:|---|
| ExponentialLiftR2.lean | 0 | 62.020 | 12 | True |
| ExponentialLiftPositiveR2.lean | 0 | 50.801 | 6 | True |
| ExponentialTomitaR2.lean | 0 | 50.246 | 9 | True |

Checker independente: EXIT 0, 79 declarações dos três módulos, incluindo auxiliares privados; apenas propext, Classical.choice e Quot.sound. Zero sorry. Logs guardam início/fim/segundos, comando, toolchain, LEAN_PATH e pinos antes/depois.

## Conferência

- **ExponentialLiftR2** — O gerador do grafo é o conjunto efetivo (e(f),e(Tf)), f em D(T), seguido do span complexo e clausura no produto F×F. A hipótese geral é T auto-adjunto no H1 existente. Ela fornece densidade do domínio e emparelhamento; combinados com totalidade exponencial, provam funcionalidade da clausura. Essa funcionalidade não é campo assumido.
- **Core e domínio** — O domínio é a projeção da clausura do grafo; o valor é escolhido e provado único. O LinearPMap resultante tem grafo igual à clausura, domínio denso e simetria. core_graph_sequence aproxima simultaneamente x e o valor do operador em F×F, portanto fornece um core de grafo genuíno. A ação exponencial e cada setor são calculados por termo. Isso não prova auto-adjunção da elevação nem identidade com toda construção espectral de segunda quantização.
- **ExponentialLiftPositiveR2** — A positividade é do operador canônico, não um enunciado sobre todo T auto-adjunto. WT(rootParameter/2), já construído e auto-adjunto, fornece um fator h com (f,h) e (h,TWf) em seu grafo pelo lema WT_double_graph_iff. O emparelhamento transforma a matriz inner(e(f),e(TWg)) em Gram dos e(h). Somas finitas dão inner(x,Lx) real não negativo; o conjunto dessa desigualdade é fechado, estendendo-a à clausura do grafo.
- **ExponentialTomitaR2** — Sexp=JF composto com canonicalLift tem o domínio efetivo da elevação. A identidade TW(SWf)=Jcandidate f e a fórmula de JF nos exponenciais preservam o core por flipJ(x,y)=(JFy,JFx); conjugação dos coeficientes é tratada. Continuidade preserva a clausura. Funcionalidade dá Sexp(D) contido em D e Sexp²=I em D. A descrição do grafo como pré-imagem por (x,y)↦(x,JFy) prova fechamento; densidade é herdada. Não há hipótese de involução da elevação disfarçada de conclusão.
- **Limite da identificação** — Sexp é um operador construído, fechado, densamente definido e involutivo, com Sexp e(f)=e(SWf). Igualdade Sexp=S_par, auto-adjunção de canonicalLift, suas identificações polares/modulares e KMS permanecem sem prova nestes três arquivos.

## Não vacuidade e alcance

[DERIVED] TW_selfadjoint é um termo previamente construído, não uma hipótese sem habitante. O domínio contém e(0)=Omega por exponential_mem_domain; Omega tem norma 1 na construção anterior. Não é um operador definido apenas no vetor zero.

Não se promove simetria/positividade/fechamento a auto-adjunção, nem se identifica Sexp com o Tomita do par. Os recibos anteriores e tentativas recusadas foram preservados e seus hashes conferidos. Originais, memória, produção e gate intactos; nenhuma chamada externa.
