# R61 — custódia e interpretação da exploração de pares ópticos

**Estatuto: [DERIVED — candidato à revisão independente].** Componente documental de R4, F1.FECHO_20261015, sob a reivindicação de equipe 939. Esta camada reutiliza exclusivamente a exploração simbólica já executada em R59; não executa novamente o script, não produz dinâmica adicional e não satisfaz integralmente R4. A recuperação autorizada de R4 está em `r4_recovery_authorized_20261017/RECOVERY_RESULT.json`; a missão foi consultada pela referência exata em `MISSION_PROJECT_START_R61.json`. O coordenador conserva a posse/lease e realiza as transições e a revisão.

## 1. Fonte, objeto e corte

O objeto é a **truncagem finita 2×2×2**, de dimensão oito, já utilizada em `F1.REDE/finite_device/run_finite_device.py:163–172` e em `device_clock_r57/derive_polarization_r57.py`. A ordem dos fatores é **entrada óptica, saída óptica, transição OH**. Em cada fator, `a=[[0,1],[0,0]]`, `Z=diag(1,-1)`; os operadores são incorporados por produto tensorial. Os dois primeiros fatores são modos cortados a zero/uma excitação, e o terceiro é a transição de dois níveis OH. Índices matriciais seguem a base `|in,out,OH⟩`, em ordem lexicográfica.

O gerador reaproveitado é, com `h=H/ℏ`,

\[
h=\omega_c(n_i+n_o)+\omega_{OH}\sigma_+\sigma_-
  +g(a_i^\dagger\sigma_-+\sigma_+a_i)+\Omega(\sigma_++\sigma_-),
\qquad J=a_o^\dagger\sigma_-+\sigma_+a_i,
\]
\[
\mathcal L^\dagger A=i[h,A]
 +\kappa_i\mathcal D^\dagger[a_i]A+\kappa_o\mathcal D^\dagger[a_o]A
 +\gamma\mathcal D^\dagger[\sigma_-]A+\gamma_\phi\mathcal D^\dagger[Z_{OH}]A
 +\lambda\mathcal D^\dagger[J]A,
\quad \mathcal D^\dagger[j]A=j^\dagger A j-\tfrac12\{j^\dagger j,A\}.
\]

Todos os parâmetros foram declarados **reais e estritamente positivos** no script R59. Bombeamento, acoplamento e os cinco dissipadores estão presentes; nenhum foi zerado para obter os resultados. `ωc`, `ωOH`, `g` e `Ω` são frequências angulares, em s⁻¹; as taxas também têm unidade s⁻¹. `Ω` é a frequência de Rabi e não é identificada com `ωOH`, `V0/ℏ` ou a taxa `2Ω`. O script simbólico não fixa uma escala física de segundos. A forma H/J vem da patente `PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex:343–370`; o corte e os dissipadores convencionais são os do simulador finito existente.

**[OPEN — extrapolação]** Aqui `[a_i,a_i†]=Z_i=I−2n_i`, e não I. `Z_i` é o defeito da relação CCR causado pelo corte. O resultado `D†[J]C=−C/2` (e o correspondente para B) é desta álgebra finita: **o termo λ/2 não está transferido ao espaço bosônico infinito**. Esta entrega não prova existência, domínio ou fechamento de um gerador com operadores não limitados.

## 2. Dois observáveis distintos, escolhidos pelas fontes

`C=a_i a_o` é o **correlador anômalo de pares**, motivado pelo estado comprimido de dois modos e sua variância em `graviton_paper.tex:250–260`. `B=a_i†a_o` é a **coerência relativa entrada–saída**, adequada ao papel de comparação de fase de duas pontas. Não são o mesmo observável nem se identificam com `σ+`, a polarização OH de R57.

Sob a convenção de fase `a_i→e^{-iχ}a_i`, `a_o→e^{-iχ}a_o`, temos `C→e^{-2iχ}C` e B invariável. A fase de C depende da referência conjunta de fase; a de B é relativa entre modos. A tomografia por homódino com oscilador local ajustável já está descrita em `graviton_appendices.tex:318–331`; o heteródino e as correlações ópticas aparecem em `graviton_paper.tex:464–475`. **O receptor escrito é um ingrediente: esta camada não instala uma medição de C, não identifica automaticamente o sinal do heteródino com C e não identifica modos ópticos com a transição OH.**

