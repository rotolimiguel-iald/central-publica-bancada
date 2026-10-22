"""Publish the checked T12 design, preserving all prior registration bytes."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,ast,hashlib
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import write,save,sha
def main():
    regfile=B/'RINGDOWN_5SIGMA_V1_1_1.json';note=OUT/'ENTREGA_015_E2_REGISTRO_V1_1_1.md'
    assert not regfile.exists() and not note.exists()
    cp=D/'CANDIDATE_V1_1_1_v3.json';reg=json.loads(cp.read_bytes());old=json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes())
    # Historical trees are read, never changed by T12.
    preserved=[]
    for root,pins in [(B/'bis/e2_code',old['own_code_tree_sha256'])]+[(ROOT/v['relative_to_Chatgpt'],v['files_sha256']) for v in old['extra_code_roots']]:
        actual={p.relative_to(root).as_posix():sha(p) for p in root.rglob('*.py')}
        assert actual==pins,str(root);preserved.append(dict(path=str(root),files=len(actual)))
    assert reg['parent_registration_sha256']==sha(B/'RINGDOWN_5SIGMA_V1_1.json')
    assert reg['e7']['producer_tree_sha256']=={p.name:sha(p) for p in (D/'producer').glob('*.py')}
    inherited=json.loads(sorted(D.glob('legacy_*.json'))[-1].read_bytes());new=json.loads(sorted(D.glob('rite_*.json'))[-1].read_bytes())
    assert inherited['returncode']==new['returncode']==0
    assert inherited['parsed_summary']['tests']==53 and inherited['parsed_summary']['skipped']==0
    assert new['parsed_summary']['success'] is True
    for log in (inherited,new):assert sha(Path(log['log']))==log['log_sha256']
    src=B/'bis/e7_prepare/producer/tgl_ringdown_ampliacao.py';target=D/'producer/tgl_ringdown_ampliacao.py'
    trees=[ast.parse(p.read_text('utf-8-sig')) for p in (src,target)];formulas={}
    for name in ['conditional_projection','prediction_draws','reading_diagnostics','fullsample_diagnostics']:
        nodes=[[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name] for tree in trees]
        assert all(len(v)==1 for v in nodes)
        text=[ast.dump(v[0],include_attributes=False) for v in nodes];assert text[0]==text[1]
        formulas[name]=hashlib.sha256(text[0].encode()).hexdigest()
    reg['registered_utc']=datetime.now(timezone.utc).isoformat()
    reg['t12_local_validation']=dict(candidate_sha256=sha(cp),legacy_log_sha256=inherited['log_sha256'],
        rite_log_sha256=new['log_sha256'],formula_ast_sha256=formulas,
        gate_changed=False,heavy_job_authorized=False)
    save(regfile,reg)
    text=f'''[REAL — subemenda de leitura NÃO-CEGA; nenhum teste físico nem descegamento]

registro_sha256: {sha(regfile)}
registered_utc: {reg['registered_utc']}

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}

V1.1.1 acrescenta a árvore E7 rito e vincula a reprodução histórica V1 sem alterar sua proveniência.
Subobjeto estatístico preservado; quatro ASTs numéricos idênticos. Controles:53 herdados e {new['parsed_summary']['tests']-new['parsed_summary']['skipped']} da variante; {new['parsed_summary']['skipped']} aposentado do carregador externo.
O consumidor não autoriza job pesado, extração nova ou leitura cega. Alvos condicionais não são poder físico calibrado; AWAITING_DATA, gate red e sigma físico null.
O recibo operacional de ativação da V1.1 base fica preservado. A ativação dos jobs sob este novo elo ainda depende do encadeamento desse recibo; não está certificada por esta testemunha.
'''
    write(note,text.encode())
    prior=B/'bis/015/E2_V1_1_REGISTRATION_RECEIPT.json';receipt=json.loads(prior.read_bytes())
    receipt.update(registration_sha256=sha(regfile),witness_sha256=sha(note),
        supersedes=str(prior.relative_to(ROOT)),supersedes_sha256=sha(prior),
        scope='VERSIONED_SUCCESSOR_NOT_INSTALLED_AS_FIXED_ACTIVATION_MARKER')
    save(D/'E2_V1_1_1_REGISTRATION_RECEIPT.json',receipt)
    save(D/'AMENDMENT_DELIVERY.json',dict(status='WITNESSED_T12_READER_AMENDMENT',at=reg['registered_utc'],
        registration_path=str(regfile),registration_sha256=sha(regfile),witness_path=str(note),witness_sha256=sha(note),
        formula_ast_sha256=formulas,preserved_V1_trees=preserved,activation_status='FIXED_BASE_RECEIPT_PENDING_RECONCILIATION',
        heavy_job_authorized=False,gate_changed=False))
    print(json.dumps(dict(registration_sha256=sha(regfile),witness_sha256=sha(note))))
if __name__=='__main__':main()
