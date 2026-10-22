[DERIVED — diferença Ward local parcial; REAL — CAS; OPEN — identidade completa]
# A7.b — inserção de gauge ordenada nos pares finitos
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T06:44:11.398178+00:00.

Inserimos G(v)=nabla v+(nabla v)^t diretamente nos vértices métrico e ghost,
preservando a ordem exterior-y / Taylor simetrizado / interior-x. Aplicamos
a Hessiana física E ao contato fonte covariante medido na entrega anterior.
Não substituímos cinco derivadas covariantes por momentos comutantes.

Na convenção comum contato/C, com a fase Fourier i separada, a combinação
-par_métrico/2 + par_ghost + E DeltaR, RELATIVA à referência harmônica, deu:

| ordem | base | coeficientes |
|---|---|---|
| K0 | p⁴Tpv, p²pTp pv, p⁴trT pv | ['-3167/17280', '-133/960', '749/17280'] |
| K1 | K[p²Tpv, pTp pv, p²trT pv] | ['-553/216', '-2897/1728', '6755/3456'] |
| K2 | K²[Tpv, trT pv] | ['-221189/12960', '29273/5184'] |

Este resultado NÃO é o coeficiente da anomalia completa. A referência
diferencial também pode ter imagem Ward; não foi demonstrada neutra.
O tadpole finito, os jatos W admissíveis e as valências superiores não
entram nessa soma. Um tadpole tau K² trh acrescentaria tau K²[G-gdiv];
tau não foi ajustado nesta medição. Nenhuma subtração foi adotada.

**Contagem exata:** 100 comparações de jatos planos, três verificações dos
ajustes e UMA validação nova com momento não axial = 104. As três
verificações dos ajustes não são três previsões independentes. No teste
não axial K1, p=(1,2,-1,1), v=(2,-1,1,3), T=e11, o valor medido e previsto
é 86045/1728. CPU 621.890625s; execução integral rc0.

Os novos adaptadores v2 apenas permitem injetar o provedor de jatos; a
reversão das duas alterações devolve exatamente os motores anteriores.
SHA de fontes, registro prévio, log e resultados constam no manifesto.
O próximo elo é calcular a contribuição da referência na MESMA prescrição,
sem apagar os harmônicos altos por não terem diferença local. Q2 OPEN.
