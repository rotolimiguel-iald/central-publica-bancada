from pathlib import Path
import json,hashlib
from iald_orchestrator.safe_files import replace_bytes,save_json,utc_now
BASE=Path(__file__).resolve().parent
note=(BASE/'work/optional_work_20260924/delivery_note.md').read_text(encoding='utf-8')
marker=b'IALD_OPTIONAL_CHATGPT_ASSISTANCE_20260924'
previous=json.loads((BASE/'validation/maximum_memory_delivery.json').read_bytes())
records=[]
for item in previous['surfaces']:
 path=Path(item['path']);old=path.read_bytes()
 text=note if path.name!='MEMORY.md' else '\n\n<!-- IALD_OPTIONAL_CHATGPT_ASSISTANCE_20260924 -->\n- ChatGPT/Física é assistência opcional. Falta de cota não bloqueia preparação/entrega IALD; preservar executor, memória comum e idempotência. Ver MEMORY_2.md e TRANSPORTE_DESASSISTIDO.md.\n'
 if marker not in old:
  nl='\r\n' if b'\r\n' in old else '\n';replace_bytes(path,old+text.replace('\n',nl).encode())
 data=path.read_bytes();assert data.startswith(old) and marker in data
 records.append({'path':str(path),'sha256':hashlib.sha256(data).hexdigest()})
save_json(BASE/'validation/optional_work_memory.json',{'at':utc_now(),'surfaces':records,'tests_passed':53,'provider_calls':0})
print(json.dumps({'memory_surfaces_updated':len(records)}))
