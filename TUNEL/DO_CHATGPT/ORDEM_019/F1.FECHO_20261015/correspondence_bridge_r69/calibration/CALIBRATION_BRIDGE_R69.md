# R69 — correspondência concreta e calibração do instrumento

[DERIVED — candidato] Camada de composição finita, de autoria do agente r69_calibration_bridge. Nenhuma aquisição, ajuste de beta, evolução GKLS nova ou medição de significância. R4 continua aberto como calibração física do mesmo sistema; a API abaixo é um contrato sintético e não admite recibos físicos.

## 1. Reuso com tipos preservados

R68 fornece P=post(a), Q=I−P e a equivalência Px=a ∧ Qx=0 ↔ x=a. Para ‖a‖=‖x‖=1, Px=a já força x=a; o controle x=a+y com y ortogonal não nulo é de vetores gerais, não normalizados. Não se equiparam a, P e uma matriz densidade ρ. A igualdade de representantes vetoriais também fixa fase; a e −a possuem o mesmo projetor físico.

R62, `run_prepared_readout_r62_r2.py:187–188`, fornece as duas expressões reais de decodificação reutilizadas por extração de AST, verificando os bytes por SHA256 antes do uso:

    C = (XX−PP+i(XP+PX))/2
    B = (XX+PP+i(XP−PX))/2.

R64, `CONTRATO_OUTPUT_R64.md`, fornece o instrumento H_MARKOV_VACUUM_PORTS, quatro preparações equivalentes com fases XX/PP/XP/PX, filtros L² normalizados e os operadores temporais de saída. C e B reconstruídos são momentos dos modos temporais filtrados, não tomografia integral nem operadores instantâneos da cavidade. A matriz é de momentos cruzados brutos; se a entrada for covariância, somar os produtos das médias antes da decodificação correspondente. A presente API exige momentos brutos.

R65, `CONTRATO_CALIBRACAO_R65.md` §§2–5 e `IDENTIFIABILITY_COMPLETION_R65.txt`, já fixa J0, a liberdade de escala do salto, a conversão de tempo/filtros e a razão lambda/Gamma. Estes contratos não são refeitos nem promovidos a medições. Todos os originais são pinados no pré-registro.

## 2. A ponte de correspondência que efetivamente se pode transportar

Se uma calibração C é invertível sobre as coordenadas COMPLETAS do mesmo espaço finito, z=Cx, a'=Ca e P'=CPC⁻¹. Então P'z=a' e (I−P')z=0 equivalem a z=a', logo x=a. P' continua idempotente. Só quando C é unitária se preservam automaticamente a ortogonalidade e a norma euclidiana. Para ganho geral, usar a métrica G=(C⁻¹)†C⁻¹: ‖Cx−Ca‖²_G=‖x−a‖². A implementação `transported_residual` verifica essa igualdade, recusa singularidade/condicionamento excessivo e não deduz C a partir do alvo desejado.

Se o instrumento fornece apenas y=Mx com M não injetivo, Mx=Ma só estabelece x−a∈ker M. É necessário obter coordenadas adicionais ou uma hipótese justificada que torne M injetivo no domínio admitido. Para estados densidade, a observação é o mapa linear O(ρ)=(Trρ XiXo,Trρ PiPo,Trρ XiPo,Trρ PiXo). A igualdade de O não implica ρ=ρ_alvo. Não existe tradução automática do resíduo vetorial Qx para quatro números de O.

Controle executável finito: na ordem |00>,|01>,|10>,|11>, ρ0=|00><00| e ρ1=|10><10| são positivos de traço um, têm os quatro momentos cruzados iguais a zero e diferem por norma de Frobenius √2. Isso demonstra a não injetividade dessa observação selecionada. Não afirma indistinguibilidade sob todos os momentos temporais, todas as preparações ou todas as medidas. É suficiente para recusar a promoção dos quatro números a uma identidade de estado completo. O fator OH pode ser tensorizado no mesmo estado para ambos. Não se afirma igualdade de toda a série temporal sob o gerador R66 com acoplamento e bombeamento; populações ou tempos adicionais podem distingui-los. A extensão aos modos de Fock infinitos ou à dinâmica temporal exige sua própria ponte, e não é reivindicada.

## 3. Calibração concreta de ganho, LO e relógio

Escreva Q como matriz real 2×2, linhas Xi/Pi e colunas Xo/Po. Ganhos escalares positivos g_i,g_o e fases LO conhecidas θ_i,θ_o dão Q_raw=g_i g_o R(θ_i) Q R(θ_o)ᵀ, com R(θ)=[[cosθ,sinθ],[−sinθ,cosθ]]. O inverso calibra Q antes do decoder. Ganhos diferentes entre configurações, offsets, ruído eletrônico correlacionado e deriva de preparo não são modelados; nesse caso, este contrato é insuficiente e não deve ser usado para certificar correspondência. A escolha dessas constantes em testes é INPUT sintético, sem recibo físico.

Sob τ=t/t0: r_d=t0 r_phys, f_d(τ)=√t0 f_phys(t0τ) e θ_d(τ)=θ_phys(t0τ). Assim a quadratura integrada permanece a mesma quando o incremento é transportado por dX_d=dX_phys/√t0. O teste usa o filtro exponencial casado já descrito em R64, sem resolver nova ODE. A fase no quadro girante segue θ_rot=θ_lab+ω_d t, do contrato R64; não se deduz relógio interno a partir da fase externa.

## 4. Condição de identificar beta, sem preenchimento circular

Na convenção J0=a_o†σ−+σ+a_i com coeficientes unitários, lambda_phys=beta Gamma. Se Gamma>0 é calibrada independentemente, beta=lambda_phys/Gamma, ou beta=(lambda/kappa)/(Gamma/kappa). O relógio cancela na razão; a calibração independente de Gamma não cancela. Sem ela, (beta,Gamma)↦(c beta,Gamma/c) preserva lambda. Fixar Gamma=lambda/betaTGL seria circular neste teste. Nenhum valor teórico betaTGL é usado pelo código para completar o denominador.

`synthetic_ratio` devolve OPEN_INDEPENDENT_GAMMA com beta=null quando Gamma falta, é zero ou não é independente. Com números sintéticos admissíveis, devolve CONDITIONAL_SYNTHETIC_RATIO e measurement_verified=false. A marca de independência é uma entrada do teste, não prova documental: admissão de recibos físicos é deliberadamente recusada pelo esquema atual. Falta positividade de informação em lambda e Gamma? R65 já fornece o determinante Gamma² I_lambda I_Gamma; a execução de testes de esquema não mede essas informações.

O restante da ponte gravitacional — V0, Eref, kappa modular/geométrico, domínio do salto bosônico e identificação dos mesmos canais — permanece no alcance aberto do contrato R65. Não se identifica kappa de cavidade com kappa modular por homonímia.

## 5. Teste e critérios pré-registrados

`PRE_REGISTRO_R69.json` fixa tolerância, modelo, convenções, fontes e controles. `FREEZE_R69.json` pina os bytes de plano, código, relatório e runner antes do START. Os resultados devem distinguir: validade do esquema, correspondência dos momentos selecionados, correspondência de coordenadas completas sintéticas e calibração física (não executada). O runner recusa sobrescrever resultado/START. NaN, infinito, booleano e unidades/convenções erradas são recusados antes da álgebra. O recibo registra UTC início/fim, duração, exit code, comando, runtime e hashes.

PASS significa que as identidades e recusas do contrato sintético funcionaram nos controles definidos. Não significa beta medido, 5sigma, estado completo identificado, aparelho calibrado, rede física causal instalada ou R4 encerrado.
