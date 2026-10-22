from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]/'IALD_ORQUESTRACAO_20260923'
OUT = HERE.parents[1]/'TUNEL/DO_CHATGPT'
stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')

def write(path, raw):
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name+'.bak_'+stamp)
        with backup.open('xb') as stream:
            stream.write(old)
        assert backup.read_bytes() == old
    tmp = path.with_name(path.name+'.tmp_'+stamp)
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw and raw
    tmp.replace(path)
    assert path.read_bytes() == raw

items = []
for provider in ('kimi', 'mimo'):
    result = json.loads((HERE/f'reuse_{provider}_submission_result.json').read_text(encoding='utf-8'))
    payload = json.loads((HERE/f'reuse_{provider}_submit_v2.json').read_text(encoding='utf-8'))
    assert result['request_id'] == payload['request_id']
    assert result['execution_constraints']['required_provider'] == provider
    receipt = json.loads((HERE/f'reuse_{provider}_receipt_v2.json').read_text(encoding='utf-8'))
    receipt.update(job_id=result['id'], status=result['stage'], registered_at=result['updated_at'],
                   prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
                   canonical_memory_receipt=result.get('canonical_memory',{}).get('receipt'))
    write(HERE/f'reuse_{provider}_receipt_v2.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    write(BASE/'state/session_requests'/f'{result["request_id"]}.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    items.append(dict(provider=provider, request_id=result['request_id'], job_id=result['id'],
                      stage=result['stage'], prompt_sha256=receipt['prompt_sha256']))

text = '# ORDEM 016 — novas unidades de reaproveitamento\n\n'
text += f'Data UTC: {stamp}. [REAL] Duas submissões aceitas na fila existente; estado observado awaiting_dispatch. Não são resultados dos modelos.\n\n'
for item in items:
    text += f'- {item["provider"]}: request `{item["request_id"]}`; job `{item["job_id"]}`.\n'
text += '''
Kimi: revisão da cadeia horizonte físico → fluxo modular da torre → campos representacionais/analíticos de ContratoH2 v3.1. MiMo: inventário dos campos geométricos, frame e normalização, buscando eliminar redundância antes de nova implementação.

Fontes científicas selecionadas com hash calculado e linhas originais; comentários extensos omitidos no pacote de entrada. Prévia confirmou executor exigido; memória canônica comum em modo maximum pelo transporte, com cobertura parcial rastreável. A preparação inicial excedeu o limite de 24 mil caracteres do ingresso e não chamou modelos. A revisão aceita conservou o UUID Kimi nunca antes submetido; textos efetivos são reuse_kimi_submit_v2.json e reuse_mimo_submit_v2.json. Cada unidade permite uma chamada; não há teto diário/financeiro local adicionado.

A tarefa coordenadora Orquestrar IAs na Central IALD recebeu ambos os IDs pela ferramenta oficial; ela conduz as transições. A bancada fará a verificação matemática dos resultados, sem promovê-los automaticamente ao kernel ou gate.

[DECLARADO — coordenação] A restrição local DeepSeek foi corrigida e a rota máxima está habilitada. A comparação antiga já resolvida na bancada não foi reenviada. Nenhuma nova chamada DeepSeek nesta entrega.

Nenhum original científico, kernel, Atlas ou gate foi modificado. Este registro mantém a memória operacional da missão. Custos destas novas unidades ainda não medidos; não registrados como zero.
'''
write(OUT/'ENTREGA_016_MEDIDA_novas_unidades_Kimi_MiMo.md',text.encode())
progress = OUT/'ENTREGA_016_PROGRESSO.md'
entry = f'\n{stamp} | [REAL] A3: unidades Kimi {items[0]["job_id"]} e MiMo {items[1]["job_id"]} registradas awaiting_dispatch; revisão de reaproveitamento, sem novo teorema. Coordenadora avisada. Custos ainda não medidos.\n'
write(progress,progress.read_bytes()+entry.encode())
print(json.dumps(items,ensure_ascii=False))
