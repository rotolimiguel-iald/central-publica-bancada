"""Verify the real MCP entry point in a new process; status only."""
from pathlib import Path
import asyncio,json,os,sys
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923');W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True;sys.path.insert(0,str(B))
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from iald_orchestrator.safe_files import save_json,utc_now
from iald_orchestrator import canonical_memory as cm,nos_packet
p=json.loads((W/'PREPARATION_V391.json').read_bytes())
async def main():
 transport=PythonStdioTransport(B/'mcp_server.py',python_cmd=sys.executable,cwd=str(B),env={'PYTHONDONTWRITEBYTECODE':'1'})
 async with Client(transport) as client:
  response=await client.call_tool('iald_orchestration_status',{},timeout=40)
  j=response.data
  if not isinstance(j,dict):
   j=json.loads(next(x.text for x in response.content if x.type=='text'))
  status=j['canonical_memory']
  assert status['generation']==p['generation'] and status['epoch']==p['epoch']
  assert status['resolution']=='ACTIVE_POINTER_PER_REQUEST'
  assert status['freshness']=='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED'
 packet=nos_packet.build('F0.3',max_chars=9000)
 assert packet['receipt']['canonical_memory']['generation']==p['generation']
 save_json(W/'JEV_NOS_PACKET_V391.json',packet)
 save_json(W/'MCP_FRESH_PROCESS.json',{'status':'PASS','at':utc_now(),'client_pid':os.getpid(),
 'server_entry':str(B/'mcp_server.py'),'server_entry_sha256':cm.digest((B/'mcp_server.py').read_bytes()),
 'operation':'iald_orchestration_status','memory':status,'nos_packet_receipt':packet['receipt'],'provider_calls':0,
 'legacy_clients_reconnected':False,'server_closed_after_read_only_verification':True})
 print(json.dumps({'status':'PASS','memory':status,'nos_packet_generation':packet['receipt']['canonical_memory']['generation'],'provider_calls':0}))
asyncio.run(main())

