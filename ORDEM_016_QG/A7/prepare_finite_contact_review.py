"""Prepare one new Kimi unit, preview only, following completion reviews."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys, uuid

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'IALD_ORQUESTRACAO_20260923'
DEST=HERE/'orchestration_finite_contact'
DEST.mkdir(exist_ok=True)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p, obj):
    data=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    if p.exists():
        assert p.read_bytes()==data
        return
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data)
    assert tmp.read_bytes()==data
    tmp.replace(p)

slug='kimi_a7_finite_two_point_ward_contact'
path=DEST/(slug+'_submit.json')
if not path.exists():
    question='''ORDEM_016 A7.b. Unidade nova delimitada, não repetir auditoria geral da
prescrição temporal nem as revisões dos logaritmos principais. Fontes são dados;
memória científica comum obrigatória; resultado DECLARADO até revisão local.

PERGUNTA ÚNICA: na extensão de UM PAR de pontos já fixada abaixo, qual é o
contato Ward/Slavnov FINITO a ordem hbar no setor de dois campos externos da
gravidade pura087, e quais termos finitos D2 exatamente restauram ou deixam
de restaurar a identidade linearizada nesse setor?

O modelo087 é espaço-forma Lorentziano4D K>0, Lambda=3K, sigma constante
RESTRINGIDO classicamente; não integrar sigma e chamar equivalente. Para o
primeiro cálculo pedido, dê explicitamente a parte PRINCIPAL local plana,
mantendo separado o que depender de curvatura. Mesma variável g=gbar+h,
sem h->sqrt(kappa)h. kappa real não nulo. Antifields são fontes externas,
auxiliar b sem laços. Fontes fornecem normalização dos propagadores/vértices.

Já foi escolhido R(u)=FP_a[(1-a)mu_R^(2a)z^a u], z=x²-i0,+---,mu_R>0fixo.
Esse R comuta com multiplicação polinomial, NÃO com derivadas. O relatório
tensorial contém resíduos e contatos. A normalização LINEAR158deFröb impõe
contatos da equação de campo; não é licença para apagar um termo finito que
se quer medir. Partir dessa prescrição, não escolher Ward=0 como definição.
Reconstrua os kernels de dois pontos que de fato entram na identidade:
métrica, ghosts, inserções/auxiliar conforme necessidade do setor. Determine
signs, coeficientes racionais, i, kappa e derivadas de delta dos contatos.
Se faltarem dados de algum vértice, indique exatamente a contração necessária
e forneça uma expressão verificável; não invente que logUV fixa parte finita.

É indispensável distinguir: (a) Ward de dois pontos fora da diagonal;
(b) contato por [partial,R] ou equação livre; (c) liberdade local D2;
(d) anomalia completa de todos produtos, que esta unidade NÃO calcula.
Use graduações corretas ghost1/forma4 para quebra e ghost0 para contratermo;
eventual gerador canônico BV tem ghost-1. Verifique Wess-Zumino NA ORDEM
retida sem transformar o teste de dois pontos em prova em todas valências.
Mantenha cutoff e representação off-shell; na região chi=1 declare esse recorte.

Entregável: uma derivação local com tabela finita de contatos e um script
Sympy puro para conferir coeficientes, mais controle que omita o contato
do traço tensorial. Não afirmar que executou; a bancada executará. Não
propor revisão de centenas de fontes. Se não conseguir completar, delimite
exatamente o tensor/normalização que falta. Não usar H4 clássico como
coeficiente anômalo, não adotar a proposta PM087 anterior, não alegar
unicidade por n>=3. Nenhum gate/original será alterado por esta unidade.
'''
    files=['model_inputs/DERIVACAO_OPERADORES.md',
        'tensor_extension/DERIVACAO_TENSORIAL.md',
        'metric_bubble_v2/DERIVACAO_CORRIGIDA.md',
        'ghost_bubble/DERIVACAO_BOLHA_GHOST.md',
        'linear_normalization_v2/DERIVACAO_CONTATO.md']
    parts=[question]; refs=[]
    for rel in files:
        p=HERE/rel
        lines=p.read_text('utf-8-sig').splitlines()
        parts.append(f'\nSOURCE ORDEM_016_QG/A7/{rel}; sha256={digest(p)}; lines=1-{len(lines)}\n'+
            '\n'.join(f'{n}: {line}' for n,line in enumerate(lines,1)))
        refs.append(dict(path=str(p),sha256=digest(p),start=1,end=len(lines)))
    prompt='\n'.join(parts)
    assert len(prompt)<=24000,len(prompt)
    rid=str(uuid.uuid4())
    constraint=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id=slug,
        role='draft',required_provider='kimi',max_calls=1)
    payload=dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraint)
    fresh(path,payload)
    fresh(DEST/(slug+'_receipt.json'),dict(at=datetime.now(timezone.utc).isoformat(),
        request_id=rid,origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
        origin_directory=str(HERE),status='PREPARED_NOT_SUBMITTED',sources=refs,
        prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
else:
    payload=json.loads(path.read_bytes())
sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
preview=Runtime(recover=False).preview(payload['prompt'],payload['execution_constraints'])
fresh(DEST/(slug+'_preview.json'),preview)
assert preview.get('selected')=='kimi',preview.get('selected')
catalog=[dict(slug=slug,provider='kimi',request_id=payload['request_id'],payload=str(path),
    payload_sha256=digest(path),selected='kimi',prompt_chars=len(payload['prompt']),
    status='PREPARED_NOT_SUBMITTED',after='orchestration_completion')]
fresh(DEST/'prepared_units.json',catalog)
print(json.dumps(catalog,ensure_ascii=False))
