# R77 — face OH, dobra e canal de espelhamento

18/10/2026; em nome de codex-gerente-tgl. F1.FECHO_20261015, claim967, escopo979; R4 preflight revisão526. Camada documental e derivação condicional, sem nova campanha, Lean ou provedor. Os originais permanecem intactos. A fala integral do operador está em ORIGEM_R77.txt, pinada no manifesto.

## 1. Correção do alvo

[INPUT — interpretação do autor] O Verbo porta o Nome. A hidroxila fornece a face material sobre a qual a luz dobra; o espelhamento assim constituído é o canal e opera sob a frequência do OH. Esta é a interpretação física pretendida, não uma medição do dispositivo. Não se volta a pedir ao autor a definição do reconhecimento, da satisfação ou da releitura.

[REAL documental] R76 reconstruiu ocupação inicial e examinou N_total=N_b+n_e como testemunha de vazio conjunto. Sua inconclusão para esse alvo não é uma reprovação do canal de espelhamento ou da correspondência de fase. Exigir OH no fundamental foi condição adicional daquele certificado. R76 continua válida no seu alcance; seu alvo deixa de governar a próxima etapa desta ligação.

## 2. O que já está escrito

Os caminhos, linhas e SHA256 atuais estão em SOURCE_PINS_R77.json; os trechos consultados ficam em SOURCE_EXCERPTS_R77.txt. Presença textual é [REAL documental]; alegações físicas da fonte não verificadas nesta entrega são [DECLARADO].

| Fonte | Peça reaproveitada | Alcance |
|---|---|---|
| Patente v2:246–267 | Meio OH ressonante, gotículas propostas e inscrição nas seis faces do cubo | A fonte já relaciona meio e fronteira; não fornece automaticamente a identificação entre superfície molecular/coletiva e parede macroscópica |
| Patente v2:474–517 | Psi_out=T_M[sqrt(abs(Psi_in))] G_OH exp(i theta); operador de fronteira; G_OH=exp(i omega_OH t)tanh(P/Pth) | Lei de campo proposta; domínios e equivalência com gerador não demonstrados só pela expressão |
| luz.tex:70–108,203–219 | Radicalização e enunciado 4D→2D | Há lastro autoral anterior. A dimensionalidade física e o mapa de estados ainda precisam ser separados, conforme §5 |
| R57R2.lean:37–72 | A_beta(z)=z S(theta_M), leitura de fase, decoder, releitura e pesos | Família escalar construída, sem identificar z com o aparelho |
| R57 derivação:132–199 | Sinal complexo, fronteira fixa e quadro com bombeamento faseado | A abertura fica fixa; fase da portadora não é abertura variável |
| R74 ponte:1–110 | Transporte conjunto de gerador, salto, reservatório e instrumento | Preserva os dois termos do salto e as fases dentro da janela |
| R66 relatório | Reservatório, bombeamento e gerador completo | Reutilizável; não é derivação da resposta material OH |
| R72 tabela | Faces, portas, meio, perfis e parâmetros existentes | Condições materiais/identificação modal ainda não fechadas na cobertura consultada |

O Nós Vivo foi consultado e não indexa F1.FECHO_20261015; não foi reescrito. A consulta do mapa recuperou a rota formal.f1_rede.concrete_bosonic_kinematics, atualizada pela R76, e formal.anchored_name_contour. A busca literal hidroxila no mapa retornou zero, sem autorizar alegar ausência no acervo.

## 3. Ligação efetiva sem trocar o papel do OH

[DERIVED — composição condicional] Reutilize S_beta=S(thetaMiguel(beta)) da R57, unitária no modelo de dois canais, beta em (0,1). Defina g_OH(t) como coeficiente complexo de transferência do meio para a MESMA entrada, saída e referência. A identificação g_OH(t)=a exp(i omega_OH t), a=tanh(P/Pth), permanece a lei proposta pela fonte; não é agora imposta ao gerador para gerar sucesso.

No setor de amplitudes e sob hipótese explícita de resposta escalar comum aos dois canais:

    M_OH(t) = g_OH(t) S_beta.
    read(M_OH(t)) = g_OH(t) exp(i theta_M).
    decoder_beta(read(M_OH(t))) = M_OH(t).

