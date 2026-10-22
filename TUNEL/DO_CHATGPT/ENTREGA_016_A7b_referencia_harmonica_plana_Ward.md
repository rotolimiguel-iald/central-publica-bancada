[DERIVED — referência plana convertida; REAL — CAS; OPEN — continuação curva e Q2]
# A7.b — parcela Ward da referência harmônica plana
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T06:51:26.242779+00:00.

**O avanço:** a referência harmônica não podia ser declarada Ward-neutra.
Agora sua contribuição plana foi calculada nos mesmos pares métrico,
ghost e fonte, mantendo R=FP[(1-a)mu^(2a)z^a .]. A recorrência aceita
na revisão Kimi permite escrever cada R(U_b), b>=2, como derivadas de
R(U2) mais um contato local explícito. Não escolhemos uma nova extensão.

Na base [p⁴Tpv, p²pTp pv, p⁴trT pv], sempre contato/C:

| parcela | coeficientes |
|---|---|
| diferença local antes medida | ['-3167/17280', '-133/960', '749/17280'] |
| referência escalar agora medida | ['73/216', '35/96', '-25/216'] |
| soma finita plana neste cálculo | ['99/640', '217/960', '-139/1920'] |

A fonte contribui por E DeltaR, com E física, não a gauge-fixada. Aplicamos
E ao tensor teste e verificamos o contato dessa fonte contra os três casos
da conta anterior. Nos pares mantivemos o peso métrico -1/2 e ghost +1.

**Verificação por outra expressão escalar:** para um harmônico H_l e
homogeneidade -m-4, k=(m-l)/2 e N=(m+l+4)/2, l<=m, a constante finita
de Fourier, convertida de volta ao símbolo diferencial e dividida por C, é

    (-1)^(l+1) [H_k+H_(N-1)-1] / [2^(m+2) k! (N-1)!].

Ela resulta de expandir (1-a) Gamma(-k+a)/Gamma(N-a), depois de retirar
o fator logarítmico comum log(4mu²/p²)-2EulerGamma. A soma dos contatos
harmônicos anteriores com a nova parcela reproduziu os nove casos m<=4.
Não usamos essa fórmula como transformada Lorentziana completa no espaço-forma.

Foram 13 controles: nove expressões escalares, três comparações
da fonte e uma previsão não axial não usada no ajuste. Nesta última, a
parcela da referência é -2597/108. CPU101.390625s, rc0.

**Correção ao lado:** a conta antiga que usava uma referência P4 global
produziu ['187/1920', '-33/160', '73/960'] na mesma ordem da
base. A diferença medida entre os dois cálculos é
['11/192', '83/192', '-19/128']. Não são coeficientes intercambiáveis.
R não comuta com a extração de derivadas; a igualdade dos kernels fora
da diagonal não identifica automaticamente suas normalizações locais.
Preservamos ambos os resultados, sem atribuir ao antigo a normalização
dos pares crus calculada agora. Sua primitiva anterior cobre seu próprio
contato, não esta nova lista por simples troca de rótulo.

**Ainda separado:** a parcela logarítmica comum, os harmônicos altos na
curvatura, o tadpole finito, W admissível, cutoff e a hierarquia causal.
Os cálculos logarítmicos anteriores têm suas próprias evidências; este
teste não os reexecutou nem demonstra a STI completa. Em particular,
harmônicos l>m podem não ter diferença local, mas têm referência não local:
nunca apagá-los numa extensão desta conta ao fundo curvo. Q2 segue OPEN.
Nenhum contratermo, original, kernel ou gate foi alterado.