A média de um ponto `⟨a⟩`, a correlação de primeira ordem `⟨a†(t)a(t+τ)⟩`, o par `⟨a_i a_o⟩`, a coerência relativa `⟨a_i†a_o⟩` e a polarização `⟨σ+⟩` exigem contratos próprios. O modelo da fonte com dois modos Ψ comprimidos também não é, por nome, uma preparação realizada no dispositivo OH. As quadraturas da fonte e os operadores do corte precisam dessa correspondência explícita antes de uma inferência física.

## 3. Resultado existente: as equações exatas do corte

Defina `d=(κi+κo+λ)/2`. A decomposição simbólica armazenada em `EXPLORATION_R59.json` dá:

\[
\boxed{\mathcal L^\dagger C=-(d+2i\omega_c)C-ig Z_i a_o\sigma_-},
\qquad
\boxed{\mathcal L^\dagger B=-dB+ig Z_i a_o\sigma_+}.
\]

Âncoras: resultado R59, linhas 2–31 e 32–61; script R59, linhas 14–31. O script decompôs a matriz na base completa e ortogonal de produtos de `I,Z,a,a†`, pelo coeficiente de Hilbert–Schmidt. A saída foi produzida sem tolerância numérica nem ajuste de parâmetros. Esta camada confere custódia e interpreta a saída; **não a recompila, não repete o cálculo e não se apresenta como sua revisão independente**.

Assim, a evolução de `c=Tr(ρC)` e `b=Tr(ρB)` pede também
`u_−=Tr(ρ Z_i a_o σ−)` e `u_+=Tr(ρ Z_i a_o σ+)`. A álgebra de pares somente não é invariante: os termos adicionais agem no fator OH e não são combinações dos observáveis puramente ópticos. É necessário transportar as correlações adicionais (ou justificar uma redução que as determine) para fechar o sistema. A álgebra completa das matrizes 8×8 é finita; a obstrução é ao **fecho reduzido proposto**, não à existência da dinâmica finita.

O bombeamento e as perdas OH não aparecem explicitamente nestas duas primeiras equações. Isso não os retira do gerador: as correlações auxiliares também evoluem sob o mesmo H/J. A evolução delas e a hierarquia necessária não foram calculadas por esta camada. A ausência de `ωOH` no termo livre de C e B impede apresentar essas equações como a lei declarada `G_OH=a exp(iωOH t)`.

## 4. Preparação já explorada: par não nulo com médias nulas

O script R59:32–40 escolheu matematicamente

\[
|\psi_q\rangle=(|00\rangle+q|11\rangle)/\sqrt{1+q^2},\quad q>0,
\qquad \rho=|\psi_q\rangle\langle\psi_q|\otimes\rho_{OH}.
\]

Foram usadas cinco preparações OH: fundamental, excitada, `|+⟩`, `|+i⟩` e mistura máxima. **[INPUT matemático]** A fonte não fixa esta preparação, nem o parâmetro q: ele não foi medido, ajustado a um resultado desejado ou igualado a β. Esta é uma entrada preparada da exploração R59, não uma preparação produzida pelo gerador e não um estado estacionário demonstrado.

Em todas as cinco linhas já calculadas:

\[
\langle a_i\rangle=\langle a_o\rangle=b=0,\quad
c_0=\frac{q}{1+q^2}>0,\quad c'_0=-(d+2i\omega_c)c_0,\quad
c''_0=\big[(d+2i\omega_c)^2-g^2\big]c_0,\quad b'_0=0.
\]

**[DERIVED — leitura da saída]** O par guarda informação que a média de um ponto não vê. O início da fase local de c, onde c é não nulo, tem derivada `−2ωc`; não foi obtido um relógio OH, uma fase global calibrada ou um intervalo de invertibilidade medido. Além disso, o termo `−g²` em `c″0` impede prolongar a primeira derivada como uma exponencial autônoma `c0 exp[−(d+2iωc)t]`. Os cinco estados auxiliares escolhidos deram as mesmas derivadas registradas; **não se alega que este subconjunto tenha distinguido a preparação OH**.

