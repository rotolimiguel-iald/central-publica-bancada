"""Record the measured resource failure; no mathematical verdict is inferred."""
from pathlib import Path
import datetime
import hashlib
import json

root = Path(__file__).resolve().parents[1]
out = root.parent / 'TUNEL' / 'DO_CHATGPT'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p, text):
    assert not p.exists(), p
    raw = text.encode('utf-8')
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw and len(raw) > 0
    tmp.rename(p)

labels = ['reproduction_01', 'reproduction_02_single_worker']
records = [(root/'A1'/'v3'/(label+'.json')) for label in labels]
data = [json.loads(p.read_text()) for p in records]
opening = out/'ENTREGA_016_ABERTURA_operador.md'
wall = sum(d['wall_seconds'] for d in data)
cpu = sum(d['cpu_user_seconds']+d['cpu_kernel_seconds'] for d in data)
lines = [
    '[REAL] A-1.a — reprodução NÃO PAGA: duas falhas de recurso, sem julgamento da validade do contrato.',
    '', 'Abertura SHA256: '+sha(opening),
    '', 'Arquivo: cópia byte a byte de v3/ContratoQG.lean (contrato v2 na árvore de dependências).',
    'Fonte SHA256: '+sha(root/'A1/v3/ContratoQG.lean'),
    '', 'A primeira execução usou os trabalhadores padrão; a segunda usou -j1. Ambas mantiveram o limite de 8 GiB por processo e terminaram com std::bad_alloc. Nenhuma produziu a reprodução esperada de rc 0. O rc de recurso não é o rc 1 no campo nomeado exigido para os probes negativos.',
    '', 'Não haverá terceira repetição do mesmo contrato nesta rodada. Não foi alterado o código da prova, o limite, o kernel nem qualquer olean canônico.',
    '', f'Tempo de máquina Lean: {wall:.6f} s de parede; CPU agregada {cpu:.6f} s. Horas de compilação: {wall/3600:.9f}; máquina pesada Parte B: 0 h.',
    '', 'O primeiro comando e sua repetição estão integralmente registrados nos recibos abaixo; cwd = kernel canônico. Pico medido é memória comprometida de processo Windows Job, não RSS. Varredura de arquivos canônicos posteriores ao marcador: zero em ambas, sem erro de leitura.',
]
for p,d in zip(records,data):
    log=p.with_suffix('.log')
    lines += ['', str(p), 'Recibo SHA256: '+sha(p), 'Log SHA256: '+sha(log),
              f"rc={d['rc']}; pico={d['peak_process_committed_bytes']} bytes; parede={d['wall_seconds']} s.",
              'Comando (vetor de argumentos): '+json.dumps(d['command'],ensure_ascii=False)]
lines += ['', '[OPEN] Reprodução dependente: W5, v3, v3.1, teoremas, paredes e probes não recebem rc inferido. Os resultados da gerência permanecem DECLARADOS para esta reprodução, não passam a REAL por referência.',
          '', 'Próximo ramo obrigatório: A-1.b. Controles algébricos com dependências mínimas podem ser medidos independentemente; não substituem a compilação contra ContratoH2/ContratoH3 v3.1. A extensão A-1.c deve conservar essa distinção. Nenhuma fronteira nem gate mudou.', '']
target=out/'ENTREGA_016_MEDIDA_A1a_memoria.md'
create(target,'\n'.join(lines))
print(json.dumps({'path':str(target),'sha256':sha(target),'wall_seconds':wall,'cpu_seconds':cpu}))
