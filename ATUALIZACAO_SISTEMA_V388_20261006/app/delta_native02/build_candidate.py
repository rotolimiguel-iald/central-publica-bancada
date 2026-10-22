"""Offline reversible transport compaction; never calls a provider or imports um.py."""
from pathlib import Path
import hashlib, json, os, re, sys, uuid
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
W=D.parent
S=W/'memory_stage'
sys.path.insert(0,str(W/'memory_build'))
import haiku_codec as codec
TAGS={'@TBL','@PATH'}
MARKER=codec.MARKER
NOTE=('\nTRANSPORTE NATIVO02 REVERSÍVEL: @TBL contém columns e rows; reconstruir cada objeto '
      'associando as colunas aos valores da linha, na ordem. Em fields, @PATH contém prefix e values; '
      'concatenar prefix a cada chave de values, conservando os valores literais e a ordem. '
      'São apenas abreviações de estrutura, sem inferência, tradução ou omissão de conteúdo científico. '
      'As remissões @/@F/@I/@L/@B/@EXPOSITION/@SUMMARY anteriores mantêm exatamente seu alcance.\n')
def need(ok,message):
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'),allow_nan=False)
def read_pin(path):
    b=Path(path).read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':sha(b)}
def fresh(path,b):
    path=Path(path)
    if path.exists():
        need(path.read_bytes()==b,'Existing output differs; preserve it and create a successor')
        return
    tmp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    need(tmp.read_bytes()==b,'Temporary bytes differ')
    tmp.rename(path)