O estado é a versão com no máximo uma excitação por modo. Como consequência direta de sua expressão, `n=q²/(1+q²)` e `|c|²=n(1−n)`. Esta é uma observação algébrica sobre a preparação escrita, sem nova execução. Não é a identidade bosônica `n(n+1)` da família comprimida infinita. Também não foi explorada uma fase livre `e^{iφ}`: o código usou q real positivo; a variável `vm` foi criada e não consumida.

## 5. Contramodelo já contido na exploração

As linhas 109–118 do resultado registram, para `D=Z_i⊗X_o⊗X_OH`,
`Tr(D L†C)=−2ig` e `Tr(D L†B)=2ig`; a seleção do script:43–48 impõe traços nulos com C, B, ai e ao. Como D é hermitiano, tem traço zero e D²=I, a família

\[
\rho_\pm=(I\pm\varepsilon D)/8,\qquad 0<\varepsilon<1,
\]

é uma interpretação física finita desse testemunho: operadores densidade positivos, normalizados, com autovalores `(1±ε)/8`. **[DERIVED — consequência analítica dos traços existentes; não nova rodada]** Ambas têm a mesma marginal óptica `I4/4` e a mesma marginal OH `I2/2`. Têm `c=b=⟨ai⟩=⟨ao⟩=0`, mas

\[
c'_+(0)=-i\varepsilon g/4,\quad c'_-(0)=+i\varepsilon g/4,
\qquad b'_+(0)=+i\varepsilon g/4,\quad b'_-(0)=-i\varepsilon g/4.
\]

Isso localiza o dado ausente: **a correlação conjunta óptica–OH**, não apenas a escolha da marginal OH. Nem a marginal óptica inteira determina sozinha a derivada, se essas correlações iniciais não forem especificadas. O testemunho tem par inicialmente zero, portanto não serve como teste de fase inicial não nula. Não é resultado de preparação experimental, contraexemplo ao dispositivo completo ou impedimento a outra redução justificada.

## 6. O que esta camada entrega e o que β ainda exige

- **[DERIVED — candidato]** Leitura explícita das equações de dois correladores e do ponto em que o fecho reduzido falha no corte existente. O resultado numérico/simbólico original fica imutável e pinado, com cópia de bytes.
- **[OPEN]** Identificação entre receptor físico, operador de saída e fase lida, com referências dos osciladores locais e preparação conjunta. Nenhuma tomografia, heteródino ou medição OH foi executada aqui.
- **[OPEN]** Justificação da passagem do corte de dois níveis ao domínio bosônico ou escolha explícita de um dispositivo efetivamente finito. O termo λ/2 não é evidência dessa passagem.
- **[OPEN]** Fechar o conjunto de correlações ou provar uma redução/dilatação que preserve o sinal e os termos de bombeamento/acoplamento/perdas. O ganho `tanh(P/Pth)` da patente e a igualdade a `G_OH` não foram derivados.
- **[OPEN]** β entra na modelagem anterior pela taxa `λ=β γΛ`, com `β=ALPHA_FINE_CODATA_2018·√e` calculada em runtime. A exploração R59 tratou λ como símbolo positivo independente; **não calculou nem mediu β**. Não se deve reinterpretar `q`, `c0`, `ωc`, `ωOH` ou a fase do par como β. Seriam necessários o mapa de unidades e parâmetros da mesma realização, uma escala γΛ determinada independentemente e um contrato que separe perdas convencionais, correlações auxiliares e a contribuição holográfica. Sem esses dados, nem λ nem seu eventual produto com uma escala externa fornecem β de forma identificável.
- **[OPEN]** R4 integral permanece aberto: não há nesta entrega a ponte física completa `V0/Eref/κ`, relógio global, família contínua, H3 ou conclusão sobre o dado. Nenhum kernel, um.py, memória canônica, Bancada ou gate foi alterado.

Os pinos medidos, as cópias byte a byte, os intervalos das fontes e a lista de artefatos estão em `CUSTODY_R61.json` e `DELIVERY_R61.json`. Estes documentos são novos; a exploração, seu script e as fontes permanecem intactos.
