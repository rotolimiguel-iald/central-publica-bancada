# R56 — continuidade concreta da leitura ao relógio do dispositivo

Autor: codex-gerente-tgl, 17/10/2026. Complemento candidato por reaproveitamento.

## 1. O elo já disponível

`SelectionAngleReconstruction` lê `z=exp(i theta)` por uma face e reconstrói
`S(theta)=z P+ + z^(-1) P-`. Na família de fase unitária, `z^(-1)=conj(z)`.
O teorema `miguel_boundary_reconstructed_from_its_selected_face` já especializa
essa reconstrução ao ângulo de Miguel. Isto não precisa ser refeito.

## 2. A composição temporal explicitamente escolhida

Na candidata Lean R56, `readerForm beta Omega t = S(thetaMiguel beta + Omega*t)`.
É uma família parametrizada, não um Hamiltoniano extraído do aparelho.
O leitor retorna `exp(i theta_M) exp(i Omega*t)` e o decodificador reconstrói a
mesma matriz em todo instante. O ângulo inicial fornece a referência de fase;
o parâmetro Omega fornece a taxa. Toda Omega tem a mesma forma inicial.
A fase escalar desta leitura tem taxa Omega; a coerência entre os dois setores,
no canal da R9, tem taxa 2*Omega. Essa diferença de objeto é preservada.

## 3. A fonte do dispositivo que deve alimentar a ponte

Em `PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex:343–370`, o
Hamiltoniano inclui frequências da cavidade e OH, acoplamento Jaynes–Cummings
e bombeamento de Rabi. Não é o Hamiltoniano M2 da R9 por simples mudança de nome.
Nas linhas 506–516, o relógio aparece como

`G_OH(t) = a exp(i omega_OH*t)`, `a = tanh(P_MW/P_th)`.

[DERIVED, sob potência e limiar positivos, finitos e constantes] `0<a<1`.
Uma fase pode ser recuperada por `G_OH/|G_OH|`; se a amplitude for zero, tal leitura
é indefinida e deve recusar. Extrair a fase não autoriza apagar a amplitude da
descrição do dispositivo. Se ela variar, sua variação também precisa ser conservada.

[DERIVED — diagnóstico algébrico da composição proposta, não observado físico]
Se tentarmos representar uma forma atenuada por `A=a S(theta)`, então o leitor
linear existente retorna `z=a exp(i theta)`. Seu decodificador recíproco dá
`a exp(i theta) P+ + a^(-1) exp(-i theta) P-`, que difere de `a S(theta)`
quando `0<a<1`. Essa é uma incompatibilidade de domínio do decodificador antigo,
não prova de perda irrecuperável nem de falha da patente.

Uma extensão candidata para amplitude real é `D_a(z)=z P+ + conj(z) P-`:
nessa família restrita de amplitudes reais, ela reconstruiria `a S(theta)`.
Outra rota conserva separadamente amplitude e fase. Ambas exigem tipagem e
verificação; nenhuma foi instalada ou apresentada aqui como realização do aparelho.
O fator G_OH da fonte é escalar: a identificação física dele com o leitor matricial
permanece uma obrigação, não é assegurada por esta conta.

## 4. Próximo resíduo verificável

Identificar no gerador e no setor do dispositivo qual observável realiza a leitura
complexa, com sua amplitude, e provar o mapa para a representação matricial aceita.
Depois transportar a referência e a dinâmica aos refinamentos da rede. Os resultados
aceitos de Fock/Takesaki/Maxwell permanecem reutilizados. H3 universal, o limite da
realização do dispositivo e o rito integral/revisão final permanecem em seus requisitos.
Não se escolhe um aparelho exclusivo por conveniência: MQC/célula,
Supercondutor/dinâmica e Psi-NET/protocolo mantêm os papéis documentados na R55.

Estatuto: fonte relida; deduções algébricas candidatas delimitadas. Não há medida
experimental nova, calibração da frequência, montagem do dispositivo ou mudança de gate.
