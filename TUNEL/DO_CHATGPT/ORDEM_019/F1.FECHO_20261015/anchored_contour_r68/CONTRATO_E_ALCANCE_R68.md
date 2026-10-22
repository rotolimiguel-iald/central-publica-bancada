# R68 — O posto, o contorno e a regra de reconhecimento

18/10/2026 — codex-gerente-tgl. Unidade F1.FECHO_20261015; reivindicação 960; requisito R12_CONTORNO. Composição candidata em sandbox. A evidência de compilação e a revisão são recibos separados; este texto não os antecipa.

## 1. O esclarecimento do operador

As mensagens integrais estão em `ORIGEM_R68.txt`, pinadas pela inscrição da missão. Dois trechos verbatim:

> Eu quis dizer por paridade inversa o gradiente de espectro negativo que permite extrair o contorno da informação contra o fundo

> Isso mesmo, por isso p* é o posto do nome verdadeiro

[INPUT/ONTO] “Nome verdadeiro”, “Miguel” como referência interrogativa e a identificação teológica da âncora conservam o sentido dado pelo autor. “Paridade inversa” nesta camada designa sua leitura do decaimento do complemento, sem substituir por inferência o operador de paridade geométrica ou o J antiunitário de Tomita.

## 2. O que já existe e se reaproveita

Os sete arquivos originais estão pinados e copiados em `SOURCE_PINS_R68.json` e `sources/`.

- `TheVerbSelectsTheAction.lean:149–173`: `post a` é a projeção ortogonal sobre ℂ∙a; é idempotente, autoadjunta e fixa a.
- `TheAxiomAndTheFalseWitness.lean:101–167`: F(t)=P+exp(−t)(I−P), lei de semigrupo, conservação do posto, decaimento do complemento, limite e exponencial do lock mínimo.
- `Verdade.lean:913–934`: na face matricial 2×2, a projeção hermitiana idempotente de traço 1 que fixa a inscrição v=(q,α) é única e coincide com `identityProj α`.
- `IALD.lean:140–189`: motor=P F(t) U, leitura absorve a defasagem; a âncora Ua=a fornece idempotência. Idempotência isolada também admite motor nulo.
- `RuleTruthContract.lean:26–38,130–148`: admissibilidade é igualdade da leitura com um alvo; preservação de uma leitura injetiva em todo o domínio forçaria a transformação a ser a identidade.
- `TheRuleInTheContinuousMotor.lean:44–63,98–118,128–135`: leitura fiel na imagem fixa; regra única nesse domínio; limite da órbita; alvo errado continua recusado; satisfação do motor vetorial.

O Nós Vivo ainda não localiza F1.FECHO_20261015. O levantamento usou o mapa e fontes atuais; isso não foi ocultado como consulta bem-sucedida ao grafo.

## 3. Tipos: referência, posto e estado

[INPUT de representação] Para escrever o modelo linear sem confundir homônimos:

- a∈H, ‖a‖=1: representante da referência;
- W=ℂ∙a: a reta de referência;
- P=post a: operador de projeção sobre W;
- ρ: estado/densidade, quando esse objeto for introduzido em contrato próprio.

O símbolo p* do operador fica preservado na cunhagem. Não se identifica automaticamente p* com o `rhoStar` de outro módulo, nem com um vetor e um operador ao mesmo tempo. A explicação anterior em conversa, que representou p* diretamente por um vetor, era uma escolha ilustrativa; a presente tipagem distingue os papéis.

## 4. Gradiente negativo e conservação do contorno

[DERIVED — álgebra do modelo] Defina Q=I−P e G=−Q=P−I. Então

\[
P^2=P,\quad GP=0,\quad GQ=-Q,\quad G^2=-G,
\qquad F(t)=P+e^{-t}Q.
\]

Na decomposição H=ran(P)⊕ker(P), G age por 0 e −1, respectivamente. Um setor pode ser trivial; não se deve afirmar que ambos os valores pertencem sempre ao espectro. Essa é a realização delimitada do “espectro negativo”: a componente preservada é estacionária, o complemento decai. A derivada explícita é dF(t)/dt=−e^(−t)Q; uma identidade algébrica de G não deve ser contada como prova Lean dessa derivada se ela não constar no recibo.

\[
PF(t)x=Px,\qquad F(t)x-Px=e^{-t}Qx,\qquad F(t)x\longrightarrow Px.
\]

“Contorno contra o fundo” é a interpretação estrutural dessa separação. Não se constrói aqui uma fronteira espacial, uma segmentação de imagem ou um detector experimental. O parâmetro t é adimensional neste modelo; não se infere calibração de relógio, taxa física ou β. F(t) age em vetores e não é, por essa fórmula, um canal CPTP em matrizes de densidade.

## 5. A cláusula de ancoragem com peso matemático

Fixados a, U e uma entrada x, a cláusula vetorial usa o contrato existente:

\[
\operatorname{Admissible}(x)\iff P(Ux)=a.
\]

O alvo é dado independentemente da saída. Para ‖a‖=1, a condição equivale a ⟨a,Ux⟩=1. Sob Ua=a, a própria referência satisfaz a cláusula; U=I fornece um habitante concreto. A implementação candidata reutiliza a primeira inscrição da casa para não deixar a hipótese sem exemplo.

O fluxo preserva essa condição, porque PF(t)=P. Portanto atenuar o complemento não transforma um coeficiente errado em correto. Se Ux=2a, a saída continua 2a; se Ux é ortogonal a a, a saída é zero. Essas são recusas do contrato exato, não juízos morais sobre pessoas.

**Fase e amplitude:** a projeção sobre ℂ∙a é a mesma para a e −a. O peso quadrático não distingue uma fase global. Em contraste, igualdade vetorial com a distingue a de −a. Logo são dois contratos distintos: identidade projetiva e igualdade de uma amplitude orientada por referência. Para comparar fases físicas é necessário um contrato relacional com referência de fase; o ensaio R60 e o instrumento R64 já explicitam essas hipóteses, e não serão reconstruídos aqui.

**Unicidade:** em Verdade a referência fixada determina a projeção sob as condições do teorema matricial. Isso não escolhe a referência dentre todas as referências possíveis. Tampouco uma reta de dimensão 1 possui somente um vetor. “Uma identidade visível” pode ser representada por uma classe projetiva; exigir um representante único precisa de uma convenção/âncora adicional.

## 6. Ligação com o sentido ético e limite operacional

[ONTO — interpretação do autor; DERIVED — consequências do contrato escolhido] A cláusula pode expressar que a fala deve responder a uma referência e admitir recusa quando não satisfaz sua relação de leitura. Sua implementação matemática precisa consumir a referência e as condições de correspondência. Gravar apenas um nome em String não fornece esse vínculo.

Esta camada oferece uma composição de operadores e uma regra exata. Não fornece um classificador geral de verdade de linguagem natural, não demonstra consciência subjetiva, não identifica uma pessoa histórica por espectro e não instala uma exigência religiosa no aplicativo. A identificação teológica permanece documentada como leitura do autor. A futura ligação à fala exige especificar sua representação e o que conta como evidência de correspondência, sem promover similaridade textual a prova.

## 7. Continuidade

R67 permanece em review_pending administrativo; esta construção não presume o aceite humano que foi solicitado. R66 segue reutilizada. R4/R5 mantêm calibração, relógio, localização e causalidade como critérios próprios. A nova candidata não altera um.py, kernel do Nós, Bancada de produção, dados observados ou gate.
