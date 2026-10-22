# F8.2.SN1 — complemento: Planck, potencial e reconciliação de ξ

Autor: codex/sn_tgl_readonly, por delegação de codex-gerente-tgl. 09/10/2026. Complemento novo ao inventário; os arquivos anteriores ficam intactos. Total: 15 fontes centrais distintas incluindo o inventário-base.

**[REAL documental]** O Tratado, `secao_01_fundamentos.tex:580`, escreve `L_acop=beta/M_P² R_mu_nu F^mu_rho F^nu_rho`. A linha 584 define **M_P=sqrt(hbar c/G)**, a massa de Planck não reduzida. Logo uma estimativa condicional desse operador deve conservar essa normalização e dizer qual invariante/curvatura caracteriza a estrela. O texto chama o termo de forma mais geral, mas esta consulta não encontrou uma prova da base completa de operadores ou matching. Classificá-lo como candidato da fonte, não como exclusividade estabelecida.

**[REAL documental; reconciliação necessária]** Nas linhas 234, 266 e 284, o Tratado usa sinal negativo e identifica `xi=beta`. A errata assinada por Luiz Antonio Rotoli Miguel em 19/09/2026, na cópia custodiada pinada no JSON, conserva o sinal negativo mas especifica **xi=1/6 conforme, não beta**; beta entra pela ação modular e pela fonte `beta K_boundary Psi`. Portanto não transferir `xi=beta` para a nova EOS por silêncio. O operador RicciFF/Planck² é distinto de xi R|Psi|²: a errata tampouco estabelece seu matching em matéria densa.

**[REAL documental / OPEN para modelo estelar]** O potencial livre da linha 259 é `V=½m0²|Psi|²`; o regime de condensação da linha 261 acrescenta `lambda|Psi|⁴/4`. A estabilidade do potencial é mencionada, mas não determina sozinha valores únicos de m0 e lambda, nem o estado/sua densidade numa anã branca. Uma realização condensada requer fixar isso pela teoria e resolver as condições do estado. O nome superfluidez não supre essa especificação.

**[DERIVED condicional]** Uma estimativa de escala de `beta R/M_P²` pode testar se este candidato é observacionalmente relevante sob as normalizações escolhidas. Ela não deriva um deslocamento luminoso ou de massa; pode resultar em supressão extrema. Isso não elimina outros mecanismos (EOS, composição/capturas ou transferência radiativa) que exijam derivação própria.

**[KERNEL, alcance]** TheNonMinimalCoupling trata de canto algébrico não minimal. Sua docstring distingue a leitura ontológica do acoplamento. O nome não cria uma ponte para a ação do campo escalar.

Os hashes dos arquivos completos e das faixas estão em `LOCAL_NMC_RECONCILIATION_20261009.json`. Esta etapa leu fontes e calculou hashes; não executou o programa científico, não abriu curvas de luz/catálogos observados, não alterou originais, memória, quadro, mapa ou gate.
