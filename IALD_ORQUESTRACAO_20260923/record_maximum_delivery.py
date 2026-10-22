from pathlib import Path
import json,hashlib
from iald_orchestrator.safe_files import replace_bytes,save_json,utc_now
BASE=Path(__file__).resolve().parent
note=(BASE/'work/maximum_delivery_note.md').read_text(encoding='utf-8')
marker=b'IALD_MAXIMUM_KIMI_MIMO_AND_PROVIDER_LOCK_20260924'
previous=json.loads((BASE/'validation/shared_memory_delivery.json').read_bytes())
paths=[Path(x['path']) for x in previous['surfaces']]+[BASE/'TRANSPORTE_DESASSISTIDO.md',BASE/'COORDINATOR.md']
records=[]
for path in paths:
 old=path.read_bytes()
 text=note if path.name!='MEMORY.md' else '\n\n<!-- IALD_MAXIMUM_KIMI_MIMO_AND_PROVIDER_LOCK_20260924 -->\n- Kimi K3 MAX e MiMo máximo, sem tetos locais; memória TGL ampliada, executor obrigatório por unidade. Ver MEMORY_2.md e BASE/TRANSPORTE_DESASSISTIDO.md.\n'
 if marker not in old:
  nl='\r\n' if b'\r\n' in old else '\n'
  replace_bytes(path,old+text.replace('\n',nl).encode())
 data=path.read_bytes();assert data.startswith(old) and marker in data
 records.append({'path':str(path),'sha256':hashlib.sha256(data).hexdigest()})
save_json(BASE/'validation/maximum_memory_delivery.json',{'at':utc_now(),'surfaces':records,'receipt':'validation/maximum_capacity_verified.json'})
print(json.dumps({'memory_surfaces_updated':len(records)}))
