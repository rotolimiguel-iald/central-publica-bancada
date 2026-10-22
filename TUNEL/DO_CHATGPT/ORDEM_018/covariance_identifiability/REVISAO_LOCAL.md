# R-A: covariância e identificabilidade das cinco hipóteses

[DERIVED — condicional; apoio ao V1, sem veredito observacional]

Contribuição delimitada à ORDEM018 do TÚNEL de 05/10/2026. Consulta prévia: rota `hubble.fase9_razao_discriminante`, seq 373. A crítica da gerência `CRITICA_FASE9.md`, §§1c, 1d e 3, já identifica a degenerescência do deslocamento universal, a divergência entre duas listas de hipóteses e a duplicação possível de erro comum. **Não refizemos a cronologia, os ajustes ou os números históricos.** Esta nota transforma esses achados num contrato matemático verificável para o V1. Decisões finais de hipóteses e abertura do composto continuam com o operador/gerência.

## A. Definir o vetor observado e a mesma likelihood

Escrever y=(b̂,h₁,…,hₙ), com um bloco de fundo b̂ e leitores locais hᵢ, e registrar a proveniência de cada bloco. A hipótese de um único valor verdadeiro de fundo b exige mapeamento dos observáveis e o uso autorizado de produtos comprimidos. Um posterior inferido sob um modelo não é automaticamente uma likelihood reutilizável sob outro; documentar a validade dessa compressão para a comparação.

No exemplo gaussiano condicional, C é a covariância conjunta positiva definida e constante nos parâmetros. Todos os modelos usam **o mesmo y e os mesmos termos de normalização**:

ℓ = −½[(y−μ)ᵀ C⁻¹(y−μ) + log det C + m log(2π)].

Correção fixa não é coeficiente ajustado à escada. Parâmetros cosmológicos/experimentais compartilhados devem ter o mesmo papel explícito em todas as hipóteses. Estimar uma alternativa β livre é um diagnóstico rival, não redefinir β_TGL nem substituir a previsão fixa pelos seus valores ajustados. A novidade de uso é auditada no acervo, não inferida desse ajuste diagnóstico; a existência anterior dos dados não invalida a retrodição sem ajuste.

## B. Cinco nomes exigem cinco modelos definidos

Tome κ=(2/3)ln E(z*) e K=exp(κβ), condicionados à convenção de fundo fixada. Seja u o vetor de uns dos leitores locais e c o vetor de resposta ao deslocamento das Cefeidas. Um leitor misto não recebe automaticamente cᵢ=0 ou 1: exige a resposta derivada do seu método e da escala em que o deslocamento foi definido.

| Hipótese | Predição local no recorte simplificado | Restrição que a distingue |
|---|---|---|
| TGL fixa | b·exp(κβ_TGL)u | β_TGL=α_CODATA2018√e em runtime; nenhuma recalibração ao composto. |
| ΛCDM de referência | b·u | K=1 neste observable. A RG continua limite clássico. |
| β livre, diagnóstico | b·exp(κβ)u | Amplitude universal variável, com domínio e prior próprios registrados. |
| Deslocamento Cefeidas | b·u+s·c, se s for aditivo em H₀ | Padrão seletivo. Se s for fracionário ou em magnitude, usar a transformação correspondente, não esta fórmula. |
| Fundo livre | **Especificação ainda indispensável** | A crítica registra duas versões: multiplicador do fundo, ou r_d livre. Têm previsões e espaços de dados distintos. |

**Resultado já localizado, explicitado sem novo fit:** para b>0 e κ≠0, o diagnóstico β livre equivale a um deslocamento universal δ=b(exp(κβ)−1), no domínio transformado. A derivada dδ/dβ=bκexp(κβ) fixa o Jacobiano do prior. Priors transportados exatamente dão a mesma evidência. Priors uniformes independentes em β e δ são priors diferentes; uma diferença de evidência entre essas parametrizações não demonstra uma assinatura observacional diferente.

Essa equivalência **não se aplica ao deslocamento só nas Cefeidas** quando c não é proporcional a u. O contraste wᵀh, com wᵀu=0 e wᵀc≠0, separa uma alteração universal de uma alteração seletiva. A precisão depende de wᵀC_local w e dos mapas instrumentais, não do número de rótulos de calibradores.

Se só há leitores Cefeidas e todos respondem igualmente, c é proporcional a u e a distinção desaparece. Com K universal, os leitores locais sozinhos também só identificam o produto bK: as colunas ∂μ/∂b=Ku e ∂μ/∂β=bκKu são proporcionais. O bloco independente de fundo pode identificar a razão; aumentar o número de leitores locais não substitui esse vínculo. São afirmações sobre esse recorte, não impossibilidade da missão.

