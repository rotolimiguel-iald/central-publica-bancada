"""Cheap self-check from archived dataset; not distinct-agent scientific approval."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import time
from scalar_functions import scalar_calibration

OUT=Path(__file__).resolve().parent
B=OUT.parents[1]
R=B.parent
A=R/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    started=time.perf_counter()
    inputs={}
    def read(p):
        raw=p.read_bytes();inputs[str(p.relative_to(R))]=hashlib.sha256(raw).hexdigest();return json.loads(raw)
    d=read(OUT/'DATASET.json');c=read(OUT/'E0_CORE.json');cost=read(OUT/'COST_RECEIPT.json')
    for name,pin in cost['outputs'].items():
        p=OUT/name
        if sha(p)!=pin['sha256'] or p.stat().st_size!=pin['bytes']:raise ValueError('Output receipt mismatch '+name)
    idx={r['product_id']:r for r in d['rows']};checks=0;opens=0
    for pop,ids in d['sets'].items():
        rows=[idx[k] for k in ids]
        for mode in ['std_ddof1','sigma_q90']:
            for rd in rows[0]['predictions']:
                expected=c['combinations'][pop][mode][rd]
                if rows[0]['predictions'][rd]['delta_tau'] is None:
                    if expected['z_comb'] is not None:raise ValueError('OPEN treated as zero/result')
                    opens+=1;continue
                actual=scalar_calibration([r['stats']['dtau'][mode] for r in rows],
                    [r['predictions'][rd]['delta_tau'] for r in rows],[r['median_dtau'] for r in rows])
                for key,value in actual.items():
                    other=expected[key]
                    if value is None or other is None:
                        if value is not other:raise ValueError('Null mismatch '+key)
                    elif not math.isclose(value,other,rel_tol=3e-12,abs_tol=1e-290):
                        raise ValueError('Scalar mismatch '+str((pop,mode,rd,key,value,other)))
                checks+=1
    summ=read(A/'A_poder_eventos/samples_summary.json')
    diffs=[]
    for row in summ['rows']:
        key=('GWTC5' if row['catalog']=='GWTC5.0' else 'GWTC3')+':'+row['event']
        r=idx[key]
        diffs.append(max(abs(r['stdtau']-row['dtau220']['std']),abs(r['stddf']-row['df220']['std'])))
    manager=read(A/'A_poder_eventos/A_poder_eventos.json')
    oldnames={'GWTC5_31':'sel31_GWTC5','GWTC5_33':'all33_GWTC5','UNION39':'union39_GWTC5+GWTC3only','GWTC3_18':'GWTC3_18','GWTC3_10':'GWTC3_10_published'}
    comparison=[]
    for name,old in oldnames.items():
        for rd in ['R-B','R-MOD','R-RAIZ-0','R-LIN']:
            new=c['combinations'][name]['std_ddof1'][rd]['z_comb'];previous=manager['combined_sigma_std'][old][rd]['z_matched']
            comparison.append({'population':name,'reading':rd,'z_new':new,'z_manager_A':previous,'difference':new-previous,
                'explanation':'GWTC3 own v4HM products instead of current products on overlaps' if name.startswith('GWTC3') else
                    'same std and point predictions; older-only six use component median prediction rather than archived median-of-draw predictions' if name=='UNION39' else 'same population and convention'})
    revision=read(R/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/revisao_da_gerencia/estatistica_poder/REFEITOS_REVISAO.json')
    r=c['combinations']['GWTC5_31'];revision_difference={
        'R_B_z_std':r['std_ddof1']['R-B']['z_comb'],'R_B_z_q90_control':r['sigma_q90']['R-B']['z_comb'],
        'R_B_z_revision':revision['catalogo31_gauss']['R-B']['z_comb_offset0'],
        'GR_false_N_std':r['std_ddof1']['GR_FALSE_FALSIFIER']['N_spurious50_median'],
        'GR_false_N_q90':r['sigma_q90']['GR_FALSE_FALSIFIER']['N_spurious50_median'],
        'GR_false_N_revision':revision['N_5sigma_contra_RG_se_vies_persistir'],
        'explanation':'ddof1 vs Gaussian-equivalent q90; control uses exact norm quantile vs 1.645; prediction at component medians vs median of predicted draws'}
    mc=read(B/'bis/E0_ROUTE_IV_POWER_v2.json')
    errors=[]
    for row in mc['per_event']:
        r=idx['GWTC5:'+row['event']]
        if row['sha256']!=r['source_sha256']:raise ValueError('MC dataset source mismatch')
        errors.extend([abs(row['sigma_df']-r['stddf']),abs(row['sigma_tau']-r['stdtau'])])
    out={'status':'PASS_LIGHT_SCALAR_SELF_CHECK_NOT_DISTINCT_AGENT_APPROVAL','utc':datetime.now(timezone.utc).isoformat(),
        'checks':checks,'explicit_OPEN_cells':opens,'algorithm':'stdlib math.fsum and NormalDist, no producer combined() import, no HDF5 reread',
        'manager_summary_39_max_abs_std_difference':max(diffs),'operator_MC_33_max_abs_sigma_difference':max(errors),
        'operator_MC_comparison_scope':'Widths/pins only; no claim to redo Monte Carlo',
        'manager_A_comparison':comparison,'revision_convention_difference':revision_difference,
        'wall_seconds':time.perf_counter()-started,'source_sha256':inputs,
        'code_sha256':sha(Path(__file__)),'scalar_functions_sha256':sha(OUT/'scalar_functions.py')}
    with (OUT/'SCALAR_VALIDATION.json').open('xb') as f:f.write((json.dumps(out,indent=2)+'\n').encode())
    print(json.dumps({k:out[k] for k in ['status','checks','explicit_OPEN_cells','manager_summary_39_max_abs_std_difference','operator_MC_33_max_abs_sigma_difference','wall_seconds']}))


if __name__=='__main__':main()
