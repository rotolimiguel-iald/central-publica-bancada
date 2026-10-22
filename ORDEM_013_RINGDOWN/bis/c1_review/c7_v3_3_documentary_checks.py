"""Close R4 by final-byte attribution checks; do not rerun science or builders."""
from pathlib import Path
from datetime import datetime,timezone
import ast,copy,hashlib,json,zipfile
B=Path(__file__).resolve().parents[2];P=B/'C7_INDEPENDENT_v3_3';OLD=B/'C7_INDEPENDENT_v3_2'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(p):return json.loads(p.read_bytes())
def put(p,raw):
    need(not p.exists(),'Output exists');tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    need(tmp.read_bytes()==raw and len(raw)>0,'Short write');tmp.rename(p)
m=get(P/'MANIFEST.json');br=get(B/'bis/C7_V3_3_BUILD.json');doc=get(B/'bis/C7_V3_3_DOCUMENTARY_VALIDATION.json')
need(sha(P/'MANIFEST.json')==br['manifest_sha256'],'Manifest receipt')
need(sha(B/br['archive'])==br['archive_sha256']==doc['archive_sha256'],'ZIP receipts')
builder=B/'refeito/build_independent_v3_3_013bis.py'
need(sha(builder)==m['builder_sha256'],'Builder identity')
oldm=get(OLD/'MANIFEST.json');need({r['path'] for r in m['files']}=={r['path'] for r in oldm['files']},'File sets differ')
content={};changed=[]
for r in m['files']:
    p=P/r['path'];need(p.resolve().is_relative_to(P.resolve()) and not p.is_symlink(),'Unsafe path')
    raw=p.read_bytes();need(len(raw)==r['bytes'] and sha(p)==r['sha256'],'Package mismatch')
    content[r['path']]=raw
    if raw!=(OLD/r['path']).read_bytes():changed.append(r['path'])
for r in oldm['files']:need(sha(OLD/r['path'])==r['sha256'],'Old package changed')
need(changed==['provenance/SHIPPED_ATTRIBUTIONS.json']==doc['changed_files'],'Unexpected byte changes')
with zipfile.ZipFile(B/br['archive']) as z:
    names=set(content)|{'MANIFEST.json'};wanted={P.name+'/'+n for n in names}
    need(set(z.namelist())==wanted and len(z.namelist())==len(wanted),'ZIP coverage')
    for n in names:need(z.read(P.name+'/'+n)==(P/n).read_bytes(),'ZIP differs')
attrs=get(P/'provenance/SHIPPED_ATTRIBUTIONS.json');names=[r['path'] for r in attrs['files']]
need(len(names)==len(set(names))==78 and set(names)==set(content)-{'provenance/SHIPPED_ATTRIBUTIONS.json'},'Attribution coverage')
for row in attrs['files']:need(row['sha256']==sha(P/row['path']),'Attribution final bytes')
need(attrs['ledger_sha256']==sha(P/'provenance/DOWNLOAD_LICENSE_LEDGER.json'),'Ledger pin')
need(doc['prior_replay_sha256']==sha(B/doc['prior_replay']),'Prior replay pin')
for n in doc['execution_files_identical']:need(content[n]==(OLD/n).read_bytes(),'Claimed execution identity')
tree=ast.parse(builder.read_text(encoding='utf-8'))
start=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='attributions' for t in n.targets))
end=next(i for i in range(start,len(tree.body)) if isinstance(tree.body[i],ast.For) and ast.unparse(tree.body[i].iter)=='sorted(content.items())')
code=compile(ast.fix_missing_locations(ast.Module(body=tree.body[start:end],type_ignores=[])),'attribution_guard_only','exec',optimize=1)
cases=[]
for case in ['intact','missing_row','duplicate_row','extra_row','bad_hash','stale_final_document']:
    c=copy.deepcopy(content);a=copy.deepcopy(attrs)
    if case=='missing_row':a['files'].pop()
    elif case=='duplicate_row':a['files'].append(copy.deepcopy(a['files'][0]))
    elif case=='extra_row':a['files'].append(dict(path='unknown.txt',sha256='invalid'))
    elif case=='bad_hash':a['files'][0]['sha256']='invalid'
    elif case=='stale_final_document':c['README.md']+=b'\nchanged'
    c['provenance/SHIPPED_ATTRIBUTIONS.json']=json.dumps(a).encode()
    error=None
    try:exec(code,dict(content=c,json=json,hashlib=hashlib))
    except ValueError as e:error=str(e)
    need((error is None)==(case=='intact'),'Guard outcome differs '+case)
    cases.append(dict(case=case,refused=error is not None,error=error))
