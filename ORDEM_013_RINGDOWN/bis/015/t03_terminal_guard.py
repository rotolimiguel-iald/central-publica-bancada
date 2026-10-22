"""Require a documented terminal T03, not successful science as a new gate."""
from pathlib import Path
import hashlib,json,math

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def owned_null_running(record):
    path=Path('/proc')/str(record['pid'])/'cmdline'
    try:args=path.read_bytes().split(b'\0')
    except FileNotFoundError:return False
    return any(x.endswith(b'/null_runner.py') for x in args) and record['cell'].encode() in args

def require_terminal(directory,running=owned_null_running):
    directory=Path(directory);run=directory/'nulls_campaign_001'
    result_path=run/'RESULT.json';r=json.loads(result_path.read_bytes())
    plan=json.loads((run/'PLAN.json').read_bytes());s=json.loads((run/'SUMMARY.json').read_bytes())
    assert r['plan_sha256']==sha(run/'PLAN.json')
    assert s['campaign_sha256']==sha(result_path)
    assert r['registration_sha256']==s['registration_sha256']==plan['registration_sha256']
    names=[v['cell'] for v in r['finished']]+r['not_started']
    assert len(names)==len(set(names)) and sorted(names)==sorted(plan['cell_ids'])
    assert len(names)==30
    hours=r['machine_hours_union']
    assert not isinstance(hours,bool) and isinstance(hours,(float,int)) and math.isfinite(hours) and 0<=hours<=1
    accepted=sum(v['accepted'] is True for v in r['finished'])
    assert s['completed']==accepted==len(s['rows'])
    complete=accepted==30 and not r['not_started'] and r['fault'] is None
    expected='SYNTHETIC_NULLS_COMPLETED_NOT_PHYSICAL_5SIGMA' if complete else 'T03_MEDIDA_PARTIAL_NO_RETRY'
    assert r['status']==expected
    assert s['status']==('T03_SYNTHETIC_TAILS_MEASURED' if complete else 'T03_MEDIDA_INCOMPLETE_WITH_COST')
    out=directory.parents[2]/'TUNEL/DO_CHATGPT'
    notes=[out/'ENTREGA_015_T03_nulos_1e8.md']
    if not complete:notes.append(out/'ENTREGA_015_MEDIDA_T03_nulos_parciais.md')
    for note in notes:
        text=note.read_text('utf-8')
        assert sha(result_path) in text and sha(run/'SUMMARY.json') in text
    for record in r['finished']:
        assert isinstance(record['returncode'],int) and 'end_utc' in record
        assert not running(record),'An owned null process is still running'
    return dict(status='T03_TERMINAL_DOCUMENTED',science_complete=complete,accepted_cells=accepted,
        remaining_cells=30-accepted,machine_hours=hours,result_sha256=sha(result_path),
        summary_sha256=sha(run/'SUMMARY.json'),cleanup='OWNED_NULL_IDENTITIES_NOT_RUNNING',
        scope='Terminal accounting permits next prescribed branch; incomplete tails remain unpaid')
