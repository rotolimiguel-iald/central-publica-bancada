"""Verify documentary corrections only; preserve original reviewed bytes."""
from pathlib import Path
import json,hashlib,datetime
from audit_provenance import OUT,atomic,metadata
ROOT=OUT.parent
review=json.loads((OUT/'REVISAO_CONSOLIDACAO_F0_F2.json').read_bytes())
sources=[];snapshots=[]
for name in ['ENTREGA_018_F0_RANKING.md','F0_RANKING_REGISTRY.json','ENTREGA_018_F2_DERIVACOES.md']:
 old=next(r for r in review['sources'] if Path(r['path']).name==name)
 candidates=[ROOT/name]+sorted(ROOT.glob(name+'.bak_*'))
 found=None
 for candidate in candidates:
  raw=candidate.read_bytes()
  if hashlib.sha256(raw).hexdigest()==old['sha256']:found=(candidate,raw);break
 assert found is not None,'Original reviewed bytes not found: '+name
 dest=OUT/('SNAPSHOT_ORIGINAL_'+name)
 if not dest.exists():atomic(dest,found[1])
 assert dest.read_bytes()==found[1]
 snapshots.append({'file':name,'original_reviewed_sha256':old['sha256'],'recovered_from':str(found[0]),'snapshot_path':str(dest),'bytes':len(found[1])})
def read(name):
 p=ROOT/name;meta,b=metadata(p);sources.append(meta);return b
f0=read('ENTREGA_018_F0_RANKING.md').decode('utf-8');registry=json.loads(read('F0_RANKING_REGISTRY.json'));f2=read('ENTREGA_018_F2_DERIVACOES.md').decode('utf-8');generator=read('consolidate_deliveries.py').decode('utf-8')
line0=next(l for l in f0.splitlines() if '**R-F ' in l);line2=next(l for l in f2.splitlines() if l.startswith('| R-F |'));rf=next(r for r in registry['routes'] if r['route']=='R-F')
s4=next(l for l in f0.splitlines() if 'cenário histórico CMB-S4' in l)
checks={
 'CONS01_BBN_explicit':'relação de consistência BBN' in s4 and 'sigma=0,09' in s4,
 'CONS01_theory_not_data_reuse':'dependência teórica não prova reutilização' in s4,
 'CONS02_F0_hypotheses':all(s in line0 for s in ['mesmo H','redshift geométrico usual','expansão adiabática']),
 'CONS02_F2_hypotheses':all(s in line2 for s in ['mesmo H','redshift geométrico usual','expansão adiabática','identidade de traço sozinha']),
 'CONS02_registry_hypotheses':all(s in rf['prediction'] for s in ['mesmo H','redshift geométrico usual','expansão adiabática']),
 'generator_has_BBN_and_adiabaticity':all(s in generator for s in ['relação de consistência BBN','sigma=0,09','redshift geométrico usual','expansão adiabática']),
 'all_registry_fields_in_current_F0':all(r[k] in f0 for r in registry['routes'] for k in ['prediction','statute','data','separation','decision','map'])}
# Adendum arithmetic and file identity only, without reading HTML scientific content.
p=json.loads(read('F0_ACT_DR2_PROTOCOL.json'));a=json.loads(read('F0_ACT_DR2_RESULT.json'))
checks['ACT_protocol_pin']=hashlib.sha256((ROOT/'F0_ACT_DR2_PROTOCOL.json').read_bytes()).hexdigest()==a['protocol']['sha256']
html_path=Path(p['source']['path']);meta,b=metadata(html_path);sources.append(meta);checks['ACT_archived_HTML_identity']=meta['sha256']==p['source']['sha256']
checks['ACT_ratio_arithmetic']=abs(a['delta_neff']/p['sigma_Neff']-a['expected_separation'])<1e-12
updates=[u for u in registry.get('source_updates',[]) if u.get('combination')=='P-ACT-LB_DR2']
checks['ACT_update_not_independent']=len(updates)==1 and updates[0].get('not_independent') is True
checks['ACT_result_pin_registry']=len(updates)==1 and hashlib.sha256((ROOT/'F0_ACT_DR2_RESULT.json').read_bytes()).hexdigest()==updates[0]['result']['sha256']
resolution={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Text corrections and arithmetic of supplied ACT DR2 adendum only; no centres, rites, fits, network or author script execution','sources':sources,'original_snapshots':snapshots,'checks':checks,'findings_resolution':{'CONS-01':'RESOLVED' if checks['CONS01_BBN_explicit'] and checks['CONS01_theory_not_data_reuse'] else 'OPEN','CONS-02':'RESOLVED' if all(v for k,v in checks.items() if k.startswith('CONS02')) else 'OPEN'},'registry_text_difference':[{'route':r['route'],'field':k,'value':r[k]} for r in registry['routes'] for k in ['prediction','statute','data','separation','decision','map'] if r[k] not in f0],'ACT_DR2':{'sigma':p['sigma_Neff'],'D':a['expected_separation'],'archived_identity_checked':True,'source_content_independently_reopened':False,'primary_read_status':'parent source reading DECLARADO to this bounded review; byte identity and arithmetic REAL'},'all_checks_pass':all(checks.values())}
atomic(OUT/'REVISAO_CONSOLIDACAO_F0_F2_CORRECOES.json',json.dumps(resolution,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':checks,'resolution':resolution['findings_resolution'],'registry_text_difference':resolution['registry_text_difference'],'snapshots':len(snapshots)},ensure_ascii=False,indent=2))
