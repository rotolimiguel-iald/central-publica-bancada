# Revisão adversarial independente — C3, R-MOD e R-PROP

[REAL — revisão documental e contas escalares independentes] 22/09/2026. Raiz B = `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`; caminhos abaixo relativos a B, salvo indicação. Fontes e produção somente lidas. O revisor não construiu o adendo nem executou seu gerador.

**Parecer: adequado como candidato documental a M3, com uma ressalva editorial na linha 25; não constitui fechamento da ponte física.** Os seis passos de R-MOD explicitam as paredes. A fórmula Γ=πβν²/κ está corretamente condicionada ao duplo comutador postulado. R-PROP enfrenta a passagem efetiva da LEITURA_03 e distingue consistência dimensional de extrapolação física não justificada. Este parecer não aprova integralmente F3 nem substitui a decisão de M3.

## Cobertura dos seis passos

| Passo / fonte no adendo | Verificação e limite |
|---|---|
| 1 — `C3_ADENDO_RMOD_RPROP_013BIS.md:7` | A cunha de Minkowski/vácuo de BW não vira Kerr térmico global. Região corrotante restrita, ansatz de Gibbs e estado de Unruh têm perdas distintas, conforme `C1_ADENDO_CORRECOES_013BIS_v3.md:26–31`. A falta de acesso integral a Kay–Wald/Sewell é declarada; não é prova dos seus teoremas. **Coberto como parede, não como construção de estado.** |
| 2 — `:9` | Reobtida a conversão modular/segundos e o coeficiente π. O texto diz expressamente “Se, adicionalmente, o gerador em s for o duplo comutador”. Não deriva essa hipótese de L=√β√K, nem identifica automaticamente K unilateral com −logΔ bilateral. **Álgebra condicional correta.** |
| 3 — `:11` | Para κ>0, a soma é geométrica com razão exp(−2πν/κ), convergindo apenas para ν>0. ν=0 ou ν<0 não normaliza esse oscilador bosônico infinito. κ>0 está no regime subextremal do módulo: `tgl_ringdown_prediction.py:41–42,111–116`. Não estender ao extremo κ=0 nem promover um modo admissível a estado regional completo. **Domínio coberto sob essa condição.** |
| 4 — `:13` | A exclusão laboratorial é transportada como INPUT e com escopo testado; a regra física que distinguiria horizonte/laboratório continua OPEN. Não reexecutei v369 nem revalidei aqui sua primária. **Coberto documentalmente como parede; número experimental não certificado nesta revisão.** |
| 5 — `:15` | Remete à tabela C1 de sete spins e ao parecer `bis/C1_CLOSING_REVIEW.md`, sem afirmar identidade entre R-MOD e R-RAIZ-0. Os valores tabelados próximos de χ=0,6785 são −0,0368350715 e −0,037164631: diferença absoluta 0,0003295595, cerca de 0,887% do segundo. Em χ=0, os valores −0,191788214 e −0,024645032 já impedem identidade. **Conferência aritmética da tabela; nenhum novo cálculo QNM.** |
| 6 — `:17` | Preserva “CONJECTURE — management hypothesis, not TGL canon” e separa fonte consultada, derivação e identificação física aberta. **Estatuto documental adequado.** |

O pedido original de seis passos consta em `..\TUNEL\PARA_CHATGPT\ORDEM_013_confrontacao_do_ringdown.md:185–193`; o adendo os enfrenta sem transformar uma parede em sucesso físico. “PAGO” só é sustentável nos sentidos documentais/condicionais delimitados na própria frase.

## Conta independente: duplo comutador versus salto raiz

[DERIVED] Defina a=2πν/κ, c=log Z e K|n⟩=(an+c)|n⟩. Então `[K,[K,ρ]]_nm=a²(n−m)²ρ_nm`. Sob o gerador postulado e ds/dt=κ/(2π), Γ_nm=πβν²(n−m)²/κ; a expressão citada é a coerência adjacente, |n−m|=1. O termo c cancela. Com κ e ν em s⁻¹ e β adimensional, Γ tem dimensão s⁻¹.

[DERIVED] Para L=√β√K, quando K≥0, a taxa seria `(κ/2π)(β/2)(√(an+c)−√(am+c))²`. O fundo c não cancela em geral. Portanto não é a mesma lei. A passagem de um oscilador ilimitado a uma dinâmica completa também requer domínio apropriado dos operadores; a conta de elementos de matriz não certifica essa construção.

[REAL — controle escalar leve, sem importar código da casa] Com κ=2 s⁻¹, ν=3 s⁻¹, Z=1/(1−exp(−2πν/κ)) e β calculado em runtime como `7.2973525693e−3 × sqrt(e)`, reobtive:

| Expressão | Resultado s⁻¹ |
|---|---:|
| (κ/2π)(β/2)(2πν/κ)² | 0,17008850228532787 |
| πβν²/κ | 0,17008850228532785 |
| Salto raiz, níveis 0↔1 | 0,017941640107555005 |
| Salto raiz, níveis 1↔2 | 0,0030963484563355324 |

Esses parâmetros são um exemplo algébrico escolhido pelo revisor, não uma medição de buraco negro. A implementação R-MOD, `tgl_ringdown_prediction.py:108–119`, exige QNM fornecido, calcula ν e κ, recusa ν≤0 e retorna β(2π/κ)ν²/2 com estatuto conjectural. Conferido por leitura, sem executar a função.

## R-PROP e ressalva documental

A passagem criticada está efetivamente em `..\TUNEL\PARA_CHATGPT\ORDEM_013_INSUMOS\LEITURA_03_NUMEROS.md:148`: “τ★ = GM_f/c³ é propriedade do remanescente na FONTE”. O uso de D_L/c como tempo aproximado também é declarado nessa fonte em `:142`. O adendo, `:21–25`, reconhece a ausência de mecanismo que transporte o relógio local da fonte pelo caminho. Um expoente grande calculado após tal extensão não refuta, por si, o ramo B local.

