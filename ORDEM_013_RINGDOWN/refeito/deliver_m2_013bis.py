"""Close C4 as a nonblind conditional measurement, preserving failed support gates."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,statistics,math,sys
B=Path(__file__).resolve().parents[1];D=B.parent/'TUNEL/DO_CHATGPT';I=B.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=B/'bis/M2_DELIVERY_MANIFEST.json'
if '--verify' in sys.argv:
    d=json.loads(manifest.read_bytes())
    for p,h in d['files'].items():
        if sha(Path(p))!=h:raise ValueError('Changed '+p)
    print('PASS',len(d['files']));raise SystemExit
files={}
def read(n):p=B/n;files[str(p)]=sha(p);return json.loads(p.read_bytes())
def new(p,s):
    if p.exists():raise FileExistsError(p)
    t=p.with_name(p.name+'.tmp');raw=s.encode()
    with t.open('xb') as f:f.write(raw)
    if t.read_bytes()!=raw:raise ValueError('Write mismatch')
    t.replace(p);files[str(p)]=sha(p)
def cite(p):files[str(p)]=sha(p);return f'[{p.name}](<{p.as_posix()}>) SHA256 `{sha(p)}`'
now=datetime.now(timezone.utc).isoformat();opening=D/'ENTREGA_013BIS_ABERTURA_operador.md'
tab=read('bis/F2_ALL_READING_TABLES_v2.json');gauss=read('bis/F2_INDEPENDENT_GAUSSIAN_DENSITY.json');clock=read('bis/F2_FREE_CLOCK_EXTENDED_v2.json')
old=read('cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json')['stacks']['3.0'];traj=read('C2_TRAJECTORY_RECOVERY.json')
null=next(c for r in traj['rows'] if r['reading']=='R-A' for c in r['comparisons'] if c['detector_noise']=='SYNTHETIC_COLORED_OU_PLUS_WHITE')
sem=statistics.stdev(f['dtau'] for f in null['fits'])/math.sqrt(null['N'])
rb=next(r for r in read('C4_220_INITIAL.json')['rows'] if r['reading']=='R-B')
g=next(r['lnB_gaussian2D'] for r in gauss['rows'] if r['reading']=='R-B')
r31=next(r for r in tab['rows'] if r['dataset']=='GWTC5_31' and r['reading']=='R-B')
lin=next(r for r in tab['rows'] if r['dataset']=='GWTC5_31' and r['reading']=='R-LIN')
common=f'''\n\nData UTC {now}. Abertura SHA256 `{sha(opening)}`. Axiomas: N/A — sem Lean; teoremas novos: 0, nenhum fonte Lean emitido. Nenhum gate, memória ou canônico alterado.\n'''
positive=f'''[REAL documental/numerical — NÃO-CEGO; KNOWN na literatura, OPEN na causa do deslocamento]

# Adendo C4 — delta-tau positivo

{tab['positive_medians_31']} de 31 medianas são positivas. O diagnóstico gaussiano ponderado tem centro {r31['observed_center']:.8g} e sigma {r31['sigma']:.8g}; não é o posterior hierárquico da LVK. O HPD da RG no diagnóstico KDE comum é {r31['GR_HPD']:.8g}. Predições locais negativas se afastam desse deslocamento positivo comum e produzem razões de densidade negativas; isso não identifica a causa física nem calibra uma exclusão.

Ao lado, sem combinar estratos: V2 da casa, início 3 ms, delta={old['delta_tau']:.8g} ± {old['sigma']:.8g}, poder B={old['power_B']:.8g}. Os eventos podem se repetir nos catálogos; não se multiplicam esses resultados.

Hipóteses não escolhidas: sistemática de forma de onda/consistência inspiral–ringdown [KNOWN como possibilidade discutida, OPEN como explicação destes dados]; viés do estimador em baixo SNR [REAL no exemplo sintético abaixo]; seleção [KNOWN como efeito discutido pela LVK, não quantificado por esta entrega]; física nova [CONJECTURE, não conclusão].

Controle sintético antigo, preservado: R-A efetivamente nulo, SNR {traj['GR_reference_SNR']}, N={null['N']}, média delta={null['mean_dtau']:.9g} ± {sem:.9g} (erro padrão amostral), mediana {null['dtau_05_50_95'][1]:.9g}. Ruído OU+branco sintético e modelo/estimador escolhidos: não é medição do viés do catálogo nem substitui as injeções LVK.

GWTC-3 §VIII.1.2, trecho integral pertinente relido no HTML: os autores apontam excesso positivo de amortecimento combinado, discutem assimetria do prior, correlações, ruído imperfeito e amostra limitada. Isso não autoriza escolher uma causa. GWTC-5, seção pSEOBNR, linhas 4431–4671 da extração lida: modelo populacional gaussiano 2D; a comparação de hipermédia conjunta e a de quatro hiperparâmetros têm estatísticas distintas; seleção favorável a tempos de amortecimento positivos não está incorporada. GWTC-4 TGR III, trechos de injeções e resultados hierárquicos lidos, também distingue catálogos simulados de evidência sobre eventos reais.

O hierárquico LVK é [KNOWN] de conferência, ao lado do produto condicional de razões; não são o mesmo estimador nem se multiplicam. Não se anuncia leitura integral de artigos: foram lidas as seções indicadas.

Fontes: {cite(B/'cache/literature/gwtc3_article_v3.html')}; {cite(I/'medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt')}; {cite(I/'medicao_da_ampliacao/B_catalogos/gwtc4_tgr3.txt')}. Fontes numéricas e hashes estão no manifesto desta entrega.
'''+common
new(B/'C4_ADENDO_DTAU_POSITIVO.md',positive)
selection='''[REAL — comparação dos resultados; DECLARADO na cronologia do auditor; seleção posterior NÃO-CEGA]

# Adendo C4 — GWTC-3, 18 versus 10

Os 18 produtos foram combinados antes de consultar a seleção final de dez. O auditor registra 23:29 → 23:30; esta entrega preserva essa atribuição, sem fabricar um carimbo imutável a partir de texto editável. A seleção é posterior à visualização de resultados, portanto NÃO-CEGA. O primário documental adotado é a Tabela 13 do artigo, anterior à bancada: doze listados menos duas exclusões dos autores = dez. Os dezoito continuam controle separado e nunca são somados aos dez.

| Leitura | ln B, 10 | ln B, 18 | Cruza -ln100 com 10 / 18? |
|---|---:|---:|---|
'''
for name in [r['reading'] for r in tab['rows'] if r['dataset']=='GWTC3_10']:
    a=next(r for r in tab['rows'] if r['dataset']=='GWTC3_10' and r['reading']==name);b=next(r for r in tab['rows'] if r['dataset']=='GWTC3_18' and r['reading']==name)
    selection+=f"| {name} | {a['lnB']:.10g} | {b['lnB']:.10g} | {a['lnB']<-math.log(100)} / {b['lnB']<-math.log(100)} |\n"
selection+='''
R-LIN cruza o limiar com dezoito e não com dez. O veredito físico permanece INCONCLUSIVE_SYSTEMATICS, pois a cláusula relativa da RG reprova nas duas seleções. A escolha documental não apaga esse efeito nem converte a seleção em cega.

'''+cite(I/'auditoria_da_gerencia/aud_5_protocolo.txt')+'\n'+cite(B/'C4_GWTC3_SELECTION.json')+common
new(B/'C4_ADENDO_GWTC3_18_vs_10.md',selection)
fiche=f'''[REAL — ficha C4; medida NÃO-CEGA INCONCLUSIVE_SYSTEMATICS]

Existiam C4_CATALOG_220.json::rows, C4_CATALOG_COMBINATION.json::catalog, C4_GWTC3_*::catalog/selection, C4_PYRING.json::rows e C4_FREE_CLOCK.json::rows. Reusados posteriores existentes, resultados/priors e seleção documentada. Novos: tabela 10×6, guardas de cobertura, gaussiana 2D independente, suporte ESS da cauda de relógio, arquivos RD/QNMRF e inspeção de aplicabilidade, adendos positivos/seleção e licença por arquivo. Não há nova PE nem multiplicação entre métodos/eventos repetidos.

NÃO PAGO: corte de relógio sustentado pelos dados (ESS insuficiente), mapeamento de realização, correção de seleção calibrada e disponibilidade conjunta df/dtau/spin no pacote GWTC4 examinado. RD não tem posterior livre220 apropriado ao mesmo ln B; justificativa independente fornecida, não número inventado.

Reprodução: scripts refeito/summarize_f2_tables_013bis_v2.py, measure_f2_density_clock_013bis.py e correct_f2_clock_support_013bis.py em cópia isolada. Conferência sem rerun: deliver_m2_013bis.py --verify. Fontes e builders no manifesto. Abertura `{sha(opening)}`; axiomas N/A — sem Lean.
'''
new(B/'REAPROVEITAMENTO_C4.md',fiche)
m2=f'''[REAL — NÃO-CEGO; C4 fecha como medida condicional INCONCLUSIVE_SYSTEMATICS, não confirmação]

# ENTREGA 013 M2 — confrontação com os produtos publicados

| Critério F2 | PAGO / NÃO PAGO, escopo e prova |
|---|---|
| Dez leituras × seis conjuntos | PAGO: 60 linhas únicas JSON/CSV, com ln B, bandas, delta, sigma, z, HPD, motivo e estatuto. Guardas recusam ausência de cálculo em vez de completar com zero. |
| Escopo 220 e modos superiores | PAGO documental: todo ln B de catálogo vale no setor 220 condicional com modos superiores de Kerr; 440 fixo na RG em 32/33 eventos (HIGHER_MODE_DEVIATIONS_FIXED_TO_GR). Efeito de liberar440 NÃO PAGO aqui, E4.2. |
| Jackknife e peso máximo | PAGO por leitura/seleção; métricas de ln B e de informação são separadas. Nenhuma evidência repetida é multiplicada. |
| Estimador independente | PAGO: gaussiana2D nos mesmos draws; C4_VALIDATION é controle de quadratura do mesmo KDE, não densidade independente. |
| Delta positivo e literatura | PAGO no adendo com quatro hipóteses não escolhidas; V2 da casa separado e seções primárias relidas. NÃO PAGO identificar a causa física ou corrigir seleção. |
| GWTC3 18/10 | PAGO: duas tabelas lado a lado, primário documental e efeito do ajuste posterior dito. Cronologia do auditor explicitamente DECLARADA. |
| GWTC4 TGR III | PAGO localizar release DCC e inspecionar texto/inventário. NÃO PAGO mesmo ln B: arquivo examinado remete a draws individuais externos e não contém joint df/dtau/spin por evento verificado. Não declarar inexistência de release. |
| RD e QNMRF | PAGO: download/pinos/checksums, inventários. RD inspecionado por cético: Kerr220 fixo, livre221 não é livre220; mesmo ln B não aplicável, null. QNMRF só listado, sem desserializar pickle. |
| Injeção LVK | PAGO extração local e esquema: uma injeção com/sem44, não curva de SNR. Interpretação/calibração é E1.3, não se inventa cobertura a partir de duas análises. |
| Relógio livre | PAGO recomputar dois priors e estender grade além do teto antigo. NÃO PAGO corte sustentado: todos os cruzamentos -ln100 têm ESS<100; data_supported_cut=null. Estabilidade de quadratura não valida cauda da densidade. |
| Emenda e contrato | PAGO: emenda NÃO-CEGA declara ESS100/status técnicos; revisões independentes encerram omissões e guardas, preservando lacunas físicas. |

GW250114, R-B: gaussiana2D ln B={g:.9g}; KDE conjunto central={rb['lnB_joint_spin_curve']:.9g}, controles de banda até {max(x['lnB_joint'] for x in rb['bandwidth']):.9g}; bootstrap 2,5/50/97,5%={rb['lnB_bootstrap_025_50_975']}. Assim, |ln B| é aproximadamente menor que0,1, com sinal indeterminado entre estimadores. Bootstrap do mesmo estimador não resolve incerteza de modelagem da densidade.

GWTC5_31, R-LIN: ln B={lin['lnB']:.10g}, jackknife [{lin['jackknife_lnB_min']:.10g}; {lin['jackknife_lnB_max']:.10g}], maior fração absoluta de ln B={lin['max_abs_lnB_fraction']:.8g}. R-B: maior fração absoluta={r31['max_abs_lnB_fraction']:.8g}. A maior fração de informação inversa da variância é {lin['max_information_fraction']:.8g}; portanto “nenhum peso>13%” não pode ser usado genericamente. Sem a cláusula relativa de RG, R-LIN cruzaria a regra de exclusão do setor220 condicional. Com a regra registrada, HPD_RG={lin['GR_HPD']:.9g}>0,95: INCONCLUSIVE_SYSTEMATICS.

## Relógio livre e parede de suporte

'''
for r in clock['original_priors']:m2+=f"Prior {r['prior']} [INPUT]: ln B livre={r['ln_evidence_free_clock_over_GR']:.9g}, quantil95 de tau_source={r['quantiles']['0.95']['tau_source_s']:.9g}s, condicionado aos limites declarados.\n\n"
for r in clock['curves']:m2+=f"Banda {r['bandwidth_multiplier']}: cruzamento bruto q={r['first_lnB_minus_log100_crossing_q']:.9g}, corte sustentado={r['data_supported_cut']}.\n\n"
m2+='''Os priors originais e o estendido não foram recortados/renormalizados para esconder cauda. O número do cruzamento é diagnóstico da aproximação, não limite físico. Os próprios quantis dependem do prior e da validade da normalização.

## Tabela completa

| Conjunto | Leitura | ln B | banda min/max | delta | sigma | z diagnóstico | HPD RG | veredito |
|---|---|---:|---|---:|---:|---:|---:|---|
'''
for r in tab['rows']:m2+=f"| {r['dataset']} | {r['reading']} | {r['lnB']:.7g} | {r['lnB_bandwidth_min']:.7g}/{r['lnB_bandwidth_max']:.7g} | {r['delta_L_weighted']:.7g} | {r['sigma']:.7g} | {r['z']:.7g} | {r['GR_HPD']:.7g} | {r['verdict']} |\n"
m2+='''
Nos zeros analíticos PROP/coerente, trata-se do cenário sub-resolução solicitado, com mapeamento físico OPEN; não de identidade universal. R-GLOBAL tem identidade relacional condicionada. PyRing sigma é proxy gaussiano do intervalo5–95%, não desvio-padrão amostral; catálogos usam diagnóstico inverso da variância, não posterior hierárquico. O CSV companheiro carrega essas ressalvas e hash do JSON.

## Reprodução, falhas e artefatos

Tentativas preservadas: dependência h5py ausente no Python bundled, distro WSL incorreta e normalização de caminhos corrigidas antes da inspeção; console cp1252 falhou ao imprimir HTML, relido com UTF-8; primeira tabela tinha guarda defeituosa e omitia estatutos no CSV, ambas versões preservadas. Relógio bruto inicialmente omitia ESS da cauda; v2 preserva números e reprova o suporte. Não foi rodada PE nova, nem escolhida uma leitura física.

'''
names=['bis/F2_ALL_READING_TABLES_v2.json','bis/F2_ALL_READING_TABLES_v2.csv','bis/F2_INDEPENDENT_GAUSSIAN_DENSITY.json','C4_VALIDATION.json','bis/F2_FREE_CLOCK_EXTENDED_v2.json','bis/F2_CLOSING_REVIEW.md','bis/F2_C6_CLOSING_REVIEW.md','bis/F2_RD_APPLICABILITY_REVIEW.md','bis/F2_RD_APPLICABILITY_REVIEW.json','bis/F2_ARCHIVE_DOWNLOADS.json','bis/F2_CONTROL_EXTRACTION.json','bis/F2_CONTROL_SCHEMAS.json','bis/F2_GWTC4_RELEASE_SEARCH.json','bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.md','REGISTRO_C4.json','bis/REGISTRO_C4_EMENDA_013BIS.json','C4_EMENDA_TECNICA_013BIS.md','C4_ADENDO_DTAU_POSITIVO.md','C4_ADENDO_GWTC3_18_vs_10.md','REAPROVEITAMENTO_C4.md','cache/MANIFESTO_DOWNLOADS_013BIS_v2.json','refeito/summarize_f2_tables_013bis_v2.py','refeito/measure_f2_density_clock_013bis.py','refeito/correct_f2_clock_support_013bis.py']
for n in names:m2+='- '+cite(B/n)+'\n'
m2+=f'''\nVerificação nesta máquina: `C:\\Python314\\python.exe -B "{Path(__file__)}" --verify`. Para repetir cálculos, usar cópia isolada com os scripts citados e ambiente /opt/lal_env/bin/python -B. Não executar notebooks ou pickles dos releases.\n'''+common
new(D/'ENTREGA_013_M2_C4_fechamento.md',m2)
files[str(opening)]=sha(opening);files[str(Path(__file__))]=sha(Path(__file__))
new(manifest,json.dumps(dict(utc=now,files=files),indent=2,ensure_ascii=False)+'\n')
print('DELIVERED',sha(D/'ENTREGA_013_M2_C4_fechamento.md'))
