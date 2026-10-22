# R70 — coeficiente do reservatório e o dado independente mínimo

Autor: `/root/r69_calibration_bridge`. [DERIVED — candidato matemático, sem medição].

## Fontes focalmente reutilizadas

`reservoir_bridge_r66/construction/CONSTRUCTION_R66.md:20–42` define cinco canais e o acoplamento; :63–99 extrai a bomba do canal OH; :118–122 fixa seu fluxo coerente. `BOSONIC_CONTINUUM_R66.txt:6–12` mantém a normalização bosônica J0 e lambda=beta gammaLambda. `JOINT_RESERVOIR_CONTINUUM_LIMIT_R66.txt:5–24` demonstra o limite reduzido, sem calibrar seus coeficientes. `RESERVOIR_ENERGY_AND_SECTORS_R66.txt:3–15` registra o recurso de chaveamento e a obstrução de energia livre. R65 §§2–5 e `IDENTIFIABILITY_COMPLETION_R65.txt:3–26` separam a normalização do salto, relógio e informação independente. Os pinos e as linhas efetivamente lidas constam de SOURCE_PINS_R70.json.

## 1. O parâmetro que uma colisão fornece

Fixe o MESMO J0=a_o†σ−+σ+a_i e uma ancila de dois níveis, com b=|0><5|. Escreva V0=J0⊗b†−J0†⊗b, anti-adjunto, e H_int(t)=iℏ g(t)V0, com g real em s⁻¹ e fase de V0 fixada. Se este pulso é isolado ou tratado no mesmo quadro de interação, sua área θ=∫g(t)dt é adimensional e Uθ=exp(θV0). A área simplifica o pulso somente quando o acoplamento mantém essa forma proporcional; Hamiltonianos que não comutam exigem ordenação temporal.

Em vácuo, os Kraus de segunda ordem são K0=I−θ²J0†J0/2+O(θ⁴) e K5=θJ0+O(θ³), portanto Φθ=I+θ²D[J0]+O(θ⁴) no corte finito. Para uma sequência fresca a ν colisões/s, se θ→0, ν→∞ e νθ²→lambda, a contribuição do gerador é lambda D[J0]. Erro por unidade de tempo é O(νθ⁴) no domínio limitado fixado; os termos de evolução livre são tratados pela composição R66. Não se reutiliza esta cota uniformemente no operador bosônico ilimitado: usa-se o limite iterado por cortes já demonstrado em R66.

**Assim lambda = lim ν θ².** Na construção R66, δ é o passo matemático, ν=1/δ e θ=√(δ lambda). Substituir dá lambda=lambda: não cria uma medição nem descobre Gamma. A taxa de bins tende a infinito; não é automaticamente fluxo físico de partículas. Só um dispositivo com colisões e relógio identificados permite interpretar ν como taxa experimental.

## 2. O estado do reservatório carrega condições verificáveis

Para η=p0|0><0|+p5|5><5|, p0+p5=1, a mesma expansão dá

    G_collision = νθ² [p0 D[J0] + p5 D[J0†]] + O(νθ⁴).

Prova: partir de |0> produz o salto J0; partir de |5> produz −J0† (o sinal desaparece no dissipador); linearidade no estado da ancila soma os dois canais. Um p5 não nulo acrescenta D[J0†], ausente do canal5 alvo de R66. Conhecer p0 não basta para substituir esse reservatório por vácuo. Coerência O(1) entre |0> e |5> gera um termo de primeira ordem νθ; o limite requer centrar essa média, incluir um Hamiltoniano compensador, ou escalar a coerência como O(√δ). Não se oculta esse termo como taxa dissipativa.

R66 faz precisamente uma coerência O(√δ) no canal3, com alpha=i Omega/√gamma_OH. Seu fluxo coerente é F_OH=|alpha|²=Omega²/gamma_OH, em s⁻¹. Se Omega e F_OH fossem medidos independentemente, F_OH>0 daria gamma_OH=Omega²/F_OH na convenção fixada. Isso calibra o canal3. Não há no pacote focal um teorema gamma_OH=Gamma do canal5; usar essa igualdade por semelhança de mecanismo seria novo postulado. O fluxo no canal5 de saída em vácuo é lambda Tr(ρJ0†J0); ele fornece lambda condicionado a ρ, não Gamma separado de beta.

## 3. Onde Gamma poderia entrar sem circularidade

