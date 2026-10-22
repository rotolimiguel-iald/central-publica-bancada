# F8.2.NU2 — ponte entre escala, dephasing e neutrinos

Autor: codex-gerente-tgl / nu2_theory_sources; unidade reivindicada pelo coordenador, evento 618. [REAL documental] Fontes pinadas no INVENTARIO_FONTES_NU2_20261009.json (15 fontes). Nenhum original, memória, quadro ou Bancada foi alterado; nenhum programa científico original foi executado ou importado, e nenhum conjunto observado foi aberto.

## Reaproveitamento

Nós Vivo F7.2/F8.2 consultado. F7.2 está FECHADA no grafo e quadro: já examinou n=-2, limites, v369 e a ponte em matéria OPEN. F8.2 contém a rota histórica Grande Atrator/Chandrasekhar. As consultas inicialmente falharam por acesso e depois concluíram mediante elevação somente de leitura. Não se reabriu a entrega anterior.

## Resultado decisivo: beta0 e beta(chi) têm papéis distintos

TheCouplingRunsBoundedBelow.lean:22–26 preserva beta0 de Thomson na fronteira; beta(chi) é leitura de bulk. Identificação alpha físico=sech(chi/2) é INPUT/ONTO, running QED KNOWN, escala de cada rito OPEN nesse arquivo. Não há chi(E,n,T,Ye) microscópico nessa pedra.

A Ponte Einstein Cartan Miguel.tex:1367–1371 declara expressamente que o coeficiente beta do dephasing Gamma=(beta/2)tau_star*omega² é independente de omega, sem correção logarítmica. Isso permanece no um.py vivo:165419–165421. O adendo v388:166219–166232 e runtime:194754–194764 preservam fronteira constante/bulk corrente. O Atlas:35126 registra a decisão de 07/10: todo rito cobra beta0 e na lei dephasing só entra beta0 (remissão, verificada contra fonte primária).

**Substituir beta0 por beta(chi(E)) na taxa de dephasing não é a previsão vigente encontrada.** É contrafactual/extensão a justificar e reconciliar. Isso permite pesquisar efeitos de bulk no plasma, mas não os torna consequência já calculada da v388.

O limite beta<=sqrt(e) é formal; couplingOfAlpha requer beta<1 (TheWholeIsOne:55–62). Usar sqrt(e) numa conta é envelope matemático deliberadamente generoso, não extremo admitido por esse contrato físico.

## Taxa e parâmetros existentes

Em segundos: Gamma_ij=(beta0/2)*tau_star*omega_ij²*Kfac, omega_ij=Delta_m²_ij/(2 E hbar). No script gamma_tgl (tgl_neutrino_decoherence.py:54–58), tau está em eV^-1 e Gamma em eV; a conversão tau_s/hbar está em tgl_decoherence_contour.py:66–70. beta é fixo. Kfac é argumento (default 1), não resultado de uma geometria calculada.

O snapshot Custo:3307 identifica K em Kfac=(K/Kstar)^beta como **Kretschmann**, distinto do gerador modular K_partial. Kstar precisa ter dimensão de K. Não foram localizados nos scripts um Kstar determinado, uma geometria estelar ou uma normalização por trajetória. tau_star é INPUT; tau_star=tP é hipótese da comparação v369, não derivação universal. A partição MODULAR_LAB_BRIDGE_OPEN permanece.

A F7.2 já estabeleceu que limites dos artigos com taxas iguais não são limites diretos da TGL com taxas proporcionais a (Delta_m²_ij)². O JUNO Gamma21=Gamma31 não é automaticamente o mesmo modelo. As conversões antigas de tau_star, inclusive 7,8e-10 s, estão corrigidas ao lado. n=-2 requer vácuo, gaps fixos e tau/Kfac independentes de E.

## Derivada completa, condicional

Se um novo modelo escolher beta(E), tau(E), r(E)=K/Kstar>0, com gaps fixos no vácuo, a identidade é:

n_eff = -2 + dln(tau)/dln(E) + beta_prime*(1/beta + ln(r)) + beta*dln(r)/dln(E),

com beta_prime=d beta/dln(E) e beta_prime/beta=-(1/2)tanh(chi/2)*dchi/dln(E).

A expressão simplificada -2-(1/2)tanh(chi/2)*chi_prime exige tau e Kfac constantes. Se Kfac=r^beta e r!=1, não se deve omitir a derivada do expoente. Na leitura vigente beta0 constante: n_eff=-2+dln(tau)/dln(E)+beta0*dln(r)/dln(E). Em matéria o primeiro termo é 2*dln|gap_H|/dln(E), não necessariamente -2.

## Ponte ao interior estelar: localizada e aberta

No escopo delimitado, não foi localizada uma derivação TGL de delta G_F, captura eletrônica, colisões, emissividade ou EOS ligando chi à anã branca. Isso é ausência de localização, não prova de ausência no acervo inteiro.

Há candidatos do Tratado (escalar não mínimo e Ricci-FF/MP²), mas a errata assinada de 19/09:23–29 fixa xi=1/6, explicitamente xi!=beta. A menção a 1 eV como escala eletrofraca em secao_03_particulas:452–461 não fornece uma taxa de captura.

TheDensityIsTransport:31–37 distingue estrutura demonstrada de identificação ONTO com neutrinos e marca OPEN qual grandeza realiza densidade/transporte. TheStation:166–177 é um teorema em matrizes finitas de invariância modular, sem amplitude ou elemento de matriz fraco. Ambas são peças existentes, sem conter o matching estelar procurado.

A equação histórica de geodésica no Tratado:426–429 tem conexão no lado esquerdo. xi_nu->0 anula a força extra à direita; não apaga a conexão. Logo ausência de lenteamento/Shapiro não segue desse limite sozinho. É diagnóstico da equação, sem alteração do original.

Em matéria, L proporcional a H_total e L proporcional a H_vácuo não são escolhas equivalentes. Dephasing com H_total preserva sua energia média sob hipóteses usuais; H_vácuo com potencial não comutante requer balanço da energia entre setores. Fixar operador, estado, perfil, colisões e relógio antecede extrair fuga/luminosidade.

## Próximo degrau

Fixar fronteira beta0 ou nova interação de bulk; construir Hamiltoniano e dissipador físico em matéria; determinar tau/Kfac/estado/perfil; projetar na resposta do detector. Para ligar a massa/luminosidade, derivar termo de colisão/emissividade e seu efeito em Ye/energia. Só então uma likelihood compatível permite medir poder. Nenhum sigma observado foi calculado nesta nota.

## Escopo e histórico técnico

Busca: Atlas/índice/Nós Vivo; v388/contrato; busca lexical TGLExt por neutrino/tau/capture/Urca; scripts F7.2; Tratado seções 01/03; Ponte canônica; Custo snapshot; errata assinada. Não é varredura exaustiva de todo o acervo.

A primeira chamada apply_patch ficou sem conclusão e foi interrompida; só build_inventory.py foi observado criado. A primeira execução falhou antes de escrever resultado por faixa 33–43 num arquivo de 42 linhas; r2 preservou o script e corrigiu isso. A segunda falhou antes do resultado por faixa 15–49 num arquivo de 45 linhas; r3 preservou ambas e corrigiu a faixa. R3 concluiu exit 0 e gerou o inventário. Esta nota é arquivo novo distinto da nota cuja escrita tinha ficado pendente; não se alegou sucesso da chamada interrompida.
