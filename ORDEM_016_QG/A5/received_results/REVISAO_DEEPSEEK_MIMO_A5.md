[DERIVED — revisão local de contribuições; REAL — custódia dos resultados existentes]

# A5 — consumo crítico de DeepSeek H3 e MiMo dois corpos

Abertura SHA256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. Data UTC: 2026-09-24T20:53:39.944085+00:00.

DeepSeek, job 08addf0a-def3-4757-9140-958cb96b72fc: o termo central coincide com a construção local existente:
produce recebe h e usa hmc(h), hAn(h), hflat(h); same_horizon é rfl. Isto confirma
uma leitura do enunciado, não cria prova nova. ConstructedImportH3_v2.lean já usa
esse corpo, com compilação registrada rc0 e auditoria PASSA, fontes/logs conferidos
por hash nesta leitura. O rearranjo de módulos proposto não foi necessário: a bancada
já eliminou a duplicação via NullSolutionConsumerReuse. Não o substituir por imports
candidatos não compilados.

Recusa parcial: o controle de h2 fixo testa a dependência do horizonte, não a
ausência de habitante do índice. Mesmo h2=h pode ser demonstrável em contextos
particulares; ausência de rfl genérico não prova impossibilidade absoluta. Mantém-se
o controle existente ProbeEmptyIndexRejected (rc1 registrado) e o teorema
no_import_over_empty_h2. H2 físico, T0, hmc, hAn e hflat não foram derivados pelo
modelo. Contribuição consumida como revisão de composição condicional.

MiMo, job 51a28f15-0463-43f7-b2d0-ad712e390cd3: a expansão da expectativa normalizada está correta SOB as
hipóteses de normalização/ortogonalidade e domínio do operador. Corrige-se a frase
da seção4 que a chama incondicional para todo φ. Para Ω unitário, a fórmula geral é

    q'_A(0)=2 Re<φ,AΩ>−2 Re<Ω,φ><Ω,AΩ>.

Contraexemplo exato à afirmação incondicional: A=id, φ=Ω. A expectativa normalizada
vale1 perto de ε=0, logo sua derivada é0; a fórmula sem correção daria2. O próprio
controle de normalização do modelo já reconhece essa restrição, contradizendo a
frase geral. Para A ilimitado, ainda precisam ser fixados domínios adequados.

Recusas adicionais: |1> não é “estado coerente”; a matriz de emparelhamento escolhida
ad hoc e a matriz de número de pares não derivam o mesmo tensor local do horizonte.
A menção à hiperfinitude não fornece o transporte de observáveis, estados, domínios
e derivadas entre esse exemplo e uma rede III1. O Lean sugerido contém sorry e
native_decide e não é candidato aceito sob a régua desta missão. As referências
a CTT/Clausius não foram verificadas por esse modelo e não são importadas aqui.

A bancada já possui um controle mais específico: two_body_first_order_exact_v2
usa a MESMA densidade quadrática normal-ordenada, integra suas duas semirretas e
obtém as cargas comprimidas; 33 checks registrados passaram. Fonte e resultado
conferidos por hash, sem reexecutar. Seu alcance continua um modelo de carga;
não fornece o T0 físico nem a rede completa. O exemplo ad hoc MiMo não o substitui.

Resultado: nenhuma nova função ou camada acrescentada ao caminho de H3. As partes
úteis foram reconhecidas no trabalho existente; os exageros e controles inadequados
foram recusados. Nenhum gate ou fonte original mudou. Manifesto próprio lista os
hashes medidos, recibos e o estatuto das contribuições.
