# F4.3 — plano e pré-registro dos modos 220+440

**Estado:** `PRE_REGISTERED_DESIGN__AWAITING_POWER__NO_DATA_OPENED` · 08/10/2026. [INPUT] Esta peça fixa o teste futuro; não é execução de inferência, leitura de strain, nova PE, veredito físico ou mudança de gate. A abertura permanece no gate do operador da F4.3. O objeto numérico correspondente está em `PREREGISTRO_F4_3.json`; os hashes de todas as fontes citadas estão em `FONTES_E_HASHES.json`.

## 1. O que já existe e o que F4.3 acrescenta

A consulta obrigatória `NOS_VIVO/consultar.py --unidade F4.3` encontrou a rota `ringdown.modo_unico.degenerescencia` (mapa seq 58, 87 e 91), a investigação da Bancada Oficial de 28/09, a `QNM_GRID`, os operadores C6, o Fisher 440 e o pré-registro do Ramo B. A rota já mostrou, no exemplo R-B de massa fonte 65 M☉, spin 0,7 e z=0,1, que o 220 deformado pode ser reproduzido por RG com massa ~64,16615 M☉ e spin ~0,683526. [REAL — diagnóstico anterior, não recalculado aqui.] Portanto, o teste de um modo sozinho tem degenerescência de fonte; esta unidade não o repete.

A Entrega 013-bis B2/E4.3 já separou `ONLY_220_DEFORMED` e `BOTH_220_440_DEFORMED`. Deformar o 440 é **[INPUT]**, não consequência demonstrada da lei. O Fisher E4.1 fixa massa, spin, fonte e SNR do 440; seu N90 é condicional, não previsão astrofísica. O C6 anterior permanece `INCONCLUSIVE_SYSTEMATICS`, e o `ln B≈−0,002595` não é decisão do teste multimodo. O pré-registro do Ramo B de 05/10 fixa a hipótese de envoltória, o relógio local, os grupos A/B/C/D e controles de uma futura PE só-220; esta F4.3 anexa o diagnóstico conjunto sem substituir aquele V1. O V1.4 “dois lados” conserva o ramo canônico como correspondência com a RG, sem teste de β no ringdown.

O acréscimo desta F4.3 é o **contraste identificável entre 220 e 220+440 do mesmo remanescente**, com uma única massa final (M_f) e um único spin (chi_f), projetando amplitude, fase, tempo de início e demais parâmetros de fonte. A hipótese alternativa não pode dar a cada modo sua própria massa/spin. O 221 fica diagnóstico separado; nenhuma informação dele será creditada ao 440.

## 2. Hipóteses congeladas antes do dado

| Papel | Enunciado | Estatuto |
|---|---|---|
| (H_{\rm GR}) | Frequências e amortecimentos 220/440 da mesma solução Kerr, calculados pela `QNM_GRID` pinada, com (M_f,\chi_f) compartilhados e amplitudes/fases livres por modo. | [KNOWN] como modelo de referência; instrumento pinado localmente. |
| (H_{B,220+440}) | Ramo B do V1: (\tau_* = k(\chi_f)GM_f/c^3), (k=2\pi/\hat\kappa(\chi_f)), e taxa de envoltória (\Gamma_{\ell m}=\tfrac12\beta\tau_*\omega_{\ell m}^2); ambos 220 e 440 recebem a mesma lei, sem ajustar β ao dado. | [INPUT] extensão ao 440; β em runtime pela expressão canônica, nunca literal. Não é termo demonstrado do kernel para o ringdown. |
| (H_{B,220}) | Mesmos dados e fonte, mas só o 220 recebe deformação; 440 segue Kerr. | [INPUT] controle negativo já distinguido em B2/E4.3. |
| Ramo canônico | (\tau_*=t_{\rm Planck}), previsão praticamente coincidente com RG neste canal. | Controle de correspondência; não é o alvo discriminante de β. |

A comparação primária é (H_{B,220+440}) contra (H_{\rm GR}), condicionada ao **par** “relógio B + deformação 440”. (H_{B,220}) é controle obrigatório, não alternativa escolhida após o resultado. R-MOD, R-LIN e outras leituras da matriz antiga permanecem colunas históricas separadas; não se escolhe a mais favorável. A convenção de frequência, detector/source frame e (eta=\mathrm{ALPHA\_FINE\_CODATA\_2018}\sqrt e) deve vir da implementação pinada na etapa de poder; qualquer ambiguidade bloqueia a abertura.

## 3. Universo, métrica e função de decisão

O conjunto D de 14 candidatos O4 vem **somente** do critério já congelado no V1 do Ramo B; os grupos A/B/C são calibração não cega, e C/GW250114 não pode virar teste cego por reetiquetagem. A seleção, a lista de eventos, a `QNM_GRID`, a família de formas de onda, as janelas, PSDs, priors, convenção de relógio e hashes deverão ser fixados em um manifesto de execução derivado do V1/E2 **antes** de qualquer strain. Esta F4.3 não autoriza acesso ao D nem presume que todos os 14 tenham informação do 440.