Para o quinto modelo:

- Se «fundo livre» for apenas libertar b na mesma μ=b·u, ele coincide com a normalização livre do ΛCDM nesse recorte.
- Se permitir um valor de fundo independente do local, pode coincidir com o espaço de médias do β livre, condicionado ao domínio dos parâmetros.
- Se significar **r_d livre**, devem entrar as previsões BAO e a calibração pertinente. Um resumo de H₀ previamente obtido com r_d fixado não substitui essa likelihood. Libertar r_d, sozinho, não implementa a dinâmica completa de um modelo EDE. O V1 precisa nomear esse rival pelo que foi efetivamente implementado.

## C. Contar a incerteza comum uma vez

Uma representação útil, quando sustentada pelas fontes, é C=D+A S Aᵀ: ruído residual D e componentes compartilhadas com covariância S e respostas A. Se σᵢ publicado é erro **total**, então Dᵢᵢ=σᵢ²−(ASAᵀ)ᵢᵢ; não somar novamente a componente comum à mesma diagonal. É preciso conferir que D é admissível e que a decomposição vem de fonte ou derivação válida. Não inventar S, A ou correlações para preencher a lacuna.

O tratamento equivalente por variáveis latentes usa y|q∼N(μ+Aq,D), q∼N(0,S), com marginalização. Usar simultaneamente a covariância já marginalizada C e as mesmas variáveis latentes duplica a incerteza. Perfil com penalidade pode reproduzir o mínimo quadrático, mas não autoriza omitir determinantes na evidência.

Erro comum pode limitar a precisão da média e cancelar no contraste. Para C=s²I+c²uuᵀ: Var(média)=s²/n+c²; Var(hᵢ−hⱼ)=2s². Portanto, tratar covariância corretamente não significa reduzir toda significância por um fator arbitrário. Pode preservar informação entre métodos que a diagonal ocultava.

Para uma medida local h e um fundo b com K fixo, o resíduo h−Kb tem variância C_hh+K²C_bb−2K C_hb. Para um vetor local, a transformação exata é T=[−Ku | I] e C_res=T C Tᵀ. Se K depender de quantidades inferidas, propagar a covariância conjunta ou usar a likelihood completa; a expressão simples não inclui automaticamente essa incerteza.

SH0ES em versões sucessivas, a mesma escada junto a um H₀ comprimido derivado dela, ou Planck+BAO junto aos mesmos Planck e BAO não podem ser multiplicados como dados independentes. A crítica histórica registra riscos específicos, não fornece por si só a matriz cruzada publicada. A conferência das fontes está a cargo da frente coordenadora.

## D. Contrato antes do composto

1. Uma lista de blocos e linhagens: dado bruto/produto comprimido, instrumento, versão, participantes compartilhados, unidades e mapa TGL/rival.
2. Uma lista de cinco hipóteses com média, covariância, parâmetros e prior normalizado. Incluir o papel de c, o tipo do deslocamento, a definição do quinto modelo e a convenção que evita duas entradas de β.
3. Uma função de veredito com ordem completa de casos, incluindo a faixa 3–5 quando usada, e os mesmos bytes no executor e no leitor. Estatística de separação prevista, resíduo observado e evidência bayesiana são saídas distintas; não somá-las como três provas independentes.
4. Verificação da componente de erro comum, positividade e condicionamento; não preencher covariância ausente com zero silencioso.
5. Calibrar o teste composto sob a regra de seleção adotada, incluindo escolhas efetuadas na exploração. Retrodição sem ajuste continua admissível; a seleção entra no desenho do teste, não num veto temporal aos dados.

Alternativas antes de qualquer MEDIDA: covariância publicada → reconstrução de componentes com fontes; se ambas forem insuficientes, análise condicional de covariâncias admissíveis com escopo explícito, sem fabricar veredito. Para degenerescência universal → vínculo externo de fundo ou contraste entre respostas instrumentais derivadas. Para r_d livre → likelihood BAO existente ou registrar separadamente a hipótese de multiplicador, sem trocar o nome de uma pela outra. A gerência decide o encaminhamento, não esta nota.

## E. Escopo e controles

O script adjacente usa somente números sintéticos, β calculado em runtime e κ fictício explicitamente rotulado. Verifica reparametrização, posto local, contraste Cefeidas/não-Cefeidas, contagem única de variância, positividade/condicionamento do exemplo e transformação de resíduo. Nenhum centro H₀ foi aberto para novo veredito; resumos históricos foram lidos no mapa e na crítica. Nenhum kernel, original científico, pré-registro existente ou serviço foi alterado. A revisão remota, quando retornar, terá estatuto DECLARADO até conferência.