result=dict(status='C7_R4_CLOSED_DOCUMENTARY_ONLY',utc=datetime.now(timezone.utc).isoformat(),files=79,attribution_hashes_verified=78,
    changed_shipped_files=changed,manifest_itself_also_changed=True,guards_under_O=cases,
    same_execution_bytes_as_v3_2=True,no_science_replay=True,
    prior_replay_reference=doc['prior_replay'],prior_replay_sha256=doc['prior_replay_sha256'],
    documentary_temporary_removal='DECLARADO in source receipt; no temporary path supplied for independent absence check',
    manifest_sha256=sha(P/'MANIFEST.json'),archive_sha256=sha(B/br['archive']),builder_sha256=sha(builder),
    attributions_sha256=sha(P/'provenance/SHIPPED_ATTRIBUTIONS.json'),source_receipt_sha256=sha(B/'bis/C7_V3_3_DOCUMENTARY_VALIDATION.json'),script_sha256=sha(Path(__file__)))
out=B/'bis/c1_review/c7_v3_3_documentary_results.json';put(out,(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode())
paths=['refeito/build_independent_v3_3_013bis.py','C7_INDEPENDENT_v3_3/MANIFEST.json','cache/C7_INDEPENDENT_v3_3.zip','C7_INDEPENDENT_v3_3/provenance/SHIPPED_ATTRIBUTIONS.json','bis/C7_V3_3_DOCUMENTARY_VALIDATION.json','bis/c1_review/c7_v3_3_documentary_checks.py','bis/c1_review/c7_v3_3_documentary_results.json']
hashrows='\n'.join(f'| `{n}` | `{sha(B/n)}` |' for n in paths)
report=f'''[REAL — fechamento documental independente de C7-R4; sem nova execução científica]

# C7 v3_3 — fechamento de R4

Data UTC: {result['utc']}.

**C7-R4 fechado na v3_3.** As 78 atribuições agora cobrem exatamente os arquivos esperados, sem duplicatas, com SHA256 calculado dos bytes finais; README e OVERVIEW conferem. SHIPPED_ATTRIBUTIONS não se auto-hasheia: sua identidade é coberta pelo manifesto externo. C7-R1–R3 permanecem fechados pelo parecer v3_2, com os mesmos bytes executáveis. Este fechamento não quita os achados separados dos wrappers dos suplementos.

Conferi 79/79 arquivos do manifesto por tamanho/hash e todos os membros/bytes do ZIP. Versus v3_2, a única alteração entre os arquivos embarcados listados no manifesto é `provenance/SHIPPED_ATTRIBUTIONS.json`; o próprio MANIFEST também muda, como esperado. Todos os outros 78 arquivos, incluindo executáveis, ciência congelada, evidência e textos, são byte a byte idênticos. A v3_2 permanece íntegra.

O builder conclui os textos antes das atribuições e aplica guardas explícitas antes da escrita do pacote. Controle independente do bloco real por AST sob optimize=1: íntegro passa; ausência, duplicação, linha extra, hash incorreto e README alterado após o hash são recusados (cinco negativas). Não executei o builder nem a C6.

O recibo documental aponta corretamente para o replay v3_2 já conferido, com SHA256 correto e identidade dos arquivos de execução. Isso transporta a evidência daquela execução sobre os mesmos bytes; não é uma execução nova na v3_3. As unidades frescas informadas no recibo são [DECLARADO — registro do construtor]; esta revisão acrescenta verificação independente dos bytes e das guardas documentais. `temporary_removed=true` do controle documental não traz o caminho temporário: sua ausência física não foi reconstatada por este parecer. A remoção dos temporários do replay v3_2 já foi conferida no parecer anterior.

Persistem os estatutos científicos e as limitações dos relatórios anteriores; licença não foi reinterpretada como autorização geral do código, nem PASS numérico como confirmação física. Sem PE/C5/campanhas, memória/canônico ou edição de produção.

Controle: `bis/c1_review/c7_v3_3_documentary_checks.py`; resultados em `c7_v3_3_documentary_results.json`.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
{hashrows}
'''
dest=B/'bis/C7_V3_3_CLOSING_REVIEW.md';put(dest,report.encode())
print(json.dumps(dict(status=result['status'],report=str(dest),report_sha256=sha(dest),attributions=78,negative_controls=5)))
