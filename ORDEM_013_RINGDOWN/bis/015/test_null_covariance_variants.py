"""Compare the 24 new diagnostic projections with the archived DG11 calculation."""
from pathlib import Path
import copy,hashlib,json,sys,time
import numpy as np
B=Path(__file__).resolve().parents[2];C=B/'bis/e2_code_v1_1';D=B/'bis/015/t03/null_covariance_tests_001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    wall=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False);sys.path.insert(0,str(C))
    import null_runner as runner
    reg=json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes())
    reference=B.parent/'TUNEL/PARA_CHATGPT/ORDEM_015_INSUMOS/reproducoes_da_gerencia/DG11/dg11_resultado.json'
    refs=json.loads(reference.read_bytes());rows=[]
    for key,original in reg['nulls']['cells'].items():
        if original['kind']!='matched_projection' or original['model']=='gaussian':continue
        for variant,label in [('zero','V_zero'),('kde_0.7','kde_0.7'),('WLS_q90','WLS_q90')]:
            cell=copy.deepcopy(original);cell['nuisance_covariance_variant']=variant
            comp=runner.projection_inputs(reg,cell);tail=runner.analytic_tail(comp,cell['model'])
            old=refs[key]['variants'][label]
            got=[comp['noise_variance_fraction'],comp['nuisance_variance_fraction'],comp['signal_information_with_nuisance'],tail['p']]
            wanted=[old['a'],old['b'],old['I'],old['p_t5']]
            assert np.allclose(got,wanted,rtol=1e-9,atol=1e-14),(key,variant,got,wanted)
            if variant=='zero':assert comp['nuisance_variance_fraction']==0
            rows.append(dict(original_cell=key,variant=variant,analytic_synthetic_tail=tail,components=comp,reference=old,
                             max_absolute_difference=float(max(abs(a-b) for a,b in zip(got,wanted))),passed=True))
    assert len(rows)==24
    cell=copy.deepcopy(original);cell['nuisance_covariance_variant']='UNREGISTERED'
    # Select an actual matched-projection cell for a targeted variant refusal.
    cell=copy.deepcopy(next(x for x in reg['nulls']['cells'].values() if x['kind']=='matched_projection'));cell['nuisance_covariance_variant']='UNREGISTERED'
    try:runner.projection_inputs(reg,cell)
    except ValueError as e:assert 'covariance variant' in str(e)
    else:raise AssertionError('Unknown covariance accepted')
    result=dict(status='24_COVARIANCE_VARIANTS_MATCH_ARCHIVED_DG11',rows=rows,unknown_variant_refused=True,
        source_sha256=sha(C/'null_runner.py'),reference_sha256=sha(reference),
        input_pins={n:sha(B.parent/n) for n in [reg['nulls']['dataset_relative_to_Chatgpt'],reg['nulls']['nuisance_relative_to_Chatgpt']]},
        draws_generated=0,clock_started=False,heavy_machine_hours=0,physical_p_emitted=False,
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,
        scope='Deterministic synthetic projections and analytic tails only, not phase-P 1e8 simulations or physical null calibration')
    with (D/'RESULT.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ('status','cpu_seconds','wall_seconds','draws_generated','physical_p_emitted')}))
if __name__=='__main__':main()
