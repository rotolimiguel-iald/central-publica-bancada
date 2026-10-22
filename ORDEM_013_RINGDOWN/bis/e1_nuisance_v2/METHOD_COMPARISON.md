# E1 — comparação de métodos e roteiro de leitura

[INPUT/OPEN] NÃO-CEGO. Nota preparada enquanto o agente principal executa v2; não contém resultados do ajuste. Nenhuma execução duplicada. Axiomas N/A; teoremas 0. Este arquivo e o formulário são auxiliares posteriores ao manifesto: não alteram o desenho pinado, a autorização ou a árvore E2.

## O que cada estimador responde

| Estimador | Resposta / covariável / peso | Papel e comparação legítima |
|---|---|---|
| WLS mediana, convenção gerência | y=mediana(dtau), x=σq90=(q95−q05)/(2×1,6449), w=σq90⁻² | Reproduzir somente o controle −0,061±0,068; +0,79±0,37; cov absoluta sem reescala por χ². Mesma população 31 ou 33, não misturar |
| WLS mediana/std | y=mediana(dtau), x=std(dtau,ddof1), w=std⁻² | Isola mudança da definição de largura em relação à linha anterior |
| WLS média/std | y=média(dtau), x=std(dtau,ddof1), w=std⁻² | Isola média versus mediana mantendo largura/peso |
| Momentos gaussianos de u | y=E[u], var=Var(u), x=std(dtau) ou 40/ρ; u=dtau−δL(Mf,χf,z) pareado | Aproxima a forma marginal por seus momentos, conservando cov(dtau,δL). Não substituir Var(u) por Var(dtau)+Var(δL) sem termo cruzado |
| KDE fullsample de u | Σlog p_i(u=c0+kx_i), com df e demais parâmetros integrados, h×0,7/1/1,4 | Primário condicional de forma marginal. Comparar com momentos no mesmo conjunto, leitura e covariável; controlar FFT com somas diretas |

Fontes de implementação: `prepare_e1.py:297` (controles WLS); `:331` (amostras pareadas/covariâncias); `:158` (KDE); `:219` (ajuste e momentos); `:455` (bandas); `:476` (comparações). Caminhos relativos a este diretório; hashes integrais ao final. Os fontes de cálculo da gerência foram apenas lidos como texto, não executados.

A decomposição entre as três primeiras linhas ajuda a explicar uma diferença com a gerência; a diferença restante para a KDE inclui assimetria/caudas e, para cada leitura, a transformação por amostra. Nenhuma dessas comparações seleciona uma leitura vencedora.

## Recepção do resultado, sem transformar saída em aprovação

1. Conferir SHA de resultado/receipt, manifesto e autorização; tempos e versões; registrar arquivo de falha se houver. Resultado existente não basta: cada célula tem estatuto próprio. Limite de threads foi solicitado por ambiente, **não verificado em runtime**.
2. Conferir 33 eventos sem duplicação e as listas 31/33; N por evento, covariância e fonte HDF. Confirmar que não houve descarte de draws ou imputação. β runtime e convenção BCW/QNM permanecem condicionais.
3. Conferir declarações Uniform por evento (não supor um único intervalo), parser e limites dos draws. Interseção de suportes é guarda conservadora mais restrita que a união induzida, não prior exato. Normalização do prior conjunto e eficiência de seleção permanecem OPEN.
4. Contar células publicadas, válidas e NÃO PAGO por motivo. Pelo desenho estático: 324 ajustes solicitados (9 referências/leituras calculáveis × 36 combinações); 891 controles KDE; 32 comparações leitura/população/covariável. São contagens **previstas**, não medidas. R-RAIZ-COHERENT e R-PROP são entradas OPEN adicionais, sem δ inventado. Recortes pequenos podem e devem falhar identificabilidade.
5. Conferir erro direto de logdensidade ≤0,002 por evento, massa KDE, distância de borda, Hessiana positiva, estacionariedade e dispersão multistart. Esses controles não calibram cobertura de intervalos ou eficiência de seleção. Falha deve continuar visível, inclusive quando não houver diagnóstico gaussiano na célula abortada.
6. Transcrever controle WLS e diferenças contra o JSON da gerência. Para cada leitura/covariável, mostrar c0,k,cov e c0/SE nominal, além das três bandas; não escolher apenas a banda favorável. Comparar recortes nominais por largura/corrida, lembrando sobreposição e seleção posterior à observação dos dados.

## E1.5 — frases permitidas e paredes

Modelo residual por leitura: dtau = δL(amostra) + c0 + kx; a referência GR usa δ=0 com **df livre e marginalizado**. Para cada população/covariável/banda, o formulário recebe d_GR=c0_GR/SE_local e d_L=c0_residualL/SE_local. São distâncias locais descritivas. O intervalo Wald local de c0_L pode conter/não conter zero, mas não é intervalo de posterior calibrado nem demonstra separação física de GR.

Formulação: “Na calibração NÃO-CEGA, com intercepto e slope livres, d_GR=… e d_L=…; a covariância é de curvatura local e a variação com banda é …. z calibrado permanece não disponível.” Para δL variável por amostra, não há um único δ a comparar ao intercepto sem convenção adicional. Efeito constante pode ser absorvido por c0. As estimativas GR/L usam os mesmos eventos: **não somar variâncias como se fossem independentes** para fabricar significância da diferença.

**Não LR/Bayes factor.** Não converter diferença de máximos em √(2ΔlogL), sigma, odds ou seleção de leitura. KDE marginalizada em df não é a restrição conjunta df=0. σ endógeno, SNR network distinto dos dois cortes de seleção, eficiência α desconhecida, ESS desconhecida e suporte global não verificado continuam explícitos. Offsets fixos: **PROIBIDA_COMO_TESTE**.

## Critérios ainda separados

E1.1 depende da saída e revisão numérica. E1.2 exige nota de leitura integral das fontes e não ganha função de seleção por ter um limiar conhecido. E1.3 conserva a injeção LVK com/sem44 como um ponto, não curva de viés. E1.4 requer C2/C5 como dois estimadores com N/erro. E1.5 fornece apenas distâncias locais descritivas neste desenho. Lacunas não contam como sucesso. Agente principal revisará cálculo; agente B revisará escopo, conforme comunicação recebida.

[DECLARADO — agente principal] Sessão exec41207, dez eventos lidos sem falha e projeção inicial 26,44 s <495 s. Não consultei a sessão nem reobtive essa duração. E2 está em construção, sem registro/nova PE; esta nota não registra E2.

UTC deste registro: 2026-09-22T19:55:31.376989+00:00

Fontes/hash calculados nesta preparação:

- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/prepare_e1.py` — `cce4cf36a0c5d8fb3a07a13f54c4e2d867aa495b0f76e739613df84d59b63e4f`
- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/PLAN.md` — `81409ab298b8d7f7a81fd67d8d0dd7f2c0c977ea5b66b8e115fdb059190eb634`
- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/DESIGN_MANIFEST.json` — `375ee6824bae3ab65dcf802904a3a025e7a43ac0f009d3a59a3fc09225925a83`
- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/AUTHORIZATION.json` — `29e80e5cc30ea83d1c0daff1adf4195b7bf4074e263a05249d24b7bd81c83892`
