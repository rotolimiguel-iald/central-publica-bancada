# Parecer independente — contrato de certificação numérica F9

[REAL — leitura documental e bytes; DERIVED — auditoria algébrica condicional] O pacote b5fe6406-4430-48a0-bc59-e58f68917c12 é coerente no escopo declarado. Não identifiquei defeito material que bloqueie sua adoção como interface candidata de preparação. Isso não ratifica o experimento, certifica um resultado numérico ou autoriza a campanha. Mapa consultado: entrega520; início da revisão521. Originais intactos.

A conferência cobriu o contrato Markdown, a interface JSON, o plano de dez controles e as fontes admitidas. A prova de calibração, a especificação da medida nuisance e o rascunho consolidado são as fontes primárias locais do alvo, não resultados numéricos produzidos aqui. O recibo contém hashes lidos e comparações de trechos; nenhuma fonte científica foi importada/executada.

## 1. Mínimos e estatísticas

A orientação está correta: um ponto factível com avaliação superior validada fornece U_i≥g_i; nunca fornece L_i. A cobertura integral do domínio com limites inferiores por célula fornece L_i=max(0,min_k ℓ_k). O mínimo das cotas superiores de testemunhas fornece U_i. Ausência de testemunha mantém +∞ explícito; ausência de informação local pode manter ℓ=0 apenas quando o alvo não negativo está definido e qualificado. Fronteiras pertencem à busca de mínimos, mesmo quando têm massa nula na integral.

A poda ℓ_k≥U corrente é segura para a busca do mínimo, mantendo sua prova e cobertura. Ela não elimina a contribuição da célula para Bayes. O ledger e a cobertura completa impedem que uma união parcial seja chamada limite global.

As entradas da cota herdada são max(0,L1), max(0,L1−U3) com nesting qualificado, e Lj−U1 para os contrastes assinados. As orientações superiores U1−L3 e Uj−L1 também são corretas. Nenhum ótimo local, tolerância de minimizador ou concordância entre starts vira cota inferior. Bounds inconsistentes são erro a registrar, não valor a cortar para produzir conclusão.

## 2. Geometria e dual

A igualdade entre o perfil e ||R b||² vale no suporte afim comum, com X fixo de posto63 dentro de Range(C), e R representando TODO o quociente de dimensão r−63. Esta última condição já está na construção da prova primária, linhas28–38. RX=0 e RCRᵀ=I sozinhas, sem a dimensão/completude do quociente, permitiriam reter menos direções e não bastariam para a igualdade. O GeometryCertificate previsto deve verificar o alvo completo que o próprio contrato declara; não é uma nova condição física.

O dual proposto é válido para qualquer v com Xᵀv=0 exatamente; v não precisa pertencer ao suporte de C. Para e=b−Xη no suporte, a expansão
(e−Cv)ᵀC⁺(e−Cv)=eᵀC⁺e−2vᵀe+vᵀCv≥0
usa CC⁺e=e e CC⁺C=C. O termo nuisance desaparece por Xᵀv=0, e tomar inf em η mantém a desigualdade. Limitar inferiormente 2vᵀ(y−μ(B))−vᵀCv para toda a célula e tomar máximo de vários certificados e zero é seguro. Um residual apenas pequeno em Xᵀv não tem correção uniforme para η irrestrito; a recusa de near-null está correta.

O dual pode evitar uma pseudoinversa explícita na cota inferior, mas não dispensa qualificação do suporte, de C e do alvo, nem fornece automaticamente o prefator de logJ. Geometria estipulada e adequação física permanecem separadas. Não se pede prova de todas as sistemáticas para definir o experimento de trabalho.

## 3. Enclosures e propagação de erros

Distância à bola externa, max(0,||x−c||−ρ)², é cota inferior pela desigualdade triangular. Caixas externas e avaliação intervalar por componentes são válidas mesmo frouxas. Uma constante Lipschitz uniforme demonstrada e erro de ponto certificado podem construir a bola; diferenças finitas amostradas não demonstram essa constante.

A identidade de resolventes e os limites ||Ĉ⁻¹||≤1/λ e ||C⁻¹||≤1/(λ−e_C) sustentam e_C/[λ(λ−e_C)], no MESMO suporte invertível e com e_C<λ. Não vale transferi-la por mudança de posto. A inclusão de Loewner inverte as métricas e, aplicada a cada η, dá q0/(1+ε)≤qC≤q0/(1−ε); tomar inf preserva ambas.

A expansão Rb−R̂b̂=(R−R̂)b̂+R(b−b̂) dá δ=e_R||b̂||+(||R̂||+e_R)e_b. Portanto o intervalo de normas ao quadrado é correto com arredondamento externo e coordenadas compatíveis. A referência à norma n validada não permite usar um float sem sua inclusão; seus extremos devem ser transportados ao intervalo final.

A separação entre erro do solver para um alvo declarado, aproximação física desse alvo e adequação de amostragem está correta. O piloto de cinco pontos e duas precisões conserva o alcance local e full_prior_qualified=false. Ele não demonstra envoltória uniforme nem é repetido. Um alvo algorítmico alternativo só pode ser identificado/ratificado expressamente, nunca substituído silenciosamente pelo contínuo para zerar o erro.

