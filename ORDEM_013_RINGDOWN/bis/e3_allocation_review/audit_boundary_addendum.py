"""Additional finite checks: exclusive publication and deferred review chain."""
import importlib.util
import json
import sys
from pathlib import Path
from datetime import datetime,timezone

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fixture_helpers',HERE/'audit_fixtures.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
results=[]


def record(name,call,reject=False):
    error=None
    try:call()
    except Exception as exc:error=type(exc).__name__+': '+str(exc)
    results.append(dict(id=name,passed=(error is not None)==reject,error=error))


def main():
    s=h.setup('addendum_exclusive');mod=h.execute(s)
    dst=s['side']/'candidates/candidate_fake'
    before={p.name:h.sha(p) for p in dst.iterdir()}
    sys.argv=[str(mod.__file__),str(s['side']/'PROPOSAL_FAKE.json')]
    record('candidate_directory_no_replacement',mod.main,True)
    results.append(dict(id='candidate_bytes_unchanged_after_rejection',passed=before=={p.name:h.sha(p) for p in dst.iterdir()}))
    s=h.setup('addendum_five_alternatives_string',lambda s:s['proposal']['decision_documentation'].update(five_alternatives='abcde'))
    record('documentary_limit_string_of_length5_accepted',lambda:h.execute(s))
    s=h.setup('addendum_quality_chain',lambda s:s['cfg'].update(mode='blind_test',event='FAKE_BLIND',
        publication_metadata_review={},data_quality_resolution={}))
    h.execute(s);guard=h.guard_fixture(s)
    dst=s['side']/'candidates/candidate_fake'
    jobs=s['root']/s['proposal']['jobs_relative_to_Chatgpt'];active=s['base']/'ORCAMENTO_40H.json'
    jobs.write_bytes((dst/'JOBS_V2.CANDIDATE.json').read_bytes())
    alloc=json.loads((dst/'ORCAMENTO_40H.CANDIDATE.json').read_bytes())
    witness=s['root']/s['proposal']['witness_relative_to_Chatgpt'];witness.parent.mkdir(parents=True)
    stamp=datetime.now(timezone.utc).isoformat()
    def repin():
        alloc['jobs_sha256']=h.sha(jobs);active.write_text(json.dumps(alloc))
        witness.write_text('allocation_sha256: '+h.sha(active)+'\nregistered_utc: '+stamp+'\n')
    repin();record('frozen_load_jobs_rejects_empty_publication_review',lambda:guard.load_jobs(s['reg'],s['digest']),True)
    evidence=s['base']/'FAKE_REVIEW_ONLY.json';h.write(evidence,{'status':'FAKE_EVIDENCE_NOT_REAL_APPROVAL'})
    extra=json.loads(jobs.read_bytes());cfg=extra['jobs']['fake_new']
    cfg['publication_metadata_review']=dict(review_passed=True,scope='FINITE_FIXTURE',relative_to_Chatgpt=evidence.relative_to(s['root']).as_posix(),
        sha256=h.sha(evidence),reviewed_utc=stamp)
    jobs.write_text(json.dumps(extra));repin()
    record('frozen_load_jobs_rejects_empty_quality_resolution',lambda:guard.load_jobs(s['reg'],s['digest']),True)
    cfg['data_quality_resolution']=dict(cfg['publication_metadata_review'],method='FAKE_FINITE_METHOD')
    cfg['data_quality_resolution'].pop('scope');jobs.write_text(json.dumps(extra));repin()
    record('frozen_load_jobs_accepts_complete_fake_reviews',lambda:guard.load_jobs(s['reg'],s['digest']))
    evidence.write_text('{"status":"FAKE_CHANGED"}')
    record('frozen_load_jobs_rejects_changed_review_evidence',lambda:guard.load_jobs(s['reg'],s['digest']),True)
    h.write(HERE/'BOUNDARY_ADDENDUM_001.json',dict(status='FINITE_METADATA_CHECKS',cases=results,
        total=len(results),passed=sum(r['passed'] for r in results),script_sha256=h.sha(Path(__file__)),
        scope='Only own fake metadata; original guard snapshot unchanged; no actual activation/launch/seeds/science'))
    print(json.dumps(dict(total=len(results),passed=sum(r['passed'] for r in results))))


if __name__=='__main__':main()
