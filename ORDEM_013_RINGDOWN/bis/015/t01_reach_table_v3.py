"""Documentary E6 correction; reuses the existing renderer without importing its runner."""
from pathlib import Path
from datetime import datetime, timezone
import ast, copy, hashlib, json, math, re, time, uuid

B=Path(__file__).resolve().parents[2];ROOT=B.parent
HERE=B/'bis/e6_prepare_v3/runs/wall_actual_001'
ORIGINAL=HERE/'QUADRO_DE_ALCANCE_V1.json'
GENERATOR=B/'bis/e6_prepare_v3/generate_reach_table.py'
OUT=ROOT/'TUNEL/DO_CHATGPT';D=B/'bis/015/t01_e6_review_v2'
cache={};counts={'pins_checked':0,'pointers_checked':0,'metric_values_checked':0}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate key')
            out[k]=v
        return out
    return json.loads(p.read_text('utf-8-sig'),object_pairs_hook=pairs,parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
def resolve_source(ref):
    relative=Path(ref['path'])
    if relative.is_absolute() or '..' in relative.parts:raise ValueError('Unsafe path')
    p=(ROOT/relative).resolve()
    if not p.is_relative_to(B.resolve()) or any(t.upper()=='E2_PRIVATE' for t in p.parts):raise ValueError('Outside public ringdown source scope')
    key=(str(p),ref['sha256'])
    if key not in cache:
        if sha(p)!=ref['sha256']:raise ValueError('Source hash mismatch')
        cache[key]=read(p) if p.suffix=='.json' else None;counts['pins_checked']+=1
    return cache[key]
def pointer(obj,path):
    if not isinstance(path,str) or (path and not path.startswith('/')):raise ValueError('Invalid pointer')
    for part in path[1:].split('/') if path else []:
        if re.search(r'~(?![01])',part):raise ValueError('Invalid escape')
        part=part.replace('~1','/').replace('~0','~')
        if isinstance(obj,list):
            if not re.fullmatch('0|[1-9][0-9]*',part):raise ValueError('Invalid list index')
            obj=obj[int(part)]
        else:obj=obj[part]
    return obj
def walk(x,path=''):
    if isinstance(x,dict):
        yield path,x
        for k,v in x.items():yield from walk(v,path+'/'+str(k).replace('~','~0').replace('/','~1'))
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from walk(v,path+'/'+str(i))
def verify_rates(obj):
    for c in obj['cells']:
        for r in c['scenarios']:
            if c['data_group']!='O4_HOJE' and any(r['metrics'][k]['value'] is not None for k in ('rate_per_year','rate_CI')):
                raise ValueError('Rate in unsupported data group')
def audit(obj,allow_expected_missing=False):
    missing=[]
    for path,node in walk(obj):
        if 'path' in node and 'sha256' in node and isinstance(node['path'],str):
            source=resolve_source(node)
            if 'pointer' in node and node['pointer'] is not None:
                try:pointer(source,node['pointer']);counts['pointers_checked']+=1
                except (KeyError,IndexError):
                    if not allow_expected_missing:raise
                    missing.append((path,node))
        ref=node.get('source')
        if 'value' in node and isinstance(ref,dict) and isinstance(ref.get('pointer'),str):
            try:v=pointer(resolve_source(ref),ref['pointer'])
            except (KeyError,IndexError):
                if not allow_expected_missing:raise
            else:
                if v!=node['value']:raise ValueError('Metric differs from source: '+path)
                counts['metric_values_checked']+=1
    return missing
def emit(p,value):
    if p.exists():raise FileExistsError(p)
    raw=(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw;temp.rename(p)
def main():
    start=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False)
    original=read(ORIGINAL);value=copy.deepcopy(original)
    missing=audit(value,True)
    assert len(missing)==20,len(missing)
    fixed=[]
    for path,ref in missing:
        old=ref['pointer'];parent=old.rsplit('/',1)[0]
        assert pointer(resolve_source(ref),parent+'/status')=='OPEN_NO_UNIQUE_LOCAL_DTAU'
        assert old.rsplit('/',1)[1] in ('delta_weighted','z_common')
        node=pointer(value,path.rsplit('/',1)[0])
        assert node['value'] is None and node['status']=='OPEN'
        ref['pointer']=None;node['unresolved_original_pointer']=old
        node['reason']='NO_FIELD_IN_SOURCE__OPEN_NO_UNIQUE_LOCAL_DTAU'
        fixed.append({'node':path,'unresolved_original_pointer':old,'source_status':'OPEN_NO_UNIQUE_LOCAL_DTAU'})
    rate_cells=0;corrections_open=0;corrections_present=0
    for c in value['cells']:
        rates=c['rate_contexts']
        if c['data_group']=='O4_HOJE':
            assert rates;rate_cells+=1
        for r in c['scenarios']:
            for name in ('rate_per_year','rate_CI'):
                m=r['metrics'][name]
                assert m['value'] is None
                if c['data_group']=='O4_HOJE':
                    field='rate' if name=='rate_per_year' else 'rate_CI'
                    m['legacy_placeholder_source']=m.get('source')
                    m['source']=None
                    m.update(value=[{'category':q['category'],'exposure':copy.deepcopy(q['exposure']),'value':copy.deepcopy(q[field]['value'])} for q in rates],
                        status='INPUT_CONDITIONAL_COPIED_BY_CONTEXT',unit='per_year' if field=='rate' else 'per_year_CI90',
                        reason='CELL_RATE_CONTEXTS_NOT_SCENARIO_SPECIFIC_SELECTION_RATE',
                        contextual_sources=[copy.deepcopy(q[field]) for q in rates])
                else:m['reason']='NO_RATE_CONTEXT_FOR_DATA_GROUP'
            m=r['metrics']['correction_over_sigma']
            if m['value'] is None:
                corrections_open+=1
                if m['reason']!='NO_FIELD_IN_SOURCE__OPEN_NO_UNIQUE_LOCAL_DTAU':
                    m['reason']='NO_FIELD_IN_SOURCE' if m.get('source') or r['references'] or r['id'].startswith('E0_') else 'NO_EXECUTION_NO_TEST_POSTERIOR'
            else:corrections_present+=1
    assert rate_cells==30 and corrections_open==964 and corrections_present==1576
    # All scientific numbers besides the explicitly requested documentary rate columns remain identical.
    for a,b in zip(original['cells'],value['cells']):
        assert a['rate_contexts']==b['rate_contexts']
        for x,y in zip(a['scenarios'],b['scenarios']):
            assert x['gate']==y['gate'] and x['verdict']==y['verdict']
            for k,m in x['metrics'].items():
                if k not in ('rate_per_year','rate_CI'):assert m['value']==y['metrics'][k]['value'],k
    verify_rates(value);audit(value)
    negative=[]
    for label,fn in [
        ('missing pointer rejected',lambda:pointer({},'/absent')),
        ('tampered source hash rejected',lambda:resolve_source({'path':str(ORIGINAL.relative_to(ROOT)).replace('\\','/'),'sha256':'0'*64}))]:
        try:fn()
        except (ValueError,KeyError):negative.append(label)
        else:raise AssertionError(label)
    bad={'cells':[{'data_group':'ET','scenarios':[{'metrics':{'rate_per_year':{'value':1},'rate_CI':{'value':None}}}]}]}
    try:verify_rates(bad)
    except ValueError:negative.append('future rate rejected')
    else:raise AssertionError('future rate')
    value['documentary_amendment']={'at':datetime.now(timezone.utc).isoformat(),'supersedes':str(ORIGINAL.relative_to(ROOT)).replace('\\','/'),'supersedes_sha256':sha(ORIGINAL),
        'generator_extension':str(Path(__file__).relative_to(ROOT)).replace('\\','/'),'generator_extension_sha256':sha(Path(__file__)),'original_generator_sha256':sha(GENERATOR),
        'statute':'DOCUMENTARY_ONLY_NOT_NEW_SCIENCE','missing_pointer_corrections':fixed}
    # Reuse only the original pure render function and literal GATE_FIELDS declaration.
    tree=ast.parse(GENERATOR.read_text('utf-8-sig'))
    nodes=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name=='render') or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GATE_FIELDS' for t in n.targets))]
    ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(GENERATOR),'exec'),ns)
    display=copy.deepcopy(value)
    for c in display['cells']:
        for r in c['scenarios']:
            for name in ('rate_per_year','rate_CI'):
                m=r['metrics'][name]
                if m['value'] is not None:
                    m['value']='; '.join(f'{q["category"]}: {q["value"]} /ano; exposição {q["exposure"]["years"]} a [{q["exposure"]["status"]}]' for q in m['value'])
    header='[DERIVED — transcrição documental de fontes; NÃO-CEGO; nenhum teste físico]\n\nA RG é o limite clássico; NOT_FALSIFIED nunca é CONFIRMED.\n\n'
    op16=sha(OUT/'ENTREGA_016_ABERTURA_operador.md');op15=sha(OUT/'ENTREGA_015_ABERTURA_operador.md')
    header+=f'Abertura016SHA256: {op16}\nAbertura015SHA256: {op15}\nPredecessorSHA256: {sha(ORIGINAL)}\n\n'
    jp=HERE/'QUADRO_DE_ALCANCE_V1_v2.json';mp=HERE/'QUADRO_DE_ALCANCE_V1_v2.md'
    emit(jp,value);emit(mp,header+ns['render'](display))
    receipt={'at':datetime.now(timezone.utc).isoformat(),'status':'DOCUMENTARY_CORRECTION_CHECKED_LOCALLY_NOT_INDEPENDENT_REVIEW',
        'input':{'path':str(ORIGINAL),'sha256':sha(ORIGINAL)},'outputs':[{'path':str(p),'sha256':sha(p)} for p in [jp,mp]],
        'verified_sources':[{'path':k[0],'sha256':k[1]} for k in cache if k[1]!='0'*64],
        'counts':counts,'repaired_pointers':len(fixed),'rate_cells':rate_cells,'correction_available':corrections_present,'correction_OPEN':corrections_open,
        'negative_probes':negative,'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'heavy_machine_hours':0,
        'opening016_sha256':op16,'opening015_sha256':op15,'gate_changed':False}
    emit(D/'RESULT.json',receipt)
    emit(OUT/'ENTREGA_015_T01g_quadro_v2.md',header+f'Taxas/IC expostas somente nas30células O4_HOJE, com todas as categorias e exposições preservadas. Demais grupos OPEN/NO_RATE_CONTEXT_FOR_DATA_GROUP. Vinte ponteiros ausentes corrigidos ao lado, com reason explícito.\n\nCorreção/σ em {corrections_present}/2540cenários; {corrections_open}OPEN com razão por linha. Esta frase corrige RELATORIO_FINAL:94 ao lado. Hashes e controles em {D/"RESULT.json"}.\n\nNenhum valor científico, gate ou veredito foi alterado. Três provas negativas passaram. Revisão independente ainda pendente.\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ['verified_sources','outputs','input']},ensure_ascii=False))
if __name__=='__main__':main()
