"""Build only the wide v389 documentary candidate; no science, provider or activation."""
from pathlib import Path
import ast, base64, copy, difflib, hashlib, json, os, re, sys
from datetime import datetime, timezone

D = Path(__file__).resolve().parent
S = D / 'memory_stage'
SUP = D / 'build_support'
OLD = D.parent.parent / 'ATUALIZACAO_SISTEMA_V388_20261006/app'
OSRC = OLD / 'memory_stage'
CUSTODY = D.parent / 'devices/stage/vault/originals_copy/um_unificado_v389'
AUDIT = D.parent / 'science_audit/controller_static_20261006/AUDITORIA_V389.json'
APP = Path('C:/IALD/projetos_pyhton/IALD')
MARKER = '## Exposição canônica integral: fórmulas e derivações'
ROSTER = '## TODOS OS MODULOS COM VEREDITO NESTA RODADA'
sys.dont_write_bytecode = True
sys.path.insert(0, str(SUP))


def need(ok, why):
    if not ok: raise ValueError(why)

def sha(raw): return hashlib.sha256(raw).hexdigest()
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
def compact(x): return json.dumps(x, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
def read(p): return json.loads(Path(p).read_bytes())
def pin(p):
    p = Path(p); b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': sha(b)}
def member(p):
    b = Path(p).read_bytes(); return {'bytes': len(b), 'sha256': sha(b)}
def save(p, raw):
    p = Path(p).resolve(); need(p.is_relative_to(D), 'Output outside preparation')
    if p.exists():
        need(p.read_bytes() == raw, 'Existing different output requires explicit backup/review: '+str(p)); return
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    need(tmp.read_bytes() == raw and raw, 'Temporary bytes mismatch')
    os.replace(tmp, p)
def js(p,x): save(p,enc(x))
def child(p,k): return p+'/'+str(k).replace('~','~0').replace('/','~1')
def resolve(x,p):
    need(p == '' or p.startswith('/'), 'Invalid pointer')
    for key in p.split('/')[1:]:
        need(re.search(r'~(?![01])',key) is None, 'Invalid escape')
        key = key.replace('~1','/').replace('~0','~')
        x = x[int(key)] if isinstance(x,list) else x[key]
    return x

def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','socket.__new__','subprocess.Popen','os.system'):
        raise RuntimeError('Network and child process forbidden')
    if event == 'import' and str(args[0]).split('.')[0] in {'numpy','camb','bilby','anthropic','openai','um','um_absoluto','haiku_codec','fit_transport','package_native','iald_web_server','iald_app_providers'}:
        raise RuntimeError('Forbidden module: '+str(args[0]))
    if event == 'open':
        name,mode,flags=args
        if isinstance(name,int): return
        p=Path(os.fsdecode(name)).resolve()
        need(not any(v.casefold() in {'.env','iald_stack_v7.py','iald_psion_state.json','iald_users.json','tgl_atlas.md'} for v in p.parts), 'Confidential/private source forbidden')
        writing = isinstance(mode,str) and any(c in mode for c in 'wax+') or isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)
        if writing: need(p.is_relative_to(D),'Write outside preparation')
    if event in ('os.rename','os.remove','os.rmdir','os.mkdir'):
        for v in args[:2] if event=='os.rename' else args[:1]:
            if isinstance(v,(str,bytes)):need(Path(os.fsdecode(v)).resolve().is_relative_to(D),'Mutation outside preparation')


