# Revisão independente do projeto linear H0DN V01

Identidade: chatgpt-codex/ordem-018/derivacoes. Unidade de origem ec4872ec-82f0-4236-a76c-1e10f89aefe5; mapa 444, rota hubble.fase9_razao_discriminante. Parecer documental sobre coeficientes/IDs e álgebra da medida. Não é abertura do V1 físico nem resultado de ajuste.

[REAL — aritmética racional independente] As 705 verificações passaram. O protocolo foi gravado antes da execução. O verificador próprio usa somente a biblioteca padrão, frações exatas, eliminação esparsa e conectividade do grafo; não executa o produtor da especificação nem o upstream. Tempo interno: 0,0170741 s de parede e 0,015625 s de CPU. O recibo lista cada check e todos os hashes lidos.

## Resultado estrutural

| Objeto | Resultado exato |
|---|---:|
| Linhas totais; nuisance | 267; 63 |
| Distâncias / grupos / SN / SBF / interceptos / masers | 178 / 13 / 55 / 14 / 2 / 5 |
| Posto X | 63 |
| Posto [X,a_h] | 64 |
| Posto [X,a_h,c_C] | 65 |
| Entradas não nulas de a_h / c_C | 7 / 119 |
| Nós HMS / MAS; componentes | 104 / 11; 9 |
| Posto da incidência estelar | 106 |
| Número e posto dos ciclos L | 72 |

A eliminação racional confirma os postos sem usar os certificados de posto do produtor como prova. As receitas esparsas por família conferem, incluindo −1/5 nos dois interceptos. Foram conferidas a identidade das 63 coordenadas nuisance no JSON da medida e as seis hospedeiras adicionais aos 53 hosts medidos diretamente: IC2006, N1344, N1374, N1375, N4458 e N4489.

O componente com ciclos possui 37 HMS, três MAS e 111 arestas: posto 39 e 72 ciclos. Os oito restantes são estrelas sem ciclos. O posto da matriz de ciclos é 72 e cada ciclo anula separadamente as incidências HMS/MAS/âncora e X, a_h, c_C. Logo os ciclos fornecidos constituem o núcleo à esquerda completo da incidência estelar: 106+72=178. Isso confirma que quatro termos de uma cópia por âncora se cancelam; não torna duas cópias individualmente idênticas.

O pertencimento das colunas estelares ao suporte de incidência foi verificado de duas maneiras: (i) cada HMS admite o mesmo vetor de coeficientes em suas cópias; (ii) acrescentar X e c_C à incidência não aumenta seu posto. a_h é zero nesse bloco. Com covariância positiva nas primitivas qualificadas, essa incidência define o suporte baseline. Não foi construído C ou recalculada a família PSD.

[OPEN explícito na entrega] Ly=0 não foi verificado em centros; tampouco foi qualificado aqui o suporte conjunto da covariância a adotar. Isso é condição de aplicação já declarada, não defeito dos coeficientes nem motivo para reconstruir a seleção.

## Normalização e marginalização

[DERIVED — conferência analítica] Denote p=63, b=y−a_h h−c_C δ_C, W=C⁺, F=XᵀWX e η̂=F⁻¹XᵀWb. Se X está no suporte de C, tem posto p e o resíduo é compatível com o núcleo, então F é positiva definida e

(b−Xη)ᵀW(b−Xη) = bᵀPb + (η−η̂)ᵀF(η−η̂),

com P=W−WX F⁻¹XᵀW. A integral gaussiana em p coordenadas produz (2π)^(p/2)/sqrt(det F). Multiplicando pela densidade original normalizada no suporte, obtém-se exatamente

L_plana = (2π)^(-(r−p)/2) / sqrt[pdet(C) det(F)] × exp(−bᵀPb/2).

O fator e o expoente declarados estão corretos. L não é uma base ortonormal do núcleo, e sua anulação não substitui a medida euclidiana escolhida para os dados ou o jacobiano de eventual redução.

Para prior uniforme no domínio finito Ω, integrar o mesmo quadrado somente sobre Ω fornece L_plana vezes Pr[N(η̂,F⁻¹)∈Ω]/Vol(Ω). A entrega conserva corretamente esse fator de truncamento, que geralmente depende do modelo.

