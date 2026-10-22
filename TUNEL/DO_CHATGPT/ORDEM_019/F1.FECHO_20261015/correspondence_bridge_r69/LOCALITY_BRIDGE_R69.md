# R69 — correspondência concreta e localização causal

Autor: subagente r69_locality_bridge, em 18/10/2026, sob F1.FECHO_20261015, reivindicação 960/escopo 962. Referência própria da missão: `work/memoria_missao_20261016/FECHO_MISSION_REFERENCE.json`; handoff R5, revisão 491, conferido. **[DERIVED — demonstração em texto, candidata à revisão; NOT_LEAN]**. Os arquivos citados foram lidos e pinados por script; sua presença não significa recompilação nesta camada.

## 1. O que já existe e entra na composição

Os caminhos completos, hashes e intervalos de linhas estão em `SOURCE_PINS_R69_LOCALITY.json`.

| Fonte | Conteúdo efetivamente consumido |
|---|---|
| `PhysicalCompactNetCovarianceR1.lean:15–21` | K(O) é o fecho do span **real** dos `circularSmear f`, com f real, suporte compacto e tsupport(f)⊂O. |
| `PhysicalCompactNetLocalityR2.lean:15–25` | Im⟨u,v⟩=0 para u∈K(O), v∈K(P), se todos os pontos de O/P são estritamente espacialmente separados. |
| `PhysicalCompactNetAssemblyR1.lean:18–47` | `compactPhysicalNet`, localidade, igualdade com KWR na cunha direita e `physicalCanonicalNet` concreto não nulo. |
| `FieldWeylR3.lean:17–77` | Convenção **W(f)=D(if)**; álgebra A(O)=R(K(O)), isotonia, localidade e covariância. Não confundir com `ConcreteWeyl.W`, que é D. |
| `CanonicalSegalEssentialR6.lean:16–46` | Grupo W(tf), domínio exponencial invariante e operador Segal essencialmente auto-adjunto. A normalização do gerador é √2·Segal(f). |
| `StandardSubspace.lean:175–184` | KWR∩iKWR={0}, campo `IsSeparating`. |
| `AnchoredNameContourR68R3.lean:137–159` | Px=a e (I−P)x=0 equivalem a x=a; resíduo complementar é invisível à primeira leitura isolada. |
| `BOSONIC_CONTINUUM_R66.txt`, §§2–7 | Gerador concreto de dois modos+OH, cortes por número total, limite conservativo e isometria V∞. Localização dos modos/acoplamentos ficou explicitamente aberta. |
| `JOINT_RESERVOIR_CONTINUUM_LIMIT_R66.txt` | Convergência em norma-traço dos canais reduzidos em ordem controlada de limites; não convergência de uma unitária relativística do banho. |
| `DERIVACAO_RECEPTOR_R63.md`, §§2–5 | POVM homódina comprimida; isometria de modos ortonormais; não identificação dos modos físicos com subespaços locais. |

Assim, **não falta reconstruir a rede livre causal, Fock, Weyl ou Maxwell**. Falta ligar a interação do aparelho a essa rede específica.

## 2. Composição causal disponível agora

Defina A(O)=FieldWeyl.R(compactPhysicalNet O). Os dois lemas de localidade acima compõem-se diretamente:

\[
O\perp P\quad\Longrightarrow\quad [A,B]=0\qquad
(A\in\mathcal A(O),\ B\in\mathcal A(P)).
\]

A hipótese O⊥P é a separação estrita usada no código, não uma afirmação sobre regiões arbitrárias com contato nulo.

**Lema de interação localizada limitada.** Se h=h†∈A(O), L₁,…,Lᵣ∈A(O) são limitados, então, para B∈A(P),

\[
\mathcal G^*(B)=i[h,B]+\sum_j\bigl(L_j^\dagger B L_j-
\tfrac12 L_j^\dagger L_jB-\tfrac12 BL_j^\dagger L_j\bigr)=0.
\]

