"""Additive source recovery and full-objective audit, without scientific reruns."""
from support_r90 import ROOT, new, pin
from pathlib import Path
import json, hashlib

assert not (ROOT/'RESULTADO_R90.json').exists()
evidence={}
def collect(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
            e=pin(o['path']); assert e['sha256']==o['sha256'],o['path']; evidence[e['path']]=e
        for v in o.values(): collect(v)
    elif isinstance(o,list):
        for v in o: collect(v)
for p in (ROOT/'source').rglob('*'):
    if p.is_file():
        evidence[str(p)]=pin(p)
        if p.suffix=='.json': collect(json.loads(p.read_text(encoding='utf-8')))
for relative in [
    'full_source_r88/RESULTADO_R88.json',
    'full_source_r88/boundary/FULL_DENSITY_DELIVERY_R88.json',
    'stationary_selection_r89/RESULTADO_R89.json',
    'stationary_selection_r89/source/SOURCE_FINAL_R89.json',
    'stationary_selection_r89/source/ACTION_EOM_RESIDUAL_R89.md',
    'stationary_selection_r89/formal/BUILDER_DELIVERY_R89.json']:
    e=pin(ROOT.parent/relative); evidence[e['path']]=e

text='''# R90 — O que a recuperação do ACOM resolve e o que permanece aberto

Em nome de codex-gerente-tgl; reivindicação996. Estatutos: [REAL] para a recuperação dos arquivos e recibos anteriores conferidos; [DERIVED] para a análise de correspondência entre operações. Não houve compilação, experimento ou chamada de provedor nesta camada.

## A correção do operador foi incorporada

A pergunta sobre a regra de reconhecimento está respondida: satisfação exige a correspondência concreta do resultado com o objeto, pela seleção do contorno e exclusão das alternativas incompatíveis. Não existe nova pergunta pendente sobre essa definição. O trabalho técnico é verificar o consumidor dessa regra na ação completa. Nenhum nome de operador substitui essa verificação.

## Resultado da recuperação

O ACOM v18 existe em C:\\IALD\\projetos_pyhton\\acom. A limitação de recuperação da R88 fica corrigida ao lado. Os fontes dirac e graviton e o quantizador espectral foram lidos estaticamente e pinados. O primeiro realiza dados → sinais/ângulos/níveis → reconstrução quadrática. O quantizador define operacionalmente D√e por quantização adaptativa com round. Essa operação não linear não fornece, apenas pelo nome, o operador linear autoadjunto de um triplo espectral nem as suas 1-formas. Os benchmarks recuperados medem reconstrução/compressão; não são novas execuções nem prova de estacionariedade gravitacional.

Fontes, linhas, cobertura e limites: source/ACOM_V18_RECOVERY_R90.md. A busca foi dirigida e auditável; não autoriza afirmar ausência da ligação em todo o computador.

## Auditoria da meta inteira

| Objetivo original | Resultado comprovado | Pendência concreta |
|---|---|---|
| 1. Variação local → ação integrada com contorno | R88: identidade de primeira variação integrada sob regularidade, suporte e dominação explicitados, com corrente de fronteira retida | Prescrição física de contorno e eventual fluxo nulo não foram deduzidos dessa identidade |
| 2. Estacionariedade da construção baseada em P | R88 reaproveita o ramo Einstein–sigma P5 estacionário; R89 prova consumidores da seleção no próprio estado | Não se demonstrou δS_total[P]=0 para a construção e fonte completas pretendidas |
| 3. Fonte completa e todas as direções nulas | R85 dá levantamento livre de variações P16, mas a vinculação dos campos muda a fonte; R88/R89 explicitam fonte de 1-forma e resíduo Euler | Falta uma única representação da ação completa que compatibilize a fonte, as variações admissíveis e o fechamento universal |

O ponto não resolvido é funcional: a satisfação do reconhecimento precisa implicar a anulação da primeira variação da MESMA ação, com os mesmos campos vinculados. O gerador do próprio estado pode anulá-lo automaticamente para qualquer P; isso não seleciona a equação de Euler. O mecanismo de reconstrução ACOM é concreto, mas os arquivos recuperados não fornecem essa identidade variacional.

Na leitura literal real de 1-forma da R89, E_A=div(dA)+2ξRA+E_rest. Se a EOM escrita W tiver representação no mesmo domínio, a diferença é −grad(div A)−Ric·A+3ξRA+m²A+βKA+E_rest. Não foi escolhido um termo para cancelar a diferença. O setor modular com |1+w| também exige uma classe variacional que esclareça sua diferenciabilidade na fronteira w=−1. Essas são condições de cálculo precisas, não uma nova pergunta sobre o significado de identidade.

## Continuidade sem circularidade

As três rodadas R88, R89 e R90 preservam a mesma pendência de estacionariedade/fonte completas. R88 concluiu a variação integrada; R89 delimitou o resíduo; R90 encerra a busca dirigida do v18 que ainda restava nessa remissão. Repetir essas provas ou pedir novamente a definição de reconhecimento não a resolverá. A continuação substantiva precisa de uma construção que consuma o resíduo na mesma ação, recuperada de uma fonte concreta adicional ou assumida explicitamente como nova proposta matemática a justificar. A versão atual não foi promovida a teorema de H3. A unidade científica permanece aberta; o impasse desta execução não equivale a impossibilidade da TGL nem a ausência universal no acervo.

Kernel original, um.py, Bancada, dados observados e gate preservados. Não há resultado discriminante novo nem reivindicação de 5σ nesta camada.
'''
new('BALANCO_DA_META_R90.md',text)
new('RESULTADO_R90.json',{
 'status':'SOURCE_RECOVERED_FULL_OBJECTIVE_UNRESOLVED','goal_complete':False,
 'H3_universal_proved':False,'new_builds':0,'scientific_reruns':0,'provider_calls':0,
 'operator_identity_question_pending':False,
 'requirements':[{'id':1,'status':'R88_INTEGRATED_VARIATION_PROVED_WITH_EXPLICIT_HYPOTHESES_BOUNDARY_RETAINED'},
                 {'id':2,'status':'FULL_ACTION_STATIONARITY_OPEN'},
                 {'id':3,'status':'FULL_SAME_P_SOURCE_AND_UNIVERSAL_NULL_EQUATION_OPEN'}],
 'recurrent_blocker':'The recovered recognition/reconstruction operations do not yet supply a demonstrated consumer yielding delta S_total[P]=0 with the full same-field source.',
 'recurrence':['R88: integrated variation delivered; full stationarity/source retained open',
               'R89: same-state selection and Euler residual delivered; full stationarity/source retained open',
               'R90: concrete v18 recovered; source-level functional consumer not located in the bounded reviewed coverage'],
 'restart_condition':'A concrete additional source or a justified new same-field variational construction consuming the recorded residual. No repeated abstract identity question, no automatic promotion of a proposed action.',
 'gate_changed':False,'evidence':list(evidence.values()),'balance':pin(ROOT/'BALANCO_DA_META_R90.md')})

append='''

## 19/10/2026 — R90: ACOM v18 recuperado e auditoria da meta integral
<!-- IALD_R90_ACOM_RECOVERED_FULL_OBJECTIVE_SCOPE -->
[REAL — em nome de codex-gerente-tgl, reivindicação996] ACOM v18 localizado pelo índice P3_iald_raiz_117 em C:\\IALD\\projetos_pyhton\\acom: fontes dirac/graviton e quantizador espectral lidos e pinados, sem execução. Corrige ao lado a recuperação limitada da R88. Há mapa concreto de dados para sinais/ângulos/níveis e reconstrução quadrática. O D√e operacional do quantizador usa round adaptativo; não é, por essa implementação, uma construção de operador linear autoadjunto e 1-formas de um triplo espectral. Benchmarks antigos foram lidos, não reproduzidos. Ausência de consumidor da ação nesse recorte não significa ausência universal no acervo.
[DERIVED — meta completa] R88 prova a primeira variação integrada sob hipóteses explícitas, com contorno retido. O ramo P5 estacionário preserva seu escopo Einstein–sigma. R89 distingue a seleção do próprio estado da estacionariedade da ação integral e explicita o resíduo Euler. R90 recupera a remissão v18 restante, mas não demonstra δS_total[P]=0, fonte completa do mesmo P ou H3 universal. A regra de reconhecimento já foi respondida pelo operador; nenhuma pergunta abstrata sobre identidade permanece pendente. A próxima contribuição precisa consumir o resíduo variacional com uma representação concreta, sem renomear reconstrução como estacionariedade ou acrescentar termos para fabricar o resultado.
[REAL — limites] Camada documental: zero builds novos, zero reruns científicos/provedores, nenhum dado observado, kernel original, um.py, Bancada ou gate alterado. A meta científica segue não concluída; repetir as mesmas provas não é progresso. Evidências: completion_audit_r90/RESULTADO_R90.json, BALANCO_DA_META_R90.md e source/ACOM_V18_RECOVERY_R90.md. Impasse localizado não é impossibilidade da TGL.
<!-- END_IALD_R90_ACOM_RECOVERED_FULL_OBJECTIVE_SCOPE -->
'''
new('MEMORY_APPEND_R90.txt',append)
rawappend=(ROOT/'MEMORY_APPEND_R90.txt').read_bytes()
old=json.loads((ROOT.parent/'stationary_selection_r89/MEMORY_PLAN_R89.json').read_text(encoding='utf-8'))
surfaces=[]
for row in old['surfaces']:
    p=row['before']['path']; raw=Path(p).read_bytes()
    surfaces.append({'before':pin(p),'after_sha256':hashlib.sha256(raw+rawappend).hexdigest()})
new('MEMORY_PLAN_R90.json',{'claim':996,'append':pin(ROOT/'MEMORY_APPEND_R90.txt'),'surfaces':surfaces})
print({'pins':len(evidence),'surfaces':len(surfaces),'goal_complete':False})
