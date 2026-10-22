"""Verify the single existing F9 result; never launch a solver or load candidates."""
import json
import math
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
from audit_inputs import file_info, save_json

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'f9_engine_assembly_integration_preparation'

def read(p):
    return json.loads(Path(p).read_bytes())

def sha(p):
    return file_info(p)['sha256']

def main():
    target = ROOT / 'RECIBO_ROOT_PREDICAO_F9.json'
    assert not target.exists()
    external = read(ROOT / 'F9_ENGINE_EXECUTION_TOOL_RECEIPT.json')
    assert external['exit_code'] == 0 and external['wall_time_seconds'] < 180
    assert 'session_id' not in external
    c = read(BASE / 'CONTRATO_WSL.json')
    rid = c['request_id']
    manifest = read(BASE / 'MANIFESTO_PREPARACAO.json')
    assert manifest['proposed_run_request_id'] == rid
    checked=[]
    for e in manifest['files']:
        actual=file_info(BASE/e['path'])
        assert all(actual[k]==e[k] for k in ('bytes','sha256')),e['path']
        checked.append(actual)
    r=read(BASE/'RESULT.json');claim=read(BASE/'CLAIM.json');auth=read(BASE/'AUTORIZACAO_ROOT.json')
    assert r['status']=='ENGINEERING_F9_PREDICTION_ONCE' and r['error'] is None
    assert r['primary_returncode']==r['cleanup_returncode']==0 and r['scientific_calls']==1
    assert r['request_id']==claim['request_id']==auth['request_id']==rid
    assert r['nonce']==claim['nonce'] and r['pid']==claim['pid']
    assert r['retry_allowed'] is False and r['D_read'] is False
    assert claim['authorization_sha256']==sha(BASE/'AUTORIZACAO_ROOT.json')
    assert claim['contract_sha256']==auth['contract_sha256']==sha(BASE/'CONTRATO_WSL.json')
    assert auth['review_sha256']==sha(BASE/'REVISAO_ROOT.json') and auth['authorized']
    assert auth['max_solver_calls']==1 and auth['no_observed_data'] and not auth['PE_authorized'] and not auth['D_authorized']
    linux=r['linux'];cleanup=r['cleanup'];child=linux['child'];case=BASE/'RUN/CASE'
    assert linux==read(BASE/'RUN/LINUX_RESULT.json') and child==read(case/'CASE_RESULT.json')
    assert cleanup==read(BASE/'RUN/CLEANUP_RESULT.json')
    for role,name in [('primary','LINUX_RESULT.json'),('cleanup','CLEANUP_RESULT.json')]:
        assert (BASE/f'RUN/{role}_stdout.bin').read_bytes()==(BASE/f'RUN/{name}').read_bytes()
        assert (BASE/f'RUN/{role}_stderr.bin').read_bytes()==b''
        cap=r['capture_state'][role]
        assert cap['all_readers_terminated'] and not cap['overflow']
        assert all(cap['eof'].values()) and all(v is None for v in cap['errors'].values())
    assert (BASE/'RUN/stdout.bin').read_bytes()==(case/'CASE_RESULT.json').read_bytes()
    assert (BASE/'RUN/stderr.bin').read_bytes()==b''
    assert linux['child_returncode']==0 and linux['child_reaped']
    assert child['status']=='ENGINEERING_PREDICTIONS_WRITTEN' and child['error'] is None
    assert child['solver_calls_attempted']==child['solver_calls_returned']==1
    assert child['module_errors']==child['native_mapping_errors']==[]
    assert child['observed_reads'] is False and child['D_read'] is False and child['new_children']==0
    assert child['parent_pid']==child['process']['ppid']==linux['process']['pid']
    assert child['process']==read(case/'CASE_CLAIM.json')['process']
    audit=child['audit_snapshot']
    assert audit['installed'] and not audit['latched'] and audit['journal_error'] is None
    assert audit['denial_count']==0 and audit['events']==[] and (case/'journal.jsonl').read_bytes()==b''
    assert cleanup['status']=='NO_LIVE_CONTROLLED_PROCESSES_VERIFIED' and cleanup['stopped']==[] and cleanup['error'] is None
    assert cleanup['launch_fence_persistent'] and (BASE/'RUN/STOP.json').is_file()
    for n,e in child['artifacts'].items():
        actual=file_info(case/n)
        assert all(actual[k]==e[k] for k in ('bytes','sha256'))
    bg=read(case/'BACKGROUND_RESULT.json');er=read(case/'ENGINE_EXECUTION_RECEIPT.json')
    packet=read(case/'BACKGROUND_PACKET.json');out=read(case/'FIVE_MODEL_OUTPUT.json')
    config=read(BASE/'EFFECTIVE_CONFIGURATION.json');parameters=read(BASE/'MODEL_PARAMETERS.json')
    assert bg==packet['result'] and bg['theta']==config['points'][0]['theta']
    assert bg['point_id']==config['points'][0]['id'] and bg['profile']=='reference'
    assert [v['z'] for v in bg['low_z']]==config['redshifts']['low_z_controls']
    assert er['request_id']==rid and er['nonce']==r['nonce'] and er['process']==child['process']
    assert er['solver_calls_attempted']==er['solver_calls_returned']==1
    assert er['background_result_sha256']==sha(case/'BACKGROUND_RESULT.json')
    assert er['configuration_sha256']==packet['identity']['engine_configuration_sha256']==sha(BASE/'EFFECTIVE_CONFIGURATION.json')
    assert er['runtime_sha256']==packet['identity']['runtime_sha256']==sha(BASE/'RUNTIME_INVENTORY.json')
    assert packet['identity']['execution_receipt_sha256']==sha(case/'ENGINE_EXECUTION_RECEIPT.json')
    assert out['identity']['background_packet_sha256']==sha(case/'BACKGROUND_PACKET.json')
    assert out['identity']['admission_sha256']==sha(BASE/'ASSEMBLY_ADMISSION.json')
    assert out['status']=='ENGINEERING_ONLY' and out['certification']['certified'] is False
    assert out['certification']['uniform_error_bound'] is None and out['certification']['numerical_certificate'] is None
    assert all(v is None for v in out['observed_outputs'].values())
    assert len(set(out['row_ids']))==283 and out['nuisance']['dimension']==63
    assert len(out['nuisance']['X_sparse_rows'])==283 and len(out['nuisance']['columns'])==63
    assert out['native_to_output_row_scale'].count(5)==7
    models=out['models'];assert set(models)==set(parameters)
    for k,v in models.items():
        assert v['parameters']==parameters[k] and len(v['mean_without_nuisance'])==283
        assert all(math.isfinite(x) for x in v['mean_without_nuisance'])
    beta=float(read(BASE/'sources/LAYOUT_ESTRUTURAL_3CMB_13BAO.json')['alpha']['decimal_token'])*math.sqrt(math.e)
    assert out['beta_TGL_runtime']==models['H1_TGL']['beta']==beta
    vectors={k:v['mean_without_nuisance'] for k,v in models.items()}
    base=vectors['H2_LCDM']
    for k in vectors:
        assert vectors[k][:3]==base[:3]
        if k!='H5_rd_free':assert vectors[k][3:16]==base[3:16]
    assert vectors['H5_rd_free'][16:]==base[16:]
    for k in ('H1_TGL','H3_beta_free','H4_Cepheid'):
        dh=models[k]['h_local_dex']-models['H2_LCDM']['h_local_dex']
        dc=models[k]['delta_C_mag']
        for i in range(16,283):
            expected=float(Fraction(out['response_columns']['a_h'][i]))*dh+float(Fraction(out['response_columns']['c_C'][i]))*dc
            assert math.isclose(vectors[k][i]-base[i],expected,rel_tol=1e-12,abs_tol=2e-12),(k,i)
    physical=[file_info(p) for p in sorted((BASE/'RUN').rglob('*')) if p.is_file()]
    save_json(target,{'at':datetime.now(timezone.utc).isoformat(),'request_id':rid,'status':'ENGINEERING_PREDICTIONS_VERIFIED_ONCE',
        'repeat_allowed':False,'external_execution':external,'manifest':file_info(BASE/'MANIFESTO_PREPARACAO.json'),
        'preparation_members_checked':checked,'evidence':physical+[file_info(BASE/n) for n in ['RESULT.json','CLAIM.json','AUTORIZACAO_ROOT.json','REVISAO_ROOT.json']],
        'metrics':{'outer_wall_seconds':external['wall_time_seconds'],'prediction_block_seconds':bg['elapsed_solver_seconds'],'peak_worker_rss_KiB_linux':bg['peak_worker_rss_KiB_linux'],'solver_calls_attempted':1,'solver_calls_returned':1,'missing_runtime_probes':len(child['missing_runtime_probes'])},
        'predictions':{'theta':bg['theta'],'E_law':bg['E_law'],'I_law':bg['I_law'],'rstar_Mpc':bg['rstar_Mpc'],'rdrag_Mpc':bg['rdrag_Mpc'],'K_TGL':math.exp(bg['I_law']*beta),'five_models':list(models),'rows':283,'nuisance_columns':63},
        'scope':'One theory-only engineering evaluation. No observed targets, fit, likelihood, Bayes evidence, significance, uniform theory-error certificate or gate change.',
        'verification':'Read/hash and arithmetic consistency of actual outputs; no candidate import, solver, new control or scientific observation in this verifier.'})
    print(json.dumps({'receipt':file_info(target),'metrics':read(target)['metrics'],'predictions':read(target)['predictions']},ensure_ascii=False))

if __name__=='__main__':
    main()