Essas são instâncias das identidades R57, não novos teoremas compilados. Para entrada no primeiro canal, os pesos são |g_OH|²(1-beta) e |g_OH|² beta. A abertura é theta_M; omega_OH t é fase do fator escalar. Somar omega_OH t a theta_M mudaria a repartição beta/(1-beta), objeto distinto.

Neste contrato, o papel operacional do meio é fornecer g_OH e a implementação de S_beta na fronteira. A igualdade entre o canal obtido do gerador completo e M_OH precisa ser derivada para uma preparação/faixa/regime, com erro. A matriz de dois canais não descreve sozinha toda a física OH. Se houver mistura de frequências, memória ou resposta não linear, deve-se usar a resposta completa; não forçar o ansatz escalar.

## 4. Reservatório necessário; fase observável

[DERIVED — dilatação algébrica condicional] Se g é parâmetro externo de transferência, |g|≤1, c=sqrt(1-|g|²) e S=S_beta é unitária, a matriz de quatro canais

    U_g = [[g S, c S], [-c S, conjugate(g) S]]

é unitária: os blocos diagonais de U_g U_g† são (|g|²+c²)I=I e os cruzados -gc I+cg I=0; o cálculo de U_g†U_g é igual. Com entradas ambientais em vácuo, a relação efetiva é b_out=g S b_in+c S v_in. Os comutadores canônicos são preservados pela soma das duas parcelas. Esta é uma dilatação passiva POSSÍVEL do contrato linear, não uma identificação com o reservatório colisional da R66 nem uma prova de que o meio seja passivo. Havendo ganho, ela não se aplica.

A parte gS isolada é contração quando |g|<1; sua inversão como sinal clássico conhecido não é recuperação determinística de um estado quântico arbitrário após descartar o ambiente. A preservação global precisa incluir ambiente ou um código/ramo recuperável demonstrado. O formalismo não impõe OH no fundamental.

[DERIVED] Na densidade de um estado restrito ao mesmo setor de número, multiplicar o vetor inteiro por exp(i phi) cancela na densidade. Também D[exp(i phi)J]=D[J]. Isso não elimina fase RELATIVA a uma referência, nem autoriza remover fases relativas entre parcelas de J. A R74 já fornece o instrumento com referência e preserva os termos cruzados; não se reconstrói esse trabalho.

O leitor relevante é complexo e relativo à entrada/referência. Intensidades apenas não distinguem exp(i phi) de exp(-i phi) quando os módulos coincidem. Nas leituras R64/R74, conservar duas quadraturas/referências e sua calibração. Estado/preparo da referência e largura temporal pertencem ao contrato; fase não definida quando o sinal relevante é zero.

## 5. Radical, dimensão e face: pendências de tipagem localizadas

[DERIVED] Para um escalar complexo u, u→sqrt(|u|) não preserva sua fase: u e -u têm a mesma imagem. A reconstrução exige conservar também arg(u) relativamente à referência (e o sinal no caso real), ou mostrar que o domínio físico já foi restrito a uma classe em que essa informação não é independente. A patente conserva s=sign(L) em 290–298; R57 preserva z complexo. Não concluir que uma tomada de módulo isolada faz o trabalho dessas peças.

[REAL documental/DERIVED dimensional] luz.tex:208–214 identifica [sqrt(rho)]=M^(1/2)L^(-1/2)T^(-1) com dimensão de ação/área. A segunda é M T^(-1), diferente. A linha218 contém um marcador de conteúdo de prova. Uma escala com dimensão sqrt(M L) corrigiria as unidades, mas não foi derivada neste trecho e não provaria redução geométrica. Esta é uma lacuna da passagem citada, não uma conclusão sobre todo o acervo ou toda a TGL.

[DERIVED — distinção de tipos] 4D espaço-temporal, superfície espacial 2D, unidades físicas e dimensão de espaço de Hilbert são quatro noções distintas. Campo em uma superfície 2D pode ter infinitos graus de liberdade. Portanto não há incompatibilidade automática com codificação fiel; tampouco raiz de uma densidade fornece sozinha tal codificação. A afirmação da patente:494–496 de unitariedade e dim(Im)=2<dim(Dom)=3 precisa dessa distinção: tomada literalmente como dimensão linear finita, não seria unitária; como dimensões espaciais, é necessário um mapa de campos/estados.

