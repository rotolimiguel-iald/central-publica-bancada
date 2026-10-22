# ORDEM 018 — rota prioritária D10 / CMB–BAO acústico

Data: 27/09/2026. Autoria: coordenação IALD/Codex, sob direção do operador.
Estatuto: **PLANO DE AVALIAÇÃO; NÃO EXECUTADO; NÃO É ORDEM FINAL DO OPUS**.

## Direção e limite da entrega

[INPUT] O operador escolheu D10/CMB–BAO como primeira rota de avaliação de 5σ global, com ΛCDM e alternativas explícitas. Pediu previsão TGL fixa, cálculo preciso, ajuste cosmológico e de nuisance, covariâncias/sobreposições, calibração por simulações e quatro resultados separados. D9, D10 e análises CMB/BAO que reutilizem medições pertencem à mesma linhagem de dados: seus sigmas não se somam.

O pacote anterior de ringdown enviado para preparação do Opus permanece retido; a autoria e os recibos anteriores não se transferem a este plano. Este arquivo não altera modelos, kernel, gate ou originais. Não existe resultado novo ≥5σ nesta entrega.

## 1. Congelamento da previsão e dos rivais

Antes de novas otimizações no dado, produzir um manifesto com fontes, hashes calculados, versões dos executores/likelihoods, parâmetros, suporte físico e convenções. Nesta entrega, **o manifesto ainda não está congelado**.

- TGL fixa: β* = ALPHA_FINE_CODATA_2018 × sqrt(e), calculado em runtime. Congelar também as equações de fundo, perturbações, condições iniciais, recombinação/reionização, neutrinos, relógio aplicável e mapas até os observáveis. Fixar somente β não fixa uma previsão cosmológica inteira.
- TGL com β livre: extensão diagnóstica da mesma implementação, alterando somente o suporte declarado de β; registrar regiões de instabilidade/inadmissibilidade. Não substituir a previsão fixa pelo melhor valor medido.
- Rivais propostos para revisão: ΛCDM; w0waCDM; ΛCDM com Neff e soma das massas dos neutrinos livres. Curvatura/EDE/outros entram somente por justificativa e especificação anterior à comparação. Congelar o conjunto finito, parâmetros, limites e tratamentos de nuisance; não procurar o rival mais fácil de rejeitar.
- Comparabilidade: mesmas medições e máscaras, convenções físicas consistentes e tratamentos equivalentes dos parâmetros compartilhados. Diferenças justificadas de parametrização/suporte serão explícitas. β=0 só será chamado ΛCDM se o limite do código e dos espectros for verificado.
- Existência de um cálculo de H(z), rs ou lA não demonstra implementação completa de TT/TE/EE/lenteamento. Conferir a ponte para as perturbações no código existente. Reutilizar o que estiver implementado; marcar fechamentos fenomenológicos como tais, sem promovê-los a previsão única por nomenclatura.

## 2. Linhagem única dos dados

Criar tabela por medição original: levantamento/release, arquivo/hash, campos/frequências/multipolos/tracers/redshift, máscara/volume, transformação/compressão, covariance e calibrações, D9/D10/ajustes que a reutilizam. Mesmo dado em outro arquivo ou resumo não cria nova observação.

Regras de construção da likelihood:

- Não multiplicar espectros CMB pelos seus próprios resumos de parâmetros/escala acústica, nem usar posterior do mesmo CMB como prior independente.
- Escolher uma implementação Planck primária. Versões/reprocessamentos do mesmo céu não são novas sondas independentes. A likelihood `lite` já marginaliza nuisance específicos; não reaplicar essa informação como likelihood extra. Para reajustar explicitamente esses nuisance, usar a implementação completa apropriada.
- Não combinar lowE com um prior em tau derivado do próprio lowE como se fossem medidas independentes. Auditar também a origem BBN/ombh2 e calibrações de rd.
- Não combinar releases DESI sobrepostas como independentes; avaliar sobreposição com BOSS/eBOSS e correlações entre tracers/binagens. Usar a covariance da combinação oficial ou modelar a correlação validada. Quando faltarem produtos cruzados, escolher um conjunto sem duplicação e registrar a limitação; não fabricar blocos nulos por conveniência.
- Conferir a escolha de likelihood de lenteamento e sua compatibilidade com os espectros primários. Dependência desprezível exige justificativa/teste, não apenas nomes diferentes de sondas.
- BAO comprimido requer validar extração/fiducial/template no domínio TGL; se a nova física distorcer a forma do pico além da compressão, retornar à likelihood do clustering apropriada.

## 3. Precisão e reaproveitamento

