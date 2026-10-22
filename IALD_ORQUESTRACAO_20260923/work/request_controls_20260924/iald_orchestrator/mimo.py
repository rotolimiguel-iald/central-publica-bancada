"""Official MiMo API; text-only, explicit paid authorization, no hidden retries."""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import time
import urllib.error
import urllib.request
from .profiles import BASE
from .safe_files import save_json, utc_now
from .secret_store import load_mimo, key_metadata

URL = 'https://api.xiaomimimo.com/v1/chat/completions'
MODEL = 'mimo-v2.6-pro'
CONTEXT_WINDOW = 1048576
MAX_OUTPUT = 131072
MAX_INPUT_BYTES = CONTEXT_WINDOW - MAX_OUTPUT - 4096
MAX_RESPONSE_BYTES = 32_000_000
RECEIPT = BASE/'validation/mimo_connection.json'
AUTHORIZATION = BASE/'state/mimo_authorization.json'
PRICE_SOURCE = 'https://mimo.mi.com/docs/en-US/price/pay-as-you-go'


def authorization():
    if not AUTHORIZATION.is_file():
        return {'enabled': False}
    data = json.loads(AUTHORIZATION.read_bytes())
    if data.get('scope') != 'IALD_LOCAL_MANUAL_TASKS' or data.get('financial_cap_usd') is not None:
        return {'enabled': False}
    return data


def signature():
    return {'adapter_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'key': key_metadata(), 'model': MODEL, 'authorization': authorization()}


def connection_status():
    if not authorization().get('enabled'):
        return 'api_billing_not_enabled'
    if not key_metadata()['stored']:
        return 'api_key_required'
    if RECEIPT.is_file():
        data = json.loads(RECEIPT.read_bytes())
        if data.get('signature') == signature() and data.get('status') == 'ready':
            return 'ready'
    # A reviewed configuration migration may preserve the prior authentication
    # evidence without misrepresenting it as a new paid connection test.
    migration = BASE/'validation/mimo_maximum_migration.json'
    if RECEIPT.is_file() and migration.is_file():
        old=json.loads(RECEIPT.read_bytes()); proof=json.loads(migration.read_bytes())
        current=signature(); previous=old.get('signature',{})
        if (old.get('status')=='ready' and proof.get('validation_type')=='OFFLINE_CAPABILITY_UPDATE_PRIOR_AUTH'
            and proof.get('previous_adapter_sha256')==previous.get('adapter_sha256')
            and proof.get('current_adapter_sha256')==current['adapter_sha256']
            and {k:v for k,v in previous.items() if k!='adapter_sha256'}=={k:v for k,v in current.items() if k!='adapter_sha256'}):
            return 'ready'
    return 'installed_pending_auth_validation'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError('MiMo solicitou redirecionamento inesperado; credencial não encaminhada.')


def parse_response(data):
    if data.get('model') != MODEL:
        raise RuntimeError('MiMo não confirmou o modelo solicitado.')
    choices = data.get('choices')
    if not isinstance(choices, list) or len(choices) != 1:
        raise RuntimeError('Resposta MiMo inválida.')
    choice = choices[0]
    message = choice.get('message', {})
    if choice.get('finish_reason') != 'stop' or message.get('tool_calls'):
        raise RuntimeError('MiMo não concluiu uma resposta textual; verificar limite técnico de saída.')
    text = message.get('content')
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError('MiMo devolveu resposta vazia.')
    usage = data.get('usage')
    if not isinstance(usage, dict):
        raise RuntimeError('MiMo não informou o consumo; execução não validada.')
    for field in ('prompt_tokens', 'completion_tokens', 'total_tokens'):
        if type(usage.get(field)) is not int or usage[field] < 0:
            raise RuntimeError('Contagem MiMo inválida.')
    if usage['total_tokens'] != usage['prompt_tokens'] + usage['completion_tokens']:
        raise RuntimeError('Contagem total MiMo inconsistente.')
    cached = (usage.get('prompt_tokens_details') or {}).get('cached_tokens', 0)
    if type(cached) is not int or not 0 <= cached <= usage['prompt_tokens']:
        raise RuntimeError('Contagem de cache MiMo inválida.')
    cost = ((usage['prompt_tokens']-cached)*Decimal('0.435') + cached*Decimal('0.0036') + usage['completion_tokens']*Decimal('0.87'))/Decimal(1_000_000)
    # No raw response or internal reasoning is retained.
    return {'text': text, 'usage': usage, 'model': MODEL,
            'cost_estimate_usd': str(cost), 'cost_status': 'ESTIMATE_FROM_PROVIDER_TOKENS_AND_PUBLISHED_RATES',
            'pricing_source': PRICE_SOURCE, 'pricing_checked_at': '2026-09-23',
            'verification': 'PROVIDER_COMPLETED_NOT_FACT_CHECKED'}


def execute(prompt, *, cancel=None, process_callback=None, max_output=MAX_OUTPUT):
    if not authorization().get('enabled'):
        raise RuntimeError('Uso pago MiMo não autorizado.')
    if not isinstance(prompt, str) or not prompt or len(prompt.encode('utf-8')) > MAX_INPUT_BYTES:
        raise ValueError('Pedido MiMo vazio ou acima do limite técnico de entrada.')
    if type(max_output) is not int or not 1 <= max_output <= MAX_OUTPUT:
        raise ValueError('Limite técnico de saída inválido.')
    if cancel and cancel.is_set():
        raise RuntimeError('Tarefa cancelada antes do envio.')
    payload = {'model': MODEL, 'messages': [{'role': 'user', 'content': prompt}],
               'max_completion_tokens': max_output, 'stream': False,
               'thinking': {'type': 'disabled' if max_output < 256 else 'enabled'}}
    key = load_mimo()
    request = urllib.request.Request(URL, json.dumps(payload).encode('utf-8'),
                                     {'Content-Type': 'application/json', 'api-key': key})
    del key
    start = time.monotonic()
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=7200) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise RuntimeError('Resposta MiMo excedeu o limite técnico.')
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'MiMo recusou a chamada (HTTP {exc.code}); conferir acesso e saldo no provedor.') from None
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError('Falha de conexão MiMo; sem nova tentativa automática.') from None
    finally:
        request.remove_header('Api-key')
    if cancel and cancel.is_set():
        raise RuntimeError('Tarefa cancelada; a chamada já enviada pode ter consumido crédito.')
    try:
        data = json.loads(body)
    except ValueError:
        raise RuntimeError('MiMo devolveu conteúdo inválido.') from None
    return dict(parse_response(data), elapsed_seconds=round(time.monotonic()-start, 3))


def validate_connection():
    try:
        result = execute('Responda somente o número: 6 × 7.', max_output=32)
        if result['text'].strip() != '42':
            raise RuntimeError('Teste MiMo não retornou o resultado esperado.')
        record = {'status': 'ready', 'result': result}
    except Exception as exc:
        record = {'status': 'installed_pending_auth_validation', 'reason': str(exc)}
    record.update(checked_at=utc_now(), signature=signature())
    save_json(RECEIPT, record)
    return record
