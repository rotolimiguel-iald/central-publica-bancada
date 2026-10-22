"""Freeze the already requested 400-draw adapter check, without native execution."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,ast
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent; B=D.parents[1]; ROOT=B.parent
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import save,write,sha
def main():
    target=D/'t04';target.mkdir(exist_ok=False)
    p=B/'RINGDOWN_5SIGMA_V1_1_2.json';reg=json.loads(p.read_bytes());cfg=reg['pe_jobs']['GW250114_PILOT_V2_S220']
    assert cfg['generation_maximum_frequency_hz']==4096 and cfg['generation_sample_rate_hz']==8192
    original=D/'t03/R5/c04_originals/draws400.json';rows=json.loads(original.read_bytes())['draws'];assert len(rows)==400
    keys=('mass_1','mass_2','chi_1','chi_2','luminosity_distance','theta_jn','phase','geocent_time','dtau220','dtau440','domega220','domega440')
    items=[]
    for r in rows:
        values={k:r['parameters'][k] for k in keys};values.update(cfg['fixed_deformation_parameters'])
        items.append(dict(label='C04_s220_draw_'+str(r['draw']),parameters=values,origin='C04_DRAW_400_WITH_REGISTERED_440_FIXED_GR'))
    save(target/'QUALIFICATION_JOB.json',dict(config=cfg,items=items))
    old=D/'r5_child.py';raw=old.read_bytes();new=raw.replace(b"bis/e2_code_v1_1'",b"bis/e2_code_v1_1_2'")
    assert new!=raw;ast.parse(new)
    write(target/'qualification_child.py',new)
    save(target/'QUALIFICATION_PLAN.json',dict(at=datetime.now(timezone.utc).isoformat(),
        registration_sha256=sha(p),source_input_sha256=sha(original),job_sha256=sha(target/'QUALIFICATION_JOB.json'),
        inherited_child_sha256=sha(old),child_sha256=sha(target/'qualification_child.py'),
        item_count=400,scope='T04 mandatory replication; same C04 draws with registered fixed440 and generation4096',
        native_execution=False,source_unchanged_from_R5=True,blind_data=False,heavy_machine_hours=0))
    cp=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    state.update(at=datetime.now(timezone.utc).isoformat(),next='T03_NULLS_RUNNING_THEN_T04',next_action='T03_NULLS_RUNNING_THEN_T04',
        active_process=dict(exec_session_id=64813,script=str(D/'run_nulls_registered_v1.py'),
                            result=str(D/'nulls_campaign_001/RESULT.json'),max_machine_hours=1,do_not_restart=True),
        R7_clock=str(B/'bis/PART_015_BUDGET_START.json'),T04_qualification_prepared=str(target/'QUALIFICATION_PLAN.json'))
    save(cp,state,True)
    print(json.dumps(dict(status='T04_PREPARED_NOT_EXECUTED',draws=400,job_sha256=sha(target/'QUALIFICATION_JOB.json'))))
if __name__=='__main__':main()
