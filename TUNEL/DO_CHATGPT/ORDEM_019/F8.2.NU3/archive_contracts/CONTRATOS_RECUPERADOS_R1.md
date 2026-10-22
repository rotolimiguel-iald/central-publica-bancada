# F8.2.NU3 — contratos dos neutrinos recuperados do acervo

**Autor:** codex-gerente-tgl / pesquisador `nu2_skeptic`. **Unidade reivindicada:** 633. **Escopo:** pesquisa documental e tradução matemática condicional; nenhum original científico executado, nenhuma amostra observada composta, nenhuma escrita na Bancada ou memória.

## Resultado da recuperação

[REAL documental] O contrato existe no acervo e não se limita ao cálculo de propagação da NU2. Foram abertos e pinados **20 arquivos**: artigos DOCX de janeiro, artigos NMC e *Lie of Light*, preditor de fluxo, três programas de junho, Custo, Ponte, artigo terminal, Tratado, rito de massa e erratas. Os manifestos guardam o SHA-256 integral de cada original, a extração e sua convenção de âncora. A referência `Sxx:linha` remete à extração correspondente; nas fontes PDF, página e equação acompanham a linha. As extrações não substituem os originais.

[DERIVED] A composição hoje executável tem **três espaços distintos**: (a) paridade × carga na fronteira; (b) realização espectral modular; (c) estados de massa/sabor na propagação. A existência das três descrições não identifica automaticamente os três operadores. Essa separação permite implementar o que já está especificado e localizar exatamente a ligação que cada aplicação física precisa fornecer.

O manifesto de consumo é **CONTRACTS_API_R2.json**. A R1 permanece intacta. Ele contém dez canais, suas equações, unidades, parâmetros, limites e fontes. `INDEX_SEARCH_RECEIPTS_R1.json` registra buscas focadas no índice existente; o índice não foi reconstruído. A busca inicial também consultou ajuda do buscador, Nós Vivo (a unidade NU3 ainda não constava), mapa e a PORTA da pasta Neutrinos. O catálogo é navegação; os originais foram abertos separadamente.

## 1. Canal da fronteira: um operador concreto já está escrito

[REAL documental] O artigo terminal escreve **Lν = X_A ⊗ I_B**, no espaço de quatro estados paridade × carga, com anticomutação com Z da paridade e comutação com a carga (S12:2821). O mesmo artigo dá a ação candidata de seleção do gap χ, com λ e μ explicitamente ainda no balanço a fechar (S12:1014–1016). Não cabe afirmar que falta todo operador neutrínico.

[DERIVED] Para a normalização sem escala física, o dissipador é

    dρ/ds = LνρLν − ρ,
    ρ(s) = (1+e^(−2s))ρ0/2 + (1−e^(−2s))Lνρ0Lν/2.

O canal é CPTP e conserva carga porque Lν comuta com ela. Se a entrada tem paridade positiva, a ocupação negativa é `−expm1(−2s)/2`. Essa é uma **probabilidade de transferência de paridade**. Ela não é uma contagem absoluta de partículas emitidas. Um tempo em segundos exige a taxa que converte s em t. Conservação da energia do subsistema exige `[H,Lν]=0`; caso contrário, o balanço deve incluir troca com o ambiente. As propriedades algébricas citadas sozinhas não provam unicidade do neutrino do Modelo Padrão entre todos os campos possíveis.

**API sugerida:** `boundary_parity_evolution(rho0, modular_time)`. Ela pode testar a fronteira agora, com o estatuto dimensional visível.

## 2. Da métrica modular à lei espectral física

[REAL documental] Na realização finita da Ponte, `Lmod=√β0 √K∂` dá exatamente

    Γij_mod = β0(√ki − √kj)²/2.

A fonte é S07:1104–1115. Os `ki` são autovalores modulares; esse K∂ não é o invariante de Kretschmann. Não igualar `ki` a `mi²/(2E)` apenas por ambos serem espectros. A discussão da escolha de √K∂ também está registrada na Ponte (S07:1235–1240); o estatuto de uma passagem não é transferido para outra por nomenclatura.

