# Revisão independente — preparação simbólica MM da F9

[REAL — documental] Request98a42877-3879-43a7-841c-8bb662be3d06, entrega511; consulta prévia do mapa e início512. Conferi os seis arquivos do manifesto,12 fontes por bytes/SHA e cinco trechos de código contra suas linhas/fontes pinadas. Foram somente hashes opacos dos artefatos de metadados; não naveguei seus campos centrais nem abri megamaser.dat. O script do autor e o upstream não foram executados/importados. Não calculei D/v/y, variâncias observadas, matrizes, caudas, ajuste ou controle.

**Conclusão: aceite documental limitado, sem achado material no recorte.** A alternativa A é concretamente implementável como experimento estipulado depois de decisão da coordenação e preenchimento autorizado das referências. Ela não recebe ratificação científica ou certificação de adequação física por este parecer. A alternativa B está corretamente descrita como outra lei de medição, ainda incompleta nas fontes admitidas. As condições já explícitas não devem ser convertidas em novos requisitos artificiais para a preparação.

## Receita upstream e derivadas

[REAL] data_loader.py:549–589 usa s_D=(|d_minus|+|d_plus|)/2, mu=5log10(D)+25, z=v_corr/c e cz_term=log10[v_corr*F(z)], com F=1−(q0+3)z/2+(11+7q0+3q0²−j0)z²/6. logh_value=cz_term−0,2mu+5 reduz exatamente à transformação simbólica log10[(U/v_unit)/(D/D_unit)], U=vF(v/c). O termo de erro usa sqrt(s_v²+s_pec²)/(v_corr ln10). A variância do contrato, [(s_D/D)²+(s_v²+s_pec²)/v²]/ln²10, é a receita desse código. Os trechos equations.py:324 e630–643 confirmam início da matriz em zero e atribuição diagonal das variâncias MM no bloco mostrado; não constituem medição de independência física.

[DERIVED] A derivada completa da MESMA transformação é a_D=−1/(ln10 D), b_v=[1/v+F'/(cF)]/ln10. U'=F+zF' e U''=(2F'+zF'')/c estão corretos. A ausência de F'/F no erro upstream foi identificada honestamente e não corrigida às escondidas na alternativa A. Não se pode concluir o tamanho empírico dessa diferença sem a etapa autorizada de dados; este parecer não a avalia.

A expressão cruzada a_i a_j SigmaDD+a_i b_j SigmaDV+b_i a_j SigmaVD+b_i b_j SigmaVV conserva sinais e dependências. O mesmo orçamento peculiar por linha não decide se o erro é comum ou independente. A proibição de contar o mesmo componente duas vezes é apropriada. O polinômio F coincide até segunda ordem com K_L/(1+z)² por expansão algébrica; a ressalva de que isso não identifica sozinho o tipo físico de distância é necessária e já está presente.

A passagem fixa para magnitude deve levar y/X/a_h/c_C por T e C por TCTᵀ. Isso dá fator25 na variância MM e fator5 na covariância cruzada com linha não escalada. Na lei singular, o Jacobiano é o restrito ao suporte, como a proposta declara; o determinante ambiente não pode ser aplicado cegamente. Nenhuma normalização de nuisance/Bayes foi alterada aqui.

## Experimento A versus condicionamento real

[DERIVED/INPUT] R* fixa a receita de variâncias e a lei estipulada de Y*, comum entre hipóteses e avaliações. Se o verdadeiro parâmetro e o experimento gaussiano estipulado satisfizerem as premissas, a projeção produz o pivô e os envelopes já derivados. Isto é uma conclusão condicional matemática válida; não precisa de uma prova impossível de todas as sistemáticas para ser apresentada com esse alcance.

Por outro lado, congelar escalas extraídas dos próprios D/v não prova que a lei condicional do estimador físico seja gaussiana de covariância conhecida. Condicionar literalmente nos mesmos D/v fixa y=f(D,v). O texto torna explícita essa distinção e não usa uma flag de C conhecida como demonstração. Mesmo uma covariância estimada independentemente não vira conhecida/exata por independência apenas.

As três superfícies permanecem distintas: ratificação do experimento, certificado da matriz comum e adequação da lei física. No JSON, ratification_status, common_C_artifact_certificate e physical_sampling_law_adequacy estão separadas e null; ratified=false, valores protegidos/null e outputs_now/null foram conferidos. PSD/hash/posto dizem respeito ao artefato, não certificam uma distribuição de medição.

