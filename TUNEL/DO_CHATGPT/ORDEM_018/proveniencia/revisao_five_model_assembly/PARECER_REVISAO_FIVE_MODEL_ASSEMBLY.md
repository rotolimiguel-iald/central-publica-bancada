# Revisão independente da montagem F9 H1–H5

[REAL — revisão estática; 06/10/2026] **Aceite limitado da montagem pura: não encontrei bloqueador novo nas fórmulas, coordenadas ou unidades.** Não é aceite da integração executável nem resultado numérico F9. A única obrigação concreta identificada abaixo já foi encaminhada pela ROOT à preparação de integração; não exige modificar ou bloquear este adaptador passivo.

## Achado acionável e encaminhamento

**F9A-I01 — grade efetiva deve conservar z=0 antes dos sete z BAO.** Em [background_controls.py](<C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_background_prediction\background_controls.py:182>), os checks E(0), DM(0), DV(0) usam diretamente o índice zero, e a linha185 exige distâncias estritamente crescentes. Substituir a grade antiga apenas pelos sete z positivos falharia nesses checks. A integração deve manter zero primeiro e os sete z únicos em ordem crescente: 0,295; 0,510; 0,706; 0,934; 1,321; 1,484; 2,33. Essa é a ordem da grade de avaliação; a ordem das13componentes BAO continua a do layout, incluindo DH/DM no último bin.

O [adaptador](<C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_five_model_assembly_preparation\five_model_assembly.py:235>) admite entradas extras em low_z, inclusive zero, portanto não precisa mudar por esse motivo. Conferi o arquivo [F9_ENGINE_ASSEMBLY_INTEGRATION_REQUEST.json](<C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\F9_ENGINE_ASSEMBLY_INTEGRATION_REQUEST.json>): o pedido f07e4aba-e976-4d78-be1c-449968d4a305 já exige explicitamente “0 plus seven BAO redshifts” preservando E(0)/DM(0). **Classificação: obrigação de integração identificada e encaminhada, sem bloqueador da montagem pura.** A presença do pedido não é execução, teste ou autorização produzida por esta revisão.

## O que foi conferido

Li integralmente os seis membros da entrega, o contrato da API e a fonte de montagem; comparei com a projeção estrutural e o contrato matemático pinados. O script próprio apenas leu bytes, analisou AST/JSON e contou metadados: **29 comparações de pins, todas coincidentes;23 arquivos distintos comparados a pins;25 arquivos distintos com hashes lidos**, incluindo o manifesto principal e o pedido posterior de integração. Não usei o gerador prepare_delivery.py para conferir sua própria entrega. Os seis SOURCE_PINS embutidos coincidem com FONTES_PINADAS e os arquivos em disco. As origens remotas/catálogos observados transcritos no layout não foram reabertos.

O manifesto principal medido tem 1471 bytes e SHA-256 `c55a567202e5c891a6f4ca5874de6d9ea95804dd6eecf10f3059f49a249184b9`. O recibo próprio lista cada caminho, tamanho e hash, preservando a distinção entre fonte medida aqui e pin de origem apenas transcrito.

| Item | Conferência independente e alcance |
|---|---|
| Dimensões/ordem |16componentes de fundo +267linhas locais =283;63 chaves nuisance distintas, todas em mag;283 row_ids distintos. A ordem local vem dos bytes do desenho; o layout define R,l_A,omega_b_h2 e as13BAO. Não recalculei rank.|
| Respostas locais |O desenho tem a_h não nulo apenas em7linhas de fluxo/MM e c_C=1 em119linhas de host;59hosts restantes e outras famílias não recebem delta_C. As16linhas de fundo recebem X/a_h/c_C nulos.|
| Escala5 |As sete linhas SN_HF/SBF_HF/megamaser recebem fator5 em X,a_h,c_C; nos dois interceptos −1/5 torna-se −1, e a_h torna-se5. A rotina devolve T por linha; não transforma observações/covariância porque não as recebe.|
| H1/H2/H3 |h=log10(H0)+I beta/ln10, I=(2/3)lnE_standard(1089,95); beta é alpha_CODATA2018 sqrt(e) em H1, zero emH2 e livre emH3. O endpoint I é a definição deste candidato restrito; não prova uma evolução geral Q nem executa uma cosmologia TGL completa.|
| H4 |delta_C=−5log1p(s)/ln10, somente na coluna c_C; s>0 produz delta_C<0. Não desloca toda a escada ou as linhas de fluxo novamente. O prior permanece uniforme em s, densidade10/3 em[−0,15;0,15].|
| H5 |rd livre só divide DM/DH/DV das BAO. R/lA/omega_b_h2 são os do fundo padrão; lA mantém rstar, sem troca por rd. Não se identifica esse candidato fenomenológico com um modelo EDE.|
| Priors |H0[50,90],wb[0,015;0,030],wc[0,08;0,18] dão densidade conjunta50/3; beta livre tem10; s tem10/3; rd[130,160] tem1/30. Esses fatores são metadados do prior nas coordenadas declaradas, não integrais realizadas.|
| Reuso do fundo |A igualdade theta nas cinco entradas vale por chamada para reusar uma avaliação. Chamadas em outros theta permitem ótimos separados; não há obrigação matemática de compartilhar os cinco melhores ajustes.|
| Estatuto |ENGINEERING_ONLY/UNBOUNDED_THEORY_ERROR, certificado falso, cotas/certificado/p/sigma/lnB/chi2 nulos. Valores de engenharia poderão ser usados como estimativas quando houver entradas válidas; cota uniforme não é requisito inventado para disponibilizá-los.|

