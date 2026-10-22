from pathlib import Path
import concurrent.futures,json,subprocess,sys
B=Path(__file__).resolve().parent;P=B.parent

def receipt_final(name,key):return json.loads((P/name).read_bytes())[key]['path']
jobs={
'inclusion':receipt_final('gamma_unbounded/FINAL_TOMITA_INCLUSION_RECEIPT_R1.json','receipt'),
'finite':receipt_final('gamma_unbounded/FINAL_WEYL_FINITE_ALGEBRA_RECEIPT_R1.json','receipt'),
'equality':receipt_final('gamma_unbounded/FINAL_TOMITA_EQUALITY_RECEIPT_R1.json','receipt'),
'duality':str(P/'weyl_net_wiring/attempts/20261015T193303_165516Z/RECEIPT.json'),
'weight':receipt_final('takesaki_fock/FOCK_DUAL_WEIGHT_RECEIPT_R1.json','build'),
 'traced':receipt_final('takesaki_fock/TRACED_CORE_ASSEMBLY_RECEIPT_R1.json','build')}
def branch(names):
 for name in names:
  q=subprocess.run([sys.executable,'-B','-X','utf8',str(B/'compile_review_r1.py'),name,jobs[name]],capture_output=True,text=True,encoding='utf-8')
  print(json.dumps({'name':name,'exit':q.returncode,'stdout':q.stdout,'stderr':q.stderr}),flush=True)
  if q.returncode:return False
 return True
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 results=list(ex.map(branch,[['inclusion','finite','equality'],['duality'],['weight','traced']]))
sys.exit(0 if all(results) else 1)