O bloco MM diagonal positivo e a covariância cruzada nula são uma proposta INPUT fiel à montagem escolhida, não alegação de independência observada. A referência não pode variar como D_ref=U(v)/H0(theta) nem trocar q0/j0 por modelo durante o ajuste, porque isso tornaria a redução e os pesos dependentes da hipótese. MM-P10 aborda exatamente essa diferença.

## Transporte primitivo B, assimetria e Jacobiano

[DERIVED] Para v fixo, aumentar D leva à cauda inferior de y: as larguras log10(1+d_plus/D) e −log10(1−d_minus/D) estão orientadas corretamente, com D>d_minus no segundo extremo. Transportar limites de um intervalo não identifica automaticamente probabilidades de1sigma. Posterior publicado não pode ser tratado como likelihood sem considerar prior/seleção; essa lacuna de fonte foi declarada, não preenchida por suposição.

O mapa5×10 de(D,V) para Y não permite um determinante quadrado que elimine as variáveis restantes. A transformação(D,V)→(Y,V), em D>0 e U(v)>0, tem inversa D=U(v)/(H_unit10^y), Jacobiano absoluto produto_i(ln10 D_i) e marginalização em V conforme o domínio transportado. As fórmulas entregues são coerentes. Se houver primitivas de calibração, a distribuição deve incluí-las ou sua marginalização deve ser explícita; manter V observado em vez de integrá-lo define outro espaço de dados, não uma igualdade silenciosa de likelihoods.

As derivadas de segunda ordem também conferem: f_DD=1/(ln10 D²), f_vv=[U''/U−(U'/U)²]/ln10 e f_Dv=0. Assim, o viés de segunda ordem fornecido tem os coeficientes e sinais corretos. A não linearidade pode alterar centro/covariância; a aproximação diferencial não herda automaticamente o pivô gaussiano fixo ou o span simples. Positividade/truncamento requer normalização da lei, não descarte posterior de realizações.

## Aplicação da cota e plano de controles

As cinco linhas têm resposta proporcional a a_h e nenhuma nova nuisance própria. Sob bloco positivo independente, acrescentam cinco dimensões de ruído; 267locais/283conjuntas,72vínculos, posto superior211, nuisance63 e residual superior148 são relações condicionais preservadas. Os limites globais17/18 seguem a inclusão de respostas, não postos medidos ou contagem de parâmetros ajustados. O contrato não transfere automaticamente o preflight262 ou sua dimensão143 para a rede inteira.

MM-P01–P12 são um plano coerente: identidade/unidades; congruência incluindo bloco cruzado; derivada completa versus upstream; sinais e dupla contagem; assimetria/domínio; Jacobiano/normalização; condições do pivô; variância endógena/estimada; suporte/blocoMM; invariância entre modelos; positividade/viés; custódia/referências ausentes. Há negativos discriminantes, e P07 manda reutilizar os recibos C01–C08, sem rerodá-los. O plano não fixa ainda uma execução concreta, tolerâncias ou orçamento de simulação; isso é compatível com seu status PLAN_ONLY, não defeito a resolver executando algo nesta revisão. Uma futura seleção de controles pode usar álgebra exata e fixtures declaradas para evitar duplicações.

## Escolhas e lacunas já delimitadas

Não há bloqueador novo a corrigir no documento. Para os dois obstáculos reais de aplicação, as alternativas já presentes são suficientes e ficam preservadas:

- Lei de medição: A, gaussiana de trabalho com referências congeladas e alcance condicional explícito; ou B, lei primitiva positiva/conjunta com transporte e calibração próprios. Nenhuma é adotada aqui.
- Dependência: bloco MM diagonal/independente assumido como INPUT do experimento; ou covariâncias cruzadas explicitamente modeladas a partir de fonte/parametrização e verificadas na matriz conjunta. Erros marginais não escolhem entre ambas. Essa escolha não autoriza novos parâmetros/priors sem o contrato correspondente.

A extensão Sigma_true<=a C_work exige uma dominância uniforme e controle do centro/suporte, como já declarado, e nenhum a foi estimado. Não imponho essa extensão como condição obrigatória para preparar A. Uma recomendação ratificável de modelo e uma demonstração de cobertura física real são objetos distintos.

[REAL] Os18pins e cinco trechos conferem; as36 verificações documentais do autor foram lidas, não convertidas em testes científicos. Nenhuma memória compartilhada ou fonte foi alterada; nenhuma adoção de C, abertura, coleta, chamada remota ou controle foi autorizado por este parecer. ROOT pode continuar a preparação dentro do escopo proposto, mantendo as flags e decisões separadas.
