"""Consolidation adapters with explicit diffs; never overwrite scientific sources."""
from pathlib import Path
import json,re,difflib
from prepare_part_d import write,save,sha,R
S=R/'FECHAMENTO_PARCIAL';L=S/'lean'
data=json.loads((S/'INVENTORY.json').read_bytes())
audit='''
-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\\t" ++ n.toString ++ "\\t" ++ kind ++ "\\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
'''
rows=[];excluded=[]
for x in data['lean']:
    p=Path(x['path']);rel=Path(x['relative']);name=p.stem
    if not x['valid_receipts']:
        excluded.append(dict(**x,reason='NO_HASH_MATCHED_SUCCESS_RECEIPT; historical failure/control retained at source'));continue
    if rel.parts[0]=='A6_EQUACAO_DA_VERDADE':
        excluded.append(dict(**x,reason='C3/package is later integrated successor; mutations are controls, not production proofs'));continue
    if name=='StressTensorDataLocal':
        excluded.append(dict(**x,reason='Superseded by StressTensorDataLocal_v2'));continue
    src=p.read_text('utf-8-sig'); transformed=src;changes=[]
    if name in ['ContratoQG_v31_Minimal','WindowLemmasVerbatim','WindowCoefficientVerbatim'] or rel.parts[0]=='C1':
        # These reproduce canonical definitions/theorems. Do not redeclare them.
        target='TGLExt.ContratoQG_v31' if name=='ContratoQG_v31_Minimal' else 'TGLExt.ContratoQG_v31_Teoremas'
        transformed='import '+target+'\nimport Lean\n'
        # Explicitly preserve the original queries after their namespace resolution.
        queries=re.findall(r'^#print axioms\s+(\S+)',src,re.M)
        base='TGLExt.ContratoQGv31'
        for q in queries:
            if not q.startswith(('TGLExt.','TGL.')):
                # Resolve against canonical audit report, rejecting ambiguity.
                report=json.loads((S/'kernel_proof_manifest_origin.json').read_bytes())['axiom_report']
                hits=[n for n in report if n==base+'.'+q or n.startswith(base+'.') and n.endswith('.'+q)]
                if len(hits)==1:q=hits[0]
                else:continue
            transformed+='#print axioms '+q+'\n'
        changes.append(dict(kind='CANONICAL_REUSE_ADAPTER',module=target,
            reason='Original declarations collide with v371 declarations; original source archived and collisions listed, no new proof claimed'))
    else:
        if 'screenBlock' in transformed and rel.parts[0]!='D4':
            transformed=re.sub(r'\bscreenBlock\b','screenBlockV31',transformed)
            changes.append(dict(kind='CANONICAL_V371_RENAME',old='screenBlock',new='screenBlockV31'))
        if rel.parts[0]=='C3' and 'TGLExt.EquationOfTruth' in transformed:
            transformed=transformed.replace('TGLExt.EquationOfTruth','ORDEM016.EquationOfTruth')
            changes.append(dict(kind='EXPLICIT_NAMESPACE_SEPARATION',old='TGLExt.EquationOfTruth',new='ORDEM016.EquationOfTruth',
                reason='The strengthened T20 source extends a copy of canonical definitions; no assertion that new definitions are identical to canonical symbols'))
        # Lean is already transitive in Mathlib, but explicit import serves the audit.
        first=re.search(r'^import .*$',transformed,re.M)
        if first:transformed=transformed[:first.start()]+'import Lean\n'+transformed[first.start():]
        else:transformed='import Lean\n'+transformed
    # Audit appended outside all original namespaces.
    transformed+='\n'+audit
    target=L/(name+'.lean')
    assert not target.exists(),target
    write(target,transformed.encode())
    original=S/'original_sources'/rel;write(original,p.read_bytes())
    diff='\n'.join(difflib.unified_diff(src.splitlines(),transformed.splitlines(),fromfile=str(p),tofile=str(target)))+'\n'
    write(S/'diffs'/(name+'.diff'),diff.encode())
    rows.append(dict(original=str(p),original_sha256=sha(p),source=str(target),sha256=sha(target),module=name,
        branch=rel.parts[0],changes=changes,previous_receipts=x['valid_receipts'],
        imports=re.findall(r'^import\s+(\S+)',transformed,re.M)))
names={x['module'] for x in rows};order=[];pending=rows.copy()
while pending:
    ready=[x for x in pending if all(m not in names or m in order for m in x['imports'])]
    assert ready,[(x['module'],x['imports']) for x in pending]
    for x in ready:order.append(x['module']);pending.remove(x)
save(S/'SOURCE_PLAN.json',dict(sources=rows,order=order,excluded=excluded,
    policy='Copies and explicit adapters; no proof bodies edited except declared identifier/namespace alignment. Prior sources retained.'))
print(json.dumps(dict(selected=len(rows),excluded=len(excluded),adapters=sum(bool(x['changes']) for x in rows))))
