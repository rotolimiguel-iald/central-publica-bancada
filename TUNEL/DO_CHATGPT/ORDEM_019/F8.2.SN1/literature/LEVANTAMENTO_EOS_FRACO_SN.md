# F8.2.SN1 — levantamento de EOS, interações fracas e observáveis de SN Ia

Autoria: Codex, subagente `sn_ew_literature`, para a gerente TGL. 09/10/2026. Escopo: literatura e relações analíticas de referência; nenhuma amostra foi ajustada, nenhum composto calculado, nenhum resultado de natureza reivindicado.

## Consulta e reaproveitamento

[REAL — consulta local] `python C:\IALD\NOS_VIVO\consultar.py --unidade F8.2` foi executado antes desta nota. O índice aponta a família `outro.grande_atrator_e_chandrasekhar` (164), já proposta para auditoria, e a rota dos setores cosmológicos. O índice não fornece uma ponte nova entre β e taxas estelares. O Atlas, verbete Chandrasekhar, mantém o resultado histórico como contorno observável e recusa usá-lo como evidência de β ou renormalização local de G. A retomada autorizada pelo operador testa uma formulação posterior; não reutiliza o antigo percentual como amplitude.

## 1. Controle analítico que já existe

[KNOWN — L01, §2 e §4, equações 6–7 e 31–39] Para matéria fria de uma espécie, elétrons ultra-relativísticos, rede iônica bcc e aproximação politrópica não magnética:

\[
P=K\rho^{4/3},\quad K=K_0(1+c_Z\alpha),\quad
c_Z=\frac{8C_M}{6}\left(\frac4{9\pi}\right)^{1/3}Z^{2/3},
\qquad C_M=-0.895929255682.
\]

\[
\frac{M}{M_{\rm Ch}}=(1+c_Z\alpha)^{3/2},\qquad
M_{\rm Ch}=3.09798\frac{m_P^3}{m^2}Y_e^2.
\]

Aqui Z=6 para carbono e Z=8 para oxigênio. Este é um efeito eletromagnético conhecido. A estrela fria idealizada não é um cálculo de ignição ou de explosão; mistura, temperatura, transporte e cinética não foram resolvidos.

[DERIVED — diferenciação da expressão acima, composição e G fixos]

\[
\frac{\partial\ln M}{\partial\ln\alpha}
=\frac32\frac{c_Z\alpha}{1+c_Z\alpha},\qquad
\frac{M(\alpha_1)}{M(\alpha_0)}
=\left(\frac{1+c_Z\alpha_1}{1+c_Z\alpha_0}\right)^{3/2}.
\]

Isso permite o controle solicitado com a MESMA EOS para α e α×multiplicador. Não identifica o multiplicador com uma previsão TGL. Como c_Z<0, aumentar uniformemente α reduz o limite nesse modelo. A fórmula antiga com `(1−β)^(3/2)` não é esta expressão.

[DERIVED — consistência termodinâmica] Se uma hipótese física futura produzir α(n_e), a energia Coulomb tem forma ε_L=A α(n_e)n_e^(4/3). Então P_L=A[α n_e^(4/3)/3+n_e^(7/3)dα/dn_e]. A substituição ponto a ponto em P_L=ε_L/3 perde um termo. Running de renormalização não equivale automaticamente a campo ambiental α(n): uma energia efetiva consistente deve evitar dupla contagem de logs e contratermos.

## 2. O setor fraco entra por processos, não por uma energia livre somável

[KNOWN — L02–L04] Capturas eletrônicas, decaimentos e Urca afetam a neutronização e o perfil térmico durante simmering. Martínez-Rodríguez et al. incluem os perfis de densidade/temperatura no MESA e revisam a estimativa anterior de Piro–Bildsten. O excesso de nêutrons afeta Mn, níquel estável e a produção radioativa. Timmes–Brown–Truran obtêm uma relação condicional entre composição inicial e Ni56; ela depende da região que atinge equilíbrio nuclear, não constitui uma lei universal L(M_total).