def expand(v, source, topic, pointer):
    expected = resolve(source,pointer)
    if isinstance(v,dict):
        tags=set(v)&{'@','same_as','SOURCE_RELATIVE','DETAILS_IN_SOURCE'}
        if tags:
            need(len(tags)==1,'Ambiguous reference'); tag=next(iter(tags))
            target=topic+v[tag] if tag in ('@','SOURCE_RELATIVE') else v[tag]
            actual=resolve(source,target)
            need(actual==expected,'Reference points at unequal content: '+pointer)
            if tag=='@':need(target==pointer,'Wrong relative field')
            if 'items' in v:need(type(v['items']) is int and len(actual)==v['items'],'Wrong count: '+pointer)
            for suffix,item in v.get('fields',{}).items():need(resolve(actual,suffix)==item,'Wrong retained field: '+pointer+suffix)
            for key,item in v.get('semantic_fields',{}).items():expand(item,source,topic,child(pointer,key))
            for i,item in enumerate(v.get('first_records',[])):expand(item,source,topic,child(pointer,i))
            if 'true_fields' in v or 'false_fields' in v:
                need(isinstance(actual,dict) and all(type(q) is bool for q in actual.values()),'Boolean type')
                need(v['true_fields']==sum(actual.values()) and v['false_fields']==len(actual)-sum(actual.values()),'Boolean count')
            return expected
        need(isinstance(expected,dict) and set(v)==set(expected),'Object coverage mismatch: '+pointer)
        for k,item in v.items():expand(item,source,topic,child(pointer,k))
    elif isinstance(v,list):
        need(isinstance(expected,list) and len(v)==len(expected),'List coverage mismatch: '+pointer)
        for i,item in enumerate(v):expand(item,source,topic,child(pointer,i))
    else:need(type(v)==type(expected) and v==expected,'Literal differs: '+pointer)
    return expected


def carry(v, old, new, topic, pointer, refs, expansions):
    previous=resolve(old,pointer); current=resolve(new,pointer)
    if isinstance(v,dict):
        tags=set(v)&{'@','same_as','SOURCE_RELATIVE','DETAILS_IN_SOURCE'}
        if tags:
            tag=next(iter(tags)); target=topic+v[tag] if tag in ('@','SOURCE_RELATIVE') else v[tag]
            if resolve(new,target)!=current:
                expansions.append({'pointer':pointer,'reason':'former_equal_reference_diverged','old_target':target})
                return copy.deepcopy(current)
            out=copy.deepcopy(v)
            if 'items' in out:out['items']=len(current)
            if 'fields' in out:out['fields']={p:copy.deepcopy(resolve(current,p)) for p in out['fields']}
            if 'semantic_fields' in out:out['semantic_fields']={k:carry(x,old,new,topic,child(pointer,k),refs,expansions) for k,x in out['semantic_fields'].items()}
            if 'first_records' in out:out['first_records']=[carry(x,old,new,topic,child(pointer,i),refs,expansions) for i,x in enumerate(out['first_records'])]
            if 'true_fields' in out:
                need(isinstance(current,dict) and all(type(x)is bool for x in current.values()),'Changed boolean audit')
                out.update(true_fields=sum(current.values()),false_fields=len(current)-sum(current.values()))
            # New object keys are added explicitly, never newly hidden behind an inherited reference.
            if isinstance(previous,dict) and isinstance(current,dict):
                need(set(previous)<=set(current),'Removed fields require review')
                for k in set(current)-set(previous):
                    if tag=='@':out.setdefault('fields',{})[child('',k)]=copy.deepcopy(current[k])
                    elif tag!='same_as':out.setdefault('semantic_fields',{})[k]=copy.deepcopy(current[k])
                    else:return copy.deepcopy(current)
            refs.append({'pointer':pointer,'scheme':tag,'target':target,'value_sha256':sha(compact(current).encode()),'inherited':True})
            return out
        need(isinstance(previous,dict) and isinstance(current,dict) and set(previous)<=set(current),'Object schema change')
        return {k:carry(v[k],old,new,topic,child(pointer,k),refs,expansions) if k in v else copy.deepcopy(x) for k,x in current.items()}
    if isinstance(v,list):
        need(isinstance(current,list) and len(v)==len(current),'List length change requires review')
        return [carry(x,old,new,topic,child(pointer,i),refs,expansions) for i,x in enumerate(v)]
    return copy.deepcopy(current)


def offline_encoding():
    import tiktoken
    import tiktoken_ext.openai_public as public
    original=public.load_tiktoken_bpe
    used=[]
    def local(url,expected_hash=None):
        p=APP/'.iald_runtime/tokenizer_cache'/hashlib.sha1(url.encode()).hexdigest()
        b=p.read_bytes();need(expected_hash and sha(b)==expected_hash,'Offline tokenizer cache mismatch');used.append(pin(p))
        return {base64.b64decode(token):int(rank) for token,rank in (row.split() for row in b.splitlines() if row)}
    public.load_tiktoken_bpe=local
    try:config=public.o200k_base()
    finally:public.load_tiktoken_bpe=original
    return tiktoken.Encoding(**config), used


