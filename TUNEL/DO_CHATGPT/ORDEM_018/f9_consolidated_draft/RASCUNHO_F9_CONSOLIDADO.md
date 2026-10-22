# F9 — rascunho consolidado para revisão de F1

[INPUT — PROPOSTA RATIFICÁVEL] Este é o ponto de leitura corrente das recomendações documentais da coordenação ROOT. Reúne os contratos existentes e explicita condições de aplicação e lacunas de implementação. **Não é V1 congelado, não autoriza abrir o composto e não conclui F1.** Não contém novos centros, ajustes, S/g, significâncias, evidências ou veredito físico. Os originais continuam intactos. O JSON RESOLUTOR_F9.json contém os pins medidos e as remissões exatas que controlam esta leitura.

Os rótulos têm três funções: **proposta ratificável** é escolha concreta já recomendada por ROOT, ainda sem adoção científica; **condição de aplicação** é hipótese matemática/estatística cujo alcance deve ser respeitado; **lacuna de implementação** é trabalho ainda necessário para tornar a proposta executável. Um resultado de preparação já registrado não se torna nova medição ao ser citado aqui.

## O que passa a valer nesta leitura documental

As referências históricas do acumulador não são alternativas executáveis concorrentes. Os seguintes campos são expressamente **SUPERSEDIDOS PARA ESTE RASCUNHO**, sem apagar sua origem:

| Campo histórico | Resolução corrente |
|---|---|
| FASE9_V1_CANDIDATE.json, verdict_proposal_order: z indefinido e limiar em valor absoluto | Cinco estatísticas G1/Q1/T21/T41/T51 e calibração superior, V2 com convenção de cauda explícita |
| Mesmo campo: retorno antecipado NOT_FALSIFIED_UNDERPOWERED | Poder é saída separada, posterior à análise das rejeições válidas; nunca esconde resíduo ou transforma ausência de calibração em não rejeição |
| hypotheses.H4_Cepheid_shift.definition_proposed: deslocamento agregado | Resposta elementar c_C delta_C; prior de s transportado, sem fator uniforme no H0 total de rede mista |
| engineering_update_20261006.background_correction_pending | BG-01/BG-02 resolvidos no adendo independente; piloto teórico posterior registrado, com alcance limitado |
| engineering_update_background_and_verdict_20261006.verdict_contract_candidate | O candidato V2, sua revisão e a cota6273/revisão484 constituem os acompanhantes correntes |
| Proposta antiga genérica de nuisance próprios | Recomendação concreta: mesma medida plana comum relativa; prior próprio permanece alternativa explícita, não obrigação omitida |

O adendo current_documentary_companions_20261006 do próprio acumulador já assinala as três supersessões centrais. Seu snapshot exato acompanha esta entrega. Não se representa o arquivo acumulado como corrompido nem se substitui V2 ou a prova do autor.

## Dados, rede e modelos

[PROPOSTA RATIFICÁVEL] Usar **o mesmo vetor** nos cinco modelos: Planck comprimido com 3 coordenadas, DESI DR2 com 13 e rede local H0DN **V01 Baseline + JAGB** com 267 equações. V01 upstream é identificação de seleção, não o futuro pré-registro V1. A seleção, IDs e ordem estão pinados; não foram reabertos centros para este rascunho.

As 267 equações são 178 distâncias estelares, 13 relações de grupo, 55 calibradores SN, 14 calibradores SBF, um intercepto SN, um intercepto SBF e cinco masers. Os 63 nuisance são 59 módulos de hospedeiras, dois módulos de grupos e dois interceptos de luminosidade. As 12 linhas JAGB em 11 hospedeiras pertencem à seleção conjunta e compartilham as dependências documentadas. A matriz X, as colunas a_h/c_C e os 72 vínculos estelares vêm da especificação linear. Postos estruturais 63/64/65 já registrados para X/[X,a_h]/[X,a_h,c_C] não são posto medido da covariância conjunta nem poder observado.

[CONDIÇÃO DE APLICAÇÃO] Fundo comprimido e rede local são fatorados como **INPUT do modelo de dados**, não como independência empiricamente provada. A adequação das compressões, q0/j0 fixos, convenções de velocidade e termos cruzados fica explícita. H0 agregado de H0DN, ramos SH0ES/CCHP, mesmas SNe, N4258 e as mesmas observações Planck/BAO não são acrescentados novamente. CC, sirenes, lentes e outros mapas não fazem parte deste composto proposto.

Defina theta=(H0, omega_b h², omega_c h²), h_bg=log10(H0/(km/s/Mpc)), I(theta)=(2/3)ln E_standard(1089,95;theta). beta_TGL é ALPHA_FINE_CODATA_2018 vezes sqrt(e) em runtime. A convenção aplica beta somente ao mapa local R-A desta comparação:
y_local = X eta + a_h h_local + c_C delta_C + epsilon.