[DERIVED] `[GM/c³]=T`, `[βτ★ω²/2]=T⁻¹` e `[ΓD/c]=1`. Não há inconsistência dimensional nessa expressão. Sua validade física continua exigindo uma nova hipótese. A crítica física da LEITURA_03 não é eliminada por essa checagem de unidades.

[DERIVED condicional] Inserindo ω(z)=ω_obs(1+z) e |dt|=dz/[(1+z)H(z)] em ∫Γdt resulta exatamente no integrando `(1+z)/H(z)` do adendo e de `tgl_ringdown_prediction.py:142–156`. Tirar τ★ da integral exige que ele seja constante **ao longo do percurso no relógio local adotado**; ser constante somente na fonte não basta. Se variar, τ★(z) fica dentro da integral. A hipótese de ruído, a referência e a função de transferência continuam abertas. Atenuação constante com amplitude livre é degenerada com essa amplitude; não vira automaticamente taxa temporal extra do ringdown.

**Ressalva editorial localizada, sem bloqueio da álgebra:** `C3_ADENDO_RMOD_RPROP_013BIS.md:25` diz “a cosmologia indicada no módulo”. A função recebe `hubble_per_s` do chamador; não seleciona H₀, Ω ou uma cosmologia. A leitura sustentada é “H(z) fornecido como entrada, a declarar em cada cálculo”, com τ★ constante em todo o percurso. Recomenda-se essa precisão em eventual versão posterior. Nenhum cálculo de Ξ ou observável calibrado foi demonstrado por esta revisão; não se deve citar a frase como evidência de cosmologia já fixada.

## Alcance da inspeção e integridade

Lidos como texto: adendo, recibo, trechos pertinentes do gerador, módulos prediction/template, adendo C1 v3, README C3, LEITURA_03 e pareceres auxiliares. `tgl_ringdown_template.py:58–73` sustenta a convenção de fase relativa a t_start e o caso face-on, absorvida a fase constante. Compatibilidade de arrays não certifica likelihood. O JSON de timing foi conferido por hash; não reextraí strain nem repeti cortes. C2 v2 é evidência condicional existente, não previsão universal.

**Primárias não relidas nesta revisão C3:** integrais BW, Kay–Wald, Sewell e execução/fonte experimental v369. A informação sobre consulta/acesso vem do adendo C1 e seus registros, explicitamente documental. Não houve nova busca web: este parecer verifica o alcance do candidato e mantém essas lacunas abertas; não apresenta novo teorema importado como verificado. Sem Lean, PE, rerun de ensemble, importação de um.py ou execução de código do construtor.

[REAL] SHA256 calculados dos bytes em disco; os nove itens `sources` do recibo coincidiram **9/9**, assim como gerador, LEITURA_03 e abertura. Hash confere identidade, não prova conteúdo físico.

| Arquivo | SHA256 calculado |
|---|---|
| C3_ADENDO_RMOD_RPROP_013BIS.md | `39b8adae645e9a7b9454a0b6e9d1fa27d31569818ac0706b08cc6e65c204e6cf` |
| bis/C3_PHYSICAL_WALLS_SOURCES.json | `76ba27b88d60a4c5ec93d1328044fac7c1f18f4942b0f8fc139affebebc8f3a9` |
| refeito/record_c3_physical_walls_013bis.py | `87c6f57d4c6f3e014fc9e92444f8616f44a64fd046788f2b3215c9e172b2f8db` |
| tgl_ringdown_template.py | `16d7fbc25e94b0351e7050aa5055db421365953782cec1a668d68f11e5cc5132` |
| tgl_ringdown_prediction.py | `fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652` |
| C2_MAPEAMENTO_ANALITICO.md | `3b1b04893605f6a01a39e18567903d0a24d678a9fc0276e01b7d99efc9df503e` |
| C1_ADENDO_CORRECOES_013BIS_v3.md | `a688b542e5d4d1c6be356d2196f6bf9661609bc9b0c50c7ea3b0152fe3e2feed` |
| C3_README_013BIS.md | `11e87185c4ceccfb8582534354da310d3ee0d136023a9272e683b756f9278f89` |
| bis/C3_C6_TIMING_013BIS.json | `56906841f92020988defa1dd774b02add88c34e6d18e9617375aab0323abcc1b` |
| C2_ADENDO_OBSERVAVEL_v2.md | `6eb9df8379ebd6ae3cd7e0c2e0ffbd70dfe78ccb5ce3b68418c8ac51c29bb6b1` |
| bis/C1_CLOSING_REVIEW.md | `b4eef1b4fa9df165f3fa2a3a679a04b1249522d99c63d79eb7af62d3be115312` |
| bis/C2_ADVERSARIAL_REVIEW.md | `8027cc47902150dae5d31fc2f4ca361a8a4874299138740685eca9594415411b` |
| ..\TUNEL\PARA_CHATGPT\ORDEM_013_INSUMOS\LEITURA_03_NUMEROS.md | `4cd1e7124cfa803ae383f6ef4c348b9721c013104404c334e0f92d5a086e5bcd` |
| ..\TUNEL\DO_CHATGPT\ENTREGA_013BIS_ABERTURA_operador.md | `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0` |

**Único arquivo escrito nesta revisão C3:** `bis/C3_PHYSICAL_WALLS_REVIEW.md`. Os arquivos escritos nas revisões anteriores RD e GWTC4 estão integralmente enumerados nos respectivos pareceres. Nenhuma comunicação externa, entrega de produção, alteração de memória/canônico ou movimento de gate.
