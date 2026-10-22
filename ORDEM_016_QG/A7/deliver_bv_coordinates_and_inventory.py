"""Document the BV coordinate bridge and the conditional vertex inventory."""
from pathlib import Path
from datetime import datetime,timezone
import json
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=H/'bv_coordinate_inventory_delivery'
def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    r=json.loads((H/'bv_antifield_coordinate/results.json').read_bytes())
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    sources=[H.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md',
        H.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
        H.parents[1]/'REEXAME_SUFICIENCIA_087_20260910/REEXAME_SUFICIENCIA.md',
        H/'sigma_restriction/results.json']
    note=f'''[DERIVED — equivalência de coordenadas BV e inventário condicionado; Q2 OPEN]

# Os sinais são transportados junto com os antifields

A fórmula98 de Fröb1803.10235v3, p26, usa derivadas direita/esquerda e
(phiA,fdagB)=deltaAB; s=(S,.) é a convenção104. Fonte primária lida:
https://arxiv.org/pdf/1803.10235v3 . A expressão seguinte é a correspondência
derivada aqui, não uma nova normalização nem uma afirmação atribuída ao artigo.

Nas coordenadas B da bancada, torne explícito o antibracket:

 (F,G)_B=sum_A epsilonA[(dR_phiA F)(dL_bdagA G)-(dR_bdagA F)(dL_phiA G)],
 epsilonA=(-1)^paridade(phiA).

Com fdagA=epsilonA*bdagA, o pullback do bracket canônico F é exatamente B.
Os campos e suas contrações não mudam. A ação livre B

 Sfree+hdagB Kg c-barcdagB b

vira Sfree+hdagF Kg c+barcdagF b. Ambas dão qh=Kg c e qbarc=-b.
O vértice B hdagB Lie_c h+cdagB c.nabla c vira
hdagF Lie_c h-cdagF c.nabla c. Também qcdag muda de sinal:

 qcdagB=-Qbarc-Kg*hdagB, qcdagF=+Qbarc+Kg*hdagF.

Portanto o sinal do defeito ghost E e o sinal do vértice mudam juntos.
A contribuição +d div(c) de aridade1 permanece. Não é permitido mudar só
um desses sinais e citar a outra convenção. A escolha implícita anunciada
em069 fica agora explicitada; o texto069 original permanece intacto.

CAS: {r['checks']}controles, CPU{r['cpu_seconds']}s, rc0. Foram conferidos
o bracket em monômios até grau3, todos os geradores, o quadrado do diferencial,
o transporte da ação e o monômio cdag c dc. O modelo finito usa um componente
de gauge e não substitui a análise funcional do espaço-tempo. Controle
negativo ímpar: q1h=c h'+2h c', q1c=c c' dá q1²h=0; trocar só o sinal
de q1c dá -2c c'h'-4h c c'', não zero.

# Inventário em primeira ordem

No modelo métrico da087 com gauge linear da069, a interação cúbica é
V1=V1metrico+V1ghost+Faf. As duas primeiras parcelas só têm campos.
A matriz Hfull com hb=Kg HQ,bh=HQ Kg*,bb=0 e blocos ghost +/-HQ
tem defeito de Ward ENTRE CAMPOS igual a zero por multiplicação de blocos,
independentemente de HD ser bisolução. Seu defeito Euler estendido aos
antifields pode ser não nulo, como calculado na entrega anterior.

Logo, mantendo a representação livre G equivarante e a prescrição Hfull
declaradas, A1 nos vértices sem antifields zera. Nesse inventário,
A1(V1)=A1(Faf); A1(V2)=0 porque os vértices quarticos são sem antifields:
as transformações difeomórficas de h e c têm somente a parcela livre e
a parcela quadrática que gera Faf. Isso não computa A2(V1,V1).

Se forem mantidas as três flutuações escalares do alvoS3, o fundo constante
não as elimina da teoria quântica. O vértice antifield adicional é
xi†_a c^mu nabla_mu xi^a. Sua contribuição de aridade1 depende só do
primeiro jato do defeito Euler escalar; esse vetor natural zera no espaço-forma
constante e par. Essa observação NÃO elimina os laços escalares em aridade2
nem demonstra um quociente quântico do modelo acoplado. O fundo físico
phi=id continua distinto da referência087.

O representante normalizado euclidiano encontrado foi
a1(V1)=337K² int chi div(c)/10. Ele é q0 da primitiva linear
337K² int chi tr(h)/20 na mesma normalização e, por qb c=0,
é q0-fechado. Com cutoff variável, int chi div(c)=-int dchi.c e não
pode ser descartado como se chi fosse constante. Trata-se de aridade1
localizada, não da primeira quebra interagente COMPLETA já removida.
O símbolo qb na frase anterior significa o diferencial livre q0; não o campo b.

O coeficiente337/10 continua condicionado à normalização euclidiana e sob
revisão independente DeepSeek6945. MiMo57e7 revê este dicionário de sinais.
A passagem aos produtos temporais, realidade, família causal admissível e
consistência com A2 ainda precisa ser verificada. Nenhum contratermo foi
adotado, nenhum resultado transferido ao par físico, nenhum gate alterado.
AberturaSHA256={opening}.
'''
    # Fix a harmless textual variable before the new immutable report is first written.
    note=note.replace('por qb c=0','por q0 c=0').replace('O símbolo qb na frase anterior significa o diferencial livre q0; não o campo b.\n','')
    write(D/'DICIONARIO_E_INVENTARIO.md',note.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_BV_coordenadas_e_inventario.md',note.encode('utf-8'))
    paths=[Path(__file__),D/'DICIONARIO_E_INVENTARIO.md',H/'bv_antifield_coordinate/results.json',
        H/'bv_antifield_coordinate/manifest.json']+sources
    put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],
        checks=r['checks'],cpu_seconds=r['cpu_seconds'],full_Q2=False,gate_changed=False))
    event=dict(at=now.isoformat(),event='BV_ANTIFIELD_COORDINATE_BRIDGE',target='A7.b',
        checks=r['checks'],cpu_seconds=r['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json'))
    append(OUT/'LEDGER_016.jsonl',json.dumps(event,ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: dicionário assinado↔canônico BV verificado, {r["checks"]}controles CPU{r["cpu_seconds"]}s. Inventário A1 no modelo métrico explicitado; A2 permaneceOPEN. DeepSeek6945running,MiMo57e7admitido aguardando worker,Kimi3quota. AberturaSHA256={opening}.\n')
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    state['at']=now.isoformat();state['completed_this_turn'].append('BV signed/canonical antifield coordinate bridge with1185checks; conditional V1/V2 inventory')
    state['next']=['Receive DeepSeek6945 coefficient review and MiMo57e7 coordinate review without duplicate execution',
        'Continue localized A2 and its WZ identity; arity1 auxiliary coefficient is337/10 K² times physical normalization still to fix',
        'Use explicit BV coordinate map when comparing Frob; scalar fluctuations are not quantum-quotiented',
        'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain']
    state['pending_orchestration']='DeepSeek6945running session9073; MiMo57e7 awaiting_dispatch; Kimi3 await actual quota recovery'
    state['bv_coordinate_inventory_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False,own_processes=[])
    state['latest_verified_orchestration']['deepseek_next'].update(status='RUNNING_CONFIRMED_BY_COORDINATOR',
        job_id='f1a5534b-6c8d-47aa-8f86-b86e29384836',execution_task_id='8c9a02b5-4221-4bff-93f0-908b062e86e8',
        worker_session=9073,observed_at='2026-09-25T17:17:28Z')
    state['latest_verified_orchestration']['mimo_new']=json.loads((H/'orchestration_bv_antifield_sign/prepared_units.json').read_bytes())[0]
    state['latest_verified_orchestration']['mimo_new'].update(status='AWAITING_DISPATCH_CONFIRMED_BY_COORDINATOR',
        job_id='ab8c32ea-cab7-4853-8675-d0e75c683d23')
    put(p,state,True)
    for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=r['checks'],cpu_seconds=r['cpu_seconds']),ensure_ascii=False))
if __name__=='__main__':main()
