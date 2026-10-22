"""Minimal counterexamples to the proposed bookkeeping validators; no adoption."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,importlib.util,json,sys,time,dataclasses
H=Path(__file__).resolve().parent;O=H/'mimo_contact_bookkeeping_audit';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
    if not isinstance(b,bytes):b=json.dumps(b,ensure_ascii=False,indent=2).encode()
    assert not p.exists(),p;t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
src=H/'received_reviews/fb3587cd-5807-4dab-9aa0-3ac178bc4deb.md'
body=src.read_text('utf-8');parts=body.split('```python\n');assert len(parts)==2
code=parts[1].split('```',1)[0];tree=ast.parse(code)
imports=[node.module for node in ast.walk(tree) if isinstance(node,ast.ImportFrom)]
assert not any(isinstance(node,ast.Import) for node in ast.walk(tree))
assert set(imports)<= {'__future__','dataclasses','enum','typing'}
new(O/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(src),
    targets=['tampered trace coefficient without supplied mutation flag','arbitrary derivative formula',
    'vanishing double pole','missing arity factor','empty Ward ledger','flagged Ward ledger',
    'same-key metadata overwrite','additive cutoff terms incorrectly grouped'],
    scope='Execute only the reviewed pure Python proposal, no filesystem/network/provider capability',
    adoption=False))
copy=O/'PROPOSTA_MIMO_ORIGINAL.py';new(copy,code.encode())
spec=importlib.util.spec_from_file_location('mimo_contact_proposal_audit_only',copy)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m
start=time.process_time();spec.loader.exec_module(m)
L=m.build_contact_table();findings=[]
def record(name,observed,expected,assertion):
    assert assertion,(name,observed)
    findings.append(dict(name=name,observed=observed,required_behavior=expected))
bad=dataclasses.replace(L.terms['CT-03'],contact_coeff='999',formula='R_munu=999 eta_munu delta')
got=m.check_trace_rmunu(bad)
record('trace_checker_ignores_term',dataclasses.asdict(got),'Reject or evaluate the modified coefficient',got.ok)
got=m.check_derivative_defect('1','2','arbitrary_nonformula')
record('derivative_checker_accepts_unknown_formula',dataclasses.asdict(got),'Reject unsupported expression',got.ok)
got=m.check_derivative_defect('0','2','2*(c_-1-c_-2)')
record('simple_pole_case_always_rejected',dataclasses.asdict(got),'Allow a verified simple-pole case; API has no certificate input',not got.ok)
got=m.check_eom_inside_T(True,True,1,1,'0')
record('arity_factor_not_checked',dataclasses.asdict(got),'Verify the required n factor',got.ok)
empty=m.Ledger();got=m.ward_coefficient_gate(empty)
record('empty_ledger_emits',got,'No coefficient emission without coverage and calculated value',got=='WARD_COEFFICIENT_EMITTED')
empty.flags.append('KEY_COLLISION:bad');got=m.ward_coefficient_gate(empty)
record('gate_ignores_error_flags',got,'Block on unresolved errors',got=='WARD_COEFFICIENT_EMITTED')
one=m.Ledger();old=L.terms['CT-03'];one.register(old)
altered=dataclasses.replace(old,contact_coeff='999')
one.register(altered)
record('metadata_overwrite_without_collision',dict(flags=one.flags,coefficient=one.terms[old.key].contact_coeff),
       'Check all relevant payload fields for immutable registration',not one.flags and one.terms[old.key].contact_coeff=='999')
record('additive_cutoff_terms_flagged_as_duplicate',L.flags,
       'CT11 and CT12 are different summands of the same variational derivative, not alternate expressions of one term',
       'UNRESOLVED_DOUBLE_COUNT_RISK:G_DVCHI' in L.flags)
# The claimed free/linear cutoff term includes a nonlinear denominator.
import sympy as s
u,dchi_du=s.symbols('u dchi_du')
wrong=dchi_du/(1+u);linear=dchi_du
assert s.simplify(wrong-linear)==-u*dchi_du/(1+u)
record('CT10_mislabels_nonlinear_remainder',str(s.simplify(wrong-linear)),
       'Only grad(chi).grad(u) belongs to the quadratic/free subtraction; -u/(1+u) is the interacting remainder',True)
result=dict(status='PROPOSED_VALIDATOR_NOT_ADOPTED',counterexamples=len(findings),findings=findings,
    cpu_seconds=time.process_time()-start,
    source_formulas='The existing R_n and tensor formulas were not changed',
    policy='No new production gate, no wrapper around existing kernel, no original edits',
    physical_claim='No Ward coefficient calculated by metadata')
new(O/'results.json',result)
new(O/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
 [Path(__file__),src,copy,O/'PRE_REGISTER.json',O/'results.json']]))
print(json.dumps(result,ensure_ascii=False))
