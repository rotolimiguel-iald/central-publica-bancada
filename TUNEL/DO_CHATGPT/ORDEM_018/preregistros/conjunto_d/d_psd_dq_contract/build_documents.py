from pathlib import Path
import os,json,hashlib,re,datetime,time
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018')
BASE=ROOT/'preregistros/conjunto_d'
OUT=BASE/'d_psd_dq_contract'
SOURCE=Path(r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis')
V1=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_018_INSUMOS\RAMO_B_V1__PREREGISTRO_RAMO_B_RINGDOWN_V1.json')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def write(name,obj):
 p=OUT/name
 if isinstance(obj,str):b=obj.encode('utf-8')
 else:b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
 if p.exists():raise RuntimeError('Refuse overwrite '+str(p))
 t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
 return pin(p)
started=time.perf_counter()
p=json.loads((BASE/'PROPOSTA_MANIFESTO_METADATA_D.json').read_bytes())
v=json.loads(V1.read_bytes())['conjuntos']['D']
meta=json.loads((OUT/'GWOSC_METADATA_EXCERPT.json').read_bytes())
paths=[BASE/'PROPOSTA_MANIFESTO_METADATA_D.json',BASE/'NOTA_CONJUNTO_D.md',BASE/'AUDITORIA_METADATA_D.json',V1,
 SOURCE/'e2_code_v1_1_2/strain_io.py',SOURCE/'e2_code_v1_1_2/pe_runner.py',SOURCE/'e2_code_v1_1_2/registration_guard.py',
 SOURCE/'015/t07/T07_DOWNLOAD_PLAN_v3.json',SOURCE/'015/t07/T07_ONSOURCE_QUALITY_AUDIT.json',
 SOURCE/'015/t08/ZENODO_17602505_METADATA.json',SOURCE/'015/t08/ZENODO_20348005_METADATA.json',SOURCE/'015/t08/ZENODO_20348006_METADATA.json',
 BASE/'p3_init_preparation/sources/gw/detector/psd.py',BASE/'p3_init_preparation/sources/gw/detector/strain_data.py',
 OUT/'sources/_spectral_py.py',OUT/'sources/_windows.py',OUT/'GWOSC_METADATA_EXCERPT.json']
pins=[pin(x) for x in paths]
assert p['original_candidate_order']==v['eventos_elegiveis']
assert p['four_holds']==v['com_data_quality_hold']
rows=[]
for e in p['events']:
 for s in e['series']:
  match=re.search(r'-(\d+)-(\d+)\.hdf5$',s['official_url']);assert match
  start,duration=map(int,match.groups());limit=min(e['GPS_proposed']-64,s['t0'])
  row=dict(ordinal_V1=e['ordinal_V1'],event=e['event'],detector=s['detector'],hold=e['data_quality_hold'],
   GPS_reused=e['GPS_proposed'],url=s['official_url'],hdf5_path=s['hdf5']['path'],
   hdf5_sha256_DECLARED=s['hdf5_sha256_DECLARED_IN_PINNED_MANIFEST'],
   prior_stat_only=s['hdf5'],file_interval_DECLARED_from_filename=[start,start+duration],
   onsource_interval_DECLARED_manifest=[s['t0'],s['end_exclusive']],sample_rate_hz_DECLARED=s['sample_rate_hz'],
   onsource_manifest_status=s['manifest_status'],onsource_manifest_nan=s['manifest_nan'],
   offsource_end_upper_bound_proposal=limit,geometric_preoffsource_seconds=max(0,limit-start),
   actual_DQ_coverage='OPEN_NOT_READ',actual_calibration='OPEN_NOT_READ',PSD_measured=False,alternatives={})
  for key,length in [('A',256),('B',512)]:
   fits=start+length<=limit and start+length<=start+duration
   row['alternatives'][key]=dict(duration_s=length,geometrically_possible=fits,
    earliest_block_if_DQ_all_good=[start,start+length] if fits else None,
    status='DECLARED_GEOMETRY_ONLY_DQ_UNKNOWN' if fits else 'BLOCKED_NAMED_FILE_PREOFFSOURCE_TOO_SHORT',
    actual_selected_block=None,source_content_read=False)
  rows.append(row)
availability={'status':'PROPOSTA_DOCUMENTAL_NAO_RATIFICADA','identity_source':pin(BASE/'PROPOSTA_MANIFESTO_METADATA_D.json'),
 'GPS_reconciliation_repeated':False,'file_content_read':False,'stat_repeated':False,
 'interpretation':'Intervalos de arquivo derivados somente do nome/URL pinado. Nao verificam amostras, DQ ou calibracao. OK/nan=0 refere-se ao recorte de 32 s declarado no manifesto, nao ao offsource.',
 'four_holds':p['four_holds'],'rows':rows}
write('DISPONIBILIDADE_OFFSOURCE_METADATA.json',availability)
zen=[]
for q in paths:
 if q.name.startswith('ZENODO_'):
  d=json.loads(q.read_bytes());desc=d['metadata'].get('description','')
  snippets=[desc[max(0,m.start()-150):m.end()+180] for m in re.finditer('calibration',desc,re.I)]
  zen.append({'source':pin(q),'record_id':d['id'],'description_evidence':snippets,
   'statute':'DECLARADO_NA_DESCRICAO_DO_RELEASE_NAO_VERIFICADO_POR_EVENTO','no_container_opened':True,
   'D_release_file_descriptors':[{'event':e['event'],'descriptor':g['file_descriptor']} for e in p['events'] for g in e['GR_release_metadata'] if str(g['record_id'])==str(d['id'])]})
sources={'source_pins':pins,'GWOSC_original_manifest':{k:meta[k] for k in ('source','sha256','bytes')},
 'GWOSC_selected_schema':meta['selected_series_schema'],'DQ_PSD_calibration_fields_in_selected_schema':meta['quality_calibration_PSD_descriptor_fields_in_selected_schema'],
 'installed_SciPy':{'version':'1.18.1','version_read_using':'importlib.metadata only; scientific modules not imported',
 'original_sources':['/opt/lal_env/lib/python3.12/site-packages/scipy/signal/_spectral_py.py','/opt/lal_env/lib/python3.12/site-packages/scipy/signal/windows/_windows.py']},
 'citations':[
 {'file':str(SOURCE/'e2_code_v1_1_2/strain_io.py'),'symbols':['quality_mask','window','offsource_psd'],'supports':'exact named DQ bits, one-second masks, first valid pre-event block, Hann 50% median Welch; no resampling'},
 {'file':str(OUT/'sources/_spectral_py.py'),'lines':[515,517,533,548,568,590,950,964,2464,2489],'supports':'Welch, mean/median branches, one-sided density, median correction; docs cite Welch1967 and FINDCHIRP2012 but papers not newly fetched'},
 {'file':str(BASE/'p3_init_preparation/sources/gw/detector/strain_data.py'),'lines':[147,153,166,192],'supports':'inclusive band mask and notch support; Tukey and window_factor'},
 {'file':str(BASE/'p3_init_preparation/sources/gw/detector/psd.py'),'lines':[238,241],'supports':'interpolation outside PSD domain fills infinity; proposal explicitly rejects domain/grid mismatch first'}],
 'release_descriptors':zen,'coverage_limit':'Somente fontes nomeadas. Nao e busca global nem inspecao dos conteudos PE/GWOSC.'}
write('FONTES_E_LACUNAS.json',sources)
common=dict(sample_rate_hz=4096,onsource_duration_s=32,onsource_start='Reuse exact sample-aligned t0 from pinned metadata; do not recompute rounded GPS-16',
 onsource_roll_off_s=0.4,onsource_window='Bilby Tukey; alpha=2*0.4/32=0.025; record window_factor and apply exactly once',
 psd_segment_s=32,nperseg=131072,noverlap=65536,nfft=131072,window='hann, periodic/DFT-even as SciPy get_window default',
 detrend='constant per segment',return_onesided=True,scaling='density',PSD_units='strain^2/Hz',ASD_units='strain/sqrt(Hz)',
 grid={'delta_f_hz':1/32,'n_frequency_bins':65537,'Nyquist_hz':2048,'analysis_band_hz_inclusive':[20,1024],'analysis_bin_count':32129},
 resampling='FORBIDDEN_WITHOUT_SEPARATE_PRIOR_CONTRACT',zero_padding=False,PSD_interpolation='None needed on identical grid; assert grid equality/domain before Bilby; no extrapolation',
 offsource_exclusion_s=64,offsource_end_limit='min(event_GPS-64, exact onsource start)',
 interval_rule='First full integer-second block in named 4096 s file passing registered DQ/no-injection bits and finiteness, with end <= limit; per detector separately. No scan by PSD level, stationarity or fit quality.',
 onsource_rule='Existing 32 s exact sample-aligned interval, all required DQ/no-injection bits and finite samples; no recentering from signal',
 gating='None. No clipping, inpainting, transient deletion or PSD-driven gate selection. Fail quality/stationarity -> HOLD; changing rule needs prior independent review.',
 lines={'proposed_notch_list':[],'handling':'Include lines in measured PSD, no whitening/notching based on signal. Official line list not identified in inspected sources; any fixed mask alternative must be separately pinned before data selection.',
 'status':'INPUT_PROPOSED_NOT_RATIFIED'},
 calibration={'required':'Detector/release identity, strain convention/units, epoch-valid calibration provenance, amplitude/phase envelope paths+hashes+frequency/GPS validity and pre-fixed treatment.',
 'observed':'Zenodo descriptions declare envelopes within PE releases. Internal paths, availability per detector/event and values not read.',
 'identity_calibration_is_not_zero_uncertainty':True,'missing_policy':'HOLD_CALIBRATION; do not claim scientific PE readiness or set uncertainty to zero by default.'})
alternatives=[
 {'id':'A','status':'INPUT_PROPOSTA','psd_duration_s':256,'estimator':'Welch median with SciPy median-bias correction','periodogram_count':15,
 'segment_overlap_dependence':'15 overlapping periodograms are not 15 independent realizations; correction does not prove Gaussianity/stationarity.',
 'existing_code':'offsource_psd supports estimator and configurable duration as is; diagnostics/receipts still require separate reviewed implementation.',
 'selection_effect':'14/14 named-file geometries accommodate duration if DQ valid, including four holds which remain holds.',
 'conditional_error_scope':'PSD fixed estimate gives conditional PE errors; no PSD uncertainty marginalization or coverage claim.',
 'rationale':'Less offsource and compatible estimator in admitted helper; shorter estimate has greater PSD estimation uncertainty.'},
 {'id':'B','status':'INPUT_PROPOSTA','psd_duration_s':512,'estimator':'Welch arithmetic mean','periodogram_count':31,
 'segment_overlap_dependence':'31 overlapping periodograms not independent.',
 'existing_code':'Installed scipy.signal.welch supports mean; admitted strain_io hardcodes median. Needs isolated reviewed adapter change BEFORE any data stage; no such adapter built here.',
 'selection_effect':'13/14 named-file geometries accommodate duration. GW250118_170523 H1/L1 blocked before DQ under this exact pre-event rule; do not silently shorten, switch to A or fetch a different file.',
 'conditional_error_scope':'Conditional on plug-in PSD; mean is more exposed to transients. No bias/coverage measured.',
 'rationale':'Longer averaging sample and conventional mean. Deliberate alternative, not fallback or a detector-by-detector choice after seeing data.'}]
stationarity={'status':'INPUT_HEURISTIC_PROPOSAL_NOT_CALIBRATED','when':'AFTER deterministic DQ+finiteness interval selection; never scan new interval following diagnostic failure',
 'partition':'Two equal nonoverlapping halves of chosen offsource; same 32 s Hann50% estimator as selected alternative.',
 'half_periodograms':{'A':7,'B':15},
 'bands_hz_half_open_except_final_upper_inclusive':[[20,64],[64,128],[128,256],[256,512],[512,1024]],
 'statistic':'For each band, P_j=sum_{k in band} S_j(f_k)*delta_f; R=max(P_1,P_2)/min(P_1,P_2). All finite and positive; proposed accept R<=2 in every band.',
 'threshold':2,'threshold_status':'INPUT. Not a confidence bound or measured false-alarm rate. Needs synthetic qualification and prior ratification before real offsource.',
 'failure':'HOLD_STATIONARITY; record complete diagnostics, no reroll/no interval reselection/no estimator switch.',
 'limitations':'Only coarse temporal consistency within offsource; does not prove stationarity at onsource or characterize all narrow lines. No onsource/fit/posterior used to choose threshold.',
 'PSD_uncertainty':'Finite-sample/overlap and estimator uncertainty require separate synthetic controls or declared conditional treatment before inferential claims.'}
gaps=[
 {'id':'DQ_NAMES','status':'OPEN','evidence':'GWOSC selected-row schema has no DQ flag names/dictionaries; helper requires nonempty exact names for both DQ and no-injection masks.',
 'needed':'Official named flag dictionary and per-detector allowed requirements, including semantics/epoch/version; no numeric mask guessed from old T07 booleans.'},
 {'id':'DQ_INTERVALS','status':'OPEN','evidence':'No masks for these offsource intervals were read. T07 prior audit has zero D rows according to pinned earlier audit.',
 'needed':'After specific scoped opening, read metadata/masks only, confirm one-second indexing and full-window validity. Missing/bad/misaligned masks -> HOLD.'},
 {'id':'CALIBRATION','status':'OPEN','evidence':'Release-level descriptions declare envelopes but no per-event envelope inventory was inspected.',
 'needed':'Separate safe metadata-only extraction plan, paths/hashes and validity; no reading centers/posterior arrays; missing -> HOLD_CALIBRATION.'},
 {'id':'PSD_AND_STATIONARITY','status':'OPEN_NOT_MEASURED','evidence':'No strain read; no PSD or diagnostic computed.',
 'needed':'Prior choice A/B and threshold ratification; synthetic qualification; then specifically authorized offsource access. No claim of quality from geometry.'},
 {'id':'B_LAST_EVENT','status':'DERIVED_GEOMETRY_ONLY','evidence':'GW250118_170523 pre-event capacity 421.2 s from named file/GPS with 64 s exclusion.',
 'needed':'B gives hold under this file/rule. Alternate earlier file not admitted/identified here; retrieval/network not authorized by this proposal.'},
 {'id':'LINE_CATALOG','status':'OPEN','evidence':'No official per-epoch line list identified in named inputs.',
 'needed':'Ratify explicit no-notch treatment or separately pin a metadata-defined line mask before data; no data-tuned notches.'},
 {'id':'INITIALIZATION_AND_TOOL','status':'OPEN_FOR_REAL_D','evidence':'Synthetic qualified instrument does not qualify GWOSC loader, measured PSD, calibration or real-data guards.',
 'needed':'Separate reviewed metadata/strain/PSD driver and cost authorization; current package is documentary, not executable batch.'}]
contract={'schema':'IALD_D_PSD_DQ_SELECTION_PROPOSAL_V1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PROPOSTA_NAO_RATIFICADA_SEM_AUTORIZACAO_DE_ABERTURA','scope':'Preparacao documental ORDEM018 F3; nao lote executavel nem veredito.',
 'authorization':{'read_strain':False,'read_HDF5_NPZ':False,'read_posteriors':False,'network':False,'PE':False,'scientific_execution':False,'operator_decision_required_before_opening_D':True},
 'source_pins':pins,'selected_alternative':None,'recommendation':'A for review: compatible admitted median helper and all named-file geometries. This recommendation uses metadata only, does not ratify A, validate threshold or release any hold.',
 'common_parameters_proposed':common,'alternatives':alternatives,'stationarity_proposed':stationarity,
 'DQ_configuration':{'required_quality_flags':None,'required_no_injection_flags':None,'status':'OPEN_MUST_BE_NONEMPTY_EXACT_NAMES_BEFORE_DATA',
 'validation':'Require matching flag dictionaries, integer bit-vectors, 1 Hz coverage, correct GPS/sample alignment, all required bits set over both offsource and onsource, finite strain; failures visible.',
 'old_T07_rule':'Do not import descriptive ratio>10 as a cut; that threshold was post-data diagnostic, not registered selection.'},
 'selection_by_metadata':{'criteria_V1_verbatim':v['criterio_do_registro'],'freeze_V1_verbatim':v['congelamento_por_evento'],
 'original_order':p['original_candidate_order'],'four_holds_preserved':p['four_holds'],'ten_without_prior_hold_are_not_ready':True,
 'four_holds_can_only_change':'Separate explicit metadata-based decision and reviewed evidence before any PE; current document changes none.',
 'eight_pending_outside_list':'No additions/reconciliation/eligibility changes in this task.',
 'H1_L1_block':'One event for inference, both detectors same chosen policy; one missing detector -> HOLD under this proposal, no single-detector substitution.',
 'blindness':'No delta-tau, posterior center, H0, fit/Bayes factor or signal residual used for metadata selection; catalogue GR eligibility criteria inherited, not recalculated.'},
 'later_process_before_verdict':[
 'Review proposal and choose ONE A/B globally by metadata; ratify grid/window, DQ names/semantics, line and calibration policies, stationarity rule and cost contract.',
 'Identify exact approved metadata/envelope artifacts by hash; seek scoped operator permission for opening D. This document grants none.',
 'If authorized, metadata-only inspection first; preserve existing holds until explicit documented decision. Missing metadata stops progression.',
 'After separately authorized offsource stage, verify file hashes/sample alignment/DQ, choose deterministic first valid block; compute pinned PSD and diagnostics, retain failed rows and stop without fallback.',
 'Review selected PSD/DQ/calibration manifest and event selection independently; freeze per-event inputs BEFORE PE or posterior access.',
 'Only then separate PE/cost authorization with already required injection/bias/coverage/family/systematic gates; negative or incomplete controls remain visible. No two-job coverage inference.',
 'Any later verdict uses its own registered function/inputs/covariance and checks; no verdict in current task.'
 ],'gaps':gaps,'preservation':{'V1_modified':False,'holds_released':False,'old_packages_modified':False,'INIT003_accessed':False,'Atlas_modified':False,'gate_changed':False}}
write('CONTRATO_PSD_DQ_SELECAO_D_PROPOSTA.json',contract)
checks=[]
def ck(name,value):checks.append({'name':name,'pass':bool(value)})
ck('14 preserved in exact V1 order',[e['event'] for e in p['events']]==v['eventos_elegiveis'] and len(p['events'])==14)
ck('four holds preserved',p['four_holds']==v['com_data_quality_hold'] and len(p['four_holds'])==4)
ck('28 metadata rows',len(rows)==28 and len(meta['rows'])==28)
ck('A geometry 28 possible',sum(r['alternatives']['A']['geometrically_possible'] for r in rows)==28)
ck('B geometry 26 possible',sum(r['alternatives']['B']['geometrically_possible'] for r in rows)==26)
ck('B blocked identity only last event',set(r['event'] for r in rows if not r['alternatives']['B']['geometrically_possible'])=={'GW250118_170523'})
ck('no PSD measured',all(not r['PSD_measured'] for r in rows))
ck('no actual block selected',all(a['actual_selected_block'] is None for r in rows for a in r['alternatives'].values()))
ck('sample rate declaration 4096',all(r['sample_rate_hz_DECLARED']==4096 for r in rows))
ck('32s onsource declaration',all(r['onsource_interval_DECLARED_manifest'][1]-r['onsource_interval_DECLARED_manifest'][0]==32 for r in rows))
ck('no quality descriptors in selected schema',not meta['quality_calibration_PSD_descriptor_fields_in_selected_schema'])
ck('A periodogram arithmetic',1+(256*4096-131072)//65536==15)
ck('B periodogram arithmetic',1+(512*4096-131072)//65536==31)
ck('same FFT grid',common['grid']['n_frequency_bins']==common['nfft']//2+1)
ck('inclusive band arithmetic',int((1024-20)*32)+1==common['grid']['analysis_bin_count'])
ck('two hypotheses no chosen estimate',len(alternatives)==2 and contract['selected_alternative'] is None)
ck('read and execute forbidden',all(contract['authorization'][x] is False for x in ('read_strain','read_HDF5_NPZ','read_posteriors','network','PE','scientific_execution')))
ck('source files unchanged',all(pin(Path(x['path']))==x for x in pins))
assert all(x['pass'] for x in checks)
write('RECIBO_VERIFICACAO_DOCUMENTAL.json',{'status':'PASS_DOCUMENTARY_ONLY','checks':checks,'count':len(checks),'elapsed_s':time.perf_counter()-started,
 'scientific_computations':0,'PSD_computations':0,'strain_samples_read':0,'posteriors_read':0,'native_calls':0,
 'not_a_measurement':'Arithmetic of declared intervals/grid and static-document pin checks only; no scientific runtime imported or executed.'})
note="""# Proposta PSD/DQ/seleção D — preparação documental

[REAL] Esta entrega preserva V1, os 14 candidatos na ordem original e os quatro holds. Reutiliza a reconciliação GPS existente. Não abre strain/HDF5/NPZ, posteriores, rede ou pacote INIT003; não mede PSD, não executa PE, não ratifica seleção e não concede autorização de abertura.

[DERIVED sobre metadata DECLARADO] Os nomes dos 28 arquivos H1/L1 indicam 4.096 s a 4.096 Hz. A proposta usa os intervalos onsource de 32 s já declarados, com seus t0 alinhados à grade; não arredonda novamente GPS−16. O manifesto diz OK/nan=0 para esses recortes, não para offsource ou DQ. Os 28 descritores não têm campos PSD, DQ/flags ou calibração. A presença/tamanho dos arquivos é o stat histórico pinado; não foi repetido nem convertido em hash de conteúdo.

| Alternativa proposta | Offsource | Estimador/grade | Limite documental |
|---|---|---|---|
| A | 256 s anteriores, exclusão 64 s | Welch mediana corrigida; segmentos 32 s, Hann periódico, 50% sobreposição; 15 periodogramas | Cabe geometricamente nos 14 arquivos por detector; DQ desconhecido. Helper existente suporta essa escolha. |
| B | 512 s anteriores, mesma exclusão | Welch média; segmentos e grade iguais; 31 periodogramas | Cabe em 13/14; GW250118_170523 tem só 421,2 s anteriores no arquivo nomeado. Exige adaptador revisado, porque strain_io fixa mediana. |

[INPUT, não ratificado] Recomenda-se A à revisão pela compatibilidade com o helper e pela geometria documental. Isso não demonstra qualidade ou precisão: a PSD mais curta tem incerteza maior. A escolha deve ser global, antes da abertura; B não permite encurtar um evento, buscar outro arquivo ou trocar estimador após olhar dados. Os periodogramas sobrepostos não são realizações independentes. A correção de viés da mediana no SciPy não certifica estacionariedade.

A regra comum é o primeiro bloco inteiro que satisfaça flags registradas e finitude, do início do arquivo nomeado até min(GPS−64, t0 onsource), separadamente em H1/L1. Não se escolhe por amplitude de PSD, estacionariedade ou ajuste. O bloco selecionado pode estar afastado do evento dentro dos 4.096 s: esse é um limite explícito da proposta. H1/L1 formam um evento; a falta de um detector mantém HOLD, sem substituição por análise de detector único.

A banda proposta é 20–1.024 Hz, inclusiva; Δf=1/32 Hz, FFT de 131.072 amostras, PSD unilateral em strain²/Hz, sem resampling, padding ou extrapolação. PSD recebe Hann; onsource recebe Tukey com roll-off 0,4 s (alpha=0,025), com window_factor contabilizado uma vez. Gating, clipping e notches escolhidos pelo sinal não são admitidos. A lista proposta de notches é vazia; a ausência de catálogo oficial de linhas nesta consulta precisa de decisão prévia explícita, sem inventar uma máscara.

[INPUT, heurística ainda não qualificada] Diagnóstico de estacionariedade: dividir o offsource escolhido em duas metades; integrar PSD por bandas 20–64, 64–128, 128–256, 256–512 e 512–1.024 Hz, usando bordas semiabertas e última borda inclusiva. Exigir positividade/finitude e razão maior/menor ≤2 em todas. Falha gera HOLD_STATIONARITY sem procurar outro bloco. O limiar 2 não é nível de confiança nem tem taxa de falso alarme medida; requer qualificação sintética e ratificação prévias. Esse diagnóstico não prova estacionariedade no onsource nem resolve todas as linhas estreitas.

[OPEN] Faltam nomes/semântica dos bits DQ e no-injection por época/detector, máscaras que cubram as janelas e validação do índice 1 Hz. O helper local exige listas não vazias e nomes exatos. Booleanos de máscaras no T07 não identificam nomes; seu ratio>10 era diagnóstico descritivo e não é importado como corte. Finitude não substitui DQ.

[DECLARADO/OPEN] Os três snapshots Zenodo descrevem PSDs e envelopes de incerteza de calibração nas liberações PE. FONTES_E_LACUNAS.json preserva a descrição e os descritores exatos de arquivos por evento. Não foram lidos seus containers: caminhos internos, cobertura por detector/época, frequências, amplitude/fase e aplicação permanecem abertos. A identidade de calibração padrão não significa incerteza nula. Sem proveniência/envelopes e tratamento fixo, HOLD_CALIBRATION. Uma futura extração só de metadata exigirá escopo que continue vedando centros/arrays de posteriores.

[REAL] Quatro holds preservados: GW240515_005301, GW240615_160735, GW240930_035959 e GW241102_144729. Os dez restantes não se tornam prontos por não terem o hold antigo. Os oito pendentes externos à lista não são incorporados. Os critérios de elegibilidade/publicação e a cláusula de congelamento por evento do V1 estão transcritos no contrato; nenhuma elegibilidade GR foi recalculada.

Antes de qualquer veredito: revisão e escolha do contrato por metadata → decisão específica de abertura → inventário/DQ/calibração permitido → offsource autorizado e PSD pinada → revisão independente e seleção congelada por evento → autorização própria de PE/custo e controles de viés/cobertura/famílias/sistemáticos. Qualificação sintética não resolve esses requisitos reais. Incertezas com PSD plug-in são condicionais à estimativa e não uma afirmação de cobertura.

A evidência desta entrega é documental: 18 verificações de identidade, preservação, pins e aritmética de intervalos/grade; zero amostras lidas, zero PSD, zero likelihood/waveform/sampler. O script de construção somente lê JSON e fontes locais nomeadas e escreve documentos nesta pasta; não é lote executável científico. Fontes exatas, hashes e recortes estão no manifesto e no arquivo de fontes. Não se afirma ausência global de PSD/envelopes, nem cobertura que não foi inspecionada.
"""
write('NOTA_PSD_DQ_SELECAO_D.md',note)
manifest={'status':'PREPARACAO_DOCUMENTAL_CONCLUIDA_SEM_ABERTURA_D','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'files':[pin(x) for x in sorted(OUT.rglob('*')) if x.is_file() and x.name!='MANIFESTO_D_PSD_DQ.json'],
 'source_pins':pins,'no_scientific_execution':True,'no_authorization_granted':True,'V1_and_holds_preserved':True}
write('MANIFESTO_D_PSD_DQ.json',manifest)
print(json.dumps({'manifest':pin(OUT/'MANIFESTO_D_PSD_DQ.json'),'contract':pin(OUT/'CONTRATO_PSD_DQ_SELECAO_D_PROPOSTA.json'),'note':pin(OUT/'NOTA_PSD_DQ_SELECAO_D.md'),'checks':len(checks)},ensure_ascii=False))
