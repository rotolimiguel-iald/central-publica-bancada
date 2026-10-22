# R79 — ponte óptica, resposta no limite e contorno da face OH

Em nome de codex-gerente-tgl, 18/10/2026, F1.FECHO_20261015, claim967/escopo983. Reuso das peças R57, R64, R66, R71–R78 e das fontes autorais/patentes. A consulta ao Nós Vivo não encontra esta unidade; a falha está custodiada. A rota local e os artefatos primários foram lidos, sem reconstruir o grafo ou repetir o que já estava entregue.

## 1. O que efetivamente se fechou nesta etapa

**[DERIVED, analítico, não Lean]** Três componentes, sob hipóteses nomeadas:

1. **Entrada coerente → controles do teste → campo de saída.** Aplicar a construção de reservatório R66 ao porto óptico1 produz h_in=i√κ_i(α* a_i−α a_i†). Nas convenções R78, u=x+iy=−i√2 α/g_in e α_out=z/g_out. A resposta é δα_out=H_+α+H_-conj(α), com H_+=−i√2 h_+/(g_in g_out), H_-=+i√2 h_-/(g_in g_out). A bomba OH e o salto conjunto são mantidos. H_COHERENT_PORT1 especifica a mesma realização, portos distintos e nenhuma mistura direta1→2. A convenção antes aberta na R78 fica resolvida nesse modelo.
2. **Primeira variação no limite bosônico.** Uma estimativa nova controla a inserção ilimitada da sonda, que pode elevar o suporte em1. A série ponderada constrói a evolução perturbada e sua derivada para estados iniciais de suporte finito, e dá convergência uniforme em todo intervalo finito para a leitura não limitada. Esta prova não exige supor a conclusão como hipótese; reutiliza o semigrupo conservativo R66 e trata a nova inserção. Não é um teorema Lean novo nem o fecho global da rede.
3. **Face material → reflexão/transmissão.** O contrato dipolar/RWA explicita g_JC, bombeamento, preenchimento, modo brilhante e resíduo escuro. No regime adicional de sonda fraca e folha elétrica fina, a susceptibilidade OH determina a resposta de contorno. São relações condicionais verificáveis; a identificação dos parâmetros do aparelho não é presumida.

O erro de truncamento da resposta já tem uma demonstração própria. Não permanece aberto pela justificativa histórica da R78. O erro numérico de máquina, a calibração e as hipóteses materiais conservam seus alcances distintos.

## 2. Refinamento pré-registrado, uma execução

**[REAL — numérico sintético]** Mantidos todos os parâmetros, preparos, tempos, epsilons e controles R78; somente o corte aumentou pelo critério analítico anterior à nova trajetória. Corte mínimo m=8, dimensão81, para majorante de truncamento de cada H_± menor que1e−10. O corte7 não satisfazia esse critério. PLAN_R79, CUT_SELECTION_R79 e PREEXEC_REVIEW_R79 foram fixados antes do FREEZE/START.

93/93 verificações aprovadas, exit0. A tabela mostra máximos nos quatro tempos fixados. A sensibilidade de quadratura é adimensional; H_± são derivadas de amplitudes coerentes na realização nomeada. Não são taxas de transmissão de energia, frequências medidas ou significância estatística.

| Caso | Máxima sensibilidade de quadratura | Máximo módulo H_+ | Máximo módulo H_- |
|---|---:|---:|---:|
| seeded_full | 3.266329191e-07 | 4.116254879e-07 | 2.660362085e-08 |
| unseeded_full | 2.54284982e-09 | 1.672755858e-09 | 8.221040303e-10 |
| seeded_blocked | 0 | 0 | 0 |

A resposta do caso sem semente permaneceu próxima à R78; não foi criada uma nova preparação para obter sinal. “Sem semente” significa sem componente coerente inicial na saída, com coerência/preparo na entrada/OH e bombeamento mantidos. Não é vácuo global nem produção de energia do nada. O controle gJC=lambda=0 retorna zero numérico nesta execução. Ele testa conjuntamente essas ligações, não atribui o efeito a uma delas isoladamente.

O majorante analítico de truncamento de cada H_±, avaliado em alta precisão no planejamento, é aproximadamente5,2998e−11. A fórmula é demonstrada; a avaliação Decimal e o solver não usam aritmética intervalar. A concordância Duhamel/diferenças centrais permanece um diagnóstico numérico separado: não se soma como se fosse cota rigorosa de arredondamento. Os valores não devem ser transformados em um nível de confiança experimental.

O termo H_- tem módulo maior que a cota de truncamento tanto no ramo semeado quanto no ramo sem semente. No cálculo, portanto, o desvio da multiplicação complexa por um único escalar persiste ao refinar o corte. Esta observação se refere à resposta marginal transitória do preparo e instrumento especificados. Não identifica um canal conjugado do aparelho real nem refuta, por si, a fórmula g_OH S_beta, que exige correspondência de objeto, regime e dois portos. Não há verificação intervalar do erro total.

