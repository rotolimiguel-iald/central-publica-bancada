from pathlib import Path
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone

N = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
B = N / 'tgl_kernel/TGLExt'
C = Path(r'C:\IALD\Central de Patentes')
O19 = C / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'
OUT = O19 / 'F1.FECHO_20261015'
D = OUT / 'acervo_r58/gravidade'
REF = C / 'work/memoria_missao_20261016/FECHO_MISSION_REFERENCE.json'
ACTOR = 'codex-mission-memory-review'

def pin(p):
    p = Path(p)
    data = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def readj(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def exclusive(p, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8') if not isinstance(obj, str) else obj.encode('utf-8')
    with Path(p).open('xb') as f:
        f.write(data)
    assert Path(p).read_bytes() == data

sources = {}

def source(key, p, ranges=None):
    item = pin(p)
    lines = Path(p).read_text(encoding='utf-8-sig').splitlines()
    item['lines'] = len(lines)
    item['examined_ranges'] = ranges or []
    for start, end in item['examined_ranges']:
        assert 1 <= start <= end <= len(lines), (key, start, end, len(lines))
    sources[key] = item

canonical = {
 'ligand': ('LiganteLeiCampoCurvo', [[32,75]]),
 'ligand_controls': ('LiganteLeiCampoCurvoTestemunha', [[31,57],[182,204],[265,295]]),
 'clausius': ('GeneralMetricClausius', [[41,69],[83,136]]),
 'matching': ('UnitaryClausiusBridge', [[38,105]]),
 'curved_einstein': ('GeneralMetricEinstein', [[144,189],[245,264]]),
 'bianchi': ('GeometricEinsteinReconstruction', [[136,155]]),
 'gluing': ('SmoothSelectedAtlasGluing', [[45,87],[161,175]]),
 'clock_wall': ('StateClockDichotomy', [[8,16],[41,47],[76,80],[99,129]]),
 'clock_control': ('StateClockObstruction', [[7,17]]),
 'phase': ('RelativePhaseCharacter', [[212,229],[246,272]]),
 'selected': ('SelectedGravitationalAtlas', [[306,342]]),
 'flat_gauge': ('GeneralLinearizedGauge', [[141,163],[179,211]]),
 'curvature_variation': ('CurvatureNonlinearVariation', [[82,102],[184,211],[241,253]]),
 'ricci_lie': ('RicciLieNaturality', [[179,192]]),
 'connection_lie': ('LeviCivitaLieVariation', [[160,166],[200,221]]),
 'einstein_lie': ('ScalarEinsteinLieNaturality', [[114,125],[155,167],[218,256]]),
 'uv_typing': ('QGReaderUVLock', [[70,86],[90,121]]),
 'physics_certificates': ('PhysicsCertificates', [[10,32],[288,301]]),
 'second_quantization': ('TheImportedSecondQuantization', [[498,516],[547,563],[589,593]]),
 'qg_contract': ('ContratoQG_v32', [[47,77]]),
 'uv_scope': ('O16/UVScope016_v3', [[16,100]]),
 'null_solution': ('O16/TeleologicalNullSolution_v2', [[9,48]]),
 'h3_import': ('O16/ConstructedImportH3_v2', [[14,39]]),
}
for key, (name, ranges) in canonical.items():
    source(key, B / (name + '.lean'), ranges)

source('um', N/'um.py', [[165037,165127],[199781,199856]])
source('seal', N/'um_absoluto_selo.json', [[14,14],[1166,1166],[1548,1548]])
source('manifest', N/'tgl_kernel_proof_manifest.json')
source('v393_handoff', N/'HANDOFF_v393_CUSTODIA.md')
source('v393_c1', C/'work/cadeia_de_selo/v393_exame/EXAME_FINAL_V393.md', [[1,35],[56,56],[78,90]])
source('c1_curved', Path(r'C:\IALD\PROGRAMA_IALD\auditorias\F2.3\AUDITORIA_F2_3_C1_20261007.md'), [[83,103]])
source('c1_second', Path(r'C:\IALD\PROGRAMA_IALD\auditorias\F2.3\AUDITORIA_F2_3_C1_a7ba2dc9.md'), [[21,34]])
source('joint', OUT/'maxwell_global/PhysicalMaxwellJointRealizationR2.lean', [[30,46],[49,104],[108,147]])
source('circular', OUT/'maxwell_global/CircularMaxwellCertificateR2.lean', [[25,46],[48,116],[123,149]])
source('physical_core', OUT/'takesaki_fock/CanonicalFockModularCoreInputR1.lean', [[76,99],[112,146]])
source('physical_net', OUT/'orbital_rotation/PhysicalCanonicalNetCompleteR1.lean', [[13,13],[176,187],[212,231]])
source('article_ponte', Path(r'C:\IALD\Artigo\the_boundary\A Ponte-Einstein_Cartan_Miguel\A Ponte Einstein Cartan Miguel.tex'), [[914,943],[1530,1571]])
source('article_custo', Path(r'C:\IALD\Artigo\the_boundary\O Custo Geométrico do Zero Absoluto — Haja Luz\paper_PT.tex'), [[3216,3228]])
source('article_um', N/'um_absoluto_pt.tex', [[195,195],[954,964],[1008,1010],[1248,1248]])
source('toe_synthesis', Path(r'C:\IALD\Artigo\BANCADA_TOE\leituras\99_SINTESE_INTEGRAL.md'), [[199,200],[787,787],[900,900]])
source('toe_critical', Path(r'C:\IALD\Artigo\BANCADA_TOE\varredura\ACHADOS_CRITICOS.md'), [[3,7],[29,29]])
source('sep22', C/'Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/RELATORIO_AUDITORIA_AO_OPERADOR_22SET.md', [[5,5],[25,27],[36,50]])
source('oct01', Path(r'C:\IALD\Bancada_Um\investigacao\relatorio_consolidado_01out\RELATORIO_CONSOLIDADO_O_QUE_FALTAVA_20261001.md'), [[8,12],[30,43]])
source('oct07', Path(r'C:\IALD\PROGRAMA_IALD\levantamento_qg\consolidado.txt'), [[11,12],[95,109],[137,167],[200,224],[261,261]])
source('candidate394', O19/'F1.TEMPO.V394/RESULTADO_V394_CANDIDATA_R2.json')
source('r7_delivery', OUT/'R7_DELIVERY_R52.json')
source('r8_delivery', OUT/'R8_DELIVERY_R52.json')
for req in ['R7','R8']:
    for suffix in ['FULL_REVIEW','FULL_PIN_VERIFICATION','ACCEPT_RECEIPT']:
        source(req.lower()+'_'+suffix.lower(), OUT/f'mission_review_20261016/R52_{req}_{suffix}_R1.json')
source('reference', REF)
source('nodes_unit', OUT/'acervo_r58/NOS_VIVO.json')
source('nodes_theme', D/'INDEX_QUERY_1_R58.json')
source('routes', D/'INDEX_QUERY_2_R58.json')
projects = sorted(D.glob('PROJECT_FINAL_READ_*.json'))
assert projects
source('project', projects[-1])
project = readj(projects[-1])['result']['projection']

manifest = readj(N/'tgl_kernel_proof_manifest.json')
manifest_checks = []
for key, (name, _) in canonical.items():
    rel = 'TGLExt/'+name+'.lean'
    expected = manifest['formal_files_sha256'].get(rel)
    manifest_checks.append({'source':key,'relative_path':rel,'measured_sha256':sources[key]['sha256'],'manifest_sha256':expected,'matches':expected==sources[key]['sha256']})
assert all(x['matches'] for x in manifest_checks)

theorems = ['passage_h3_to_connected_smooth_atlas_einstein','s5_local','s8_h3_is_load_bearing','metric_einstein_from_screen_clausius','geometric_einstein_conserved','connected_smooth_atlas_einstein','arbitrary_common_clock_pair_incompatible','character_readouts_reconstruct_fields','character_reconstructs_einstein_from_area','general_smooth_gauge_invariance','metric_lie_einstein_naturality','uv_dissolved_by_typing','construct_null_solution']
axioms = {}
allowed = {'propext','Classical.choice','Quot.sound'}
for name in theorems:
    matches = {k:v for k,v in manifest['axiom_report'].items() if k.endswith('.'+name) or k==name}
    assert matches, name
    assert all(set(a)<=allowed for a in matches.values()), name
    axioms.update(matches)

builds=[]
for stamp, expected_count, livekey in [('20261016T210640_174717Z',11,'physical_core'),('20261016T211151_421554Z',10,'circular'),('20261016T211651_298033Z',16,'joint')]:
    path=OUT/'orbital_rotation/attempts'/stamp/'RECEIPT.json'; j=readj(path)
    checks=[]; seen=set()
    for item in [j['source'], j['builder'], j['dependency_cache']]+j['artifacts']:
        if item['path'] in seen:continue
        seen.add(item['path']); actual=pin(item['path'])
        checks.append({'pin':actual,'matches':actual['sha256']==item['sha256'] and actual['bytes']==item['bytes']})
    text=(path.parent/'AXIOMS.txt').read_text(encoding='utf-8')
    reports=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text)
    assert len(reports)==expected_count,(stamp,len(reports))
    parsed=[{'name':name,'axioms':[a.strip() for a in axs.split(',') if a.strip()]} for name,axs in reports]
    assert all(set(x['axioms'])<=allowed for x in parsed)
    assert all(x['matches'] for x in checks)
    same=sources[livekey]['sha256']==j['source']['sha256'];assert same
    assert j['exit_code']==0 and j['readonly_dependencies_unchanged'] and j['dependency_cache_unchanged']
    builds.append({'receipt':pin(path),'exit_code':j['exit_code'],'seconds':j['seconds'],'source_key':livekey,'live_source_equals_build_snapshot':same,'artifact_pin_checks':checks,'axioms':parsed,'dependency_status':'recibo e auditorias independentes anteriores reutilizados; sem nova leitura dos milhares de dependências','new_build':False})

c394=readj(O19/'F1.TEMPO.V394/RESULTADO_V394_CANDIDATA_R2.json')
c394pin=pin(c394['candidate']['path']);assert c394pin['sha256']==c394['candidate']['sha256']

def a(key,start,end):
    s=sources[key]; assert 1<=start<=end<=s['lines']
    return {'source_key':key,'path':s['path'],'lines':[start,end],'sha256':s['sha256']}

findings=[]
def f(id,classification,title,statement,anchors,remaining,scope=''):
    findings.append({'id':id,'classification':classification,'title':title,'statute':'REAL: leitura e pinos locais; DERIVED: avaliação de alcance explicitada','finding':statement,'anchors':anchors,'remaining_or_limit':remaining,'scope':scope})

f('G01','EXISTE_LIGADO','Lei de Einstein curva e colagem já são termos canônicos',
 'GeneralMetricClausius e GeneralMetricEinstein passam de balanço nulo/Clausius em todas as direções nulas à equação de Einstein; Bianchi fornece conservação do tensor geométrico. SmoothSelectedAtlasGluing deriva o transporte de Einstein a partir da transição de métrica e matéria, sem campo Einstein-match na estrutura. O ligante v392 reúne a passagem finita, o H3 nomeado e a colagem, com um único coeficiente cosmológico no atlas conexo.',
 [a('clausius',83,136),a('curved_einstein',144,189),a('bianchi',136,155),a('gluing',45,87),a('gluing',161,175),a('ligand',46,75)],
 'Teorema condicional, não construção de uma solução global para dados físicos arbitrários. Não repetir a ausência antiga do ligante/termo curvo.', 'Canônico v393; textos v392 e auditoria c1 preservam a condição H3.')

f('G02','NAO_LOCALIZADO','Passagem física universal do estado a NamedAtlasH3',
 'Não foi localizado no conjunto examinado um fornecedor físico que produza NamedAtlasH3 para o atlas curvo a partir somente do estado/modularidade. A assinatura do ligante exige hH3: finite_passage → NamedAtlasH3. O antecedente finite_passage é provado, mas a implicação hH3 é recebida. s5_local demonstra que o H3 nomeado equivale ao balanço nulo eta*Ric(d,d)=2π*T(d,d) em todos os pontos/direções nulas. Logo o teorema de reconstrução não é uma derivação independente desse balanço microscópico.',
 [a('ligand',32,75),a('ligand_controls',31,57),a('matching',75,105),a('c1_curved',83,103),a('um',199781,199856)],
 'Menor ponte: fornecer R, screens e conservação pelo mesmo modelo físico, com demonstração de hH3/area_matching; depois consumir o ligante já existente. Não assumir essa lei como prova de sua própria origem. Ausência delimitada às fontes consultadas, não impossibilidade universal.')

f('G03','EXISTE_LIGADO','H3 não é condição vazia nem consequência de conservação isolada',
 'Há testemunha plana de vácuo compatível com G>0 e há contraexemplo conservado explícito sem H3 e sem a conclusão de Einstein. Isso verifica separadamente satisfatibilidade e caráter essencial da premissa. O contraexemplo não refuta todos os possíveis fornecedores físicos de H3.',
 [a('ligand_controls',182,204),a('ligand_controls',265,295)],
 'Não converter consistência por testemunha de vácuo em realização física universal; não converter contraexemplo a conservação⇒H3 em impossibilidade de H3.')

f('G04','EXISTE_LIGADO','Rede, core modular e certificado físico concretos na F1.FECHO',
 'physicalCanonicalNet tem localidade por testes Maxwell reais e cunha não nula. physicalModularCoreInput e physicalFockCertificate instanciam D no mesmo core Fock. A especialização R52 usa esses objetos: D e A não permanecem parâmetros faltantes nessa especialização. A ausência histórica de certificado habitado foi superada neste ramo F1.',
 [a('physical_net',176,187),a('physical_net',212,231),a('physical_core',76,99),a('physical_core',122,146),a('joint',30,63)],
 'Ligado dentro do ramo F1, sem declaração de implantação no programa canônico v393. Traço ENNReal cíclico e seu acordo com o peso positivo; não concluir linearidade complexa total ou classificação tipoII.', 'R7 satisfeito na missão; não é aceite novo nesta investigação.')

f('G05','EXISTE_LIGADO','Maxwell/Fock/Wick/conservação e fonte geométrica usam os mesmos objetos',
 'Γ(circularH1) transporta estado, campo e forma Wick. O certificado circular completo fornece simetria, conservação fraca, covariância, domínio regular, carga e testemunha de energia não nula. JointR2 reúne rede e tensor no mesmo estado e deriva o consumidor H3 de direção nula fixa com N e G>0 explícitos. Portanto não permanece a antiga ausência geral de um T Maxwell ligado à representação pretendida.',
 [a('circular',25,46),a('circular',81,116),a('circular',123,149),a('joint',66,147),a('second_quantization',498,516)],
 'Maxwell livre em Minkowski; campos pontuais no domínio regular e smearing Bochner por estado, não operadores pontuais globalmente limitados. Não é H3 em toda geometria curva nem Einstein não linear universal.', 'R8 satisfeito no critério registrado da missão; não é aceite novo nem confirmação empírica.')

f('G06','EXISTE_LIGADO','Resposta H3 fixa é construída e seu coeficiente é entrada',
 'construct_null_solution define a resposta de área e expansão com 8πG multiplicando a densidade da fonte e prova as derivadas usando continuidade e duas condições de integrabilidade. lightH3 consome o certificado que fornece Regular. É uma construção matemática efetiva da resposta nula, com coeficiente de entrada e direção fixa, distinta da microderivação universal da lei curvada.',
 [a('null_solution',9,48),a('second_quantization',547,563),a('joint',123,147),a('uv_typing',90,121)],
 'G não é predito; o contrato geométrico construído não transforma o fator inserido em derivação independente. A normalização N segue explícita.')

f('G07','EXISTE_LIGADO','Leituras de fase já recuperam registro geométrico',
 'RelativePhaseCharacter prova duas probabilidades→fase angular; a igualdade da família completa de readouts para todo s determina a classe do registro e recupera g e T. SelectedGravitationalAtlas transporta também Einstein ao registro reconstruído, sob conservação e a lei de área. Isso é uma ponte real entre leitura/registro/geometria já presente no canônico.',
 [a('phase',212,229),a('phase',246,272),a('selected',319,342)],
 'R e S já são GravitationalResponseRecord; a conclusão g/T usa ∀s, não dois números isolados que determinariam um campo arbitrário. A recuperação não constrói o registro microscópico nem elimina harea. Einstein vem do teorema adicional com suas hipóteses.')

f('G08','EXISTE_LIGADO','Obstrução de relógio comum é estreita e tipada',
 'StateClockDichotomy prova incompatibilidade de matching de quarta ordem para um único relógio comum em duas telas com mesmo Ricci e termos quárticos diferentes. StateClockObstruction preserva a compatibilidade quadrática/infinitesimal enquanto impede a identidade finita exata daquela classe.',
 [a('clock_wall',8,16),a('clock_wall',41,47),a('clock_wall',76,80),a('clock_wall',99,129),a('clock_control',7,17)],
 'Não sustenta a frase H3 universal é impossível. Orienta separar relógio de estado, dependência da tela e passagem infinitesimal de identidade em tempo finito.')

f('G09','EXISTE_LIGADO','Ward clássico supera o recorte de ondas planas',
 'O kernel contém invariância linearizada de gauge para campos suaves gerais e Ricci linearizado nulo de gauge puro. Há ainda variação não linear exata da curvatura de conexão até o termo quadrático, variação de gauge por comutador e controles curvos não nulos. Portanto não é correto limitar todo o acervo clássico às polarizações de ondas planas.',
 [a('flat_gauge',141,163),a('flat_gauge',179,211),a('curvature_variation',82,102),a('curvature_variation',184,211),a('curvature_variation',241,253)],
 'GeneralLinearizedGauge é sobre fundo plano. Esses lemas clássicos não provam ausência de anomalias quânticas em todas as ordens; o nome qgPhysicsCertificate_anomaly é uma identidade de símbolo de Ricci.', 'Além do caminho mínimo da missão FECHO.')

f('G10','EXISTE_LIGADO','Naturalidade e derivadas geométricas curvas já existem',
 'LeviCivitaLieVariation, RicciLieNaturality e ScalarEinsteinLieNaturality constroem a variação da conexão, Ricci e Einstein sob Lie. O enunciado metric_lie_einstein_naturality é HasDerivAt efetivo para δG_g(L_Vg)=L_VG(g), sob suavidade, simetria e não degenerescência da métrica.',
 [a('connection_lie',160,166),a('connection_lie',200,221),a('ricci_lie',179,192),a('einstein_lie',218,256)],
 'Resolve uma obrigação clássica de covariância/naturalidade; não fornece uma medida de caminho, operador métrico quântico, renormalização ou dinâmica microscópica universal.')

f('G11','EXISTE_LIGADO','Tipagem UV do caminho atual e escopo ampliado são perguntas distintas',
 'uv_dissolved_by_typing prova três proposições explícitas: mesma fonte implica mesma resposta clássica; excitação da identidade é zero; qualquer G positivo pode parametrizar o contrato. A conclusão não contém renormalizedAllOrders. UVScope016_v3 separa Completion com UV/QME/par físico, e seus lemas extraem essas hipóteses; o contraexemplo PUnit é lógico. Isso delimita o contrato semiclassico adotado, sem uma prova universal de completude UV.',
 [a('uv_typing',90,121),a('uv_scope',16,100),a('physics_certificates',288,301),a('um',165037,165127)],
 'Não impor renormalização de uma métrica quantizada como premissa ausente de um teorema que não a quantiza. Se a alegação for estendida a QG interagente/UV em todas as ordens, os pacotes proposicionais não fornecem essa construção.', 'A parte fora_do_caminho tem valor e obrigações próprias; não é descartada nem confundida com a missão FECHO.')

f('G12','KNOWN','Os artigos explicitam a ponte física e os resultados importados',
 'A Ponte distingue os axiomas físicos da Face C e a hipótese universal de horizonte; cita BFV/Hadamard/Kay-Wald/Rindler e explicita obrigações não perturbativas. O Custo distingue níveis da ponte e o problema físico de independência de folheação. O artigo Um atual registra a errata do termo curvo já existente e corrige a antiga leitura H2⇒H3 incondicional.',
 [a('article_ponte',914,943),a('article_ponte',1530,1571),a('article_custo',3216,3228),a('article_um',195,195),a('article_um',1008,1010),a('article_um',1248,1248)],
 'KNOWN significa citação/estatuto importado conforme fontes locais; não houve nova verificação da literatura externa. Hipóteses físicas permanecem entradas até fornecedor demonstrado. Um teorema condicional válido não prova sozinho a antecedente física.')

f('G13','EXISTE_NAO_LIGADO','Inventários antigos localizam resíduos, mas não são estado vigente',
 'BANCADA_TOE documentava a implicação mestra e lacunas do levantamento antigo. 01out e 07out registravam a falta do ligante curvo, certificados não habitados e escopo UV. O ligante foi incorporado v392/v393; certificados/core/Maxwell concretos foram construídos depois em F1. O relatório 22set trata sobretudo limites modulares e observacionais daquela rodada. A pendência universal específica não autoriza ressuscitar ausências já superadas.',
 [a('toe_synthesis',199,200),a('toe_critical',3,7),a('sep22',36,50),a('oct01',30,43),a('oct07',137,167),a('oct07',200,224),a('c1_second',21,34)],
 'EXISTE_NAO_LIGADO aqui é o estatuto do inventário histórico como fonte de navegação, sem promoção automática ao estado atual. R-MOD/ritos/natureza têm requisitos próprios e não são sinônimos de falta de todo teorema QG.')

f('G14','EXISTE_LIGADO','Versão canônica, candidata e sandbox conservam identidades distintas',
 'O selo corrente identifica v393; seu handoff declara custódia parcial B(3), e o exame c1 não é confirmação de execução da Bancada. O RESULTADO_V394_CANDIDATA_R2 declara candidata incremental para auditoria, sem rito integral, novo selo, alteração de produção ou gate. As construções F1 recentes têm recibos próprios e não são atribuídas retroativamente a v393 ou v394.',
 [a('seal',14,14),a('v393_c1',1,35),a('v393_c1',56,56)],
 'Os números da candidata (108 declarações/7153 degraus/5716 verificações) são lidos do recibo, não reproduzidos aqui. O hash do candidato foi conferido. Índice datado/servidor indisponível não prova ausência científica atual.', 'A palavra fechamento descreve o contrato matemático interno demonstrado, não confirmação física nem release integral sem custódia.')

f('G15','NAO_LOCALIZADO','Fonte específica do levantamento de 02set não identificada',
 'A fonte exata de 02set não foi localizada nesta recuperação. A coordenação informou busca mecânica ampla sem identidade confirmada; a pista ORDEM_004/D1+D7 não foi promovida a fonte. O corpus histórico de 03set e o Nós Vivo datado não abrangem necessariamente avanços posteriores.',
 [], 'Lacuna de cobertura documental, não ausência de um teorema. Não foi repetida a varredura ampla realizada pelo coordenador.')

f('G16','EXISTE_LIGADO','Pendências de dispositivo e alcance de QG não se confundem',
 'A missão FECHO mantém R4/R5 de ponte temporal/dispositivo em working, enquanto R7/R8 foram aceitos nos critérios registrados. As assinaturas examinadas de Einstein curvo e de H3 Maxwell não requerem um aparelho patenteado como premissa. Sua exposição matemática deve mostrar objetos/hipóteses/conclusão próprios; a realização do dispositivo é outra obrigação autorizada da missão.',
 [a('ligand',46,72),a('second_quantization',547,563),a('joint',123,147)],
 'Sem aceite novo, fechamento de quadro ou alteração de gate. Sem alegação QG confirmada. A falta do dispositivo não apaga a implicação formal; sua realização também não substituiria a prova de hH3 universal.')

coverage=[
 {'collection':'Três artigos','status':'consulta dirigida às cláusulas H3/Einstein e erratas','source_keys':['article_ponte','article_custo','article_um']},
 {'collection':'Canônico v393','status':'leitura estática, selo/manifesto/handoff; sem import ou execução','source_keys':['um','seal','manifest','v393_handoff','v393_c1']},
 {'collection':'Kernel curvo/H3/Ward/UV','status':f'{len(canonical)} fontes verificadas contra manifesto; seleção por assunto, não reauditoria integral','source_keys':list(canonical)},
 {'collection':'BANCADA_TOE 23ago','status':'histórico reexaminado por remissão; ausências antigas reconciliadas','source_keys':['toe_synthesis','toe_critical']},
 {'collection':'02set','status':'NAO_LOCALIZADO: identidade exata não confirmada; busca ampla da coordenação não repetida','source_keys':[]},
 {'collection':'22set','status':'relatório histórico consultado; rito observacional separado','source_keys':['sep22']},
 {'collection':'01out','status':'inventário histórico consultado','source_keys':['oct01']},
 {'collection':'07out/c1','status':'levantamento e auditorias do ligante reexaminados','source_keys':['oct07','c1_curved','c1_second']},
 {'collection':'F1/R52','status':'fontes atuais, três recibos e auditorias anteriores; sem rebuild','source_keys':['physical_core','physical_net','circular','joint','r7_delivery','r8_delivery']},
 {'collection':'Nós Vivo / Mapa','status':'recibos consultados; índice não decide validade nem presença posterior','source_keys':['nodes_unit','nodes_theme','routes']},
]

report={
 'schema':'iald.r58.gravity-h3-completeness-inventory.v1','created_utc':datetime.now(timezone.utc).isoformat(),
 'author':ACTOR,'unit':'F1.FECHO_20261015','board_claim_delegated':939,
 'mission_reference':pin(REF),'project':sources['project'],'mission_revision':project['revision'],
 'status':'INVENTARIO_FOCAL_CONCLUIDO_COM_LIMITES_EXPLICITOS','statute':'REAL: fontes/pinos verificados; DERIVED: avaliação de escopo; KNOWN: literatura apenas citada localmente',
 'summary':'A lei curva condicional, a colagem e naturalidade geométrica existem no canônico. O ramo F1 construiu core/rede/Maxwell concretos e H3 nulo fixo. Não foi localizado fornecedor físico universal de NamedAtlasH3; ele permanece antecedente explícito e equivale ao balanço nulo. Tipagem UV semiclassica não é prova de renormalização geral, nem a ausência dessa prova invalida o teorema de alcance menor.',
 'findings':findings,'coverage':coverage,'sources':sources,
 'verification':{'canonical_file_checks':manifest_checks,'selected_axiom_report':axioms,'build_receipt_checks':builds,'candidate394_measured':c394pin,'candidate394_receipt_counts':c394['counts'],'candidate394_receipt_scope':{k:c394[k] for k in ['status','scientific_verdict','whole_rite_rerun','new_seal','production_changed','gate_changed','pending']},'source_count':len(sources),'new_builds':0,'provider_calls':0,'original_writes':0,'mission_mutations':0,'dependency_reaudit':False},
 'limits':['Este é um levantamento de fontes e alcance, sem nova prova científica ou aceitação de requisito.','Hashes e enunciados conferidos não reproduzem uma compilação; os recibos preservados fornecem a evidência de execução.','NAO_LOCALIZADO é relativo à cobertura declarada, sem inferência de inexistência global.','Não foi lido ou exportado arquivo confidencial; um.py foi somente leitura estática.','R4/R5/dispositivo são pendências da missão, não condições adicionadas às assinaturas dos teoremas.','Nenhuma confirmação física, mudança do gate ou anúncio de implantação de candidata.'],
 'script':pin(Path(__file__)),
}
exclusive(D/'GRAVIDADE_H3_COMPLETUDE_INVENTORY_R58.json',report)
lines=['R58 — GRAVITAÇÃO / H3 / COMPLETUDE','Autor: '+ACTOR,'Referência: '+str(REF),'Revisão consultada: '+str(project['revision']),'Estatuto: inventário local medido; avaliação de alcance derivada; literatura importada não reverificada externamente.','',report['summary'],'']
for item in findings:
    lines += [f"{item['id']} [{item['classification']}] {item['title']}",item['finding'],'Limite/ponte: '+item['remaining_or_limit']]
    if item['scope']:lines.append('Escopo: '+item['scope'])
    for anchor in item['anchors']:lines.append(f"  Fonte: {anchor['path']}:{anchor['lines'][0]}–{anchor['lines'][1]} | SHA256 {anchor['sha256']}")
    lines.append('')
lines += ['COBERTURA']+[f"- {c['collection']}: {c['status']}" for c in coverage]
lines += ['',f"VERIFICAÇÃO: {len(sources)} fontes/recibos pinados; {len(manifest_checks)} módulos coincidem com manifesto; {len(axioms)} enunciados no axiom_report somente trio; três builds históricos EXIT0, {sum(len(x['axioms']) for x in builds)} relatórios de axiomas; nenhuma compilação nova.",'','ARQUIVOS DE EVIDÊNCIA (pinos medidos)']
for key,item in sources.items():lines.append(f"{key}: {item['path']} | {item['bytes']} bytes | SHA256 {item['sha256']}")
exclusive(D/'GRAVIDADE_H3_COMPLETUDE_INVENTORY_R58.txt','\n'.join(lines)+'\n')
print(json.dumps({'report':pin(D/'GRAVIDADE_H3_COMPLETUDE_INVENTORY_R58.json'),'text':pin(D/'GRAVIDADE_H3_COMPLETUDE_INVENTORY_R58.txt'),'counts':dict(Counter(x['classification'] for x in findings)),'sources':len(sources),'canonical_matches':len(manifest_checks),'selected_axiom_reports':len(axioms),'revision':project['revision']},ensure_ascii=False,indent=2))
