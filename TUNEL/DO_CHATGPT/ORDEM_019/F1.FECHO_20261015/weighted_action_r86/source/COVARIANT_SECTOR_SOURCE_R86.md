# R86 — Completamento covariante da fonte setorial e conservação do campo reduzido

Autor: /root/r69_locality_bridge. Estatuto: [DERIVED — cálculo analítico condicional; candidato para revisão], sem nova compilação Lean ou campanha numérica. Missão própria projetada/check revision567, ready=true. Os resultados do kernel abaixo são leitura de fonte; não foram recompilados nesta subtarefa. A ação completa da TGL e sua seleção dinâmica não são declaradas resolvidas.

## 1. Reuso e alcance da busca

SectorFluidClosure.lean:21–25 fornece rho_i(t), w_i CONSTANTE e H_sector_nonexchange como hipótese. Linhas36–41 definem rho_tilde_i=(1+beta(1+w_i))rho_i e p_tilde_i=w_i rho_tilde_i. Linhas47–54 e85–102 transportam a continuidade; 104–119 limitam o uso do módulo à densidade total positiva e entalpia total não negativa. SectorFriedmann.lean:22–33 fornece conservação covariante NO FLRW; 45–48 ainda exige H_null. Não é uma ação de correntes fora do fundo.

O artigo tgl_paper_unified.py:10364–10384 escreve L_mod=L_LCDM beta|1+w_eff(z)|; 10349–10362 escreve (1/(2 kappa²)+xi|Psi|²)R. A leitura desses trechos não fixa L_LCDM=-rho, as variáveis materiais conservadas, nem o funcional w_eff fora do fundo. Portanto L_LCDM=-rho será HIPÓTESE NOMEADA do completamento abaixo, não citação dessa definição no artigo.

Busca focal em TGLExt por barotrop, particle-current, fluid-action, number-density, enthalpy e correctedTotalPressure retornou sobretudo as pedras setoriais/FLRW e OrientedBoundaryFace. Busca literal no um.py por rho_of_n/fluid_action/Brown/Schutz não encontrou esses identificadores; SectorFluidClosure aparece embutido (linha127532). Isto é cobertura lexical destes arquivos, não ausência em todo acervo. Nenhum um.py foi importado/executado. A remissão Atlas5364 já registra a conservação sob H_nx e diferença entre as rotas; não a reconstruímos como descoberta.

## 2. Um completamento explícito que reproduz AS DUAS funções setoriais

Hipóteses H_fluid: assinatura (+---); correntes vetoriais densitizadas J_i^a, timelike; n_i=sqrt(g_ab J_i^a J_i^b)/sqrt(|det g|)>0; U_i^a=J_i^a/(sqrt|g| n_i); corrente conservada; equações materiais obtidas variando os campos de fluido; beta constante na variação; rho_i(n_i)=C_i n_i^(1+w_i), C_i>0, w_i constante. A corrente pode ser representada por três rótulos materiais X_i^I e o jacobiano antissimétrico J_i^a=epsilon^{abcd} partial_b X_i^1 partial_c X_i^2 partial_d X_i^3 (com normalização fixa), que é identicamente conservado. Não foi construída aqui identificação desses X com P ou Psi.

A densidade física e a pressão barotrópica satisfazem

    p_i=n_i rho_i'(n_i)-rho_i=w_i rho_i.
    A_i=1+beta(1+w_i), rho_tilde_i=A_i rho_i.
    p_tilde_i=n_i rho_tilde_i'-rho_tilde_i=A_i p_i.

Isso reproduz simultaneamente correctedTotalRho E correctedTotalPressure do kernel, incluindo matéria, radiação e termo constante w=-1. O último pode ser tratado diretamente como densidade constante: não precisa de corrente física de partículas. Não se fixou beta numericamente.

No domínio H=sum_i(rho_i+p_i)>=0, rho_total>0,

    rho_tilde_total=rho_total+beta H
                   =rho_total[1+beta|1+w_eff|].

Assim, SE L_LCDM=-sum_i rho_i e o fator modular multiplica só esse Lagrangiano material, com w_eff=sum_i p_i/sum_i rho_i como funcional dessas mesmas correntes, então L_LCDM+L_mod=-sum_i A_i rho_i. Isto é uma extensão covariante concreta que casa com o fundo. Se L_LCDM inclui EH/outros campos, ou w_eff é apenas z prescrito, a identidade de ações NÃO segue. Para variações arbitrárias que permaneçam na ramificação usamos H>0 em vizinhança; na fronteira H=0 o módulo exige análise de diferenciabilidade. O vácuo puro H identicamente0 é regular e separado. Não extrapolar à ramificação phantom sem mudar o peso.

## 3. Sinal Hilbert e assinatura: duas escolhas pareadas, não equivalentes silenciosamente

Com J densitizado FIXO e variação da métrica inversa,

    delta n = (n/2)(g_ab-U_a U_b) delta g^{ab},
    delta sqrt|g| = -(sqrt|g|/2)g_ab delta g^{ab}.

Logo, para S_minus=-integral sqrt|g| rho(n),

    (2/sqrt|g|) delta S_minus/delta g^{ab}
       = (rho+p)U_a U_b-p g_ab =: T_phys,ab.