| Modelo | h_local | delta_C | BAO/CMB |
|---|---|---|---|
| H1 TGL fixa | h_bg + I beta_TGL/ln(10) | 0 | rd padrão / rstar padrão |
| H2 LCDM | h_bg | 0 | padrão / padrão |
| H3 beta livre diagnóstico | h_bg + I beta/ln(10) | 0 | padrão / padrão |
| H4 Cefeidas diferencial | h_bg | −5 log10(1+s) pela coluna c_C | padrão / padrão |
| H5 régua BAO livre | h_bg | 0 | rd livre / rstar padrão |

[CONDIÇÃO DE APLICAÇÃO] H3 contém H1 e H2. Preferência relativa pelo valor fixo não rejeita toda a classe H3. H5 é a opção fenomenológica A da nota de escalas acústicas; não é EDE nem dinâmica primordial completa. Em H4, a transformação de s define o prior, não uma resposta uniforme de toda a rede. O mapa físico universal R-A é hipótese de correspondência limitada aos indicadores admitidos, a explicitar na ratificação; não importa automaticamente todos os setores da TGL.

## Medidas, priors e normalização

[PROPOSTA RATIFICÁVEL] Os priors físicos são os já propostos, sem novos limites: uniformes independentes H0 em [50,90], omega_b h² em [0,015;0,030], omega_c h² em [0,08;0,18], densidade conjunta 50/3 nas coordenadas indicadas; beta diagnóstico em [−0,05;0,05], densidade10; s em [−0,15;0,15], densidade10/3; rd em [130,160] Mpc, densidade1/30.

A medida de H4 transporta o prior: pi(delta_C)=(ln10/1,5)10^(−delta_C/5), no intervalo imagem de s. Para H5 parametrizado por q=rd_livre/rd_CAMB(theta), os extremos são 130/rd_CAMB e 160/rd_CAMB, e a densidade condicional é rd_CAMB/30. Uniformizar delta_C ou q mudaria o prior; isso não é feito.

[PROPOSTA RATIFICÁVEL] Adotar a mesma medida kappa d eta em R^63, nas mesmas coordenadas físicas, comparando somente integrais relativas finitas e não nulas. Não é prior próprio para sorteio, nem evidência absoluta normalizada. Uma alternativa documentada é prior próprio comum com hiperparâmetros científicos fixados antes do composto; ela exigiria sua própria normalização e não é adotada silenciosamente.

[DERIVED — CONDIÇÃO DE APLICAÇÃO] Para C_s fixa, PSD, rank r_s e suporte afim comum, X inteiramente no suporte e com posto63, F=XᵀC_s⁺X invertível:
L_flat = kappa (2pi)^(-(r_s−63)/2) [pdet(C_s) det(F)]^(-1/2) exp(−bᵀP_s b/2),
P_s=C_s⁺−C_s⁺X F^(-1)XᵀC_s⁺, b=y−mu_i.
A restrição do núcleo também deve ser satisfeita. Determinantes e jacobianos só cancelam quando comuns e independentes dos parâmetros integrados. A likelihood perfilada usada nas estatísticas frequentistas e a integral plana usada em Bayes são objetos separados.

Unidades são transportadas conjuntamente: linhas em log10 multiplicadas por5 para a convenção de magnitude, com a mesma transformação em y, X, a_h, c_C e C. Pseudoinversa não autoriza ignorar restrição determinística; sem suporte comum não há comparação automática de densidades. Não adicionar à covariância um erro já integrado e depois o mesmo nuisance novamente.

## Covariâncias e sensibilidades

[PROPOSTA RATIFICÁVEL] A família finita candidata combina os 300 rótulos interiores estelares já qualificados numericamente com duas receitas SBF: upstream somente e(m110), e adição independente de e(M110) **condicional**. São 600 rótulos potenciais, não 600 matrizes conjuntas já montadas/qualificadas, nem distribuição medida da verdade. A contagem antiga de 283 projetos primitivos estelares distintos não é contagem de matrizes completas F9. Deduplicação futura exige igualdade certificada de covariância, resposta e normalização, preservando todos os rótulos.

A construção estelar C=D0+A diag(a²)Aᵀ+B Dm Rm Dm Bᵀ+H Dh Rh Dh Hᵀ preserva os erros marginais e âncoras comuns. O contrato pina grupos, sinais e malha; baseline Rm=Rh=I é cenário condicional. Não abrange correlações MAS–HMS gerais nem casos de fronteira que mudam suporte. Não acrescenta automaticamente 0,06 mag ou outro orçamento. As sensibilidades não são escolhidas, ajustadas ou promediadas pelo resultado.

