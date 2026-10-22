# Q01 — medidas dos priors extras: preparação delimitada

Pedido ROOT2f83697e-2a4b-4b15-9397-83ecd29a42a6; identidade4f5a24b4-594d-4c6d-84f6-cd06dc4c6064 gravada antes do código. Início no mapa626. [REAL documental] Nenhum candidato foi importado ou executado; não existem AUTH, RUN_CLAIM, ROOT_DECISION ou resultado de cálculo nesta preparação.

## Recorte útil e alternativas

A dependência Q01/F1e menciona expressamente H3/H4 truncados, Jacobiano H5, plano/subidentificação e erros propagados. Q01 escalar já qualificou nove entradas dos serviços f820; Q01-THETA qualificou a integração externa e coleção. Nenhuma dessas unidades executou a composição dos operadores escalares df482 com os serviços. Esta preparação cobre essa composição em onze casos distintos, sem repetir unidades consumidas.

Alternativa A, escolhida: usar _analytic, _rd_quadrature e _Curve.peak originais e pinados, com restrições gaussianas afins unidimensionais explícitas e serviços f820 originais. H3/H4 têm primitivas analíticas; H5 é confrontado em r_d original, com regra fixa independente e limite clássico de resto.

Alternativa B: testar prepare_joint → integrate_at_fixed_theta em283×63, com C e X sintéticos completos. Esse é um próximo recorte distinto, dependente de runtime NumPy/backend e fixtures compatíveis. Não se inventou esse ambiente nem se abriu WSL nesta entrega. Esta unidade menor não finge substituir a alternativa B.

**Alcance exato:** testa reconstrução escalar do prior, reancoragem, máximo restrito, Jacobianos, casos constante/zero e falhas de serviço. NÃO executa _Curve.__init__, prepare_joint, evaluate_five ou integrate_at_fixed_theta; não testa sua montagem de vetores, escolha de direções/parâmetros ou suporte matricial. As propriedades do fixture não autenticam um PreparedJoint. A ligação integral permanece por qualificar.

## Curva e referências

O fixture é log L(x)=c−a(x−m)²/2, com a≥0. Para a>0 ele se realiza numa reta residual por r(x)=√a(x−m); portanto é uma restrição possível de uma geometria gaussiana afim. Essa construção justifica a curva de teste, mas não é execução da projeção283×63. Sua referência x0 fornece b=a(m−x0). O máximo restrito é calculado pela função _Curve.peak ORIGINAL, sem copiar o algoritmo. Somente log_likelihood vem da expressão escalar conhecida.

Defina F(a,m;l,u)=√(π/(2a))[erf(√(a/2)(u−m))−erf(√(a/2)(l−m))]. Para fator exp(tx), completar quadrados dá:

Integral exp[c−a(x−m)²/2+tx] dx = exp[c+tm+t²/(2a)] F(a,m+t/a;l,u).

As referências H3/H4 usam essa primitiva, sem chamar os serviços do candidato para obter o valor esperado. As diferenças de erf foram escolhidas em argumentos moderados. O uso de math.erf/log não é aritmética intervalar; tolerância de engenharia3e−8 em log e margem de arredondamento5e−12 são fixadas antes da execução.

| Caso | Curva e medida | O que verifica |
|---|---|---|
| B01 | a=400,m=0,01,c=0; β∈[−0,05;0,05],densidade10 | máximo interior e normalização pelo comprimento do prior |
| B02 | a=400,m=0,12,c=0; mesmo prior | máximo restrito no extremo0,05; reancoragem conserva a integral truncada |
| S01 | a=4,m=0,08,c=0 em δ=−5log10(1+s),s∈[−0,15;0,15] | λ=ln10/5; densidade λexp(−λδ)/0,30; inclui sinal, constante e deslocamento m−λ/a do máximo do integrando |
| R01 | a=10⁶,m=1/145,c=0 em q=1/r_d,r_d∈[130;160] | densidade1/(30q²), ancoragem e quadratura positiva; referência independente em r_d |
| F01/F02/F03 | a=0 e log L constante2/−3/5, nas três medidas próprias | prior normalizado conserva log L; nenhum serviço ou máximo deve ser chamado |
| Z01 | fixture declara suporte zero comum | −∞ com estatuto correto e sem serviço; não é underflow numérico |
| N01 | serviço sintético retorna identidade errada | SERVICE_ERROR, sem sucesso parcial |
| N02 | serviço sintético engole erro DOMAIN_ERROR do callback e retorna número positivo | QUADRATURE_CALLBACK_FAILED preserva exatamente a causa engolida |
| N03 | serviço sintético avalia um ponto válido, mas retorna área0 | QUADRATURE_ZERO_OR_UNDERFLOW; erro não vira ausência física de probabilidade |

F01–F03 cobrem o atalho de prior próprio normalizado; não exercitam os Jacobianos quando a=0. Z01 pressupõe o sinalizador de suporte e não o prova com uma matriz. As três respostas falsas de serviço são controles negativos explícitos, sem monkeypatch do df482/f820.

