"""Add existing published GR remnant metadata; no posterior/test data access."""
from pathlib import Path
from datetime import datetime, timezone
import re,json,hashlib,math,time,sys
from pypdf import PdfReader
B=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
D=B.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos'
sources={};start=time.perf_counter()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    raw=p.read_bytes();sources[str(p.resolve())]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()};return raw
def require(ok,msg):
    if not ok:raise ValueError(msg)
def dump(name,data):
    with (O/name).open('xb') as f:f.write((json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
for n in ['GR_O4A_ADENDO.json','GR_O4A_ADENDO.md','GR_O4A_RECEIPT.json']:require(not (O/n).exists(),'Existing '+n)
pdf=D/'arxiv_2603.19021_gwtc4_tgr3.pdf';read(pdf)
text=read(D/'gwtc4_tgr3.txt').decode('utf-8');reader=PdfReader(pdf)
pdf_rows={}
def values(s):return [float(x.replace('−','-')) for x in re.findall(r'[−-]?\d+(?:\.\d+)?',s)]
for pageno in [3,4]:
    parts=re.split(r'(GW23\d{4}\s+\d{6})',reader.pages[pageno-1].extract_text())
    for j in range(1,len(parts),2):
        event=re.sub(r'\s+','_',parts[j]); ns=values(parts[j+1])[:9]
        require(len(ns)==9 and ns[3]>0 and 0<=ns[6]<1 and ns[4]>=0 and ns[5]<=0,'Invalid row '+event)
        require(event not in pdf_rows,'Duplicate '+event)
        pdf_rows[event]={'event':event,'table':1,'pdf_page':pageno,'table_snr_not_used_for_selection':ns[0],
            'final_mass_detector':ns[3],'final_mass_upper_error':ns[4],'final_mass_lower_error':ns[5],
            'final_spin':ns[6],'final_spin_upper_error':ns[7],'final_spin_lower_error':ns[8],
            'source_pdf_sha256':sha(pdf),'source':'GWTC4 TGR III table1; GR catalog IMR baseline',
            'statute':'KNOWN_PUBLISHED_GR_BASELINE_NOT_NEW_MEASUREMENT','mass_frame':'detector (1+z)Mf in Msun','spin_type':'final dimensionless chi_f, not chi_eff',
            'intervals':'Published marginal central values with asymmetric errors; overlap with table2 explicitly identifies medians/symmetric90% credible intervals',
            'median_convention_documentary':'Table1 catalog central values; table2 IMR columns explicitly median and match all 22 overlapping events',
            'inspiral_only':False,'independent_of_strain':False,'deformation_fit_used':False,'median_rule_registered_in_E2':False}
require(len(pdf_rows)==42,'Expected 42 O4a table1 rows')
# Separately archived text extraction, isolated to the first table, cross-check all central/error columns.
firsttable=text[text.index('Table 1. Event selection table'):text.index('2. RINGDOWN TESTS')]
parts=re.split(r'(GW23\d{4}\s+\d{6})',firsttable);count=0
for j in range(1,len(parts),2):
    event=re.sub(r'\s+','_',parts[j]);nums=values(parts[j+1])[:9];r=pdf_rows[event]
    require(nums[3:9]==[r[k] for k in ['final_mass_detector','final_mass_upper_error','final_mass_lower_error','final_spin','final_spin_upper_error','final_spin_lower_error']],'Independent extraction disagreement '+event);count+=1
require(count==42,'Archived text coverage')
# Table2 IMR columns, explicitly GR baseline and median/90% in caption; never Kerr recovery columns.
parts=re.split(r'(GW23\d{10})',reader.pages[6].extract_text());overlap=[]
for j in range(1,len(parts),2):
    event=parts[j][:8]+'_'+parts[j][8:]; ns=values(parts[j+1]);r=pdf_rows[event]
    require(ns[1:4]==[r['final_mass_detector'],r['final_mass_upper_error'],r['final_mass_lower_error']],'IMR mass disagreement '+event)
    require(ns[10:13]==[r['final_spin'],r['final_spin_upper_error'],r['final_spin_lower_error']],'IMR spin disagreement '+event)
    overlap.append(event)
require(len(overlap)==22,'Table2 overlap count')
draft=json.loads(read(B/'bis/e0_metadata/GR_METADATA_DRAFT_REVIEW.json'))
inventory=json.loads(read(B/'bis/e0_metadata/GWOSC_INVENTORY.json'))
old={r['event']:r for r in draft['events']};rows=[]
for e in inventory['events']:
    if not e['run'].startswith('O4'):continue
    r=old[e['event']];meta=r['gr_metadata'];newmeta=pdf_rows.get(e['event']) if e['run']=='O4a' else None
    require(not(meta and newmeta),'Do not silently override existing GR metadata')
    if newmeta:meta=newmeta
    rho=e['network_matched_filter_snr'];known=meta is not None and rho is not None
    eligible=(rho>=12 and meta['final_mass_detector']>=40 and 0<=meta['final_spin']<.98) if known else None
    rows.append({'event':e['event'],'run':e['run'],'GWOSC_version_key':e['version_key'],'SNR_network_GWOSC':rho,
        'metadata_origin':'GWTC4_TGR_III_table1' if newmeta else ('GWTC5_TGR_tables2_3' if meta else None),
        'GR_metadata':meta,'metadata_status':'GR_BASELINE_AVAILABLE' if meta else 'AWAITING_GR_METADATA',
        'adopted_INPUT_eligibility':eligible,'priority_SNR30':rho>=30 if rho is not None else None,
        'decision_scope':'INPUT E0.3 only; not E2/test-set registration or LVK pSEOB split-SNR eligibility',
        'fresh_GR_metadata_added':newmeta is not None,
        'mass90_interval_crosses40':meta['final_mass_detector']+meta['final_mass_lower_error']<40<=meta['final_mass_detector']+meta['final_mass_upper_error'] if meta else None,
        'selection_uses_interval':False,'posterior_accessed':False})
summary={}
for run in ['O4a','O4b','O4c_discovery_only','O4_public_total']:
    rr=[r for r in rows if r['run']==run or run=='O4_public_total'];rr=[r for r in rr if r['SNR_network_GWOSC'] is not None and r['SNR_network_GWOSC']>=12]
    summary[run]={'SNR_ge12':len(rr),'GR_available':sum(r['GR_metadata'] is not None for r in rr),'INPUT_pass':sum(r['adopted_INPUT_eligibility'] is True for r in rr),
        'INPUT_known_fail':sum(r['adopted_INPUT_eligibility'] is False for r in rr),'awaiting_GR':sum(r['GR_metadata'] is None for r in rr),
        'pass_events':[r['event'] for r in rr if r['adopted_INPUT_eligibility'] is True],
        'awaiting_events':[r['event'] for r in rr if r['GR_metadata'] is None],
        'known_fail_events':[r['event'] for r in rr if r['adopted_INPUT_eligibility'] is False],
        'priority_eligible_events':[r['event'] for r in rr if r['adopted_INPUT_eligibility'] is True and r['priority_SNR30']]}
require(summary['O4_public_total']['SNR_ge12']==74,'Snapshot count')
data={'utc':datetime.now(timezone.utc).isoformat(),'status':'ADDITIVE_GR_O4A_METADATA_AND_ADOPTED_INPUT_APPLICATION__NO_E2_REGISTRATION',
 'source_reading_scope':'Existing GWTC4 TGR III PDF pp1,3,4,5,6,7, table1 O4a rows and table2 IMR columns/caption; not whole paper. No new downloads or posterior access.',
 'validation':{'table1_O4a_rows':42,'PDF_versus_archived_text_compared_fields':42*6,'table2_explicit_IMR_median_rows':len(overlap),'table2_events':overlap},
 'source_convention':'Table1 takes binary parameters from each run catalog; table2 overlap proves exact equality of Mf_det/chi_f and errors with explicitly labeled GR full-IMR medians. Physical baseline is GR; pre-deformation does not mean inspiral-only or independent data.',
 'scope_caveats':['Snapshot GWOSC metadata from E0; no update of SNR or catalog versions in this adendum','Old GWTC4.0 TGR baseline values joined to E0 preferred GWOSC versions; no claim that these are newly recomputed medians for GWTC4.1','Some old TGR SNRs are below12 even when preferred GWOSC total is >=12; keep chosen GWOSC convention','Missing old-table rows remain awaiting, including single-detector event excluded by paper; absence is not physics failure','No fuzzy event-name matching; similarly dated events distinct','Eligibility uses medians by adopted INPUT, not credible-bound or posterior-width cuts','No table of deformation posteriors read for new test events'],
 'criteria':{'SNR_network_min_inclusive':12,'Mf_detector_median_min_inclusive_Msun':40,'chif_median_min_inclusive':0,'chif_median_max_exclusive':.98,'priority_SNR_network_min':30,'missing_status':'AWAITING_GR_METADATA','statute':'INPUT_USER_ADOPTED'},
 'summary':summary,'all_42_added_table_rows':list(pdf_rows.values()),'O4_snapshot_rows':rows,'source_hashes':sources,'code_sha256':sha(Path(__file__))}
dump('GR_O4A_ADENDO.json',data)
doc=['# Adendo — metadados GR de O4a','', '[KNOWN — propriedades GR publicadas; REAL — extração/conferência; INPUT — corte adotado]', '',
 'Acrescentadas **42 linhas O4a** da Tabela1 do [GWTC-4.0 TGR III](https://arxiv.org/abs/2603.19021), sem posterior, strain ou PE. A extração PDF concorda nos 252 campos de massa/spin/erros com o texto arquivado. As 22 linhas comuns à Tabela2 coincidem com suas colunas **IMR**, explicitamente medianas e intervalos de90%; não foram usadas as colunas de recuperação Kerr/pyRing. Massas são remanescentes no referencial do detector, (1+z)Mf, e spin é chi_f.', '',
 'A Tabela1 remete aos parâmetros dos catálogos GR; sua convenção de centralidade é corroborada pela identidade com as 22 linhas IMR da Tabela2. São dados de pré-deformação sob GR completo, não inspiral isolada nem medidas independentes do mesmo strain. O adendo preserva a origem histórica GWTC4.0 TGR: não promete reanálise desses remanescentes na versão preferida GWTC4.1 do GWOSC.', '',
 '| corrida | SNR GWOSC≥12 | com GR | passa INPUT | não passa, GR conhecido | aguarda GR |','|---|---:|---:|---:|---:|---:|']
for run,s in summary.items():doc.append(f"|{run}|{s['SNR_ge12']}|{s['GR_available']}|{s['INPUT_pass']}|{s['INPUT_known_fail']}|{s['awaiting_GR']}|")
doc += ['', 'Critério aplicado: SNR de rede GWOSC≥12, mediana Mf_det≥40 M☉, 0≤mediana chi_f<0,98; prioridade≥30. As decisões são aplicação do INPUT adotado, não registro E2 nem seleção LVK por inspiral/pós-inspiral. Intervalos que atravessam40 são marcados, sem mudar a regra da mediana.', '',
 'O4a ainda aguardando GR no universo SNR≥12: '+', '.join(summary['O4a']['awaiting_events'])+'.', '',
 'O4a que passa o INPUT: '+', '.join(summary['O4a']['pass_events'])+'.', '',
 'SNRs da tabela histórica são preservados apenas como referência. Usa-se o snapshot GWOSC do E0, inclusive quando cruza12 diferentemente do SNR antigo. Eventos de nomes parecidos não foram fundidos. GW230814_230901, omitido pelo artigo por ser de um detector, não é GW230814_061920. A ausência de uma linha não significa reprovação física ou aceitação; permanece AWAITING_GR_METADATA.', '',
 'O rascunho GR anterior e o selo E0 permanecem intactos. Este adendo traz JSON com todos os nomes/valores/fontes, código e recibo de hashes. Leitura pontual das páginas declaradas; nenhuma leitura integral reivindicada. Nenhuma largura de deformação entrou na seleção, e nenhum dado de teste foi aberto.', '']
with (O/'GR_O4A_ADENDO.md').open('xb') as f:f.write('\n'.join(doc).encode())
require(all(sha(Path(p))==v['sha256'] for p,v in sources.items()),'Input mutated')
dump('GR_O4A_RECEIPT.json',{'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_DOCUMENTARY_EXTRACTION','python_optimize':sys.flags.optimize,'wall_seconds':time.perf_counter()-start,'code_sha256':sha(Path(__file__)),'outputs':{n:{'sha256':sha(O/n),'bytes':(O/n).stat().st_size} for n in ['GR_O4A_ADENDO.json','GR_O4A_ADENDO.md']},'input_bytes_unchanged':True,'posterior_or_strain_read':False})
print(json.dumps({'status':data['status'],'summary':summary,'seconds':time.perf_counter()-start}))