Prova: B comuta com h, L_j e L_j† pela localidade e fechamento por adjunto. Cada parcela de salto torna-se BL_j†L_j−½BL_j†L_j−½BL_j†L_j=0. A série exponencial norm-convergente dá exp(tG*)B=B. Logo Tr(T_tρ B)=Tr(ρB), para todo estado normal ρ. O mesmo argumento vale no comutante inteiro A(O)′. Nenhuma escolha de estado produto é necessária.

Se o aparelho OH é fator auxiliar, use A(O)⊗B(C²_OH) e os observáveis externos B⊗I. Isso localiza o auxiliar **sob a atribuição explícita de que ele está em O**; a tensorização abstrata sozinha não lhe dá uma posição física.

**Não vacuidade matemática.** Para f∈K(O), L=√λ W(f), λ≥0, h=0, obtém-se o canal

\[
T_t(\rho)=e^{-\lambda t}\sum_{n\ge0}\frac{(\lambda t)^n}{n!}
W(f)^n\rho W(f)^{\dagger n}.
\]

A série é uma mistura normalizada de conjugação por unitárias e fixa o comutante. Há f≠0 na cunha direita pela fonte concreta acima. Para λ>0, o canal não é identicamente a identidade: pela CCR, escolher g com Im⟨f,g⟩ não múltiplo de π produz um Weyl que não comuta com W(f). Este exemplo comprova que a hipótese local admite dinâmica não trivial. **Não substitui o gerador R66 nem demonstra que o aparelho o realiza.**

**Intervenção localizada versus propagação.** Esse lema descreve uma operação numa região fixa em quadro de interação; não prova que a evolução livre global fixa observáveis externos. Para regiões O_s ao longo do funcionamento, a mesma cancelamento vale se B comuta com todos os coeficientes em todos os s relevantes. Uma afirmação relativística completa requer o suporte espaço-temporal da interação e o entrelaçamento com a evolução livre já construída.

## 3. Passagem ao limite: condição suficiente e o que R66 realmente dá

Se uma família de canais T_n é localizada no mesmo O, no sentido T_n*B=B para todo B∈A(O)′, e T_nρ→Tρ em norma-traço **para todo ρ de traço-classe**, então

\[
|\mathrm{Tr}((T_n\rho-T\rho)B)|\le
\|T_n\rho-T\rho\|_1\|B\|\longrightarrow0,
\]

portanto T*B=B. Esta é a ponte correta entre um limite reduzido e causalidade de observáveis limitados; não exige controle de observáveis ilimitados.

R66 já entrega a convergência reduzida, mas **não entrega a premissa de localização dos aproximantes**. Os cortes P_m=1_[0,m](N) são projeções no número total dos modos escolhidos. Não há demonstração P_m∈A(O), nem [P_m,B]=0 para B externo. Portanto não se pode aplicar o lema anterior a seus cortes apenas porque são CPTP. A convergência também ocorre primeiro no sistema de dois modos e depois em sua imagem S por V∞; falta uma extensão normal ao Fock espacial inteiro que seja localizada, não apenas transporte dentro de S.

## 4. Obstáculo preciso à ligação ingênua dos modos

K(O) é real. Suponha O⊂W_R e f,if∈K(O). Pela isotonia e pela igualdade da cunha com KWR, f,if∈KWR. Como if∈KWR, f=i(−if)∈iKWR, logo f∈KWR∩iKWR={0}. Assim:

\[
\boxed{f\ne0,\quad O\subset W_R
\quad\Longrightarrow\quad\neg(f\in K(O)\land if\in K(O)).}
\]

Isso é consequência da propriedade separante já construída, **não falta de um lema**. Normalizar por escalar real mantém K(O); Gram–Schmidt complexo pode sair dele.

