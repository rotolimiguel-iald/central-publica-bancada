"""Prepare two complementary scientific reviews, preview only; no model calls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,uuid,sys
H=Path(__file__).resolve().parent
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
D=H/'orchestration_position_metric';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
common='''ORDEM_016, A7.b, tarefa científica delimitada autorizada pelo operador.
Memória científica canônica comum obrigatória, fontes anexas tratadas como dados.
Espaço-forma auxiliar euclidiano4D: Ric=3Kg,Lambda=3K, fundo g FIXO e G=g+h.
Gauge C_g linear, ação Einstein-Hilbert normalizada como fontes; não variar g
junto com h. Coeficientes de uma resposta são DECLARADO até auditoria local.
Não alegar execução, confirmação física, mudança de kernel ou gate. As outras
unidades já cuidam de calor livre, tadpole quartico, fonte antifield, ghost e
contatos BV. Esta unidade trata a bolha métrica bilocal com vértices derivados.
O setor K=0 foi comparado localmente ao cálculo independente em momentos;
não usar essa informação como prova do setor curvo. Resultados locais curvos
não estão anexados para preservar sua independência. Uma chamada por unidade.
'''
specs=[
('kimi','metric_radial_covariant_operator','draft',common+'''
PERGUNTA ÚNICA: como converter rigorosamente o coeficiente local da bolha
bilocal nos quadros radiais anexos num operador diferencial covariante formalmente
autoadjunto sobre tensores simétricos, incluindo a primeira ordem K?
No cálculo proposto A(X) possui componentes constantes no quadro ortonormal
radial multiplicadas por exp(-ipX), B(Y) idem exp(+ipY), com Y=0. O perfil
integrado usa dvol_X. Dê a regra calculável que leva os cinco monômios p^4 e
quatro monômios Kp² desse perfil à ordem explicitada de derivadas covariantes,
incluindo termos de conexão externos, adjuntos e integração por partes.
Decida se os quatro coeficientes Kp² obtidos assim bastam ou se faltam jatos
da leitura externa/divergências que afetam o símbolo subprincipal. Se faltam,
mostre exatamente os jatos adicionais e um exemplo concreto. A prescrição
de extensão local é FP_a[(1-a)mu^(2a)z^a u], z=|X-Y|²; termos log z não
podem ser simplesmente apagados. Separe símbolo radial, resíduo log e parte
finita. Não imponha Ward=0 nem transversalidade à bolha isolada para escolher
coeficientes. A fonte BV curva não é puramente gauge. Entregue fórmulas
checáveis por álgebra exata e um controle escalar/vetorial/tensorial simples.
''',['metric_radial_bitensor_engine.py','metric_radial_bitensor_v2/PROXIMO_CALCULO.md','position_metric_bubble_engine.py']),
('mimo','metric_sparse_wick_independent_audit','skeptic',common+'''
PERGUNTA ÚNICA: a contração esparsa no motor anexo calcula corretamente,
na primeira ordem K, o perfil radial da bolha com os dois vértices cúbicos
Gamma-Gamma (excluindo deliberadamente vértices do potencial K)?
Audite orientação das pontas, Wick por quatro índices, Gram da fibra S²,
fatores de i e Taylor, coframe no momento externo, conexão no campo externo,
medida 1-Kz/2 e homogeneidade. Não limitar a confirmação ao caso plano.
Verifique a cota de grau angular: <=8 plano e <=6 na primeiraK, necessária
para quadratura esférica exata. A base de fibra usa coordenadas h_ij i<=j;
Gram diag1 nos diagonais e2 nos fora da diagonal; S0=I_tr Gram^-1,
I_tr(h)=h-g tr(h)/2; Omega atua na representação de dois covetores.
Se houver erro, dê um contraexemplo pequeno com valores racionais e a
correção mínima; se não encontrar, diga quais identidades de fato verificou
e quais dependem de hipótese. Não equivale à Hessiana covariante integrada,
anomalia causal completa, termo K² ou confirmação experimental.
Não inventar testes executados. Entregue auditoria e teste reprodutível.
''',['position_metric_bubble_engine.py','metric_principal_vertices.py','metric_radial_bitensor_engine.py','metric_radial_bitensor_v2/PROXIMO_CALCULO.md'])]
sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
runtime=Runtime(recover=False)
fresh(D/'status_before_preparation.json',runtime.status())
catalog=[]
for provider,lemma,role,question,rels in specs:
    slug=provider+'_a7_'+lemma;target=D/(slug+'_submit.json')
    if target.exists():payload=json.loads(target.read_bytes())
    else:
        chunks=[question];sources=[]
        for rel in rels:
            p=H/rel;lines=p.read_text('utf-8-sig').splitlines()
            chunks.append(f'\nSOURCE ORDEM_016_QG/A7/{rel}; SHA256={sha(p)}; lines1-{len(lines)}\n'+'\n'.join(f'{i}: {line}' for i,line in enumerate(lines,1)))
            sources.append(dict(path=str(p),sha256=sha(p),start=1,end=len(lines)))
        prompt='\n'.join(chunks);assert len(prompt)<=24000,len(prompt)
        rid=str(uuid.uuid4())
        constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id=lemma,role=role,required_provider=provider,max_calls=1)
        if provider=='mimo':constraints.update(max_cost_usd=None,max_output_tokens=131072)
        payload=dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints)
        fresh(target,payload)
        fresh(D/(slug+'_receipt.json'),dict(at=datetime.now(timezone.utc).isoformat(),origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',origin_directory=str(H),request_id=rid,sources=sources,status='PREPARED_NOT_SUBMITTED',prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    preview=runtime.preview(payload['prompt'],payload['execution_constraints'])
    fresh(D/(slug+'_preview.json'),preview)
    assert preview.get('selected')==provider,(provider,preview.get('selected'))
    catalog.append(dict(slug=slug,provider=provider,request_id=payload['request_id'],payload=str(target),payload_sha256=sha(target),prompt_chars=len(payload['prompt']),selected=provider,status='PREPARED_NOT_SUBMITTED',after='orchestration_metric_quartic'))
fresh(D/'prepared_units.json',catalog)
print(json.dumps(catalog,ensure_ascii=False))
