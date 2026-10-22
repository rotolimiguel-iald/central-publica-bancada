"""Copy the independently accepted report bytes into the tunnel; no science."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, json, hashlib, os
B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def new(p,raw):
    tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Short write')
    os.link(tmp,p);tmp.unlink()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--draft',type=Path,required=True)
    ap.add_argument('--review',type=Path,required=True);ap.add_argument('--review-sha256',required=True);a=ap.parse_args()
    if not all(p.resolve().is_relative_to(R) for p in (a.draft,a.review)):raise ValueError('Outside work package')
    if sha(a.review)!=a.review_sha256:raise ValueError('Review changed')
    review=json.loads(a.review.read_bytes())
    if review.get('approved') is not True or review.get('draft_sha256')!=sha(a.draft) or review.get('blocking_findings')!=[]:
        raise ValueError('Final draft not independently accepted')
    budget=json.loads((B/'bis/PART_B_BUDGET_START.json').read_bytes())
    allocation=json.loads((B/'ORCAMENTO_40H.json').read_bytes())
    now=datetime.now(timezone.utc);elapsed=(now-datetime.fromisoformat(budget['started_utc'])).total_seconds()/3600
    if now>=datetime.fromisoformat(allocation['wall_accounting']['finalization_stop_utc']) or elapsed>=40:raise TimeoutError('Allocated cap expired')
    destination=D/'ENTREGA_013BIS_RELATORIO_FINAL.md';receipt=B/'bis/FINAL_DELIVERY_RECEIPT.json'
    if any(p.exists() or p.with_name(p.name+'.pending').exists() for p in (destination,receipt)):raise FileExistsError('Preserve final delivery')
    raw=a.draft.read_bytes();new(destination,raw)
    if sha(destination)!=review['draft_sha256']:raise ValueError('Delivery bytes differ')
    stamp=datetime.now(timezone.utc);elapsed=(stamp-datetime.fromisoformat(budget['started_utc'])).total_seconds()/3600
    result=dict(status='ORDER_013BIS_DELIVERED_RESULTS_AND_MEASURED_WALLS',created_utc=stamp.isoformat(),
        report=dict(path=destination.relative_to(R).as_posix(),sha256=sha(destination),bytes=destination.stat().st_size),
        independent_review=dict(path=a.review.relative_to(R).as_posix(),sha256=sha(a.review)),
        original_draft=dict(path=a.draft.relative_to(R).as_posix(),sha256=sha(a.draft)),
        opening_sha256=sha(D/'ENTREGA_013BIS_ABERTURA_operador.md'),
        elapsed_continuous_PartB_wall_hours=elapsed,remaining_of_40_hours=40-elapsed,
        hard_deadline_utc=budget['hard_deadline_utc'],allocation_sha256=sha(B/'ORCAMENTO_40H.json'),
        physical_5sigma_paid=False,new_blind_PE_completed=0,calibration_new_injections_completed=0,
        nature_test_status='AWAITING_DATA_WITH_SYSTEMATICS_GATE_RED',
        acceptance_scope='Bancada report closure; external management audit and operator ratification remain external actions',
        script_sha256=sha(Path(__file__)))
    new(receipt,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(dict(report=str(destination),sha256=sha(destination),receipt_sha256=sha(receipt),hours=elapsed),ensure_ascii=False))
if __name__=='__main__':main()