def json_bytes(v):return (json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def collision(v):
    if isinstance(v,dict):
        need(not TAGS.intersection(v),'Reserved native02 key in source')
        for x in v.values():collision(x)
    elif isinstance(v,list):
        for x in v:collision(x)
def encode(v,changes,path=''):
    if isinstance(v,list):
        out=[encode(x,changes,path+'/'+str(i)) for i,x in enumerate(v)]
        if len(out)>=3 and all(isinstance(x,dict) for x in out) and all(list(x)==list(out[0]) for x in out):
            columns=list(out[0])
            table={'@TBL':{'columns':columns,'rows':[[x[k] for k in columns] for x in out]}}
            gain=len(dump(out).encode())-len(dump(table).encode())
            if gain>100:
                changes.append({'kind':'homogeneous_table','pointer':path,'columns':columns,'row_count':len(out),'saved_bytes':gain})
                return table
        return out
    if not isinstance(v,dict):return v
    out={k:encode(x,changes,path+'/'+k.replace('~','~0').replace('/','~1')) for k,x in v.items()}
    fields=out.get('fields')
    if isinstance(fields,dict) and len(fields)>=3 and all(isinstance(k,str) and k.startswith('/') for k in fields):
        keys=list(fields)
        prefixes=set()
        for key in keys:
            bits=key.split('/')
            prefixes.update('/'.join(bits[:i])+'/' for i in range(2,len(bits)))
        choices=[]
        for prefix in sorted(prefixes):
            matches=[i for i,k in enumerate(keys) if k.startswith(prefix)]
            if len(matches)<3 or matches!=list(range(matches[0],matches[-1]+1)):continue
            block={'@PATH':{'prefix':prefix,'values':{keys[i][len(prefix):]:fields[keys[i]] for i in matches}}}
            new={}
            for i,k in enumerate(keys):
                if i==matches[0]:new.update(block)
                elif i not in matches:new[k]=fields[k]
            gain=len(dump(fields).encode())-len(dump(new).encode())
            if gain>100:choices.append((gain,prefix,new,matches))
        if choices:
            gain,prefix,new,matches=max(choices,key=lambda row:(row[0],row[1]))
            out['fields']=new
            changes.append({'kind':'contiguous_pointer_prefix','pointer':path+'/fields','prefix':prefix,'field_count':len(matches),'saved_bytes':gain})
    return out
def decode(v):
    if isinstance(v,list):return [decode(x) for x in v]
    if not isinstance(v,dict):return v
    if '@TBL' in v:
        need(set(v)=={'@TBL'} and isinstance(v['@TBL'],dict),'Malformed table')
        t=v['@TBL'];need(set(t)=={'columns','rows'},'Table schema')
        cols=t['columns'];rows=t['rows']
        need(isinstance(cols,list) and all(isinstance(k,str) for k in cols) and len(set(cols))==len(cols),'Duplicate/malformed columns')
        need(isinstance(rows,list) and all(isinstance(row,list) and len(row)==len(cols) for row in rows),'Row width')
        return [{k:decode(x) for k,x in zip(cols,row)} for row in rows]
    out={}
    for key,item in v.items():
        if key=='@PATH':
            need(isinstance(item,dict) and set(item)=={'prefix','values'},'Path schema')
            prefix=item['prefix'];vals=item['values']
            need(isinstance(prefix,str) and prefix.startswith('/') and prefix.endswith('/') and isinstance(vals,dict),'Path prefix')
            for suffix,value in vals.items():
                full=prefix+suffix
                need(full not in out and full not in v,'Path collision')
                out[full]=decode(value)
        else:
            need(key not in out,'Duplicate decoded key')
            out[key]=decode(item)
    return out
def protected_spans(text,manifest):
    spans=[]
    for key in ('mother_instruction','operational_core'):
        row=manifest[key];b=Path(row['path']).read_bytes()
        need(sha(b)==row['sha256'],'Fixed memory pin mismatch')
        value=b.decode('utf-8-sig')
        need(text.count(value)==1,'Fixed memory occurrence')
        start=text.index(value);spans.append((start,start+len(value)))
    return spans
def convert(text,manifest):
    need(NOTE not in text,'Already converted')
    split=text.index(MARKER)
    fixed=protected_spans(text,manifest)
    output=[];offset=0;records=[]
    for line_number,line in enumerate(text.splitlines(keepends=True),1):
        new=line
        protected=offset>=split or any(a<=offset<b or offset<a<offset+len(line) for a,b in fixed)
        if not protected and line.startswith('{'):
            ending='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
            content=line[:-len(ending)] if ending else line
            try:value=codec.strict_json(content)
            except ValueError:value=None
            if isinstance(value,dict):
                collision(value)
                # Exact JSON byte restoration; skip noncanonical serialization.
                if dump(value)==content:
                    changes=[];encoded=encode(value,changes)
                    if changes and len(dump(encoded).encode())<len(content.encode()):
                        need(dump(decode(encoded))==content,'Roundtrip differs')
                        new=dump(encoded)+ending
                        records.append({'line':line_number,'original_sha256':sha(line.encode()),'candidate_sha256':sha(new.encode()),'original_bytes':len(line.encode()),'candidate_bytes':len(new.encode()),'changes':changes})
        output.append(new);offset+=len(line)
    packed=''.join(output)
    first=packed.index('\n')
    packed=packed[:first+1]+NOTE+packed[first+1:]
    return packed,records
def restore(text):
    need(text.count(NOTE)==1,'Transport note absent/ambiguous')
    text=text.replace(NOTE,'',1)
    out=[]
    for line in text.splitlines(keepends=True):
        if line.startswith('{') and ('"@TBL"' in line or '"@PATH"' in line):
            ending='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
            line=dump(decode(codec.strict_json(line)))+ending
        out.append(line)
    return ''.join(out)
def source_pins():
    paths=[S/'haiku_prefix.md',S/'haiku_provenance.json',S/'haiku_transport_fit.json',
           S/'manifest_staged.json',W/'COUNT_PLAN.json',W/'COUNT_STARTED.json',W/'COUNT_RESULT.json',
           W/'REVIEW_MANIFEST.json',W/'delta_app01/REVIEW_MANIFEST.json',
           W/'delta_app01/install_plan_candidate.json',W/'memory_build/haiku_codec.py',
           W/'memory_build/fit_transport.py',W/'memory_build/package_native.py']
    return [read_pin(p) for p in paths]
def main():
    baseline=source_pins()
    # Verify immutable scientific/application stage without importing its science.
    seals=[]
    for source in (W/'REVIEW_MANIFEST.json',W/'delta_app01/REVIEW_MANIFEST.json'):
        manifest=json.loads(source.read_bytes())
        for row in manifest.get('members',manifest.get('files',[])):
            p=Path(row['path']);actual=read_pin(p)
            need(actual['bytes']==row['bytes'] and actual['sha256']==row['sha256'],'Sealed member drift: '+str(p))
            seals.append(actual)
    raw=(S/'haiku_prefix.md').read_bytes();text=raw.decode('utf-8')
    native=json.loads((W/'COUNT_RESULT.json').read_bytes())
    need(sha(raw)==native['draft_sha256'],'Count/prefix binding')
    manifest=json.loads((S/'manifest_staged.json').read_bytes())
    candidate,records=convert(text,manifest)
    need(restore(candidate).encode()==raw,'Whole-prefix byte roundtrip')
    data=json.loads(Path(next(x for x in manifest['entries'] if x['id']=='resultado_publicado_integral')['path']).read_bytes())
    headings=lambda s:[m.group(1) for m in re.finditer(r'(?m)^### ([^\n]+)\n',s) if m.group(1) in data['core']]
    need(headings(text)==headings(candidate) and len(headings(text))==377,'Topic coverage')
    current=Path(r'C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json')
    installed=json.loads(current.read_bytes())
    previous=json.loads(Path(next(x for x in installed['entries'] if x['id']=='resultado_publicado_integral')['path']).read_bytes())
    new_topics=sorted(set(data['core'])-set(previous['core']))
    cache=Path(r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
    old_proxy=codec.offline_tokens(text,cache);new_proxy=codec.offline_tokens(candidate,cache)
    ratio=native['budget']['permanent_tokens']/old_proxy
    inferred=round(new_proxy*ratio)
    all_pins=baseline+[read_pin(Path(manifest[k]['path'])) for k in ('mother_instruction','operational_core')]
    for row in seals+all_pins:
        actual=read_pin(row['path']);need(actual==row,'Input changed during build')
    status='NOT_EXPECTED_TO_FIT_NATIVE_GATE__DO_NOT_RECOUNT_WITHOUT_REDESIGN_OR_ROOT_DECISION'
    receipt={'schema':'iald.haiku.native02.local_projection.v1','status':status,'builder':read_pin(Path(__file__)),
        'original_prefix':read_pin(S/'haiku_prefix.md'),'candidate_sha256':sha(candidate.encode()),'candidate_bytes':len(candidate.encode()),
        'transformed_json_lines':len(records),'transformation_records':records,'full_prefix_roundtrip_byte_exact':True,
        'representation_only':True,'removed_scientific_fields':0,'added_external_omissions':0,'topic_count':377,
        'topic_order_unchanged':True,'new_topics_relative_to_installed_release':new_topics,'new_topics_count':len(new_topics),
        'original_projection_limit':'Existing source omissions/remissions remain; this roundtrip preserves the original projection, not a claim the full corpus fits in context.',
        'mother_and_core_exact':True,'exposition_bytes_unchanged':candidate.partition(MARKER)[2]==text.partition(MARKER)[2],
        'formulas_hypotheses_status_verdicts_unchanged_after_decode':True,'canonical_source_and_full_cluster_unchanged':True,
        'offline_proxy':{'tokenizer':'o200k_base from verified local cache','original':old_proxy,'candidate':new_proxy,
                         'native_tokens':None,'native_fit_verified':False,'ratio_from_single_prior_measurement':ratio,
                         'native_estimate_UNVALIDATED':inferred,'remaining_estimate_UNVALIDATED':200000-inferred-1474-4096-1024,
                         'limit':'Tokenization ratio and overhead are not invariant; estimate is not a count.'},
        'required_native_range_if_1474_overhead':[180000,183406],'official_first_measurement_preserved':read_pin(W/'COUNT_RESULT.json'),
        'inputs':all_pins,'sealed_members_verified':len(seals),'network_requests':0,'generation_requests':0,'production_changed':False}
    fresh(D/'haiku_prefix.md',candidate.encode())
    fresh(D/'TRANSFORMATION_MAP.json',json_bytes(receipt))
    fresh(D/'SOURCE_PINS.json',json_bytes({'files':all_pins,'sealed_members_verified':len(seals)}))
    print(json.dumps({k:receipt[k] for k in ('status','candidate_sha256','candidate_bytes','transformed_json_lines','new_topics_count','offline_proxy')},ensure_ascii=False))
if __name__=='__main__':main()
