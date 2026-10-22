from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,sys,uuid
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'IALD_ORQUESTRACAO_20260923'
request_id=str(uuid.uuid4())
def create(p,data):
    assert not p.exists(),p
    raw=json.dumps(data,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw
    t.rename(p)
blocks=[];sources=[]
for name in ['VectorRapiditySpectrum.lean','RapidityJacobian.lean']:
    p=HERE/name;raw=p.read_bytes();lines=raw.decode().splitlines();digest=hashlib.sha256(raw).hexdigest()
    sources.append(dict(path=str(p),sha256=digest,first_line=1,last_line=len(lines)))
    blocks.append(f'FONTE {name}, SHA256 {digest}, linhas 1-{len(lines)}\n'+
                  '\n'.join(f'{i}: {line}' for i,line in enumerate(lines,1)))
prompt='''ORDEM_016, A3.4. NOVA unidade independente: revisão cética da passagem da medida orbital para rapidez e do transporte de ausência de autovetores. O operador autorizou o DeepSeek máximo inclusive alta complexidade; a integração foi corrigida. Esta unidade NÃO retoma o pedido antigo de hipóteses de resolvente, já resolvido localmente, nem substitui a revisão Kimi A3.d encerrada por cota. Uma chamada, sem repetição/fallback; memória científica canônica comum pelo transporte.

PERGUNTA ÚNICA: sob quais hipóteses EXATAS é legítimo transportar o lema já compilado de ausência de autovetores do deslocamento em L²(R;E) às três órbitas da ORDEM016 (massivo escalar, massa zero helicidade 0, massa zero helicidades +1⊕−1), usando a parametrização abaixo, e qual ligação realmente falta demonstrar? Entregue prova matemática ou contraexemplo específico e o menor plano de formalização reaproveitável. Foque domínio/medida a.e./Fubini/ação de helicidade; não abra nova teoria, não faça escolha física, não rederive normalização H2/BW, não declare QG/gate fechados.

Dados de trabalho: p=(r cosh ξ,r sinh ξ,q₂,q₃), r=sqrt(m²+q₂²+q₃²); órbita futura p₀>0, p₀²−p₁²−p₂²−p₃²=m², medida d³p/p₀. Para m>0, r>0 em toda fibra; para m=0, excluir q⊥=0 e provar que a linha excluída é nula na medida orbital (inclusive a singularidade no vértice, que está fora da órbita). O jacobiano longitudinal é r cosh ξ=p₀, logo formalmente d³p/p₀=dξ d²q⊥. Não aceitar só essa frase: conferir bijetividade e equivalência de medidas. No chart, boosts no plano 0–1 traduzem ξ. No fóton, um eventual fator de helicidade pode ser cociclo unitário dependente de ξ,q; não o substituir por 1 sem provar a escolha de gauge ou usar argumento normativo que o dispense.

Estado local: VectorRapiditySpectrum.lean compilou rc0, duas declarações #print axioms no trio propext/Classical.choice/Quot.sound. Você não executou Lean; isso é evidência fornecida pela bancada. RapidityJacobian.lean está EM COMPILAÇÃO, ainda sem aceite nesta pergunta; trate como rascunho. O lema genérico assume deslocamento puro e fase escalar global por s; verifique se norma invariante em cada fibra basta mesmo com cociclo. Distingua ponto-a-ponto de quase em toda parte, o espaço de uma partícula de Fock e prova de ausência de autovetores de prova de KMS. O alvo não autoriza inferir a rede física completa de um chart.

Não afirme nomes/táticas Mathlib sem fonte fornecida, não alegue compilação nem acesso a caminhos locais. Resposta em português, com hipóteses e defeitos delimitados, preservando DERIVED/OPEN/DECLARADO. A sessão local é a única que escreve e compila.

'''+ '\n\n'.join(blocks)
assert len(prompt)<=24000
constraints=dict(mission_id='ORDEM_016',branch_id='A3.4',lemma_id='orbit_measure_rapidity_helicity_scope',
                 role='skeptic',required_provider='deepseek',max_calls=1,max_cost_usd=None,max_output_tokens=393216)
receipt=dict(request_id=request_id,job_id=None,created_at=datetime.now(timezone.utc).isoformat(),
             origin_thread='01a070fc-9484-7e13-a654-c6b5f61093a4',origin_house='Central de Patentes',
             origin_folder=str(HERE.parent),status='prepared',sources=sources,
             prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),execution_constraints=constraints)
create(HERE/'deepseek_orbit_receipt.json',receipt)
create(BASE/'state/session_requests'/f'{request_id}.json',receipt)
create(HERE/'deepseek_orbit_submit.json',dict(operation='submit',request_id=request_id,prompt=prompt,execution_constraints=constraints))
sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
runtime=Runtime(recover=False)
status=runtime.status();create(HERE/'deepseek_orbit_status.json',status)
preview=runtime.preview(prompt,constraints);create(HERE/'deepseek_orbit_preview.json',preview)
assert preview.get('selected')=='deepseek',preview.get('status')
print(json.dumps(dict(request_id=request_id,selected=preview['selected'],status=preview['status'],prompt_chars=len(prompt))))
