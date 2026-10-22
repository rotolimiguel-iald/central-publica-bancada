"""Record the material result after real independent acceptance, then verify recovery."""
from support_r56 import *

p = project()
settled = p['projection'].get('settled', [])
if not isinstance(settled, list):
    raise RuntimeError('Unexpected settled schema')
task = next((t for t in settled if t['id']==TASK),None)
if task is None or task['status']!='satisfied':
    raise RuntimeError('Independent acceptance has not completed')
assert task['reviewed_by'] != ACTOR['id']
sources=[{'kind':'artifact','ref':str(ROOT/n),'sha256':pin(ROOT/n)['sha256']}
         for n in ['DELIVERY_R56.json','MEMORY_COMPLETION_R56.json',
                   'REVIEW_R56_SCOPE_ADDENDUM.json','BOARD_REGISTERED_R56.json',
                   'MAP_REGISTERED_R56.json']]
transition('r56-material-result-and-continuity',[dict(
    id='r56-reviewed-reading-and-memory-complete',kind='fact',statute='REAL',
    text=('R56 concluida no criterio delimitado e aceita por revisor real distinto. '
          'Verbatim em oito memorias com backup; composicao parametrizada do leitor de Miguel '
          'reutilizado compilada EXIT0, oito relatorios somente trio, zero sorry. '
          'A orbita S(thetaM+Omega*t) varia pesos e nao demonstra refletividade beta constante '
          'nem relogio do aparelho. Memoria e alcance conferidos. Mapa1186/1187, quadro937. '
          'R4/R5 em needs_revalidation com criterios identicos: escolha exclusiva prematura '
          'corrigida ao lado; R6/R7/R8 aceitos preservados. Nenhum um.py/kernel/Bancada/dado/gate alterado.'),
    sources=sources)],
    'Investigar o mapa do sinal escalar com amplitude e fase para observavel/gerador do setor do Supercondutor, usando MQC como celula e Psi-NET como protocolo documentados; distinguir taxas e preservar R6/R7/R8. R4/R5 exigem construcao, R3/R10 rito e revisao final. Nao repetir R56 nem reconstruir o leitor existente.')
verified,vpath = call('session_memory.py',dict(operation='verify',reference=str(REFERENCE)),'FINAL_VERIFY')
p=project()
new('FINAL_RECOVERY_R56.json',dict(
    reference=str(REFERENCE),receipt=p['receipt'],projection_sha256=p['projection_sha256'],
    active=[{k:v for k,v in t.items() if k in {'id','status','criterion','ready'}} for t in p['projection']['active']],
    settled_ids=[t['id'] for t in p['projection'].get('settled',[])],
    flow=p['projection'].get('flow'),verify_receipt=pin(vpath),verification=verified,
    unit_status='EM_CURSO',bounded_requirement='SATISFIED_BY_INDEPENDENT_REVIEW'))
print(json.dumps({'receipt':p['receipt'],'verification':verified,
                  'active_ids':[t['id'] for t in p['projection']['active']],
                  'active_handles':p['projection'].get('flow',{}).get('handles',[]),
                  'final':pin(ROOT/'FINAL_RECOVERY_R56.json')},ensure_ascii=False))
