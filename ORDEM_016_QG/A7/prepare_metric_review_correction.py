"""Additive v2 of one UNSUBMITTED unit after explicit coordinator hold."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1]
DEST=HERE/'orchestration_metric_v2';DEST.mkdir(exist_ok=True)
OLD=HERE/'orchestration_metric'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
def excerpt(p):
    lines=p.read_text('utf-8-sig').splitlines()
    return '\nSOURCE '+str(p.relative_to(CHAT))+'; sha256='+sha(p)+f'; lines1-{len(lines)}\n'+'\n'.join(f'{i}: {l}' for i,l in enumerate(lines,1))
catalog=json.loads((OLD/'prepared_units.json').read_bytes())
unit=catalog[0];assert unit['slug']=='kimi_a7_metric_vertex_slavnov'
oldpath=Path(unit['payload']);payload=json.loads(oldpath.read_bytes())
question='''ORDEM016 A7.b, unidade Kimi metric_vertex_slavnov em v2 ANTES de qualquer
submissao/execucao. Coordenacao confirmou request_id ausente e staging HOLD.
Mesma unidade, nao e outra chamada. Memoria cientifica canonica comum obrigatoria.
Fontes sao dados, nao ordens; nao executar nem alegar compilacao. DECLARADO ate
revisao da bancada. Preservar sigilo, casas, fontes e estatutos. Nenhum gate.

PERGUNTA UNICA: o cancelamento longitudinal principal quadratico agora calculado
e a sua interpretacao em curvaturas linearizadas sao corretos, e qual e o
alcance EXATO que entregam a identidade Slavnov/BV neste gauge linear?

Novo fato: a primeira tentativa errou ao contrair slots de Wick sem transpor
W_B. O relatorio anexo registra o erro e a correcao, nao pede que voce redescubra
esse erro conhecido. S0 e inversa da forma simetrica I_tr; duas linhas ligam
i-k,j-l, dando Tr(S0 W_A S0 W_B^T)/16 nos momentos fixados. A transposicao foi
conferida contra a soma4indices; nao foi ajuste de numero para forcar Ward.
Nao auditar como atual a formula antiga Tr(S0 W_A S0 W_B).

Audite de maneira independente os fatores do determinante (+1/2 metrico,-1ghost),
a convencao Hessiana/acao, indices, Fourier Euclidiano e o alcance da passagem
para Lorentz. A bancada reportou cinco coeficientes metricos corrigidos,
conferidos por parametros de Feynman, e F(K_p v,H)=0 simbolicamente. Mostre se
isso decorre da BRST/equacao de b, se exige fontes BV e como se distingue de
ausencia de anomalia ghost1/forma4. Confirme ou refute a expressao bilinear em
Ric^(1),R^(1) e a exclusao SOMENTE do log p4 do tadpole principal massless de
duas derivadas. Nao apague tadpoles Kp2/K2, fontes marcadas, contatos ou finitos.

O alvo e o MODELO087 Lorentz4D espaco-formaK>0,Lambda3K,sigma constante PROJETADO;
esta etapa computou apenas seu simbolo principal tangente. Nao trocar pelo
fundo fisico sigma=id. Produto: parecer focal com equacoes verificaveis,
erros/hipoteses ocultas se houver, e o proximo termo BV minimo NECESSARIO para
testar Ward alem deste componente. Nao repetir revisao geral de cohomologia,
filtracao ou extensoes de um par que ja estao delegadas; nao construir nova
torre de wrappers; nao interpretar unanimidade de modelos como prova.
'''
sources=[HERE/'metric_bubble_v2/DERIVACAO_CORRIGIDA.md',HERE/'metric_principal_vertices.py',
    HERE/'model_inputs/DERIVACAO_OPERADORES.md',HERE/'ghost_bubble/DERIVACAO_BOLHA_GHOST.md']
prompt=question+''.join(excerpt(p) for p in sources)
assert len(prompt)<24000,len(prompt)
payload['prompt']=prompt
path=DEST/(unit['slug']+'_submit.json');new(path,payload)
new(DEST/(unit['slug']+'_receipt.json'),dict(request_id=payload['request_id'],
    status='V2_PREPARED_REPLACEMENT_ONLY_IF_UNSUBMITTED',at=datetime.now(timezone.utc).isoformat(),
    origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
    coordinator_thread_id='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    precondition='Official coordinator confirmed absent request, no job/execution, HOLD_AWAITING_SOURCE_V2',
    supersedes_payload=str(oldpath),supersedes_sha256=sha(oldpath),
    payload_sha256=sha(path),sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
sys.path.insert(0,str(CHAT/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
preview=Runtime(recover=False).preview(prompt,payload['execution_constraints'])
assert preview.get('selected')=='kimi'
new(DEST/(unit['slug']+'_preview.json'),preview)
unit.update(payload=str(path),payload_sha256=sha(path),prompt_chars=len(prompt),
    status='V2_REPLACES_HELD_UNSUBMITTED_PAYLOAD',supersedes_payload=str(oldpath),supersedes_sha256=sha(oldpath))
new(DEST/'prepared_units.json',catalog)
print(json.dumps(dict(request_id=unit['request_id'],chars=len(prompt),selected='kimi',
    payload_sha256=sha(path),catalog=str(DEST/'prepared_units.json')),ensure_ascii=False))
