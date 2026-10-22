"""Load guarded runtime and inspect capability registration; no observed fit."""
from pathlib import Path
import ast, json, sys, time, hashlib, asyncio
BASE=Path(__file__).resolve().parent;ROOT=BASE/'candidate'
sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
start=time.perf_counter()
for p in ROOT.rglob('*.py'):ast.parse(p.read_bytes(),filename=str(p))
from bancada.canonical import require_current
receipt=require_current('candidate_integration')
from bancada.motor import Motor
motor=Motor(str(ROOT))
assert motor.prov_alpha['um_py_sha256']==receipt['um_py_sha256']
assert motor.beta_tgl==receipt['beta_tgl']
from bancada.neutrino_contract import contract,simulate
nu=contract()
s=simulate(dict(channel='boundary_parity_4state',s=0.5,rho=[[[int(i==j==0),0] for j in range(4)] for i in range(4)]))
import mcp_um
async def inspect():
 tools=await mcp_um.mcp.list_tools()
 return [x.name for x in tools]
capabilities=asyncio.run(inspect())
assert {'contratos','neutrino_contrato','neutrino_sintetico'} <= set(capabilities)
result=dict(ok=True,seconds=time.perf_counter()-start,canonical=receipt,engine=dict(device=str(motor.dev),alpha_provenance=motor.prov_alpha,beta=motor.beta_tgl,table_validation=motor.erro_tabela),neutrino_contract_pin=nu['pin'],synthetic=s,tools=capabilities,observed_fit=False)
with (BASE/'CANDIDATE_RUNTIME_R2.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(dict(ok=True,seconds=result['seconds'],canonical=receipt['canonical_version'],tools=len(capabilities),device=str(motor.dev)),ensure_ascii=False))
