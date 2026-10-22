# F2 — plano anterior ao cálculo de sensibilidade

[INPUT] ORDEM_018, catálogo R-D/E/F/G/L/J/K. Autor: chatgpt-codex/ordem-018/derivacoes. Sem ajuste, sem abertura de dado para veredito e sem execução do um.py. Consulta inicial ao mapa concluída; seq em mapas_consultados.json. Resultados antigos não serão reexecutados.

## Árvore de alternativas antes da medida

1. Mapa distância incerto: A ler motor.py e artigo/canônico; B derivar separadamente leitura sombra e acumulada; C manter mapas físicos de BAO/lentes como condicionais se não constarem da implementação. Não identificar K de um ponto com integral de distância.
2. Dualidade/temperatura sem mapa: A conservação de fótons, geodésicas e dephasing de energia; B transferência de energia/número ou mapa instrumental distinto. Demonstrar dependências; não escolher B para ampliar poder.
3. Crescimento sem dinâmica: A apenas transformação algébrica do parâmetro S8; B equação perturbativa completa com mu(a,k), slip e condições iniciais. Não chamar A de previsão de shear.
4. Relógios sem nova escala: A consultar protocolo P1/P2/P3 existente; B conferir c³/tempo duas vezes na v386 e ramo B. Não escolher massa externa ou tau pela sensibilidade. Sem medida P1/P2/P3 nova.
5. Neutrinos: A consultar m2 vivo; B consultar soma/ordenamento e supersessão. Rota aposentada é resultado da leitura, não convite para nova execução.
6. Fonte indisponível: A caminho canônico leitura restrita; B MCP mapa com fonte/seq; C fonte primária pública por URL exata. Falha vai ao registro, nunca vira ausência absoluta.

## Cálculos previamente especificados

Usar beta = alpha_CODATA_2018 * sqrt(e), alpha lido da fonte um.py. Fundo ILUSTRATIVO plano matéria+Lambda: Omega_m=0.3, H0=70, sem ajuste aos alvos e sem reivindicar previsão cosmológica completa. Baixo z <=3; sem radiação nesta ilustração. Variar Omega_m=0.25/0.3/0.35 como sensibilidade de fundo declarado, não ajuste.

E(z)=sqrt(Omega_m(1+z)^3+1-Omega_m).
k(z)=E(z)^(2 beta/3).
Q(z)=integral_0^z [k(u)/E(u)]du / integral_0^z [1/E(u)]du.
dL_acumulada/dL_sombra = Q. Diferença de magnitude=5log10 Q.
Calcular em z=0.1,0.5,1,1.5,2.3,3; Simpson composto n=2000 e4000; tolerância absoluta do refinamento 1e-10. Zero beta dá1; 1<=Q<=k(z) para z>0; z→0 dá1. Não importar motor canônico.

Crescimento: somente sqrt(1+beta)-1 sob sigma8 fixo; incremento dimensional ilustrativo S8_ref=0.8. Sigma publicada KiDS-Legacy +0.016/-0.021; divisão pela maior barra como proxy otimista (fundo tratado fixo). Não computar tensão contra centro observado. Nenhuma trajetória futura com ano sem sigma prospectiva verificável.
Temperatura: sigma_gamma direto SZ Planck0.018 (arXiv1502.07858); combinado0.008 (arXiv1511.04335) contém distâncias e hipóteses de opacidade, só cenário condicional. Não inferir gamma=beta.
Lentes: sigma_H0 maior3.9 km/s/Mpc (arXiv2506.03023); se aplicável hipótese endpoint k(z_s) calcular H0_ref*(k-1)/3.9 e identificar NÃO derivada para lentes.
Relógios: não repetir medições; como identidade de unidade, Gamma=.5beta*tP*(2pi*f)^2 em f=100Hz; requisito de poder sigma_Gamma<=Gamma/5. tP de hbar,G,c (CODATA2018).
Neutrino: calcular apenas previsão m2=beta*sin45°*1eV e dm21=m2² sob m1=0,NO. Sem comparar a centros, sem reabrir soma. Sigma_dm21=0.12e-5 eV² (JUNO2511.14593) é resolução, não separação de rival. LambdaCDM não fixa dm21: não existe n-sigma TGL-vs-LambdaCDM calculável deste sigma isolado.

## Portão

Nenhum número abaixo será declarado poder discriminar enquanto faltar mapa do observável. Frases de precisão disponíveis não são vereditos. Sem nova chamada de provedor nesta subtarefa; request_ids=[]; revisão independente cabe à coordenação/gerência.
