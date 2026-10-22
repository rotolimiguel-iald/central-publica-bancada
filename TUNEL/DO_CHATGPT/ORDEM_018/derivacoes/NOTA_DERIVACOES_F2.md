# NOTA_DERIVACOES_F2 — ORDEM_018
[DERIVED condicional / OPEN, com fontes lidas por hash] 06/10/2026 UTC. Autor: chatgpt-codex/ordem-018/derivacoes.

A leitura das fontes resolve duas ambiguidades do catálogo: a distância acumulada contém uma **integral** de K, e o canal da soma de massas dos neutrinos já foi aposentado como discriminante. Para dualidade, temperatura, lentes e crescimento, a lei escalar K não seleciona sozinha um mapa observacional. Abaixo estão as extensões compatíveis e as condições que permitem distingui-las. Nenhum dado novo foi aberto para veredito; nenhum ajuste foi executado.

## Evidência e método

A ordem, o protocolo anti-parede, os trechos do Atlas, o programa canônico e os motores da Bancada foram lidos. O canônico não foi importado nem executado. O arquivo F2_FONTES_SHA256.json traz hashes calculados dos originais e das seis fontes primárias públicas. source_excerpts contém somente recortes com linhas e proveniência, não uma bifurcação do cânone. mapas_consultados.json é extrato da consulta MCP, com notas abreviadas identificadas pelos seq; o mapa original continua autoridade.

PLANO_F2_ANTES_DOS_CALCULOS.md foi gravado e hasheado ANTES dos cálculos. f2_analysis.py calcula beta pela constante ALPHA_FINE_CODATA_2018 lida do um.py, vezes sqrt(e); produz F2_CALCULOS_CONDICIONAIS.json. Resultado runtime: beta=0,012031300400803142. Tempo do cálculo e captura local: 0,418 s nesta rodada; 54 verificações passaram (refinamento, limite beta=0, desigualdade da média). A GPU não beneficia estas integrais escalares; nenhuma inference remota ocorreu nesta subtarefa. request_ids=[]; toda a análise ainda depende da revisão da coordenação/gerência.

Os números de planejamento usam Hfid=70 km/s/Mpc, Omega_m=0,3, Lambda=0,7, zero radiação somente para a ilustração z<=3. Não são ajuste a alvo. O JSON também varia Omega_m=0,25/0,35. Portanto não transferir seus números ao fundo completo da Fase9 nem ao CMB. As páginas científicas contêm centros publicados, incidentais à leitura de sigmas e definições; esses centros NÃO entram nos cálculos nem geram veredito. Não alegamos cegueira à literatura.

## R-D — dependência em z: taxa local e distância integrada são diferentes

Mapa consultado: d1.fase3bis_d1b_convencao_artigo seq220; d1.fase5_sh0es_01out seq236–242. Os resultados existentes sombra/acumulada não foram repetidos.

[DERIVED, sob FRW plano, equação de continuidade e rho+p>=0] Defina N=ln(1+z). A equação de Raychaudhuri dá dlnE/dN=(3/2)(1+w_eff), logo
I(z)=integral_0^N |1+w_eff|dN=(2/3)lnE(z),
k(z)=exp(beta I(z))=E(z)^(2beta/3), K*=k(z*).
A troca de |1+w| por 1+w usa a hipótese indicada; não estender silenciosamente a fases phantom.

A fonte implementada (motor.py184–211; fundo_gpu.py141–149) usa na leitura acumulada
A(z)=exp(beta[I(z*)-I(z)])=K*/k(z)
e D_M,ac(z)=(c/H0) integral_0^z du/[E(u)A(u)].
Na sombra D_M,s(z)=(c/H0) integral du/E(u)/K*.
Portanto:
Q(z)=D_M,ac/D_M,s = integral k(u)du/E(u) / integral du/E(u).
O mesmo Q vale para a razão de d_L nas duas leituras com o mesmo fator (1+z). Não vale substituir Q por k no ponto final. Para E crescente, 1<=Q<=k(z). No limite pequeno z, k-1~beta Omega_m z e Q-1~beta Omega_m z/2.

| z | k(z)-1 (taxa local) | Q(z)-1 (distância) | 5log10 Q (mag) |
|---:|---:|---:|---:|
|0,5|0,21598%|0,09837%|0,002135|
|1|0,45477%|0,19751%|0,004285|
|1,5|0,67768%|0,28630%|0,006208|
|2,3|0,98363%|0,40433%|0,008762|
|3|1,20663%|0,48783%|0,010567|

