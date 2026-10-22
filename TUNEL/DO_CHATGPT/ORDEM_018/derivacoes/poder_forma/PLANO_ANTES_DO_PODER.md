# PLANO DE PODER DA FORMA — R-D / R-E
[INPUT — recorte da coordenação ORDEM_018; DERIVED condicional] Autor chatgpt-codex/ordem-018/derivacoes. Este arquivo será gravado e hasheado antes do primeiro cálculo de poder. Não produz veredito nem usa centros observados.

## Consulta prévia e obstáculos
Mapa MCP consultado antes: discriminante.ordem018.f2.r_d/r_e (seq376/377); d1.fase5_sh0es_01out (seq236–242); bao_cmb.d10.degenerescencia_do_fundo; supernovas.pantheon_errata_cosmologica (seq34/149). Não repetir fits antigos. Esta conta nova é um forecast de template com somente redshift/covariância e nuisances analíticos, solicitado pela coordenação.
Obstáculo mapa físico: alternativa A manter BAO do fundo nu do motor e corrigir só luminosidade; alternativa B transportar universalmente distâncias/rateios, preservando dualidade. Medir ambas CONDICIONALMENTE, sem escolher pelo dado.
Obstáculo amplitude: alternativa A fixar amplitudes (diagnóstico superior); alternativa B projetar intercepto SN e amplitude BAO independentes; alternativa C acrescentar a tangente Omega_m compartilhada. Comparar a informação restante. Não interpretar amplitude fixa como forma.
Obstáculo proveniência da covariance Pantheon: alternativa A conferir bytes no release público primário; alternativa B qualificar resultado como condicionado ao arquivo local se a fonte não puder ser conferida. Não promover DECLARADO em silêncio. Divergência é bloqueio para equivalência, não licença para trocar arquivo após ver sinal.
Obstáculo independência SN/BAO: alternativa A resultados separados; alternativa B bloco conjunto com crosscovariance ZERO explicitamente assumida. Sem alegar que essa independência foi medida.

## Hipóteses e derivação congeladas
FRW plano; E(z)^2=Omega_m(1+z)^3+Omega_r(1+z)^4+1-Omega_m-Omega_r; rho+p>=0; beta=ALPHA_FINE_CODATA_2018*sqrt(e) em runtime. Alpha é lido do trecho científico já capturado do um.py, nunca importar o programa. Fiduciais de planejamento: H0=70 km/s/Mpc, Omega_m=0.3, Omega_r=0.00009, c=299792.458 km/s, r_d=147 Mpc. r_d é somente INPUT dimensional explícito, não centro de BAO nem ajustado. A pequena radiação substitui a ilustração anterior Or=0 para alinhar o fundo ao F0 da coordenação; z<=2.33 não envolve uma conta de CMB.
k(z)=E(z)^(2beta/3).
D_M,s=(c/H0)/Kstar * integral_0^z du/E(u).
D_M,ac=(c/H0)/Kstar * integral_0^z k(u)du/E(u).
Q(z)=D_M,ac/D_M,s=integral k/E / integral 1/E.
Kstar cancela na razão; seu valor não será calculado nem ajustado nesta conta.
Sinal SN: s_mu(zHD)=5log10 Q(zHD); o fator heliocêntrico em dL=(1+zHEL)DM cancela. Mudança constante de M/H0/Kstar é intercepto.
Mapa A (implementado no motor no recorte lido): BAO não recebe k/Q; s_BAO=0. Se dA fica geométrico, eta_ac/eta_s=Q, enquanto a normalização de eta não é identificada sem calibrador. Isto não prova violação física de reciprocidade.
Mapa B (extensão adicional hipotética): D_A=(D_M/(1+z)) e D_L=(1+z)D_M com o mesmo transporte; eta=1. Razões ac/s: DM=Q, DH=k, DV=Q^(2/3)*k^(1/3). Fator global1/Kstar absorvido pela amplitude. Não chamar esta extensão de previsão já derivada do motor.

## Fontes e seleção
Pantheon metadata: C:/IALD/observaveis_tgl/tgl_data_cache/pantheon/Pantheon+SH0ES.dat. Ler somente zHD, zHEL, IS_CALIBRATOR; ignorar valores m_b_corr, MU_SH0ES, CEPH_DIST e demais centros. Máscara zHD>0.01 e IS_CALIBRATOR==0, sem ajuste após cálculo.
Covariance STAT+SYS local: C:/IALD/projetos_pyhton/acom/tgl_data_cache/pantheon_covariance.dat. Primeiro N=1701, depois N² termos. Registrar hash e dimensões.
DESI: C:/IALD/Artigo/teste_acustico_beta_tgl_v1/_originais/desi_gaussian_bao_ALL_GCcomb_mean.txt (somente primeira e terceira colunas: z e tipo; não converter a segunda) e covariance correspondente desi_gaussian_bao_ALL_GCcomb_cov.txt.
Proveniência primária consultada: https://github.com/PantheonPlusSH0ES/DataRelease/tree/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR e https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2. Registrar checksums lidos e recibos da comparação remota; não copiar centros para resultados.

## Medida
Distância gaussiana esperada D=sqrt(s^T W s); não é significância observada, veredito, fator de Bayes ou probabilidade de detecção. Covariance fixa no fiducial. W=C^-1-C^-1 J(J^T C^-1 J)^-1 J^T C^-1 implementado com Cholesky e SVD/QR de J branqueada (sem inversão explícita). Interceptos/amplitude marginalizados analiticamente com prior plano; Omega_m em aproximação tangente sem prior, não fit aos centros.
SN: J=1; segunda versão J=[1,dmu_bg/dOmega_m].
BAO B: y_bg=[DV/rd,DM/rd,DH/rd] no fiducial, s=y_bg*(ratio-1); J=y_bg; segunda versão J=[y_bg,dy_bg/dOmega_m]. Fonte A: s=0.
Conjunto A/B: covariance bloco-diagonal; J=[intercepto SN, amplitude BAO, derivada Omega_m compartilhada], com também versão sem Omega_m. Os dois interceptos são independentes por ausência de calibração externa H0,M,rd. Não importar prior Planck/SH0ES/JUNO nem centro qualquer.
Derivada por diferenças centrais h=1e-4 e h/2; quadratura Gauss-Legendre n=64 e128 por z; tolerâncias comparadas. Se não convergir reportar e refinar antes de interpretação. Covariance exige finite, simetria até1e-6 absoluto, diagonal positiva e Cholesky da parte simétrica. Registrar assimetria, sem repair de autovalor.
Controles: beta=0 implica sinal zero; sinal SN constante e BAO proporcional a y_bg devem desaparecer na projeção; D não cresce ao aumentar espaço nuisance. Calcular alvo ideal de melhoria uniforme de sigma 5/D somente se D>0, como escala matemática sem prazo ou promessa de realizabilidade.
Publicar arrays z, tipo, template, derivadas e checks; nenhuma realização de dado/centro. Resultado JSON + script + nota + manifesto hashes. Não executar um.py/motores, não chamar provedores, não alterar originais. Registrar ao mapa após exame.
