"""Search current scientific source text, deduplicated by bytes, without execution."""
import collections
import hashlib
import json
from pathlib import Path
import re
import survey_r58 as s

topics={
 'physical_two_point':re.compile(r'Wightman|two[- ]point|dois pontos|duas pontas|\bGNS\b|covariance.{0,20}(state|field)|circularSmear',re.I),
 'continuum':re.compile(r'limite.{0,20}cont.nu|continuum|inductive limit|limite indutivo|refinamento|coarse.grain|packetRefinement',re.I),
 'device_readout':re.compile(r'lock.in|homodin|heterodin|demodula|Jaynes|Rabi|MQC|supercondutor',re.I),
 'clock_link':re.compile(r'E_?ref|V_?0.{0,18}(hbar|ℏ)|retorno.{0,15}fase|[âa]ngulo de Miguel|kappa_is_input',re.I),
}
allowed_top={'Artigo','Central de Patentes','PROGRAMA_IALD','Bancada_Um','Patentes','observaveis_tgl','papers_latex','psinet','SkyGrid_Piloto','Dissertação','Base Referencial Completa TGL','IMac LA'}
excluded_parts={'cache','checkpoints','vault','evidencias','state','node_modules','.lake','mathlib','lean','third_party','site-packages','releases','scientific_memory','canonical_memory','public','vendor','corpus'}
counts=collections.Counter(); skipped=collections.Counter(); by_top=collections.Counter(); errors=[]; seen={}; pins=[]
with (s.ROOT/'CURRENT_SOURCE_MATCHES.jsonl').open('x',encoding='utf-8',newline='\n') as out:
 for line in (s.ROOT/'FILE_INVENTORY.jsonl').open(encoding='utf-8'):
    item=json.loads(line);p=Path(item['path']);rel=p.relative_to(s.BASE);parts={x.lower() for x in rel.parts}
    if item['top'] not in allowed_top and len(rel.parts)!=1: skipped['other_root']+=1;continue
    if item['kind']!='text' or p.suffix.lower() not in {'.lean','.py','.tex','.md','.txt','.rst'}: skipped['not_source_text']+=1;continue
    if item['historical'] or excluded_parts & parts: skipped['history_dependency_or_data']+=1;continue
    if any(x in str(p).lower() for x in ['\u005c.env','iald_psion_state','iald_stack_v7','credential','senha','chave da api']):skipped['protected']+=1;continue
    if item['bytes']>8*1024*1024: skipped['over_8MiB_agent_direct_read_or_unread']+=1;continue
    if item['top']=='Central de Patentes' and len(rel.parts)>1 and rel.parts[1] not in {'Chatgpt','work','memory'}: skipped['other_central_app_area']+=1;continue
    try:raw=p.read_bytes()
    except OSError as exc:errors.append({'path':str(p),'error':str(exc)});continue
    counts['files_hashed']+=1;counts['bytes_hashed']+=len(raw);digest=hashlib.sha256(raw).hexdigest()
    if digest in seen:counts['duplicate_bytes']+=1;continue
    seen[digest]=str(p)
    try:text=raw.decode('utf-8-sig')
    except UnicodeError: skipped['not_utf8']+=1;continue
    counts['unique_utf8_scanned']+=1;by_top[item['top']]+=1
    hits={}
    for name,rx in topics.items():
        allhits=list(rx.finditer(text))
        if allhits: hits[name]={'count':len(allhits),'examples':[{'line':text.count('\n',0,h.start())+1,'context':text[max(0,h.start()-100):h.end()+200]} for h in allhits[:2]]}
    if not hits:continue
    counts['unique_matching_sources']+=1
    row={'path':str(p),'sha256':digest,'bytes':len(raw),'topics':hits}
    out.write(json.dumps(row,ensure_ascii=False)+'\n')
    if len(hits)>=3:pins.append({'path':str(p),'sha256':digest,'bytes':len(raw),'topics':list(hits)})
s.new('CURRENT_SEARCH_RESULT.json',{'counts':dict(counts),'skipped_file_counts':dict(skipped),'by_top':dict(by_top),'errors':errors,
 'patterns':{k:v.pattern for k,v in topics.items()},'matches':s.pin(s.ROOT/'CURRENT_SOURCE_MATCHES.jsonl'),
 'scope':'Fresh local source search with exact hashes, byte duplicates collapsed. Search not semantic verification; large originals handled by direct readers and explicit exclusions.'})
s.new('CURRENT_CROSS_TOPIC_CANDIDATES.json',pins)
print(json.dumps({'counts':dict(counts),'candidate_sources':len(pins),'errors':len(errors)},ensure_ascii=False))
