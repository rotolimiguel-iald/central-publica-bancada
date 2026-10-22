from pathlib import Path
import datetime, hashlib, json, re
B=Path(__file__).resolve().parent
P=B.parent
def pin(p):
 p=Path(p);raw=p.read_bytes()
 return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def put(p,s):
 raw=(json.dumps(s,ensure_ascii=False,indent=2)+'\n').encode('utf-8') if isinstance(s,dict) else s.encode('utf-8')
 with p.open('xb') as f:f.write(raw)
 assert p.read_bytes()==raw
verified={}
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x:
   p=pin(x['path']);assert p['sha256']==x['sha256'],x['path']
   if 'bytes' in x:assert p['bytes']==x['bytes']
   verified[p['path']]=p
  for y in x.values():verify(y)
 elif isinstance(x,list):
  for y in x:verify(y)
bp=P/'gamma_unbounded/FINAL_WEYL_GRAPH_CORE_RECEIPT_R1.json';builder=read(bp);verify(builder)
builds=[];counts={'explicit_declarations':0,'theorems_including_private':0}
for name,row in zip(['polarization','closure','core'],builder['modules']):
 rp=B/name/'RECEIPT_R1.json';r=read(rp);verify(r)
 assert r['passed'] and r['exit_code']==0 and r['source_exact_copy']
 assert r['source']['sha256']==row['source']['sha256']
 text=Path(r['source']['path']).read_text(encoding='utf-8')
 counts['explicit_declarations']+=len(re.findall(r'^(?:(?:private|noncomputable) )?(?:theorem|def|abbrev) ',text,re.M))
 counts['theorems_including_private']+=len(re.findall(r'^(?:private )?theorem ',text,re.M))
 builds.append({'module':Path(r['source']['path']).stem,'receipt':pin(rp),'start_utc':r['start_utc'],'end_utc':r['end_utc'],'seconds':r['seconds'],'exit_code':r['exit_code'],'axiom_prints':r['axiom_count'],'source':r['source'],'olean':r['olean'],'olean_identical':r['olean_identical_to_accepted'],'log':r['log']})
ap=B/'all_local/RECEIPT_R1.json';audit=read(ap);verify(audit)
assert audit['passed'] and audit['exit_code']==0
assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in audit['axioms'].values())
assert any('mem_closed_of_functionals' in n for n in audit['axioms'])
assert any('functional_pair' in n for n in audit['axioms'])
counts['all_local_declarations_including_private']=audit['all_decl_count']
counts['selected_axiom_prints']=sum(b['axiom_prints'] for b in builds)
out={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'codex-atrator-skeptic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'PASSA_COM_ESCOPO_CORE_CONJUNTO_DO_LIFT','material_findings':[], 'builder_receipt':pin(bp),'builds':builds,'all_local_audit':pin(ap),'counts':counts,
 'findings':[
  {'id':'G1','status':'REAL','result':'PASSA','claim':'A polarização é simultânea nas duas coordenadas: séries escalares somadas e unicidade dos coeficientes; a continuação analítica atua em polinômios setoriais. A é aditiva e homogênea real, sem continuidade ou linearidade complexa assumida.','anchor':'PairedExponentialPolarizationR3.lean:24-109'},
  {'id':'G2','status':'REAL','result':'PASSA','claim':'A pertença ao fecho é deduzida de todos os funcionais contínuos anuladores, pelo dual separante do quociente normado por submódulo fechado. Cada funcional em F×F é decomposto em dois funcionais de F e representado por Riesz. Não há hipótese de densidade do próprio grafo como premissa.','anchor':'PairedExponentialClosureR4.lean:13-64'},
  {'id':'G3','status':'REAL','result':'PASSA','claim':'TW|K=J|K é derivado da condição fixa de SW e da involutividade de J; a decomposição dom(TW)=K+iK vem da involução SW. A complexificação fornece TW(h+ik)=Jh+iJk, corretamente distinta de J(h+ik)=Jh-iJk.','anchor':'WeylExponentialGraphCoreR4.lean:21-61'},
  {'id':'G4','status':'REAL','result':'PASSA','claim':'Os pares (e(ik),e(iJk)), k∈KWR, geram por span complexo um subespaço cujo fecho é closedGraph TW, o grafo fechado do canonicalLift. As duas inclusões são provadas. A continuação no raio complexo é usada para recuperar os pares reais a partir dos imaginários.','anchor':'WeylExponentialGraphCoreR4.lean:68-111'},
  {'id':'G5','status':'REAL','result':'PASSA','claim':'weyl_graph_core_sequence produz sequência no span dos pares de Weyl convergindo a (x,canonicalLift x) em F×F. É aproximação de entrada e imagem; não apenas totalidade dos primeiros vetores.','anchor':'WeylExponentialGraphCoreR4.lean:113-123'},
  {'id':'G6','status':'DERIVED','result':'ESCOPO','claim':'O core não é vazio: k=0 fornece (Omega,Omega), com Omega de norma 1 pela construção exponencial já auditada. Esta observação reutiliza o resultado anterior, sem novo ensaio de não vacuidade.'},
  {'id':'G7','status':'OPEN','result':'ESCOPO','claim':'Os pares são coordenadas do grafo complexo do lift. O grafo antilinear de Sexp requer transportar a segunda coordenada por Gamma(J). A igualdade Sexp=S_par, a maximalidade pertinente, os fatores polares e KMS não são demonstrados por estes três módulos.'}
 ],'method':'Cópias exatas das três fontes; recompilações sequenciais com dependências previamente auditadas somente lidas. Checker separado por module index sobre env.constants.toList inclui auxiliares privados; não recompilou os módulos positivos/Tomita anteriores.',
 'related_review':pin(P/'gamma_review/REVISAO_GAMMA_R1.json'),'verified_pins':list(verified.values()),'script':pin(__file__),
 'boundaries':{'canonical_sources_written':False,'memory_written':False,'production_written':False,'providers_called':False,'observed_data_opened':False,'gate_changed':False,'administrative_audited_or_closed_claimed':False}}
