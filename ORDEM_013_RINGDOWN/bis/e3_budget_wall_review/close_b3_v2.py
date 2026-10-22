"""Focused static closing; exercise only isolated JSON parser with in-memory bytes."""
import ast
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):
 raw=x if isinstance(x,bytes) else (x.encode() if isinstance(x,str) else (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())

def main():
 source=B/'refeito/deliver_b3_wall_v2_013bis.py';raw=source.read_bytes();text=raw.decode('utf-8');tree=ast.parse(text)
 snapshot=HERE/'snapshot_v2/deliver_b3_wall_v2_013bis.py';put(snapshot,raw)
 checks=[]
 def ck(n,x):
  checks.append({'name':n,'passed':bool(x)})
  if not x:raise ValueError(n)
 fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main')
 first_write=min(x.lineno for x in ast.walk(fn) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='new')
 guards={
 'budget receipt hash':'Allocation mismatch', 'approved review pin':'Allocation review mismatch',
 'three candidate bindings':'Candidate binding differs','activation status and parent':'Allocation activation/parent differs',
 'review and parent binding':'Activation review binding differs','witness pin':'Witness differs',
 'machine witness hash':'Machine witness missing','machine witness time':'Witness chronology differs',
 'reserve':'Reserve expired','zero counts':'Not a wall allocation','empty jobs and pin':'Jobs changed',
 'approved manifest pin':'Candidate sources changed','all manifest files':'Frozen candidate dependency changed',
 'Kerr review frozen pin':'Independent Kerr review changed','Kerr comparison reviewed pin':'Kerr comparison lacks matching review',
 'all three destinations plus pending':'Preserve prior delivery'}
 loc={}
 for name,message in guards.items():
  nodes=[x for x in ast.walk(fn) if isinstance(x,ast.Constant) and x.value==message]
  ck(name+' before first write',len(nodes)==1 and nodes[0].lineno<first_write);loc[name]=nodes[0].lineno
 # Execute only the extracted load function; replace Path with an in-memory byte holder.
 loadfn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='load')
 module=ast.fix_missing_locations(ast.Module(body=[loadfn],type_ignores=[]))
 class Buffer:
  def __init__(self,value):self.value=value
  def read_bytes(self):return self.value
 env={'Path':lambda p:p,'json':json,'math':math}
 exec(compile(module,'<isolated_B3_v2_JSON_parser>','exec'),env)
 ck('strict JSON valid',env['load'](Buffer(b'{"x":1.25,"a":[1,2]}'))=={'x':1.25,'a':[1,2]})
 for label,value in [('duplicate',b'{"x":1,"x":2}'),('nested duplicate',b'{"a":{"x":1,"x":2}}'),
                     ('NaN',b'{"x":NaN}'),('Infinity',b'{"x":Infinity}'),('negative Infinity',b'{"x":-Infinity}'),
                     ('overflow',b'{"x":1e999}')]:
  try:env['load'](Buffer(value))
  except ValueError:ck('strict JSON rejects '+label,True)
  else:raise ValueError('Bad JSON accepted '+label)
 for label,s in [('detector mass frame','Mf está em massas solares no referencial do detector; af é adimensional.'),
                 ('normalized difference wording','A diferença de medianas dividida pela largura em quadratura'),
                 ('review scope','posteriores completos e metadados/pins no escopo do parecer'),
                 ('Welch cost','Kerr_Welch_separate_diagnostic'),('abbreviated commands','não comandos completos de replay')]:ck(label,s in text)
 folder=B/'bis/e3_budget_wall';manifest=json.loads((folder/'MANIFEST.json').read_bytes())
 for row in manifest['files']:ck('candidate manifest '+row['relative_path'],sha(folder/row['relative_path'])==row['sha256'])
 frozen=json.loads((folder/'FROZEN_INPUTS.json').read_bytes());pins={r['source_relative_to_Chatgpt']:r['sha256'] for r in frozen['files']}
 krpath=B/'bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json'
 ck('actual Kerr review matches frozen',sha(krpath)==pins[krpath.relative_to(B.parent).as_posix()])
 kr=json.loads(krpath.read_bytes());comp=B/'cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json'
 match=[v for k,v in kr['input_hashes'].items() if k.endswith('/cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json')]
 ck('actual comparison reviewed',match==[sha(comp)] and kr['blocking_findings']==[])
 ck('old source preserved',sha(B/'refeito/deliver_b3_wall_013bis.py')==sha(HERE/'snapshot/refeito/deliver_b3_wall_013bis.py'))
 ck('new source stable',sha(source)==hashlib.sha256(raw).hexdigest())
 report={'status':'B3_V2_FOCUSED_SOURCE_REVIEW_CLOSED_NO_BLOCKING_FINDINGS_IN_SCOPE',
         'created_utc':datetime.now(timezone.utc).isoformat(),'source':str(source),'source_sha256':sha(source),
         'first_write_line':first_write,'preflight_guard_lines':loc,'check_count':len(checks),'checks':checks,
         'closed_findings':['B3-R2 for reviewed candidate/activation flow','B3-N1','B3-N2','B3-N3','B3-N4'],
         'blocking_findings':[],
         'dependency':'B3-R1 activation-witness correction/review belongs to B/main; this closing neither reviews nor executes the new activator. Delivery refuses missing/mismatched machine fields.',
         'execution_scope':'Only exact extracted load() function against in-memory mock bytes. No delivery main, module import, production file writes, activation, waveform, strain or posterior payload.',
         'limitations':['Future active budget/receipt/witness not certified here; preflight runs only at authorized delivery.',
             'Budget-to-candidate scientific content preservation relies on independently reviewed activator; delivery verifies hash bindings, not deep equality of every inherited field.',
             'Publication is exclusive per file, not an all-or-none transaction. Late missing ancillary reference or concurrent mutation can leave fiche published before final report. No success is claimed if failure occurs; preserve remnants and diagnose.',
             'Files are reread for hashes/formatting; concurrent writers are outside this focused frozen-artifact review. No general race-free filesystem guarantee.'],
         'evidence_pins':{'candidate_manifest':sha(folder/'MANIFEST.json'),'Kerr_review':sha(krpath),'Kerr_COMPARISON':sha(comp),
                          'previous_review':sha(HERE/'REVIEW.json')}}
 put(HERE/'B3_V2_CLOSING_REVIEW.json',report)
 put(HERE/'B3_V2_CLOSING_REVIEW.md',f'''# Fechamento focal B3 v2

**Sem bloqueadores no recorte revisado. B3-R2 e notas N1–N4 fechados para estes bytes.** Fonte `refeito/deliver_b3_wall_v2_013bis.py`, SHA256 `{sha(source)}`.

{len(checks)} controles passaram:16 guardas antes da primeira escrita (linha{first_write}), parser JSON estrito com seis recusas em memória, correções editoriais, manifesto completo do candidato, revisão Kerr congelada e COMPARISON vinculado ao pin revisado. Original B3 preservado. Sem executar main/importar o módulo de entrega, sem ativação ou ciência.

A cadeia conferida é aprovação→candidato/manifesto→fontes congeladas→revisão Kerr→COMPARISON. Ativação confere status, parent, candidato, review, witness/hash/campos de máquina; jobs vazios e reserva são exigidos antes da ficha. Massa no frame do detector, razão descritiva, escopo dos posteriores, Welch separado e comandos abreviados foram corrigidos.

R1 é dependência do ativador v2 sob revisão de B, não reaberta nem aprovada aqui. Este parecer aceita o código da entrega para a cadeia de ativação revisada; não certifica artefatos ativos futuros. O ativador é responsável por preservar os campos herdados do candidato.

Limites operacionais: escrita exclusiva por arquivo, sem transação de três saídas; referência auxiliar ausente ao final ou concorrência pode deixar ficha parcial. Isso não constitui entrega completa nem autoriza sobrescrever. Não se atribui garantia geral contra corrida de arquivos. Nenhum bloqueador adicional observado no cenário de fontes congeladas apresentado.

Arquivos novos: `close_b3_v2.py`, `snapshot_v2/deliver_b3_wall_v2_013bis.py`, `B3_V2_CLOSING_REVIEW.json`, este parecer e `MANIFEST_V2_CLOSING.json`. Recibos anteriores intactos.
''')
 names=['close_b3_v2.py','snapshot_v2/deliver_b3_wall_v2_013bis.py','B3_V2_CLOSING_REVIEW.json','B3_V2_CLOSING_REVIEW.md']
 put(HERE/'MANIFEST_V2_CLOSING.json',{'files':[dict(path=n,sha256=sha(HERE/n),bytes=(HERE/n).stat().st_size) for n in names],
     'self':'MANIFEST_V2_CLOSING.json; self hash omitted'})
 print(json.dumps({'status':report['status'],'checks':len(checks),'source_sha256':sha(source),'receipt_sha256':sha(HERE/'B3_V2_CLOSING_REVIEW.json')}))

if __name__=='__main__':main()
