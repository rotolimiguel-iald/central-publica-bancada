# F1.REDE — contrato conectado, versão R1

**Estatuto: [DERIVED — candidato].** Contrato completo quanto a objetos, hipóteses,
consumidores e falsificadores; a realização integral da rede 4D continua aberta.
Base de pensamento: v392 autorizada pelo operador. Nenhum original ou produção foi editado.

## 1. O que os seus textos já dão

O MQC fornece a célula cúbica de 27 sítios e seis interfaces; o Supercondutor
fornece os modos de entrada/saída, OH, Hamiltoniano e salto dissipativo. A Ψ-NET
fornece o protocolo e o TGL-Tensor a representação. O artigo *A Ponte* explicita
a montagem local covariante condicional, e Q6 exige inclusões isométricas que
entrelaçam operadores. O manuscrito já tem o modelo GHZ N=4,5: ele é reaproveitamento.
Os caminhos, hashes completos e linhas/páginas estão em `sources/ARTICLE_SOURCE_PINS_R1.json`.

A confirmação «Sim está na central de patentes» identifica o acervo. O nome do
dispositivo continua ambíguo; o contrato conserva MQC e Supercondutor como fontes
físicas relacionadas, sem escolher uma identidade não confirmada.

## 2. Construção finita exata

Para uma célula/rede com sítios V, dimensões d_v e regiões R⊆V:

    H_V = ⊗_(v∈V) C^(d_v)
    A_V(R) = B(H_R) ⊗ I_(V\R).

Se R⊆S, escrever H_S=H_R⊗H_(S\R) dá a inclusão A(R)→A(S), A↦A⊗I.
Se R∩S=∅, as matrizes atuam em fatores diferentes, portanto AB=BA.
Isto constrói uma rede local finita [DERIVED]; não é uma suposição de isotonia.
As arestas determinam os termos de interação e canais entre suportes.

O H_eff e o salto da fonte são mantidos, com a correspondência de notação explicitada:

    H/ℏ = ωc(n_in+n_out) + ωOH σ+σ−
          + gJC(a_in†σ− + σ+a_in) + Ω(σ+ + σ−)
    L_holo = a_out†σ− + σ+a_in
    L(ρ) = −i[H,ρ]/ℏ + Σ_j γ_j D[L_j](ρ),  γ_j≥0
    γ_holo = β γΛ,  β = ALPHA_FINE_CODATA_2018 √e (runtime).

No modelo finito, esse gerador produz um semigrupo CPTP. Para modos bosônicos
sem truncamento, domínios e existência do semigrupo são obrigações adicionais.
A contabilidade de energia é d⟨H⟩/dt=Tr(ρ L†H)+Tr(ρ ∂tH): dissipação e
bombeamento aparecem como fluxos. Não há conservação do sistema aberto isolado
sem contabilizar esses fluxos.

O protótipo físico exige calibração das taxas, dimensões, tempos e perdas.
Parâmetros de teste sintético são [INPUT], não medidas da máquina nem parâmetros
ajustados para produzir concordância.

## 3. A informação que atravessa cada interface

O código L↦(√|L|,sign L) é invertível sobre o número real antes da quantização.
Com b bits, o arredondamento perde informação e a reconstrução tem erro mensurável.
Para transportar um estado quântico desconhecido, o contrato exige outro objeto:
Φ(ρ)=Σ K_jρK_j†, ΣK_j†K_j=I. Medição seguida de preparação deve ser marcada
como tal. Preservação de emaranhamento exige teste/prova do canal correspondente.

A Ψ-NET pode endereçar, sincronizar e comandar essas portas. Essa atribuição
operacional não prova que a codificação clássica implemente um canal quântico.
PsiBit, bit e qubit já têm distinção expressa no Tratado, seção 05, linhas 26–44.

Para um qubit normalizado, positividade dá |ρ01|²≤ρ00ρ11≤1/4. Portanto a coerência
que pode aproximar-se de um é C=2|ρ01| (ou outra normalização explicitada), não
o elemento bruto. O acervo já contém um modelo MQC com C normalizada; o contrato
deve consumi-lo, preservando ao lado a notação histórica do PDF.

## 4. A ligação modular que o modelo realmente permite

Para uma densidade fiel ρ>0 em B(H), usar o Hilbert de Hilbert–Schmidt:

    Ω = ρ^(1/2),  ΔX = ρXρ^(-1),  JX=X†,
    σ_t(A)=ρ^(it) A ρ^(-it).

Este é o fluxo modular do estado, distinto do semigrupo dissipativo que pode
produzi-lo. Se o estado estacionário tiver núcleo, a inversa exige restrição de
suporte ou nova formulação. Takesaki entra no ponto exato: para uma subálgebra,
verificar a invariância modular e a expectativa condicional preservadora de estado.
F1.TAKESAKI trata essa passagem; não há motivo para duplicá-la.

Também há uma restrição dimensional concreta. Para uma região de r qubits,
dim span(A(R)Ω)≤4^r. Na representação física de 27 qubits, dim H=2^27;
uma única célula local de um qubit não pode tornar Ω cíclico no Hilbert inteiro.
Logo a passagem a uma rede contínua com o requisito local de vácuo exige um limite
controlado e uma representação apropriada, não mera renomeação dos 27 sítios.

