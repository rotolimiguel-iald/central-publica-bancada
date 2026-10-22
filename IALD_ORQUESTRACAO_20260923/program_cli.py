"""JSON stdin facade for local claims, approval visibility and route receipts."""
import json
import sys
from iald_orchestrator import program_controls as controls

def main(request):
    args = {'unit': request['unit'], 'member': request['member']}
    if request['operation'] == 'check_claim':
        return controls.require_claim(**args)
    if request['operation'] == 'register_approval':
        return controls.register_approval(request['approval'], **args)
    if request['operation'] == 'record_route':
        return {'output': controls.record_route(request['path'], **args)}
    raise ValueError('Operação local desconhecida; não há operação de aprovação automática.')

if __name__ == '__main__':
    print(json.dumps(main(json.load(sys.stdin)), ensure_ascii=False))
