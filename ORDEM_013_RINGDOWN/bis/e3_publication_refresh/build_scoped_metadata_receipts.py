"""Publish metadata-only review receipts; never imports or runs production gates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, os

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
CHAT=B.parent
def raw(p): return p.read_bytes()
def sha(p): return hashlib.sha256(raw(p)).hexdigest()
def read(p): return json.loads(raw(p))
def publish(path,value):
    data=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8') if not isinstance(value,str) else value.encode('utf-8')
    tmp=path.with_suffix(path.suffix+'.pending')
    with tmp.open('xb') as f: f.write(data)
    assert raw(tmp)==data and len(data)>0
    os.link(tmp,path)
    tmp.unlink()
    return {'relative_to_Chatgpt':path.relative_to(CHAT).as_posix(),'sha256':sha(path),'bytes':len(data)}

regpath=B/'RINGDOWN_5SIGMA_V1.json'
reg=read(regpath)
regsha=sha(regpath)
censuspath=CHAT/reg['publication_census']['path']
assert sha(censuspath)==reg['publication_census']['sha256']
census=read(censuspath)
searchpath=HERE/'SEARCH_METADATA_POST_E2.json'
search=read(searchpath)
queries={r['event']:r for r in search['query_batches']}
events={k:v for k,v in reg['test_candidates'].items() if v['eligible'] is True and v['published_deformation_at_registration'] is False}
assert len(events)==14 and set(events)==set(queries)==set(census['not_found_scope_events'])
holds={k for k,v in events.items() if v['data_quality_hold']}
assert len(holds)==4 and holds==set(census['data_quality_holds'])
catalog=CHAT/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos'
paths=[regpath,censuspath,searchpath,B/'bis/e2_code/registration_guard.py',catalog/'gwtc4_tgr3.txt',catalog/'gwtc5_tgr.txt',catalog/'gwtc5_tgr_table2_3_parsed.json']
pins={p.relative_to(CHAT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in paths}
for p in paths[-3:]:
    old=next(v for k,v in census['source_pins'].items() if k.replace('\\','/').endswith('/'+p.name))
    assert sha(p)==old['sha256']
assert sha(B/'bis/e2_code/registration_guard.py')==reg['own_code_tree_sha256']['registration_guard.py']
table5={r['event']:{k:r[k] for k in ['table','RD','pSEOBNR','QNMRF']} for r in read(paths[-1]) if r['event'] in events}
assert len(table5)==13
assert all(row['table']==2 and all(row[k] is False for k in ['RD','pSEOBNR','QNMRF']) for row in table5.values())
# Only event-name column extracted from the pinned local primary Table 2.
lines=raw(catalog/'gwtc4_tgr3.txt').decode('utf-8').splitlines()
table4=sorted(set(m.group(0).replace(' ','_') for m in re.finditer(r'GW\d{6}[ _]\d{6}','\n'.join(lines[1831:2176]))))
assert table4==sorted(census['tgr4_table2_name_only_membership'])
assert 'GW230919_215712' not in table4
reviewed=datetime.now(timezone.utc).isoformat()
assert datetime.fromisoformat(reviewed)>datetime.fromisoformat(reg['registered_utc'])
scope=('Revisão documental pós-E2: lookup individual do ID completo em arXiv, LVK/DCC/GWOSC e Zenodo, '
       'mais alias curto com ringdown/spectroscopy/quasinormal; títulos/URLs/datas e metadados primários atuais; '
       'cruzamento separado com seleção por método dos textos/tabelas locais pinados TGR4/TGR5. '
       'NOT_FOUND_IN_SCOPE não é ausência universal. Sem posterior/amostras/quantis/strain, sem admissão ou PE; holds preservados.')
index={}
for event,entry in sorted(events.items()):
    q=queries[event]
    observed=datetime.strptime(q['observed_utc'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc)
    assert datetime.fromisoformat(reg['registered_utc'])<observed<=datetime.fromisoformat(reviewed)
    assert len(q['queries'])==4
    results=q['metadata_results']
    primary=['https://arxiv.org/abs/2603.19021','https://dcc-llo.ligo.org/LIGO-P2600130/public','https://zenodo.org/records/20275769'] if entry['run']=='O4a' else ['https://arxiv.org/abs/2607.19293','https://dcc.ligo.org/LIGO-P2500781/public','https://dcc.ligo.org/LIGO-P2600410/public']
    if entry['run']!='O4a':
        primary+=['https://zenodo.org/records/20348006' if event>='GW241210_060606' else 'https://zenodo.org/records/20348005']
    if event in holds:primary+=['https://arxiv.org/abs/2605.27090']
    leads=[]
    if event=='GW240515_005301':
        primary+=['https://arxiv.org/abs/2608.11620','https://zenodo.org/records/20452853']
        leads=[{'url':'https://arxiv.org/abs/2608.11620','classification':'OTHER_PRIMARY_TOPIC_ULTRALIGHT_BOSONS','limit':'Título/metadados de bosons/spin não demonstram ajuste de deformações QNM do evento.'},
               {'url':'https://zenodo.org/records/20452853','classification':'FRAMEWORK_COMPILATION_METADATA_ONLY','limit':'Lead por alias curto; título/descrição de compilação e discussão populacional não estabelecem publicação de deformações QNM deste ID. Conteúdo integral fora do escopo; não certificado como ausente.'}]
    opened=[s for s in search['opened_metadata'] if s['url'] in primary]
    domains={d:{'requested_queries':[a['q'] for a in q['queries'] if any(d==x or (d=='LVK_DCC_GWOSC' and x in ['dcc.ligo.org','ligo.org','virgo-gw.eu','gwosc.org']) for x in a['domains'])],
                'result_urls':[a['url'] for a in results if (d in a['url'] if d!='LVK_DCC_GWOSC' else any(x in a['url'] for x in ['ligo.org','gwosc.org','virgo-gw.eu']))],
                'coverage':'INDEXED_METADATA_LOOKUP_NOT_EXHAUSTIVE'} for d in ['arxiv.org','LVK_DCC_GWOSC','zenodo.org']}
    document={
        'schema_version':'E3_PUBLICATION_METADATA_REVIEW_V1','event':event,'parent_registration_sha256':regsha,
        'registration_utc':reg['registered_utc'],'reviewed_utc':reviewed,'review_passed':True,'scope':scope,
        'status':'SCOPED_DOCUMENTARY_REVIEW_COMPLETED__NO_PE_ADMISSION',
        'eventknown_delta_publication':'NOT_FOUND_IN_SCOPE','known_delta_publication_in_reviewed_scope':False,
        'universal_publication_absence':None,'publication_exists_outside_scope':'UNKNOWN',
        'registration_values_read_only':{'eligible':entry['eligible'],'published_deformation_at_registration':entry['published_deformation_at_registration'],'data_quality_hold':entry['data_quality_hold']},
        'quality_hold_preserved':entry['data_quality_hold'],'quality_hold_resolution_performed':False,
        'pe_or_admission_decision':None,'blindness_certified':False,'result_independent_method':True,
        'definition':'FOUND requires a primary publication or release establishing event-specific fitting of QNM frequency/damping deviations or equivalent free spectrum. GR remnant estimates, multimode Kerr detection, inspiral tests and boson-spin studies alone do not establish this.',
        'fresh_lookup':q,'domain_coverage':domains,'opened_current_primary_metadata':opened,
        'publication_date_scope':'Exact primary metadata dates/versions retained where exposed; search Published hints are not authoritative. Review is after E2, not a claim that publication occurred after E2.',
        'local_method_evidence':({'source':'gwtc4_tgr3.txt','locator':'Table 2, local lines 1832-2177: names only; section 2.1 parametrized-method linkage from frozen census','event_in_table2':False,'table2_names':table4} if event not in table5 else {'source':'gwtc5_tgr_table2_3_parsed.json','primary_text':'gwtc5_tgr.txt','locator':'Table 2 event-to-method flags, not result values','flags':table5[event]}),
        'version_limit':'Fresh arXiv metadata identifies TGR4/TGR5 v1; DCC TGR5 paper v17 and release v1. Local source bytes retain their own pins; equivalence to current remote full text is not asserted.',
        'new_metadata_leads':leads,
        'exposure':{'new_candidate_QNM_numeric_value_displayed_or_retained':False,'new_posterior_sample_quantile_or_strain_files_accessed':False,'search_snippets_filtered_before_model':True,'raw_snippets_not_persisted':True,'no_absolute_blindness_claim':True,'prior_incident_preserved_reference':{'census':str(censuspath.relative_to(CHAT).as_posix()),'sha256':sha(censuspath),'incident_event':census['incidental_exposure']['event']},'prior_B2_document_read':'B2 full document, including existing 440 diagnostic section, was displayed in the preceding null review; disclosed in E2_NULL_CAMPAIGN_INDEPENDENT_REVIEW.md. No new posterior files.','limits':'DECLARADO scoped observation of model-visible content, not an audit of every external search-engine intermediate or other agent.'},
        'limitations':['Exact-name indexing is incomplete; no-hit arXiv queries cannot exclude a publication.','Short alias can identify another event on the same day; no alias-only attribution of a deformation publication.','Indexed GR catalog products are not reclassified as deformation results.','Full texts outside pinned method tables, unindexed publications, supplementary numerical products and new posterior/strain files are outside scope.','review_passed attests only completion of this documented metadata contract; it does not clear quality holds, exposure adjudication, other gates or launch PE.'],
        'statutes':['REAL: metadata consultations, local hashes, event/method membership and chronology','DERIVED: scoped cross-match','INPUT: registered roles/holds preserved','DECLARADO: exposure limited to this review','OPEN: universal absence, physical calibration, PE admission and blindness'],
        'source_pins_relative_to_Chatgpt':pins}
    receipt=publish(HERE/(event+'.json'),document)
    wrapper={k:receipt[k] for k in ['relative_to_Chatgpt','sha256']}
    wrapper.update(reviewed_utc=reviewed,review_passed=True,scope=scope)
    index[event]={'publication_metadata_review':wrapper,'data_quality_hold':entry['data_quality_hold'],'quality_hold_resolution':None,'pe_admission':None,'eventknown_delta_publication':document['eventknown_delta_publication']}

summary={'schema_version':'E3_PUBLICATION_METADATA_INDEX_V1','status':'14_SCOPED_DOCUMENTARY_REVIEWS_COMPLETE__NO_JOB_ALLOCATION','parent_registration_sha256':regsha,'registration_utc':reg['registered_utc'],'reviewed_utc':reviewed,'events':index,'summary':{'events':14,'without_quality_hold':10,'quality_holds_preserved':4,'new_QNM_deviation_publications_found_in_scope':0,'targeted_queries':56,'supplementary_queries':8,'opened_primary_metadata_pages':11},'scope':scope,'producer_or_E2_sources_modified':False,'new_MC_or_PE':False,'builder_sha256':sha(Path(__file__)),'shared_metadata_sha256':sha(searchpath)}
indexpin=publish(HERE/'PUBLICATION_METADATA_REVIEW_INDEX.json',summary)
# Static receipt-contract validation only. No load_jobs/authorize_event execution.
assert len(index)==14
for event,info in index.items():
    w=info['publication_metadata_review'];p=CHAT/w['relative_to_Chatgpt'];d=read(p)
    assert p.resolve().is_relative_to(HERE.resolve())
    assert sha(p)==w['sha256'] and d['event']==event and d['parent_registration_sha256']==regsha
    assert d['reviewed_utc']==w['reviewed_utc'] and d['scope']==w['scope'] and bool(w['scope'].strip())
    assert d['review_passed'] is w['review_passed'] is True
    assert datetime.fromisoformat(reg['registered_utc'])<=datetime.fromisoformat(w['reviewed_utc'])<=datetime.now(timezone.utc)
    assert info['data_quality_hold']==events[event]['data_quality_hold'] and info['quality_hold_resolution'] is None
assert all(sha(CHAT/p)==v['sha256'] for p,v in pins.items())
validation=publish(HERE/'RECEIPT_CONTRACT_VALIDATION.json',{'status':'STATIC_METADATA_CONTRACT_CHECKS_PASS','events_checked':14,'parent_registration_sha256':regsha,'index':indexpin,'checks':['exact 14 registered eligible=true/published=false identities','UTC after actual registered_utc and not future','receipt SHA and event/parent/scope equality','review_passed true solely for documented scoped review','four unchanged holds; no quality resolutions created','pinned source bytes stable','no production imports or load_jobs/PE execution'],'validated_utc':datetime.now(timezone.utc).isoformat()})
lines=['# E3 — atualização documental de publicação após E2','',f'[REAL] Revisão concluída em {reviewed}; E2 registrado em {reg["registered_utc"]}.','',
       '**14 revisões documentais concluídas; nenhuma nova publicação de deformações QNM encontrada no escopo. Ausência universal permanece OPEN.** Dez eventos sem hold registrado; quatro holds preservados. Não há alocação, decisão de admissão ou execução de PE.','',
       'Foram feitas 56 consultas individualizadas (ID completo em arXiv, LVK/DCC/GWOSC e Zenodo; alias curto com termos de ringdown), oito consultas suplementares e leitura filtrada de 11 páginas primárias atuais. Títulos/URLs/datas e metadados são separados dos textos locais pinados; não se presume igualdade entre versões remotas e locais. Não foram abertos novos PDFs, posteriors, amostras, quantis ou strain.','',
       'Os metadados atuais identificam [TGR4 v1](https://arxiv.org/abs/2603.19021), de 19/03/2026, e [TGR5 v1](https://arxiv.org/abs/2607.19293), de 21/07/2026. O [registro DCC TGR5](https://dcc.ligo.org/LIGO-P2500781/public) está em v17 e sua [release](https://dcc.ligo.org/LIGO-P2600410/public) em v1. A tabela local TGR4 não inclui GW230919_215712 no conjunto pyRing parametrizado; os 13 O4b têm RD/pSEOBNR/QNMRF=false na seleção local TGR5. Isso não exclui outros estudos. Releases GR não são deformações.','',
       'GW240515 teve também leads de bosons/spin e compilação teórica por alias; títulos e descrições não estabeleceram ajuste QNM desse ID. A compilação integral não foi lida e permanece fora do escopo. O hold desse evento continua.','',
       '`PUBLICATION_METADATA_REVIEW_INDEX.json` fornece, por evento, o objeto `publication_metadata_review` com arquivo/hash/scope/reviewed_utc/review_passed, compatível com os campos lidos por `validate_job_reviews`/`load_jobs`. `review_passed=true` significa somente que esse contrato documental delimitado foi cumprido. A validação foi estática: não chamou os gates nem admitiu eventos. Os quatro holds continuam exigindo resolução independente.','',
       '| Evento | Consulta atual UTC | Resultado no escopo | Hold | Recibo |','|---|---|---|---|---|']
for event,info in index.items():
    lines.append(f'| {event} | {queries[event]["observed_utc"]} | NOT_FOUND_IN_SCOPE | {"PRESERVADO" if info["data_quality_hold"] else "Não registrado"} | [{event}.json]({event}.json) |')
lines+=['','Limites: indexação por nome incompleta, fontes não indexadas e artigos integrais fora das tabelas pinadas não cobertos. URLs de API GWOSC retornadas na busca são referências de índice; endpoints de parâmetros não foram abertos. Datas relativas do buscador não substituem datas primárias. Nenhum resultado quantitativo foi usado para selecionar evento.','',
        'Exposição: nesta atualização, nenhum valor numérico de deformação QNM de candidato foi exibido ou retido. Snippets foram filtrados antes da apresentação. O incidente anterior GW231123 do censo e a leitura integral de B2 na sidecar de nulos permanecem declarados; não se certifica cegueira absoluta.','',
        'Estatutos: [REAL] consultas/pins/cronologia; [DERIVED] cruzamento nominal; [INPUT] contratos e holds registrados; [DECLARADO] exposição no escopo; [OPEN] ausência universal, cegueira e admissão. NOT_FALSIFIED nunca CONFIRMED.','',
        'Pins calculados dos bytes:','',f'- Registro E2: `{regsha}`.',f'- Censo anterior: `{sha(censuspath)}`.',f'- Metadados atuais: `{sha(searchpath)}`.',f'- Índice dos 14 recibos: `{indexpin["sha256"]}`.',f'- Validação estática: `{validation["sha256"]}`.',f'- Guard lido: `{sha(B/"bis/e2_code/registration_guard.py")}`.','',
        'Pins completos e fontes por evento estão nos recibos; nenhum artefato E2 ou produtor foi alterado.']
report=publish(HERE/'PUBLICATION_REFRESH_REVIEW.md','\n'.join(lines)+'\n')
print(json.dumps({'status':summary['status'],'index':indexpin,'report':report,'validation':validation},ensure_ascii=False))
