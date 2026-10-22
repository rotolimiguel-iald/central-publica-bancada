from pathlib import Path
import hashlib,json
P=Path(__file__).parent
R=Path(r'C:\IALD\Central de Patentes\work\rite394_20261015\r2')
core=json.loads((R/'um_absoluto.json').read_bytes())['core']
review=json.loads((P/'FULL_RITE_OUTPUT_REVIEW_R1.json').read_bytes())
def skim(v,d=0):
    if isinstance(v,str):return v if len(v)<900 else v[:900]+'…'
    if isinstance(v,dict):
        if d>=4:return {'keys':list(v)[:30]}
        return {k:skim(x,d+1) for k,x in v.items() if k not in {'axiom_report','row_checks','grid','table','samples'}}
    if isinstance(v,list):
        if len(v)>15:return {'length':len(v),'first':skim(v[:3],d+1),'last':skim(v[-2:],d+1)}
        return [skim(x,d+1) for x in v]
    return v
rows={}
for k in review['historical_verdict_changes_to_reconcile']:
    r=core[k];checks=r.get('checks',[])
    if isinstance(checks,dict):failed={a:b for a,b in checks.items() if b is False or isinstance(b,dict) and b.get('ok') is False}
    else:failed=[x for x in checks if isinstance(x,list) and len(x)>1 and x[-1] is False or isinstance(x,dict) and x.get('ok') is False]
    rows[k]={'failed_checks':failed,'record':skim(r)}
dest=P/'RITE_DELTAS_DETAILS_R1.json'
with dest.open('x',encoding='utf-8') as f:json.dump(rows,f,ensure_ascii=False,indent=2);f.write('\n')
focus=['void_floor_protocol','void_density_power','void_density_opening','void_density_v41','nivel2_rite','stokes_contour','kh_n1_cobertura_v393']
print(json.dumps({k:rows[k] for k in focus},ensure_ascii=False))
print(json.dumps({'receipt':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}))
