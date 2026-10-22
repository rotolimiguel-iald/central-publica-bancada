"""Append the authorized clarification and a bounded reuse task to the same mission."""
from support_r56 import *

origin=pin(ROOT/'OPERADOR_VERBATIM_R56.json')
reuse=pin(ROOT/'REAPROVEITAMENTO_R56.md')
def source(p, kind):return {'kind':kind,'ref':p['path'],'sha256':p['sha256']}

records=[
 {'id':'r56-human-miguel-reading','kind':'decision','statute':'INPUT',
  'text':'O operador identifica a medida com semelhanca por paridade inversa, o observador com a forma matricial da luz e o angulo de Miguel com a leitura da abertura da fronteira. Mandou memorizar e prosseguir. Falas integrais na fonte; identificacoes ontologicas nao sao promovidas a teoremas por este registro.',
  'sources':[source(origin,'operator')]},
 {'id':'r56-existing-angular-reconstruction','kind':'fact','statute':'REAL',
  'text':'Consulta das fontes: SelectionAngleReconstruction.lean:83-87 ja contem miguel_boundary_reconstructed_from_its_selected_face; 79-81 liga angFamily=Smat; 89-97 mostra nao injetividade fora da familia. O fato medido nesta etapa e presenca/conteudo do codigo, nao nova compilacao. Reutilizar esse elo, nao reconstruir como ausente.',
  'sources':[source(reuse,'artifact'),source(pin(KERNEL/'TGLExt/SelectionAngleReconstruction.lean'),'artifact')]},
 {'id':'r56-erratum-reading-reconstruction','kind':'erratum','statute':'INPUT',
  'text':'Errata em nome de codex-gerente-tgl: minhas respostas anteriores apresentaram a leitura/reconstrucao angular como tarefa nova; o elo matricial ja existe. R55 tambem corrige a escolha exclusiva MQC/Supercondutor/Psi-NET. R4/R5 permanecem abertos no seu alcance fisico; aceites R7/R8 preservados. R11 sera apenas composicao e registro de alcance, sem concluir a missao inteira.',
  'sources':[source(origin,'operator'),source(reuse,'artifact')]}]
transition('r56-authorized-reading-anchor',records,
 'Reutilizar o angulo de Miguel e o leitor existente; compor a leitura temporal em sandbox, depois revisar. Nao refazer Takesaki/Fock/Maxwell aceitos.')
action('extend','r56-add-angular-reuse', requirements=[{
 'id':TASK,'criterion':'Preservar verbatim e referencia existente da leitura do angulo de Miguel em memoria. Compor em sandbox leitura, reconstrucao, releitura e fase relativa sob evolucao angular explicitamente parametrizada; pin, build com trio, controle de alcance e revisao independente. Nao satisfaz por si R4/R5/H3 universal.',
 'depends_on':['R1']}], reason='Ordem humana atual para memorizar e prosseguir apos identificar teorema existente; etapa delimitada de reaproveitamento, sem adotar nova hipotese fisica.', sources=[origin,reuse])
action('claim','r56-claim-angular-reuse',task_id=TASK,lease_seconds=14400)
checked,path=preflight()
print(json.dumps({'ready':checked.get('ready'),'receipt':str(path)},ensure_ascii=False))
