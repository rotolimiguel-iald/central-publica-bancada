from pathlib import Path
import datetime, hashlib, json, re

B = Path(__file__).resolve().parent
P = B.parent

def pin(p):
    p = Path(p)
    raw = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def put(p, value):
    raw = value.encode('utf-8')
    with p.open('xb') as f:
        f.write(raw)
    assert p.read_bytes() == raw

builds = {}
for name, count in [('vectors', 5), ('totality', 8)]:
    path = B / name / 'RECEIPT_R1.json'
    rec = json.loads(path.read_text(encoding='utf-8'))
    assert rec['passed'] and rec['exit_code'] == 0 and rec['axiom_count'] == count
    assert all(set(v) <= {'propext', 'Classical.choice', 'Quot.sound'} for v in rec['axioms'].values())
    for item in rec['dependencies_before_after']:
        assert pin(item['path'])['sha256'] == item['sha256']
    assert pin(rec['source']['path']) == rec['source']
    assert pin(rec['olean']['path']) == rec['olean']
    builds[name] = {'receipt': pin(path), **{k: rec[k] for k in ['start_utc', 'end_utc', 'seconds', 'exit_code', 'axiom_count', 'source', 'olean', 'olean_identical_to_accepted', 'log']}}

sources = [Path(builds[n]['source']['path']) for n in ['vectors', 'totality']]
anchors = []
for source in sources:
    for lineno, line in enumerate(source.read_text(encoding='utf-8').splitlines(), 1):
        if re.match(r'(?:theorem|def) (?:weight|component|exponential|coefficient|pureTensor_inner|scalar_series|coefficients_zero_of_orthogonal|pure_inner_zero_of_orthogonal|sector_eq_zero_of_pure_inner_zero|gamma_exponential|gammaJ_exponential)\b', line):
            anchors.append({'source': str(source), 'line': lineno, 'declaration': line})

mathlib = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib')
support = [
    (mathlib / 'Analysis/Analytic/Basic.lean', '1104-1127: hasFPowerSeriesAt_iff'),
    (mathlib / 'Analysis/Analytic/Uniqueness.lean', '90-103: HasFPowerSeriesAt.apply_eq_zero'),
    (P.parent / 'F1.REDE/fock_construction/attempts/20261013T223041_528152Z/BosonicSectors.lean', '32-34,93-119: actual tensor powers, completion and closed symmetric sectors'),
    (P.parent / 'F1.REDE/fock_construction/attempts/20261013T223456_898217Z/BosonicFock.lean', '17-27: existing direct sum F, vacuum and unit norm'),
]
checks = [
    {'id': 'normalization', 'verdict': 'PASSA', 'reason': 'O setor n usa x tensor n dividido por sqrt(n!), incluindo setor zero = 1. O quadrado da norma é ||x||^(2n)/n!, sem perda ou duplicação de fatoriais.'},
    {'id': 'membership_inner', 'verdict': 'PASSA', 'reason': 'Memℓp com p=2 deriva da somabilidade da série exponencial. A identidade inner(e(x),e(y))=exp(inner(x,y)) deriva das componentes e lp.hasSum_inner; a conjugação do fator real está consumida.'},
    {'id': 'totality', 'verdict': 'PASSA', 'reason': 'A hipótese temporária de ortogonalidade a todos e(x) implica uma série escalar identicamente zero para e(z*x). A unicidade analítica anula cada coeficiente; positividade dos pesos permite removê-los. O núcleo fechado do funcional inner(v_n,·) contém o span e seu fecho, logo v_n=0. O complemento ortogonal trivial prova totalidade. Não há hipótese de totalidade na conclusão nem substituição de F.'},
    {'id': 'second_quantization', 'verdict': 'PASSA', 'reason': 'Gamma(u)e(x)=e(ux) segue setor a setor das ações unitárias existentes. GammaJ(j,hj)e(x)=e(jx) usa a ação antilinear existente, j antiunitária involutiva e o fato de os pesos serem reais; não afirma que toda antiunitária seja involutiva.'},
    {'id': 'nonvacuity', 'verdict': 'PASSA', 'reason': 'exponential_zero identifica e(0) com o vacuum existente, cuja norma é 1. A família e o Fock são objetos concretos do tipo canônico, não campos postulados de um contrato.'},
]
report = {
    'unit': 'F1.FECHO_20261015', 'claim_event': 845,
    'reviewer': '/root/atrator_skeptic',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'verdict': 'PASSA_NO_ESCOPO_MATEMATICO', 'material_findings': [],
    'checks': checks, 'builds': builds, 'anchors': anchors,
    'support_read': [{**pin(p), 'lines': lines} for p, lines in support],
    'builder_delivery': pin(P / 'network_exponential/FINAL_EXPONENTIAL_RECEIPT_R1.json'),
    'scope': [
        'Revisão independente das duas fontes aceitas e recompilação uma vez de cada; a totalidade importa a base recompilada pelo revisor.',
        'Os vetores exponenciais são não normalizados: ||e(x)||²=exp(||x||²). A normalização adicional de estados coerentes não é parte desta tarefa.',
        'Deriva totalidade no Fock de setores fechados gerados por potências diagonais já construído; não reabre a equivalência desse modelo com outras apresentações do Fock.',
        'Não é revisão independente do lema GramTotalExtensionR4, que foi construído por este agente e é revisto pelo pai.',
        'Não verifica nesta entrega a construção de Weyl, relações CCR, KMS, BW, certificado físico ou confirmação experimental.',
        'Não foram alterados originais, memória, produção, kernel do Nós ou gate. Ato AUDITADA/FECHADA permanece da gerência.'
    ],
    'generator': pin(__file__),
}
put(B / 'REVISAO_EXPONENCIAIS_R1.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
lines = ['# Revisão independente dos vetores exponenciais e da totalidade', '',
    '[REAL] PASSA no escopo matemático das duas fontes aceitas. Nenhum achado material.', '',
    '| Fonte | EXIT | Segundos | Impressões de axiomas | .olean idêntico |',
    '|---|---:|---:|---:|---|']
for name, build in builds.items():
    lines.append(f"| {Path(build['source']['path']).name} | {build['exit_code']} | {build['seconds']:.6f} | {build['axiom_count']} | {build['olean_identical_to_accepted']} |")
lines += ['', 'As 13 impressões usam apenas propext, Classical.choice e Quot.sound; zero sorry. Logs incluem comando, toolchain Lean 4.31.0, LEAN_PATH literal, início, fim, segundos e exit. Dependências pinadas conferidas antes/depois; totalidade usa a base recompilada independentemente.', '']
for c in checks:
    lines += [f"- **{c['id']} — {c['verdict']}:** {c['reason']}"]
lines += ['', '## Alcance', ''] + ['- ' + s for s in report['scope']]
lines += ['', 'Hashes, linhas, fontes e recibos completos: REVISAO_EXPONENCIAIS_R1.json.']
put(B / 'REVISAO_EXPONENCIAIS_R1.md', '\n'.join(lines) + '\n')
print(json.dumps({'verdict': report['verdict'], 'json': pin(B / 'REVISAO_EXPONENCIAIS_R1.json'), 'md': pin(B / 'REVISAO_EXPONENCIAIS_R1.md')}, ensure_ascii=False))
