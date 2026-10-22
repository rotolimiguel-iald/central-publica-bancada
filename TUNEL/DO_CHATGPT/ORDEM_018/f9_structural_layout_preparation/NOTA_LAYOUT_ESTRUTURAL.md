# Layout estrutural de fundo F9

[REAL — projeção documental, sem centros] O JSON fornece a API ordenada de16componentes: primeiro Planck R, l_A, omega_b_h2; depois as13linhas DESI na ordem do arquivo pinado no T4. A origem foi localizada pelo RESOLUTOR_F9, sem adivinhar nomes.

Duas rotas foram examinadas: reutilizar metadados/código existentes ou projetar somente rótulo e redshift do catálogo pinado. O código T4 resolve ordem CMB, unidades e denominador BAO, mas recebe redshifts/rótulos do arquivo externo. Por isso usou-se a segunda rota apenas para essas duas colunas.

O extrator lê e hasheia os bytes completos de T4_desi_mean.txt. A expressão regular captura somente a primeira e a terceira colunas; o token central é não capturado, não decodificado, não convertido nem escrito. Não se alega que o arquivo inteiro nunca foi lido. ENTRADAS_HISTORICAS_E_COVARIANCIAS.json também foi lido em bytes, mas não parseado como JSON: somente o token lexical de alpha foi extraído. A covariância DESI foi apenas hasheada, sem valores parseados.

A ordem BAO começa por DV em0.295; segue DM/DH em0.510,0.706,0.934,1.321,1.484; termina em z2.33 com DH e depois DM. Os textos decimais originais são preservados no JSON. Não substituir por redshifts aproximados da DR1 ou pela lista low_z_controls do piloto.

Os rótulos históricos *_over_rs são divididos por r_drag em T4_reproduzir.py:99–100. Portanto a API explicita rdrag, sem trocar por rstar. As16componentes são adimensionais; distâncias e réguas anteriores às razões são em Mpc. O bloco CC histórico do T4 não integra este layout de3+13.

R e l_A usam DM_star e rstar no redshift térmico de recombinação derivado pelo fundo. Esse redshift depende dos parâmetros e fica null até o motor produzir sua previsão. omega_b_h2 é parâmetro de densidade, não uma medida em um bin de redshift. O z_lei histórico1089.95 é fixo, separado, utilizado em E(z_lei); não substitui zstar nem zdrag.

ALPHA_FINE_CODATA_2018 foi lida na linha25 do pipeline histórico admitido. Seu pin coincide com o inventário histórico; o mesmo token consta do input T4 e é consumido na linha74 do reprodutor. A representação e a linha integral constam do JSON. Beta permanece alpha*sqrt(e) em runtime, sem literal beta ou cálculo nesta unidade. O acesso default ao original da linha alpha foi negado; a leitura elevada posterior foi estreita, somente hash/linha, sem execução ou importação.

Nenhum centro, tabela CAMB, solver, controle, hipótese real, veredito, memória compartilhada, download ou modelo remoto foi executado/alterado. A estrutura resolve a lacuna de labels/redshifts/origem de alpha; não certifica a precisão do fundo ou autoriza sua execução. O script de extração é documental e recusa sobrescrever suas saídas.
