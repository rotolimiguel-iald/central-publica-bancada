"""Publish the exact independently accepted byte snapshot and an honest receipt."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, json, hashlib, os, math

B = Path(__file__).resolve().parents[1]
R = B.parent
D = R / 'TUNEL/DO_CHATGPT'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def strict(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('Duplicate JSON key')
            out[key] = value
        return out
    def invalid(value):
        raise ValueError('Invalid JSON number')
    def number(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError('Nonfinite JSON number')
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid, parse_float=number)

def new(path, raw):
    tmp = path.with_name(path.name + '.pending')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if tmp.stat().st_size != len(raw):
        raise OSError('Short write')
    os.link(tmp, path)
    tmp.unlink()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--draft', type=Path, required=True)
    ap.add_argument('--review', type=Path, required=True)
    ap.add_argument('--review-sha256', required=True)
    args = ap.parse_args()
    draft_path, review_path = args.draft.resolve(), args.review.resolve()
    if not all(p.is_relative_to(R) for p in (draft_path, review_path)):
        raise ValueError('Outside work package')
    review_raw, draft_raw = review_path.read_bytes(), draft_path.read_bytes()
    review_pin, draft_pin = digest(review_raw), digest(draft_raw)
    if review_pin != args.review_sha256:
        raise ValueError('Review changed')
    review = strict(review_raw)
    if (review.get('approved') is not True or review.get('draft_sha256') != draft_pin
            or review.get('blocking_findings') != []):
        raise ValueError('Final draft not independently accepted')
    budget_raw = (B / 'bis/PART_B_BUDGET_START.json').read_bytes()
    allocation_raw = (B / 'ORCAMENTO_40H.json').read_bytes()
    budget, allocation = strict(budget_raw), strict(allocation_raw)
    started = datetime.fromisoformat(budget['started_utc'])
    deadline = min(datetime.fromisoformat(budget['hard_deadline_utc']),
                   datetime.fromisoformat(allocation['wall_accounting']['finalization_stop_utc']))
    if datetime.now(timezone.utc) >= deadline:
        raise TimeoutError('Allocated cap expired')
    destination = D / 'ENTREGA_013BIS_RELATORIO_FINAL.md'
    receipt = B / 'bis/FINAL_DELIVERY_RECEIPT.json'
    if any(p.exists() or p.with_name(p.name + '.pending').exists() for p in (destination, receipt)):
        raise FileExistsError('Preserve final delivery')
    opening_pin = digest((D / 'ENTREGA_013BIS_ABERTURA_operador.md').read_bytes())
    new(destination, draft_raw)
    actual_pin = digest(destination.read_bytes())
    stamp = datetime.now(timezone.utc)
    elapsed = (stamp - started).total_seconds() / 3600
    failure = ('DELIVERY_BYTES_DIFFER' if actual_pin != draft_pin else
               'COMPLETION_OUTSIDE_ALLOCATED_CAP' if stamp >= deadline or elapsed >= 40 else None)
    result = dict(status='ORDER_013BIS_DELIVERED_RESULTS_AND_MEASURED_WALLS' if failure is None
                  else 'FINAL_DELIVERY_FAILED_VISIBLE', failure=failure, created_utc=stamp.isoformat(),
        report=dict(path=destination.relative_to(R).as_posix(), sha256=actual_pin, bytes=len(draft_raw)),
        independent_review=dict(path=review_path.relative_to(R).as_posix(), sha256=review_pin),
        original_draft=dict(path=draft_path.relative_to(R).as_posix(), sha256=draft_pin),
        opening_sha256=opening_pin, elapsed_continuous_PartB_wall_hours=elapsed,
        remaining_of_40_hours=40-elapsed, hard_deadline_utc=budget['hard_deadline_utc'],
        allocation_sha256=digest(allocation_raw), physical_5sigma_paid=False,
        new_blind_PE_completed=0, calibration_new_injections_completed=0,
        nature_test_status='AWAITING_DATA_WITH_SYSTEMATICS_GATE_RED',
        acceptance_scope='Bancada report closure; external management audit and operator ratification remain external actions',
        timing_scope='Completion timestamp is after report copy/hash and before receipt serialization',
        script_sha256=digest(Path(__file__).read_bytes()))
    new(receipt, (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode())
    print(json.dumps(dict(report=str(destination), sha256=actual_pin, receipt_sha256=digest(receipt.read_bytes()),
                         hours=elapsed, failure=failure), ensure_ascii=False))
    if failure:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
