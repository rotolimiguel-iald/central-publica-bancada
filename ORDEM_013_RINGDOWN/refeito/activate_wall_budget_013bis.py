"""Register a reviewed zero-new-PE budget; no execution or runtime change."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os

B=Path(__file__).resolve().parents[1]
R=B.parent
D=R/'TUNEL/DO_CHATGPT'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def new(p,value):
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode() if not isinstance(value,str) else value.encode()
    if len(raw)>25*1024*1024:raise ValueError('Document exceeds size limit')
    tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Short write')
    os.link(tmp,p);tmp.unlink()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--review',type=Path,required=True)
    ap.add_argument('--review-sha256',required=True);a=ap.parse_args()
    candidate=B/'bis/e3_budget_wall/ORCAMENTO_40H_CANDIDATE.json'
    if sha(a.review)!=a.review_sha256:raise ValueError('Review pin mismatch')
    review=json.loads(a.review.read_bytes())
    if review.get('approved') is not True or review.get('candidate_sha256')!=sha(candidate):
        raise ValueError('Candidate not independently approved')
    doc=json.loads(candidate.read_bytes());reg=B/'RINGDOWN_5SIGMA_V1.json'
    if doc['parent_registration_sha256']!=sha(reg):raise ValueError('Registration mismatch')
    if any(doc['allocation'][key]!=0 for key in ('new_PE_count','new_injection_count','new_download_count','new_science_wall_seconds','pipeline_repair_seconds')):
        raise ValueError('This authorizer only closes the measured instrument wall')
    now=datetime.now(timezone.utc)
    if now>=datetime.fromisoformat(doc['wall_accounting']['finalization_stop_utc']):raise TimeoutError('Reserve expired')
    if sha(R/doc['jobs_relative_to_Chatgpt'])!=doc['jobs_sha256']:raise ValueError('Jobs metadata changed')
    witness=D/'ENTREGA_013BIS_E3_ORCAMENTO_PAREDE_V1.md'
    output=B/'ORCAMENTO_40H.json';receipt=B/'bis/E3_WALL_BUDGET_ACTIVATION_V1.json'
    if any(p.exists() for p in (witness,output,receipt)):raise FileExistsError('Preserve prior activation')
    doc.update(schema_version='E3_BUDGET_WALL_REGISTERED_V1',status='REGISTERED_ZERO_NEW_PE_MEASURED_INSTRUMENT_WALL',
        registered_utc=now.isoformat(),witness_relative_to_Chatgpt=witness.relative_to(R).as_posix(),
        candidate_sha256=sha(candidate),independent_review={'path':a.review.relative_to(R).as_posix(),'sha256':sha(a.review)},
        authorizer_sha256=sha(Path(__file__)),
        runtime_effect='Documentary allocation only. Does not erase static E2 jobs or modify the guard. No static pilot rerun authorized.')
    new(output,doc)
    new(witness,'[REAL — E3.2 registrado após revisão; nenhuma nova PE/injeção/download alocada]\n\n'
        f'Orçamento `{output.relative_to(R).as_posix()}` — SHA256 `{sha(output)}`. Registro E2 `{sha(reg)}`. '
        f'Candidato `{sha(candidate)}`; revisão independente `{sha(a.review)}`.\n\n'
        f'Registro UTC {now.isoformat()}; prazo final de integração {doc["wall_accounting"]["finalization_stop_utc"]}. '
        'A falha técnica foi medida; custo por posterior convergido continua OPEN. Nenhuma impossibilidade física foi inferida. '
        'As cinco alternativas e os pesos esperados estão no orçamento, com seus estatutos.\n\n'
        f'Abertura `{sha(D/"ENTREGA_013BIS_ABERTURA_operador.md")}`. N/A — sem Lean. '
        'A ordem segue para os registros de parede E3.3/TEST, quadro E6, módulo E7 e relatório final.\n')
    new(receipt,dict(status='E3_2_WALL_ALLOCATION_REGISTERED',authorized_utc=now.isoformat(),
        started_utc=now.isoformat(),finished_utc=datetime.now(timezone.utc).isoformat(),
        budget_sha256=sha(output),candidate_sha256=sha(candidate),review_sha256=sha(a.review),
        witness_sha256=sha(witness),registration_sha256=sha(reg),new_PE_jobs=0,new_injections=0,
        new_downloads=0,physical_calibration_paid=False))
    print(json.dumps(dict(status='REGISTERED_ZERO_NEW_PE_MEASURED_INSTRUMENT_WALL',budget_sha256=sha(output),receipt_sha256=sha(receipt))))

if __name__=='__main__':main()
