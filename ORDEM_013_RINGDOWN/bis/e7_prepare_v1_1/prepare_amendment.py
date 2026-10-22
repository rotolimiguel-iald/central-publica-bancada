"""Build T12 candidate only; publication is a separate post-test step."""
from pathlib import Path
from datetime import datetime,timezone
import json, hashlib, sys, copy
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import save,sha
def candidate():
    parent=B/'RINGDOWN_5SIGMA_V1_1.json'
    later=list(B.glob('RINGDOWN_5SIGMA_V1_1_*.json'))
    if later:raise ValueError('Inspect existing amendment before preparing; never duplicate')
    reg=json.loads(parent.read_bytes());reg['parent_registration_sha256']=sha(parent)
    reg['registered_utc']=datetime.now(timezone.utc).isoformat()
    reg['witness_relative_to_Chatgpt']='TUNEL/DO_CHATGPT/ENTREGA_015_E2_REGISTRO_V1_1_1.md'
    reg['e7']['producer_directory']=str((D/'producer').relative_to(ROOT)).replace('\\','/')
    reg['e7']['producer_tree_sha256']={p.name:sha(p) for p in sorted((D/'producer').glob('*.py'))}
    reg['e7']['guard_path']=reg['e7']['producer_directory']+'/tgl_ringdown_ampliacao.py'
    reg['e7']['guard_sha256']=reg['e7']['producer_tree_sha256']['tgl_ringdown_ampliacao.py']
    reg['e7']['guard_pin_status']='EMBEDDED_CALIBRATION_ONLY_READER_NOT_JOB_AUTHORIZATION'
    spec={}
    for key,path in {
        'legacy_registration':B/'RINGDOWN_5SIGMA_V1.json',
        'execution_receipt':B/'bis/E7_FINAL_EXECUTION_V1.json',
        'legacy_authorization':B/'bis/E7_FINAL_AUTHORIZATION_V1.json',
        'qnm_grid':B/'QNM_GRID.json',
        'qnm_coefficients':D/'QNM_CUBIC_COEFFICIENTS.json',
        't05_receipt':B/'bis/015/t05/RESULT.json',
    }.items():
        spec[key+'_path']=path.relative_to(ROOT).as_posix();spec[key+'_sha256']=sha(path)
    spec['posterior_product_name']='POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json'
    aliases=[e for e in reg['calibration_event_ids'] if e.split('_')[0]=='GW250114']
    assert len(aliases)==1
    spec['calibration_aliases']={'GW250114':aliases[0]}
    spec.update(scope='HISTORICAL_CALIBRATION_REPLAY_ONLY',blind_adapter_implemented=False,
        formulas='FOUR_LEGACY_FORMULA_ASTS_UNCHANGED',heavy_job_authorized=False)
    reg['e7_rite_v1_1']=spec
    reg['extra_code_roots'].append(dict(relative_to_Chatgpt=reg['e7']['producer_directory'],
                                    files_sha256=reg['e7']['producer_tree_sha256']))
    reg['t12_amendment_reason']='New portable E7 consumer with witnessed historical provenance and T05 paired QNM diagnostic; no statistical change'
    return reg
if __name__=='__main__':
    save(D/'CANDIDATE_V1_1_1.json',candidate())
    print(sha(D/'CANDIDATE_V1_1_1.json'))
