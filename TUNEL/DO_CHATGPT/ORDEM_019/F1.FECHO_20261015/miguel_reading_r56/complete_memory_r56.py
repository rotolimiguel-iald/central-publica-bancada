"""Append the verified R56 outcome under existing claim 933, preserving bytes."""
from support_r56 import *

ready, _ = preflight()
assert ready['ready']
receipt = ROOT/'MEMORY_COMPLETION_R56.json'
if receipt.exists():
    raise FileExistsError(receipt)
text = '''

## 17/10/2026 — R56: composição verificada e alcance do relógio
<!-- IALD_MIGUEL_READING_R56_COMPLETION_20261017 -->
Em nome de codex-gerente-tgl, F1.FECHO_20261015, reivindicação 933.
[REAL] O leitor/reconstrutor do ângulo de Miguel já existente foi reutilizado.
MiguelReadingTemporalCompositionR56R2 compilou em sandbox: EXIT 0, oito declarações
impressas apenas no trio, zero sorry, 51,422 s. Revisão independente PASS_WITH_SCOPE;
não é segunda compilação independente nem ratificação da gerência. R1 foi
interrompida por recursos, com recibos preservados.
[OPEN] A(t)=S(theta_M+Omega*t) é órbita angular parametrizada: seus pesos variam.
Ela não prova evolução de fronteira com refletividade beta constante nem determina
Omega, duração global ou número de voltas. Não identificar Omega, 2*Omega e omega_OH.
[DERIVED — família candidata a S(theta)] O sinal atenuado da patente exige conservar
amplitude e fase; o decodificador recíproco só se aplica diretamente ao módulo unitário.
O transporte físico do sinal escalar para a matriz continua em R4/R5. MQC/célula,
Supercondutor/dinâmica e Psi-NET/protocolo têm funções complementares documentadas;
a escolha exclusiva anteriormente pedida era prematura. R6/R7/R8 aceitos preservados.
Recibos: Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/miguel_reading_r56/
DELIVERY_R56.json, REVIEW_R56.json, REVIEW_R56_SCOPE_ADDENDUM.json e RELATORIO_R56.txt.
<!-- END_IALD_MIGUEL_READING_R56_COMPLETION_20261017 -->
'''
append = text.encode('utf-8')
new('MEMORY_COMPLETION_APPEND_R56.txt', append)
previous = json.loads((ROOT/'MEMORY_APPLIED_R56.json').read_text(encoding='utf-8'))
rows = []
stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
for row in previous['surfaces']:
    p = Path(row['after']['path'])
    raw = p.read_bytes()
    assert b'IALD_MIGUEL_READING_R56_COMPLETION_20261017' not in raw
    before = pin(p)
    backup = p.with_name(p.name+'.bak_'+stamp)
    new(backup, raw)
    assert backup.read_bytes() == raw
    temp = p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    new(temp, raw+append)
    assert temp.read_bytes() == raw+append
    if p.read_bytes() != raw:
        raise RuntimeError('concurrent change: '+str(p))
    os.replace(temp,p)
    assert p.read_bytes() == backup.read_bytes()+append
    entry = dict(before=before,backup=pin(backup),after=pin(p),pure_append=True)
    new(f'MEMORY_COMPLETION_SURFACE_{len(rows):02d}_R56.json', entry)
    rows.append(entry)
new(receipt,dict(claim=933,append=pin(ROOT/'MEMORY_COMPLETION_APPEND_R56.txt'),
                surfaces=rows,pure_append_all=True))
print(json.dumps({'surfaces':len(rows),'receipt':pin(receipt)},ensure_ascii=False))