[REAL da leitura do código] Na convenção do artigo beta_no_fundo=nao, BAO é calculado do fundo nu e r_drag; o boost acima é aplicado ao canal Pantheon+SH0ES (motor.py215–217). Uma separação k(z)-1 dividida pelo erro de D_H/r_d do DESI **não é** o poder desse motor. Alterar H físico, d_A ou r_d requer outro mapa e outra pré-especificação.

[PODER] Nenhum novo z-score de Pantheon+ foi calculado. O mapa seq241–242 já registra baixa capacidade de separar as duas leituras com os dados usados; seus resultados são históricos. A presente conta corrige o sinal/objeto da previsão, não repete a Fase5. Uma medida efetiva independente de forma em z1 precisaria sigma_mu<=0,000857 mag para separar estas curvas a5sigma com nuisance congelado; covariância/calibração só podem ser tratadas no desenho completo. Não existe aqui previsão datada 2027/2030.

Decisão a encaminhar: distinguir o teste de forma ac/sombra já estudado de um eventual novo observável físico; congelar se K* é a leitura fixa e quais canais podem usar A(z). O fator da face não é a leitura angular por homonímia.

## R-E — dualidade de distâncias

[DERIVED] Escreva d_L,obs=f_L(z)d_L,geom e d_A,obs=f_A(z)d_A,geom. Sob reciprocidade métrica e conservação de fótons, d_L,geom=(1+z)^2 d_A,geom; logo eta_obs=f_L/f_A.

Alternativa A: leitura comum f_L=f_A preserva eta=1, mesmo se cada distância muda.
Alternativa B: somente luminosidade lê a sombra, d_A fica geométrica: eta=1/K*. Na extensão acumulada do motor acima, eta=Q(z)/K*. Se a calibração absoluta for marginalizada, a **forma** normalizada eta(z)/eta(0) seria Q(z), não k(z). Esta é uma tradução condicional, não uma violação física derivada da reciprocidade.

