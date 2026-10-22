# Fase 8 — pré-registro V1 em rascunho, preparação primordial ORDEM018

**Estado: AWAITING_OPERATOR_RATIFICATION.** [INPUT] Preparação R-B/R-M. Este derivado não substitui o V1 anterior, não ratifica escolhas e não abre um composto. Há decisão do operador necessária sobre mapa físico, instrumento, alvos, priors e regra de análise. As cópias em ORDEM_018_INSUMOS permanecem intactas.

[REAL] O mapa primordial.fase8_era_da_radiacao foi consultado antes do trabalho. Canal Neff, Nível2 e BBN descircularizado já têm linhagem na bancada; não foram executados outra vez. BENCH_REUTILIZADO.json confere quatro hashes dos congelados originais em leitura somente. O script novo calcular_sensibilidades.py executa álgebra de desenho, sem importar um.py, abrir strain/posteriors ou executar PE/BBN.

## 1. Objeto e alternativas explícitas

[DERIVED condicional] β é calculado em runtime como ALPHA_FINE_CODATA_2018 × √e. α vem do retrato auditado Fase8, cujo hash é reconferido. Não há ajuste de β às abundâncias.

No domínio simplificado do fundo, seja ρtot=ρr+ρm+ρΛ. A implementação final deve preservar as espécies e suas transições relativísticas.

| Mapa | Definição proposta | Alcance e decisão |
|---|---|---|
| A — radiação e matéria | H_A²/H_0²=1+β[(4/3)ρr+ρm]/ρtot | Leitura local registrada de ρ+p; ratificar para este teste. |
| B — somente matéria | H_B²/H_0²=1+βρm/ρtot | Contrafactual de controle. A antiga decisão de Ωm em R não autoriza retirar radiação do fundo; mudar a lei requer nova decisão. |
| C — speed-up BBN | S(T)=H_A(T)/H_0(T); no limite radiativo S=√(1+4β/3) | Representação de A no instrumento BBN; não terceira hipótese independente nem observação adicional. |

[DERIVED] No limite radiativo, δρr/ρr=0,01604173387 e S=1,00798895523. Em B, S_B−1≈β f_m(T)/2, que desaparece quando a fração de matéria tende a zero. Não fixamos número a 1 MeV sem a convenção de entropia, temperatura, redshift, composição e f_m(T).

Antes da aniquilação e±, no plasma ideal com Nν=3, ΔNν_equiv=(43/7)(4β/3)≈0,09854. Depois, com o benchmark N_SM=3,044 e F=(7/8)(4/11)^(4/3), ΔNeff=(4β/3)(1+F N_SM)/F=0,1194660753. **Nν e Neff são variáveis distintas.** Os valores de referência das publicações também diferem. Nenhum ΔN único representa exatamente uma fração constante de ρr durante toda a aniquilação. Correções QED, aquecimento/decoupling de neutrinos e matéria finita pertencem à implementação a validar. Em particular, elétrons com massa não desprezível durante a aniquilação têm w(T) diferente de 1/3; aplicar literalmente ρ+p requer decidir como essa contribuição entra em S(T). Não promover o limite S constante a identidade exata dessa transição.

[OPEN] A equivalência de fundo não demonstra equivalência de perturbações. Nomear o fechamento free-streaming TGL-S ou fluido TGL-L antes de transportar limites CMB. Não transferir a precisão de uma hipótese para outra.

## 2. Uma entrada de β por instrumento

Na bancada, Φ_total já inclui β[(4/3)ρr+ρm]: manter Neff basal nessa representação. Na representação CAMB por parâmetros efetivos, usar o mapa Neff/ωc_eff sem reaplicar Φ_total. β=0 deve recuperar a referência. Conferir H(T) nos limites em que as representações são equivalentes; esta preparação não mediu uma tolerância de implementação.