[DERIVED — identidade de sensibilidade idealizada] Mantendo os demais parâmetros, δlnM_Ch=2δlnY_e−2δlnm−(3/2)δlnG. Portanto um efeito em Y_e pode entrar sem renormalizar G. O sinal e a amplitude de δY_e exigem integrar taxas e a evolução térmica; não seguem de β(χ) isoladamente.

[OPEN — ponte que falta especificar] Devem ser definidos o processo microscópico, escala de transferência, esquema de acoplamentos, elemento de matriz nuclear, distribuição eletrônica, correções de plasma e balanço de neutrinos. A lei β_TGL=√e α(χ) não determina sozinha G_F, g_A, elementos de matriz ou taxas de captura.

[KNOWN — L07] O running eletrofraco relaciona α, g, g′ e o ângulo fraco com condições de matching e esquema especificados. [DERIVED — distinção de notação] β_TGL é um coeficiente; a função beta RG é μ dg/dμ. A igualdade de nome não é uma ponte. Uma correção de running não acrescenta, por si, um reservatório de energia eletrofraca.

## 3. Observável candidato que reduz a degenerescência de distância

[KNOWN — L05] Com expansão livre homóloga, energia interna dominada por radiação e alimentação Ni56→Co56→Fe56, dE/dt=Q_dep−L_bol−E/t. Multiplicação por t dá tE=∫t′Q_dep dt′−∫t′L_bol dt′. É uma conservação condicionada às aproximações, não uma regra irrestrita para qualquer nova dissipação.

[KNOWN — L06, §§2.1, 2.3, 3.3 e 6; somente consulta web] A razão L_bol(t)/∫_0^t t′L_bol(t′)dt′ cancela uma normalização multiplicativa constante, incluindo a distância, e informa o escape gama t0. Massa ejetada não se determina univocamente de t0 e Ni56. O método ainda tem erros de modelo, cobertura UV/IR, extinção dependente de cor, tempo de explosão e energia residual; cancelamento de distância não elimina esses termos.

[PROPOSTA] Se houver derivação TGL para composição/ejeção, prever conjuntamente uma mudança nessa forma temporal e uma razão de elementos neutronizados (por exemplo Ni estável/Fe ou Mn/Fe), com covariância e seleção de canais de progenitor. O elemento químico é uma assinatura de processo; um excesso isolado também pode vir de metallicidade, densidade de ignição ou canal explosivo. Não somar significâncias como se fossem independentes, nem somar com a Fase 9. Um deslocamento constante de luminosidade, sem referência externa, pode ser absorvido na calibração. A v388 precisa fornecer o residual frente ao MESMO Modelo Padrão e à MESMA astrofísica de referência.

## 4. Candidato covariante RμνFμρFνρ/Mp²

[DECLARADO — localização comunicada pelo agente revisor; este subagente não abriu o Tratado] O candidato comunicado está em `secao_01_fundamentos.tex:580`, com coeficiente β/Mp². Esta seção avalia essa forma matemática, não autentica sua derivação TGL.

[DERIVED — análise dimensional] Em unidades naturais, R tem dimensão 2 e F dimensão 2; RFF é operador de dimensão 6, compatível com coeficiente β/Mp² numa lagrangiana de dimensão 4. A escala perturbativa local é da ordem β R/Mp², com a convenção de massa de Planck explicitada. Não é δL/L sem resolver dinâmica e transporte.

[KNOWN — L08] Drummond–Hathrell calculam termos de curvatura–fóton na QED de um loop. A escala do termo QED é fixada pelo elétron, O(α/m_e²), e precisa entrar na referência. A presença da estrutura RFF não é assinatura exclusiva TGL. Ação local real com esse operador também não fornece, sozinha, uma taxa GKLS: dissipação exige redução de graus de liberdade e a respectiva derivação.

[DERIVED — limites] No Schwarzschild de vácuo exato, Ricci=0: a densidade desse operador Ricci específico e sua correção à equação de Maxwell em FUNDO FIXO desaparecem. Não concluir que a variação métrica/backreaction desaparece: variar Ricci pode produzir derivadas de FF. Weyl/Riemann permanece não nulo; estruturas Riemann FF são diferentes. Dentro da estrela, matéria/radiação tornam Ricci não nulo.

