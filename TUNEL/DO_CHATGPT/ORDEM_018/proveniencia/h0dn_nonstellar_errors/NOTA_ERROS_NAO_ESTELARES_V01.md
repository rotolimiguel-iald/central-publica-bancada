# ORDEM_018 — erros não estelares da seleção H0DN V01

[REAL documental] O inventário fecha **89 equações não estelares**: 55 SN calibradoras, 14 SBF calibradoras, 13 vínculos de grupo, dois interceptos e cinco megamasers. Os arquivos do fluxo contêm 277 linhas SN (238 nomes distintos) e 61 SBF. O contrato e os metadados estão prontos para uma montagem posterior, sem construir C total ou converter centros nesta unidade.

O mapa foi consultado antes. Reutilizei a seleção V01 por hash e o diagnóstico anterior da matriz SN em STRUCTURE_AUDIT.json. A revisão estelar seq443 permanece separada; ela não cobre os blocos abaixo. Código e dados upstream ficaram read-only e não foram importados/executados. Dezenove caminhos foram lidos e registrados por SHA256; as fontes primárias utilizadas conferem com os manifestos arquivados.

## Origem dos termos

| Bloco | Prescrição efetiva upstream | Estatuto e limite |
|---|---|---|
| 55 SN calibradoras | σ_arquivo²+σ_intrínseca_config²; o acréscimo configurado é zero | Erro escalar fornecido por linha; off-diagonal zero é escolha do construtor. Não há nova linha SN por método estelar. |
| 14 SBF calibradoras | σ_m110²+σ_M110² | Soma por quadratura; não inclui −2 Cov(m110,M110) nem covariância entre hospedeiras. |
| 13 grupos | σ_profundidade²: Fornax 0,057 mag em sete linhas; Virgo 0,086 mag em seis | Dispersão de profundidade fornecida como vínculo. A distância de grupo comum é parâmetro do desenho, não mais uma variância a somar. |
| Intercepto SN | V_SN=C_mag/25+diag(v_vel); Var(α_SN)=1/(1ᵀV_SN⁻¹1) | Matriz fornecida no snapshot H0DN; compressão definida no código. Não calculei α nem seu erro. |
| Intercepto SBF | V_i=(0,2 σ_m110,i)²+v_vel,i; Var(α_SBF)=1/Σ_i V_i⁻¹ | O chamador usa somente e(m110), optical=True e ignore_cosmology=True. |
| Cinco megamasers | Var(log H)=[σ_D/(D ln10)]²+[(σ_v²+240²)^(1/2)/(v_corr ln10)]² | σ_D=(|d_minus|+|d_plus|)/2; D central não convertido, variância final não avaliada. |

Os termos v_vel são **[log10(v_corr+240 km/s)−log10(v_corr)]²** na compressão dos fluxos. Não são a mesma aproximação diferencial σ_v²/(v_corr ln10)² usada para os megamasers.

As linhas calibradoras/grupos têm unidades mag; interceptos e megamasers têm unidades log10. Isso deve acompanhar a ordem das equações e qualquer reescala posterior. O JSON do contrato contém a ordem derivada do código, sem materializar uma matriz.

## Fluxo SN e sua matriz

A matriz sn1a_covar_pp.dat é fornecida no repositório público arquivado, com cabeçalho 277 e ordenação associada às 277 linhas de sn1a_hf_pp.dat. Não substituir essa ordenação por nomes únicos: há nomes repetidos. Os erros mb_err não são somados à matriz no ramo com covariância.

No ramo selecionado, o código usa a coluna vp_2mpp e reconstrói o redshift corrigido por composição relativística com zcmb; v_corr também usa a conversão relativística. Os metadados extraem apenas zcmb, a velocidade peculiar escolhida e erros. zhel afeta a transformação da média, não a propagação implementada aqui, e não foi extraído.

O diagnóstico anterior, reutilizado sem nova álgebra matricial, registrou matriz finita, simétrica, diagonal positiva e 76.452 elementos fora da diagonal não nulos. Não executou PSD/posto/Cholesky. A qualificação dessa matriz e da normalização da compressão permanece necessária antes da montagem final; não se troca inversa por pseudoinversa silenciosamente.