Esse tensor dá diag(rho,p a²,p a²,p a²) no FLRW, exatamente FLRWFieldEquations.lean:68–70. O par S_minus, T=+2 deltaS é consistente com a hipótese L_LCDM=-rho. Já adotando T=-2 deltaS, S_minus produz -T_phys. Nesse segundo convênio, S_plus=+integral sqrt|g|rho produz +T_phys.

Assim, com a variação de +F_c R usada em R85, a ação +EH+S_minus conduz F_c G=-T_phys/2, não +T_phys/2. Para obter a equação com sinal positivo pode-se parear -EH+S_minus e T=+2 deltaS, ou +EH+S_plus e T=-2 deltaS. A escolha do sinal RELATIVO é informação física do contrato; esta nota não escolhe uma delas como a ação canônica. A assinatura/curvatura do kernel não elimina essa distinção. R83 deriva densidades locais e não resolve automaticamente o pareamento de todos os termos do artigo.

## 4. Variação de w: condição exata de compatibilidade

Se rho=rho(n) é qualquer função C² positiva, p=n rho'-rho e se escolhemos rho_tilde=rho+beta(rho+p)=rho+beta n rho', a MESMA variação exige

    p_tilde=p+beta n p'.

Já o reescalonamento de fundo A p, com A=1+beta(1+p/rho), difere por

    p_tilde-Ap=beta[n p'-(1+w)p]=beta n rho w'(n).

Portanto w constante é suficiente; para beta,n,rho não nulos é também necessário para essa igualdade em intervalo. Não se pode impor as duas fórmulas de fundo com w(n) variável e omitir o termo derivado. Para vários setores independentes o termo faltante soma beta n_i rho_i w_i'(n_i). Com entalpia negativa, a extensão pelo módulo muda o sinal da correção em cada ramificação do H total, não o de cada setor arbitrariamente.

## 5. Conservação: o que segue e o que precisa de equação material

Para T_phys=(rho+p)UU-pg e theta=div U,

    div T_b = U_b[U(rho)+(rho+p)theta]
              +(rho+p)a_b-(delta_b^a-U_b U^a)partial_a p.

A corrente conservada dá U(n)+n theta=0 e anula o termo de energia por p=n rho'-rho. O restante é a equação de Euler do fluido. Conservação da corrente SOZINHA não anula o gradiente espacial/força. Os campos de rótulo materiais variacionais fornecem esse Euler quando estão on-shell; no fundo homogêneo/comóvel os gradientes espaciais e aceleração desaparecem e recuperamos precisamente H_sector_nonexchange. A multiplicação constante A_i preserva cada equação; se há troca entre setores ou A(x), entram termos adicionais.

O completamento, portanto, constrói fonte e lei de conservação condicional às equações materiais nomeadas em geometria geral. Não gera por si a métrica de P, não impõe estacionariedade gravitacional e não identifica esses fluidos com selectedSigmaRecord. Mesmo em ramo conservado, H_null de SectorFriedmann permanece necessário até outra derivação.

## 6. Consequência forte para a redução same-P de R85

Reutilize s=P_selected, c=ds, q=g^{-1}(c,c)>0 e

    A(s)=cG/[4(1-s)], B(s)=cG/[8s(1-s)^2],
    L_eff=A+Bq, T_eff=L_eff g-2B c tensor c.

É a convenção T=-2 deltaS para S=integral sqrt|g|L_eff, mantida de R85. Para conexão Levi-Civita, derivação direta (partial_b q=2 c^a Hess_ab s, Hess simétrica) fornece

    nabla^a T_eff,ab = E_s partial_b s,
    E_s=A'(s)+B'(s)q-2 nabla_a(B(s)nabla^a s).

Como q>0, ds não é zero em nenhum ponto; portanto div T_eff=0 SE E SOMENTE SE E_s=0. É uma equação diferencial real de P; não um selo produzido pela normalização sum P=1. No setor EH constante, Bianchi e equação métrica F_c G=T_eff/2 obrigam E_s=0. Isso oferece verificação independente de qualquer suposto habitante estacionário e não fornece esse habitante automaticamente.

Para uma função nomeada F(s) multiplicando R (e somente nesse contrato reduzido),

    F G_ab+(g_ab box-nabla_a nabla_b)F = T_eff,ab/2,
    div[lado esquerdo]_b=-(R/2)partial_b F.

Assim a equação métrica obriga [E_s+F'(s)R]ds=0 e, pelo relógio timelike,

    E_s+F'(s)R=0.

Esta é a equação escalar completa desse setor, coerente com a variação direta. Se fluidos conservados independentes forem acrescentados, não alteram a identidade; se dependem de s/P ou trocam energia, seus termos escalares/transferências devem ser incluídos. Não assumir u=|Psi|²=F(s) sem ponte; não importar essa conclusão para o acoplamento completo do artigo por nome.

## 7. Progresso material e pendência precisa

[DERIVED] Existe completamento covariante explícito da fonte setorial de w constante e ele produz ambas as correções e sua conservação on-shell, não só a equação 00. [DERIVED] O termo beta n rho w' identifica o erro exato de extrapolar esse fechamento a w variável. [DERIVED] Na ação reduzida same-P, a conservação requer a equação E_s, ou E_s+F'R no contrato não minimal. [OPEN] Vincular correntes/rótulos e o sinal relativo da ação a Psi/P e à dinâmica independente existente; verificar a fonte total incluindo os termos restantes. A nota não é escolha do modelo físico, não é ação canônica instalada e não fecha R16.