[REAL documental] A lei física madura está na Ponte (S07:817–830), no Custo (S11:3116–3122) e nos programas originais de junho (S08:49–58; S09:62–70):

    Γω = β0 τ★ ω² Kfac / 2,
    Kfac = (K_Kretschmann/K★)^β0 quando esse perfil é fornecido.

[DERIVED condicional] Uma realização energia-preservante dessa lei é

    dρ/dt = −i[H,ρ]/ℏ − β0τ★Kfac [H,[H,ρ]]/(2ℏ²),
    Lphys = √(β0τ★Kfac) H/ℏ.

Com H em eV, ℏ em eV·s, τ★ em s e Kfac adimensional:

    Γij[s⁻¹] = β0τ★Kfac (Δm²ij/(2Eℏ))²/2,
    Γij[eV] = ℏ Γij[s⁻¹].

Para H fixo essa realização conserva traço, positividade e `tr(Hρ)`. Em vácuo ultrarrelativístico, H≈diag(mi²)/(2E), o perfil tem n=−2 se τ★ e Kfac forem fixos na energia. As taxas dos três pares são ligadas pelos mesmos três níveis: a textura é proporcional aos quadrados dos três splittings, e não a três taxas livres. A matriz PMNS é a leitura de sabor, com entrada física própria.

Uma densidade já diagonal nessa base é estacionária **exatamente** para esse dissipador. Isso não cancela uma fonte de produção, a interação fraca ou uma mudança do Hamiltoniano no meio: são outros termos. A NU2 calculou um efeito minúsculo sobre entrada coerente em uma geometria ideal; isso não demonstrava inexistência de todos os contratos neutrínicos da teoria.

**API sugerida:** `mass_dephasing_rates(E_eV, dm2_eV2, tau_star_s, Kfac, alpha_thomson)`, seguida de `propagate_mass_density(...)`. O ramo tP deve entrar nomeado como instância condicional. Os artigos já nomeiam τ★; não se deve afirmar que o contrato não existe porque seu valor físico é uma entrada.

## 3. Onde entra o fator de escala

[REAL documental] A v388 define `β(χ)=√e/cosh(χ/2)` e identifica a relação entre χ e escala física como INPUT/ONTO (S19:11–27). A família matemática atinge √e em χ=0; o contrato que usa β como probabilidade tem domínio mais restrito, β<1 (S19:100–102).

A Ponte distingue a corrida no bulk e a fronteira Thomson (S07:1328–1341), e fixa explicitamente o coeficiente de dephasing **independente da frequência** (S07:1367–1371). Por isso, a implementação vigente usa `β0=ALPHA_FINE_CODATA_2018×sqrt(e)` em runtime. A família β(χ) continua disponível para o regime ao qual foi atribuída. Substituir β0 por β(E) no dissipador maduro seria outro contrato; χ(E), τ(E) e K(E) teriam de ser especificados antes, sem ganho espectral presumido.

O Tratado chama a referência de 1 eV na fórmula de massa de escala eletrofraca (S16:452–461). O rito congelado posterior é mais preciso: chama-a **NORM, declarada, não derivada** (S13:38–39). A frase histórica não fornece uma nova taxa de reação fraca ou uma prescrição para trocar 1 eV por mW, mZ ou pela energia medida do neutrino.

## 4. Produção, massa e NMC: há contratos, com linhagens próprias

