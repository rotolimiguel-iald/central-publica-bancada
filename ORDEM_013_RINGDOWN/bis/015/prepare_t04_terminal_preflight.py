"""Version operational wrappers; scientific registration and source stay pinned."""
from pathlib import Path
import sys,json,ast
from datetime import datetime,timezone
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2];OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import save,write,sha

def main():
    old=D/'t04/supervise_t04_v2.py';source=old.read_text()
    source=source.replace("    assert nulls.exists(),'T03 must finish first'", "    sys.path.insert(0,str(D.parent))\n    from t03_terminal_guard import require_terminal\n    terminal=require_terminal(D.parent)")
    source=source.replace("allocated_seconds=cap,script_sha256=sha(Path(__file__)),blind=False)","allocated_seconds=cap,script_sha256=sha(Path(__file__)),blind=False,\n        T03_terminal=terminal,T03_terminal_guard_sha256=sha(D.parent/'t03_terminal_guard.py'))")
    new=D/'t04/supervise_t04_v3.py';ast.parse(source);write(new,source.encode())
    budget_old=D/'prepare_budget_v2.py';source=budget_old.read_text()
    source=source.replace("    measured=D/'nulls_campaign_001/RESULT.json'", "    from t03_terminal_guard import require_terminal\n    terminal=require_terminal(D)\n    measured=D/'nulls_campaign_001/RESULT.json'")
    source=source.replace("pilot_safety='Existing", "T03_terminal=terminal,T03_terminal_guard_sha256=sha(D/'t03_terminal_guard.py'),\n        pilot_safety='Existing")
    budget_new=D/'prepare_budget_v2_checked.py';ast.parse(source);write(budget_new,source.encode())
    for path in (D/'t03_terminal_guard.py',D/'t04/process_lifecycle_fixture.py',D/'deliver_nulls_campaign.py'):
        ast.parse(path.read_text())
    receipt=dict(at=datetime.now(timezone.utc).isoformat(),status='PREPARED_NOT_EXECUTED',
        supersedes={str(new):sha(old),str(budget_new):sha(budget_old)},
        files={str(p):sha(p) for p in (new,budget_new,D/'t03_terminal_guard.py',D/'t04/process_lifecycle_fixture.py')},
        scientific_code_changed=False,gate_changed=False,
        rule='Order015 section3: terminal MEDIDA permits next branch; no fabricated all30success prerequisite')
    save(D/'T04_TERMINAL_PREFLIGHT_PREPARED.json',receipt)
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