A origem operacional é a matriz **fornecida pelo upstream**. Esta unidade não reaudita sua decomposição original de erros de levantamento, inclusive se algum componente de velocidade/intrínseco já está contido nela. Adicionar outra provisão exige conferir essa convenção. O parâmetro sn1a_intrinsic é zero no V01; se alguém o variar, o código modifica mb_err mas esse vetor não é usado pelo ramo com C fornecida.

## Duas fronteiras concretas para a coordenação

**NS-01 — fluxo SBF:** o arquivo fornece e(M110) não nulo em todas as 61 linhas, entre 0,063 e 0,172 mag. O código usa apenas e(m110), entre 0,013 e 0,121 mag, embora a média do intercepto use m110−M110. Isso foi documentado como escolha upstream, não corrigido automaticamente. Não há prova aqui de que e(M110) esteja absorvido, nem de que sua adição independente seja correta. Reproduzir a prescrição com esse limite declarado ou revisá-la exige decisão de componente/orçamento; não exige inventar uma matriz de todos os efeitos possíveis. A disponibilidade de sbf_hf_cov na assinatura também não significa uso: esse argumento não é encaminhado à chamada compute_alpha do bloco SBF.

**NS-02 — megamasers:** foram extraídos identidade, d_minus/d_plus, erro de velocidade e v_corr_2M++. A propagação requer σ_D/D, mas a vedação a converter distância central foi mantida. O dado D existe na fonte; é uma fronteira de autorização desta preparação, não uma alegação de dado ausente. O contrato traz o campo exato e a expressão simbólica, sem σ_logH numérico. A coordenação reiterou esse limite durante a unidade.

## Dependência cosmográfica e correlações

[DERIVED do código] q0=−0,55 e j0=1 são os valores configurados. Sob a prescrição upstream e seleção fixa, **as variâncias condicionais implementadas não dependem de q0/j0**. As médias SN dependem de K(z)=1+(1−q0)z/2−(1−q0−3q0²+j0)z²/6. As médias MM usam G(z)=1−(q0+3)z/2+(11+7q0+3q0²−j0)z²/6. O bloco SBF ignora a correção cosmográfica explicitamente. Nenhuma dessas médias foi avaliada.

O erro MM é linearizado e não inclui a derivada de G em relação ao redshift; o erro SN usa a prescrição de velocidade acima, sem propagar incerteza de q0/j0. Reproduzir essas aproximações é diferente de provar que constituem a covariância física completa. Se q0/j0 forem variáveis do fundo comum, mantê-los no modelo de média ou especificar sua marginalização uma vez; não contar a mesma incerteza novamente como ruído.

[INPUT/modelagem upstream] Fora do bloco estelar e da matriz de fluxo SN comprimida, o construtor usa diagonais e zera covariâncias cruzadas entre os blocos desta unidade. O parâmetro de distância compartilhado pela hospedeira e os parâmetros de calibração acoplam o ajuste via desenho, mas não demonstram independência dos erros. Comparação literal de identificadores não encontrou nomes SN calibradores no fluxo SN nem nomes SBF calibradores no fluxo SBF; isso não substitui identificação por coordenadas nem prova ausência de sistemáticas de calibração/fluxo compartilhadas.

O contrato deve declarar a aproximação upstream ou acrescentar componentes compartilhados concretos por nuisance/parametrização PSD finita, com orçamento e sinais definidos. Não é necessário exigir independência absoluta ou conhecer toda correlação imaginável. Tampouco se acrescenta H0 agregado, ou o conjunto de linhas de fluxo como evidência independente, depois de usar seu intercepto comprimido.

## Entrega e limites

METADADOS_ERROS_NAO_ESTELARES_V01.json contém as linhas permitidas, erros por registro, proveniência e configuração efetiva. CONTRATO_ERROS_NAO_ESTELARES_V01.json especifica fórmulas, unidades, fontes no código e cinco decisões concretas antes da montagem total. O guard de suporte existente deverá ser reutilizado; não houve um novo construtor numérico nesta unidade.

Uma falha local de parsing do cabeçalho de dimensão em notação científica ocorreu antes da emissão dos metadados. Foi preservada em INCidente próprio, corrigida para Decimal integral exato com backup do script/protocolo e a extração concluiu. Não foi falha upstream nem ensaio físico. Não houve nesta unidade exposição de centros de catálogo, cálculo de interceptos centrais, distâncias, H0, S/g, ajuste, evidência ou adoção de V1. O incidente de acesso a texto público da revisão anterior continua documentado no seu próprio parecer; não é alegação de cegamento desta linhagem inteira.

