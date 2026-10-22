from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid,sys

folder=Path(__file__).resolve().parent
base=folder.parents[1]/'IALD_ORQUESTRACAO_20260923'
request_id=str(uuid.uuid4())
now=datetime.now(timezone.utc).isoformat()
sources=['LightRayCoreMembership.lean','LightRayCoreExtension_v2.lean',
         'LightRayFourierBoundary_v2.lean','density_route_next.md']
parts=[]
metadata=[]
for name in sources:
    p=folder/name;raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    lines=raw.decode('utf-8').splitlines()
    metadata.append({'file':name,'sha256':digest,'lines':len(lines)})
    parts.append(f'FONTE LOCAL FORNECIDA: {name}, linhas 1-{len(lines)}, SHA256 {digest}\n'+
                 '\n'.join(f'{i+1}: {line}' for i,line in enumerate(lines)))
prompt='''ORDEM 016, A2.3.a, revisão cética independente do Kimi K3 máximo.
Autorização direta do operador nesta tarefa: "use vc mesmo as ferramentas disponíveis das outras IA's, experimente usar o Kimi para algumas tarefas da missão, não precisa ficar passando para a outra sessão". Unidade NOVA de revisão da construção local. Não repetir, retomar ou substituir a chamada MiMo encerrada: dela não existe resultado disponível.

PERGUNTA ÚNICA: a ligação local do transporte U(a) ao K construído e o argumento proposto para densidade REAL das gaussianas são matematicamente válidos, ou qual é a primeira falha precisa que impede concluir a meia-inclusão? Atue como cético: confira sinais, fatores Fourier, integrabilidade, identificação de domínios, fechamento real versus complexo e possível circularidade; se houver falha, dê reparo mínimo ou contraexemplo. Distinga o resultado efetivo de qualquer alegação de que 2π foi forçado.

Convenções: H=L²(R,dp) espectral; T_c=M_exp(-cp) com domínio ponderado; JH(p)=conj(H(-p)); S_c=JT_c; K_c=Fix S_c é subespaço padrão fechado. Fourier usa exp(-2πixp). Em rapidez, K=F^-1 K_c, c=2π². U(a)f(x)=exp(iaexp(x))f(x). A bancada compilou isoladamente a cadeia analítica Cauchy/L1/L2, o balanço Fg(p)=exp(cp)conj(Fg(-p)) para g=m_a f_r, e os arquivos de ligação abaixo; rc0 e axiomas no trio conforme recibos locais. Isso não é transposição ao kernel nem prova da densidade. O último lema usa hdensity explicitamente. Você não deve afirmar compilação própria, executar programas, alterar arquivos, pesquisar acervos adicionais ou mover gate.

Entregue a crítica em português, com hipóteses e passos verificáveis. O roteiro de densidade é OPEN/a formalizar, produzido pela bancada local, não por MiMo. Uma crítica favorável não substitui Lean. Não atribua confirmação física. Preserve os estatutos e indique exatamente o alcance. Se propor táticas, não invente nomes existentes na biblioteca. Fontes fornecidas a seguir contêm o material novo; a memória científica canônica comum é acrescida pelo transporte com seu recibo de cobertura real.

'''+ '\n\n'.join(parts)
constraints={'mission_id':'ORDEM_016','branch_id':'A2.3.a',
             'lemma_id':'core_transport_and_density_audit','role':'skeptic',
             'required_provider':'kimi','max_calls':1}
payload={'operation':'submit_execution','request_id':request_id,'prompt':prompt,
         'execution_constraints':constraints}
receipt={'request_id':request_id,'job_id':None,'execution_task_id':None,'status':'prepared_direct',
         'created_at':now,'origin_thread':'01a070fc-9484-7e13-a654-c6b5f61093a4',
         'origin_house':'Central de Patentes','purpose':'ORDEM016 A2.3.a independent skeptic',
         'authorization':'Latest operator explicitly requested direct tools, without another session.',
         'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'sources':metadata,
         'execution_constraints':constraints}
def create(p,value):
    assert not p.exists(),p
    raw=json.dumps(value,ensure_ascii=False,indent=2).encode()
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw
    temp.rename(p)
create(folder/'a23_kimi_direct_receipt.json',receipt)
create(base/'state/session_requests'/f'{request_id}.json',receipt)
create(folder/'a23_kimi_direct_submit.json',payload)
sys.path.insert(0,str(base))
from iald_orchestrator.runtime import Runtime
preview=Runtime(recover=False).preview(prompt,constraints)
create(folder/'a23_kimi_direct_preview.json',preview)
assert preview['selected']=='kimi',preview.get('status')
print(json.dumps({'request_id':request_id,'selected':preview['selected'],'status':preview['status'],
                 'prompt_chars':len(prompt),'canonical_memory':preview.get('canonical_memory')},ensure_ascii=False))