Se houver opacidade física com probabilidade de sobrevivência P_gamma, d_L,obs=d_L,geom/sqrt(P_gamma), eta=P_gamma^(-1/2); para eta≠1 deve-se especificar esse transporte ou outra hipótese de reciprocidade. Uma correção de calibração não prova destruição de fótons. A discussão de mecanismos e sua conexão com temperatura aparece em [Avgoustidis et al.](https://arxiv.org/abs/1112.1862).

[OPEN] K sozinho não decide f_A nem o transporte de fótons. Os 1–2% do catálogo são estimativa herdada, não uma covariance publicada conferida nesta subtarefa; não os transformamos em resultado. Sem mapa único, não há n-sigma TGL calculável. Se o operador adotar B e houver precisão efetiva de1% [cenário, não dado], a forma em z1 seria0,198sigma e em z2,3 seria0,404sigma, antes de nuisance/correlações.

## R-F — temperatura do CMB

A correção do setor gravitacional rho+p não fixa automaticamente a energia/número dos fótons.

Alternativa A [DERIVED sob hipótese explícita]: dephasing na base do mesmo H dos fótons, Lrho=-a[H,[H,rho]], preserva as populações diagonais e Tr(Hrho): Tr(H[H,[H,rho]])=0. Com redshift geométrico usual e expansão adiabática, T=T0(1+z), gamma_T=0. Mudar a taxa H(a) não muda sozinho esta relação T(a). Nem beta nem 4beta/3 implicam gamma_T.

Alternativa B [DERIVED condicional]: transferência de energia Q_gamma tal que dot(rho_gamma)+4Hrho_gamma=Q_gamma. Para espectro de corpo negro rho_gamma proportional T^4,
dot(T)/T=-H+Q_gamma/(4rho_gamma).
O parametrizador T=T0(1+z)^(1-gamma_T) exige gamma_T=Q_gamma/(4Hrho_gamma) constante. Preservar corpo negro impõe também a evolução compatível do número de fótons; uma taxa de dephasing não fornece esse Q_gamma. Outra possibilidade é um mapa de leitura de frequência/temperatura, que igualmente precisa ser especificado.

[OPEN] Não foi localizada nas fontes inspecionadas uma regra que identifique Q_gamma ou esse mapa com K; não se afirma ausência em todo o acervo. Portanto gamma_T=beta seria um postulado adicional, não conclusão da lei existente.

[PODER] A fonte direta [Luzzi et al.](https://arxiv.org/abs/1502.07858) fornece sigma_gamma=0,018 para os104 aglomerados SZ, até z0,94. [Avgoustidis et al.](https://arxiv.org/abs/1511.04335) fornece0,008 no combinado direto+indireto; não contar este segundo como medição independente de dualidade/SNe. Como gamma_T não foi fixado pela TGL neste mapa, o poder numérico TGL é não definido. Sob A a separação desse observável é zero. Não se promete prazo futuro sem previsão e sigma.

## R-G — lentes fortes

[KNOWN/DERIVED] Delta_t=(D_Delta_t/c) Delta_phi, com D_Delta_t=(1+z_l)D_l D_s/D_ls. A fórmula padrão é a do método discutido pelo [TDCOSMO2025](https://arxiv.org/abs/2506.03023v4).

Se D_i=f_i D_i^bg, a leitura de tempo tiver fator f_t e a reconstrução do potencial um fator f_phi, então
D_Delta_t,fit/D_Delta_t,bg=f_t f_phi f_l f_s/f_ls,
H0_fit/H0_bg=(f_t f_phi f_l f_s/f_ls)^(-1),
para o restante da cosmologia fixo.
É indispensável o mapa de DOIS redshifts de D_ls e a relação da leitura de tempo com a reconstrução da lente. A degenerescência de folha de massa já precisa ser marginalizada na análise observacional.

Alternativa A: todos os comprimentos relevantes recebem o mesmo f=1/K*, f_t=f_phi=1; então Hfit=K*Hbg.
Alternativa B: apenas a luminosidade tem a leitura calibrada; geometria angular e atrasos seguem o fundo nu; então Hfit=Hbg.
Ambas são compatíveis com a lei escalar de calibração sem uma ponte adicional. Portanto H0_lens=k(z_s)Hbg não segue de K sozinho.

[PODER condicional] A barra maior publicada é3,9 km/s/Mpc; a fonte inclui Pantheon+ para Omega_m, logo não é inteiramente independente dessa combinação. Se, apenas como hipótese adicional, se usar o endpoint k(z_s) como fator de H, a fiducial H=70 dá proxies0,122sigma (z_s1,5),0,177sigma (z_s2,3),0,217sigma (z_s3). Estes números não selecionam o mapa e não incluem sistemáticas/nuisance. R-G não pode entrar como calibrador de R-A com o mesmo fator antes dessa escolha.

## R-L — S8 e crescimento

[DERIVED algébrico] S8=sigma8 sqrt(Omega_m/0,3). Se sigma8 for mantido e APENAS a quantidade rotulada Omega_m virar (1+beta)Omega_m, S8 muda por sqrt(1+beta)-1=0,599766%. Com S8_ref=0,8, DeltaS8=0,004798. A maior barra KiDS-Legacy publicada é0,021; o proxy condicional é0,2285sigma.

Isso é aritmética de parametrização. O mapa R_eff do motor (181–182) multiplica o parâmetro de deslocamento do CMB por sqrt(1+beta), explicitamente INPUT. Ele não fornece por si só a evolução de P(k,z).

Para previsão de crescimento é preciso, no regime linear aplicável, resolver
D''+[2+dlnH/dlna]D'-(3/2)Omega_m(a)mu(a,k)D=0,
com condições iniciais, relação entre potenciais (slip), mapa de lenteamento e cálculo de sigma8/P(k). Alterar fundo e fonte pode mudar D em direções que a raiz algébrica não captura.

Alternativa A: mesma dinâmica/normalização, apenas releitura de parâmetro (pode nem alterar observável).
Alternativa B: dinâmica modificada fixa por uma ponte perturbativa, produzindo P(k,z) e shear distintos.
[OPEN] Sem B não há previsão de sinal da tensão de shear. [KiDS-Legacy](https://arxiv.org/abs/2503.19441) relata consistência com Planck; não se deve perpetuar como fato universal a antiga frase “S8 está baixo”. Os centros publicados não foram usados para julgar a TGL. A aritmética positiva do cenário não é uma correção física demonstrada nem resolve uma tensão por decreto.

## R-J — relógios e o tempo lido duas vezes

Mapa relogios.v1 seq8,9,99,102,253. Fonte: um.py199223–199289. P1/P2/P3 já foram examinadas; não se repetiu seu ensaio. A identificação do Hamiltoniano modular com o Hamiltoniano de um aparelho é uma condição, não o mesmo objeto pelo nome.

[DERIVED na lei operacional, condicional a tau*=tP] Gamma=.5 beta tau* omega². Recomputação de identidade de unidades em100Hz, com G_CODATA2018: Gamma=1,28036e-40 s^-1; para5sigma seria necessário sigma_Gamma<=2,56072e-41 s^-1. O pequeno desvio do G truncado histórico está registrado no mapa seq102; não muda o alcance.

A v386, um.py193632 e193647–193649, deixa c³ e tau*=kGM/c³ no ramoB do ringdown; “tempo lido duas vezes” conserva o mesmo conjunto fixo e NÃO fornece uma nova escala de laboratório. O c que escala a tríade compacta na pedra é INPUT beta; não confundir com a velocidade dimensional da luz em GM/c³.

Alternativa A: releitura idempotente P²=P não acrescenta evolução.
Alternativa B: composição real de um semigrupo T(t)²=T(2t) apenas dobra o tempo total; não deriva novo tau*, massa ou ganho de ordens de grandeza.
Uma lei física nova exige Hamiltoniano, partição local/global e escala com dimensão de tempo. Escolher massa da Terra/átomo só para aumentar Gamma seria extensão adicional e essas alternativas já constam da varredura v369. RamoB de buraco negro é tratado por F3, não reaplicado a relógio arbitrário.

Resultado F2: nenhuma nova previsão quantitativa de relógio de laboratório foi estabelecida pela frase “duas vezes”. Não é uma parede nem prova de inexistência; é o escopo da fonte consultada e a exigência concreta da ponte faltante.

## R-K — neutrinos: existe m2 condicional; soma já aposentada

Mapa neutrinos.m2.normalizacao seq59,93,98,101,128,136,142,256; neutrinos.massa_v1_e_soma seq161. Conferência primária: um.py2879–2959,4215–4283 e4584–4641.

[DERIVED a partir de INPUTs declarados] m2=beta sin45°*(1eV)=8,507414meV. Sob m1=0 e ordenamento normal, Delta_m21²=m2²=7,2376095e-5 eV².
O próprio código diz: sin45° é POSTULATE (2935–2938),1eV é NORM não derivada (4617); m1~0 e NO condicionam a comparação com sqrt(Delta_m21²). Portanto existe uma previsão restritiva para esses INPUTs, sem ajustar beta; ela não é uma derivação do ordenamento nem da escala absoluta inteira a partir de beta sozinho. A anterioridade/custódia foi corrigida no canônico (2941–2954); preserva-se a lei de novidade de uso, sem depreciação temporal.

A soma usa m3=sqrt(m2²+Delta_m32²) com splitting atmosférico IMPORTADO. **O canônico4275–4277 e4584–4592 já a aposentou como discriminante por decisão D2 de10/08**: a proximidade ao mínimo NH torna o limite cosmológico incapaz, no desenho existente, de separar aquele par. Esta subtarefa não reabre soma, não reutiliza seu limite como evidência independente de beta e não converte0,064eV/95% numa sigma gaussiana.

O [JUNO primário](https://arxiv.org/abs/2511.14593v1) fornece sigma_Delta_m21²=0,12e-5 eV² em59,1dias. Essa é resolução, não distância entre duas previsões. LambdaCDM não fixa um valor único do splitting: não há n-sigma TGL/LambdaCDM calculável só com esse erro. O teste já existente pode tensionar a hipótese m2 fixa conforme refinamentos; sua kill_rule exige DUAS determinações mutuamente autônomas. NuFIT contendo JUNO não é a segunda. A exigência e a limitação das projeções estão nos seq98,128,142. Nenhum novo pull ou veredito foi calculado.

## Resultado operacional e próximos passos

| Rota | Previsão obtida nesta F2 | Estado da análise | Próximo objeto verificável |
|---|---|---|---|
|R-D|Q integral para ac/sombra; números acima|DERIVED condicional; comparação antiga não repetida|mapa adotado, alvo distinto e covariância se novo teste|
|R-E|eta=f_L/f_A;1 ou Q/K* conforme ponte|OPEN mapa único|transporte de fótons e calibração/BAO|
|R-F|gamma_T=0 sob dephasing conservativo; Q_gamma exigido no outro ramo|OPEN identificação física|operador de energia/número e redshift|
|R-G|Hratio=(f_t f_phi f_l f_s/f_ls)^-1|OPEN mapa de lentes|relação de dois redshifts, atrasos e potencial|
|R-L|+0,5998% somente com sigma8 fixo|OPEN dinâmica|P(k,z), slip, mu e condições iniciais|
|R-J|lei canônica sem nova escala|fonte examinada; sem nova previsão|ponte modular/aparelho, sem escolher tau por poder|
|R-K|m2=8,507414meV condicional|canal vivo já existente; soma aposentada|nova determinação autônoma sob frozen vigente|

Não há projeções numéricas atribuídas a2027/2030 sem sigma publicada para o estimador e mapa escolhidos. Os limiares de precisão são critérios de planejamento, não datas. Nenhum gate ou original foi alterado. A coordenação recebe os artefatos para revisão independente e registro de decisões; auto-revisão não fecha a F2 por autoridade própria.


# Errata ao lado — R-G: convenção explícita de f_phi
[DERIVED condicional / OPEN na ponte física] 06/10/2026 UTC. Autor: chatgpt-codex/ordem-018/derivacoes. Responde ao achado F2-REV-01 da revisão adversarial, registrado no mapa seq391, e corrige a ambiguidade da rota seq379. O texto anterior da NOTA_DERIVACOES_F2.md é preservado integralmente como história.

## Convenção adotada e derivação
Para o mesmo par ordenado de imagens, diferenças de potencial não nulas e o mesmo redshift da lente, fixam-se:
- F_D = f_l f_s/f_ls, com D_Delta_t,phys = F_D D_Delta_t,bg.
- Delta_t_phys = D_Delta_t,phys Delta_phi_true/c.
- f_t = Delta_t_obs/Delta_t_phys, logo Delta_t_obs = f_t D_Delta_t,phys Delta_phi_true/c.
- **f_phi = Delta_phi_fit/Delta_phi_true**: potencial reconstruído dividido pelo verdadeiro.
- O ajuste usa Delta_t_obs = D_Delta_t,fit Delta_phi_fit/c.

Igualando as duas expressões do atraso observado:
D_Delta_t,fit Delta_phi_fit = f_t D_Delta_t,phys Delta_phi_true.
Portanto, na convenção agora explícita:
**D_Delta_t,fit/D_Delta_t,bg = f_t F_D/f_phi = f_t f_l f_s/(f_phi f_ls).**
Mantendo fixos os demais parâmetros da geometria de referência, D_Delta_t,bg é proporcional a H0_bg^(-1), e a leitura correspondente é:
**H0_fit/H0_bg = f_phi/(f_t F_D) = f_phi f_ls/(f_t f_l f_s).**

Estas expressões qualificam as linhas74–76 e o resumo R-G na linha132 da versão originalmente revisada. Não há mais um f_phi sem direção definida.

## Reconciliação da expressão histórica
O produto escrito anteriormente, D_fit/D_bg = f_t f_phi F_D, só corresponde à convenção inversa. Se desejado, denote-a agora por g_phi = Delta_phi_true/Delta_phi_fit = 1/f_phi; então D_fit/D_bg = f_t g_phi F_D e H_fit/H_bg = (f_t g_phi F_D)^(-1). Os símbolos f_phi e g_phi não podem ser intercambiados sem a inversão. Isso preserva a expressão histórica com seu alcance explicitado, em vez de apagá-la.

Como controle algébrico de direção: com f_t=F_D=1 e Delta_phi_fit=2 Delta_phi_true, a equação de ajuste exige D_fit=D_phys/2 e H_fit=2H_bg. Não se trata de cálculo observacional ou escolha de modelo pelo dado.

## Impacto delimitado
Os casos anteriores com f_phi=1 mantêm exatamente as relações e números já escritos. Os proxies de endpoint de F2_CALCULOS_CONDICIONAIS.json não variam esse fator e permanecem byte a byte intactos, assim como f2_analysis.py. A presente errata não recalcula integrais, dados, poder, lentes ou covariâncias e não altera o forecast poder_forma.

K(z) sozinho ainda não determina F_D, f_t nem Delta_phi_fit/Delta_phi_true. A ponte física de lentes permanece [OPEN]. A correção de convenção é [DERIVED condicional]; não é aprovação de um mapa físico, veredito ou alteração de gate.

## Rastreabilidade
Revisão lida: ../proveniencia/REVISAO_ADVERSARIAL_F2.md e REVISAO_ADVERSARIAL_F2_FONTES.json. Seus hashes foram recalculados dos bytes nesta correção. Não foram alterados os documentos da revisora.
Antes de cada alteração de documento/recibo existente, fez-se backup imediato de bytes na mesma pasta; gravação temporária, verificação e substituição. O prefixo integral da nota anterior foi conferido contra a cópia e a identidade indicada pela revisão. MANIFESTO_F2.json registra os novos hashes; o recibo do mapa recebe a errata sem apagar a inscrição anterior.