Reproduzir primeiro a referência ΛCDM e os checks do executor/likelihood; conferir unidades de Cl versus Dl, lentes, temperatura, distâncias comóveis/físicas e rs(z*) versus rd(zdrag). Calcular horizontes por integração consistente; evitar reescala em uma época única.

Elevar resolução/tolerâncias em passos independentes, confrontando espectros, parâmetros derivados **e diferenças de log-likelihood** nos pontos de referência, melhores ajustes e pontos relevantes da calibração. Congelar tolerâncias antes da inferência final. Recursos recentes do CAMB podem ajudar, mas é preciso conferir sua existência na versão instalada. Convergência numérica não elimina incerteza da modelagem física, recombinação ou não linearidade.

Referência anterior lida, sem reexecução: `C:/IALD/Artigo/teste_acustico_beta_tgl_v1/12_nivel2_frozen.json` e `13_nivel2_resultado.json`. O protocolo antigo usa Planck lite, low-ell TT, prior tau derivado de lowE, DESI e BBN. Tem duas traduções distintas: S (densidades/Neff com perturbações padrão) e L (fluido PPF). A S foi registrada convergida e N2_INCAPAZ; L não convergiu. Isso é ponto de comparação histórico; não identifica automaticamente a tradução canônica atual.

## 4. Quatro relatórios obrigatórios

| Saída | Cálculo | Interpretação permitida |
|---|---|---|
| (i) Previsão fixa | Ajustar θ cosmológicos/nuisance com β=β*, resíduos e adequação por simulação | Compatibilidade/incompatibilidade do modelo fixo com os dados |
| (ii) β livre | Ajustar a mesma família, perfil e posterior com priors declarados | Valor favorecido e degenerescências, não confirmação do valor previsto |
| (iii) Tensão fixa/livre | qβ = 2[maxβ,θ log L − maxθ log L(β*,θ)]; calibrar sob TGL fixa | Quanto os dados exigem sair da previsão; discrepância grande conta contra ela |
| (iv) Rivais e poder | Para cada Rj, Tj=2[maxθ log L(TGL fixa)−maxη log L(Rj)]; calibrar sob Rj e medir potência sob TGL | Evidência observada contra cada rival e probabilidade prospectiva de rejeitá-lo |

As estatísticas de likelihood incluem dados auxiliares legítimos, se houver. Priors bayesianos e penalizações não serão ocultados dentro de um “chi2” frequentista. Posterior, evidência bayesiana, adequação e p-valor têm papéis distintos. Reportar os dois sentidos da comparação quando pertinente. Uma alternativa TGL incompatível não se torna explicação satisfatória apenas porque um rival se ajusta ainda pior.

## 5. Calibração global e caudas

- Simular sob cada rival, com o modelo de observação/ruído/covariance e nuisance pertinentes. Refazer em cada simulação todos os ajustes, cortes adaptativos e seleções que existirem na estatística real. Para hipóteses compostas, conferir cobertura no espaço de nuisance; simular só no melhor ajuste fornece uma calibração condicional, não garantia uniforme.
- Tj pode ser negativo, e rivais podem não ser aninhados. Não impor distribuição qui-quadrado nem usar sqrt(Delta chi2) como Z sem demonstrar/validar as hipóteses.
- Definir “global”: conjunto de dados e família de escolhas examinadas. A seleção da rota acústica sucede análises já vistas. Registrar isso. Simulações que não incluem o processo de seleção conhecido produzem apenas significância condicional ao protocolo congelado agora. Validação independente/retida pode resolver a dependência que não se consiga reconstruir.
- Não somar Z de D9/D10. Para rejeitar **todos** os rivais de um conjunto finito fixado, uma construção conservadora é p_global=max_j p_j, desde que cada p_j tenha cobertura válida para o rival composto e para a busca efetuada. Isso é diferente de escolher a menor significância-p entre várias rotas. Se a reivindicação for “alguma rota rejeita”, calibrar a seleção conjunta pertinente.
- Convenção proposta: Z unilateral, p=erfc(5/sqrt(2))/2 ≈ 2,8665157e−7. Relatar intervalo de incerteza Monte Carlo no p, não p=0.
- Exemplo aritmético: zero excedências em N simulações independentes dá limite superior unilateral de 95% p_u=1−0,05^(1/N). Exigir p_u abaixo do limiar de 5σ precisa N≥10.450.778. Isso ainda não estima bem a cauda nem cobre a incerteza de modelagem. Preferir métodos de eventos raros/importance sampling ou aproximações assintóticas **validadas**, cruzando regiões acessíveis com Monte Carlo comum.
- Quantis extremos de uma cadeia posterior MCMC não são simulações sob o rival e não calibram esse p_global. Os quantis rotulados “5sigma” no resultado antigo não serão reaproveitados como significância de descoberta.
- Poder: calcular P_TGL(rejeitar Rj no limiar registrado) sobre pontos/grades de θ ou uma distribuição declarada; reportar curvas, bandas e poder conjunto. Não converter posterior-predictive p-value ou Bayes factor automaticamente em Z.

