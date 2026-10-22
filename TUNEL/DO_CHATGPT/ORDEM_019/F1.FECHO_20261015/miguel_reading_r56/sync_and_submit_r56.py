"""Reconcile the obsolete R4/R5 note without changing criteria; submit bounded R11."""
from support_r56 import *

def api_pin(p):
    return {k:v for k,v in pin(p).items() if k in {'path','sha256'}}

sources = [api_pin(ROOT/n) for n in ['OPERADOR_VERBATIM_R56.json',
            'REVIEW_R56_SCOPE_ADDENDUM.json']]
sources.append(api_pin(ROOT.parent/'CONFERENCIA_PONTE_DISPOSITIVO_R55.txt'))
reason = ('Errata em nome de codex-gerente-tgl, autorizacao humana atual e revisao R56: '
          'a escolha exclusiva MQC/Supercondutor/Psi-NET era prematura. Investigar papeis '
          'complementares ja documentados (celula/dinamica/protocolo), sem presumir identidade '
          'fisica nem identificar inequivocamente o aparelho singular. Criterio literal preservado. '
          'R4/R5 nao satisfeitos; R3/R10 pendentes; R6/R7/R8 aceitos preservados. '
          'Uma escolha fisica realmente incompatível e indeterminada nas fontes volta ao operador.')
for task_id in ('R4','R5'):
    p=project()
    task=next(t for t in p['projection']['active'] if t['id']==task_id)
    assert task['status']=='blocked'
    action('amend','r56-correct-obsolete-device-note-'+task_id,task_id=task_id,
           criterion=task['criterion'],reason=reason,sources=sources)

p=project()
task=next(t for t in p['projection']['active'] if t['id']==TASK)
result,path=action('submit','r56-submit-reviewed-angular-composition',task_id=TASK,
    lease_id=task['lease']['id'],evidence=[api_pin(ROOT/n) for n in [
        'DELIVERY_R56.json','MEMORY_COMPLETION_R56.json','REVIEW_R56.json',
        'REVIEW_R56_SCOPE_ADDENDUM.json']],
    note='Candidata delimitada e revisada; oito memorias com bytes, composicao Lean EXIT0/trio. R4/R5 continuam abertos; nao e realizacao fisica do dispositivo.')
print(json.dumps({'task':result.get('task'),'receipt':str(path)},ensure_ascii=False))