| Ramo recuperado | O que foi escrito | Leitura para a implementação |
|---|---|---|
| Eco → neutrinos, janeiro | Eeco=βlegado EGW; mνc²=βlegado sin45°·1 eV; Nν=Eeco/(mνc²) (S01:395–424; S06:15–25) | O nome antigo α² vale 0,012031, não αEM². O β cancela de Nν. A quantidade por área é fluência; o denominador é energia de repouso, não espectro relativístico. A reta de inclinação 1 é identidade da receita. |
| NMC de produção, 2025 | Lint=−Γ(S)R|Ψ|² ψ̄νψν; deslocamento de massa Γ(S)R|Ψ|²; dnν/dt=Γ0 nγ R/MPl² (S02, p.2 Eq5/9/12) | Contrato localizado. Γ(S) não é Γij. Com campos canônicos naturais, Γ(S) tem dimensão E⁻³. A taxa exige Γ0 em E, mas o texto imprime Γ0∼αEM MPl², em E². É diagnóstico dimensional específico; não inserir taxa absoluta corrigida sem marcar a escolha. |
| NMC de fase | Pee com multiplicador `1+(α²/MPl²)Φ/c²`, Φ=∫g dz; fator de meio ne/ne,ref·Eν/Eres (S15, p.9 Eq33–41) | O potencial/c² é adimensional; o 1/MPl² restante torna a correção impressa dimensional. A ação RμνFμρFνρ/MPl², por sua vez, tem dimensão correta. Não apagar MPl² para aumentar o sinal. |
| Massa m2 | m2=β0 sin45°·1 eV; comparação com √Δm²21 sob m1≈0 (S13:33–66; S12:2831) | Rito ativo, com normalização declarada. Não determina PMNS, produção ou taxa de fuga. A soma foi aposentada como discriminante de β. |
| Massa mais leve | mlightest=ρΛ^(1/4), demais massas com splittings medidos (S11:1788–1864) | Outro contrato preservado no Custo. Não combinar silenciosamente m1≈2,29 meV com a comparação m1≈0 do rito m2. |
| Degradação temporal | D=exp(−∫Γdτ), massa m0+a log(Δt/τ0), fórmula PMNS preservada (S03, p.7 Eq11, p.11 Eq28, p.14 Eq35) | Fenomenologia histórica com parâmetros nomeados. Não é a fórmula 8,51 meV; a atenuação de amplitude não é por si só um canal CPTP. |

[DERIVED] No exterior de Schwarzschild exatamente no vácuo, R=0 e Rμν=0, enquanto Kretschmann não é zero. Assim o R da produção antiga, o Ricci tensorial do RFF e o K da lei de dephasing têm papéis diferentes. Uma estrela com matéria e um exterior ideal também são regimes diferentes.

O manuscrito NMC antigo preserva explicitamente coerência de sabor e põe a entropia no setor gravitacional (S02, p.9 Eq51). A identificação com um dissipador na base de massas precisa ser feita por operador, não pelo uso comum da palavra decoerência.

## 5. Erratas que governam a ligação atual

[REAL documental] O artigo terminal corrige o timing NMC: o neutrino mantém o Shapiro padrão da RG; o excesso é do setor eletromagnético do fóton (S12:2833). O esquema calculável de comparação é `lag_intrínseco + atraso_massivo(E) − atraso_extra_fóton`. Os 10–100 ms e o forecast de 21σ escritos no artigo não foram reproduzidos aqui a partir de uma lente nem constituem significância observada.

[REAL documental] No Custo, a massa de Chandrasekhar via mudança universal local de G foi retirada ao lado (S11:3315), e o observável gravitacional maduro é dephasing; a receita de eco atrasado não é uma previsão desse dissipador (S11:3307). A errata assinada de 19/09 fixa o sinal negativo de −ξR|Ψ|² e ξ=1/6, **distinto de β** (S18). A versão nova não pode recuperar automaticamente a antiga fórmula de massa estelar apenas trocando o número de β.

[REAL documental] O literal 7,8×10⁻¹⁰ s no bloco J.4b não é limite medido de τ★, como fixa a errata S20. O limite JUNO da fonte publica outra textura de taxas e não deve virar uma cota TGL sem a mesma definição do operador e da verossimilhança.

## Encaminhamento

Implementar primeiro os três módulos matemáticos acima, com modelos e relógios nomeados, testes sintéticos de conservação e solução analítica. Para a estrela, conservar uma contabilidade comum: a energia que sai num canal de produção deve ser a que falta no emissor/ambiente; um canal de dephasing que conserva H não fornece esse débito por si só. O passo concreto posterior é escolher, dentre os contratos recuperados, o operador e o regime que governam emissão/propagação e compor com a equação de transporte e o modelo estelar. Esta pesquisa não iniciou ajuste, não calculou poder observado e não moveu gate.