## 6. Sequência e divisão preparada

1. Bancada: âncoras D9/D10 atuais, manifesto de sobreposição, runtime/likelihoods instalados, reprodução numérica de referência.
2. Kimi: revisão da identificabilidade, estatística global e cobertura entre modelos não aninhados.
3. MiMo: revisão do mapa de medições/priors repetidos e critérios de precisão/reprodução.
4. DeepSeek, se necessário: crítica independente a uma unidade concreta após as duas revisões; evitar duplicação genérica.
5. Coordenação: incorporar pareceres verificados, passar à assistência Física e à redação final do Opus quando disponível/autorizada, conservando o bloqueio do pacote antigo e a fila única.
6. Somente então: congelamento auditado, estudo de sensibilidade e execução de ajustes/calibração. Sem ampliar cadeias antigas apenas para acumular amostras quando a degenerescência continuar identificada.

Os itens 2–5 são preparação de divisão, não recibos de execução. A coordenação irmã recebeu a direção e pedido de preparar payloads; nenhum resultado externo novo é pressuposto.

## Fontes primárias consultadas para o desenho

- [CAMB: verificações de precisão](https://camb.readthedocs.io/en/latest/check_accuracy.html): comparação com referência de maior precisão e limites do teste numérico.
- [Cobaya: likelihoods Planck](https://cobaya.readthedocs.io/en/latest/likelihood_planck.html): versões completas/lite, nuisance e restrições de combinações.
- [DESI: produtos de inferência BAO DR1](https://data.desi.lbl.gov/doc/releases/dr1/vac/bao-cosmo-params/): likelihoods e modelos de referência.
- [DESI: clustering, matrizes e mocks](https://data.desi.lbl.gov/doc/releases/dr1/vac/full-shape-bao-clustering/): produtos de medição/covariance.
- [Algeri, Conrad e van Dyk: comparação não aninhada](https://arxiv.org/abs/1509.01010): limites da calibração usual do teste de razão de likelihood e validação por simulação.

Este é um desenho estatístico local a revisar, não uma alegação de execução daqueles métodos ou disponibilidade local de todos esses produtos.


<!-- ORDEM018_D10_CMB_BAO_OPERATOR_CLARIFIED_20260927_ANCHORS -->
## Âncoras cosmológicas conferidas após a preparação — 27/09/2026

[REAL — leitura, sem execução] Na cópia histórica C:/IALD/Artigo/teste_acustico_beta_tgl_v1/_originais/tgl_paper_unified.py, D9_DESI_BAO começa na linha4231: seu texto descreve13 medidas DESI DR2 em9 redshifts e seu laço usa erros individuais, com H0/Om0/rd de referência. D10_acoustic_scale_closure começa na linha4337; sound_horizon na4317. D10 calcula escalas acústicas a fundo fixo, e as linhas4375–4381 declaram que o desvio absoluto em sigma tem limitação de precisão e não é tensão medida. Portanto, reutilizar a integral correta é distinto de reaproveitar aquele sigma como resultado global.

[OPEN — reconciliação] O frozen do Nível2 tem12 BAO. A seleção13/12 e as releases devem ser conferidas pelos arquivos de medições, não resolvidas somando os dois conjuntos. A inspeção local não estabeleceu equivalência entre os fechamentos S/L antigos e a implementação canônica atual. Isso é pendência localizada de recuperação/verificação, não afirmação de que tal derivação inexista no acervo. Revisão local delegada a Fermat, seguida de leitura direta das âncoras D9/D10 pela coordenação.



<!-- ORDEM018_D10_COMPLETED_REVIEWS_BAO_LINEAGE_20260927 -->
## Revisão complementar — 27/09/2026

Consulte D10_PARECERES_CONFERIDOS_E_LINHAGEM_BAO.md e state/D10_BAO_LINEAGE_AUDIT.json. A reconciliação13/12 foi realizada: N2 usa prefixo dofallback; DR2 localé vetor distinto com covariance13x13 disponível. Corrigidas inferências dospareceres; plano ainda nãoé congelamento final nem execução cosmológica.
