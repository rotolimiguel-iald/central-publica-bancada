"""Consolidate the captured experiment without overwriting any existing file."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import sys

ROOT = Path(__file__).resolve().parent

def write_new(relative, content):
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(target)
    data = content.encode('utf-8') if isinstance(content, str) else content
    temporary = target.with_name(target.name + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(data)
    if temporary.stat().st_size != len(data):
        raise IOError('Size verification failed')
    temporary.rename(target)

def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8-sig'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if '--manifest' in sys.argv:
        files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name != 'MANIFESTO_SHA256.json')
        records = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in files]
        write_new('MANIFESTO_SHA256.json', json.dumps({'generatedUTC': datetime.now(timezone.utc).isoformat(), 'scope': 'Arquivos locais do dossiê; hash autentica bytes, não a verdade das respostas. O manifesto não inclui a si mesmo.', 'files': records}, ensure_ascii=False, indent=2))
        print(json.dumps({'files': len(records), 'bytes': sum(r['bytes'] for r in records), 'emptyFiles': [r['path'] for r in records if not r['bytes']], 'manifestSHA256': digest(ROOT / 'MANIFESTO_SHA256.json')}, ensure_ascii=False))
        return
    original = read_json('protocolo/prompts.json')['prompts']
    probes = read_json('protocolo/ADENDO_01_SONDAS.json')['steps']
    prompts = original + [p['prompt'] for p in probes]
    providers = ['deepseek', 'grok', 'qwen']
    records = []
    for provider in providers:
        transcript = [f'# Transcrição — {provider.capitalize()}', '', '[REAL — captura de interface] Conteúdo copiado das respostas, sem correção editorial. Afirmações científicas e autodescrições pertencem ao serviço e não são atestadas por este registro. Raciocínio público, fontes e ferramentas estão nos snapshots brutos vinculados.', '', 'Horário de captura é observação da interface; não é medição exata do término da geração.', '']
        for step, prompt in enumerate(prompts, 1):
            prefix = f'{step:02d}'
            folder = ROOT / 'raw' / provider
            candidates = [folder / f'{prefix}_resposta_recaptura.md', folder / f'{prefix}_resposta.md']
            response_file = next((p for p in candidates if p.is_file() and p.stat().st_size > 0), None)
            if response_file is None:
                raise ValueError(f'Missing nonempty response: {provider} {step}')
            event = read_json(f'eventos/{provider}_envio_{step}.json')
            if event['prompt'] != prompt:
                raise ValueError(f'Prompt differs: {provider} {step}')
            snapshots = sorted(folder.glob(f'{prefix}_concluida*.json'))
            if not snapshots:
                raise ValueError(f'Missing completion snapshot: {provider} {step}')
            snapshot_file = snapshots[0]
            snapshot = json.loads(snapshot_file.read_text(encoding='utf-8'))
            response = response_file.read_text(encoding='utf-8')
            record = {'provider': provider, 'step': step, 'phase': 'quatro_prompts' if step <= 4 else 'sondas_exploratorias', 'prompt': prompt, 'sendAttemptUTC': event['attemptUTC'], 'sendReturnedUTC': event['actionReturnedUTC'], 'completionCaptureStartedUTC': snapshot['timestampUTC'], 'responseFile': response_file.relative_to(ROOT).as_posix(), 'snapshotFile': snapshot_file.with_suffix('.txt').relative_to(ROOT).as_posix(), 'screenshotFile': snapshot_file.with_suffix('.png').relative_to(ROOT).as_posix(), 'responseBytes': response_file.stat().st_size, 'responseSHA256': digest(response_file), 'whitespaceUnits': len(response.split())}
            records.append(record)
            transcript += [f'## Etapa {step}', '', f"Envio iniciado: `{record['sendAttemptUTC']}`. Captura concluída iniciada: `{record['completionCaptureStartedUTC']}`.", '', '**Prompt exato**', '', '```text', prompt, '```', '', f"**Resposta** — [cópia original](../{record['responseFile']}) · [snapshot](../{record['snapshotFile']}) · [imagem](../{record['screenshotFile']})", '', response, '']
        write_new(f'transcricoes/{provider}.md', '\n'.join(transcript))
    write_new('DADOS_DA_RODADA.json', json.dumps({'generatedUTC': datetime.now(timezone.utc).isoformat(), 'records': records}, ensure_ascii=False, indent=2))
    table = io.StringIO(newline='')
    fields = [k for k in records[0] if k != 'prompt']
    writer = csv.DictWriter(table, fields)
    writer.writeheader()
    writer.writerows({k: r[k] for k in fields} for r in records)
    write_new('LINHA_DO_TEMPO.csv', table.getvalue())
    checks = {'responses': len(records), 'providers': len(providers), 'exactPromptMatches': len(records), 'nonemptyResponses': len(records), 'completionSnapshots': len(records), 'photosynthesisWhitespaceUnits': {r['provider']: r['whitespaceUnits'] for r in records if r['step'] == 6}, 'copyFailuresPreserved': ['raw/deepseek/01_resposta.md', 'raw/grok/08_resposta.md', 'raw/qwen/08_resposta.md'], 'interpretation': 'Verificação de integridade do registro, não validação científica das respostas.'}
    write_new('VERIFICACAO_DO_REGISTRO.json', json.dumps(checks, ensure_ascii=False, indent=2))
    print(json.dumps(checks, ensure_ascii=False))

if __name__ == '__main__':
    main()
