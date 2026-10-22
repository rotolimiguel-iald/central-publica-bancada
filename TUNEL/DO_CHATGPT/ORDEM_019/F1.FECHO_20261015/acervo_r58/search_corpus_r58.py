"""Search the existing extracted corpus locally; no external calls."""
import collections
import hashlib
import json
from pathlib import Path
import re
import survey_r58 as s

PATTERNS = {
    'two_point': r'Wightman|Hadamard|\bGNS\b|two[- ]point|dois pontos|duas pontas|correla.{0,25}(v.cuo|campo|espacial)',
    'continuum': r'limite.{0,25}cont.nu|continuum|inductive limit|limite indutivo|refinamento|coarse.grain|rede.{0,25}(cont.nua|qu.ntica)',
    'readout': r'lock.in|homodin|heterodin|demodula|receptor|Jaynes|Rabi|calibra.{0,25}(tempo|rel.gio|fase)',
    'clock_gravity': r'primeira lei|c\s*\^\s*3|c³|c\*\*3|retorno.{0,25}fase|V_?0.{0,20}(hbar|ℏ)|E_?ref|[âa]ngulo de Miguel',
    'modular_horizon': r'Takesaki|Clausius|Jacobson|Bisognano|KMS|horizonte.{0,25}(local|nulo)',
    'conservation': r'conserva.{0,30}(tensor|energia)|stress.{0,10}tensor|MaxwellCertificate|StressTensorData|Einstein.Cart',
}
rxs = {k: re.compile(v, re.I) for k,v in PATTERNS.items()}
index_path = Path(r'C:\IALD\INDICE_DO_ACERVO\corpus_index.json')
index = json.loads(index_path.read_text(encoding='utf-8'))
counts = collections.Counter(); topic_counts = collections.Counter(); by_top = collections.Counter(); errors=[]; seen={}; candidates=[]
with (s.ROOT/'CORPUS_MATCHES.jsonl').open('x', encoding='utf-8', newline='\n') as out:
    for item in index['itens']:
        path = Path(item['path']); lowered=str(path).lower()
        if not lowered.startswith('c:\\iald\\') or item.get('status') != 'OK': continue
        rel = path.relative_to(s.BASE)
        if rel.parts[0].lower() in s.PRIVATE_ROOTS or any(x.lower() in {'escritorio', 'advocacia'} for x in rel.parts): continue
        if path.name.lower() in s.SECRET_NAMES or path.name.lower().startswith(('.env','iald_psion_state')): continue
        counts['eligible_documents'] += 1
        try: raw=Path(item['corpus']).read_bytes(); text=raw.decode('utf-8')
        except (OSError, UnicodeError) as exc: errors.append({'path':str(path),'error':str(exc)});continue
        digest=hashlib.sha256(raw).hexdigest()
        counts['read_extractions']+=1; counts['extraction_bytes']+=len(raw)
        if digest in seen:
            counts['duplicate_extractions']+=1
            continue
        seen[digest]=str(path)
        matches={}
        for topic,rx in rxs.items():
            hits=list(rx.finditer(text))
            if not hits: continue
            topic_counts[topic]+=1
            matches[topic]={'count':len(hits),'examples':[{'extracted_line':text.count('\n',0,h.start())+1,
                'context':text[max(0,h.start()-160):h.end()+240]} for h in hits[:3]]}
        if not matches:continue
        row={'original':str(path),'indexed_mtime':item.get('mtime'),'extraction':item['corpus'],
            'extraction_sha256':digest,'topics':matches,'original_exists':path.exists()}
        out.write(json.dumps(row,ensure_ascii=False)+'\n');counts['matching_unique_documents']+=1;by_top[rel.parts[0]]+=1
        if len(matches)>=3 and not any(x in lowered for x in ['\\memory\\','\\.claude\\','\\logs\\','\\backup','\\the_boundary\\']):
            candidates.append({'path':str(path),'topics':list(matches),'hit_counts':{k:v['count'] for k,v in matches.items()},'size':item.get('size'),'mtime':item.get('mtime')})
result={'index':s.pin(index_path),'index_date':index.get('gerado_em'),'patterns':PATTERNS,
        'counts':dict(counts),'topic_documents':dict(topic_counts),'by_top':dict(by_top),'errors':errors,
        'limitations':['Lexical search over dated extraction; not semantic proof or fresh full corpus. Originals must be read and hashed before citation.',
            'Equal extraction hashes deduplicated; dates are index mtime, not authorship/publication evidence.'],
        'matches':s.pin(s.ROOT/'CORPUS_MATCHES.jsonl')}
s.new('CORPUS_SEARCH_RESULT.json',result)
s.new('CROSS_TOPIC_CANDIDATES.json',sorted(candidates,key=lambda x:(-len(x['topics']),x['path'])))
print(json.dumps({'counts':dict(counts),'topic_documents':dict(topic_counts),'by_top':dict(by_top),'candidates':len(candidates)},ensure_ascii=False))
