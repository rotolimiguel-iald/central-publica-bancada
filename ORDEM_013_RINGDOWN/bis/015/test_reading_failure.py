"""Per-reading permissions and real PE exception-handler probes; no PE or seed read."""
from pathlib import Path
from datetime import datetime,timezone
from unittest.mock import patch
import ast,copy,hashlib,json,multiprocessing,sys,time
B=Path(__file__).resolve().parents[2];C=B/'bis/e2_code_v1_1';D=B/'bis/015/t03/reading_failure_tests_001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    wall=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False);sys.path.insert(0,str(C))
    import blinding as b,pe_runner as runner,pseob_source as source
    original=json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes());reg=copy.deepcopy(original)
    targets={x['reading']:x['I_tau_expected_target90'] for x in original['planning_targets'] if x['population']=='GWTC5_31'}
    reg['blinding']['minimum_information_to_unblind_by_reading']=targets
    dataset=hashlib.sha256(b'SYNTHETIC READINGS ONLY').hexdigest();reg['blinding']['unblinding_dataset_sha256']=dataset
    reg['blinding']['release_columns_by_reading']={'R-LIN':['R-LIN:matched_z'],'R-B':['R-B:matched_z']}
    information=targets['R-LIN'];receipt=dict(status='REGISTERED_UNBLINDING_GATE_MET',reading='R-LIN',scope='per-reading',
        information=information,systematic_gate=True,independent_review_passed=True,dataset_sha256=dataset,
        seed_commitment_sha256=reg['blinding']['seed_commitment_sha256'],registration_id=reg['registration_id'],released_columns=['R-LIN:matched_z'])
    results=[]
    def equal(name,actual,expected):
        assert actual==expected,(name,actual,expected);results.append(dict(name=name,passed=True))
    def denied(name,fn):
        try:fn()
        except ValueError:results.append(dict(name=name,passed=True));return
        raise AssertionError('Expected refusal '+name)
    equal('exact_R_LIN_target_allowed',b.unblinding_allowed(reg,'R-LIN',information,True,receipt),True)
    for name,value in [('below_exact_target',information-1),('below_rounded_7513_27',7513.26),('nan_information',float('nan')),('infinite_information',float('inf')),('boolean_information',True),('string_information','7513.27')]:
        r=copy.deepcopy(receipt);r['information']=value
        equal(name,b.unblinding_allowed(reg,'R-LIN',value,True,r),False)
    r=copy.deepcopy(receipt);r['information']=7513.27;equal('above_exact_target_7513_27',b.unblinding_allowed(reg,'R-LIN',7513.27,True,r),True)
    for reading in ['ABSENT']+[k for k,v in targets.items() if v is None]:
        equal('no_target_'+reading,b.unblinding_allowed(reg,reading,information,True,receipt),False)
    equal('red_systematics_gate',b.unblinding_allowed(reg,'R-LIN',information,False,receipt),False)
    for name,key,value in [('another_reading','reading','R-B'),('global_scope','scope','global'),('bad_dataset','dataset_sha256','x'*64),
        ('another_registration','registration_id','WRONG'),('seed_commitment_changed','seed_commitment_sha256','0'*64),
        ('review_unpaid','independent_review_passed',False),('receipt_gate_red','systematic_gate',False)]:
        r=copy.deepcopy(receipt);r[key]=value;equal(name,b.unblinding_allowed(reg,'R-LIN',information,True,r),False)
    columns={'R-LIN:matched_z':[1.,2.],'R-B:matched_z':[3.,4.],'dtau220':[9.,9.]}
    with patch.object(b,'contained',side_effect=AssertionError('No seed path may be accessed')):
        selected=b.select_authorized_reading(columns,reg,'R-LIN',information,True,receipt)
        equal('only_authorized_reading_columns',selected['columns'],{'R-LIN:matched_z':[1.,2.]})
    m=copy.deepcopy(reg);m['blinding']['release_columns_by_reading']['R-LIN']=['dtau220'];r=copy.deepcopy(receipt);r['released_columns']=['dtau220']
    denied('raw_shared_posterior_not_per_reading_release',lambda:b.select_authorized_reading(columns,m,'R-LIN',information,True,r))
    r=copy.deepcopy(receipt);r['released_columns']=['R-B:matched_z']
    denied('release_receipt_wrong_columns',lambda:b.select_authorized_reading(columns,reg,'R-LIN',information,True,r))
    # Verify the amended reporting did not change the R5-qualified source/prior functions.
    sc=json.loads((B/'bis/015/t03/R5_SOURCE_CLOSING.json').read_bytes())
    for label,pin in sc['source_path_function_hashes'].items():
        file,name=label.split(':');node=next(n for n in ast.parse((C/file).read_text()).body if isinstance(n,ast.FunctionDef) and n.name==name)
        equal('R5_AST_'+label,hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest(),pin)
    # Directly drive the original main entry's exception path after source initialization.
    def run_failure(case,count,measured,early=False):
        out=D/case;out.mkdir();cfg={'event':'SYNTHETIC_CALIBRATION','mode':'calibration'}
        context={'stop_utc':datetime.now(timezone.utc).isoformat()}
        def injected_deadline(_):
            with source.COST_COUNTER.get_lock():source.COST_COUNTER[0]=5;source.COST_COUNTER[2]=measured
            with (out/'EDOM_LOG.jsonl').open('a',encoding='utf-8') as f:
                for _ in range(count):f.write(json.dumps({'parameters':dict(mass_1=15.,mass_2=10.,chi_1=.99,chi_2=.99),'status':'SYNTHETIC_EDOM'})+'\n')
            raise RuntimeError('Injected before PE; no strain or likelihood evaluated')
        with patch.object(sys,'argv',['pe_runner.py','--job','SYNTHETIC_JOB','--launch-context','FIXTURE']),\
             patch.object(runner,'checked_registration',return_value=({},'a'*64)),\
             patch.object(runner,'load_jobs',return_value={'SYNTHETIC_JOB':cfg}),\
             patch.object(runner,'authorize_event',return_value=True),\
             patch.object(runner,'validate_config',return_value=True),\
             patch.object(runner,'validate_launch',return_value=(context,out)),\
             patch.object(source,'set_deadline',side_effect=injected_deadline),\
             patch.object(multiprocessing,'get_start_method',return_value='spawn' if early else 'fork'):
            try:runner.main()
            except RuntimeError as e:
                if early:assert 'WSL fork workers' in str(e)
                else:assert 'Injected before PE' in str(e)
            else:raise AssertionError('Synthetic exception was swallowed')
        result=json.loads((out/'FAILURE.json').read_bytes())
        equal(case+'_no_accepted_posterior',result['status'],'FAILED_NO_ACCEPTED_POSTERIOR')
        return out,result['edom']
    out,edom=run_failure('after_initialization',2,2)
    equal('exception_records_EDOM_fraction',edom['fraction'],2/5)
    equal('exception_records_EDOM_log_hash',edom['log_sha256'],sha(out/'EDOM_LOG.jsonl'))
    equal('exception_does_not_claim_region_checked',edom['inside'],None)
    equal('exception_summary_preserved',json.loads((out/'EDOM_SUMMARY.json').read_bytes()),edom)
    _,edom=run_failure('counter_log_mismatch',1,2);equal('audit_failure_visible',edom['status'],'EDOM_AUDIT_FAILED')
    _,edom=run_failure('before_initialization',0,0,True);equal('no_initialized_counter_visible',edom['status'],'EDOM_UNAVAILABLE_BEFORE_SOURCE_INITIALIZATION')
    assert not (B/'bis/PART_015_BUDGET_START.json').exists()
    result=dict(status='READING_AND_EXCEPTION_CONTROLS_PASSED',tests=results,
        files_sha256={n:sha(C/n) for n in ('blinding.py','pe_runner.py')},target_R_LIN_exact=information,
        seed_read=False,physical_data_unblinded=False,PE_started=False,heavy_machine_hours=0,
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,
        limit='Tests use synthetic reading-labelled columns and injected ordinary exceptions. Fatal native signals cannot execute a Python exception handler.')
    with (D/'RESULT.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ('status','cpu_seconds','wall_seconds','target_R_LIN_exact')}|{'tests':len(results)}))
if __name__=='__main__':main()
