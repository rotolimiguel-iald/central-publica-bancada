from iald_orchestrator.mimo import validate_connection
import json
record = validate_connection()
print(json.dumps({key: value for key, value in record.items() if key != 'signature'}, ensure_ascii=False))
