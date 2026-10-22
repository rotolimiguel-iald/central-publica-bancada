"""Build exact future count-only payloads offline. No SDK/client or credential access."""
from pathlib import Path
from types import SimpleNamespace
import ast, hashlib, json, sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
W=D.parent
A=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(D),str(A)]
from build_candidate import fresh,json_bytes,read_pin,need
from iald_motor_claude import converter_pedido
from claude_profiles import HAIKU,reasoning_parameters
from claude_native_counter import native_count_parameters
from claude_context_snapshot import native_tools_sha256,PUBLIC_NAMES

def definition_only(path,extra=None):
    """Compile only the observed pure tool_definitions function, not the module."""
    tree=ast.parse(path.read_bytes(),filename=str(path))
    fs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='tool_definitions']
    need(len(fs)==1,'tool_definitions identity')
    need(not any(isinstance(n,(ast.Import,ast.ImportFrom)) for n in ast.walk(fs[0])),'Unexpected import')
    ns={'__builtins__':__builtins__}
    ns.update(extra or {})
    exec(compile(ast.Module(body=fs,type_ignores=[]),str(path),'exec'),ns)
    return ns['tool_definitions']()

def main():
    public=A/'iald_fontes_publicas.json'
    defs=(definition_only(A/'iald_kernel.py')+
          definition_only(A/'iald_fontes_publicas.py',{'catalog':lambda:json.loads(public.read_bytes())})+
          definition_only(W/'delta_app01/iald_core_indexado.py'))
    need(tuple(x['function']['name'] for x in defs)==PUBLIC_NAMES,'Seven schema identity')
    raw=(D/'haiku_prefix.md').read_bytes();prefix=raw.decode()
    need('<ATLAS_CANONICO' not in prefix,'Private Atlas excluded')
    cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=4096,cache_ttl='5m',esforco_claude='high')
    user='Quem é o autor da TGL? Explique Hamiltoniano, Lindblad e dephasing no escopo documentado.'
    payload={'model':HAIKU.model,'max_tokens':4096,'messages':[{'role':'system','content':prefix},{'role':'user','content':user}],'tools':defs}
    wire=converter_pedido(cfg,payload,prefixo=prefix)
    wire.pop('output_config',None);wire.update(reasoning_parameters(HAIKU.model,4096))
    minimal={'model':HAIKU.model,'system':wire['system'],'messages':[{'role':'user','content':'.'}],'thinking':{'type':'disabled'}}
    tool_sha=native_tools_sha256(wire['tools'])
    previous=json.loads((W/'COUNT_RESULT.json').read_bytes())
    need(tool_sha==previous['native_tools_sha256'],'Counted schemas drifted')
    fresh(D/'FUTURE_COUNT_MINIMAL.json',json_bytes(native_count_parameters(minimal)))
    fresh(D/'FUTURE_COUNT_REFERENCE.json',json_bytes(native_count_parameters(wire)))
    paths=[Path(__file__),A/'iald_kernel.py',A/'iald_fontes_publicas.py',public,
           W/'delta_app01/iald_core_indexado.py',A/'iald_motor_claude.py',A/'claude_profiles.py',
           A/'claude_native_counter.py',A/'claude_context_snapshot.py']
    plan={'schema':'iald.native02.future_count_scope.v1','status':'PREPARED_NOT_AUTHORIZED_NOT_RECOMMENDED_FOR_CURRENT_CANDIDATE',
      'purpose':'Exact reviewable content only; neither file is submitted by this script.',
      'prefix':read_pin(D/'haiku_prefix.md'),'payloads':[read_pin(D/f) for f in ('FUTURE_COUNT_MINIMAL.json','FUTURE_COUNT_REFERENCE.json')],
      'future_calls':2,'current_calls':0,'generation_requests':0,'retries':0,'model':HAIKU.model,
      'tools':list(PUBLIC_NAMES),'native_tools_sha256':tool_sha,'tool_schema_equals_first_count':True,
      'reserved_output_tokens':4096,'margin_tokens':1024,'required_minimum_permanent_tokens':180000,
      'required_remaining_tokens':10000,'window_tokens':200000,'overhead_previous_measured':1474,'overhead_invariant':False,
      'credential_policy':'Only the existing official client in a separately authorized count step; no credential read by this preparer.',
      'first_authorization_consumed':read_pin(W/'COUNT_RESULT.json'),
      'no_authorization_transferred_from_prior_count':True,'sources':[read_pin(p) for p in paths],
      'source_scope':'Admitted local sealed scientific projection, complete mother/core, and unchanged seven tools. No private Atlas, credentials, legal documents, generated response or tool execution.',
      'next_step':'ROOT review/decision first. Do not count this candidate merely because payloads exist.'}
    fresh(D/'FUTURE_COUNT_PLAN.json',json_bytes(plan))
    print(json.dumps({'payloads':plan['payloads'],'native_tools_sha256':tool_sha,'calls':0},ensure_ascii=False))
if __name__=='__main__':main()