## 5. Nova construção já compilada: rede da reta

`light_ray/ConcreteLightRayNet.lean` constrói K_a=U(a)K_0 a partir do O16.
Prova isotonia, covariância por translação/dilatação e K_a≠0. A revisão independente
recompilou o mesmo `.olean` e verificou os pins. O controle negativo preserva o
teorema que veda translações fiéis em quatro dimensões obtidas através de uma só
coordenada linear. Não veda a construção 4D com sua estrutura completa.

As dependências formais, comandos, LEAN_PATH, tempos, axiomas e hashes ficam nos
recibos `RESULTADO_LIGHT_RAY_R1.json` e `review_light_ray/REVIEW_LIGHT_RAY_R1.json`.

## 6. Construção da rede 4D e obrigações de identificação

O alvo é o H1 existente: L² da órbita sem massa com fibra C², não outro Hilbert
isomorfo sem identificação de operadores. Para a representação de Wigner ±1,
fixa-se a ação de Poincaré com a fase de helicidade e sua extensão antiunitária.
Ela deve restringir-se exatamente a U1 nas translações e B0 no boost escolhido.
O cociclo removido nesse boost deve ser apresentado por um entrelaçador unitário;
rotações e outros planos não são preenchidos pela matriz angular 2×2 do O16.

O esquema BGL parte desses dados e define S_W=J_WΔ_W^(1/2), K(W)=Fix(S_W),
com Δ_W^(it)=U(Λ_W(−2πt)). Para regiões convexas causalmente completas,
K(O)=∩_(W⊇O)K(W); as demais regiões usam extensão local. Standardness,
covariância, dualidade e isotonia têm hipóteses precisas na fonte [KNOWN].
Referência: [BGL, proposições 2.3–2.4, teoremas 2.5/3.4 e corolário 3.5](https://arxiv.org/abs/math-ph/0203021).

No kernel, a rota é concreta: carta orbital→rapidez; Fubini L² vetorial;
Fourier parcial; multiplicador; J; T=Δ^(1/2); S=JT; Δ=S†S.
`D1a3OutputBGL` já tipa o alvo; a construção deve fornecer seus campos, domínios
e provas. A ponte Fubini está em construção separada desta R1 e não é promovida
a equivalência pronta por este documento. O sinal −2π deve ser conferido com a
convenção do Fourier e do boost; não se copia da reta por semelhança.

Com K(O), a camada bosônica usa Fock simétrico e álgebras geradas pelos Weyl W(f),
f∈K(O), com fecho de bicomutante. Na convenção
W(f)W(g)=exp(−i Im⟨f,g⟩/2)W(f+g), ortogonalidade simplética fornece comutação.
Os campos do FockCertificate e do MaxwellCertificate exigem seus próprios
habitantes e pontes; a definição da álgebra sozinha não os fornece.

## 7. Do dispositivo à rede contínua

A família G_ε precisa de mapas coerentes, estados positivos e convergência de
correladores. É necessário demonstrar o limite de energia positiva, covariância
relativística e helicidades ±1; depois exibir V com VU_device=U1V e
VB_device=B0V. Esse é o conteúdo que faria da rede do dispositivo uma realização
da rede canônica, além de uma analogia de geometria/informação [OPEN].

Os escritos já pedem inclusões que entrelaçam operadores: Q6, linhas 169–206.
O contrato atual torna explícitos os objetos e falsificadores dessa exigência.

## 8. Curvatura e alcance da conclusão

Reaproveitar o ligante auditado da F2.3: H3 em todo ponto/direção nula,
conservação e hipóteses do atlas dão a equação de Einstein no alcance já fixado.
Nem o protocolo nem o dispositivo, por si, descarregam H3.

Há uma ressalva matemática ao lado de *A Ponte*, linhas 1517–1532. Um atrator
único que produzisse estados compatíveis com todos os morfismos ainda seria um
estado natural. Chamá-lo de colapso não evita essa propriedade. O teorema de
Fewster–Verch requer localidade dinâmica, uma representação GNS fiel com
Reeh–Schlieder em espaço-tempo de Cauchy não compacto e, para trivialidade total,
localidade estendida. É preciso identificar qual hipótese não se aplica ou
delimitar a categoria; a simples unicidade não faz isso [DERIVED/OPEN].
Fonte: [Fewster–Verch, definição 6.12 e teorema 6.13](https://arxiv.org/abs/1106.4785).

## 9. Critério de conclusão e fiscalização

`CONTRATO_REDE_R1.json` contém nove blocos N0–N9, entradas, saída, consumidor,
obrigações, fontes e falsificador de cada um. O êxito da rede finita e da reta
não satisfaz automaticamente o critério da rede 4D. A revisão DeepSeek tem
identidade preservada na fila e entra como [DECLARADO] até conferência local.

Esta construção não abre dado observado nem produz sigma experimental. Não
altera kernel, um.py, Bancada produtiva, patentes, ratificação ou gate.
