"""Exact algebraic controls and additive custody; no canonical imports or execution."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parent
REF = r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json'
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}
TASK = 'R14_VARIATIONAL_H3_SCOPE'

def new(name, value):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    with (ROOT / name).open('xb') as f:
        f.write((text + '\n').encode('utf-8'))
    return ROOT / name

def pin(path):
    p = Path(path).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def call(req, label, cli='mission_cli.py'):
    new(label + '_REQUEST.json', req)
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(Path(r'C:\IALD\MEMORIA_IALD') / cli)], input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding='utf-8')
    d = json.loads(p.stdout)
    new(label + '_RESULT.json', {'exit_code': p.returncode, 'response': d, 'stderr': p.stderr})
    if p.returncode or not d.get('ok'):
        raise RuntimeError(d)
    return d['result']

def project(label):
    return call({'operation': 'project', 'reference': REF, 'max_chars': 650000}, label)

def mutate(op, label, **kw):
    p = project(label + '_SYNC')
    return call({'operation': op, 'reference': REF, 'actor': ACTOR, 'expected_revision': p['receipt']['revision'], 'projection_sha256': p['projection_sha256'], 'event_id': 'r82-' + label, **kw}, label)

def initialize():
    new('ORIGEM.txt', 'Continuidade autorizada pelo operador: Prossiga. Escopo R82: seguir R81 para a acao gravitacional ja escrita, reaproveitando o levantamento R58. OH adiado. A leitura de identidade nao sera promovida a estacionariedade sem demonstracao. Nenhum dado observado, provedor, kernel, um.py ou gate sera alterado. Reivindicacao quadro 989.')
    mutate('extend', 'EXTEND', requirements=[{'id': TASK, 'criterion': 'Derivar analiticamente a contribuicao nao minimal da acao escrita, explicitar sua projecao nula e o contrato com H3/fonte total, com controles exatos e revisao independente. Nao equivale a construir estacionariedade nem H3 universal.', 'depends_on': []}], reason='Continuidade humana autorizada; resultado delimitado da rota variacional apos levantamento R58/R81.', sources=[pin(ROOT / 'ORIGEM.txt')])
    mutate('claim', 'CLAIM', task_id=TASK, lease_seconds=7200)
    print('Initialized', TASK)

def controls():
    # These are scalar contractions at a point, not solutions of field equations.
    cases = []
    for xi in [Q(0), Q(1,6), Q(-1,7)]:
        for u in [Q(0), Q(1,3), Q(2)]:
            for h in [Q(0), Q(2,5)]:
                for r in [Q(0), Q(3,2)]:
                    k2 = Q(5,4)
                    f = 1 / (2*k2) + xi*u
                    t = 2*f*r - 2*xi*h
                    total = t - 2*xi*u*r + 2*xi*h
                    assert r == k2*total
                    assert (r-k2*t) == 2*k2*xi*(h-u*r)
                    cases.append({'xi':str(xi),'u':str(u),'h':str(h),'ricci':str(r),'minimal_source':str(t),'effective_source':str(total)})
    # Omitting the curvature and Hessian terms gives a nonzero null residual.
    xi,u,h,r,k2 = Q(1,6),Q(1),Q(0),Q(1),Q(1)
    t = (1+2*k2*xi*u)*r/k2-2*xi*h
    assert t == Q(4,3) and r-k2*t == Q(-1,3)
    # Calibration can match without xi=0 when h=u*r, a nontrivial cancellation.
    h=u*r
    t=(1+2*k2*xi*u)*r/k2-2*xi*h
    assert r == k2*t
    new('EXACT_CONTROLS_R82.json', {'status':'PASS_ALGEBRA_ONLY','rational_cases':len(cases),'cases':cases,'omission_control':{'ricci':'1','minimal_source':'4/3','residual':'-1/3'},'cancellation_control':'h=u*ricci; residual=0','field_solutions_constructed':False,'functional_variation_tested_by_script':False,'H3_universal_proved':False})
    base = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
    names = ['ScalarMatterDensityVariation.lean','MetricRicciVariation.lean','MetricEinsteinVariation.lean','JointCoherentGravitation.lean','GeneralSourceEinsteinBridge.lean','UnifiedRecordedPreparation.lean','GravitationalResponseRecord.lean','TheNonMinimalCoupling.lean','OpticalConstructedHeat.lean']
    sources = [base / n for n in names] + [Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py'), Path(r'C:\IALD\papers_latex\graviton_paper\graviton_part2_intro.tex')]
    new('SOURCE_PINS_R82.json', {'sources':[pin(p) for p in sources], 'nos_vivo_query':{'unit':'F1.FECHO_20261015','exit_code':1,'message':'unidade nao esta no grafo; indice nao reconstruido'},'reuse':'R58 survey and R81, plus direct source inspection; not a whole-computer absence assertion'})
    print(f'{len(cases)} exact rational controls and two targeted controls passed')

if __name__ == '__main__':
    {'init': initialize, 'controls': controls}[sys.argv[1]]()
