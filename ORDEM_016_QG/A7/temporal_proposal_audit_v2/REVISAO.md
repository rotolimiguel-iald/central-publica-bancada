[REAL — revisão local da proposta temporal; OPEN — prescrição causal completa]
# PM087 recebida do Kimi não está pronta para congelamento
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T00:42:58.822103+00:00.

O parecer foi lido integralmente e cotejado com suas fontes. O fundo da069
a=2cos(r/2), phi=id, não pode ser chamado de deSitter de raio2 para então
apagar phi. Para FLRW Lorentziano com fatias S3 unitárias, igualdade das
curvaturas seccionais exige a a''-(a')²-1=0. O perfil cos dá-2; o controle
cosh dá0. A inversão global da convenção de Riemann não muda essa desigualdade.
Não substituímos o horizonte: o teste087 continua o espaço-forma abstratoK>0.

A proposta confunde grau superficial omega com scaling degree sd. Em um
ciclo a um laço com n vértices de até2 derivadas, sd<=4n e dimensão relativa
4(n-1), portanto omega<=4, não4-4(n-1). Derivadas externas reduzem a cota
correspondente; inserções marcadas conservam sua própria contagem.
Não segue extensão única para n>=3. Contraexemplo crítico em aridade3:
|x|^-8 em R8 tem sd8; uma extensão pode mudar por c delta8. A integral radial
é logarítmica. A cota superficial também não diz quantos tensores locais existem.

Outras lacunas documentais: falta barc no multiplet, embora b tenha sido
incluído e chamado minimal; sqrt(kappa) altera nossa normalização e não é
real para todo kappa real não nulo permitido; Emax2 não segue de BV minimal;
mu, parametrix e hierarquia dos coeficientes finitos não foram efetivamente
fixados. A filtração quântica já medida permanece, sem reabrir truncamento falso.

CASv2:10checks,3afirmações rejeitadas,rc0,CPU0.21875s. A v1
falhou ao comparar uma expressão trigonométrica não normalizada: simplificar
deu -4cos(r/2)^2/(cos r+1); trigsimp(expand_trig(expand(...))) dá-2.
Não era contraexemplo físico. V1, preregistro e traceback preservados; v2
somente fixa essa normalização simbólica, sem mudar o alvo. Nenhuma nova
chamada de modelo. Relatar lista de escolhas faltantes não congela PM087.