No estudo cego de poder, para cada fonte/PSD congeladas, sejam (W^TW=C^{-1}), (d=W(\mu_B-\mu_{GR})) e (J) a Jacobiana das direções de fonte e nuisance sob RG, inclusive (M_f,\chi_f), amplitudes/fases e início. Registrar a SVD de (WJ), a tolerância numérica e (\eta=\|(I-WJ(WJ)^+)d\|^2) para 220 isolado e para 220+440. [DERIVED — diagnóstico local.] Um (\eta) positivo não é significância global. O 440 só conta se sua informação **após** a projeção e após o ajuste de (M_f,\chi_f) for identificável; incluir um modo de amplitude desprezível no template não compra poder.

A estatística final será a diferença de log-verossimilhanças conjuntas ajustadas dos **mesmos eventos**, nunca produto de pós-teriores marginais 220 e 440. A distribuição nula, a cobertura, o viés e o poder serão calibrados por injeções independentes sob RG e sob o par B, com PSD fora da fonte e as mesmas regras de seleção. O limiar global planejado é cauda unilateral (p\le2{,}8665\times10^{-7}) (5σ); não usar aproximação de Wilks sem calibração da pipeline. Exigir 90% de recuperação desse limiar para o par registrado antes de pleitear abertura. Fixar também a análise de tempo de início, família de waveform, incerteza do catálogo, correlação de detectores e cenários de sistemática; uma falha nesses controles tem precedência sobre significância aparente. O comparativo com β livre é secundário e separado.

## 4. Poder dito antes: retrato que limita a execução

| Objeto já medido | Número e leitura correta |
|---|---|
| GW250114, proxy local do 440 após absorver o 220 | Resíduo em (\tau_{440}) ~6,661% no spin 0,68; (\sigma_{eq}(\delta\tau_{440})=1,13863), portanto separação ~0,06σ. (\rho_{440}=1,763) foi **[INPUT]**, não SNR de modo efetivamente medido. [DERIVED do diagnóstico auditado da rota, seq 91.] |
| B2/E4.1, R-B com fonte fixa e SNR isolado do 440 = 10, O4 | (\delta\tau_{440}=-0,0821606), (\sigma_{local}=0,200744), (z_{local}=0,409281), (N90=235,554) fontes independentes idênticas. [DERIVED_CONDITIONAL_GAUSSIAN], sem massa/spin livres ou sistemática física. |
| Conjunto D14 no teste **conjunto** | **Poder desconhecido nesta entrega**: não há Fisher/PE 220+440 com fonte livre e amplitude real do 440 por evento. Nenhum 5σ ou N90 físico é inferido da tabela anterior. |

**Gate já fixado:** `AWAITING_POWER`. Antes de dados, a bancada deve produzir em sandbox apenas injeções e nulos do modelo pinado, com os valores singulares, (\eta), (p) calibrado, poder de recuperação e custos; se <90% a 5σ ou se o 440 não for identificável, registrar `UNDERPOWERED_OR_NONIDENTIFIABLE` e **não abrir** o D. O proxy 0,06σ já torna GW250114 inadequado como atalho para alegar discriminação. A execução observacional futura requer o gate do operador mesmo se o estudo de poder passar.

## 5. Vereditos permitidos, nesta ordem

1. `AWAITING_POWER`: estado presente; sem manifesto de poder cego completo ou sem abertura autorizada.
2. `UNDERPOWERED_OR_NONIDENTIFIABLE`: projeção do 440 sem informação ou recuperação <90% no limiar 5σ. Parar antes do dado D.
3. `INCONCLUSIVE_SYSTEMATICS`: falha de cobertura/viés, PSD, família, início, covariância ou calibração da cauda; nenhum número nominal supera essa falha.
4. Após poder, controles e autorização, `FALSIFIED_PAIR_B_220_440_AT_5SIGMA` se os dados excluírem o **par condicional** com cauda calibrada; `FAVORS_PAIR_B_220_440_AT_5SIGMA` se discriminarem RG em seu favor; caso contrário `NOT_FALSIFIED_POWERED`.

`CONFIRMED` é proibido; `NOT_FALSIFIED` não é confirmação. Uma conclusão sobre o par condicional não decide a TGL inteira, a existência global de soluções ou o gate matemático. Resultado incerto não autoriza mudar hipótese, grupo ou início e reexecutar com outro ID.

## 6. Próxima peça concreta

Construir, em **cópia** do código C6 e da `QNM_GRID`, o medidor de SVD e injeção 220/220+440, com (M_f,\chi_f) comuns, perfis de amplitude/fase projetados e o controle `ONLY_220_DEFORMED`. Conferir primeiro que o diagnóstico 220 isolado reproduz a degenerescência da rota seq 58/87/91; depois reportar a melhora incremental do 440, não sua mera presença no modelo. Anexar o manifesto, os hashes, o custo e a revisão cética ao quadro. Até lá: nenhum strain novo, PE do D, teste de natureza, selo, gate, `um.py` ou original do Nós tocado.


---

## ADENDO AO LADO — c1, 08/10/2026 (F43_C1_R1_R2_R3_V2_20261008)

