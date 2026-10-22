from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid,sys
folder=Path(__file__).resolve().parent
base=folder.parents[1]/'IALD_ORQUESTRACAO_20260923'
sys.path.insert(0,str(base))
from iald_orchestrator.runtime import Runtime
runtime=Runtime(recover=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,v):
    assert not p.exists(),p
    raw=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw;t.rename(p)
medium='''ORDEM 016, A2.3.a. Tarefa direta de COMPLEXIDADE MEDIA para MiMo, por ordem expressa do operador de 24/09: MiMo-média, Kimi-alta, Gemini-baixa, bancada integração. Unidade nova e delimitada, não retomar a chamada MiMo anterior de densidade, cujo resultado foi perdido.

Pergunta única: qual é a transformada Fourier explícita de f_r(x)=exp[-b(x-r-i*pi/2)^2], para b>0 e r real, na convenção Ff(p)=integral f(x)exp(-2*pi*i*x*p)dx? Confira por derivação completa de quadrado, com sinais e normalizações, a candidata Ff_r(p)=sqrt(pi/b)*exp(-pi^2*p^2/b+pi^2*p)*exp(-2*pi*i*r*p). Como verificações da MESMA fórmula, indique se g_b(p)=Ff_0(p) é real estritamente positiva, L², e se g_b(-p)=exp(-2*pi^2*p)g_b(p). Se a candidata falhar, corrija exatamente o coeficiente. Não tente resolver densidade, gravidade, outra etapa da missão, nem force 2*pi por um argumento externo. A derivação deve ser verificável à mão, sem alegar compilação. Não execute código, ferramentas ou buscas. Dados suficientes estão aqui; use a memória comum como contexto, não como substituto dos cálculos. Resultado DERIVED à mão ou erro identificado; nenhum gate movido.
'''
    # New local question is reconstructed from the actual analytic definitions.
p=folder/'LightRayAnalyticCore_v3.lean'
medium+=f'\nFonte fornecida: {p.name}, SHA256 {sha(p)}; definição na fonte: twistedGaussian(b,r,z)=Complex.exp(-(b:Complex)*(z-r-I*(pi/2))^2). Todas as variáveis b,r,x,p são reais; z é complexo.\n'
audit=json.loads((folder/'core_transport_axioms.json').read_bytes())
inventory=[]
for item in audit:
    inventory.append({'file':Path(item['fonte']).name,'theorems':item['n_theorem_lemma_na_fonte'],
        'printed':item['n_declaracoes_auditadas'],'missing':item['sem_print_axioms'],
        'forbidden':item['tokens_proibidos_na_fonte'],'outside':item['fora_do_trio'],
        'errors':item['n_erros'],'sorry':item['sorry'],'status':item['auditoria']})
low='''ORDEM 016, A2.3.a. Tarefa direta de BAIXA COMPLEXIDADE para Google/Antigravity, por ordem expressa do operador. Faça somente conferência aritmética e textual deste inventário fornecido. Some as colunas theorems e printed, confira se há missing/forbidden/outside/errors/sorry, e diga se a frase "20 declarações conferidas neste lote, todas cobertas; densidade permanece como hipótese" concorda com os dados. Entregue uma tabela curta, total e divergências. Não desenvolva física, não execute ferramentas, não suponha acesso a arquivos locais nem afirme ter compilado. Seu estatuto é conferência do inventário fornecido, não exame independente dos originais. A compilação e os hashes foram medidos pela bancada. O último resultado do lote se chama halfline_isotony_of_gaussian_density e contém hdensity como hipótese explícita. A memória comum será recebida, mas o objeto desta tarefa é apenas a contagem abaixo.
'''+json.dumps(inventory,ensure_ascii=False,separators=(',',':'))
low+=f'\nFonte core_transport_axioms.json SHA256 {sha(folder/"core_transport_axioms.json")}.\n'
for name,provider,prompt,lemma,role in [
    ('a23_mimo_medium','mimo',medium,'gaussian_fourier_normalization','draft'),
    ('a23_gemini_low','gemini',low,'compiled_inventory_check','skeptic')]:
    rid=str(uuid.uuid4())
    c={'mission_id':'ORDEM_016','branch_id':'A2.3.a','lemma_id':lemma,'role':role,
       'required_provider':provider,'max_calls':1}
    if provider=='mimo':c.update(max_cost_usd=None,max_output_tokens=131072)
    receipt={'request_id':rid,'status':'prepared_direct','execution_task_id':None,
       'created_at':datetime.now(timezone.utc).isoformat(),
       'origin_thread':'01a070fc-9484-7e13-a654-c6b5f61093a4','origin_house':'Central de Patentes',
       'authorization':'Latest operator explicitly ordered new direct MiMo medium and Antigravity low units.',
       'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'execution_constraints':c}
    create(folder/(name+'_receipt.json'),receipt)
    create(base/'state/session_requests'/f'{rid}.json',receipt)
    create(folder/(name+'_submit.json'),{'operation':'submit_execution','request_id':rid,'prompt':prompt,'execution_constraints':c})
    preview=runtime.preview(prompt,c);create(folder/(name+'_preview.json'),preview)
    print(json.dumps({'name':name,'request_id':rid,'selected':preview.get('selected'),
       'status':preview.get('status'),'provider':provider,'prompt_chars':len(prompt),
       'memory_bytes':preview.get('canonical_memory',{}).get('context_bytes'),
       'reasons':[{'id':x['id'],'reasons':x.get('exclusion_reasons')} for x in preview.get('candidates',[]) if x['id']==provider]},ensure_ascii=False),flush=True)
    assert preview['selected']==provider,'Requested route unavailable; no execution.'