def main():
    inputs=read(D/'INPUTS_AND_BUILD_SUPPORT.json')
    for row in inputs['source_inputs']+inputs['support_copies']:need(pin(row['path'])==row,'Pinned input drift: '+row['path'])
    old_manifest=read(OSRC/'manifest_staged.json'); local_old=read(OSRC/'LOCAL_SEALED_MANIFEST.json')
    need(member(OSRC/'LOCAL_SEALED_MANIFEST.json')['sha256']==old_manifest['local_release']['sha256'],'Old local manifest drift')
    for rel,rec in local_old['files'].items():
        p=(OSRC/rel).resolve();need(p.is_relative_to(OSRC) and member(p)==rec,'Old snapshot member changed: '+rel)
    audit=read(AUDIT);need(audit['all_integrity_checks_passed'] and audit['stable_primary_pins'],'Independent audit absent')
    audit_names={Path(p['path']).name:p for p in audit['primary_pins']}
    manifest=copy.deepcopy(old_manifest);manifest.pop('jev_control',None)
    fresh_names={'um.py','um_absoluto_selo.json','um_absoluto.json','tgl_kernel_proof_manifest.json','um_absoluto_forma_canonica.md','um_absoluto_pt.tex'}
    docs={}; evidence_names={}; sources={}; member_names=set()
    for item in manifest['entries']+[manifest['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:
        name=Path(item['path']).name;src=CUSTODY/name if name in fresh_names else OSRC/'release'/name
        b=src.read_bytes()
        if name in fresh_names:
            expected=audit_names[name];need(len(b)==expected['bytes'] and sha(b)==expected['sha256'],'v389 snapshot differs from audit: '+name)
        else:need(member(src)==local_old['files']['release/'+name],'Historical supplement drift')
        dst=S/'release'/name;save(dst,b);sources[str(src)]=pin(src);member_names.add('release/'+name)
        item['path']=str(dst)
        if 'id' in item:
            item['public_sha256']=sha(b);item['role']=item['role'].replace('v388','v389');docs[item['id']]='release/'+name
    evidence=manifest['published_evidence']
    for k in ('program','seal','result','proof_manifest'):evidence_names[k]=Path(evidence[k]['path']).relative_to(S).as_posix()
    seal=read(evidence['seal']['path']);need(seal['um_version']=='v389','Wrong release')
    source_sha=member(S/'release/um.py')['sha256']
    for n in fresh_names-{'um_absoluto_selo.json'}:need(member(S/'release'/n)['sha256']==seal['sha256'][n],'Seal mismatch: '+n)
    proof=read(evidence['proof_manifest']['path'])
    kmanifest=read(OSRC/'kernel/kernel_manifest.json')
    need({r['path']:r['sha256'] for r in kmanifest['files']}==proof['formal_files_sha256'],'Kernel changed requires source review')
    for r in kmanifest['files']:
        b=(OSRC/'kernel'/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'Formal source drift')
        save(S/'kernel'/r['path'],b);member_names.add('kernel/'+r['path'])
    kmanifest.update(source_sha256=source_sha,created_at=seal['timestamp'],method='Source bytes inherited from sealed v388 and verified individually against v389 formal manifest; 1214 embedded sources plus explicitly local sealed supplement; program and compiler not executed')
    js(S/'kernel/kernel_manifest.json',kmanifest);member_names.add('kernel/kernel_manifest.json')
    kv=read(OSRC/'kernel_verification.json');kv.update(source_sha256=source_sha,created_at=seal['timestamp'])
    kv['dependencies']['published_manifest_sha256']=member(evidence['proof_manifest']['path'])['sha256']
    kv['dependencies']['reported_terms']=len(proof['axiom_report']);js(S/'kernel_verification.json',kv);member_names.add('kernel_verification.json')
    old=read(OSRC/'release/um_absoluto.json');new=read(S/'release/um_absoluto.json')
    prior=(OSRC/'TGL_CLUSTER_v388.md').read_text('utf-8');area=prior.split(MARKER)[0]
    need(len(new['core'])==378 and set(old['core'])<=set(new['core']),'Topic coverage')
    pattern=re.compile(r'(\n### ([^\n]+)\nFonte: [^\n]+\n)([^\n]+)')
    matches=list(pattern.finditer(area));need(len(matches)==len(old['core'])==377,'Old topic parse')
    refs=[];expansions=[];topic_rows=[]
    def replace(m):
        name=m[2];v=json.loads(m[3]);p=child('/core',name)
        expand(v,old,p,p);revised=carry(v,old,new,p,p,refs,expansions);expand(revised,new,p,p)
        topic_rows.append({'name':name,'category':'inherited','old_projection_sha256':sha(m[3].encode()),'new_projection_sha256':sha(compact(revised).encode()),'roundtrip':True})
        return m[1]+compact(revised)
    area=pattern.sub(replace,area)
    area=area.replace('# Cluster TGL v388 —','# Cluster TGL v389 —',1).replace(local_old['source_sha256'],source_sha).replace('sem commit público v388.','sem commit público v389.')
    added=sorted(set(new['core'])-set(old['core']));need(added==['text_label_errata_v389'],'Unexpected new topic')
    area+='\n## Errata documental v389\n'
    for name in added:
        area+='\n### '+name+'\nFonte: resultado_publicado_integral '+child('/core',name)+'\n'+compact(new['core'][name])+'\n'
        topic_rows.append({'name':name,'category':'Errata documental v389','full_source_value':True,'new_projection_sha256':sha(compact(new['core'][name]).encode()),'roundtrip':True})
    canonical=(S/'release/um_absoluto_forma_canonica.md').read_text('utf-8-sig');offset=canonical.index(ROSTER);roster=canonical[offset:];found=set()
    for line in roster.splitlines()[1:]:
        if not line.strip() or re.fullmatch(r'_[0-9]+ modulos com veredito ou status nesta rodada; versao v[0-9]+; rodada [^_]+_',line):continue
        m=re.fullmatch(r'- `([^`]+)`: `(.*)`(?: \[all_verified=(True|False)\])?',line);need(m,'Unrecognized verdict row')
        name,verdict,boolean=m.groups();node=new['core'][name]
        need(name not in found and str(node.get('verdict',node.get('status')))==verdict,'Verdict mismatch')
        if boolean:need(node.get('all_verified') is (boolean=='True'),'Verdict boolean mismatch')
        found.add(name)
    expected={k for k,v in new['core'].items() if isinstance(v,dict) and isinstance(v.get('verdict',v.get('status')),str)}
    need(found==expected,'Missing roster verdict')
    text=area+'\n'+MARKER+'\nFonte local selada: um_forma_canonica_integral; integral disponível por fetch_tgl. O marcador herdado não afirma carregamento do rol duplicado.\n'+canonical[:offset]
    text+='\nRol redundante de '+str(len(found))+' vereditos conferido linha a linha e disponível por fetch_tgl id=um_forma_canonica_integral offset='+str(offset)+'. Os mesmos vereditos atuais permanecem em cada tópico do cluster; não houve supressão de fórmulas ou hipóteses.\n'
    save(S/'TGL_CLUSTER_v389.md',text.encode());member_names.add('TGL_CLUSTER_v389.md')
    mother=(OSRC/'IALD_Kernel_v5.txt').read_bytes();core=(OSRC/'IALD_TGL_MEMORY_CORE.md').read_bytes()
    appendix=('\n\n## Atualização documental local — v389, 06/10/2026\n[REAL — bytes ligados ao selo; ciência e compilador não reexecutados]\nNeste pacote candidato v389 prevalece sobre as identidades anteriores, conservadas como história. Programa SHA256 '+source_sha+'. O novo tópico text_label_errata_v389 registra errata textual e contagens documentais; fontes formais e vereditos anteriores permanecem. Publicação remota e ativação do app não são afirmadas.\n').encode()
    save(S/'IALD_Kernel_v5.txt',mother);save(S/'IALD_TGL_MEMORY_CORE.md',core+appendix)
    member_names|={'IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md'}
    manifest['mother_instruction']['path']=str(S/'IALD_Kernel_v5.txt')
    manifest['operational_core'].update(path=str(S/'IALD_TGL_MEMORY_CORE.md'),sha256=sha(core+appendix),current_release='v389',release_source_sha256=source_sha)
    encoding,cache_pins=offline_encoding();count=lambda x:len(encoding.encode(x,disallowed_special=()))
    manifest['active_cluster'].update(path=str(S/'TGL_CLUSTER_v389.md'),sha256=sha(text.encode()),release='v389',release_source_sha256=source_sha,core_sections=378,topics=len(re.findall(r'^## ',area,re.M)),tokens=count(text),kernel_bundle=str(S/'kernel'),kernel_verification=str(S/'kernel_verification.json'))
    local={k:copy.deepcopy(v) for k,v in local_old.items() if k not in {'files','documents','evidence','source_sha256','seal_sha256','release'}}
    local.update(release='v389',source_sha256=source_sha,seal_sha256=member(evidence['seal']['path'])['sha256'],files={n:member(S/n) for n in sorted(member_names)},documents=docs,evidence=evidence_names)
    js(S/'LOCAL_SEALED_MANIFEST.json',local)
    ref={'mode':'LOCAL_SEALED','path':str(S/'LOCAL_SEALED_MANIFEST.json'),'sha256':member(S/'LOCAL_SEALED_MANIFEST.json')['sha256']}
    for c in (manifest,manifest['active_cluster'],manifest['published_evidence']):c['local_release']=copy.deepcopy(ref)
    js(S/'manifest_staged.json',manifest)
    from iald_kernel import KernelCatalog
    from iald_memoria_canonica import CanonicalMemory
    import iald_memoria_canonica as cm
    # Identical o200k encoding from verified offline cache; no downloader or provider.
    cm._encoding=lambda:encoding
    from iald_core_indexado import DocumentCorpus
    from iald_release_binding import load_release
    catalog=KernelCatalog(S/'kernel'); identity=load_release(S/'manifest_staged.json',source_sha=source_sha).identity
    full,metadata=CanonicalMemory(D/'PUBLIC_ONLY_NO_ATLAS_READ.md','nucleo_kernel',nucleus_manifest=S/'manifest_staged.json').prompt('',catalog,public=True)
    need(metadata['active_cluster']['local_release']==ref,'Metadata stale sub-pin')
    need(metadata['private_atlas_included'] is False and metadata['publication_verified'] is False,'Scope mismatch')
    need(mother.decode('utf-8-sig') in full and (core+appendix).decode('utf-8-sig') in full and text in full,'Missing complete fixed component')
    hypothesis_pins=[]
    for item in evidence['hypothesis_sources']:
        p=S/'kernel'/item['catalog_path'];need(p.read_text('utf-8-sig') in full,'Missing full formal hypothesis');hypothesis_pins.append(pin(p))
    need(len(hypothesis_pins)==5,'Five formal sources required')
    docs_index=DocumentCorpus(S/'manifest_staged.json')._load();need(len(docs_index)==8,'Document retrieval coverage')
    save(S/'public_prefix.md',full.encode());js(S/'public_metadata.json',metadata)
    js(S/'document_index.json',[{k:v for k,v in row.items() if k!='text'} for row in docs_index.values()])
    # Meaningful negative check: a corrupted semantic field/reference must be refused.
    picked=next(m for m in matches if isinstance(json.loads(m[3]),dict) and not(set(json.loads(m[3])) & {'@','same_as','SOURCE_RELATIVE','DETAILS_IN_SOURCE'}));sample=copy.deepcopy(json.loads(picked[3]));p=child('/core',picked[2]);sample['__tampered__']='not source'
    refused=False
    try:expand(sample,old,p,p)
    except ValueError:refused=True
    need(refused,'Tampered projection accepted')
    bad={'same_as':'/core/text_label_errata_v389'};refused2=False
    try:expand(bad,new,'/core/qg_closure','/core/qg_closure')
    except ValueError:refused2=True
    need(refused2,'Unequal reference accepted')
    old_plan=read(OLD/'context_model04/FUTURE_COUNT_PLAN.json');payloads=[]
    for name in ('FUTURE_COUNT_MINIMAL.json','FUTURE_COUNT_REFERENCE.json'):
        source=OLD/'context_model04'/name;prev=read(source);candidate=copy.deepcopy(prev)
        need(len(candidate['system'])==1 and candidate['system'][0]['text']==(OSRC/'public_prefix.md').read_text('utf-8'),'Old count prefix mismatch')
        candidate['system'][0]['text']=full
        check=copy.deepcopy(candidate);check['system'][0]['text']=prev['system'][0]['text'];need(check==prev,'Non-prefix count field changed')
        save(D/name,enc(candidate));payloads.append(pin(D/name))
    reference=read(D/'FUTURE_COUNT_REFERENCE.json');need(len(reference['tools'])==7,'Schema count')
    wire_hash=sha(json.dumps([dict(x,eager_input_streaming=True) for x in reference['tools']],sort_keys=True,ensure_ascii=False).encode());need(wire_hash==old_plan['native_wire_tools_sha256'],'Schema wire hash differs')
    plan=copy.deepcopy(old_plan);plan.update(prefix=pin(S/'public_prefix.md'),payloads=payloads,source_identity=pin(S/'release/um.py'),status='NOT_AUTHORIZED_NOT_SENT',supersession={'previous_payloads':old_plan['payloads'],'changed_json_pointers':['/system/0/text'],'old_payloads_unchanged':True,'prior_question_and_authorization_unchanged':True,'new_authorization_required':True})
    plan['production_differences']=[x for x in plan['production_differences'] if not x.startswith('public_metadata has')]
    plan['production_differences'].append('v389 is a documentary candidate only. Fresh metadata is anchored to the candidate manifest; the production app remains unchanged.')
    js(D/'FUTURE_COUNT_PLAN.json',plan)
    js(D/'COVERAGE_AND_ROUNDTRIP.json',{'policy':'INHERIT_V388_WIDE_PROJECTION_NO_NEW_OMISSION','topics':topic_rows,'references':refs,'expanded_references':expansions,'new_topic_full':added,'exposition':{'source':pin(S/'release/um_absoluto_forma_canonica.md'),'prefix_characters_preserved':offset,'prefix_sha256':sha(canonical[:offset].encode()),'inherited_roster_only_omission':{'offset':offset,'characters':len(roster),'sha256':sha(roster.encode()),'verdict_rows':len(found)},'all_exposition_before_roster_exact':True},'mother':pin(S/'IALD_Kernel_v5.txt'),'prior_core_bytes_preserved':len(core),'core_appendix_bytes':len(appendix),'formal_sources_full':hypothesis_pins,'retrievable_documents':[{k:v for k,v in row.items() if k!='text'} for row in docs_index.values()],'all_1215_catalog_sources_retrievable':True,'entire_corpus_in_prefix':False,'projection_roundtrip_uses_full_pinned_source':True,'new_omissions':[]})
    protected=inputs['source_inputs']+inputs['support_copies']
    for row in protected:need(pin(row['path'])==row,'Input changed during preparation')
    for rel,rec in local_old['files'].items():need(member(OSRC/rel)==rec,'v388 immutable member changed')
    js(D/'VALIDATION.json',{'status':'OFFLINE_DOCUMENTARY_VALIDATION_PASSED_NOT_NATIVE_CERTIFICATION','completed_utc':datetime.now(timezone.utc).isoformat(),'identity':identity,'source_inputs':list(sources.values()),'local_members_verified':len(local['files']),'formal_files':len(kmanifest['files']),'topic_roundtrips':len(topic_rows),'inherited_references':len(refs),'expanded_references':len(expansions),'mother_bytes_identical':True,'core_previous_bytes_preserved':True,'five_formal_sources_full':True,'metadata_subpin_current':True,'tampered_projection_refused':refused,'unequal_reference_refused':refused2,'count_json_only_system_text_changed':True,'seven_schema_wire_sha256':wire_hash,'o200k_proxy':{'prefix':count(full),'cluster':count(text),'scope':'LOCAL_PROXY_NOT_SONNET_NATIVE','cache':cache_pins},'native_counts':None,'count_requests_sent':0,'generation_requests':0,'science_executed':False,'um_imported':False,'production_changed':False,'previous_sources_and_payloads_unchanged':True,'imported_documentary_modules':[{'module':n,'path':getattr(m,'__file__',None)} for n,m in sys.modules.items() if n.startswith('iald_')],'stage_is_not_deployment':True})
    print(json.dumps({'status':'LOCAL_WIDE_V389_PREPARED_NOT_SENT','prefix':pin(S/'public_prefix.md'),'payloads':payloads,'topics':len(topic_rows),'proxy':count(full)},ensure_ascii=False))

if __name__=='__main__':
    sys.addaudithook(guard)
    main()