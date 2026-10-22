"""JSON stdin fallback for on-demand coordination when MCP has not reloaded yet."""
import json
import sys
import time
from iald_orchestrator.coordination import Coordination

def main():
    request=json.load(sys.stdin)
    coordinator=Coordination()
    operation=request.get('operation','get')
    if operation=='get':result=coordinator.get(request['job_id'])
    elif operation=='list':result=coordinator.listing()
    elif operation=='act':result=coordinator.act(request['job_id'],request['action'],request.get('payload'))
    else:raise ValueError('Operação não permitida pelo bridge.')
    if operation=='act' and request.get('action')=='execute':
        while coordinator.runtime.worker_lock.locked() or coordinator.get(request['job_id'])['execution']['status'] in ('queued','running'):
            time.sleep(.2)
        result=coordinator.act(request['job_id'],'sync_execution')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