As tabelas PRIMAT/PArthENoPE mencionadas na crítica preexistente orientam o desenho, mas variar Nν não implementa automaticamente S constante. Aqui foram usadas tabelas publicadas, sem repetir interpolação da bancada. A presença das tabelas CAMB fica documentada pela crítica anterior; não foi novamente verificada nesta etapa.

## 3. Fontes e sensibilidades

As cinco fontes públicas foram arquivadas e pinadas em FONTES_PRIMARIAS.json. PARAMETROS_PRIMARIOS.json registra a transcrição; o cálculo reconfere os hashes.

[KNOWN] [Fields et al. 2020](https://arxiv.org/pdf/1912.01132v1), Eqs. 15–17 e Table II (PDF pp. 19–22), fornece derivadas logarítmicas. Para (Yp,D/H), a derivada em G_N é (0,357;0,952), em η (0,039;−1,597) e em τn (0,729;0,409); Yp fiducial teórico é 0,24696. [DERIVED] Com as demais entradas fixas e H²∝G_N, G_N/G_N0=S² implica dln(Yp,D/H)/dlnS=(0,714;1,904).

[KNOWN] [Pitrou et al. 2018](https://arxiv.org/html/1801.08023v2), Eq. 145/Table 6, fornece polinômios na variação fracionária de Nν. Coeficientes lineares para (Yp,D/H): (0,163552;0,40901); quadráticos: (−0,036124;−0,00599); cúbicos: (0,009938;0,00224). Em ωb e τn, as derivadas são (0,039039;−1,64550) e (0,731614;0,42220). A Table 7 apresenta, para seu modelo nuclear e ωb fixo, dispersões fracionárias 0,068% e 1,49%. Isso não é precisão universal atual nem erro de uma implementação TGL nova.

[DERIVED] O 0,57 do antigo módulo não é validado por essas fontes. Para speed-up uniforme, o coeficiente conferido é 1,904; eventual errata do original cabe à coordenação. Variações de Nν e G_N são experimentos diferentes. Os dois casos Pitrou em ΔN_equiv inicial/final são diagnósticos de espécies adicionais, sem demonstração de limites rigorosos para S(T).

As fórmulas ΔYp=Yp0[(1+4β/3)^0,357−1] e Δln(D/H)=0,952 ln(1+4β/3) integram um expoente local congelado. A precisão de truncamento da previsão TGL permanece [OPEN]. Uma rede BBN com S(T), taxas e priors fixados é necessária para converter esse proxy em previsão do teste.

## 4. Poder somente por incertezas

[KNOWN] σ(Yp)=0,0034 em [Aver et al. 2021](https://arxiv.org/abs/2010.04180v1) e 0,0013 no preprint [Aver et al. 2026, LBT Project IV](https://arxiv.org/abs/2601.22238v1), de 29/01/2026. A publicação nova é candidata explícita à ratificação, escolhida por atualização de precisão, não pelo centro observado. Não considerar as duas amostras réplicas independentes.

[KNOWN] [Cooke, Pettini e Steidel 2018](https://arxiv.org/abs/1710.11129v3) informa σ[log10(D/H)]=0,0052 na combinação de sete absorvedores. Usamos σln=ln(10)×0,0052, sem normalizar por um centro observado.

[DERIVED condicional] Resultados do proxy Fields:

| Quantidade de desenho | Valor |
|---|---:|
| ΔYp teórico | 0,001407084174 |
| Δln(D/H) teórico | 0,015150532556 |
| Δlog10(D/H) teórico | 0,006579792687 |
| ΔYp/σAver2021 | 0,41385 |
| ΔYp/σAver2026 | 1,08237 |
| Δlog10(D/H)/σCooke2018 | 1,26534 |
| σYp para separação 5, se só este erro | 0,000281416835 |
| σlog10(D/H) para separação 5, se só este erro | 0,001315958537 |

Esses quocientes são separações de desenho em unidades de σ, não probabilidade de rejeição, tensão com o centro, veredito ou poder marginalizado. Incertezas teóricas e priors podem reduzir a separação; nenhuma estatística conjunta foi calculada. As páginas lidas contêm centros observados: não se alega cegamento histórico. Os centros não entram nos parâmetros/cálculo. O pré-registro é do teste, sem ajuste de β ao dado e com novidade de uso documentada.

## 5. Identificabilidade, priors e erros

Para o vetor (lnYp,lnD/H), as colunas nuisance de Fields são X=[[0,039,0,729],[-1,597,0,409]], referentes a (lnη,lnτn). Seu determinante é 1,180164: posto 2. Com ambos os deslocamentos totalmente livres, Δperp=[I−X(XᵀC⁻¹X)⁻¹XᵀC⁻¹]Δ=0 para qualquer vetor Δ de dimensão 2. Isso não declara que os priors físicos sejam livres: demonstra por que precisam constar no teste.

Com priors Gaussianos de covariância P especificados independentemente, uma forma de desenho é Ceff=Cobs+Cnuclear+J P Jᵀ e Q=ΔᵀCeff⁻¹Δ. A forma equivalente de perfil penalizado usa C⁻¹−C⁻¹J(JᵀC⁻¹J+P⁻¹)⁻¹JᵀC⁻¹. Registrar convenção, unidades, correlações, posto e condição numérica. Se um prior já foi integrado em Cteoria, não somá-lo outra vez. Covariância ausente não autoriza presumir independência.

Não usar ωb obtido do próprio D/H para prever D/H. Um prior CMB com consistência BBN padrão também exige auditoria de circularidade/transferência ao mapa A. Taxas nucleares, τn, dispersão astrofísica e sistemáticas da amostra entram explicitamente no orçamento.

O 1,49% de erro nuclear/weak de Pitrou2018 é da ordem do efeito fracionário 1,5266% do proxy Fields. Essa comparação de escalas não constitui likelihood híbrida legítima nem piso irreduzível. Se a regra ratificada exigir σsys/|Δpred|≤0,3, conferir esse orçamento antes de classificar poder; não aplicá-la usando modelos misturados.

## 6. Neff e calendários

[INPUT local] σNeff=0,17 do retrato Fase8 implica separação 0,70274; a coordenação confere a fonte primária Planck em recibo próprio. Sob A, separação 5 requer σNeff≤0,02389321505.

[KNOWN] Fields2020 §VI adota forecast histórico CMB-S4 de 0,03 condicionado à relação BBN; com Yp livre, Eq. 45 fornece aproximadamente 0,09. [DERIVED condicional] Correspondem a 3,9822 e 1,3274 unidades de σ para ΔNeff acima. Não são desempenho atual verificado nem se transportam sem auditar a relação BBN. Uma relação modificada e determinística poderia recuperar parte da precisão, mas exige Fisher/likelihood recalculada.

[OPEN] Calendários CMB-S4 e Simons Observatory: desconhecidos até fonte atual confiável. Nenhuma data 2030/2032, promessa de entrega ou σSimons foi adotada.

## 7. Travas e decisões

DECISOES_PENDENTES_FASE8.json mantém D1–D11 sem decisão preenchida. O operador deve ratificar escolhas concretas antes de uma análise do composto. Estimador final, orçamento de erros, covariância, alvo final, limiares e autorização de execução permanecem pendentes.

Proposta de ordem de validação: autorização/identidade/hash → modelo/controles/sistemáticas → poder com Ctotal e priors → estatística observada e regra fixa. Se controles falharem, registrar inconclusão; não converter falha sistemática em confirmação nem antecipar resultado científico.

Nenhum resultado aqui decide Big Bang/t=0, move gate, altera Atlas/kernel ou confirma TGL. A próxima unidade útil é ratificar o instrumento e o orçamento de erros do mapa escolhido; repetir o rito antigo sem pergunta nova não resolve essas pendências.
