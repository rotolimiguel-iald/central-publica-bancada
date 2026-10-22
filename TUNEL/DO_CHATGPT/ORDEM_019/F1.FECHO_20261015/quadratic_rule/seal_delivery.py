"""Seal the first passing quadratic-rule build with source-derived hashes."""
from pathlib import Path
import datetime
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
REUSE = BASE.parent.parent / 'F1.TEMPO.V394'

def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def write_new(path, data):
    with path.open('xb') as f:
        f.write(data)

passing = []
for receipt_path in sorted((BASE/'attempts').glob('*/BUILD_RECEIPT.json')):
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    if receipt['passed']:
        passing.append((receipt_path, receipt))
if len(passing) != 1:
    raise RuntimeError(f'Expected one reviewed passing build, got {len(passing)}')
receipt_path, receipt = passing[0]
snapshot = Path(receipt['source']['path'])
assert pin(snapshot) == receipt['source']
assert snapshot.read_bytes() == (BASE/'src/TGLExt/RuleQuadraticResidual.lean').read_bytes()
source = snapshot.read_text(encoding='utf-8')
assert not re.search(r'\b(sorry|admit)\b|^\s*axiom\s', source, re.M)
expected = re.findall(r'^#print axioms (\S+)', source, re.M)
assert len(expected) == 18 and set(expected) == set(receipt['axiom_reports'])
assert all(set(v) <= {'propext','Classical.choice','Quot.sound'} for v in receipt['axiom_reports'].values())
final_source = BASE/'RuleQuadraticResidual.lean'
write_new(final_source, snapshot.read_bytes())
stdout = Path(receipt['stdout']['path'])
write_new(BASE/'AXIOMAS_R1.txt', stdout.read_bytes())
readme = '''# Regra quadrática — F1.FECHO_20261015

[REAL — compilado] `RuleQuadraticResidual.lean`: 18 declarações com axiomas somente
propext, Classical.choice e Quot.sound; EXIT 0; nenhum sorry/admit/axioma novo.
Reivindicação delegada 845, codex-gerente-tgl. A aceitação independente cabe à gerência.

## Forma e reaproveitamento

`residual A X := TGLExt.purityR (Eg X - A)`, em M2. `purityR` é a soma dos módulos
quadrados das entradas, isto é, Frobenius², não a norma matricial padrão implícita.
Reutiliza PageInformation.purityR e purityR_eq, Bicommutant.frob_self_eq_zero_iff,
RuleTruthContract.Admissible, TimeGravitonMatrix.Eg e TimeGravitonFlow.reading_flow.
Não refaz a rede, a leitura ou o fluxo. A consulta da unidade nova ao Nós Vivo devolveu
"unidade não está no grafo"; foram abertas diretamente as fontes já levantadas.

## Resultados

- PASSA: residual A X ≥ 0; residual A X = 0 sse Eg X = A, a regra já tipada.
- PASSA: residual A (T_t X) = residual A X, para o mesmo alvo A; continuidade e derivada zero.
- PASSA: numa inscrição fixa A, seu próprio resíduo é zero; entre inscrições, zero sse igualdade.
- PASSA: se Eg A ≠ A, o alvo é impossível e o resíduo é estritamente positivo para todo X.
- PASSA: o alvo A=I/2 é fixo e aceita transportedRho, embora a densidade bruta seja diferente de A.
- PASSA: a mesma transportedRho tem residual P+ = 1/2, e continua rejeitada em todo tempo.
- PASSA: inhabited_and_discriminating exibe os testemunhos anteriores simultaneamente.

## Hipóteses e alcance

As identidades de resíduo valem para parâmetros reais arbitrários do fluxo algébrico;
o setor de canal físico usa taxa e tempo não negativos, como no contrato já construído.
O alvo é argumento fixado antes da avaliação, não é redefinido como Eg(X) para cada entrada.
A invariância não é hipótese: decorre de reading_flow. Ela não mede a aproximação do
estado bruto ao alvo, e não é um escore decrescente de progresso nem um relógio.
O alvo realizável pode ser carregado como `RuleContinuousMotor.Inscription Eg`.
O caso de alvo impossível não é universalmente vazio: Eg(rootPlus)=0 e rootPlus≠0
já estão provados na base reutilizada; não se afirma que esse rootPlus seja densidade.
Esta pedra prova o contrato no M2 especificado, sem declarar extensão global 4D,
confirmação natural, instalação no original, escrita de memória ou mudança de gate.

## Reprodução

O recibo de build contém comando, início/fim UTC, duração, toolchain e LEAN_PATH literal.
Cada execução de build_quadratic.py cria snapshot, logs e .olean novos numa pasta própria.
As bibliotecas já copiadas de formal_verified e os packages canônicos são somente lidos.
O fonte de entrega é byte a byte o snapshot compilado. Não houve tentativa falha nesta entrega.
'''
write_new(BASE/'LEITURA_R1.md',readme.encode('utf-8'))
dependencies = [
    REUSE/'formal_verified/src/TGLExt/TimeGravitonMatrix.lean',
    REUSE/'formal_verified/src/TGLExt/TimeGravitonFlow.lean',
    REUSE/'candidate_r2/tgl_kernel/TGLExt/PageInformation.lean',
    REUSE/'candidate_r2/tgl_kernel/TGLExt/Bicommutant.lean',
    REUSE/'candidate_r2/tgl_kernel/TGLExt/LeftRight.lean',
    REUSE/'candidate_r2/tgl_kernel/TGLExt/RuleTruthContract.lean',
    REUSE/'candidate_r2/tgl_kernel/TGLExt/TheRuleInTheContinuousMotor.lean',
]
delivery = {
    'unit':'F1.FECHO_20261015','claim_event':845,
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'ENTREGA_TECNICA_PASSA_AGUARDA_REVISAO_INDEPENDENTE',
    'build':pin(receipt_path),'exit_code':receipt['exit_code'],
    'declarations':len(expected),'axioms_allowed':['propext','Classical.choice','Quot.sound'],
    'source_without_sorry_admit_or_new_axiom':True,
    'results':{'zero_iff_rule':'PASSA','invariance':'PASSA','time_continuity':'PASSA',
       'inscription_zero_iff_equal':'PASSA','impossible_anchor':'PASSA',
       'concrete_accepted_anchor':'PASSA','concrete_changed_anchor_half':'PASSA',
       'concrete_nonvacuity':'PASSA'},
    'scope':'M2 quadratic residual of the existing Eg reading, fixed target and existing flow; not raw-state distance.',
    'dependencies':[pin(p) for p in dependencies],
    'artifacts':[pin(p) for p in [final_source,BASE/'AXIOMAS_R1.txt',BASE/'LEITURA_R1.md',
       BASE/'build_quadratic.py',BASE/'seal_delivery.py',receipt_path.parent/'BUILD.log',
       receipt_path.parent/'STDOUT.log',receipt_path.parent/'STDERR.log',Path(receipt['olean']['path'])]],
    'prior_attempts':[],
    'originals_memory_production_gate_touched':False,
}
payload=json.dumps(delivery,ensure_ascii=False,indent=2).encode('utf-8')+b'\n'
write_new(BASE/'DELIVERY_R1.json',payload)
print(json.dumps({'path':str(BASE/'DELIVERY_R1.json'),'sha256':hashlib.sha256(payload).hexdigest(),
    'source_sha256':pin(final_source)['sha256'],'declarations':len(expected)},ensure_ascii=False))
