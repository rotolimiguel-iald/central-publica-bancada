"""Draft provenance/coverage review of proposed GR metadata cut; no registration."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, math, re, collections
from pypdf import PdfReader
B=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
I=B.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,m):
    if not x:raise ValueError(m)
def new(name,x):
    with (O/name).open('xb') as f:f.write((json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
tpath=I/'gwtc5_tgr_table2_3_parsed.json';pdfpath=I/'arxiv_2607.19293_gwtc5_tgr.pdf'
old=json.loads(tpath.read_bytes());reader=PdfReader(pdfpath)
parts=re.split(r'(GW\d{6}\s+\d{6})','\n'.join(reader.pages[k].extract_text() for k in [3,4]))
parsed={}
for j in range(1,len(parts),2):
    event=re.sub(r'\s+','_',parts[j]);part=parts[j+1];ifos=re.search(r'\b(?:HLV|HL|HV|LV)\b',part)
    require(ifos is not None,event)
    ns=re.findall(r'[−-]?\d+(?:\.\d+)?',part[ifos.end():])
    require(len(ns)>=12,'Incomplete columns '+event)
    nums=[float(n.replace('−','-')) for n in ns[:12]]
    require(event not in parsed,'Duplicate event')
    parsed[event]=dict(chirp_mass_detector=nums[0],chi_eff=nums[3],final_mass_detector=nums[6],
        final_mass_upper_error=nums[7],final_mass_lower_error=nums[8],final_spin=nums[9],
        final_spin_upper_error=nums[10],final_spin_lower_error=nums[11])
require(len(old)==len(parsed)==77,'Coverage')
for r in old:
    v=parsed[r['event']]
    require([v[k] for k in ['chirp_mass_detector','chi_eff','final_mass_detector','final_spin']]==
        [float(r[k].replace('−','-')) for k in ['Mdet','chieff','Mf_det','chif']],r['event'])
    v['table']=r['table'];v['table_snr_NOT_USED_FOR_SELECTION']=r['snr']
inventory=json.loads((O/'GWOSC_INVENTORY.json').read_bytes());rows=[]
for e in inventory['events']:
    meta=parsed.get(e['event']);rho=e['network_matched_filter_snr']
    rows.append(dict(event=e['event'],run=e['run'],gwosc_version=e['version_key'],network_snr=rho,
        gr_metadata=meta,gr_metadata_status='GR_CATALOG_IMR_BASELINE_CONFIRMED_DOCUMENTALLY' if meta else 'AWAITING_GR_METADATA',
        proposed_input_would_pass=(rho>=12 and meta['final_mass_detector']>=40 and 0<=meta['final_spin']<.98) if meta and rho is not None else None,
        proposed_priority_snr30=(rho>=30) if rho is not None else None,
        adopted_eligibility=None,criterion_registered=False))
summary={}
for run in ['O1','O2','O3a','O3b','O4a','O4b','O4c_discovery_only','O4_public_total']:
    rs=[r for r in rows if r['run']==run or (run=='O4_public_total' and r['run'].startswith('O4'))]
    at12=[r for r in rs if r['network_snr'] is not None and r['network_snr']>=12]
    summary[run]=dict(snr_ge12=len(at12),gr_metadata_available=sum(r['gr_metadata'] is not None for r in at12),
        awaiting_gr_metadata=sum(r['gr_metadata'] is None for r in at12),
        would_pass_proposed_input=sum(r['proposed_input_would_pass'] is True for r in at12),
        would_not_pass_known_values=sum(r['proposed_input_would_pass'] is False for r in at12),
        awaiting_events=[r['event'] for r in at12 if r['gr_metadata'] is None],
        known_below_mass40=[r['event'] for r in at12 if r['gr_metadata'] is not None and r['gr_metadata']['final_mass_detector']<40])
fitpath=B/'bis/E0_SNR_INFORMATION_FIT.json';fit=json.loads(fitpath.read_bytes())
for path,h in fit['source_hashes'].items(): require(sha(B/path)==h,'Fit input hash '+path)
known={r['event']:r for r in inventory['events']}
for r in fit['metadata_join']:require(known[r['metadata_event']]['network_matched_filter_snr']==r['SNR_network'],'Fit SNR join')
inputs=[tpath,pdfpath,B/'cache/e0_metadata/gwtc5_catalog_dcc_v6.pdf',B/'cache/e0_metadata/gwtc5_introduction_v1.html',
    O/'GWOSC_INVENTORY.json',fitpath,Path(__file__)]
out=dict(status='DRAFT_FOR_USER_REVIEW__NOT_SELECTION_REGISTRATION',utc=datetime.now(timezone.utc).isoformat(),
    gr_provenance=dict(tgr='arXiv2607.19293 section2 pp3-4 + Tables2-3 pp4-5: standard GW-catalog PE source properties',
        catalog='LIGO-P2600152-v6 section3 p12: baseline analyses before GR tests; standard IMR waveform families, default prior and median/90% intervals',
        conclusion='GR IMR baseline quantities, not estimates with dtau deformation fitted; not inspiral-only or statistically independent of the same strain',
        relation_status='KNOWN_SOURCE_MODEL_AND_DOCUMENTED_PROVENANCE; no new GR measurement',
        mass_frame='Detector/redshifted remnant mass (1+z)Mf directly from TGR table, not source mass or product of medians',
        spin_type='Dimensionless remnant final spin chi_f, not chi_eff',
        parser_warning='Historical Mdet field is REDSHIFTED CHIRP mass, not total or remnant mass. Use Mf_det only for proposed remnant-mass cut'),
    table_validation=dict(pdf_rows=77,parsed_json_rows=77,all_four_central_columns_match=True,table2_O4b=72,table3_new_O4a=5),
    proposal_INPUT_only=dict(network_snr_min=12,remnant_detector_mass_min_solar=40,final_spin_min_inclusive=0,final_spin_max_exclusive=.98,
        priority_network_snr_min=30,status='AWAITING_USER_REVIEW_NOT_REGISTERED',
        missing='AWAITING_GR_METADATA; decision null',
        uncertainty='Point-median proposal only; no credible-bound or probability rule chosen. Some mass intervals cross 40.'),
    by_run=summary,events=rows,
    fit_review_scope=dict(hashes_match=True,snr_joins_match=True,OLS_rerun=False,numerical_fit_approved=False,
        note='Inherited convention.sigma_fit_performed=false describes original metadata artifact, not this fit; root status explicitly says planning fit'),
    source_hashes={str(p):sha(p) for p in inputs})
new('GR_METADATA_DRAFT_REVIEW.json',out)
lines=['| corrida | SNR≥12 | com GR Mf/chi_f | aguardando | atenderia INPUT | não atenderia, valores conhecidos |','|---|---:|---:|---:|---:|---:|']
for k,r in summary.items():lines.append(f"| {k} | {r['snr_ge12']} | {r['gr_metadata_available']} | {r['awaiting_gr_metadata']} | {r['would_pass_proposed_input']} | {r['would_not_pass_known_values']} |")
report=f'''# Revisão da procedência GR — RASCUNHO PARA DECISÃO

[REAL documental; critério INPUT NÃO REGISTRADO; não é entrega nem seleção aprovada]

**A tabela fornece Mf e chi_f da análise padrão GR do catálogo, anterior ao ajuste de deformações.** §2 do [TGR](https://arxiv.org/abs/2607.19293), pp3–4, atribui essas propriedades à PE dos catálogos; o [catálogo primário, §3 p12](https://dcc.ligo.org/public/0206/P2600152/006/gwtc-5_results_noauthors_flattened.pdf) descreve a inferência IMR padrão como baseline para os testes de GR e identifica modelos/prior/resumos. Isso sustenta procedência **GR full-IMR**, não inspiral-only nem independência estatística do mesmo strain. Não são massas/spins obtidos deixando δτ livre. Leitura limitada às seções/tabelas indicadas.

Extraí diretamente do PDF as 77 linhas das Tabelas2–3 e comparei quatro medianas por linha: **308/308 coincidem** com o JSON recebido. São 72 eventos O4b e cinco O4a adicionais, não o catálogo inteiro. `Mf_det` é massa **final redshifted**, em Msol; `chif` é spin final adimensional. Atenção: `Mdet` no JSON antigo é **massa de chirp redshifted**, não massa total. GW250114: Mf_det=68,31 e chi_f=0,68; SNR da tabela76,9 fica só na proveniência, enquanto o corte continua com GWOSC78,6.

Sem adotar o critério, fiz apenas uma tabela de impacto do INPUT proposto: SNR≥12, mediana Mf_det≥40, 0≤mediana chi_f<0,98; prioridade SNR≥30. Não há uso de larguraδ ou de chi_eff como substituto. Toda ausência recebe `AWAITING_GR_METADATA` e decisão null. `adopted_eligibility` é null em todas as linhas.

{chr(10).join(lines)}

**A cobertura continua incompleta**, sobretudo para O4a antigo e a discovery O4c. Uma linha ausente da tabela TGR não falha física nem passa o corte. A própria tabela tem seleção para testes; sua disponibilidade não pode virar automaticamente seleção científica adicional. Intervalos publicados podem atravessar Mf=40 (p.ex. GW240428_225440: 38,27 +2,82/−0,93). A convenção por mediana foi apenas simulada para a decisão proposta; adotar quantil/probabilidade seria outra regra a registrar.

O fit `E0_SNR_INFORMATION_FIT.json`, SHA256 `{sha(fitpath)}`, foi lido: hashes das três fontes e associação SNR por evento conferem; **não refiz OLS/bootstrap nem aprovei o ajuste numericamente**. O campo herdado `convention.sigma_fit_performed=false` descreve o inventário de origem, não a execução do fit; convém contextualizá-lo no registro final.

Complementos documentais: a [documentação GWOSC5](https://gwosc.org/GWTC-5.0/) esclarece que o default de SNR usa PE quando disponível e, sem PE, a maior SNR das buscas. Mantemos uma convenção de catálogo, não um único estimador homogêneo. O catálogo primário, p28, prevê os resultados O4c em GWTC6, **sem data de publicação**. Isso documenta intenção, não lançamento.

O mapeamento por evento, incertezas, contagens e hashes estão no JSON ao lado. O manifesto anterior permanece intacto; as fontes adicionais têm recibos próprios em cache e um manifesto complementar. Nenhum posterior/strain novo, nenhuma alteração de E2, nenhuma publicação de critério.
'''
with (O/'GR_METADATA_DRAFT_REVIEW.md').open('xb') as f:f.write(report.encode())
extra=[p for p in (B/'cache/e0_metadata').glob('*.receipt.json') if p.name.startswith('gwtc5_')]
new('GR_ADDENDUM_MANIFEST.json',dict(status='DRAFT_DOCUMENTARY_ADDENDUM',files={str(p):sha(p) for p in inputs+[O/'GR_METADATA_DRAFT_REVIEW.json',O/'GR_METADATA_DRAFT_REVIEW.md']+extra}))
print(json.dumps(summary,ensure_ascii=False))
