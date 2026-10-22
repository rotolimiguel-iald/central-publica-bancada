"""Produce v2 contract/schema metadata only; AST parse, no generator execution."""
from pathlib import Path
import ast,hashlib,json,os,copy

HERE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def emit(name,obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>25_000_000:raise ValueError('Size cap')
    p=HERE/name;t=p.with_name(p.name+'.pending')
    with t.open('xb') as f:f.write(raw)
    if t.stat().st_size!=len(raw):raise ValueError('Short write')
    os.link(t,p);t.unlink()


def main():
    tree=ast.parse((HERE/'generate_reach_table.py').read_bytes())
    constants={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
               and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('SEMANTIC_UNITS','FUTURE_GROUPS','EVIDENCE_VERDICTS')}
    old=json.loads((HERE/'v1_snapshot/CONTRACT.json').read_bytes())
    stage=json.loads((HERE/'v1_snapshot/STAGE_RECEIPT_SCHEMA.json').read_bytes())
    pin=copy.deepcopy(stage['properties']['artifact'])
    pointer={'type':'string','pattern':'^(/.*)?$'}
    timeline={'type':'object','required':['kind','evidence'],
        'properties':{'kind':{'enum':['ALLOCATION_REGISTERED','EXECUTED','NO_EXECUTION']},'evidence':pin,
        **{k:pointer for k in ('authorized_utc_pointer','started_utc_pointer','finished_utc_pointer',
             'recorded_utc_pointer','reason_pointer','predecessor_evidence_sha256_pointer')}},
        'additionalProperties':False,
        'allOf':[{'if':{'properties':{'kind':{'const':'NO_EXECUTION'}}},
                  'then':{'required':['recorded_utc_pointer','reason_pointer']},
                  'else':{'required':['authorized_utc_pointer','started_utc_pointer','finished_utc_pointer']}}]}
    stage['properties']['schema']={'const':'E6_REVIEWED_STAGE_V2'}
    stage['properties'].update(predecessor=pin,timeline=timeline)
    stage['required']+=['predecessor','timeline']
    stage['allOf']=[{'if':{'properties':{'stage':{'enum':['E3.3','TEST']}}},
                     'then':{'properties':{'timeline':{'required':['predecessor_evidence_sha256_pointer']}}}}]
    stage['$comment']='V2 reviewed source chronology/predecessor metadata; no fabricated execution timestamps. Semantic enforcement in generator.'
    emit('STAGE_RECEIPT_SCHEMA.json',stage)
    old.update(schema='E6_PREPARATION_CONTRACT_V2',status='PREPARED_V2_NOT_AUTHORIZED',
        supersedes_manifest_sha256=sha(HERE/'v1_snapshot/PREPARATION_MANIFEST.json'),
        semantic_units=constants['SEMANTIC_UNITS'],future_projection_only_groups=constants['FUTURE_GROUPS'],
        evidence_verdicts=constants['EVIDENCE_VERDICTS'],
        stage_receipt_schema_sha256=sha(HERE/'STAGE_RECEIPT_SCHEMA.json'),
        timeline_contract={'activation_floor':'E2_ACTIVATION_COMPLETE.finished_utc',
            'receipt_predecessors':'E3.2->E2_ACTIVATION, E3.3->E3.2, TEST->E3.3; exact path and SHA',
            'source_predecessors':'E3.3/TEST timeline evidence binds prior timeline evidence SHA by explicit source pointer',
            'source_times':'Pinned JSON pointers, separately from actual adapter issuance; no retrospective fabrication',
            'execution_order':'Prior effective finish <= next effective start; activity/wall at or after activation floor',
            'existing_GO':'Authorization source may predate activation; activity may not',
            'no_execution':'PARTIAL/BLOCKED/UNAVAILABLE wall requires sourced recorded time and reason, no invented start/end',
            'review_coverage':'Independent review repeats exact timeline and predecessor'},
        verification_scope='Metadata-only finite fixtures plus AST; no actual E6 assembly, source numerics unchanged',
        mapping='v1_snapshot/SOURCE_MAP.md plus PREPARATION_V2.md semantic restrictions')
    old['authorization_contract']['chronology']='Aware actual source activity chronology after E2 activation plus ordered adapters/reviews before E6 authorization <= now'
    old['independent_review_contract']['required']+=['timeline','predecessor']
    old['source_test_summary_contract']['underpowered']='power_assessment=INSUFFICIENT_REVIEWED; paid validity, no high power threshold'
    old['source_test_summary_contract']['future_groups']='AWAITING_DATA, test_data_present=false, all explicit physical quantities null; no current-contract exception'
    old['source_test_summary_contract']['physical_fields']=['z_physical','lnB','gate.correction_over_sigma_physical']
    old['source_gate_contract']['calibration_ratio']='E3.3 physical ratio must be null; TEST ratio is not compared to absent calibration-stage observation'
    emit('CONTRACT.json',old)
    schema=json.loads((HERE/'v1_snapshot/OUTPUT_SCHEMA.json').read_bytes())
    schema['properties']['schema']={'const':'E6_REACH_TABLE_V2'}
    cell=schema['properties']['cells']['items'];cell['allOf']=[]
    for route,units in constants['SEMANTIC_UNITS'].items():
        props={'metrics':{'properties':{}},'gate':{'properties':{}}}
        for name,allowed in units.items():
            group='metrics' if name in old['metrics'] else 'gate'
            typed={'if':{'properties':{'value':{'not':{'type':'null'}}}},
                   'then':{'properties':{'unit':{'enum':allowed}}}} if allowed else {'properties':{'value':{'type':'null'}}}
            props[group]['properties'][name]={'allOf':[typed]}
        cell['allOf'].append({'if':{'properties':{'route':{'const':route}}},
                             'then':{'properties':{'scenarios':{'items':{'properties':props}}}}})
    nullmetric={'properties':{'value':{'type':'null'}}}
    cell['allOf'].append({'if':{'properties':{'data_group':{'enum':constants['FUTURE_GROUPS']}}},
        'then':{'properties':{'scenarios':{'items':{'properties':{'verdict':{'const':'AWAITING_DATA'},
            'physical_test_present':{'const':False},'metrics':{'properties':{'z_physical':nullmetric,'lnB':nullmetric}},
            'gate':{'properties':{'correction_over_sigma_physical':nullmetric}}}}}}}})
    emit('OUTPUT_SCHEMA.json',schema)
    print(json.dumps(dict(status='V2_METADATA_PREPARED_NO_GENERATOR_EXECUTION',generator_sha256=sha(HERE/'generate_reach_table.py'))))


if __name__=='__main__':main()
