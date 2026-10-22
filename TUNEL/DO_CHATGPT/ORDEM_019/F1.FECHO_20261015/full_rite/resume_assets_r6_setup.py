"""Preserve the restricted preparation failure and prepare a scoped resume."""
from pathlib import Path
import ast, datetime, hashlib, json
HERE = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\Central de Patentes\work\rite394_20261015\r3")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
source=HERE/'prepare_assets_r5.py'
text=source.read_text(encoding='utf-8').replace('_R5','_R6').replace('target.name + ".copying"','target.name + ".copying_r6"')
ast.parse(text)
with (HERE/'prepare_assets_r6.py').open('x',encoding='utf-8',newline='\n') as f: f.write(text)
launcher=HERE/'launch_full_rite_r3.py'
text=launcher.read_text(encoding='utf-8').replace('PREPARATION_RECEIPT_R5','PREPARATION_RECEIPT_R6')
ast.parse(text)
with (HERE/'launch_full_rite_r3a.py').open('x',encoding='utf-8',newline='\n') as f: f.write(text)
record={'status':'FAILED_PREPARATION_ONLY_NO_RITE_STARTED',
 'observed_terminal_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'exit_code':1,'source':str(source),'source_sha256':sha(source),
 'failure':r"PermissionError [WinError 5] during mkdir inside r3\cache\lensing\planck\COM_Lensing_4096_R3.00\MV",
 'partial_bytes_retained':True,'candidate_not_executed':True,
 'retry':'prepare_assets_r6.py --resume exact r3; verify existing file bytes, never overwrite, scoped elevated filesystem copying',
 'no_link_no_network_no_source_mutation':True}
with (HERE/'PREPARATION_R5_REFUSAL.json').open('x',encoding='utf-8') as f: json.dump(record,f,ensure_ascii=False,indent=2)
print(json.dumps({'created':3,'retry':str(HERE/'prepare_assets_r6.py')}))