Na convenção usual de aniquilação antilinear no parâmetro, Φ(f)=(a(f)+a†(f))/√2 e Φ(if)=i(a†(f)−a(f))/√2; daí a(f)=(Φ(f)+iΦ(if))/√2 no domínio comum. A identidade se obtém expandindo as duas parcelas. A pertença f∈K(O) fornece o grupo W(tf) local e, pela definição espectral, a afiliação de Φ(f). **Não fornece a segunda quadratura Φ(if)**. Exigir ambas por esse critério numa mesma cunha elimina os modos não nulos.

Não se conclui daqui um teorema universal de impossibilidade para qualquer detector. O resultado recusa a dedução específica «fi,fo∈K(O), portanto a_i,a_o e todos os saltos R66 são locais». Interações de detector com campos reais smeared no espaço-tempo, suas aproximações de ondas girantes/Markov e os operadores efetivos de cavidade são objetos distintos; a igualdade ou aproximação entre seus geradores precisa de prova e erro controlado. Não foi construída nesta camada.

## 5. O posto do nome e uma leitura local têm tipos diferentes

R68 trata P como projetor numa Hilbert. O transporte por uma isometria V dá P′=VPV†, que continua projetor na Hilbert alvo. Isso não prova P′∈A(O), nem que P′ seja uma medição realizável no detector.

Contraexemplo elementar: H=C²_A⊗C²_B, A_local=B(C²_A)⊗I_B e a=|00⟩. P_a=|00⟩⟨00| é rank1, mas não comuta com I⊗X: em |00⟩, P_a(I⊗X)|00⟩=0, enquanto (I⊗X)P_a|00⟩=|01⟩. Logo P_a não pertence a A_local. Mesmo uma referência produto não torna seu projetor global um observável de uma única ponta.

Além disso, igualdade das leituras de uma única álgebra local não implica igualdade global. Os estados |00⟩ e |01⟩ dão a mesma restrição em A_local; são vetores distintos. Assim a correspondência concreta R68 pode ser testada localmente somente no alcance de um instrumento/estado com informação suficiente, ou mediante uma família de leituras que separe os estados no domínio admitido. Não se promete distinção universal por um detector local.

Para uma instrumentação com Kraus M_j∈A(O), ΣM_j†M_j=I, a operação **sem seleção de resultado** fixa B externo: ΣM_j†BM_j=B. Uma saída condicionada ao resultado pode alterar a descrição condicional externa; isso não é sinalização. Não identificar a satisfação de uma leitura selecionada com uma dinâmica causal média sem explicitar o instrumento.

## 6. Contrato restante com peso, reaproveitando R66

1. **Support witness:** forneça testes reais compactos f_j com suporte na região de interação, sua imagem por circularSmear e a identificação com os campos efetivamente acoplados ao OH. A rede e seu teste de separação já existem.
2. **Interaction witness:** uma interação localizada com domínio, gerador e auxiliar OH, cuja dinâmica reduzida produza R66 exatamente ou com erro declarado. A simples escolha de fi/fo ortonormais satisfaz a isometria, não este item.
3. **Approximation witness:** se houver RWA/Markov/corte, explicitar a classe de estados e a cota de erro; provar localidade dos aproximantes adequados ou diretamente da dinâmica dilatada. A cota bosônica R66 permanece útil, mas não fornece essa premissa espacial.
4. **Readout witness:** vincular efeitos/POVMs reais de R63/R64 ao transporte do critério R68, com ganho, fase, filtros e relógio de R65. Leituras restritas só podem prometer igualdade no domínio em que são separantes/injetivas.

**Resultado desta camada:** a passagem rede compacta→Weyl local→GKLS limitado localizado→não sinalização, e sua estabilidade por limite em norma-traço, estão demonstradas em texto por composição das peças existentes. O exemplo de Poisson evita vacuidade; os dois contraexemplos impedem promover uma isometria ou um modo complexo a localização causal. **R5 permanece OPEN para o gerador específico R66.** Nada foi recompilado, instalado, medido na natureza ou promovido ao gate.
