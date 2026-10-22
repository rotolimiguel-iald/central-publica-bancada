# E1.2–E1.4 — seleção e controles existentes

[REAL — custódia e contas leves; KNOWN — passagens primárias; OPEN — eficiência estatística e transferência]

Selo E0 conferido por bytes: JSON e MD coincidem com os hashes fornecidos. Esta frente fecha leitura documental e controles arquivados; não paga uma curva de calibração pSEOB nem eficiência de seleção. Nenhum nuisance ajustado, posterior novo acessado ou E2/E3 executado.

## Seleção: regra de entrada e eficiência são objetos distintos

O indicador pSEOBNR exige **SNR ≥8 em cada parte: inspiral e pós-inspiral**, além da elegibilidade de catálogo/qualidade. Em O4, onde disponível, a fonte usa a mediana da análise GR SEOBNRv5PHM; até O3b, nas reanálises descritas, usa MAP IMRPhenomXPHM MSA. Não se substituem esses dois números pela SNR total GWOSC, pela SNR do 220 numa janela de 10 tM, nem por largura posterior. Os valores separados e a implementação exata da separação em frequência não foram reconstruídos: função operativa documental especificada, execução por evento ainda não certificada.

Separadamente, o INPUT adotado E0.3 é SNR de rede GWOSC≥12, mediana Mf_det≥40 M☉ e 0≤mediana chi_f<0,98; prioridade≥30. Falta de metadados mantém AWAITING_GR_METADATA. Essas medianas são prévias à deformação, sob GR; não são medidas independentes do strain. Critério adotado não significa eficiência conhecida.

A eficiência ε(θ)=∫I_seleção(d)p(d|θ)dd e sua média populacional α(Λ)=∫ε(θ)p(θ|Λ)dθ permanecem **null/OPEN**. Para inferência condicionada a N selecionados, a normalização α(Λ)^−N exige modelo consistente; não inserimos α=1, correção numérica ou ajuste. Uma lista publicada, o corte determinístico ou um ajuste c(σ) não medem essa integral.

Leitura efetiva: passagens das seções 7.2 do [GWTC-5](https://arxiv.org/abs/2607.19293), 2.2 do [GWTC-4 III](https://arxiv.org/abs/2603.19021) e [VIII.1.2 do GWTC-3](https://arxiv.org/html/2112.06861v3#S8.SS1.SSS2), com hashes e localizadores em SOURCE_PASSAGES/JSON. Não leitura integral. As páginas HTML dos dois primeiros retornaram 404; usamos os PDFs/textos primários já arquivados. A LVK descreve possível seleção favorável a amortecimento positivo e não a inclui na inferência hierárquica citada. Isso não quantifica o efeito nem escolhe sua causa: prior assimétrico, correlações, ruído e amostra finita continuam alternativas.

## Uma injeção LVK e alcance do RD

Reutilizado o diagnóstico F2 auditado: **uma** injeção com duas recuperações com/sem 44, 20.000 linhas posteriores em cada. São o mesmo ponto físico, não 40.000 injeções nem curva em SNR. Priors 220 U(−0,8;2) têm massa positiva 5/7; 440 continua nuisance livre nas duas recuperações. lnB permanece null; conteúdos KDE em GR não são cobertura frequentista. Não se estimou eficiência, c(SNR), poder ou transferência da largura estocástica.

No RD arquivado, os desvios físicos 220 estão fixos; há desvios do 221. Sua convenção é logarítmica: δf=exp(df)−1, δτ=exp(−dg)−1. Coordenadas unitárias variáveis e massa/spin Kerr não criam deformação 220 livre. Portanto não fornecem o mesmo lnB220 de robustez nem curva pSEOB. A ausência da curva está registrada como **NÃO PAGO**, a tratar em E3; não é ausência de todo controle útil.

## C2: viés com sinal, um estimador sintético

| SNR do controle | N | média δτ̂ | EP da média | estatuto da conferência |
|---|---:|---:|---:|---|
|20|50|0.030314300|0.013149525|50 estimativas arquivadas recalculadas|
|20|2000|0.010300029|0.002255976|resumo da gerência; EP=sd/√N conferido|
|40|2000|0.002599262|0.001108156|resumo da gerência; EP=sd/√N conferido|
|200|2000|0.000130100|0.000220686|resumo da gerência; EP=sd/√N conferido|

Os 2000 ajustes individuais não estão no resumo; não foram regenerados. 4/ρ² é aproximação descritiva compatível com estes erros, não lei universal ou nuisance escolhido. Os pontos reutilizam ruído e não são independentes. O ensaio posterior de 1000 trajetórias em SNR20 tem janela/ruído diferentes; não integra esta curva. Cauchy R-LIN não possui variância de fase; a dispersão arquivada é do estimador limitado.

## C5: outro estimador e outra base de SNR

Recalculadas 24 células R-B da mesma família, a=0/1, duas PSDs e SNR40/200/600, com 206 estimativas arquivadas por célula. Não é PE completa de parâmetros astrofísicos: remanescente fixo, amplitudes de quadratura marginalizadas e perfil de a. Todas usam os mesmos pares de ruído entre células; não há N=1648 independente por SNR.

| SNR rede desde 10 tM | mediana histórica do proxy absoluto | faixa entre 8 células | faixa EP média δτ exata |
|---:|---:|---|---|
|40|0.008302087|[0.0027675675841960126, 0.020317082963432088]|[0.0031071409885306154, 0.004280700715539091]|
|200|0.001056387|[0.0004934876163706958, 0.001943907385008953]|[0.0006162913512802048, 0.0006973736873641915]|
|600|0.000351930|[0.0002443560895934051, 0.0006103780212673448]|[0.00020519806626885143, 0.0002212784457832365]|

A coluna histórica é proxy linear **absoluta**, não média com sinal. O JSON conserva-a e acrescenta, por célula, a conversão exata −a x/(1+a x), verdade injetada, viés médio/mediano, EP condicional e intervalo da mediana por estatísticas de ordem. As faixas da tabela não são IC. Os erros não incluem incerteza de PSD/modelo nem dependência entre intervalos. Nenhum EP agregado é inventado.

O resumo histórico de 0,0083@40 e 0,0011@200 é reproduzido, mas não pode ser unido a +0,030@20 de C2 para formar uma curva. A fonte C5 é representativa a 403 Mpc; SNR é da rede ilustrativa na janela desde 10 tM, diferente da SNR total GWOSC. Mesma família contém o gerador: fechamento condicionado. As limitações de forma de onda/SEOB em SNR≥200 e o crime inverso permanecem; erros pequenos não pagam a calibração física. Fisher 2/ρ é limite local de fonte fixa e não resolve degenerescência de um 220 com massa/spin livres.

O parecer principal de sistemáticas (2388 comparações) foi lido e seu vínculo por hash conferido; não é atribuído a esta frente. Aqui foram feitos somente os controles de 24 células descritos. Nenhuma leitura física foi escolhida. Gate sistemático e curva/eficiência operacional permanecem abertos.

## Custódia e reprodução leve

SELECTION_AND_CONTROLS.json contém parâmetros, erros, escopos e SHA256 completos de cada fonte. RECEIPT.json identifica código/saídas e confirma entradas inalteradas. O código recusa destinos existentes e não importa construtores científicos. O replay N50 da gerência e os ajustes N50 originais diferem em menos de 2e−8 nas estatísticas comparadas, não por igualdade de bytes; diferenças registradas. Não houve campanha ou alteração de produção.
