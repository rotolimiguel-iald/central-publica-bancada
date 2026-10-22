"""Verify the materialized KH candidate against the reviewed generator, no execution."""
from pathlib import Path
import ast,datetime,hashlib,json,time
B=Path(__file__).resolve().parent;P=B.parent
def pin(p):
 p=Path(p);r=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(r).hexdigest(),'bytes':len(r)}
def read(p):return json.loads(Path(p).read_bytes())
def put(p,v):
 r=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode() if isinstance(v,dict) else v.encode()
 with p.open('xb') as f:f.write(r)
 assert p.read_bytes()==r
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
receipt=P/'CANDIDATE_R4_KH_RECEIPT_R1.json';r=read(receipt)
src=Path(r['source']);dst=Path(r['destination'])
assert pin(src)['sha256']==r['source_sha256'] and pin(dst)['sha256']==r['destination_sha256']
builder=P/'full_rite/build_kh_n1_patch_r3.py';contract=P/'full_rite/kh_patch_tests_r3/KH_N1_V394_PREAUDIT_CONTRACT_R3.json'
review_kh=P/'kh_patch_review/REVISAO_KH_PATCH_R3.json';review_net=B/'REVISAO_CANDIDATA_R4_R1.json'
k=read(review_kh);n=read(review_net)
assert k['verdict']=='PASSA_COM_ESCOPO_PREAUDITORIA_PINADA' and n['verdict']=='PASSA_CANDIDATA_R4_COMPONENTES'
assert pin(builder) in k['sources'] and pin(src) in n['sources']
pins=[pin(p) for p in [receipt,src,dst,builder,contract,review_kh,review_net]]
ns={'__name__':'independent_review_no_main','__file__':str(builder)}
exec(compile(builder.read_bytes(),str(builder),'exec'),ns)
expected,detail=ns['compose'](src.read_bytes().decode('utf-8'),read(contract),contract,contract.read_bytes())
assert expected.encode()==dst.read_bytes(),'Materialized bytes differ from reviewed composition'
a=ast.parse(src.read_bytes());b=ast.parse(dst.read_bytes())
allowed={'_V393_SPECS','_V393_FONTES','_V393_NOMES_REGISTROS'}
def rest(t):return [ast.dump(n,include_attributes=False) for n in t.body if not(isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id in allowed for x in n.targets))]
assert rest(a)==rest(b)
assert ns['literal'](a,'_EMBEDDED_KERNEL_FILES')[1]==ns['literal'](b,'_EMBEDDED_KERNEL_FILES')[1]
assert ns['literal'](a,'_V394_NETWORK_CONTRACT')[1]==ns['literal'](b,'_V394_NETWORK_CONTRACT')[1]
for p in pins:assert pin(p['path'])==p
out={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'codex-atrator-skeptic','start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-t,
 'verdict':'PASSA_CANDIDATA_R4_KH_PREPARACAO_RITO','material_findings':[],'materialized_bytes_exactly_reproduced':True,'changed_ast_assignments_only':sorted(allowed),'all_functions_unchanged_from_r4':True,'embedded_and_network_contract_unchanged':True,'sources':pins,'script':pin(__file__),
 'scope':'Recomposição independente em memória do candidato efetivo, byte a byte, com contrato validado contra pré-auditoria real. Herda a revisão de R4 e do KH-N1 R3. Nenhum main/import um.py, rito integral, dado ou produção executado; o resultado integral permanece a medir.','no_gate_change':True,'review_harness_erratum':'R1 comparou após read_text normalizar CRLF da baseline; a tentativa não escreveu parecer. R2 conserva bytes por read_bytes().decode(), como o gerador, e preserva R1.'}
put(B/'REVISAO_CANDIDATA_R4_KH_R1.json',out)
put(B/'REVISAO_CANDIDATA_R4_KH_R1.md','# Revisão da candidata R4 + KH-N1\n\n**PASSA para preparação do rito no escopo autorizado.**\n\n[REAL] A recomposição independente reproduz exatamente todos os bytes da candidata materializada. Apenas `_V393_SPECS`, `_V393_FONTES` e `_V393_NOMES_REGISTROS` mudam frente à R4 revista; funções, fontes Lean e contrato da rede ficam idênticos.\n\nHerda as revisões `REVISAO_CANDIDATA_R4_R1.json` e `REVISAO_KH_PATCH_R3.json`. Não executou main nem o rito integral; esse resultado continua por medir. Nenhum gate muda. Pins em REVISAO_CANDIDATA_R4_KH_R1.json.\n')
print(json.dumps({'review':pin(B/'REVISAO_CANDIDATA_R4_KH_R1.json'),'md':pin(B/'REVISAO_CANDIDATA_R4_KH_R1.md'),'verdict':out['verdict']},ensure_ascii=False))
