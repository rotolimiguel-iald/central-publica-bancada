"""Corpus membership and GR metadata join only; no posterior values opened."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,time
B=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
sources={};start=time.perf_counter()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):
    p=B/n;raw=p.read_bytes();sources[n]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()};return json.loads(raw)
def require(ok,msg):
    if not ok:raise ValueError(msg)
def dump(n,obj):
    with (O/n).open('xb') as f:f.write((json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
for n in ['CALIBRATION_AND_CANDIDATE_CENSUS.json','CALIBRATION_AND_CANDIDATE_CENSUS.md','CENSUS_RECEIPT.json']:require(not (O/n).exists(),'Existing '+n)
index=load('cache/public/21454847/archive_index.json');ext=load('cache/public/21454847/extraction_receipt.json');archive=load('cache/public/21454847/pSEOB.tar.gz.receipt.json')
require(index['archive_sha256']==ext['archive_sha256']==archive['sha256'],'archive receipt link')
members=[m for m in index['members'] if m['name'].endswith('.h5')]
require(len(members)==33 and all(m['regular'] and not m['link'] for m in members),'archive HDF33')
names={Path(m['name']).name for m in members};require(len(names)==33,'duplicate members')
schema=load('C4_CATALOG_SCHEMA.json');oldschema=load('C4_GWTC3_SCHEMA.json');old=load('C4_GWTC3_220.json');dataset=load('bis/e0_core/DATASET.json')
require(names=={r['filename'] for r in schema['rows']},'index/schema coverage')
ex={Path(r['member']).name:r for r in ext['files']};sizes={Path(m['name']).name:m['size'] for m in members}
for r in schema['rows']:
    name=r['filename'];m=re.fullmatch(r'pSEOB_(GW\d{6}_\d{6})_Prod0\.h5',name)
    require(m and m[1]==r['event'],'filename event identity')
    require(ex[name]['sha256']==r['sha256'] and ex[name]['size']==sizes[name],'extraction/schema hash or size')
    p=B/'cache/public/21454847/extracted/pSEOB/metafiles'/name
    require(p.is_file() and p.stat().st_size==sizes[name],'file existence/size; no HDF open')
require(len(oldschema['rows'])==len(old['rows'])==18,'legacy18')
legacyfiles={r['member']:r for r in oldschema['rows']}
for r in old['rows']:require(legacyfiles[r['legacy_member']]['sha256']==r['source_sha256'],'legacy product link')
five={r['event'] for r in schema['rows']};three={r['event'] for r in old['rows']}
require(len(five)==33 and len(three)==18,'unique within releases')
overlap=five&three;union=five|three;require(len(overlap)==12 and len(union)==39,'union39')
require(set(old['duplicate_reconciliation']['overlap'])==overlap,'archived overlap')
require(set(old['duplicate_reconciliation']['older_only'])==three-five,'older only')
require({r['event'] for r in dataset['rows']}==union and len(dataset['rows'])==51,'E0 corpus')
for catalog,es in [('GWTC5',five),('GWTC3',three)]:
    require(set(dataset['sets'][f'{catalog}_{len(es)}'])=={f'{catalog}:{e}' for e in es},'E0 population')
gr=load('bis/e1_selection/GR_O4A_ADENDO.json');greceipt=load('bis/e1_selection/GR_O4A_RECEIPT.json')
require(greceipt['outputs']['GR_O4A_ADENDO.json']['sha256']==sha(O/'GR_O4A_ADENDO.json'),'GR adendum receipt')
tables=[];census={}
for r in gr['O4_snapshot_rows']:
    rho=r['SNR_network_GWOSC']
    if rho is None or rho<12:continue
    event=r['event'];available=event in union;passed=r['adopted_INPUT_eligibility']
    role='CALIBRATION_NONBLIND_EXISTING_POSTERIOR' if available else ('CANDIDATE_ONLY_ABSENT_FROM_AUDITED_CORPUS' if passed is True else ('AWAITING_GR_METADATA' if passed is None else 'INPUT_NOT_MET_WITH_KNOWN_METADATA'))
    tables.append({'event':event,'run':r['run'],'SNR_network_GWOSC':rho,'GR_final_mass_detector_median':r['GR_metadata']['final_mass_detector'] if r['GR_metadata'] else None,
        'GR_final_spin_median':r['GR_metadata']['final_spin'] if r['GR_metadata'] else None,'metadata_origin':r['metadata_origin'],
        'GR_input_eligibility':passed,'in_GWTC5_33':event in five,'in_GWTC3_18':event in three,'in_audited_39_event_corpus':available,
        'role':role,'priority_ge30':r['priority_SNR30'],'universal_never_published':None,'blindness_certified':False,'E2_registered':False})
for run in ['O4a','O4b','O4c_discovery_only','O4_public_total']:
    rr=[r for r in tables if r['run']==run or run=='O4_public_total']
    published=[r for r in rr if r['in_audited_39_event_corpus']];eligible=[r for r in rr if r['GR_input_eligibility'] is True];candidates=[r for r in eligible if not r['in_audited_39_event_corpus']]
    census[run]={'SNR_ge12':len(rr),'published_in_audited_corpus':len(published),'absent_from_audited_corpus':len(rr)-len(published),
        'eligible_INPUT':len(eligible),'eligible_with_archived_220':sum(r['in_audited_39_event_corpus'] for r in eligible),'eligible_absent_from_audited_corpus':len(candidates),
        'awaiting_GR':sum(r['GR_input_eligibility'] is None for r in rr),'candidate_events':[r['event'] for r in candidates],
        'published_events':[r['event'] for r in published],'absent_events':[r['event'] for r in rr if not r['in_audited_39_event_corpus']],
        'candidate_priority_ge30':[r['event'] for r in candidates if r['priority_ge30']]}
cb=census['O4b'];require([cb[k] for k in ['SNR_ge12','published_in_audited_corpus','absent_from_audited_corpus','eligible_INPUT','eligible_with_archived_220','eligible_absent_from_audited_corpus']]==[45,14,31,27,14,13],'Requested O4b census')
calibration=[]
for event in sorted(union):
    available=[]
    for prefix,s in [('GWTC5',five),('GWTC3',three)]:
        if event in s:available.append(prefix+':'+event)
    calibration.append({'event':event,'available_products':available,'preferred_for_deduplicated_census':('GWTC5' if event in five else 'GWTC3')+':'+event,'scope':'Nonblind calibration membership; no combined likelihood computed or independent multiplication of overlaps'})
data={'status':'PASS_METADATA_CENSUS__NOT_UNIVERSAL_PUBLICATION_SEARCH_OR_E2_REGISTRATION','utc':datetime.now(timezone.utc).isoformat(),
 'corpus':{'GWTC5_21454847_HDF_members':33,'GWTC3_17461225_products':18,'total_products':51,'overlap_events':12,'union_unique_events':39,'GWTC5_event_list':sorted(five),'GWTC3_event_list':sorted(three),'overlap_list':sorted(overlap),'legacy_only_list':sorted(three-five),'deduplicated_event_list':sorted(union),'calibration_products':calibration},
 'selection_membership_scope':'All33 plus18 count as exposed calibration corpus, even events excluded from particular31/10 scientific combinations. No excluded product becomes a blind event.',
 'counts_by_run':census,'SNR_ge12_metadata_rows':tables,
 'absence_status':'NOT_FOUND_IN_PINNED_21454847_AND_17461225_PSEOB_CORPUS_ONLY',
 'scope':['No posterior values read; current extracted filenames/stat sizes and pinned archive index/schema receipts cross-checked','Archive/raw HDF SHA strings cross-linked to receipts; no fresh full-tar or HDF byte hash in this lightweight census','No claim never published universally, no literature-wide absence proof, no certification of blindness','E0 snapshot network SNR convention preserved; GR O4a historical TGR medians added beside earlier artifacts','Candidates only: E2 must state corpus cutoff, external-release audit scope and blindness handling before test access','No E2/E3 executed, no nuisance refit, no reading chosen'],
 'source_hashes':sources,'code_sha256':sha(Path(__file__))}
dump('CALIBRATION_AND_CANDIDATE_CENSUS.json',data)
doc=['# Censo independente — calibração e candidatos antes de E2','', '[REAL — conjuntos/índices/metadados conferidos; INPUT — elegibilidade; OPEN — ausência universal e cegamento]', '',
 '**Conferido: 33 HDF no pSEOB do record21454847; 18 produtos GWTC3; 12 eventos sobrepostos; união de39 eventos únicos, em51 produtos.** O número39 não pertence ao tar pSEOB do GWTC5. Nomes do índice, recibo de extração e esquema coincidem nos33; hashes declarados e tamanhos se encadeiam. O censo não reabriu valores HDF5 nem rehasheou os grandes binários.', '',
 'Calibração exposta inclui todos33+18, inclusive controles excluídos de combinações31/10. Esses eventos não se tornam cegos por terem sido excluídos de um resultado. A preferência pelo produto GWTC5 em duplicatas é organização do censo; não foi calculada likelihood de união nem multiplicados posteriores sobrepostos.', '',
 '| corrida | SNR≥12 | com220 no corpus | ausentes no corpus | elegíveis INPUT | elegíveis com220 | candidatos elegíveis ausentes | aguardando GR |',
 '|---|---:|---:|---:|---:|---:|---:|---:|']
for run,c in census.items():doc.append(f"|{run}|{c['SNR_ge12']}|{c['published_in_audited_corpus']}|{c['absent_from_audited_corpus']}|{c['eligible_INPUT']}|{c['eligible_with_archived_220']}|{c['eligible_absent_from_audited_corpus']}|{c['awaiting_GR']}|")
doc+=['', '## Os13 candidatos O4b no corpus auditado','', '| evento | SNR GWOSC | mediana Mf_det/M☉ | mediana chi_f |','|---|---:|---:|---:|']
for r in tables:
    if r['event'] in cb['candidate_events']:doc.append(f"|{r['event']}|{r['SNR_network_GWOSC']:g}|{r['GR_final_mass_detector_median']:g}|{r['GR_final_spin_median']:g}|")
doc+=['', '**O4b:45−14=31 ausentes antes do corteGR; 27−14=13 candidatos elegíveis depois dele.** O evento O4b sem metadadosGR, GW241230_233618, permanece aguardando. Não se conta como aprovado ou reprovado. Os17 valores conhecidos que não passam foram mantidos no JSON.', '',
 'O adendo O4a acrescenta17 elegíveis, dos quais7 possuem posterior no corpus e10 são candidatos por ausência nesse corpus: '+', '.join(census['O4a']['candidate_events'])+'. Há6 O4a ainda aguardandoGR. GW250207_115645 segue aguardandoGR, sem certificação de elegibilidade por substituição de chi_eff.', '',
 'Nenhum dos candidatos elegíveis desta interseção alcança a prioridade SNR≥30. Esse fato não muda o corte mínimo≥12. A lista completa39 de calibração, os12 duplicados, os6 exclusivos antigos e todas as74 linhas O4 com SNR≥12 estão no JSON.', '',
 '## Limite de ausência e uso antes de E2','',
 '**Ausente dos dois corpora pSEOB pinados não equivale a nunca publicado em qualquer lugar.** Não fiz busca universal de todas as releases/estudos, não certifico cegamento e não abri posteriores de candidatos. Estatutos `universal_never_published=null`, `blindness_certified=false` e `E2_registered=false` permanecem explícitos. O registro E2 deve fixar o universo de consulta/corte temporal e como tratar eventual posterior externo/exposição anterior; este censo não o substitui.', '',
 'Bases: snapshot GWOSC do E0, critérios INPUT adotados, TGR5 tabelas2–3 e adendo TGR4III tabela1. A SNR da tabela histórica não substituiu a SNR GWOSC. Fontes/arrays originais preservados. Código `check_calibration_candidate_census.py`, JSON homônimo de resultados e `CENSUS_RECEIPT.json` registram hashes e escopo de conferência.', '']
with (O/'CALIBRATION_AND_CANDIDATE_CENSUS.md').open('xb') as f:f.write('\n'.join(doc).encode())
require(all(sha(B/p)==v['sha256'] for p,v in sources.items()),'Input changed')
dump('CENSUS_RECEIPT.json',{'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_READONLY_CORPUS_CENSUS','wall_seconds':time.perf_counter()-start,'code_sha256':sha(Path(__file__)),'outputs':{n:{'sha256':sha(O/n),'bytes':(O/n).stat().st_size} for n in ['CALIBRATION_AND_CANDIDATE_CENSUS.json','CALIBRATION_AND_CANDIDATE_CENSUS.md']},'sources_unchanged':True,'posterior_values_accessed':False})
print(json.dumps({'corpus_products':51,'unique_events':39,'O4b':cb,'O4a':census['O4a'],'seconds':time.perf_counter()-start}))
