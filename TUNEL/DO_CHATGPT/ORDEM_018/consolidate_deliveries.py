"""Build traceable local deliverables from checked, conditional calculations."""
from pathlib import Path
import json
from datetime import datetime, timezone
from audit_inputs import safe_write, save_json, file_info

ROOT = Path(__file__).resolve().parent


def link(name, label=None):
    return f'[{label or name}](</{(ROOT / name).as_posix()}>)'


def read(name):
    return json.loads((ROOT / name).read_bytes())


def main():
    original = read('F0_POWER_RESULT.json')
    updated = read('F0_UPDATED_SIGMAS_RESULT.json')
    simons = read('F0_SIMONS_RESULT.json')
    stamp = datetime.now(timezone.utc).isoformat()
    rows = [
        dict(route='R-A', rank='1', name='Razão de Hubble', prediction='K*=E(z*)^(2 beta/3); Hlocal=K*Hbg, sob o mapa universal ratificável', statute='DERIVED condicional / INPUT do mapa', data='R22 sigma 1,04; CCHP TRGB combinado 1,936; TRGB JWST 2,224; JAGB 2,720 km/s/Mpc. H0DN sigma 0,81 é candidato documental adicional.', separation='R22 5,001; TRGB combinado 2,917; TRGB JWST 2,562; JAGB 2,114. H0DN 6,018 apenas sob a compressão universal e demais hipóteses do planejamento.', decision='Fixar fundo sem escada, canais/operadores, covariância conjunta e cinco hipóteses; depois ratificar V1. H0DN requer auditoria da rede antes de entrar.', map='373, 383–388; revisão H0DN em curso', source='FONTES_PUBLICAS.json; FONTES_ATUALIZACAO_F0.json; F0_UPDATED_SIGMAS_RESULT.json'),
        dict(route='R-B', rank='2 (com R-M)', name='Era da radiação / CMB', prediction='delta rho_r/rho_r=4 beta/3; DeltaNeff=0,119466 na equivalência pós-e±', statute='DERIVED condicional ao mapa e fechamento perturbativo', data='Planck+BAO sigma 0,17; P-ACT-LB 0,13; P-ACT-LB-D-He 0,11; não independentes', separation='0,703; 0,919; 1,086, respectivamente. A última já usa BBN.', decision='Ratificar mapa rho+p, tratamento perturbativo e BBN; impedir dupla entrada de beta e dupla contagem de dados.', map='371, 375, 392', source='preregistros/primordial/FONTES_PRIMARIAS.json; FONTES_ATUALIZACAO_F0.json'),
        dict(route='R-M', rank='2 (com R-B)', name='BBN direta', prediction='Proxy S=sqrt(1+4 beta/3); DeltaYp=0,00140708 e Delta log10(D/H)=0,00657979, sob sensibilidades declaradas', statute='DERIVED condicional, não integração BBN exata', data='Aver 2026 sigma Yp 0,0013; Cooke 2018 sigma log10(D/H) 0,0052; teoria/nuisance adicionais', separation='1,082 e 1,265 por canal, antes de teoria/nuisance. Não combinar em quadratura.', decision='Congelar S(T), código/rede nuclear, priors externos independentes de omega_b e tau_n e covariância. Dois observáveis não identificam dois nuisance livres mais o contraste.', map='375, 392', source='preregistros/primordial/CALCULO_SENSIBILIDADES_SIGMAS.json; preregistros/primordial/PREREGISTRO_FASE8_V1_RASCUNHO_ORDEM018.md'),
        dict(route='R-H', rank='3 condicional', name='Sirenes-padrão', prediction='Hsirene=K*Hbg é hipótese de extensão; falta fixar propagação GW / leitura de distância', statute='OPEN na ponte observacional; DERIVED no cenário universal', data='GWTC-5.0, 236 GW, larguras assimétricas 7,5 e 9,4 km/s/Mpc; contém GW170817', separation='0,780–0,623 como proxies gaussianos de largura; não uma análise da likelihood assimétrica', decision='Derivar/fixar distância GW antes de usar como calibrador universal; não somar GW170817 nem subconjuntos ao catálogo.', map='consulta sem rota própria anterior; registro desta entrega', source='FONTES_PUBLICAS_ADICIONAIS.json; F0_ADDITIONAL_POWER.json'),
        dict(route='R-C', rank='não ordenar D antes de instrumento', name='Ringdown ramo B', prediction='delta tau220=-x/(1+x); x=beta [2pi/kappa_hat(chi)] N(chi)', statute='DERIVED no contrato F2b; V1 congelado, teste D pendente', data='D: 14 elegíveis declarados, quatro holds. A31: sigmas/spins de calibração já conhecidos.', separation='D não medido. Em A31, só a geometria do contraste dá 11,383 bruto e 0,742 após c0+kc sigma livres; isto não é forecast nem veredito D.', decision='Operacionalizar nuisance, código IMR só-220, seleção/holds, controles C1–C9, saída cega e custo do piloto. Não fixar c0=0 para recuperar significância.', map='365, 374; atualização documental D em curso', source='preregistros/NOTA_PREREGISTROS_F3.md; VERIFICACAO_INDEPENDENTE_RINGDOWN_SHAPE.json'),
        dict(route='R-D', rank='4 condicional', name='Forma em redshift', prediction='Q(z)=[integral k/E]/[integral 1/E], k=E^(2 beta/3), para acumulada/sombra', statute='DERIVED sob FRW plano, continuidade e rho+p>=0', data='1580 linhas SN sem calibradores na máscara auditada; covariância DESI DR2 de 13 componentes', separation='Mapa implementado A: SN+BAO com amplitudes próprias e Omega_m comum, D=0,164; SN só amplitude D=0,183 e com Omega_m D=0,030. Mapa hipotético B dá 0,294 conjunto após nuisance.', decision='Conservar distinção taxa/integração e decidir quais canais recebem K. Não atribuir sinal beta ao BAO nu do motor A.', map='376, 389–391, 394', source='derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/poder_forma/NOTA_PODER_FORMA.md'),
        dict(route='R-E', rank='sem ranking físico único', name='Dualidade de distâncias', prediction='eta=fL/fA; geometria comum dá 1; luminosidade apenas pode dar Q/K*, forma Q', statute='DERIVED condicional / OPEN no mapa único', data='Mesmo SN/BAO de R-D; os 1–2% herdados não constituem nova covariância verificada', separation='Zero para mapa comum; restante depende do mapa e nuisance. Não reutilizar R-D como evidência independente.', decision='Fixar transporte/conservação de fótons, leituras e calibração; eta=E^(2 beta/3) não segue automaticamente.', map='377, 389–391, 394', source='derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/poder_forma/NOTA_PODER_FORMA.md'),
        dict(route='R-G', rank='sem ranking físico único', name='Lentes e atrasos', prediction='Hfit/Hbg=fphi/(ft FD), FD=fl fs/fls; fphi=DeltaPhi_fit/DeltaPhi_true', statute='DERIVED condicional / OPEN nas leituras', data='TDCOSMO 2025 sigma maior 3,9 km/s/Mpc; uso de Pantheon+ para Omega_m', separation='Endpoint k(zs) hipotético: 0,122–0,217 para zs 1,5–3. Esse endpoint não foi derivado como mapa de lentes.', decision='Fixar geometria de dois redshifts, tempo e potencial; só então admitir ou não a universalidade de R-A.', map='379, 391, 393 (errata)', source='derivacoes/ERRATA_R_G_FPHI.md; derivacoes/F2_FONTES_SHA256.json'),
        dict(route='R-L', rank='sem ranking físico único', name='Crescimento / S8', prediction='sqrt(1+beta)-1=0,599766% se sigma8 permanecer fixo; não é previsão de shear', statute='DERIVED algébrico / OPEN dinâmica', data='KiDS-Legacy sigma maior S8 0,021', separation='Proxy aritmético 0,2285 em S8 fiducial 0,8; sinal físico não determinado', decision='Derivar P(k,z), mu, slip, condições iniciais e operador de lenteamento antes do contraste.', map='380, 391', source='derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/F2_CALCULOS_CONDICIONAIS.json'),
        dict(route='R-F', rank='sem previsão diferente estabelecida', name='Temperatura CMB', prediction='Dephasing na base do mesmo H conserva energia; com redshift geométrico usual e expansão adiabática, T=T0(1+z). Outro ramo exige Qgamma ou mapa de frequência.', statute='DERIVED sob hipóteses / OPEN no ramo alternativo', data='SZ direto sigma_gamma 0,018; combinado direto+indireto 0,008 sobrepõe dualidade/SN', separation='Zero nesse ramo conservativo com redshift usual e adiabaticidade; gamma=beta não derivado', decision='Especificar energia/número de fótons e corpo negro antes de propor gamma não nulo.', map='378, 391', source='derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/F2_FONTES_SHA256.json'),
        dict(route='R-I', rank='consistência / perfil OPEN', name='Piso dos vazios', prediction='Tc[f]=(3/xc^3) integral_0^xc f(x)x^2 dx >= beta; xc=0,25', statute='limite canônico; DERIVED na distinção média/perfil', data='Fontes das funções canônicas e mapa V11 consultados; nenhum catálogo reaberto', separation='Não há contraste de perfil fixado pelo piso; compatibilidade de ambos com desigualdade não separa os modelos.', decision='Localizar/derivar solução radial F_beta ou lei populacional Pi_beta e operador observacional antes de escolher estatístico.', map='395–397; errata do índice seq158', source='derivacoes/R_I_PISO_E_PERFIL.md; derivacoes/R_I_MANIFESTO.json'),
        dict(route='R-J', rank='sem nova escala de laboratório', name='Relógios', prediction='Gamma=.5 beta tau* omega^2; tau*=tP dá 1,28036e-40 s^-1 a 100 Hz', statute='DERIVED condicional; ligação ao aparelho OPEN', data='P1/P2/P3 no mapa consultados, não refeitos', separation='Nenhum novo poder estabelecido. Duas leituras não fornecem outra tau* por si.', decision='Derivar Hamiltoniano/partição/escala física; não selecionar massa pelo ganho desejado.', map='381, 391; relogios.v1 seq8/9/99/102/253', source='derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/F2_CALCULOS_CONDICIONAIS.json'),
        dict(route='R-K', rank='teste restritivo, não LCDM fixo', name='Neutrinos', prediction='m2=beta sin45° vezes 1 eV=8,507414 meV, com ângulo POSTULATE e escala NORM; m1=0 e NO para splitting', statute='DERIVED de INPUTs; não ordenamento derivado', data='JUNO sigma_Dm21^2=0,12e-5 eV^2; kill_rule histórica exige duas determinações autônomas', separation='LCDM não fixa splitting único. Soma já aposentada por D2; não converter limite 95% em sigma.', decision='Preservar teste vigente de m2 e independência das determinações; não reabrir soma.', map='382, 391; neutrinos seq59/93/98/101/128/136/142/161/256', source='derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/F2_FONTES_SHA256.json'),
    ]
    save_json(ROOT/'F0_RANKING_REGISTRY.json', {'created_at':stamp,'status':'INVENTORY_AND_CONDITIONAL_RANKING','observed_centres_used_for_ranking':False,'routes':rows,'remote_execution_request_ids':[], 'prepared_not_dispatched_request_ids':['a4534bcd-8058-48a7-b5fa-34bc046dc46e']})
    intro = f'''# ORDEM 018 — F0: inventário e ranking condicional

[REAL — consolidação local, {stamp}] **R-A (Hubble) é a primeira candidata para completar o contrato discriminante.** H0DN acrescenta uma rede pública de calibradores cuja precisão merece auditoria; não fornece uma observação independente para multiplicar por SH0ES/CCHP. Nenhuma rota recebe nesta entrega um novo veredito discriminante.

Aqui D é a distância gaussiana esperada entre previsões, calculada com incertezas publicadas e hipóteses explícitas. D não é a significância observada nem a probabilidade de rejeição. Para R-A, o desenho congelado usa Hfid=70, Omega_m=0,3, Omega_r=0,00009, z*=1089 e sigma_bg=0,5 km/s/Mpc; não são ajustes aos centros. Beta é calculado por ALPHA_FINE_CODATA_2018 vezes sqrt(e). D usa sigma_contraste=sqrt(sigma_local²+K*² sigma_bg²), com covariância cruzada nula e incerteza de K desprezada neste planejamento. Ambas precisam ser revistas no contrato completo.

O cálculo {link('F0_UPDATED_SIGMAS_RESULT.json')} dá D={updated['h0dn']['expected_separation']:.6f} para sigma H0DN=0,81; a potência gaussiana idealizada a 5 sigma é {100*updated['h0dn']['gaussian_power_at_5sigma']:.2f}%. R22 dá D={original['hubble'][0]['expected_separation']:.6f}, potência {100*original['hubble'][0]['power_at_5sigma_unadjusted']:.2f}%. **Estes números não incluem a liberdade de deslocamentos/calibração das cinco hipóteses, incerteza do mapa, seleção de canais ou erro em K.** Só medem a separação idealizada do par universal sob o desenho fixo. Cinco sigma de separação esperada correspondem a cerca de 50% de potência naquele teste gaussiano, não a certeza de detecção.

## Ranking auditável

As prioridades numéricas abaixo são condicionais. Rotas sem ponte observacional determinada não ganham posição física por um proxy algébrico. Os valores R-B/R-M se sobrepõem; R-D/R-E também. A indicação de prioridade não permite somar suas distâncias em quadratura.

| Rota / prioridade | Previsão e estatuto | Dados e separação esperada hoje | Decisão necessária | Mapa |
|---|---|---|---|---|
'''
    for r in rows:
        intro += f"| **{r['route']} — {r['name']}** / {r['rank']} | {r['prediction']}. [{r['statute']}] | {r['data']} **{r['separation']}** | {r['decision']} | {r['map']} |\n"
    intro += f'''
## 2027 e 2030: não substituir precisão por calendário

Para **todas as 13 rotas**, a documentação auditada não fornece uma previsão numérica ratificada do estimador completo para 2027 ou 2030. Os limiares abaixo são metas de precisão e os cenários publicados mantêm seus próprios horizontes. Não usamos extrapolação de N^(-1/2) ignorando sistemáticas.

- **R-A/R-H:** no desenho ideal acima, D=5 pede sigma_local <= {original['sigma_local_needed_5sigma_given_bg']:.6f} km/s/Mpc. R22 já está nesse limite e H0DN abaixo dele, mas a distinção entre os mecanismos exige a rede/covariância e o fundo independente. Para sirenes ainda não foi verificado um calendário dessa precisão sob o mapa TGL.
- **R-B:** D=5 pede sigma_Neff <= {original['neff']['sigma_needed_5sigma']:.8f}. [Simons Observatory enhanced, v3](https://arxiv.org/html/2503.00636v3), tabela 2, prevê sigma=0,045 para o levantamento inteiro **2025–2034**, incluindo Planck, ruído-meta e erros estatísticos; dá D={simons['expected_separation']:.6f} sob equivalência Neff. Isso não é forecast 2030. O cenário histórico CMB-S4 sigma=0,03 pressupõe a relação de consistência BBN e daria D=3,982; com Yp livre, a referência da F3 fornece sigma=0,09. Não transportar esse sigma para Yp livre ou BBN modificada sem tratamento consistente; a dependência teórica não prova reutilização dos mesmos dados de abundâncias. A [página oficial](https://cmb-s4.org/) registra retirada do apoio DOE/NSF em 09/07/2025 e encerramento ordenado. Não manter CMB-S4 como promessa operacional para 2030.
- **R-M:** antes de nuisances/teoria, os proxies pedem sigma_Yp <= 0,00028142 e sigma_log10(D/H) <= 0,00131596. A melhoria experimental precisa acompanhar rede nuclear e priors externos. Nenhuma data foi certificada.
- **R-C:** custo/poder do conjunto D dependem do instrumento e dos controles. A norma A31 após nuisance não é previsão de D em 2027/2030.
- **R-D/R-E:** o cenário conjunto do mapa A precisaria reduzir a covariância inteira idealizada em desvio-padrão por fator 30,49 para D=5. É um escalonamento matemático, não plano DESI/Euclid nem exigência apenas de número de objetos.
- **R-F/R-G/R-I/R-J/R-K/R-L:** primeiro resolver a ponte ou preservar o teste vigente; não atribuir prazo a uma previsão ainda não especificada.

## Fontes, caminhos e revisão

Os links abaixo localizam os recibos com URLs, arquivos baixados e hashes calculados. A fonte pública contém valores centrais incidentais à consulta; eles não entraram no ranking. Não alegamos cegueira à literatura.

| Canal | Fonte primária e recibo local |
|---|---|
| R-A | [SH0ES R22](https://arxiv.org/abs/2112.04510), [CCHP v3](https://arxiv.org/abs/2408.06153v3), [H0DN](https://arxiv.org/abs/2510.23823), {link('FONTES_PUBLICAS.json')} e {link('FONTES_ATUALIZACAO_F0.json')} |
| R-B | [Planck 2018](https://arxiv.org/abs/1807.06209v4), [ACT DR6 v2](https://arxiv.org/html/2503.14454v2), {link('FONTES_ATUALIZACAO_F0.json')}, {link('FONTE_SIMONS.json')} |
| R-H | [GWTC-5 cosmologia](https://arxiv.org/abs/2605.27227), {link('FONTES_PUBLICAS_ADICIONAIS.json')} |
| R-D/E/F/G/L/J/K | {link('derivacoes/F2_FONTES_SHA256.json')}, {link('derivacoes/poder_forma/FONTES_COVARIANCIAS_METADATA.json')}, {link('derivacoes/NOTA_DERIVACOES_F2.md')} |
| R-C | {link('preregistros/AUDITORIA_PREREGISTROS_F3.json')}, {link('VERIFICACAO_INDEPENDENTE_RINGDOWN_SHAPE.json')} |
| R-I | {link('derivacoes/R_I_FONTES_E_TRECHOS.json')}, {link('derivacoes/R_I_PISO_E_PERFIL.md')} |
| R-M | {link('preregistros/primordial/FONTES_PRIMARIAS.json')}, {link('preregistros/primordial/CALCULO_SENSIBILIDADES_SIGMAS.json')} |

F2 foi submetida a revisão independente: {link('proveniencia/REVISAO_ADVERSARIAL_F2.md')} localizou a ambiguidade de fphi nas lentes, corrigida ao lado em seq393. {link('proveniencia/REVISAO_PODER_FORMA.md')} reproduziu as projeções de forma por GLS independente (51 verificações; diferença máxima D 5,8e-9). Os demais limites não são ratificação de uma previsão física pelo revisor.

Scripts: {link('poder_f0.py')}, {link('derivacoes/f2_analysis.py')}, {link('derivacoes/poder_forma/forecast_shape.py')}, {link('preregistros/primordial/calcular_sensibilidades.py')}. Protocolos prévios e JSONs permitem reproduzir cada número. {link('F0_RANKING_REGISTRY.json')} guarda as 13 linhas estruturadas.

[REAL — orquestração] Três subtarefas locais trabalharam em proveniência, derivações e pré-registros, com revisão cruzada. **Nenhuma chamada nova a executor remoto foi realizada nesta missão.** A unidade MiMo request_id a4534bcd-8058-48a7-b5fa-34bc046dc46e ficou preparada e bloqueada na prévia local de integridade, sem job de execução. ChatGPT/Física não foi utilizado. A fila antiga é outra série ORDEM018 e foi preservada. Este ranking não move kernel, gate ou veredito e não encerra F1/F3/F4.
'''
    safe_write(ROOT/'ENTREGA_018_F0_RANKING.md', intro)

    f2 = f'''# ORDEM 018 — F2: derivações e limites observacionais

[REAL — análise local e revisão independente concluídas no escopo documental/algébrico, {stamp}] As sete rotas solicitadas foram examinadas com estatutos explícitos. O resultado principal é que a distância usa a **integral de k(z)**; temperatura, lentes e crescimento precisam de pontes adicionais para virar previsões observacionais. Uma lacuna localizada é resultado da F2, sem declarar inexistência no acervo inteiro.

O desenvolvimento completo, fontes com linhas, duas alternativas por lacuna e cálculos estão em {link('derivacoes/NOTA_DERIVACOES_F2.md')}. O manifesto {link('derivacoes/MANIFESTO_F2.json')} fixa os artefatos; beta é sempre recalculado de alpha_CODATA2018 vezes sqrt(e). Não se executou o canônico nem se abriu dado para novo veredito.

| Rota | Equação / previsão | Estatuto e sensibilidade |
|---|---|---|
| R-D | k=E^(2 beta/3); Q=(integral k/E)/(integral 1/E). Q−1=0,19751% em z=1 e 0,40433% em z=2,3, na fiducial de baixo z da nota. | [DERIVED condicional] Taxa no ponto final não é distância integrada. No mapa implementado, BAO permanece nu. |
| R-E | eta=fL/fA: 1 se leitura comum; Q/K* se luminosidade apenas, forma normalizada Q. | [OPEN mapa] A lei K não seleciona fA nem transporte de fótons. R-D e R-E não são dados independentes. |
| R-F | Tr(H[H,[H,rho]])=0 para dephasing na base do mesmo H. Com redshift geométrico usual e expansão adiabática, T=T0(1+z); uma gamma_T constante exigiria Qgamma=4 gamma_T H rho_gamma. | [DERIVED sob essas hipóteses / OPEN outro ramo] sigma_gamma direto 0,018; combinado 0,008 sobrepõe SN/dualidade. A identidade de traço sozinha não deriva a lei cosmológica; gamma=beta não derivado. |
| R-G | FD=fl fs/fls; fphi=DeltaPhi_fit/DeltaPhi_true; **Hfit/Hbg=fphi/(ft FD)**. | [DERIVED condicional / OPEN ponte] sigma maior TDCOSMO 3,9; depende de Pantheon+ para Omega_m. A errata seq393 prevalece sobre a expressão ambígua anterior. |
| R-L | Com sigma8 fixo: sqrt(1+beta)−1=0,599766%; em S8=0,8, Delta=0,004798. | [DERIVED aritmético / OPEN dinâmica] Proxy Delta/0,021=0,2285. Falta P(k,z), mu, slip, normalização e operador observacional; não determina sinal da tensão física. |
| R-J | Gamma=.5 beta tau* omega²; tau*=tP e 100 Hz dão 1,28036e−40 s⁻¹. | [DERIVED condicional] Duas leituras não derivam outra escala dimensional. P1/P2/P3 não foram reabertas. |
| R-K | m2=beta sin45° vezes 1 eV=8,507414 meV; m1=0, NO dão Dm21²=7,2376095e−5 eV². | [DERIVED de POSTULATE/NORM] sigma JUNO=0,12e−5; LCDM não fixa splitting. Soma aposentada por D2 preservada; teste vigente pede determinações autônomas. |

## Verificação numérica da forma

{link('derivacoes/poder_forma/NOTA_PODER_FORMA.md')} utiliza somente redshifts, tipos e covariâncias publicadas, sem centros observados. Foram conferidas as identidades das matrizes; a amostra SN tem 1580 **linhas de curvas de luz**, não necessariamente 1580 objetos independentes. A projeção por Cholesky/SVD remove amplitudes e a tangente de Omega_m.

- Mapa A (implementado): SN D=0,183 com amplitude livre; D=0,030 com amplitude e Omega_m. BAO não recebe sinal beta, mas restringe Omega_m comum: conjunto D=0,164, com amplitudes próprias.
- Mapa B (hipotético comum): conjunto D=0,294 após nuisance; eta=1. Este cenário não foi adotado como previsão da TGL.
- A covariância cruzada SN–BAO foi assumida zero neste planejamento. A hipótese e os nuisance congelados delimitam os números.

Estas são separações gaussianas esperadas condicionais, não z-scores observados nem probabilidades de detecção. Não se promete um calendário Euclid/DESI-Y5 com base em reduzir matematicamente todas as barras.

## Revisão e alcance da conclusão

{link('proveniencia/REVISAO_ADVERSARIAL_F2.md')} conferiu as derivações e encontrou uma convenção ambígua de lentes. {link('derivacoes/ERRATA_R_G_FPHI.md')} a resolve: se o potencial reconstruído dobra com os outros fatores unitários, Dfit cai à metade e Hfit dobra. A expressão antiga foi preservada como história e recebe a correção ao lado. Os casos fphi=1 não mudam.

{link('proveniencia/REVISAO_PODER_FORMA.md')} realizou 51 verificações independentes; diferença máxima nas distâncias gaussianas 5,8e−9. A análise inicial tem 54 verificações; o forecast, 57. São verificações diferentes, não um placar de comprovação física.

Mapa: R-D/E/F/G/L/J/K seq376–382; forma seq389–390; revisão seq391; errata seq393; revisão de forma seq394. Nenhum executor remoto nesta subtarefa, request_ids despachados=[]; assistência Work ausente. **F2 está entregue como investigação das sete rotas, incluindo seus itens OPEN; não declara fechadas as pontes observacionais.**
'''
    safe_write(ROOT/'ENTREGA_018_F2_DERIVACOES.md', f2)
    p=ROOT/'ENTREGA_018_F1_HUBBLE.md'
    marker='<!-- ORDEM018_F1_H0DN_DOCUMENTARY_UPDATE -->'
    if marker not in p.read_text(encoding='utf-8'):
        addition=f'''

{marker}
## Adendo de fontes e identificação — {stamp}

[KNOWN — fonte primária / DERIVED — cenário de precisão] A rede [H0DN](https://arxiv.org/abs/2510.23823), com [código público](https://github.com/StefCas789/H0DN), publica sigma H0=0,81 km/s/Mpc. A precisão dá separação idealizada 6,018 no desenho fixo do F0; não há fit ou novo veredito. A rede compartilha componentes com SH0ES/TRGB/JAGB e não pode ser multiplicada como observação independente deles. Recibos em FONTES_ATUALIZACAO_F0.json e F0_UPDATED_SIGMAS_RESULT.json.

[DECLARADO — revisão documental da gerência em curso] A revisão oficial desta tarefa irmã encontrou uso de pseudoinversa na covariância global, seguida de inversão de A^T C^+ A. O contrato SPD da nota anterior precisa admitir suporte singular com teste de posto/identificabilidade antes de qualquer ajuste. Um deslocamento só-Cefeidas deve entrar nos módulos selecionados, não em todo H0DN. Variantes leave-one-out são análises do mesmo acervo, não novas medidas independentes. A confirmação por linhas/hashes ficará no relatório específico; não executamos o código remoto.

Permanecem pendentes a reprodução conjunta Fase4/5, as cinco evidências, a covariância cruzada entre canais e a ratificação do V1. O teste histórico SN-only já reproduzido não atende sozinho esses itens. O conjunto de insumos de F1 continua revisão local sem assistência Work; a prévia MiMo foi recusada antes de envio.
'''
        safe_write(p, p.read_bytes()+addition.encode('utf-8'))
    print(json.dumps({'written':['ENTREGA_018_F0_RANKING.md','F0_RANKING_REGISTRY.json','ENTREGA_018_F2_DERIVACOES.md','ENTREGA_018_F1_HUBBLE.md'],'routes':len(rows)},ensure_ascii=False))


if __name__ == '__main__':
    main()
