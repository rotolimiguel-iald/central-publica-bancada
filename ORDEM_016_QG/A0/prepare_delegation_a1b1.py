import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
base = root.parent / 'IALD_ORQUESTRACAO_20260923'
dest = root / 'A0' / 'delegation_a1b1.json'

def atomic_new(path, value):
    data = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('xb') as f:
        f.write(data)
    assert tmp.stat().st_size == len(data)
    os.replace(tmp, path)

if dest.exists():
    print(dest.read_text(encoding='utf-8'))
    raise SystemExit(0)

source = root / 'A1' / 'minimal_imports' / 'ContratoQG_v31_Minimal.lean'
order = root.parent / 'TUNEL' / 'PARA_CHATGPT' / 'ORDEM_016_a_gravidade_quantica_primeiro.md'
prompt = '''ORDEM 016, A-1.b1: uma unidade de rascunho matemático, destinada ao MiMo. A origem continuará responsável por escrever/compilar Lean. NÃO executar outro provedor como substituto: se a rota não puder fixar MiMo ou limitar o custo desta chamada a US$0,50, manter pendência e informar. Não mudar cotas, filtros, política global, nem disparar revisão adicional. Kimi será usado posteriormente para crítica, em pedido separado. A nova autorização do operador admite Claude/Gemini também, mas esta unidade foi atribuída ao MiMo. Projeto Física: apenas preservar sentido e preparar/transportar o pedido, sem transformar opinião em prova; não afirmar carregar memória integral.

PERGUNTA ÚNICA: qual é a menor construção explícita de um fluxo interno D(t) que NÃO comuta com translações U(a), preservando um vetor de vácuo, e que permita testar honestamente um contrato AQFT com cunha? Forneça uma construção e calcule um comutador não nulo; identifique precisamente quais hipóteses adicionais ela NÃO satisfaz. Não confundir uma matriz finita com habitante de TGLSpecificAQFTWitness.

Contexto: contrato H2 exige representação U de R^4, continuidade, fidelidade, energia positiva, vácuo unitário invariante, rede local com vetor cíclico/separante, fluxo modular KMS e covariância de boost. A parede commuting_translations_excluded só rejeita D que comuta com U; precisamos de controle fora dessa classe. Uma tentativa ingênua H=C^3, vac=e0, U(a)=diag(1,exp(i*a0),exp(2*i*a0)), D rotação de e1/e2 não comuta, mas U não é fiel em R^4 e B(H) não tem vac separante. Não esconda essas falhas. Um modelo parcial pode ser útil como controle, não como H2 construído. Não escolher o par físico do operador. Responder em até 2500 palavras, sem busca remota, código executado, axioma novo ou alegação de compilação. Uma pergunta, uma chamada; nenhum material confidencial fornecido.
'''
prompt += '\nProveniência local (não presumir acesso remoto):\n'
prompt += f'{order.name}:414; SHA256={hashlib.sha256(order.read_bytes()).hexdigest()}\n'
prompt += f'{source.name}; SHA256={hashlib.sha256(source.read_bytes()).hexdigest()}; resumo das exigências acima, não substitui texto integral.\n'
rid = str(uuid.uuid4())
receipt = {'request_id': rid, 'origin_thread_id': '01a070fc-9484-7e13-a654-c6b5f61093a4',
           'origin_house': 'Central de Patentes / Chatgpt / ORDEM_016_QG',
           'created_at': datetime.now(timezone.utc).isoformat(), 'target': 'A-1.b1',
           'requested_provider': 'mimo', 'max_cost_usd': 0.50, 'prompt': prompt,
           'prompt_sha256': hashlib.sha256(prompt.encode('utf-8')).hexdigest(),
           'status': 'prepared_not_submitted', 'job_id': None}
atomic_new(base / 'state' / 'session_requests' / (rid + '.json'), receipt)
atomic_new(dest, receipt)
atomic_new(root / 'A0' / 'delegation_a1b1_submit.json',
           {'operation': 'submit', 'prompt': prompt, 'request_id': rid})
print(json.dumps({'request_id': rid, 'prompt_sha256': receipt['prompt_sha256'], 'status': receipt['status']}))
