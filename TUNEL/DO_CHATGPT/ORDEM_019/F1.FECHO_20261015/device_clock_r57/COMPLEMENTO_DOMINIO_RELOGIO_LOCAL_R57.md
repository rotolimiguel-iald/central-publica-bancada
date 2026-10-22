# R57 — domínio, relógio local e leitura relativa

Autor: codex-device-clock-r57. Complemento novo de DERIVACAO_R57.md; não altera
o script nem as 34 verificações exatas custodiadas em SYMBOLIC_RESULT_R57.json.
R4 integral permanece aberto. Não é resultado de um detector real.

## Escopo exato das derivadas

[DERIVED — modelo finito] As fórmulas de z'(0), z''(0), phi''(0) e a diferença
entre duas preparações foram calculadas na truncagem **2×2×2** já usada pela casa.
Não são cálculos da patente bosônica inteira. Em particular, o fator
a_out a_out† é I-n_out nesse cutoff, enquanto é I+n_out na CCR bosônica.

[DERIVED — núcleo algébrico, alcance distinto] Há também uma obstrução algébrica
à identificação universal de sigma+ como eigenobservável na representação
bosônica, sem precisar transferir as derivadas finitas: tome o núcleo invariante
das combinações finitas de vetores de Fock, tensor C², e psi=|0,0,g>.
Todos os produtos polinomiais de H, J e dos cinco saltos usados nesta conta estão
definidos nesse núcleo. O termo da bomba dá
`<psi, i[Omega_Rabi(sigma++sigma-),sigma+] psi> = i Omega_Rabi`,
pois `[sigma-+sigma+,sigma+]=Z` e Z|g>=|g>. Os termos livre e JC têm expectativa
zero nesse vetor; cada dissipador também tem expectativa zero: os abaixadores
e J anulam psi, e o dissipador de Z é -2 sigma+. Portanto a expectativa de
`L†(sigma+) - i omega_OH sigma+` é i Omega_Rabi != 0.
Isso exclui a identidade de eigenoperador nesse núcleo comum, com bomba positiva.
Não demonstra geração/fecho de um semigrupo com operadores não limitados nem
transfere o contraexemplo de segunda derivada ao modelo bosônico inteiro.

## Um relógio local construído a partir da dinâmica completa

[DERIVED — análise local do modelo finito] Com a preparação válida rho0 de §3,
`z(t)=2 Tr(exp(t L) rho0 sigma+)` é analítica, porque L atua em espaço finito.
Como z(0)=a>0, existe vizinhança sem zeros onde se escolhe Log z com argumento
zero em t=0. Para phi(t)=Im Log(z(t)/a), os coeficientes já calculados dão

```
phi(0)=0, phi'(0)=omega_OH>0,
phi(t)=omega_OH*t + [Omega_Rabi*(gamma_OH+lambda)/a]*t² + O(t³).
```

Por continuidade de phi', existe intervalo local com phi'>0, logo leitura
estritamente crescente. Pelo teorema da função inversa real,

```
t(phi)=phi/omega_OH
       - [Omega_Rabi*(gamma_OH+lambda)/(a*omega_OH³)]*phi² + O(phi³).
```

Essa é uma leitura local de tempo calculada do gerador completo, com correção
de fase, não a imposição de exp(i omega_OH*t). O coeficiente angular inicial
continua sendo o parâmetro omega_OH do H. Não foi medido o tamanho do intervalo,
obtida monotonicidade global, calibrado o segundo, nem demonstrado o receptor
que lê exatamente z. O sinal pode ter zeros depois. Nenhum termo físico foi
suprimido; R4 exige ainda a realização e calibração no mesmo sistema.

## Lock-in e banda base

[REAL — leitura documental] O original JAN09 custodiado em
`continuity_r57/sources/SUPERCONDUTOR_JAN09_EXTRACT_R57.txt`, parágrafo154,
declara referência do lock-in de 1Hz a100MHz e leitura da saída relativamente
à entrada. Os parágrafos48,103–106 e168 declaram OH perto de1,667GHz.
Isso não autoriza dizer que esse lock-in recebe diretamente a portadora OH.
As especificações são declarações da fonte, não medição instrumental nesta unidade.

[DERIVED — hipótese LAB_PHASE_LOCKED_DRIVE] A transformação de quadro já
verificada implica `z_lab(t)=exp(i omega_d*t) z_rot(t)`. Um modelo adicional
de demodulação complexa ideal, por misturador/referência coerente, daria

```
b(t)=exp(-i omega_d*t)*z_lab(t)=z_rot(t).
```

A portadora externa cancela. O receptor relativo lê a amplitude/fase do envelope
ou uma frequência intermediária especificada pelo detector, não demonstra
omega_d como relógio interno. Se o envelope estiver estacionário, b é constante;
se evoluir, sua fase é a diferença relativa. Misturador, filtros, banda efetiva,
ruído e mapa do sinal óptico até essa variável complexa ainda precisam de contrato
e realização. A descrição documental do lock-in não fornece esses elos por si.

## Continuidade útil

A codificação `A_beta(z)=z*S(thetaMiguel beta)` preserva a abertura normalizada
da fronteira para z não nulo e aceita o sinal dinâmico completo acima, sem
substituí-lo por uma órbita angular escolhida. Sua prova algébrica é independente
da realização física do receptor. V0, Eref, Killing-kappa e omega_OH permanecem
grandezas distintas até a ponte que as identifique com unidades e domínio.
