"""Official Antigravity lifecycle hook: deny tools and attest hook activation."""
import json
from pathlib import Path
import sys
import uuid

BASE=Path(__file__).resolve().parent
GUARDS=BASE/'state/antigravity_guard'

def main():
    payload=json.load(sys.stdin)
    conversation=str(uuid.UUID(payload['conversationId']))
    GUARDS.mkdir(parents=True,exist_ok=True)
    event=sys.argv[1]
    record={'event':event,'conversation_id':conversation,'model':payload.get('modelName')}
    if event=='pretool':
        record['tool']=payload.get('toolCall',{}).get('name')
        response={'decision':'deny','reason':'IALD_TEXT_ONLY: ferramentas desativadas neste conector.'}
    elif event=='preinvocation':
        response={}
    else:
        raise ValueError('Unsupported hook')
    # Unique records contain metadata only, never prompts, arguments or credentials.
    path=GUARDS/(conversation+'_'+uuid.uuid4().hex+'.json')
    data=json.dumps(record).encode('utf-8')
    with path.open('xb') as output:
        output.write(data)
    print(json.dumps(response))

if __name__=='__main__':
    main()