put(B/'REVISAO_GRAPH_CORE_R1.json',out)
rows='\n'.join(f"| {x['module']} | {x['seconds']:.3f} | {x['exit_code']} | {x['axiom_prints']} | {x['olean_identical']} |" for x in builds)
md=f"""# Revisão independente — core conjunto dos exponenciais de Weyl

**PASSA COM ESCOPO**, sem achado material. Ato técnico; AUDITADA/FECHADA continua com a gerência.

| Módulo | segundos | exit | prints de axiomas | .olean idêntico |
|---|---:|---:|---:|---|
{rows}

[REAL] {counts['explicit_declarations']} declarações explícitas e {counts['theorems_including_private']} teoremas, incluindo os dois privados do fecho. O checker independente verificou {audit['all_decl_count']} declarações, com auxiliares privados, em {audit['seconds']:.3f} s e EXIT 0: somente propext, Classical.choice e Quot.sound, zero sorry/axioma local. Recibos guardam comando, início, fim, tempo, toolchain e LEAN_PATH literal.

[REAL] A polarização controla a soma de dois produtos internos e preserva o par inteiro. Hahn–Banach é aplicado ao quociente pelo submódulo fechado de F×F, com representação separada dos dois funcionais por Riesz. A prova não substitui densidade de grafo por densidade na primeira coordenada.

[REAL] A decomposição do domínio e TW|K=J|K dão TW(h+ik)=Jh+iJk. O sinal é o da extensão linear TW, não o da ação antilinear J no vetor h+ik. Os spans complexos dos pares reais e dos pares de Weyl têm o mesmo fecho do grafo do canonicalLift. A sequência final aproxima simultaneamente x e canonicalLift(x).

[DERIVED] k=0 dá o par não nulo (Omega,Omega), reutilizando a norma 1 do vácuo já auditada.

[OPEN] Estes pares são o core do lift complexo; transportar a segunda coordenada por Gamma(J) é a passagem ao candidato antilinear. Não se provou aqui Sexp=S_par, maximalidade, identificação polar ou KMS. Nenhum original, memória, produção, dado observado ou gate foi alterado.

Hashes, âncoras, declarações e recibos: REVISAO_GRAPH_CORE_R1.json.
"""
put(B/'REVISAO_GRAPH_CORE_R1.md',md)
print(json.dumps({'json':pin(B/'REVISAO_GRAPH_CORE_R1.json'),'md':pin(B/'REVISAO_GRAPH_CORE_R1.md'),'counts':counts,'builds':[{k:x[k] for k in ['module','seconds','olean_identical']} for x in builds],'audit_seconds':audit['seconds']},ensure_ascii=False))
