"""Check the received review against an existing compiled artifact, without rebuilding."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CHAT = HERE.parents[1]
A6 = ROOT / 'A6_EQUACAO_DA_VERDADE'
DEST = A6 / 'received_reviews'
OUT = CHAT / 'TUNEL/DO_CHATGPT'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def new(path, raw):
    if isinstance(raw, str):
        raw = raw.encode('utf-8')
    if path.exists():
        assert path.read_bytes() == raw
        return
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw and raw
    tmp.replace(path)

manifest = A6 / 'B_fechamentos/bridges_and_single_time_manifest.json'
unit = next(u for u in json.loads(manifest.read_text('utf-8'))['units'] if u['branch'] == 'B1c')
source = Path(unit['source'])
log = Path(unit['audit']['log'])
assert sha(source) == unit['source_sha256'] == unit['receipt']['source_sha256']
assert sha(log) == unit['log_sha256'] == unit['receipt']['log_sha256']
assert unit['receipt']['rc'] == 0 and unit['audit']['auditoria'] == 'PASSA'
assert unit['audit']['sem_print_axioms'] == [] and not unit['audit']['sorry']
assert unit['audit']['fora_do_trio'] == {}
name = 'TGLExt.EquationOfTruth.single_time_conserved_iff_factors'
assert name in unit['audit']['axiomas'] and name in log.read_text('utf-8')
response = DEST / '874ce4fd-a36b-4883-aad4-6722f55f59f3.md'
receipt = json.loads(response.with_suffix('.json').read_text('utf-8'))
assert sha(response) == receipt['response_sha256']
opening = sha(OUT / 'ENTREGA_016_ABERTURA_operador.md')
review = f'''[REAL — revisão de resposta e integridade da evidência anterior; sem nova compilação]
# Kimi A6.B1c: reaproveitamento, sem duplicação

Abertura da ORDEM016: sha256 `{opening}`.

A resposta Kimi foi lida integralmente e comparada com a fonte local. Sua prova em prosa
(iterar a conservação, passar à subsequência n*s0 e usar continuidade/unicidade do limite)
é o argumento já implementado em `single_time_conserved_iff_factors`, linhas 712–738
de `{source.name}`. Reutilizar o lema existente; não acrescentar os cinco lemas propostos.

Integridade conferida nesta revisão: fonte `{sha(source)}`, log `{sha(log)}`.
Manifesto anterior registra rc=0, {unit['audit']['n_theorem_lemma_na_fonte']} lemas/teoremas
auditados, nenhuma declaração sem print axioms e nenhum axioma fora do trio permitido.
Isto é conferência dos artefatos da compilação anterior, não uma compilação nova.

Correções ao esboço recebido:
- O retorno do bicondicional introduz `fun h s x`, embora seu alvo só quantifique x;
  o tempo nessa direção é s0 fixado. O código existente já usa `intro hf x`.
- `conserved_iterate` declara s0 implícito, mas o esboço o passa como argumento explícito.
- Na iteração, n*s0+s0 inverte a ordem da composição exposta por iterate_succ_apply';
  usar s0+n*s0 como já faz a prova compilada, ou justificar a comutação.
- Nomes de API/unfolds foram apresentados como candidatos; não representam código compilado.
- A sugestão final `lake build` é recusada pela ordem. Não será executada.
- A amostra é única no TEMPO, mas a hipótese conserva a leitura para TODO x.
  Um único ponto amostrado não basta para o teorema.

O contraexemplo em s0=0 é correto para mostrar que esse tempo não pode ser incluído no
domínio s0>=0. Não demonstra que positividade seja a hipótese mais fraca em todos os reais:
para H limitado, T(-s0) é o inverso de T(s0), e conservação universal em tempo negativo
implica conservação no positivo por substituição x=T(-s0)y. Não se ampliou a assinatura.

Resultado: revisão independente do argumento, com falhas do rascunho identificadas.
Nenhum teorema adicional, recompilação, alteração de original ou movimento de gate.
Resposta recebida: `{sha(response)}`. Uso informado: {json.dumps(receipt['result_metadata'].get('usage'), ensure_ascii=False)}.
'''
review_path = DEST / 'REVISAO_KIMI_A6_B1c.md'
new(review_path, review)
evidence = dict(status='REAL_EXISTING_ARTIFACT_REUSED', source=str(source),
    source_sha256=sha(source), log=str(log), log_sha256=sha(log),
    previous_compile_rc=unit['receipt']['rc'], previous_audit=unit['audit']['auditoria'],
    response_sha256=sha(response), review_sha256=sha(review_path),
    new_compilation=False, new_external_execution=False, gate_changed=False)
new(DEST / 'REVISAO_KIMI_A6_B1c.json', json.dumps(evidence, ensure_ascii=False, indent=2))
new(OUT / 'ENTREGA_016_A6_revisao_Kimi_B1c.md', review)
ledger = OUT / 'LEDGER_016.jsonl'
old = ledger.read_bytes()
event = 'A6_KIMI_B1C_REVIEW_EXISTING_LEMMA_REUSED'
rows = [json.loads(s) for s in old.decode('utf-8-sig').splitlines() if s.strip()]
if not any(r.get('event') == event for r in rows):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(ledger.with_name(ledger.name + '.bak_' + stamp), old)
    row = dict(event=event, at=datetime.now(timezone.utc).isoformat(),
        execution_id=receipt['execution_id'], review=str(review_path),
        review_sha256=sha(review_path), new_external_execution=False)
    raw = old + (json.dumps(row, ensure_ascii=False) + '\n').encode()
    tmp = ledger.with_name(ledger.name + '.tmp_' + stamp)
    new(tmp, raw)
    tmp.replace(ledger)
print(json.dumps(evidence, ensure_ascii=False))