A transformação do prior H4 é coerente: se um consumidor integrar em delta, deverá usar |ds/delta|=(ln10/5)10^(-delta/5), portanto pi_delta=(ln10/1,5)10^(-delta/5), no intervalo transformado. Da mesma forma, integrar H5 em q=rd/rdrag(theta) exige pi(q|theta)=rdrag(theta)/30 e extremos dependentes de theta. A API evita esses Jacobianos adicionais mantendo s e rd como coordenadas originais; não os omite de uma integração que teria feito.

## Interface, falhas e fronteiras de confiança

[five_model_assembly.py](<C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_five_model_assembly_preparation\five_model_assembly.py:180>) verifica bytes do desenho/layout, conjunto de seis fontes, schema da admissão, unidades, theta, z_lei distinto do zstar térmico, estado/error do pacote e presença das distâncias nos sete z exatos. O mapeamento l_A→lA, omega_b_h2→ombh2 e *_over_rdrag→*_over_rd corresponde aos campos existentes do motor. E/I são comparados com tolerância explícita apenas de coerência aritmética. Falhas de schema/pin/domínio/resultado upstream interrompem a montagem: não há ramo que gere vetor zero ou likelihood zero, descarte hipótese ou redefina prior em resposta a erro de engenharia. O chamador continua responsável por conservar a causa upstream e tratar quaisquer exceções de software como falhas visíveis.

A admissão é uma interface ainda sem instância qualificada nesta entrega. Seu SHA precisa vir de registro externo confiável. O SHA do pacote é computado a partir de seus próprios bytes, servindo à proveniência; não autentica sozinho a alegação de que CAMB executou. Configuração efetiva, runtime e recibo do motor têm que ser verificados pelo chamador: strings SHA sintaticamente válidas não demonstram seus conteúdos. A configuração nova deve registrar theta, perfil, grade e parâmetros efetivos, separada do protocolo histórico pinado de seis z/cinco theta. Isso é limite explicitado na [API](<C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_five_model_assembly_preparation\API_CONTRATO.md:53>), não falsa certificação do adaptador. Não examinei nem qualifiquei um wrapper ainda em preparação.

A AST mostra apenas imports hashlib/json/math/fractions e nenhuma chamada top-level fora de definições. Isso sustenta a inspeção da interface passiva; **não prova completude dos imports transitivos de um futuro runtime isolado**. O episódio NC02 permanece terminal e não foi reexecutado ou reinterpretado por este aceite.

## Obrigações preservadas para a integração

O consumidor terá de aplicar efetivamente y_out=T y_native e C_out=T C_native Tᵀ, na mesma ordem dos row_ids, preservando offsets fixos. Será preciso conferir suporte afim, núcleo, normalização e posto do sistema realmente utilizado; a frase no retorno não os prova. O adaptador não calcula C, whitening, marginalização, otimização, estatísticas ou evidências.

X eta fica separado e usa as mesmas63 coordenadas físicas. A medida plana comum κdeta admite somente os usos relativos condicionados do resolutor; não é prior de amostragem nem evidência absoluta. Alterar medida, domínio nuisance ou C requer manter os prefatores/Jacobianos correspondentes no cálculo consumidor; nenhuma dessas integrações foi feita aqui.

Os5MM foram preservados na média, no desenho e no fator5. O [contrato MM](<C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_mm_model_preparation\CONTRATO_MM_CANDIDATO.json>) segue não ratificado: a proposta gaussiana de trabalho com referências/erros fixos é condicional, não uma distribuição demonstrada dos estimadores originais. Centros, cinco variâncias numéricas, C conjunta e calibração seguem ausentes nesta revisão. A montagem de médias não resolve nem elimina essa condição.

[OPEN — implementação posterior] Envelope efetivo, entrada de background nos z corretos, integração y/C/nuisance e runtime real continuam a preparar/revisar no escopo de ROOT. Não encontrei razão para acrescentar campanha de controles nesta revisão estática. Este parecer não autoriza solver, controle, abertura de dados, nova unidade ou consumo de claim; não ratifica V1, não certifica mínimo global e não produz significância observada. Nenhum arquivo do autor, memória compartilhada, ledger, kernel ou gate foi alterado.

## Custódia da revisão

Fontes e metadados: [RECIBO_REVISAO_ESTATICA.json](<C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\proveniencia\revisao_five_model_assembly\RECIBO_REVISAO_ESTATICA.json>). Instrumento próprio: [audit_static_metadata.py](<C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\proveniencia\revisao_five_model_assembly\audit_static_metadata.py>). Mapa consultado antes: rota hubble.fase9_razao_discriminante, referências542/545; o registro posterior sela somente este exame documental. Todas as escritas próprias usam temporário, verificação e substituição; correções do instrumento/recibo têm backup imediato de bytes. Não foram importados candidatos, Fraction ou solvers, nem lidos centros observados. As contagens de metadados não são controles científicos.