Para η gaussiano próprio, independente do ruído, a soma de variáveis gaussianas dá média Xm_η+a_h h+c_C δ_C e covariância C+XV_ηXᵀ. A expressão é uma probabilidade gaussiana normalizada, interpretada sobre seu suporte real. Se X está no suporte de C, este não aumenta; em situação geral pode aumentar. Não confundir essa integração sobre distâncias/magnitudes físicas com somar novamente erros de âncora/MAS/HMS que já estejam em C.

A constante arbitrária comum κ da medida plana multiplica todas as integrais por uma única constante. Ela cancela em razões finitas e não nulas com as mesmas coordenadas físicas, domínio e suporte de dados. Isso não dá evidência absoluta. Os fatores calculáveis pdet(C), det(F), potências de 2π e jacobianos dependentes de parâmetros permanecem dentro das integrais externas; o texto distingue corretamente esses fatores de κ.

As transformações de prior também conferem: dD/dμ=(ln10/5)D; se δ_C=−5log10(1+s), então |ds/dδ_C|=(ln10/5)10^(−δ_C/5). As unidades, limites transportados e normalizações continuam necessários. h ligado a θ não é um nuisance local independente a integrar novamente; uma Dirac em h−h_model(θ), na coordenada dh declarada, representa corretamente o vínculo.

Essas conferências são álgebra simbólica; não avaliaram F, P, probabilidades, S/g, H0, ajustes, evidências ou ln B observados.

## Alcance e escolha pendente

[DERIVED] Não há ausência de medida matematicamente adequada. A entrega oferece duas classes de medidas admissíveis: priors próprios normalizados e uma medida plana comum para razões relativas, com suas condições. MEDIDA_NUISANCE_CANDIDATA.json marca expressamente adopted_choice=null e os hiperparâmetros não escolhidos. Os nulls não são valores inválidos disfarçados: documentam uma decisão ainda não adotada.

A coordenação pode escolher uma dessas medidas comuns ao completar o contrato; se escolher a opção própria, deve especificar seus parâmetros/domínio. Não é necessário impor prior próprio aos 63 nuisance comuns para negar, por princípio, a alternativa relativa já derivada. Priors próprios dos parâmetros exclusivos de modelos e as condições de suporte/finidade permanecem exigências reais já registradas. A escolha ou suas larguras não devem ser calibradas pelos centros locais para favorecer um rival.

Há uma qualificação útil da frase do §4 sobre “demais blocos não degenerados”: ela é suficiente na montagem separada por blocos com suporte conjunto correspondente. Se forem introduzidas covariâncias cruzadas, a não degenerescência dos blocos marginais, sozinha, não garante isso. Algebricamente, uma covariância [[1,1],[1,1]] tem dois blocos marginais positivos e um núcleo conjunto. Trata-se apenas de uma ressalva de alcance; o próprio JSON e os §§4/7 já exigem o guard da covariância efetiva inteira. Não foi encontrado defeito bloqueante no projeto entregue nem é necessário repetir PSD ou criar outro guard.

A redução cinemática comum de interceptos e masers e as constantes de compressão já são explicitadas. Mantê-las no contrato fixo, ou requalificá-las se a transformação passar a depender de θ, é condição suficiente de implementação; não constitui ausência de um dado independente artificialmente exigido. O vínculo físico R-A, H5 e as dependências entre blocos continuam decisões do contrato, sem serem promovidos a teoremas pela incidência.

## Entrega e limites

Aceite documental da estrutura e das fórmulas, com a qualificação de suporte conjunto acima. Nenhum reparo foi aplicado aos arquivos da gerente. A conferência integral da custódia/incorporação segue com ROOT; esta revisão fixa os seis arquivos que leu e confere seus pins de produto no manifesto.

Foram lidos somente a especificação sem valores, a nota, a medida candidata, validação/manifesto e o produtor como texto. Não foram abertos catálogos de centros, executado upstream, montado C completo, repetidos PSD/E45/P3, calculados ajustes/S/g/H0/ln B, nem emitido veredito científico. Próximo passo autorizado por este parecer: incorporar a revisão e completar a decisão documental de medida; execução de composto depende do contrato e da autorização pertinentes.

Reprodução estrita desta revisão: verify_documentary_linear.py e PROTOCOLO_REVISAO_LINEAR.json. Resultado: REVISAO_LINEAR_RECIBO.json. Os arquivos recusam sobrescrita; esta unidade não exige rerodada para uso do recibo.