## Oráculo de H5 na coordenada original

A média esperada é (1/30)∫₁₃₀¹⁶⁰ exp[−a(1/r−m)²/2]dr. O harness usa Simpson composto de256 painéis fixos,257 avaliações, na variável r. O candidato integra na variável q e seu serviço é adaptativo; não compartilham rotina, malha ou Jacobiano de implementação.

Para justificar um limite independente do erro de discretização, escreva g(r)=−a(1/r−m)²/2, z=max|1/r−m| no intervalo e R=130. Limites de módulo:

- U1=az/R².
- U2=a/R⁴+2az/R³.
- U3=6a/R⁵+6az/R⁴.
- U4=36a/R⁶+24az/R⁵.

Como exp(g)≤1, a quarta derivada de exp(g) tem módulo ≤B4=U4+4U1U3+3U2²+6U1²U2+U1⁴. O erro da média de Simpson é ≤h⁴B4/180, h=30/256. O harness conserva esse valor e converte o intervalo positivo em margem logarítmica −log(1−erro/média). Soma a margem de arredondamento5e−12 e a tolerância de confronto3e−8; nunca relaxa a tolerância após observar resultado.

A desigualdade é analítica em aritmética real. Sua avaliação por float não é arredondada para fora e a margem de biblioteca não é um certificado: o resultado permanece qualificação finita de engenharia, não precisão uniforme ou prova intervalar.

## Orçamento e observabilidade

Onze entradas nos operadores df482. Quatro chamadas reais a f820 (três janelas e uma quadratura), três serviços negativos fabricados, quatro atalhos sem serviço. Tetos:3×4098+4097+2=16393 avaliações de serviço/callback,4105 leituras de log L e257 avaliações adicionais do oráculo em r. As contagens adaptativas reais são desconhecidas até uma execução autorizada; não são inferidas do teto.

As janelas são contadas por sys.setprofile sobre o integrand do arquivo f820 pinado, sem monkeypatch. O profiler é removido em finally. Na quadratura q, um wrapper conta as chamadas efetivas e recusa nós repetidos. Duplicação de coordenadas das sub-janelas não é alegada como medida: esse campo é null onde não foi investigado. Recibos de sucesso precisam concordar com as contagens observadas.

Runtime local C:\Python314\python.exe, flags -I -S -B -X utf8, biblioteca padrão. O supervisor é derivado do runner Q01 já pinado, em pasta/identidade novas; o runner antigo não é executado. Worker carrega bytes exatos de df482, f820 e harness, registra hash do código e vínculos das funções. Fonte e executável são pinados; fechamento de todas DLLs/biblioteca padrão não é reivindicado.

Um filho Windows oculto, sem shell, casos seriais. Prazo nominal30s desde main, cooperativo23s, espera25s e reserva de recolhimento. Não é tempo real garantido; inicialização do supervisor fica fora da medida. Sem Job Object de RAM/quota de disco: limites de avaliações e aceite de streams até64KiB não se apresentam como hard cap desses recursos.

## Custódia e comando candidato

O driver exige decisão futura ROOT ligada ao hash do manifesto e revisão independente; só depois cria RUN_CLAIM exclusivo antes do filho. Worker cria sua marca antes do carregamento científico. Output ou claim parcial/presente bloqueia repetição. Resultado do worker é provisório: aceitação exige exit0 externo do supervisor, recibo terminal PASS e ausência de registros de falha. Não há retry, fallback, alteração do output ou renomeação de unidade incerta.

Comando futuro, NÃO executado nesta preparação:

```powershell
& 'C:\Python314\python.exe' -I -S -B -X utf8 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_extra_prior_qualification_preparation\driver.py' --decision-sha256 '<SHA256_REAL_DA_FUTURA_ROOT_DECISION.json>'
```

O schema descritivo de decisão no contrato não é uma autorização válida. build_preparation.py apenas empacota, calcula hashes e analisa AST. Nenhuma importação candidata, cálculo, solver, observado, WSL, instalação ou provedor ocorreu nesta preparação. Originais e unidades consumidas permaneceram intactos.

## Coordenação e pendências

A comparação I02 entre joint._admission['prediction_admission_sha256'] e plan['assembly_admission_sha256'] deve preceder qualquer fundo. ROOT informou pela ferramenta oficial o reparo separado99e2bfa7-36b8-4e0f-92e7-1a6918e80591, mapa628, em revisão independente. Não o duplicamos nem o tratamos como guard/filesystem/runtime já qualificado. P3/empacotamento/imports também está com outro responsável.

Stack remoto: uma coordenação antiga/zero execuções, limites5/3/1, divergência de âncora/geração. Preview de provedor não é pertinente a esta unidade stdlib e não foi acionado. Não houve repin ou substituição de executor. Q01escalar, Q01-THETA, c435, ffd6, NC02 e demais terminais não são reabertos. Memórias globais e ledger permanecem sob consolidação ROOT.
