from support_r84 import *
new('ORIGEM.txt', 'Objetivo autorizado pelo operador: 1. Passar da variacao local a acao integrada, tratando os termos de contorno. 2. Demonstrar a estacionariedade na construcao baseada em P. 3. Identificar a fonte completa e demonstrar que as variacoes disponiveis sustentam a equacao pretendida em todas as direcoes nulas. Preservar o objetivo integral; nao supor sua conclusao. Claim993; OH adiado; sem originais/producao/dados/gate.')
mutate('extend','EXTEND',requirements=[{'id':TASK,'criterion':'Passar da variacao local a acao integrada com contorno; demonstrar estacionariedade da construcao em P; identificar fonte completa e provar alcance das variacoes para todas as direcoes nulas. Reuso e provas verificadas; nenhum criterio parcial substitui o objetivo.','depends_on':[]}],reason='Objetivo integral explicitamente autorizado nesta continuacao.',sources=[pin(ROOT/'ORIGEM.txt')])
mutate('claim','CLAIM',task_id=TASK,lease_seconds=14400)
check('INITIAL_PREFLIGHT')
print(TASK)
