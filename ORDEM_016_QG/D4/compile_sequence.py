"""Run dependent compilations only after checking each isolated compiler receipt."""
from pathlib import Path
import sys,json,subprocess,hashlib
D=Path(__file__).resolve().parent
stages=[('PhotonWitness.lean','witness_01'),('PhotonModularRealization.lean','modular_01'),('PhotonMassiveTransport.lean','transport_01'),('PhotonContract.lean','contract_01'),('PhotonContractTheorems.lean','theorems_01')]
for name,label in stages:
 p=D/name;rp=D/(label+'.json')
 if not rp.exists():
  subprocess.run([sys.executable,'-X','utf8','-B',str(D/'compile_one.py'),name,label],check=True)
 x=json.loads(rp.read_bytes())
 assert x['source_sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
 print(json.dumps(dict(stage=label,rc=x['rc'])),flush=True)
 if x['rc']!=0:raise SystemExit(1)
