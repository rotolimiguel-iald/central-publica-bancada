"""Inactive until principal GO; inspect produced E6 metadata without assembly/science."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import itertools
import json
import math
import os
import re

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ROOT = B.parent
PACKAGE = B / 'bis/e6_prepare_v3'
LIMIT = 25 * 1024 * 1024
STAGES = ('E3.2', 'E3.3', 'TEST')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    require(Path(path).stat().st_size <= LIMIT, 'Metadata exceeds 25 MiB')
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate key: ' + key)
            result[key] = value
        return result
    def number(raw):
        value = float(raw)
        require(math.isfinite(value), 'Nonfinite number')
        return value
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
        parse_float=number, parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))


def exact(left, right):
    return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(right, sort_keys=True, allow_nan=False)


def utc(text):
    value = datetime.fromisoformat(text.replace('Z', '+00:00'))
    require(value.tzinfo is not None, 'Naive timestamp')
    return value.astimezone(timezone.utc)


def pointer(value, path):
    require(isinstance(path, str) and (path == '' or path.startswith('/')), 'Invalid JSON pointer')
    for token in path[1:].split('/') if path else []:
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            require(re.fullmatch(r'0|[1-9][0-9]*', token) is not None, 'Invalid array pointer')
            value = value[int(token)]
        else:
            value = value[token]
    return value


class Audit:
    def __init__(self):
        self.pins = {}
        self.objects = {}
        self.checks = []
        self.copies = 0

    def check(self, label, ok):
        self.checks.append({'name': label, 'passed': bool(ok)})
        require(ok, label)

    def pinned(self, ref):
        require(set(ref) == {'path', 'sha256'}, 'Pin shape')
        relative = Path(ref['path'])
        require(not relative.is_absolute(), 'Absolute source path')
        path = (ROOT / relative).resolve()
        require(path.is_relative_to(B.resolve()) or path.is_relative_to((ROOT/'TUNEL/DO_CHATGPT').resolve()), 'Source outside package/tunnel')
        require(path.suffix.lower() in ('.json', '.md') and not path.is_symlink(), 'Metadata files only')
        require(not any('PRIVATE' in part.upper() or part.lower() == 'cache' for part in path.parts), 'No private/cache payload inspection')
        require(re.fullmatch('[0-9a-f]{64}', ref['sha256']) is not None, 'SHA256 format')
        require(path.stat().st_size <= LIMIT and sha(path) == ref['sha256'], 'Source hash/size: ' + str(path))
        self.pins[str(path)] = ref['sha256']
        return path

    def obj(self, ref):
        path = self.pinned(ref)
        if str(path) not in self.objects:
            self.objects[str(path)] = read(path)
        return self.objects[str(path)]

    def metric(self, label, metric, allowed_refs, units=None):
        self.check(label+' shape', set(metric) == {'value','status','unit','source','reason'})
        self.check(label+' labels', all(isinstance(metric[k],str) and metric[k] for k in ('status','unit','reason')))
        value = metric['value']; ref = metric['source']
        if value is None:
            self.check(label+' null stays OPEN', metric['status'] == 'OPEN')
        else:
            self.check(label+' numeric shape', type(value) in (int,float) or (isinstance(value,list) and all(type(x) in (int,float) for x in value)))
            self.check(label+' numeric source', ref is not None)
            if units is not None:
                self.check(label+' semantic unit', metric['unit'] in units)
        if ref is not None:
            self.check(label+' source allowed', set(ref) == {'path','sha256','pointer'} and (ref['path'],ref['sha256']) in allowed_refs)
            obj = self.obj({'path':ref['path'],'sha256':ref['sha256']})
            try:
                copied = pointer(obj, ref['pointer'])
            except (KeyError, IndexError):
                self.check(label+' missing pointer explicit OPEN', value is None and metric['status'] == 'OPEN')
            else:
                self.check(label+' exact source-pointer copy', exact(value,copied))
                self.copies += 1


def inspect(args, audit):
    prep = read(HERE/'PREPARATION_RECEIPT.json')
    audit.check('verifier preparation pin',sha(__file__)==prep['verifier_sha256'])
    for name, digest in prep['package_pins'].items():
        audit.check('prepared package '+name, sha(PACKAGE/name) == digest)
    result_ref = {'path':args.result.resolve().relative_to(ROOT).as_posix(),'sha256':args.result_sha256}
    auth_ref = {'path':args.authorization.resolve().relative_to(ROOT).as_posix(),'sha256':args.authorization_sha256}
    data = audit.obj(result_ref); auth = audit.obj(auth_ref)
    contract = read(PACKAGE/'CONTRACT.json')
    frozen = read(PACKAGE/'SOURCE_PINS.json')['sources']
    audit.check('E6 schema/status', data['schema']=='E6_REACH_TABLE_V2' and data['status']=='ASSEMBLED_REVIEWED_SOURCES_NOT_NEW_SCIENCE')
    audit.check('authorization package', auth['package_sha256'] == {n:prep['package_pins'][n] for n in auth['package_sha256']} and set(auth['package_sha256']) == {'generate_reach_table.py','CONTRACT.json','SOURCE_PINS.json','OUTPUT_SCHEMA.json'})
    audit.check('authorization purpose', auth['status']=='AUTHORIZED_E6_ASSEMBLY_AFTER_REVIEWED_E3_AND_TEST' and auth['new_scientific_computation_allowed'] is False)
    audit.check('authorization result pin', data['authorization_sha256']==args.authorization_sha256)
    audit.check('generator pin', data['generator_sha256']==prep['package_pins']['generate_reach_table.py'])
    reg = audit.obj(auth['registration'])
    audit.check('E2 identity', auth['registration']==frozen['E2'] and data['registration_sha256']==frozen['E2']['sha256'])
    witness = audit.pinned(auth['witness']).read_text(encoding='utf-8-sig')
    audit.check('E2 witness', re.findall(r'^registro_sha256: ([0-9a-f]{64})\s*$',witness,re.M)==[data['registration_sha256']])
    activation = audit.obj(frozen['E2_ACTIVATION'])
    audit.check('E2 activated', activation['status']=='E2_ACTIVATION_COMPLETE' and activation['registration_sha256']==data['registration_sha256'] and activation['witness_sha256']==auth['witness']['sha256'])
    floor = utc(activation['finished_utc']); issued = utc(auth['issued_utc'])
    audit.check('E2/auth chronology', utc(reg['registered_utc'])<=floor<=issued<=datetime.now(timezone.utc))
    audit.check('axes exact', data['readings']==contract['readings'] and data['routes']==contract['routes'] and data['data_groups']==contract['data_groups'])
    expected = set(itertools.product(contract['routes'],contract['readings'],contract['data_groups']))
    keys = [(x['route'],x['reading'],x['data_group']) for x in data['cells']]
    audit.check('180 unique cells 10x3x6',len(data['readings'])==10 and len(data['routes'])==3 and len(data['data_groups'])==6 and len(keys)==len(set(keys))==len(expected)==180 and set(keys)==expected)
    audit.check('no new physical computation',all(data[k] is False for k in ('new_scientific_computations','lnB_recomputed','E7_extraction_authorized','order_completed')))
    audit.check('three actual stage references',set(auth['reviewed_stages'])==set(STAGES) and data['reviewed_stage_receipts']==auth['reviewed_stages'])
    sources = dict(frozen); stages={}; previous=None; previous_ref=frozen['E2_ACTIVATION']; previous_finish=floor
    for stage in STAGES:
        ref=auth['reviewed_stages'][stage]; row=audit.obj(ref); review=audit.obj(row['review']); artifact=audit.obj(row['artifact'])
        audit.check(stage+' real adapter contract',row['schema']=='E6_REVIEWED_STAGE_V2' and row['stage']==stage and row['registration_sha256']==data['registration_sha256'])
        audit.check(stage+' independent review',review['status']=='ACCEPTED_FOR_E6_MAPPING' and review['stage']==stage and review['registration_sha256']==data['registration_sha256'] and review['artifact_sha256']==row['artifact']['sha256'] and review['blocking_findings']==[] and isinstance(review['reviewer'],str) and bool(review['reviewer'].strip()))
        audit.check(stage+' exact review mapping',all(exact(review[k],row[k]) for k in ('bindings','timeline','predecessor','outcome')))
        ri=utc(row['issued_utc']); rt=utc(review['reviewed_utc'])
        audit.check(stage+' issuance chronology',floor<=ri<=rt<=issued and (previous is None or utc(previous['issued_utc'])<=ri))
        audit.check(stage+' predecessor receipt',row['predecessor']==previous_ref)
        tl=row['timeline']; evidence=audit.obj(tl['evidence'])
        if previous is not None:
            audit.check(stage+' predecessor source',pointer(evidence,tl['predecessor_evidence_sha256_pointer'])==previous['timeline']['evidence']['sha256'])
        if tl['kind']=='NO_EXECUTION':
            audit.check(stage+' wall outcome',row['outcome'] in ('PARTIAL','BLOCKED','UNAVAILABLE'))
            reason=pointer(evidence,tl['reason_pointer'])
            audit.check(stage+' sourced wall reason',isinstance(reason,str) and bool(reason.strip()))
            start=finish=utc(pointer(evidence,tl['recorded_utc_pointer']))
        else:
            audit.check(stage+' allocation only',stage=='E3.2' and tl['kind']=='ALLOCATION_REGISTERED' and row['outcome'] in ('COMPLETED','PARTIAL'))
            start=utc(pointer(evidence,tl['started_utc_pointer']));finish=utc(pointer(evidence,tl['finished_utc_pointer']))
            audit.check(stage+' source authorization',utc(pointer(evidence,tl['authorized_utc_pointer']))<=start)
        if stage=='E3.2':
            audit.check('actual documentary budget slot',row['artifact']['path']=='ORDEM_013_RINGDOWN/ORCAMENTO_40H.json' and artifact['status']=='REGISTERED_ZERO_NEW_PE_MEASURED_INSTRUMENT_WALL')
            audit.check('actual zero new allocation',all(type(artifact['allocation'][k]) is int and artifact['allocation'][k]==0 for k in ('new_PE_count','new_injection_count','new_download_count','new_science_wall_seconds','pipeline_repair_seconds')))
        else:
            audit.check(stage+' wall source scope',artifact['status']=='NO_EXECUTION' and artifact['test_posterior_available'] is False and artifact['cost_per_converged_PE'] is None)
        audit.check(stage+' sourced actual chronology',floor<=previous_finish<=start<=finish<=ri<=issued)
        sources['STAGE_'+stage]=row['artifact'];stages[stage]=(row,artifact,ref)
        previous=row;previous_ref=ref;previous_finish=finish
    audit.check('exact source pin set',data['source_pins']==sources)
    allowed={(v['path'],v['sha256']) for v in sources.values()}
    for ref in sources.values(): audit.obj(ref)
    cells={key:cell for key,cell in zip(keys,data['cells'])};mapped=set()
    for stage,(row,artifact,ref) in stages.items():
        for binding in row['bindings']:
            key=tuple(binding[k] for k in ('route','reading','data_group')); identity=stage+':'+binding['scenario_id']
            match=[x for x in cells[key]['scenarios'] if x['id']==identity]
            audit.check(stage+' binding represented '+str(key)+identity,len(match)==1)
            scenario=match[0];mapped.add((key,identity))
            audit.check(identity+' stage transport',scenario['stage_outcome']==row['outcome'] and scenario['scope']==binding['scope'] and scenario['references']==[ref,row['review'],row['artifact']])
            for name,mapping in binding['metrics'].items():
                audit.check(identity+'/'+name+' binding',scenario['metrics'][name]['source']==dict(**row['artifact'],pointer=mapping['pointer']) and scenario['metrics'][name]['unit']==mapping['unit'])
            if binding.get('gate_pointer') is not None:
                gate=pointer(artifact,binding['gate_pointer'])
                audit.check(identity+' red gate',gate['color']=='red' and scenario['gate']['color']=='red' and scenario['gate']['status']==gate['status'])
                audit.check(identity+' unpaid physical calibration',gate['physical_calibration_paid'] is False)
                audit.check(identity+' paid flags copied',scenario['gate']['paid_flags']=={k:gate[k] for k in contract['paid_flags']})
            if stage=='TEST':
                summary=pointer(artifact,binding['test_summary_pointer'])
                audit.check(identity+' no observed test',summary['test_data_present'] is False and summary['verdict']=='AWAITING_DATA')
    scenarios=0
    for key,cell in cells.items():
        route=cell['route']; units=contract['semantic_units'][route]
        audit.check(str(key)+' reading statute',cell['reading_statute']==contract['reading_statutes'][cell['reading']])
        audit.check(str(key)+' scenarios unique',bool(cell['scenarios']) and len(cell['scenarios'])==len({x['id'] for x in cell['scenarios']}))
        for scenario in cell['scenarios']:
            label=str(key)+'/'+scenario['id'];scenarios+=1
            if any(scenario['id'].startswith(s+':') for s in STAGES):
                audit.check(label+' no extra mapped scenario',(key,scenario['id']) in mapped)
            audit.check(label+' absent physical test',scenario['physical_test_present'] is False and scenario['verdict']=='AWAITING_DATA')
            audit.check(label+' no green gate',scenario['gate']['color'] in ('red','OPEN'))
            audit.check(label+' metric set',set(scenario['metrics'])==set(contract['metrics']))
            for name,metric in scenario['metrics'].items(): audit.metric(label+'/'+name,metric,allowed,units[name])
            for name in contract['gate_fields']: audit.metric(label+'/gate/'+name,scenario['gate'][name],allowed,units[name])
            audit.check(label+' physical null',all(scenario['metrics'][n]['value'] is None for n in ('z_physical','lnB')) and scenario['gate']['correction_over_sigma_physical']['value'] is None)
        for j,context in enumerate(cell['rate_contexts']):
            audit.metric(str(key)+'/rate/'+str(j),context['rate'],allowed,units['rate_per_year'])
            audit.metric(str(key)+'/rate_CI/'+str(j),context['rate_CI'],allowed,units['rate_CI'])
        historical=cell.get('historical_gate_context')
        if historical is not None:
            audit.check(str(key)+' historical floor scope',route=='TAU220_POPULATION' and historical['color'] in ('red','OPEN') and historical['status']=='INPUT_HISTORICAL_220_REFERENCE_NOT_CURRENT_CALIBRATION')
            for name in ('sigma_c_calibrated','floor5_INPUT','floor15_sensitivity'):
                audit.metric(str(key)+'/historical/'+name,historical[name],allowed,units[name])
    context=data['E1_gate_context']; ref=context['source']
    audit.check('E1 gate context source',dict(path=ref['path'],sha256=ref['sha256'])==frozen['E1'] and exact(context['value'],pointer(audit.obj(frozen['E1']),ref['pointer'])))
    run=args.result.resolve().parent
    require(run.is_relative_to((PACKAGE/'runs').resolve()),'Result must be actual frozen-package run')
    receipt_path=run/'RESULT_RECEIPT.json'; receipt=read(receipt_path)
    markdown=run/'QUADRO_DE_ALCANCE_V1.md'
    audit.check('output artifact receipt hashes',receipt['json_sha256']==args.result_sha256 and receipt['markdown_sha256']==sha(markdown) and receipt['generator_sha256']==data['generator_sha256'] and receipt['registration_sha256']==data['registration_sha256'] and receipt['status']==data['status'] and receipt['E7_extraction_authorized'] is False)
    audit.pins[str(receipt_path)]=sha(receipt_path);audit.pins[str(markdown)]=sha(markdown)
    for path,digest in audit.pins.items(): audit.check('unchanged '+path,sha(path)==digest)
    for name,digest in prep['package_pins'].items():audit.check('final package pin '+name,sha(PACKAGE/name)==digest)
    return {'cells':180,'readings':10,'routes':3,'groups':6,'scenarios':scenarios,'exact_pointer_copies':audit.copies,'stage_outcomes':{s:stages[s][0]['outcome'] for s in STAGES}}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--principal-go',action='store_true')
    ap.add_argument('--result',type=Path);ap.add_argument('--result-sha256')
    ap.add_argument('--authorization',type=Path);ap.add_argument('--authorization-sha256')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    if not args.principal_go:
        print('INACTIVE: wait for principal GO and produced E6 result; no result inspected.')
        return
    require(all((args.result,args.result_sha256,args.authorization,args.authorization_sha256,args.output)), 'Explicit produced result/auth hashes and new output required')
    output=args.output.resolve()
    require(output.parent==HERE.resolve() and output.suffix=='.json' and not output.exists(),'Exclusive review output directly in reviewer folder')
    audit=Audit(); findings=[];summary={}
    try:
        summary=inspect(args,audit)
    except Exception as exc:
        findings=[{'type':type(exc).__name__,'message':str(exc)}]
    result=dict(status='E6_ACTUAL_RESULT_REVIEWED_DOCUMENTARY_ONLY' if not findings else 'E6_ACTUAL_REVIEW_BLOCKED',
        approved=not findings,e6_result_sha256=args.result_sha256,created_utc=datetime.now(timezone.utc).isoformat(),
        blocking_findings=findings,summary=summary,checks=audit.checks,verified_input_hashes=audit.pins,
        verifier_sha256=sha(__file__),assembler_rerun=False,scientific_recomputation=False,
        scope='Actual artifact transport, metadata chronology and no-physical-test scope only. No new physics, posterior/strain reads, assembler imports or reruns. Stage independent reviews are separately authored; chronology validates their pinned documentary claims, not independent OS proof of every activity.')
    raw=(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2)+'\n').encode()
    require(len(raw)<=LIMIT,'Review too large')
    temp=output.with_name(output.name+'.pending')
    with temp.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    require(temp.stat().st_size==len(raw),'Short review write')
    os.link(temp,output);temp.unlink()
    print(json.dumps({'approved':result['approved'],'review_sha256':sha(output),'blocking_findings':findings}))


if __name__=='__main__':main()