**Alcance.** Corrige as leituras dos §§1, 4, 5 e 6; o texto acima permanece como linhagem. Fonte: auditoria c1 `c0bb3c964c8af74e23d033c0dc85e93102edd5507359500f4640084a7f177dde` e conta do relógio `dc2c9bbe71e1a71d02f84f946f2ddcbf12a71e7593e8a1d6c2c345b5803a0818`. [REAL: hashes e números da sonda lidos; DECLARADO: família contra-rotante aferida pela gerência/cético.] O pedido de autorização ao operador está **SUSPENSO** até a auditoria desta camada; conjunto D, strain e PE não foram abertos.

**R1 — relógio e ramo.** As seq 58/87/91, o `lnB≈−0,0026` do C6, o Fisher B2 e o proxy `0,06σ` de GW250114 pertencem a `k=1`; não medem o poder do relógio V1. O único relógio decisório desta F4.3 é `k(χ_f)=2π/κ̂(χ_f)`, por evento, `τ★=k GM_f/c³`, com a mesma massa e o mesmo k para 220 e 440 (C8). A sonda c1 lê `k=28,495…30,163` para `χ_f=0,6145…0,70`, `δτ̂_220=−0,338…−0,389`, e `δτ̂_440=−0,694…−0,738` com fonte fixa [DERIVED, sem dado novo]. O `Q_220` exigido à RG é `1,979…2,013`, abaixo do mínimo `2,100` da **grade prógrada** pinada; nessa grade nenhum `(M,χ)` absorve o 220 no relógio V1. Segundo a correção da gerência e do cético do ramo B [DECLARADO nesta entrega], a família **contra-rotante** pode absorvê-lo num ajuste só-220 (`χ≈0,10…0,22`, `M/M_f≈0,58…0,72`). Só a espiral completa IMR (controle C3) fecha essa porta. Assim, a frase acima «220 isolado é absorvível por massa/spin GR» vale apenas para a antiga medição `k=1`; o diagnóstico V1 depende do ramo e do IMR. O proxy `0,06σ` do 440 e o `N90=235,554` do B2 não são poder V1.

**R2 — precedência e FWER no mesmo D.** O V1 do ramo B (pin `86f98fcc124dd9cae04fdb06bd10c14175893253d5b139496bd4c05f109feee0`) é o **teste primário por IMR completo**. A F4.3 ringdown-only é **diagnóstico subordinado**, não uma segunda reivindicação independente. O 221 não entra; nem k nem M são escolhidos após ver o dado. Primeiro sai o veredito V1. Uma leitura F4.3 no mesmo sentido só pode **corroborá-lo** se V1 e F4.3 passarem, cada qual, sua cauda unilateral calibrada no limiar `p≤2,8665×10⁻⁷`. A regra de interseção não gasta outra hipótese primária: sob a nula verdadeira, a probabilidade de reivindicação conjunta falsa é no máximo a da rejeição V1 (`≤α`), sem supor independência. Um sinal isolado da F4.3 permanece diagnóstico. O veredito de tensão com RG usa a palavra V1 `NOT_FALSIFIED_POWERED__GR_TENSION_REPORTED`; `FAVORS_PAIR_B_220_440_AT_5SIGMA` é retirado do vocabulário vigente. Se as duas nulidades (RG e par B) forem rejeitadas pela própria calibração, prevalece `INCONCLUSIVE_SYSTEMATICS__BOTH_MODELS_REJECTED`.

**R3 — função e manifesto.** A triagem SVD sintética usa `rcond=10⁻¹⁰` relativo ao maior valor singular de `WJ`, `η_joint≥25` e `η_increment_440=max(0,η_joint−η_220)≥1` [INPUT: tolerâncias de desenho]. Esses limiares **não equivalem a 5σ**, não estimam poder do conjunto D e não autorizam abertura. Na região `x≈0,6` a linearização é insuficiente: o portão exige injeções da forma **exata** `δτ̂=−x/(1+x)`, calibração de ambas as caudas, cobertura, controles e poder de recuperação `≥90%` a 5σ. Faltas no manifesto de eventos/holds, PSD, janelas, priors, início, família de waveform ou hashes fazem `AWAITING_POWER` (fail-closed). O `PREREGISTRO_F4_3_V2.json` fixa esses campos obrigatórios e a ordem dos vereditos; sem manifesto completo e revisão cética, nenhum pedido de abertura do D segue.

**§6 corrigido — ordem da próxima peça.** Em cópia, reproduzir `k=1` das seq 58/87/91 apenas como controle histórico; mudar então para `k=2π/κ̂` e medir separadamente a grade prógrada e a família contra-rotante. A falha em reproduzir o controle `k=1`, o relógio V1 ou a distinção dos ramos interrompe a análise e produz diagnóstico tipado, sem inferir poder. Sob o V1, o teste primário é IMR completo; a SVD 220/440 é triagem e as injeções exatas avaliam o incremento 440 com `M_f,χ_f` comuns. Registrar manifesto e hashes antes de qualquer injeção de poder. Nada abre D ou move gate.