Um modelo microscópico adicional poderia demonstrar θ_eff²=beta θ_ref², com θ_ref acessível por um protocolo independente e com mesma normalização, fase, modo e quadro. Então

    Gamma = lim ν θ_ref²,       lambda = beta Gamma.

A referência θ_ref deve ser definida SEM usar a própria betaTGL e sem dividir θ_eff pela raiz de uma beta pressuposta. Espectroscopia do mesmo acoplamento efetivo geralmente mede θ_eff; renomeá-lo θ_ref não resolve a degenerescência. Medir ν, p0, tempo, ganhos e LO elimina ambiguidades do instrumento, mas não fornece θ_ref automaticamente.

Esta igualdade microscópica NÃO foi localizada nas fontes focais R65/R66, que introduzem L5=√(beta gammaLambda)J0 como coeficiente de entrada. Isso é uma lacuna deste pacote consultado; não se afirma ausência em todo o acervo. Sem aquela ponte, a interface devolve OPEN_INDEPENDENT_REFERENCE, sem preencher Gamma ou beta. Mesmo com valores e uma hipótese textual sintéticos, ela retorna apenas CONDITIONAL_SYNTHETIC_REFERENCE, nunca medição verificada.

## 4. Por que on/off e mais correlações não bastam, neste modelo

Proposição condicional de não identificabilidade: para cada controle c (inclusive drive on/off e intensidade), suponha que o gerador, preparo, instrumento e estatística de saída dependam de beta,Gamma exclusivamente por lambda=beta Gamma, enquanto os demais parâmetros e escolhas de controle não dependem deles. Então (beta,Gamma) e (s beta,Gamma/s), s>0 admissível, têm exatamente as mesmas leis de todos esses experimentos.

Prova: geradores e instrumentos coincidem para cada c, logo os propagadores, as inserções de saída e suas probabilidades coincidem. Com sequência de controles, compõem-se os mesmos mapas. Em feedback, condicionado ao histórico y_<k, a mesma política escolhe o mesmo controle, e a mesma distribuição condicional produz y_k; indução dá a mesma lei conjunta. Monitorar também o canal5 não altera isso quando seu operador é √lambda J0 e sua realização depende apenas de lambda. No nível de trajetórias e contagens, é a mesma amplitude de salto.

Derivadas, quando existentes: ∂_beta log p=Gamma ∂_lambda log p e ∂_Gamma log p=beta ∂_lambda log p. Os vetores de score são proporcionais. A direção (beta,−Gamma) é nula na informação. Somar campanhas on/off preserva posto≤1; aumentar a sensibilidade a lambda não acrescenta a direção faltante. Uma alteração conhecida D→a(c)D também preserva o produto. A prova não exclui um controle novo cuja física dependa separadamente de Gamma; exige que essa dependência seja derivada e calibrada, não inferida do nome do controle.

## 5. Dado mínimo independente e critério de conclusão

O dado mínimo é uma lei de referência p_ref(z|Gamma) com informação positiva sobre Gamma, independente da previsão betaTGL e do produto lambda; deve vir acompanhada da ponte ao MESMO J0 e da avaliação de parâmetros nuisance/covariâncias. A implementação microscópica acima fornece um candidato concreto: ν e θ_ref independentes mais a relação comprovada θ_eff²=beta θ_ref². Alternativamente, uma ponte comprovada Gamma=c_ref kappa permite medir c_ref e kappa independentemente. R65 já mostra det I=Gamma² I_lambda I_Gamma quando as calibrações são independentes e os demais parâmetros condicionados. Nenhuma dessas informações é medida nesta entrega.

Interface `reservoir_calibration_r70.py`: coeficientes racionais exatos de colisão e população; registro explícito do salto reverso; referência ausente recusa promoção; classe de controles dependente só de lambda mantém OPEN_BETA_GAMMA_DEGENERACY. As unidades e normalização devem corresponder. O script de controles foi preparado como PROPOSTA NÃO EXECUTADA; por orientação da raiz, não foi criada nova bateria para repetir a identificabilidade R65. Não há pré-registro congelado nem recibo de teste R70 deste agente. Os racionais do script proposto não são betaTGL.

R4 avança de uma escala abstrata para o fator físico que falta ligar: o acoplamento de referência do canal5. Não se declara calibração concluída, 5sigma, identificação de V0/Eref/kappa modular ou passagem para saída bosônica ilimitada. R69 continua fornecendo o decoder e as recusas instrumentais; quatro correlações não viram tomografia completa.
