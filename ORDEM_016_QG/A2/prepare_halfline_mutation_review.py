from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import uuid

folder = Path(__file__).resolve().parent
base = folder.parents[1]/'IALD_ORQUESTRACAO_20260923'
out = folder.parents[1]/'TUNEL/DO_CHATGPT'
now = datetime.now(timezone.utc)
request_id = str(uuid.uuid4())

def create(path, data):
    assert not path.exists(), path
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode()
    temp = path.with_name(path.name+'.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.rename(path)

names = ['LightRayGaussianDensity_v2.lean', 'LightRayGaussianOrthogonality_v2.lean',
         'LightRayDensitySeparation_v2.lean', 'LightRayCoreExtension_v2.lean',
         'LightRayGaussianTransform_v5.lean']
parts, metadata = [], []
for name in names:
    raw = (folder/name).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    lines = raw.decode().splitlines()
    metadata.append({'file': name, 'sha256': digest, 'first_line': 1, 'last_line': len(lines)})
    parts.append(f'FONTE: {name}, linhas1-{len(lines)}, SHA256 {digest}\n'+
                 '\n'.join(f'{i+1}: {line}' for i, line in enumerate(lines)))
prompt = '''ORDEM016 A2.3.a: nova unidade ALTA de controle adversarial da meia-inclusão agora compilada. Kimi K3 máximo, cético. Não é repetição da unidade terminal core_transport_and_density_audit: naquela ainda não existia a prova de densidade; esta pede os controles negativos concretos da conclusão nova.

Pergunta única: quais controles negativos NÃO VACUOS verificam precisamente o alcance e os sinais do novo halfline_isotony? A ordem exige substituir a largura π por π/2 ou3π/2 e substituir a≥0 por a≤0. Dê o ponto matemático/tipado que deve falhar em cada controle, uma testemunha quando possível, e confira se uma simples tentativa de aplicar o teorema antigo a tipos incompatíveis seria apenas teste superficial. Não confunda uma falha de compilação de argumento com prova de que a proposição é falsa. Note que a=0 é identidade; o controle negativo de sinal deve usar a<0. Não alegue compilar, executar programas, escrever arquivos, buscar acervo ou mover gate. A bancada escreverá e compilará os probes.

Dados: H=L²(R,dξ); Fourier usa exp(-2πiξp). U(a)f(ξ)=exp(ia exp ξ)f(ξ). No espaço espectral T_c=M_exp(-cp) tem domínio ponderado real, JH(p)=conjH(-p), K_c=Fix(JT_c). K_π=F^-1K_c com c=2π². Para largura w, a correspondente constante Fourier é c=2πw. Núcleo f_r(ξ)=exp[-b(ξ-r-iπ/2)^2], b>0; span REAL. Multiplicador m_a(z)=exp(ia exp z), norma exp(-a expξ sin y), contração para a≥0,0≤y≤π, torção m_a(ξ+iπ)=conj m_a(ξ). A cadeia anterior demonstrou holomorfia, integrabilidade, desaparecimento do contorno vertical, balanço modular, domínio ponderado e U(a)f_r. Agora foram compilados os lemas abaixo, incluindo densidade real por projeção ortogonal e halfline_isotony SEM hdensity. Compilação isolada rc0, #print axioms apenas trio; evidência da bancada, não sua. O alvo A2.3.d de unicidade da largura ainda não está provado; não promovê-lo por nomenclatura.

Entregue crítica fundamentada, alcance exato e até três probes matematicamente pertinentes; não proponha outra teoria ou alvos fora dessa árvore. A memória científica comum será acrescentada pelo transporte, com cobertura registrada. Fontes novas custodiadas fornecidas abaixo.

''' + '\n\n'.join(parts)
constraints = {'mission_id':'ORDEM_016','branch_id':'A2.3.a',
               'lemma_id':'halfline_mutation_controls','role':'skeptic',
               'required_provider':'kimi','max_calls':1}
payload = {'operation':'submit','request_id':request_id,'prompt':prompt,
           'execution_constraints':constraints}
receipt = {'request_id':request_id,'job_id':None,'execution_task_id':None,
           'created_at':now.isoformat(),'status':'prepared_coordination',
           'origin_thread':'01a070fc-9484-7e13-a654-c6b5f61093a4',
           'origin_house':'Central de Patentes',
           'authorization':'Operator resumed task division; Kimi-high. New mandatory mutation review of newly compiled halfline theorem.',
           'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
           'execution_constraints':constraints,'sources':metadata}
create(folder/'a23_kimi_mutation_receipt.json',receipt)
create(base/'state/session_requests'/f'{request_id}.json',receipt)
create(folder/'a23_kimi_mutation_submit.json',payload)
sys.path.insert(0,str(base))
from iald_orchestrator.runtime import Runtime
preview=Runtime(recover=False).preview(prompt,constraints)
create(folder/'a23_kimi_mutation_preview.json',preview)
assert preview['selected']=='kimi', preview.get('status')
print(json.dumps({'request_id':request_id,'selected':preview['selected'],
                  'prompt_chars':len(prompt),'sources':metadata},ensure_ascii=False))
