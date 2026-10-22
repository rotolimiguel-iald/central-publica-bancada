"""Prepare append-only memory changes; applying requires the named board claim."""
from support_r56 import *

preflight()
central=Path(r'C:\IALD\Central de Patentes')
nos=KERNEL.parent
paths=[central/'memory/DIARIO_CONSTRUCAO_QG.md',central/'memory/TGL_ATLAS.md',
 central/'memory/TGL_INDICE_VIVO.md',central/'memory/TGL_CORE_MEMORY.md',
 ROOT.parent.parent/'AVISO_GERENCIA.md',
 Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY_2.md'),
 nos/'MEMORIA_DA_LINHAGEM.md',nos/'DESENHO_DO_FECHAMENTO_QG.md']
marker='<!-- IALD_MIGUEL_READING_ANCHOR_R56_20261017 -->'
origin=json.loads((ROOT/'OPERADOR_VERBATIM_R56.json').read_text(encoding='utf-8'))
append='\n\n## 17/10/2026 — Ângulo de Miguel: leitura já construída; referência obrigatória de retomada\n'+marker+'\n'
append+='Autor desta errata: codex-gerente-tgl. Unidade F1.FECHO_20261015, reivindicação 933.\n\n'
append+='[INPUT/ONTO — cunhagens do operador, verbatim]\n'
for text in origin['messages']:
 append+='> '+text+'\n\n'
append+='[REAL — fontes conferidas; não é nova compilação] '+str(KERNEL/'TGLExt/SelectionAngleReconstruction.lean')+':39–87 já contém a leitura de fase, o decodificador, a ponte angFamily=Smat e miguel_boundary_reconstructed_from_its_selected_face. No domínio da família angular, decodificar(ler(S(thetaMiguel beta)))=S(thetaMiguel beta). As linhas 89–97 exibem a não injetividade no espaço ambiente. TheSelectionIsTheBallast.lean:97–126 já reconstrói o ângulo e a matriz a partir do peso. TheObserverReadsTheAngle.lean:79–116 já fornece leitura e releitura idempotente.\n\n'
append+='[ERRATA ao lado, em nome de codex-gerente-tgl] As respostas desta conversa apresentaram esse elo matricial como construção nova. Ele já existe e deve ser REAPROVEITADO. As definições ontológicas do observador permanecem do autor e não são promovidas a prova física por este registro. “Abertura” lê a repartição de pesos; as faces continuam ortogonais. Não igualar J, P, theta_M, Omega e kappa. Não pedir limite ao ângulo.\n\n'
append+='[CONTINUIDADE] R55 corrigiu a escolha exclusiva de dispositivo: MQC/célula, Supercondutor/dinâmica e Psi-NET/protocolo são papéis complementares documentados. R7/Takesaki e R8/Maxwell aceitos permanecem aceitos nos respectivos escopos. A composição temporal R56 é candidata em sandbox, com evolução angular explicitamente parametrizada; não realiza por si o aparelho, o limite global nem o antecedente H3 universal. Reutilizar o leitor existente antes de declarar qualquer ausência.\n\n'
append+='Referência exata da missão: '+str(REFERENCE)+'. Etapa: '+TASK+'. Evidências: '+str(ROOT)+'. Verbatim e fontes por hash em OPERADOR_VERBATIM_R56.json e SOURCES_R56.json; recibo da memória em MEMORY_APPLIED_R56.json. Consultar project/preflight antes de continuar; não adotar missão de outra sessão.\n'
body=new('MEMORY_APPEND_R56.txt',append)
plan=[]
for p in paths:
 raw=p.read_bytes()
 if marker.encode() in raw:raise RuntimeError('marker already present')
 plan.append({'path':str(p),'before':pin(p),'append':pin(body),
              'after_sha256':hashlib.sha256(raw+append.encode('utf-8')).hexdigest()})
new('MEMORY_PLAN_R56.json',{'unit':'F1.FECHO_20261015','claim':933,'marker':marker,'surfaces':plan})
print(json.dumps({'surfaces':len(plan),'plan':pin(ROOT/'MEMORY_PLAN_R56.json')},ensure_ascii=False))