[REAL — recibos existentes, não reexecutados] A covariância de fluxo SN e sua compressão por GLS foram qualificadas e revistas. Os erros SN/SBF propagados no recibo FLOW conservam as prescrições upstream, inclusive dispersão de velocidade e ordem das linhas repetidas. A segunda receita SBF não constitui decomposição física validada dos erros comuns de calibração/cor. O preflight262 excluiu apenas para preparação os cinco MM e não alterou a seleção267. Seu rank190 local não é rank da rede completa.

[CONDIÇÃO DE APLICAÇÃO / LACUNA] As cinco variâncias MM continuam simbólicas nesta preparação: a propagação relativa exige sigma_D/D e a distância central não foi aberta aqui. Duas alternativas já documentadas:
1. Fixar um modelo gaussiano **condicional aos erros publicados**, com convenções e limitações explícitas e decisão de adoção; a cota será exata apenas dentro desse experimento condicional, se suas hipóteses forem satisfeitas.
2. Especificar a distribuição primitiva e propagar a transformação/estimação com calibração própria, preservando assimetria e dependências relevantes.

O simples plug-in de uma covariância dependente dos dados, mesmo se estimada independentemente, não ganha uma cota finita exata por declaração. Não se exige provar ausência de toda sistemática imaginável; exige-se dizer qual experimento foi adotado e qual inferência ele sustenta. A alternativa física por componentes/Jacobianos assinados permanece disponível para ampliar a família estelar, sem confundi-la com a família finita atual.

## Fundo CAMB e domínio

[PROPOSTA RATIFICÁVEL] Fundo padrão plano comum, com H/E/distâncias derivados do mesmo motor. O protocolo fixa neutrinos térmicos CAMB, massa0,06eV em uma espécie, N_eff3,046, BBN consistente PRIMAT2024 e RECFAST aproximação Planck; explicita a referência BBN3,044 e demais parâmetros. São INPUTs de aproximação, não identidade provada com a antiga compressão Planck. z_lei=1089,95 permanece distinto de zstar calculado; rstar CMB não é rdrag BAO.

[REAL — recibo existente] Cinco pontos teóricos em duas precisões passaram no piloto já autorizado. Isso confirma apenas aqueles pontos/controles, não o prior contínuo inteiro nem erro da evidência. O reparo de claim antes do solver foi revisto; falhas/interrupções conservam identidade e não autorizam repetição.

[LACUNA DE IMPLEMENTAÇÃO] A tabela histórica cobre domínio mais estreito que o prior candidato. Não é permitido zerar likelihood fora da tabela nem renormalizar silenciosamente o prior. Alternativas existentes: motor direto com cobertura/erros e custo certificados para a unidade planejada; ou tabela ampliada com interpolação fora dos nós qualificada e todos os campos necessários. O piloto não escolheu nem executou uma campanha de domínio inteiro. Ausência de bibliotecas no sandbox Windows não prova ausência no runtime normal; ambientes são pinados separadamente.

## Inferência frequentista proposta e cota conservadora

[PROPOSTA RATIFICÁVEL] Adotar a decisão V2 e a cota documental6273, aceita condicionalmente pela revisão independente484. Seja g_i o mínimo global do RSS projetado em cada hipótese:
G1=g1; Q1=g1−g3; T21=g2−g1; T41=g4−g1; T51=g5−g1.
Os nulos são H1 para G/Q, e H2/H4/H5 para os respectivos T. São cinco testes da família conjunta R-A, não correção de todas as buscas históricas.

[DERIVED — CONDIÇÕES] Para ruído gaussiano com C_s conhecida/fixa, suporte e normalização comuns e verdadeiro parâmetro no domínio, R_s X=0 e R_s C_s R_sᵀ=I_nu, nu=r_s−63. O RSS no verdadeiro parâmetro tem distribuição qui-quadrado_nu e domina g_null. Logo G1, Q1 e Tj1 recebem envelopes superiores residuais, sem subtrair mais três/quatro parâmetros físicos como regra de Wilks.

A recomendação ROOT é envelope residual para G e envelope do **span global** para Q/T: todas as diferenças de médias devem caber no espaço fixo de 16 coordenadas de fundo mais a_h (limite17); H4 acrescenta c_C (limite18). São limites estruturais condicionais, não ranks medidos, informação efetiva ou potência. Tangente/Jacobiano num único ponto não substitui inclusão global. A alternativa mais conservadora é usar dimensão residual justificada para todos os testes. O limite residual148 só se aplica com os72 vínculos exatos herdados, matriz conjunta PSD e rank suportado63 de X; não se presume medido. Rank efetivo ou limite superior válido deve ser certificado por cenário.