## 4. Integral relativa e priors

Completar o quadrado em η para F=XᵀC⁺X produz integral gaussiana (2π)^(63/2)/sqrt(det F). Com a densidade sobre o suporte, resulta
J_i,s=κ A_s I_i,s,
A_s=(2π)^(-(r_s−63)/2)/sqrt(pdet(C_s) det F),
I_i,s=∫ exp(−q_i,s/2) π_i dξ.
Isso coincide com a fonte local da medida nuisance. κ é constante comum arbitrária, não prior normalizado em R^63. J isolado só é relativo; os priors dos parâmetros físicos continuam próprios e normalizados. A_s cancela na razão por cenário somente com mesmas unidades, C, X, suporte e independência dos parâmetros integrados. Se variar dentro da integral, a função comum não cancela automaticamente.

Os domínios/densidades da interface coincidem com o rascunho pinado: base H0/wb/wc e densidade50/3; β livre densidade10; s densidade10/3; rd livre densidade1/30. A transformação afim ao cubo conserva massa1. O jacobiano de s para δ é |ds/dδ|=(ln10/5)10^(−δ/5), dando a densidade indicada. Para rd=q rd_CAMB(θ), o jacobiano é rd_CAMB(θ), com limites dependentes de θ; a matriz de transformação completa é triangular e não acrescenta outro fator. Usar as coordenadas originais evita alterar esses priors.

A normalização de logJ requer também intervalo para log A_s, embora razões possam cancelá-lo simbolicamente. Esse cancelamento não elimina o erro de q. Faixas entre cenários são sensibilidade; não são intervalos posteriores nem justificam multiplicar razões dos mesmos dados.

## 5. Células desconhecidas e integral

Para ℓ≤q≤u e massa w, a monotonicidade da exponencial dá w exp(−u/2)≤contribuição≤w exp(−ℓ/2). Somar sobre partição de massa1 com arredondamento externo certifica a integral. Restos de quadratura/derivadas são requisitos para alegar maior precisão, não inferíveis da diferença entre ordens.

Uma célula completamente definida mas com previsão numericamente desconhecida admite contribuição [0,w] pelo bound universal 0≤exp(−q/2)≤1. O marcador de falha permanece. Isso não fixa a likelihood em zero nem renormaliza o prior. Se o próprio alvo é indefinido, o intervalo universal não resolve o contrato: a distinção INVALID_TARGET está adequada.

Os intervalos de razão e log-razão usam os extremos no sentido correto. Limite inferior nulo fornece intervalo estendido/insuficiente, sem log(0) como medição ou underflow como massa comprovadamente nula. O fator exp(±ε_q/2) é válido apenas para erro uniforme no domínio, somado ao erro próprio da quadratura. Nenhuma razão é convertida em sigma.

## 6. Completude, interface e controles futuros

Os certificados carregam cenário, hash da lista inteira, domínio/prior, alvo, engine/configuração, C, X/respostas, suporte, cobertura, backend e dependências. A exigência textual de verificar a lista completa, e não só os itens presentes, é consistente com o recibo de família já adotado na interface de cauda. Um placeholder p=1 não supre geometria/calibração ausentes nem produz completude por si. Um L=0 verdadeiramente certificado, com todas as hipóteses válidas, é diferente: pode ser uma cota válida frouxa.

A interface conserva outputs observados null, execução/adoção false e precisão/tolerâncias científicas ainda indefinidas. Os dez NC01–NC10 são casos propostos, não controles passados. Os tetos propostos não são custo medido ou licença para campanha. Não é necessário duplicar C01–C08, CAMB, INIT003 ou controles de cauda/guard já consumidos.

## 7. Obstáculos reais e alternativas

- Erro uniforme do motor ainda não certificado: A, construir enclosures uniformes de um alvo declarado; B, manter engenharia adaptativa com erros abertos e cotas universais válidas quando aplicáveis. B pode propor pontos a A; não promove estimativas.
- Álgebra no suporte ainda exige verificador: fatoração/pseudoinversa validada no quociente completo, ou dual com anulamento exato para a cota inferior. A segunda reduz uma dependência computacional, não resolve sozinha a normalização da evidência.
- Cobertura/informação incompleta: incluir regiões desconhecidas com ℓ=0 e [0,w] se o alvo está definido; ou declarar cobertura/alvo inválido quando as hipóteses do bound universal faltam. Não excluir massa para estreitar o intervalo.
- Backend intervalar ainda não qualificado: selecionar/pinar um backend adequado em unidade futura, ou conservar BLOCKED_DEPENDENCY/ENGINEERING_ONLY. Esta revisão não instala nada nem estabelece tolerância retrospectiva.

Conclusão de escopo: contrato documental apto à preparação posterior delimitada, sem achado bloqueante. Certificados realmente produzidos, backend, oráculo contínuo, runtime e adoção do experimento permanecem [OPEN]. Nenhum centro, C real, solver, integral, mínimo, SF, controle sintético ou modelo remoto foi consumido nesta revisão.