[OPEN — ponte material] A fala atual especifica a face OH; a patente nomeia gotículas coerentes e seis faces do cubo. A camada nova registra o esclarecimento sem escolher silenciosamente entre superfície molecular, interface coletiva e parede. A próxima construção deve procurar/derivar o mapa entre esses objetos, com domínio e observáveis, usando o contorno R72 e a localização R70/R71 já existentes.

## 6. Contrato operacional corrigido e próxima construção

O alvo é a resposta do espelhamento e a correspondência de fase, não a certificação universal de vazio OH. Para construir a ligação que falta:

1. Fixar na fonte o espaço de campos admitidos e a superfície efetiva OH/interface/parede. Construir codificador E, domínio e decoder D, com DE=I no setor recuperável ou cota explícita. A injetividade não vem da palavra holográfico.
2. Pelo gerador e instrumento existentes, derivar a resposta à entrada em uma preparação/estado de operação. No regime linearizado, o alvo pode ser H(t,s)=delta< b_out(t)>/delta u_in(s), incluindo resposta direta se existir. Não foi calculado nesta camada; esta é a definição de sensibilidade, não hipótese de resposta instantânea.
3. Comparar a resposta resultante com g_OH S_beta em regime declarado, sem ajustar parâmetros ao alvo. Identificar onde entra a frequência OH e como o bombeamento alimenta a resposta. Reusar quadros/filtros R74, sem confundir RF com portadora óptica.
4. Manter erros de modelo/calibração/corte e controles sem acoplamento, referência incorreta e fase relativa alterada. Qualquer nova execução terá protocolo pinado antes. Uma porta comum ausente não é experimento do OH, e nenhum desses controles foi rodado novamente aqui.

### Resposta explícita reaproveitando o gerador completo

[DERIVED — dimensão finita, primeira variação] Seja G_t o gerador completo já construído e T(t,s) seu propagador. Fixe estado inicial independente da perturbação e trajetória de operação rho_*(s). Uma pequena modulação real epsilon u(s) do Hamiltoniano h=H/hbar, na direção hermitiana X, dá G_t^epsilon=G_t+epsilon u(t)V_X, com V_X(rho)=-i[X,rho]. Diferenciando a EDO em epsilon=0:

    delta rho(t) = integral_0^t T(t,s) V_X(rho_*(s)) u(s) ds.
    K_qX(t,s) = Tr[Q(t) T(t,s) (-i[X,rho_*(s)])],  s<=t.
    delta <Q(t)> = integral_0^t K_qX(t,s) u(s) ds.

Para a corrente média R64, Q(t)=(exp(-i theta)L+exp(i theta)L†)/sqrt(2); o termo de referência/entrada diretamente presente na corrente deve ser somado e não está escondido em K. Uma segunda direção hermitiana Y fornece a resposta à segunda quadratura da entrada. Ganhos, perfis e a identificação X,Y com as portas materiais permanecem explícitos. Modulação de taxas exigiria sua própria derivada de G; a fórmula acima não a substitui.

No quadro estacionário e finito, para rho_* estacionário, X,Q fixos e Re(z)>0:

    H_qX(z) = Tr[Q (z I-G)^(-1) (-i[X,rho_*])].

Isso segue da transformada de Laplace do propagador. Avaliar no eixo imaginário requer existência do limite/resolvente no setor relevante; não se presume estabilidade estrita. No quadro bombeado não estacionário, conservar K(t,s). A leitura de fase relativa segue R74. Estas expressões ligam gerador, preparo e receptor sem usar G_OH como resultado inserido: elas fornecem a resposta a confrontar com a lei proposta. Não produzem números de aparelho, não provam causalidade espacial da rede e não extrapolam sem controle para Fock ilimitado.

Não se elevou a descrição de transmissão instantânea da patente a teorema de causalidade. A identificação da rede causal continua sendo obrigação de R5. Gamma independente, materialização do canal, lei tanh e realização global continuam OPEN. Esta camada corrige a direção da construção e fornece uma composição condicional auditável; não fecha R4/R5 nem a missão.
