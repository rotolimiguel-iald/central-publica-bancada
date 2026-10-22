"""Record the observed project test without replacing its memory or sources."""
from pathlib import Path
from datetime import datetime
import json
import os

base = Path(__file__).resolve().parent
path = base / 'coordinator.json'
old = path.read_bytes()
value = json.loads(old)
value.update(
    transport_status='APP_MEDIATED_SOURCE_AND_PROMPT_TEST_PASSED',
    validation_task_id='6ab402ba-7838-83e9-94d5-12c7da627a42',
    validation_task_title='Preparar prompt TGL IALD',
    uploaded_files_count=16,
    consulted_files_in_test=4,
    validation_record='validation/chatgpt_work_project_test.json',
    final_response_roundtrip_validated=False,
)
new = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
backup.write_bytes(old)
assert backup.read_bytes() == old
temp = path.with_suffix('.tmp')
temp.write_bytes(new)
assert temp.read_bytes() == new and len(new) > len(old)
assert path.read_bytes() == old
os.replace(temp, path)
assert path.read_bytes() == new
print(json.dumps({'status':value['transport_status'], 'backup':str(backup)}, ensure_ascii=False))
