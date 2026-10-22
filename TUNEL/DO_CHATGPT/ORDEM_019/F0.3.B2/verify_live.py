"""Verify updated HTTP and a fresh stdio MCP process, using synthetic input only."""
from pathlib import Path
import asyncio, json, sys, time, urllib.request, hashlib
BASE=Path(__file__).resolve().parent
BENCH=Path(r'C:/IALD/Bancada_Um')
def http(path,body=None):
 data=None if body is None else json.dumps(body).encode()
 req=urllib.request.Request('http://127.0.0.1:18777'+path,data=data,headers={'Content-Type':'application/json','X-Cliente':'B2-live-verification'})
 with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read())
start=time.monotonic();state=None
while time.monotonic()-start<240:
 try:
  state=http('/api/estado')
  if state.get('erro'):raise RuntimeError(state['erro'])
  if state.get('pronta'):break
 except urllib.error.URLError:pass
 time.sleep(2)
assert state and state.get('pronta'),state
expected=hashlib.sha256((BENCH/'canonical_contracts.json').read_bytes()).hexdigest()
assert state['canone']['canonical_manifest_sha256']==expected
assert state['motor']['fontes']['alpha']['um_py_sha256']==state['canone']['um_py_sha256']
request=dict(channel='boundary_parity_4state',s=0.5,rho=[[[int(i==j==0),0] for j in range(4)] for i in range(4)])
http_result=http('/api/neutrino/sintetico',request)
contract=http('/api/neutrino/contrato')
refusals={}
for name,body in [('unknown_neutrino_parameter',dict(request,beta=0.1)),('nan',dict(request,s=float('nan'))),('wrong_type',dict(request,s=True))]:
 try:http('/api/neutrino/sintetico',body);raise AssertionError('accepted '+name)
 except urllib.error.HTTPError as exc:refusals[name]=dict(status=exc.code,response=json.loads(exc.read()))
async def fresh_mcp():
 from mcp import ClientSession, StdioServerParameters
 from mcp.client.stdio import stdio_client
 params=StdioServerParameters(command=sys.executable,args=['-B','-X','utf8',str(BENCH/'mcp_um.py')])
 async with stdio_client(params) as (read,write):
  async with ClientSession(read,write) as session:
   await session.initialize()
   listing=await session.list_tools()
   names=[t.name for t in listing.tools]
   assert {'contratos','neutrino_contrato','neutrino_sintetico'} <= set(names)
   r=await session.call_tool('neutrino_sintetico',{'payload':request})
   assert not r.isError
   payload=r.structuredContent
   if payload is None:
    payload=json.loads(next(t.text for t in r.content if hasattr(t,'text')))
   assert payload['canonical']['canonical_manifest_sha256']==expected
   assert payload['synthetic'] is True
   return dict(tools=names,result=payload)
mcp=asyncio.run(fresh_mcp())
record=dict(ok=True,seconds=time.monotonic()-start,state=state,http_synthetic=http_result,contract_pin=contract['pin'],refusals=refusals,mcp=mcp,observed_fit=False)
with (BASE/'LIVE_VERIFICATION_R1.json').open('x',encoding='utf-8') as f:json.dump(record,f,ensure_ascii=False,indent=2)
print(json.dumps(dict(ok=True,version=state['canone']['canonical_version'],manifest=expected,tools=len(mcp['tools']),refusals=len(refusals),seconds=record['seconds'])))
