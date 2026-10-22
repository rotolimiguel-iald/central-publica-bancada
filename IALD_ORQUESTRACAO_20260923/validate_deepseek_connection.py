"""One public request after explicit operator authorization; never automatic retry."""
import json
from iald_orchestrator.deepseek import validate_connection

if __name__ == '__main__':
    result = validate_connection()
    print(json.dumps({k: v for k, v in result.items() if k != 'signature'}, ensure_ascii=False))
