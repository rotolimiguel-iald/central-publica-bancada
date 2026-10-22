"""One audited Jev connectivity probe; never repeat an uncertain attempt."""

import hashlib
import json
import urllib.error
import uuid
from datetime import datetime, timezone

from iald_orchestrator.jev import ACTIVATION, ask_with_memory, parse_answer
from iald_orchestrator.jev_secret_store import key_metadata
from iald_orchestrator.safe_files import save_json


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    if not key_metadata()['stored']:
        raise RuntimeError('Chave Jev não cadastrada no cofre.')
    current = json.loads(ACTIVATION.read_bytes()) if ACTIVATION.is_file() else {}
    if current.get('probe_status') in {'dispatching', 'ready', 'uncertain'}:
        print(json.dumps({'status': current['probe_status'], 'probe_id': current.get('probe_id'),
                          'new_provider_call': False}))
        return
    prompt = 'Audite uma demonstração matemática com hipóteses e passos formais explícitos.'
    questions = {'complexity': {'type': 'choice',
        'instructions': 'Classifique a profundidade da tarefa; não execute a tarefa.',
        'criteria': {'standard': 'Resposta direta sem auditoria formal',
                     'deep': 'Auditoria matemática de várias etapas'}}}
    probe_id = str(uuid.uuid4())
    record = {'enabled': False, 'probe_status': 'dispatching', 'probe_id': probe_id,
              'started_at': now(), 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
              'scope': 'STRUCTURED_ROUTING_ONLY', 'provider_calls': 0}
    save_json(ACTIVATION, record)
    try:
        # Once the call begins, a transport error does not prove zero provider usage.
        record['provider_calls'] = 'one_attempt_uncertain_until_response'
        save_json(ACTIVATION, record)
        data, memory_receipt = ask_with_memory(prompt, questions, max_chars=9000)
        classification = parse_answer(data, prompt)
        if classification['complexity'] != 'deep':
            raise ValueError('Probe classification failed the expected deterministic floor.')
    except urllib.error.HTTPError as exc:
        record.update(probe_status='rejected', http_status=exc.code, error_type='HTTPError',
                      ended_at=now(), enabled=False)
        save_json(ACTIVATION, record)
        print(json.dumps({'status': 'rejected', 'http_status': exc.code, 'probe_id': probe_id,
                          'new_provider_call': True}))
        return
    except Exception as exc:
        record.update(probe_status='uncertain', error_type=type(exc).__name__,
                      ended_at=now(), enabled=False)
        save_json(ACTIVATION, record)
        print(json.dumps({'status': 'uncertain', 'error_type': type(exc).__name__,
                          'probe_id': probe_id, 'new_provider_call': True}))
        return
    record.update(probe_status='ready', enabled=True, model=data.get('model'),
                  validated_at=now(), provider_calls=1, usage=data.get('usage'),
                  canonical_memory=memory_receipt, choice=classification.get('complexity'))
    save_json(ACTIVATION, record)
    print(json.dumps({'status': 'ready', 'model': record['model'], 'probe_id': probe_id,
                      'usage': record['usage'], 'new_provider_call': True}))


if __name__ == '__main__':
    main()
