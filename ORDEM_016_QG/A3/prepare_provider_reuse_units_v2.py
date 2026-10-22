"""Reuse the unsubmitted Kimi ID and trim source excerpts to the documented ingress limit."""
from pathlib import Path
import json, hashlib, uuid, sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
# Load only the local declarative plan, stopping before its preparation loop.
plan_source = (HERE/'prepare_provider_reuse_units.py').read_text(encoding='utf-8')
exec(compile(plan_source.split('sys.path.insert(0, str(BASE))')[0], 'reuse_plans', 'exec'))

def code_excerpt(path, start=1, end=None):
    raw = path.read_bytes()
    original = raw.decode('utf-8-sig').splitlines()
    end = len(original) if end is None else min(end, len(original))
    depth = 0
    output = []
    for number, line in enumerate(original, 1):
        code = ''
        i = 0
        while i < len(line):
            if line[i:i+2] == '/-':
                depth += 1; i += 2
            elif depth and line[i:i+2] == '-/':
                depth -= 1; i += 2
            elif depth:
                i += 1
            elif line[i:i+2] == '--':
                break
            else:
                code += line[i]; i += 1
        if start <= number <= end and code.strip():
            output.append(f'{number}: {code.rstrip()}')
    meta = dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(),
                start_line=start, end_line=end, presentation='comments_and_blank_lines_omitted')
    return meta, f'FONTE {path.name}, SHA256 inteiro {meta["sha256"]}, linhas {start}-{end}; comentários e linhas vazias omitidos.\n'+'\n'.join(output)

plans['kimi']['sources'][0] = (CONTRACT/'ContratoQG_v31.lean',159,243)
plans['kimi']['sources'][4] = (KERNEL/'TheMasterFires.lean',100,137)
plans['mimo']['sources'][0] = (CONTRACT/'ContratoQG_v31.lean',195,243)
plans['mimo']['sources'][5] = (KERNEL/'StrongAssembly.lean',130,155)
sys.path.insert(0, str(BASE))
from iald_orchestrator.runtime import Runtime
runtime = Runtime(recover=False)
summary = []
for provider, plan in plans.items():
    if (HERE/f'reuse_{provider}_preview_v2.json').exists():
        existing = json.loads((HERE/f'reuse_{provider}_submit_v2.json').read_text(encoding='utf-8'))
        checked = json.loads((HERE/f'reuse_{provider}_preview_v2.json').read_text(encoding='utf-8'))
        assert checked.get('selected') == provider
        summary.append(dict(provider=provider, request_id=existing['request_id'], selected=provider,
                            status=checked['status'], prompt_chars=len(existing['prompt']),
                            canonical_memory=checked.get('canonical_memory')))
        continue
    blocks = [code_excerpt(*entry) for entry in plan['sources']]
    introduction = common.replace('Preserve a distinção entre matriz Lorentz, representação unitária no Hilbert e ação sobre a rede de álgebras. Estatutos e limitações locais precisam acompanhar conclusões.', '')
    introduction = introduction.replace('Uma lista literal remaining em Python ou um comentário histórico não é prova de inexistência.', '')
    prompt = introduction + '\n' + plan['task'] + '\n\n' + '\n\n'.join(b[1] for b in blocks)
    assert len(prompt) <= 24000, (provider, len(prompt))
    constraints = dict(mission_id='ORDEM_016', branch_id='A3.d', lemma_id=plan['lemma'],
                       role=plan['role'], required_provider=provider, max_calls=1)
    if provider == 'mimo':
        constraints.update(max_cost_usd=None, max_output_tokens=131072)
    old = HERE/f'reuse_{provider}_receipt.json'
    request_id = json.loads(old.read_text(encoding='utf-8'))['request_id'] if old.exists() else str(uuid.uuid4())
    receipt = dict(request_id=request_id, job_id=None, status='prepared_not_submitted',
                   created_at=datetime.now(timezone.utc).isoformat(),
                   origin_thread='01a070fc-9484-7e13-a654-c6b5f61093a4',
                   origin_house='Central de Patentes', origin_folder=str(ROOT),
                   sources=[b[0] for b in blocks], execution_constraints=constraints,
                   revision_reason='Local preparation only; prior oversized payload was never submitted.',
                   prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest())
    payload = dict(operation='submit', request_id=request_id, prompt=prompt, execution_constraints=constraints)
    create(HERE/f'reuse_{provider}_receipt_v2.json', receipt)
    create(BASE/'state/session_requests'/f'{request_id}_prepared_v2.json', receipt)
    if not (BASE/'state/session_requests'/f'{request_id}.json').exists():
        create(BASE/'state/session_requests'/f'{request_id}.json', receipt)
    create(HERE/f'reuse_{provider}_submit_v2.json', payload)
    preview = runtime.preview(prompt, constraints)
    create(HERE/f'reuse_{provider}_preview_v2.json', preview)
    assert preview.get('selected') == provider, (provider, preview.get('status'), preview.get('selected'))
    summary.append(dict(provider=provider, request_id=request_id, selected=preview['selected'],
                        status=preview['status'], prompt_chars=len(prompt),
                        canonical_memory=preview.get('canonical_memory')))
create(HERE/'reuse_dispatch_previews_v2.json', summary)
print(json.dumps([{k:v for k,v in item.items() if k!='canonical_memory'} for item in summary], ensure_ascii=False))
