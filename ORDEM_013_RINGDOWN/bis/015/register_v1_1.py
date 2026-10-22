"""Witness the checked nonblind design; never start R7, PE or unblinding."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,copy
B=Path(__file__).resolve().parents[2];ROOT=B.parent;D=B/'bis/015/t03';C=B/'bis/e2_code_v1_1';OUT=ROOT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_bytes())
def bytes_new(p,raw):
    tmp=p.with_name(p.name+'.pending');assert not p.exists() and not tmp.exists()
    with tmp.open('xb') as f:f.write(raw);f.flush()
    assert tmp.read_bytes()==raw
    import os
    os.link(tmp,p);tmp.unlink()
def main():
    sys.path.insert(0,str(C));import registration_guard as g
    regpath=B/'RINGDOWN_5SIGMA_V1_1.json';note=OUT/'ENTREGA_015_E2_REGISTRO_V1_1.md';receipt=B/'bis/015/E2_V1_1_REGISTRATION_RECEIPT.json'
    assert not any(p.exists() for p in [regpath,note,receipt,B/'bis/PART_015_BUDGET_START.json'])
    cp=D/'CANDIDATE_V1_1_002.json';r=load(cp);old=load(B/'RINGDOWN_5SIGMA_V1.json')
    assert sha(B/'RINGDOWN_5SIGMA_V1.json')==g.V1_PIN and sha(ROOT/old['witness_relative_to_Chatgpt'])==g.V1_WITNESS_PIN
    g.verify_statistical_identity(old,r)
    assert {p.relative_to(C).as_posix():sha(p) for p in C.rglob('*.py')}==r['own_code_tree_sha256']
    for rt,pins in [(B/'bis/e2_code',old['own_code_tree_sha256'])]+[(ROOT/x['relative_to_Chatgpt'],x['files_sha256']) for x in old['extra_code_roots']]:
        assert {p.relative_to(rt).as_posix():sha(p) for p in rt.rglob('*.py')}==pins
    for name,h in r['input_pins_relative_to_Chatgpt'].items():assert sha(ROOT/name)==h
    proof=ROOT/r['activation_v1_1']['probes_result_relative_to_Chatgpt'];pr=load(proof)
    assert pr['status']=='V1_1_GUARD_PROBES_PASSED' and len(pr['tests'])==150 and all(x['passed'] for x in pr['tests'])
    assert pr['candidate_sha256']==sha(cp) and pr['own_code_tree_sha256']==r['own_code_tree_sha256']
    r5=ROOT/r['activation_v1_1']['qualification_R5_relative_to_Chatgpt'];q=load(r5)
    assert q['status']=='R5_SOURCE_ONLY_QUALIFIED' and q['n_items']>=1000 and q['status_counts']=={'FINITE_WAVEFORM':q['n_items']}
    now=datetime.now(timezone.utc).isoformat();r.update(status='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST',registered_utc=now)
    r['registration_provenance_v1_1'].update(candidate_sha256=sha(cp),registration_script_sha256=sha(Path(__file__)),guard_probes_sha256=sha(proof))
    r['unpaid_before_execution']=[s for s in r['unpaid_before_execution'] if not s.startswith('Final full-code')]
    g.publish_new(regpath,r)
    text=f'''[REAL — desenho NÃO-CEGO registrado; não é posterior, teste da natureza ou autorização de descegamento]

registro_sha256: {sha(regpath)}
registered_utc: {now}

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}

V1.1 ao lado da V1 preservada; subobjeto estatístico idêntico, hashes conferidos. Candidato002: {sha(cp)}. Controles:150, sha256 {sha(proof)}. Qualificação source-only R5: {q['n_items']} retornos finitos, sem EDOM/abort no desenho 4096Hz/8192Hz, sha256 {sha(r5)}. Cobertura finita, não prova para todo o contínuo.

Um piloto só-220 NÃO-CEGO;30 novas células sintéticas registradas, ainda não executadas.30 eventos distintos recebem metadados, sem promoção. Inferência física permanece sem p até calibração E3.3. A cadeia de alocações e o relógio R7 ainda precedem qualquer job pesado. Nenhuma semente lida, nenhum posterior produzido ou descegado. Auditoria da gerência e decisões do operador continuam necessárias para eventos cegos. Nenhum gate alterado.
'''
    bytes_new(note,text.encode())
    marker=dict(status='E2_V1_1_REGISTERED',registration_sha256=sha(regpath),witness_sha256=sha(note),probes_result_sha256=sha(proof),qualification_R5_sha256=sha(r5))
    g.publish_new(receipt,marker)
    # This checks genuine published bytes, not monkeypatched fixtures.
    loaded,digest,loadednote=g.load_registration_chain_v1_1()
    assert digest==sha(regpath);g.check_activation_v1_1(loaded,digest,loadednote)
    try:g.checked_registration()
    except FileNotFoundError as e:
        assert Path(e.filename)==B/'bis/PART_015_BUDGET_START.json',str(e)
        outcome=dict(type=type(e).__name__,message=str(e),expected=True)
    else:raise AssertionError('Unexpected execution authorization before R7')
    result=dict(status='REGISTERED_ACTIVATION_CHECKED_HEAVY_EXECUTION_BLOCKED_BY_MISSING_R7',at=datetime.now(timezone.utc).isoformat(),
        receipt=marker,actual_entry=outcome,real_clock_created=False,heavy_jobs=0,seed_read=False,gate_changed=False)
    g.publish_new(D/'REGISTRATION_DELIVERY.json',result)
    print(json.dumps(result))
if __name__=='__main__':main()
