from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[2]
SRC=B.parent/'TUNEL/PARA_CHATGPT/ORDEM_015_INSUMOS/reproducoes_da_gerencia'
D=B/'refeito/015'
groups={'dg14':['probe.py','probe2.py'],'DG02':['dg02_nyquist.py'],
        'E3_piloto_orcamento_cegos':['run_repro.py','grid_stage.py','fine_stage.py','replay_stage.py','wf_case.py']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
items=[]
for group,names in groups.items():
    dest=D/group;dest.mkdir(parents=True,exist_ok=False)
    for name in names:
        p=SRC/group/name;q=dest/name
        with q.open('xb') as f:f.write(p.read_bytes())
        assert sha(p)==sha(q)
        items.append({'source':str(p),'copy':str(q),'sha256':sha(q)})
(D/'dg14/out').mkdir()
p=D/'SOURCE_COPY_MANIFEST.json'
with p.open('xb') as f:f.write((json.dumps({'copied_only_code':True,'no_management_results_copied':True,'files':items},indent=2)+'\n').encode())
print(json.dumps({'copies':len(items),'manifest':str(p)}))
