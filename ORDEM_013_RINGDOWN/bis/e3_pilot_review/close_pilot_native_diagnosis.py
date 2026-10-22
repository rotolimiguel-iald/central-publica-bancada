"""Independent documentary closure of A's bounded diagnosis. No native execution."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib,json,math

HERE=Path(__file__).resolve().parent
B=HERE.parents[1];D=B/'bis/e3_pilot_failure_diagnostic'
checks=[];pins={}
def sha(p):
    v=hashlib.sha256(p.read_bytes()).hexdigest();pins[str(p)]=v;return v
def load(p):
    sha(p);return json.loads(p.read_bytes())
def check(name,ok):
    checks.append({'name':name,'passed':bool(ok)})
    if not ok:raise ValueError(name)

class ExtractLines(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.depth=0;self.current=[];self.lines=[]
    def handle_starttag(self,tag,attrs):
        if tag=='div':
            if self.depth:self.depth+=1
            elif 'line' in dict(attrs).get('class','').split():self.depth=1;self.current=[]
    def handle_endtag(self,tag):
        if tag=='div' and self.depth:
            self.depth-=1
            if not self.depth:self.lines.append(''.join(self.current))
    def handle_data(self,data):
        if self.depth:self.current.append(data)

diagnosis=load(D/'DIAGNOSIS.json');manifest=load(D/'MANIFEST.json')
check('A_closed_without_repair',diagnosis['status']=='DIAGNOSTIC_COMPLETE_REPAIR_NOT_IMPLEMENTED_OR_APPROVED')
check('A_checks_reported_true',len(diagnosis['checks'])==96 and all(c['passed'] is True for c in diagnosis['checks']))
entries=manifest['files'];names=[e['relative_path'] for e in entries]
check('manifest_unique',len(names)==len(set(names)))
check('manifest_complete',set(names)|{'MANIFEST.json'}=={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()})
for e in entries:
    p=D/e['relative_path']
    check('confined:'+e['relative_path'],p.resolve().is_relative_to(D.resolve()))
    check('manifest_pin:'+e['relative_path'],sha(p)==e['sha256'] and p.stat().st_size==e['bytes'])
addendum=load(D/'SOURCE_HASH_ADDENDUM.json')
oldreview=load(HERE/'PILOT_NATIVE_DIAGNOSTIC_INDEPENDENT_REVIEW.json')
plan=load(D/'PLAN_INPUTS.json')
check('original_plan_preserved',sha(D/'PLAN_INPUTS.json')==addendum['original_plan']['sha256']==oldreview['input_hashes'][str(D/'PLAN_INPUTS.json')])
check('mapping_set_three',len(addendum['mappings'])==3)
for item in addendum['mappings']:
    original=item['original_plan_entry_preserved']
    check('original_entry_preserved:'+original['primary_url'],original in plan['source_evidence'])
    for key in ('correct_html','correct_extracted_text'):
        e=item[key];p=Path(e['path'])
        check('mapped_path:'+key+':'+p.name,p.resolve().is_relative_to(D.resolve()))
        check('mapped_hash_bytes:'+key+':'+p.name,sha(p)==e['sha256'] and p.stat().st_size==e['bytes'])
    html=Path(item['correct_html']['path']);txt=Path(item['correct_extracted_text']['path'])
    check('original_HTML_identity:'+html.name,sha(html)==original['sha256'] and html.stat().st_size==original['bytes'])
    parser=ExtractLines();parser.feed(html.read_text(encoding='utf-8'))
    check('independent_reextraction:'+txt.name,('\n'.join(parser.lines)+'\n').encode()==txt.read_bytes())
static=load(D/'STATIC_SOURCE_ADDITION.json')
for e in static['sources']:
    check('additional_html_pin:'+e['html'],sha(D/'sources'/e['html'])==e['html_sha256'])
    check('additional_text_pin:'+e['text'],sha(D/'sources'/e['text'])==e['text_sha256'])
    parser=ExtractLines();parser.feed((D/'sources'/e['html']).read_text(encoding='utf-8'))
    check('additional_reextraction:'+e['text'],('\n'.join(parser.lines)+'\n').encode()==(D/'sources'/e['text']).read_bytes())
controllers=[load(p) for p in sorted((D/'cases').glob('*.CONTROLLER.json'))]
deadline=datetime.fromisoformat(plan['deadline_utc'])
check('cap_ten_no_extra',len(controllers)==plan['max_sequential_waveform_children']==10)
check('all_children_finished_before_diagnostic_deadline',all(datetime.fromisoformat(c['finished_utc'])<deadline for c in controllers))
check('diagnostic_deadline_passed',datetime.now(timezone.utc)>deadline)
last=max(datetime.fromisoformat(c['finished_utc']) for c in controllers)
source_calls=list((D/'cases').glob('*.CALL_*.json'));returns=list((D/'cases').glob('*.RETURN_*.json'))
check('finite_calls_16_returns_15',len(source_calls)==16 and len(returns)==15)
drawlow=load(D/'cases/DRAW8_1024.json');drawhigh=load(D/'cases/DRAW8_2048.json')
diff=[k for k in set(drawlow)|set(drawhigh) if drawlow.get(k)!=drawhigh.get(k)]
check('draw8_only_generation_fmax_changed',diff==['generation_fmax'])
check('draw8_is_inside_original_prior',all(plan['pilot_configuration_INPUT']['priors'][k]['minimum']<=v<=plan['pilot_configuration_INPUT']['priors'][k]['maximum'] for k,v in drawhigh['parameters'].items()))
check('draw8_mass_ratio_allowed',.125<=drawhigh['parameters']['mass_2']/drawhigh['parameters']['mass_1']<=1)
check('draw8_abort_observed',load(D/'cases/DRAW8_2048.CONTROLLER.json')['returncode']==-6)
check('no_draw8_8192_evidence',not (D/'cases/DRAW8_8192.CONTROLLER.json').exists())
buffer=(D/'sources/LALSimIMRSpinAlignedEOB.c').read_text()
attach=(D/'sources/LALSimIMREOBHybridRingdown.c').read_text()
check('buffer_expansion_dtau220_static','if(dtau220 > 0)' in buffer and '20 * (1. + dtau220)' in buffer)
check('mode440_tail_static','cimag(modefreqs->data[0])/(1. + dtau440)' in attach)
check('mode_dependent_length_static','EOB_RD_EFOLDS / cimag(modefreqs->data[0]) / dt' in attach)
reg=load(B/'RINGDOWN_5SIGMA_V1.json');code=B/'bis/e2_code'
check('fourteen_original_sources_intact',{p.relative_to(code).as_posix():sha(p) for p in code.rglob('*.py')}==reg['own_code_tree_sha256'])
ctx=load(B/'cache/E3_PSEOB_PILOT_V1/LAUNCH_CONTEXT.json')
check('original_pilot_stop_preserved',diagnosis['original']['stop_utc_retained']==ctx['stop_utc'])
report={
 'status':'BOUNDED_DIAGNOSIS_CLOSED_TECHNICAL_WALL_NO_SUPPORTED_PE_ADAPTER',
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'diagnostic_closure_blocking_findings':[],
 'continuation_blocking_findings':[
   {'id':'NF-R2','status':'TECHNICAL_WALL_WITHIN_CURRENT_EVIDENCE_AND_FROZEN_RUNTIME','reason':'No concrete implemented and validated numerical adapter preserves the full registered source domain and likelihood band; changing fmax2048 has an observed native abort,8192 has only limited passing cases.'},
   {'id':'NF-R3','status':'NO_EXECUTION_APPROVAL','reason':'No concrete reviewed versioned amendment/launcher exists. Documentary witness alone cannot supply missing waveform/likelihood validity.'}],
 'closed_findings':[{'id':'NF-R4','status':'CLOSED','evidence':'Preserved original plan; HTML/text hashes and independent byte-identical extraction verified.'}],
 'original_SIGSEGV_root_cause':'OPEN; not imposed as universal prerequisite for future concrete fail-closed repair.',
 'candidate_assessment':[
   {'candidate':'higher_fmax2048_only','decision':'UNSUPPORTED','evidence':'DRAW8_2048 rc-6 allocator failure for the same registered point.'},
   {'candidate':'higher_fmax8192_only','decision':'NOT_ESTABLISHED','evidence':'Passing DRAW2 and representative LOW_DEFORMED do not test failing DRAW8 or complex-band transport; no new campaign authorized.'},
   {'candidate':'raise_EDOM_instead_of_None_and_isolate_native_calls','decision':'CONTAINMENT_DESIGN_ONLY_NOT_A_WORKING_PE_REPAIR','evidence':'Can preserve integrity by visibly aborting the attempt, but cannot provide missing likelihood or protect against silent finite corruption without a concrete verified implementation.'},
   {'candidate':'clip_dtau_or_domega_remove_modes_reject_failing_points','decision':'OUTSIDE_CONTRACT','evidence':'Changes registered prior/support/family; not a technical repair preserving the requested model.'},
   {'candidate':'native_buffer_capacity_repair','decision':'FUTURE_ENGINEERING_HYPOTHESIS_NOT_AUTHORIZED_OR_VALIDATED_HERE','evidence':'Requires actual capacity/offset/overflow checks and source/binary/import validation in separate version; cannot be supplied by an external Python retry while runtime remains frozen.'}],
 'finite_action_now':'Close this diagnostic window and record pilot technically unavailable for the registered model in the current runtime. Preserve priors, data, failed output and budget. Do not launch unchanged PE or an fmax-only workaround. Continue other independent authorized order items.',
 'future_reopening_condition':'A concrete separately versioned repaired implementation with evidence for the known failing point, numerical transport and visible-error semantics may be reviewed. No demand to prove every native root cause; no additional campaign or runtime mutation is authorized by this receipt.',
 'timing':{'diagnostic_deadline_utc':plan['deadline_utc'],'last_native_child_finish_utc':last.isoformat(),
           'pilot_original_absolute_stop_utc':ctx['stop_utc'],'diagnostic_and_pilot_deadlines_are_distinct':True,
           'summed_child_wall_seconds':math.fsum(c['wall_seconds'] for c in controllers),
           'summed_child_cpu_seconds':math.fsum(c['child_cpu_seconds'] for c in controllers)},
 'source_hypothesis_status':'CONJECTURE: dtau220-driven allocation vs mode-specific dtau440-dependent attachment can motivate capacity review; retLen/indAmax/Nrdwave inequality not measured for failure.',
 'coordination':'Read A final DIAGNOSIS/manifest/addendum and underlying completed receipts; no claim of direct message or additional execution.',
 'checks':checks,'check_count':len(checks),'input_hashes':pins,
 'scientific_execution':False,'waveforms_executed_by_reviewer':0,'PE_executed_by_reviewer':0,
 'strain_or_posterior_read':False,'execution_authorized':False,'old_receipts_preserved':True,
 'script_sha256':sha(Path(__file__))}
out=HERE/'PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json'
with out.open('xb') as f:f.write((json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
print(json.dumps({'status':report['status'],'checks':len(checks),'receipt_sha256':sha(out),'closed':['NF-R4'],'wall':report['timing']},indent=2))