[LACUNA DE IMPLEMENTAÇÃO] Certificar L_i <= g_i <= U_i. Otimizador local viável fornece U, não L. Os limites inferiores utilizáveis são max(0,L1), max(0,L1−U3) quando H1 está contida em H3, e Lj−U1. Uma SF numericamente superior, incluindo erros, transforma limite inferior da estatística em p superior. Limite trivial L=0 pode ser válido e frouxo; não é ausência de calibração. Dimensão zero exige a massa em zero e cauda inclusiva; não chamada genérica com df0. Certificados probabilísticos precisam de orçamento dentro do alpha total.

Para cada teste, p_robusto=max de p_superior sobre **toda** a família congelada, ou cobertura equivalente certificada com todos os rótulos. p_FWER=min(1,5 p_robusto). O máximo de cenários disponíveis de uma família incompleta não é essa quantidade. A convenção é alpha5=0,5 erfc(5/sqrt2), cauda superior; eventual Z equivalente não é resíduo gaussiano medido. Não se converte sqrt(Delta chi²), lnB ou combinação de p correlacionados em sigma.

[CONDIÇÃO V2] Uma rejeição completa/calibrada de qualquer dos dois testes H1 permanece reportável mesmo que o outro esteja indisponível. Não rejeição H1 exige ambos completos, válidos e não rejeitados. Discriminação combinada contra Hj exige essa condição H1, teste Hj completo/rejeitado e Tj1 positivo certificado em todos os cenários; cada rival é separado. Rivais ausentes ficam ausentes e não apagam uma rejeição válida. NOT_FALSIFIED_IN_THIS_CONTRACT não significa CONFIRMED nem valida o modelo. Uma cota frouxa que não rejeita não prova que o p exato exceda alpha. SYSTEMATICS_COVERAGE_LIMITED acompanha o alcance finito.

Os oito controles sintéticos da prova pertencem a outra unidade. Este rascunho não os executa nem declara seu estado mais recente sem recibo selecionado. A prova documental não é, por si, certificado da aplicação ao composto.

## Bayes, poder e proveniência

[PROPOSTA RATIFICÁVEL] Calcular futuramente integrais relativas J_i com priors físicos normalizados e a mesma medida nuisance. Relatar cinco logJ até uma constante arbitrária comum, dez razões pareadas por cenário, erros e intervalos entre cenários. Não misturar cenários sem pesos prévios nem somar/multiplicar famílias dependentes. Os antigos limiares de lnB, se mantidos como flags, são campos descritivos separados; não fazem parte da calibração5sigma.

Poder/informação é saída separada. O preflight de erros não é detecção nem poder global. Falta de poder não esconde resíduo, rejeição ou tensão; falta de calibração não produz não rejeição. Outras rotas/Planck-only permanecem análises distintas até contrato próprio e seleção/multiplicidade definidos.

[REAL documental / limite de interpretação] A cronologia está no parecer de proveniência pinado. Retrodição sem ajuste e novidade de uso não são depreciadas por derivação posterior ou uso de IA. Datas internas/mtimes não são automaticamente publicação imutável; a cadeia documental e eventuais ramos inversos preservam suas distinções. Esse exame não remove questões específicas de seleção nem acrescenta nova prova de antecedência.

E45 é **reprodução histórica**, não este teste. P4_d1b contém Planck+DR2+SH0ES escalar; P5_sombra contém Planck+DR2+Pantheon+SH0ES sem duplicar o escalar. Suas razões permanecem identificadas por família e não são multiplicadas. A abertura histórica da ORDEM018 juntou diagnósticos P5 com razões P4; a nota E45 registra a correção ao lado. Os recibos preservam malhas25/35, caixas, caudas não medidas, suporte histórico, perfil de M e diferenças Savage–Dickey. Nada disso é um novo lnB, novo ajuste ou resíduo de previsão sem escada nesta consolidação.

## Próximo objeto revisável

[LACUNAS CONCRETAS] Restam ratificação das escolhas explicitadas, montagem/pins finais do modelo conjunto267+16 com MM definido, qualificação de suporte por cenário, domínio/erro do motor e certificados de mínimos/caudas, normalização/integrador Bayes com tolerâncias e recursos, e função de saída aplicada ao contrato inteiro. Há componentes prontos e revisados; não se pede que controles consumidos sejam repetidos.

O futuro V1 deverá incorporar as decisões concretas e seus pins antes da abertura prevista na ORDEM018. Este pacote entrega um rascunho único e coerente para essa revisão. Todos os campos observados e vereditos atuais permanecem null.
