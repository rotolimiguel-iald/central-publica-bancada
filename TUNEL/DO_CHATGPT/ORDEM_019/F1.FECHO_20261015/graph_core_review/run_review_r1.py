from pathlib import Path
import json,subprocess,sys
B=Path(__file__).resolve().parent
r=json.loads((B.parent/'gamma_unbounded/FINAL_WEYL_GRAPH_CORE_RECEIPT_R1.json').read_text(encoding='utf-8'))
for name,row in zip(['polarization','closure','core'],r['modules']):
 subprocess.run([sys.executable,'-B','-X','utf8',str(B/'compile_review_r1.py'),name,row['receipt']['path']],check=True)
subprocess.run([sys.executable,'-B','-X','utf8',str(B/'audit_all_local_r1.py')],check=True)
