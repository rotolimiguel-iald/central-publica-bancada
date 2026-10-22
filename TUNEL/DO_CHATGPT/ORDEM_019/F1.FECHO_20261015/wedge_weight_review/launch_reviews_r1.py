from pathlib import Path
import concurrent.futures,json,subprocess,sys
B=Path(__file__).resolve().parent;P=B.parent
items=[('anti',P/'weyl_net_wiring/attempts/20261015T195243_576449Z/RECEIPT.json'),('noniso',P/'weyl_net_wiring/attempts/20261015T195536_203581Z/RECEIPT.json'),('fixed',P/'takesaki_fock/attempts/20261015T194904_396265Z/RECEIPT.json'),('resolvent',P/'takesaki_fock/attempts/20261015T194536_653452Z/RECEIPT.json')]
def run(item):
 name,rp=item
 p=subprocess.run([sys.executable,'-B','-X','utf8',str(B/'compile_review_r1.py'),name,str(rp)],capture_output=True,text=True,encoding='utf-8')
 print(p.stdout,p.stderr,flush=True);return p.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:codes=list(ex.map(run,items))
if any(codes):raise SystemExit(1)
raise SystemExit(run(('faithful',P/'takesaki_fock/attempts/20261015T195046_772592Z/RECEIPT.json')))
