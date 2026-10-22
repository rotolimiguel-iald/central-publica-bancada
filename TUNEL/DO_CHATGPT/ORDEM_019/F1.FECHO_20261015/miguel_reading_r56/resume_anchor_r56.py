"""Resume after local schema refusal; preserve the completed ACOM inscription."""
from support_r56 import *

sources=[{k:v for k,v in pin(ROOT/name).items() if k in {'path','sha256'}} for name in
         ['OPERADOR_VERBATIM_R56.json','REAPROVEITAMENTO_R56.md']]
action('extend','r56-add-angular-reuse-schema-r2',requirements=[{
 'id':TASK,'criterion':'Preservar verbatim e referencia existente da leitura do angulo de Miguel em memoria. Compor em sandbox leitura, reconstrucao, releitura e fase relativa sob evolucao angular explicitamente parametrizada; pin, build com trio, controle de alcance e revisao independente. Nao satisfaz por si R4/R5/H3 universal.',
 'depends_on':['R1']}],reason='Ordem humana atual para memorizar e prosseguir; reprise apenas da transicao local recusada por campo bytes excedente no esquema de pin. Inscricao ACOM anterior preservada, sem duplicar.',sources=sources)
action('claim','r56-claim-angular-reuse',task_id=TASK,lease_seconds=14400)
checked,path=preflight()
print(json.dumps({'ready':checked.get('ready'),'receipt':str(path)},ensure_ascii=False))
