"""Create E6 preparation metadata and parse AST; NEVER run/import the generator."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import tempfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ROOT = BASE.parent
LIMIT = 25*1024*1024


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def emit(name, obj):
    raw=(json.dumps(obj,ensure_ascii=False,allow_nan=False,indent=2)+'\n').encode('utf-8')
    if len(raw)>LIMIT: raise ValueError('Metadata exceeds limit')
    target=HERE/name
    if target.exists(): raise FileExistsError(target)
    fd,temp=tempfile.mkstemp(dir=HERE,prefix='.static-')
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(raw);stream.flush();os.fsync(stream.fileno())
        if Path(temp).stat().st_size!=len(raw): raise ValueError('Short write')
        os.link(temp,target)
    finally:
        Path(temp).unlink(missing_ok=True)


def ref(path):
    return dict(path=path.relative_to(ROOT).as_posix(),sha256=digest(path))


def object_schema(properties, required=None, extra=False):
    return dict(type='object',properties=properties,
                required=list(properties) if required is None else required,additionalProperties=extra)


def main():
    names=('CONTRACT.json','SOURCE_PINS.json','OUTPUT_SCHEMA.json','STAGE_RECEIPT_SCHEMA.json',
           'STATIC_RECEIPT.json','PREPARATION_MANIFEST.json')
    if any((HERE/n).exists() for n in names): raise FileExistsError('Preparation already published; preserve bytes')
    source_paths={
        'E2':BASE/'RINGDOWN_5SIGMA_V1.json',
        'E2_ACTIVATION':BASE/'bis/E2_REGISTRATION_RECEIPT.json',
        'C1':BASE/'C1_LEITURAS_v4.json',
        'E0':BASE/'PORTAO_DA_AMPLIACAO_V1.json',
        'E1':BASE/'NUISANCE_V1.json',
        'ROUTE_IV':BASE/'bis/E0_ROUTE_IV_POWER_v2.json',
        'E4_PLAN':BASE/'bis/e4_e5_prepare/PLAN.json',
        'E4_RESULT':BASE/'bis/e4_e5_prepare/runs/authorized_001/DETERMINISTIC_DIAGNOSTICS.json',
        'E4_RECEIPT':BASE/'bis/e4_e5_prepare/runs/authorized_001/RESULT_RECEIPT.json',
        'E4_REVIEW':BASE/'bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json',
    }
    sources={key:ref(path) for key,path in source_paths.items()}
    metadata={key:json.loads(path.read_text(encoding='utf-8-sig')) for key,path in source_paths.items()}
    documents={
        'ORDER':ROOT/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md',
        'E0_REPORT':BASE/'PORTAO_DA_AMPLIACAO_V1.md',
        'E2_WITNESS':ROOT/metadata['E2']['witness_relative_to_Chatgpt'],
        'E4_REVIEW_REPORT':BASE/'bis/e4_indep_review/E4_E5_INDEPENDENT_REVIEW.md',
    }
    documents={key:ref(path) for key,path in documents.items()}
    generator=HERE/'generate_reach_table.py'
    tree=ast.parse(generator.read_text(encoding='utf-8-sig'),filename=str(generator))
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import): imports.extend(alias.name for alias in node.names)
        elif isinstance(node,ast.ImportFrom): imports.append(node.module)
    allowed={'pathlib','datetime','argparse','hashlib','json','math','os','re','tempfile'}
    if set(imports)-allowed: raise ValueError('Non-allowlisted import')
    forbidden={'eval','exec','__import__','compile','import_module','system','popen'}
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            name=node.func.id if isinstance(node.func,ast.Name) else getattr(node.func,'attr',None)
            if name in forbidden: raise ValueError('Dynamic execution call in generator')
        if isinstance(node,ast.Assert): raise ValueError('Assertions cannot guard optimized runtime')
    constants={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            if node.targets[0].id in ('ROUTES','GROUPS','METRICS','GATE_FIELDS','STAGES','PAID_FLAGS'):
                constants[node.targets[0].id]=ast.literal_eval(node.value)
    main_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    calls=[n.value.func.id for n in main_node.body if isinstance(n,ast.Assign)
           and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name)]
    if calls.index('activate')>=calls.index('assemble_baselines'): raise ValueError('Guard ordering')
    own_trees={p.name:ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p)) for p in HERE.glob('*.py')}
    readings=metadata['E2']['readings']
    if len(readings)!=10 or len(set(readings))!=10: raise ValueError('Expected ten unique E2 readings')
    c1rows={r['reading']:r for r in metadata['C1']['rows']}
    if set(readings)!=set(c1rows): raise ValueError('C1/E2 reading mismatch')
    statutes={r:c1rows[r]['clock_status'].split('_',1)[0] for r in readings}
    if set(statutes.values())-{'INPUT','CONJECTURE'}: raise ValueError('Unknown C1 statute')
    text={'type':'string','minLength':1}
    sha={'type':'string','pattern':'^[0-9a-f]{64}$'}
    pin=object_schema({'path':text,'sha256':sha})
    pointer={'type':'string','pattern':'^(/.*)?$'}
    origin=object_schema({'path':text,'sha256':sha,'pointer':pointer})
    metric=object_schema({'value':{'type':['number','array','null'],'items':{'type':'number'}},
        'status':text,'unit':text,'source':{'anyOf':[origin,{'type':'null'}]},'reason':text})
    metric['allOf']=[{'if':{'properties':{'value':{'type':'null'}}},
                     'then':{'properties':{'status':{'const':'OPEN'}}},
                     'else':{'properties':{'source':origin}}}]
    gate=object_schema(dict(color={'enum':['green','red','OPEN']},status=text,
        **{k:metric for k in constants['GATE_FIELDS']}),extra=True)
    scenario=object_schema({'id':text,'scope':text,
        'metrics':object_schema({k:metric for k in constants['METRICS']}),
        'gate':gate,'verdict':{'enum':metadata['E2']['permitted_verdicts']},
        'physical_test_present':{'type':'boolean'},'references':{'type':'array'}},extra=True)
    cell=object_schema({'route':{'enum':constants['ROUTES']},'reading':{'enum':readings},
        'data_group':{'enum':constants['GROUPS']},'reading_statute':{'enum':['INPUT','CONJECTURE']},
        'scenarios':{'type':'array','minItems':1,'items':scenario},
        'rate_contexts':{'type':'array'},'notes':{'type':'array','items':text}},extra=True)
    schema=object_schema({'schema':{'const':'E6_REACH_TABLE_V1'},
        'status':{'const':'ASSEMBLED_REVIEWED_SOURCES_NOT_NEW_SCIENCE'},
        'registration_sha256':sha,'authorization_sha256':sha,'generator_sha256':sha,
        'readings':{'const':readings},'routes':{'const':constants['ROUTES']},'data_groups':{'const':constants['GROUPS']},
        'cells':{'type':'array','minItems':180,'maxItems':180,'items':cell},
        'reviewed_stage_receipts':object_schema({s:pin for s in constants['STAGES']}),
        'source_pins':{'type':'object','additionalProperties':pin},
        'new_scientific_computations':{'const':False},'lnB_recomputed':{'const':False},
        'E7_extraction_authorized':{'const':False},'order_completed':{'const':False}},extra=True)
    schema['$schema']='https://json-schema.org/draft/2020-12/schema'
    schema['$comment']='Structural schema only. Cross-source scientific and activation constraints live in CONTRACT/code; schema validation is not execution approval.'
    binding_props=dict(route={'enum':constants['ROUTES']},reading={'enum':readings},
        data_group={'enum':constants['GROUPS']},scenario_id=text,scope=text,
        metrics={'type':'object','propertyNames':{'enum':constants['METRICS']},
                 'additionalProperties':object_schema({'pointer':pointer,'unit':text})},
        gate_pointer={'anyOf':[pointer,{'type':'null'}]},test_summary_pointer=pointer,
        calibration_receipt_sha256=sha,calibration_scenario_id=text)
    binding=object_schema(binding_props,required=['route','reading','data_group','scenario_id','scope','metrics'])
    stage=object_schema({'schema':{'const':'E6_REVIEWED_STAGE_V1'},'stage':{'enum':constants['STAGES']},
        'registration_sha256':sha,'outcome':{'enum':['COMPLETED','PARTIAL','BLOCKED','UNAVAILABLE']},
        'issued_utc':{'type':'string','format':'date-time'},'artifact':pin,'review':pin,
        'bindings':{'type':'array','items':binding}})
    stage['$schema']='https://json-schema.org/draft/2020-12/schema'
    stage['$comment']='Proposed normalized interface, not an existing E3 receipt or a fabricated acceptance. Independent review must duplicate exact bindings and outcome.'
    emit('STAGE_RECEIPT_SCHEMA.json',stage)
    contract=dict(schema='E6_PREPARATION_CONTRACT_V1',status='PREPARED_ONLY_NOT_AUTHORIZED',
        readings=readings,reading_statutes=statutes,
        reading_statute_details={r:{k:c1rows[r][k] for k in ('clock_status','canonical_scope')} for r in readings},
        routes=constants['ROUTES'],data_groups=constants['GROUPS'],metrics=constants['METRICS'],gate_fields=constants['GATE_FIELDS'],
        permitted_verdicts=metadata['E2']['permitted_verdicts'],
        stage_receipt_schema_sha256=digest(HERE/'STAGE_RECEIPT_SCHEMA.json'),
        required_reviewed_stages=constants['STAGES'],paid_flags=constants['PAID_FLAGS'],
        authorization_contract=dict(status='AUTHORIZED_E6_ASSEMBLY_AFTER_REVIEWED_E3_AND_TEST',
            required=['status','new_scientific_computation_allowed','package_sha256','registration','witness',
                      'issued_utc','reviewed_stages','run_id'],
            new_scientific_computation_allowed=False,package_files=['generate_reach_table.py','CONTRACT.json','SOURCE_PINS.json','OUTPUT_SCHEMA.json'],
            pin_format='Exactly {path: relative-to-Chatgpt JSON/MD, sha256: actual bytes SHA256}',
            chronology='aware UTC: E2/activation <= stage receipt <= independent review <= authorization <= now'),
        independent_review_contract=dict(status='ACCEPTED_FOR_E6_MAPPING',
            required=['status','stage','registration_sha256','artifact_sha256','blocking_findings','reviewed_utc','bindings','outcome','reviewer'],
            blocking_findings=[],bindings='Exact copy of reviewed receipt bindings',reviewer='Named independent reviewer, not generated by this package'),
        source_gate_contract=dict(required=['color','status','units','decision_reviewed']+list(constants['PAID_FLAGS'])+list(constants['GATE_FIELDS']),
            units='Map every gate metric to a nonempty same-channel unit; null explicitly allowed for inapplicable quantities',
            green='Reviewed decision; tau sigma_c >=0 and < floor5; IV recovered jitter and sigma_sys both numeric and nonnegative; no gate calculated here'),
        source_test_summary_contract=dict(required=['verdict','test_data_present'],
            physical_or_strong_requires=['unblinding_authorized','population_checks_passed','decision_rule_paid','reading_multiplicity_paid'],
            relative_exclusion_requires='relative_exclusion_rule_paid',
            calibrated_binding='Same route/reading/data_group, referenced scenario_id and exact E3.3 receipt SHA; numerical gate and units must agree'),
        no_test='AWAITING_DATA',red_or_open_with_test='INCONCLUSIVE_SYSTEMATICS; z_physical and lnB null',
        missing='null/OPEN with reason; never numerical zero replacement',
        sources='SOURCE_PINS.json',mapping='SOURCE_MAP.md',
        restrictions=['No science/PE/MC/waveform/strain/posterior I/O','No E6 execution in preparation',
                      'No E7 extraction authorization','No E4/E7 source changes','No new BF/selection/model/physical gate',
                      'Outputs exclusive inside e6_prepare; each at most 25 MiB'],
        verification_scope='AST only; no execution tests or scientific validation',order_completed=False)
    emit('CONTRACT.json',contract)
    emit('SOURCE_PINS.json',dict(schema='E6_SOURCE_PINS_V1',sources=sources,document_pins=documents,
                              current_science_reads='Existing diagnostic JSON/plan only; no posterior payloads'))
    emit('OUTPUT_SCHEMA.json',schema)
    for key,path in source_paths.items():
        if digest(path)!=sources[key]['sha256']: raise ValueError('Source changed during preparation: '+key)
    emit('STATIC_RECEIPT.json',dict(status='AST_PARSED_AND_METADATA_PINNED_ONLY',
        created_utc=datetime.now(timezone.utc).isoformat(),generator_sha256=digest(generator),
        parsed_python_files={n:digest(HERE/n) for n in own_trees},imports=sorted(set(imports)),
        static_checks=['AST parse without import/exec','Import allowlist','No assert guards','No dynamic execution calls',
                       'activate precedes assemble in main AST','ten unique readings agree with C1','source byte pins unchanged'],
        generator_executed=False,science_executed=False,negative_fixtures_executed=False,
        output_schema_runtime_validation_performed=False,
        limitation='Static checks are not proof of runtime behavior, data mapping, scientific validity or E6 completion'))
    artifacts={}
    for path in sorted(HERE.iterdir()):
        if not path.is_file() or path.name.startswith('.'): continue
        if path.stat().st_size>LIMIT: raise ValueError('Oversized output')
        artifacts[path.name]=dict(sha256=digest(path),bytes=path.stat().st_size)
    emit('PREPARATION_MANIFEST.json',dict(schema='E6_PREPARATION_MANIFEST_V1',status='READY_FOR_REVIEW_NOT_EXECUTED',
        created_utc=datetime.now(timezone.utc).isoformat(),artifacts=artifacts,
        self_hash='External delivery only; avoids circular self-reference',
        activation_package_sha256={name:digest(HERE/name) for name in contract['authorization_contract']['package_files']},
        registration_sha256=sources['E2']['sha256'],E6_executed=False,E7_extraction_authorized=False,order_completed=False))
    print(json.dumps(dict(status='PREPARATION_ONLY_AST_COMPLETE',manifest_sha256=digest(HERE/'PREPARATION_MANIFEST.json'),
                          artifacts=len(artifacts)+1,generator_executed=False,science_executed=False)))


if __name__=='__main__':
    main()