## 3. A ponte material e a pergunta agora objetiva

Sob H_DIPOLE_RWA, o produto H_int=−d·E entrega, por expansão:

    g_s=−d_eg,s·E1(r_s)/hbar,
    Ω_s=−d_eg,s·E_p(r_s)/(2hbar).

A segunda fórmula usa fasor definido por E(t)=Re[E_p e^(−iωt)] e o Hamiltoniano Ωσ_x da patente; o fator2 não é descartado. Para um ensemble no setor zero/uma excitação, G²=Σ|g_s|², Ω_B=Σg_s*Ω_s/G e ||Ω_dark||²=Σ|Ω_s|²−|Ω_B|². Isso fornece um critério real para a redução a um único σ: a parte escura e sua mistura pelas outras dinâmicas precisam ser desprezíveis ou controladas. “Muitos OH” não equivalem automaticamente a um qubit.

A fonte já declara dipolo1,7Debye e alinhamento por RF; o primeiro não foi promovido ao elemento de transição d_eg de qualquer par de níveis. Pressão de H2O não foi promovida a densidade OH ativa. Portas780nm e frequência OH não foram identificadas entre si por nome. A relação κ=ω/Q foi recuperada, distinguindo perda total, saída monitorada e decaimento de amplitude.

No regime H_LINEAR_OH_SHEET, para uma polarização escalar, folha fina e mesma admitância realY>0 nos dois lados:

    σ_s(ω)=−iωε0χ_sheet(ω),
    r=−σ_s/(2Y+σ_s),  t=2Y/(2Y+σ_s),
    A=1−|r|²−|t|²=4Y Reσ_s/|2Y+σ_s|².

Essas relações DERIVAM o espelhamento a partir da resposta de superfície no submodelo nomeado; não põem β como entrada para forçar o resultado. A comparação exigida é |σ_s|²=β|2Y+σ_s|², além das fases/portos para comparar operadores. No ramo sem perda, σ_s=i b, isso equivale a b²=4Y²β/(1−β). Nenhum b foi escolhido/ajustado para satisfazê-la. Beta numérico só é calculado em runtime. A matriz de duas portas e o domínio sem polos estão em SHEET_SCATTERING_R79.

## 4. O que continua realmente aberto

**R4 — identificação do mesmo aparelho:** admitir/perfilar d_eg, E1, campo de bomba, nOH ativo, orientação e espessura; controlar o regime de duas transições/RWA/folha e a parcela escura; determinar taxas e a conversão para tempo físico. A frequência OH sozinha não determina essas grandezas. As relações de identificação já estão escritas: não é necessário pedir novamente uma definição conceitual de reconhecimento ou espelhamento.

**Banho comum:** o salto J=F1+F2 exige a matriz de correlação dissipativa λ[[1,1],[1,1]], de posto1 com termos cruzados. Dois banhos independentes não a realizam. R66 já dá uma construção de reservatório que produz J; resta identificá-la materialmente, incluindo frequências/regime e os demais termos, sem inserir a textura desejada como suposta conclusão derivada do dipolo. Calibrar g/Ω não mede por si γΛ.

**R5/global:** a ligação integral da rede causal e seu relógio ao dispositivo continua separada. A presente prova cobre duas famílias de modos bosônicos e OH no domínio nomeado. R3 e R10 precisam de revalidação final da missão. Nenhuma dessas pendências é apagada por este componente.

Próximo passo útil: consumir os perfis e dados de projeto já existentes para verificar as condições materiais acima, particularmente a projeção brilhante/escura e a matriz de correlações do banho. Não repetir a campanhaR78 ou o refinamentoR79, não voltar a construir a ponte de drive e não reinterpretar ausência de calibração como ausência de toda a rede.

## 5. Custódia e escopo

Notas: OPTICAL_DRIVE_BRIDGE_R79, CUT_RESPONSE_BOUND_R79, MATERIAL_IDENTIFICATION_R79, MATERIAL_DOMAINS_R79 e SHEET_SCATTERING_R79; seus manifestos pinam fontes/excertos e cobertura. Comparação dos resultados existentes: COMPARISON_R79.json, pós-processamento sem nova trajetória. A revisão independente pré-execução e a revisão final são artefatos separados.

Execução: 2026-10-19T01:01:58.778351+00:00 → 2026-10-19T01:01:59.958342+00:00; 1.179460700s. RESULT_R79.json SHA256 `97f191adbba8ed04d279a69bb65e2749b423c93d7b7521d96c25d8db7cb2df40`.

Nenhuma chamada a provedor, dado observado, novo build Lean, alteração de um.py, kernel do Nós, Bancada ou gate. PASS neste escopo não é confirmação física nem5sigma. Memória atualizada apenas com reivindicação, backups de bytes e revisão.