[OPEN] A conservação total requer ação e equações covariantes para todos os setores. Se β(χ(x)) varia, tratar χ como fundo prescrito não basta para provar ∇μT_total^μν=0. É preciso declarar sua dinâmica ou a fonte de troca. Nenhum destes fatos, sozinho, demonstra uma modificação da pressão estelar, de M_Ch ou da luminosidade.

## Catálogo primário e custódia

1. **L01 — Chamel et al., Electron Captures and Stability of White Dwarfs**, arXiv:2110.11038v1, contribuição com novos resultados analíticos e numéricos dos autores: https://arxiv.org/html/2110.11038v1 . Âncoras: §§2–4, Eq.6–17 e 31–39. HTML integral custodiado.
2. **L02 — Martínez-Rodríguez et al., Neutronization During Carbon Simmering In Type Ia Supernova Progenitors**, ApJ 825,57 (2016): https://arxiv.org/abs/1602.00673v2 . Âncora: resumo, resultado do cálculo MESA. Página de resumo custodiada; PDF não custodiado.
3. **L03 — Piro e Bildsten, Neutronization During Type Ia Supernova Simmering**, ApJ 673,1009 (2008): https://arxiv.org/abs/0710.1600 . Âncora: resumo; histórico confrontado com L02. Página de resumo custodiada.
4. **L04 — Timmes, Brown e Truran, On Variations in the Peak Luminosity of Type Ia Supernovae**, ApJL 590,L83 (2003): https://arxiv.org/abs/astro-ph/0305114 . Âncora: resumo/hipóteses da relação composição–Ni. Página de resumo custodiada.
5. **L05 — Katz, Kushnir e Dong, An exact integral relation between the Ni56 mass and the bolometric light curve of a type Ia supernova** (2013): https://arxiv.org/abs/1301.6766 . Âncora: resumo com equação e hipóteses. Página de resumo custodiada.
6. **L06 — Wygoda, Elbaz e Katz, Type Ia supernovae have two physical width–luminosity relations… I. Bolometric**, MNRAS 484,3941 (2019): https://academic.oup.com/mnras/article/484/3/3941/5289612 . Âncoras: §§2.1/2.3/3.3/6. [KNOWN — consultado via ferramenta web; CUSTÓDIA LOCAL OPEN, GET recusado 403]. Não há pin dos bytes da página nesta entrega.
7. **L07 — Erler e Ramsey-Musolf, Weak mixing angle at low energies**, PRD72,073003 (2005), versão final2007: https://arxiv.org/html/hep-ph/0409169v2 . Âncoras: introdução Eq.1–5; RGE e matching. HTML integral custodiado.
8. **L08 — Drummond e Hathrell, QED vacuum polarization in a background gravitational field and its effect on the velocity of photons**, PRD22,343 (1980): https://journals.aps.org/prd/abstract/10.1103/PhysRevD.22.343 . Âncora: resumo do editor; artigo original identificado. Página de resumo custodiada, não o PDF integral.

Os hashes foram calculados dos bytes pelo script e estão em `SOURCE_CUSTODY_PUBLIC_FETCH.json`. A primeira tentativa, sem rede liberada, permanece em `SOURCE_CUSTODY.json`: sete recusas explícitas, nenhum falso pin. Custódia HTML não é custódia PDF nem reprodução independente da física. A navegação de literatura expôs resultados publicados; nenhum catálogo foi aberto como amostra decisória e nenhum teste cego é alegado.

## Conclusão de viabilidade documental

[REAL — levantamento] Há uma EOS analítica de referência, canais fracos conhecidos e um observável de forma temporal com normalização cancelada. [OPEN] A derivação TGL→escala física→EOS/taxas→ejeção continua necessária. [PROPOSTA] Usar primeiro sensibilidades condicionais e exigir o residual frente à referência antes de estimar poder. Esta nota não fornece um sinal TGL numérico, cinco sigmas ou confirmação.
