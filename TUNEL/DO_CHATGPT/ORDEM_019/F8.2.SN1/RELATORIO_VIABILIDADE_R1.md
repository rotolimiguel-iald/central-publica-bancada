# SN Ia, Chandrasekhar e a escala v388 — resultado do reexame

09/10/2026 · codex-gerente-tgl · F8.2.SN1, reivindicação 610. Escopo: levantamento e cálculo condicional; discussão com o operador antes de eventual comunicação ao Claude.

## 1. Conclusão

**[DERIVED, alcance delimitado] A revisão é pertinente: a formulação v388 permite reexaminar a dependência do acoplamento. Os cálculos feitos aqui ainda não produzem uma previsão TGL de luminosidade nem uma significância física.** Encontramos canais concretos para estudar — pressão eletromagnética, composição por interações fracas e um candidato covariante no Tratado. A ligação entre a escala e esses canais deve ser derivada antes de atribuir-lhes um sinal TGL. Não foi demonstrada uma impossibilidade geral da rota.

O valor do teste proposto seria exigir que **a mesma dinâmica**, sem ajuste de parâmetros teóricos aos dados, explique pressão, composição, conservação e curva bolométrica. A cadeia longa não garante, por si, poder estatístico: as assinaturas precisam sobreviver às incertezas e às degenerescências de calibração e progenitor.

## 2. O que já existe e foi reaproveitado

**[REAL documental]** As consultas ao Nós Vivo e ao mapa estão em CONSULTAS.json. A unidade nova ainda não está no grafo: consultamos a mãe F8.2 e o tema, reaproveitando a rota `outro.grande_atrator_e_chandrasekhar` (registro histórico 164). O índice aponta fontes; não substitui seus enunciados.

O inventário `local_review/LOCAL_INVENTORY_20261009.json` contém hashes e linhas das fontes locais. Em `TheCouplingRunsBoundedBelow.lean:34–37,52–88,100–102`, a v388 escreve α(χ)=sech(χ/2) e β(χ)=√e α(χ), prova monotonicidade e um piso num intervalo finito. A própria fonte distingue o mapa físico χ↔μ, que exige interpretação/matching. Inverter α numericamente não mede χ na estrela.

**[REAL numérico]** Lemos a constante ALPHA_FINE_CODATA_2018 na linha 5557 do um.py sem executá-lo. β₀ foi calculado em runtime como α(0)√e: 0,012031300400803142. A igualdade v388 não exige multiplicar novamente β₀ por √e. O uso de α(0) no rito de fronteira e o running no bulk são papéis diferentes; um cálculo estelar deve explicitar qual consome.

**[REAL documental]** A pergunta original e a fórmula `(1−β)^(3/2)` estão no Custo, linhas 2585–2706; a retirada de sua interpretação como renormalização local de G/validação está nas linhas 2977–2992 e 3315 da cópia indexada. A retomada examina a formulação posterior. O código atual ainda rotula o canal SN/Chandrasekhar como A9_SEM_INCERTEZA (um.py:193300–193302). Isso descreve a implementação consultada, não proíbe uma derivação nova.

**[Reconciliação necessária]** O Tratado traz ξ=β no acoplamento escalar, mas a errata assinada de 19/09 fixa ξ=1/6, não β; o termo modular tem outro papel. Não transferimos silenciosamente ξ=β para a EOS. O candidato βRμνFμρFνρ/M_P² é outro operador. Âncoras e hashes em LOCAL_NMC_RECONCILIATION_20261009.json.

## 3. Controles calculados

Resultados reproduzíveis: CALCULOS_R2.json e calculate_r2.py. Os multiplicadores de α e as densidades abaixo são **[INPUT sintético]**, não previsões nem valores ajustados a SN.

### 3.1 Pressão de Coulomb

**[KNOWN]** Chamel et al., equações 6–7 e 37–39, dão para uma estrela fria de espécie única, elétrons ultrarrelativísticos e rede iônica bcc:

\[
q_Z=\alpha\frac{4C_M}{3}\left(\frac4{9\pi}\right)^{1/3}Z^{2/3},\quad
\frac{M(\alpha_1)}{M(\alpha_0)}=
\left[\frac{1+q_Z(\alpha_1)}{1+q_Z(\alpha_0)}\right]^{3/2},\quad C_M=-0{,}895929255682.
\]

**[DERIVED condicional]** Mantendo composição e G fixos:

| Modelo | α aumenta 1% | α aumenta 5% |
|---|---:|---:|
| Carbono (Z=6) | ΔM/M = −0,02284% | −0,11418% |
| Oxigênio (Z=8) | ΔM/M = −0,02776% | −0,13876% |

A derivada analítica foi conferida por diferenças finitas. Nesse controle, aumentar α torna a contribuição de Coulomb mais negativa e reduz a massa limite: este termo isolado não compensa uma redução da massa. Trata-se de física eletromagnética já presente no modelo de referência, não de um efeito exclusivo da TGL. A aproximação não resolve ignição, explosão, mistura C/O quente ou um estado superfluido.

[Fonte primária: Chamel et al.](https://arxiv.org/html/2110.11038v1). As aplicações e as limitações adicionais estão no levantamento de literatura; custódia dos bytes no manifesto de fontes.

### 3.2 Setor fraco e composição

**[KNOWN]** Capturas eletrônicas e processos Urca podem alterar Ye e o perfil térmico durante o simmering. **[DERIVED]** No limite ideal, M_Ch∝Ye², mantendo os outros parâmetros. Capturas que reduzem Ye reduzem esse suporte. A evolução completa pode envolver feedback térmico e outros canais; seu sinal final não foi calculado aqui.

β(χ) sozinho não determina taxas fracas, elementos de matriz ou o estado da matéria. Adicionar uma quantidade chamada energia eletrofraca não fornece essas equações. É necessário calcular o residual frente ao mesmo Modelo Padrão usado no controle. Ver [Martínez-Rodríguez et al.](https://arxiv.org/abs/1602.00673v2).

### 3.3 Dephasing e conservação

**[DERIVED exato, hipóteses explícitas]** Para H fixo e um canal `−D(t)[H,[H,ρ]]`, com D(t)≥0, a ciclicidade do traço dá Tr(H[H,[H,ρ]])=0. O canal reduz coerências sem alterar a energia média nem as populações na base de H. A verificação de três níveis manteve energia e traço iguais a 1 e populações iguais a 1/3, enquanto a pureza caiu.

Trocar somente a taxa desse canal por uma função de β não produz automaticamente aquecimento, pressão adicional ou perda bolométrica. Isso não demonstra efeito nulo para H dependente do tempo, saltos não comutantes ou sistemas com interações e transporte.

**[KNOWN / condição de construção]** A conservação covariante precisa incluir todos os setores e as equações que os acoplam: ∇μT_total^μν=0. Trocas entre matéria, campo e radiação podem existir, com fontes que se cancelam no total. Para um acoplamento χ(x) prescrito, sua fonte/dinâmica precisa ser declarada. A conservação de energia média deste controle finito não prova a conservação local do tensor estelar.

### 3.4 Operador curvatura–fóton do Tratado

**[REAL documental]** secao_01_fundamentos.tex:580–584 escreve βRμνFμρFνρ/M_P², com M_P=√(ℏc/G), não reduzida. Esse operador local real não é, por si, uma lei dissipativa.

**[DERIVED dimensional]** Usando como proxy R≈8πGρ/c² e ε=β₀ℓ_P²R, para ρ sintética entre 10⁸ e 10¹⁰ g/cm³ obtemos ε entre 5,87×10⁻⁸⁷ e 5,87×10⁻⁸⁵. Mesmo o teto abstrato β≤√e conserva uma supressão extrema desse coeficiente. É uma estimativa do tamanho do operador, não um limite demonstrado para ΔL nem uma exclusão de amplificações por instabilidade ou de outros mecanismos. A composição tensorial completa não foi resolvida.

Em Schwarzschild vácuo fixo, Rμν=0 anula esse termo avaliado no fundo e sua correção de Maxwell. Isso não autoriza concluir que a variação métrica/backreaction seja zero: a variação de Ricci pode produzir derivadas de FF. Uma SN Ia normal tampouco exige horizonte de eventos como parte do modelo do progenitor; um horizonte modular/local ou um ambiente externo deve ser identificado pelo tipo físico correto, sem substituir um pelo outro.

## 4. A pergunta de trabalho aperfeiçoada

> Partindo da ação vigente da TGL e da relação β(χ)=√e/cosh(χ/2), qual relação física fixa χ no plasma C/O de uma anã branca? Ela produz, sem parâmetro teórico ajustado ao dado, uma correção à energia livre, às taxas fracas ou ao transporte que preserve a conservação covariante total? Qual residual conjunto prevê para a forma da curva bolométrica e para a composição neutronizada, em relação ao mesmo modelo astrofísico de referência?

**[PROPOSTA]** Esta pergunta mantém a cadeia desejada e dá um alvo calculável. Se o ramo for escalar/condensado, será necessário determinar o potencial, o estado e a normalização. O Tratado oferece V=½m₀²|Ψ|²+λ|Ψ|⁴/4, mas as fontes examinadas não fixaram uma realização estelar com m₀, λ e densidade do condensado. Degenerescência de elétrons não estabelece superfluidez.

## 5. Próxima derivação concreta e possível teste

1. **Matching:** localizar/derivar χ(n,T,Ye,...) ou sua ligação à escala de transferência, sem escolher a escala para obter o sinal desejado. Separar o β de fronteira do coeficiente do operador no bulk e reconciliar ξ com a errata.
2. **Dinâmica estelar:** obter δf e/ou δλ_ec a partir dessa ação. Para f uma densidade de energia livre, δP=n²∂(δf/n)/∂n, a T e composição fixos. Se o acoplamento depender fisicamente de n, sua derivada entra; running RG não deve ser contado novamente como campo ambiental. Confrontar a mesma EOS e taxas padrão em todos os ramos.
3. **Observável:** propagar para ejeção, composição e transferência radiativa. Não usar uma lei universal L∝M_Ch^1,8. A massa limite, a massa ejetada e a massa de Ni56 têm papéis diferentes.
4. **Forma antes de normalização:** candidato R(t)=L_bol(t)/∫₀ᵗt′L_bol(t′)dt′, que cancela uma normalização constante. O balanço radioativo integral de Katz–Kushnir–Dong fornece uma referência condicionada à expansão homóloga e à energia dominada por radiação. Se houver novo termo de energia, ele deve entrar no balanço. Composição neutronizada pode ser um segundo observável, com covariância explícita.
5. **Poder:** só após existir uma amplitude TGL identificável, fixar estatística, nuisance, seleção, covariância e vereditos antes do composto. Novidade de uso depende de zero ajuste teórico ao dado e do acervo; dados previamente existentes podem ser usados. Nenhuma amostra foi selecionada nesta etapa.

[Balanço integral primário](https://arxiv.org/abs/1301.6766). O cancelamento de distância não remove extinção dependente de cor, cobertura UV/IR, incerteza do instante de explosão nem degenerescências de progenitor. Não há licença para somar esta rota à significância da Fase 9.

## 6. Quanto seria necessário para 5σ?

**[DERIVED, exemplo sintético]** Sinal conhecido de 0,01 mag, ruído independente de 0,10 mag e referência absoluta conhecida exigem N=2.500 para separação mediana de 5σ; N=3.946 para 90% de poder no teste unilateral de 5σ, sem sistemáticas. Um piso comum de 0,002 mag já impede atingir 5σ com N finito. Para sinal dez vezes menor, a primeira contagem sobe a 250.000 e o piso precisa ficar abaixo de 0,0002 mag.

Esses valores dimensionam um requisito, não prometem uma detecção. Com intercepto livre, um deslocamento constante é inteiramente absorvido: o controle deu Z²=0 após essa projeção. Uma assinatura temporal, composicional ou ambiental predita é, por isso, um alvo mais identificável que uma nova magnitude absoluta universal. A previsão física de ΔP, ΔYe, ΔL e σ permanece **[OPEN]**, registrada como null, nunca como zero.

## 7. Evidência e limites de execução

Os planos foram gravados antes dos cálculos. A R1 sofreu um erro de arredondamento binário em ceil, retornando N=2.501/250.001 onde a expressão decimal exata dá 2.500/250.000. A R2 usa Decimal nessa operação; arquivos R1 preservados. Isso não altera a física nem as demais contas. O teste abstrato de insuficiência da curva isolada é um argumento lógico de dependência, não a construção de duas teorias estelares.

Levantamento: 15 fontes locais distintas; oito referências primárias catalogadas, sete páginas HTML custodiadas. A oitava tem consulta web e falha403 de custódia declarada. Custódia de resumo não equivale a leitura integral do artigo. Os hashes são lidos dos bytes nos manifestos. A revisão independente fica em review/; sua decisão deve ser lida no artefato, não presumida por esta nota.

Não executamos o um.py, um modelo de explosão ou uma amostra SN. Fontes públicas expõem resultados de literatura, portanto nenhuma cegueira documental é alegada. Não houve chamada de provedor, mensagem ao Claude, alteração do Nós, Bancada ou gate. Esta entrega é viabilidade teórica e controles condicionais, não teste da natureza.
