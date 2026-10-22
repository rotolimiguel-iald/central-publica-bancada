"""Integration smoke of the real witness/runtime and E7 without science data."""
import sys,json,time
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'bis/e2_code'))
import registration_guard as guard

def main():
    start=time.perf_counter();reg,digest=guard.checked_registration()
    sys.path.insert(0,str(B/'bis/e7_prepare/producer'))
    import tgl_ringdown_ampliacao as e7
    context,_=e7.checked_context(B.parent,B/'RINGDOWN_5SIGMA_V1.json',digest)
    if context!=reg:raise ValueError('E7 integration returned different registration')
    jobs=guard.load_jobs(reg,digest)
    from pe_runner import validate_config
    for cfg in jobs.values():validate_config(cfg)
    checks=[]
    for event,mode in [(reg['calibration_event_ids'][0],'blind_test'),('NOT_REGISTERED','blind_test'),(reg['calibration_event_ids'][0],'unknown')]:
        try:guard.authorize_event(reg,event,mode)
        except ValueError as exc:checks.append({'event':event,'mode':mode,'rejected':True,'reason':str(exc)})
        else:raise AssertionError('Invalid event admitted')
    seed=guard.contained(reg['blinding']['seed_relative_to_Chatgpt'])
    if seed.stat().st_size!=32 or guard.sha(seed)!=reg['blinding']['seed_commitment_sha256']:raise ValueError('Seed commitment differs')
    out=B/'bis/E2_REGISTRATION_SMOKE.json'
    value={'status':'PASS_REAL_REGISTRATION_RUNTIME_WITNESS_AND_E7_CONTEXT_NO_SCIENCE',
      'registration_sha256':digest,'witness_sha256':guard.sha(guard.contained(reg['witness_relative_to_Chatgpt'])),
      'own_code_files':len(reg['own_code_tree_sha256']),
      'extra_code_files':sum(len(x['files_sha256']) for x in reg['extra_code_roots']),
      'registered_inputs':len(reg['input_pins_relative_to_Chatgpt']),'jobs_validated':list(jobs),
      'negative_identity_checks':checks,'seed_commitment_matches':True,'seed_bytes_or_offsets_disclosed':False,
      'new_posterior_or_strain_values_read':False,'PE_MC_waveforms_executed':False,
      'wall_seconds':time.perf_counter()-start,'utc':datetime.now(timezone.utc).isoformat(),
      'script_sha256':guard.sha(Path(__file__))}
    guard.publish_new(out,value);print(json.dumps({'status':value['status'],'sha256':guard.sha(out),'wall_seconds':value['wall_seconds']}))

if __name__=='__main__':main()
