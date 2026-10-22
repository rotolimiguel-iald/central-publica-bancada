"""Compare the received D2 proposal with the already executed independent harness."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
import mpmath as mp
HERE=Path(__file__).resolve().parent;A6=HERE.parent/'A6_EQUACAO_DA_VERDADE';D=A6/'D_harness'
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT';DEST=A6/'received_reviews/deepseek_d2_local';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    b=x.encode() if isinstance(x,str) else x
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(b)
    assert b and t.read_bytes()==b;t.replace(p)
def new(p,o):assert not p.exists();save(p,json.dumps(o,ensure_ascii=False,indent=2))
checks=[]
def check(n,v):assert v,n;checks.append(n)
response=A6/'received_reviews/14baed7e-08f4-4787-aeea-8538cc7dd075.md'
receipt=json.loads(response.with_suffix('.json').read_bytes())
check('provider_response_custody',sha(response)==receipt['response_sha256'])
manifest=json.loads((D/'independent_harness_manifest.json').read_bytes())
for item in manifest['artifacts']:check('custody_'+Path(item['path']).name,sha(Path(item['path']))==item['sha256'])
r=json.loads((D/'harness_T20_v2_results.json').read_bytes())
check('44checks9controls',len(r['checks'])==44 and all(x['ok'] for x in r['checks']) and len(r['controls'])==9 and all(x['detected'] for x in r['controls']))
check('260positive_intervals',len(r['intervals'])==260 and all(x['strict_positive'] for x in r['intervals']))
residual=max(Decimal(x['residual']) for x in r['matrix_trials'])
check('12complex_matrix_residuals',len(r['matrix_trials'])==12 and residual<=Decimal('1e-40'))
source=(D/'harness_T20_v2.py').read_text('utf-8-sig')
check('separate_interval_precision',"mp.iv.dps=CONFIG['interval_precision']" in source and r['configuration']['interval_precision']==60)
before=mp.iv.dps;mp.mp.dps=60;after=mp.iv.dps
check('deepseek_precision_assignment_does_not_set_iv',before==after and after!=60)
check('complex_residual_not_real_part_only','abs(Dvalue-(refsent-sent))' in source)
check('zero_coherence_case_exists',any(x['name']=='S6 degenerate zero-coherence states constant' and x['ok'] for x in r['checks']))
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
result=dict(at=now.isoformat(),statute='REAL_SOURCE_AND_RECEIPT_COMPARISON_NO_HARNESS_RERUN',checks=checks,
    checks_passed=len(checks),iv_precision_before=before,iv_precision_after_mp_assignment=after,
    existing_harness_counts=dict(exact_checks=44,negative_controls=9,intervals=260,matrix_trials=12),
    max_matrix_residual=str(residual),new_external_execution=False,gate_changed=False)
new(DEST/'results.json',result)
report=f'''[REAL — cotejo de fonte e recibos; DECLARADO — proposta DeepSeek, não executada]
# A6.D2 — aproveitamento do parecer recebido

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.

Resposta integral lida; execução{receipt['execution_id']}, SHA`{sha(response)}`.
O DeepSeek entregou desenho/código candidato, não resultado de teste.
Não substituí nem rodei novamente o D2 já executado na bancada.

O cotejo confirmou os sete artefatos do manifesto e as contagens atuais:
44checagens,9controles,260avaliações intervalares positivas e12comparações
de log matricial; resíduo máximo{residual}. Mantido o escopo da grade finita.

Diferenças úteis: o candidato ajusta mp.mp.dps=60, mas um processo local
confirmou que iv.dps continua{after}; o nosso D2 define iv.dps=60 explicitamente.
O candidato aceita sinal uniforme-1 e pede conferência pelo chamador;
o D2 executado exige estritamente intervalo positivo. Sua descrição diz
INCONCLUSIVE ao cruzar zero, enquanto o código candidato levanta AssertionError.
São limites do candidato, não regressões no D2 custodiado.

O candidato reutiliza autovalores simbólicos nos dois lados; nossa conferência
usa log matricial por autodecomposição sympy e entropia por eighe independente
em mpmath, com fase complexa(3+4i)/5 e módulo do resíduo complexo inteiro.
A operação sp.re do candidato não foi importada para nosso harness.

O pedido cita zero-coerência; o candidato deixa um argumento kappa sem
implementação. A receitaD2 não exige introduzir um parâmetro de gravidade
por esse nome. No D2 local k=|c|² e estados diagonais constantes são tratados
separadamente, incluindo p=1/2. Não confundir k com κ de horizonte.

O alerta contra declarar prova universal a partir de65pontos é correto e
já está no escopo do manifesto: o pedido exige≥64pontos, não cobertura de
todo contínuo. Nenhuma nova prova matemática, confirmação física ou mudança
de gate resulta deste cotejo. {len(checks)}verificações locais de recibo/fonte;
sem recompilação, sem nova execução remota e sem reabrir ramo já concluído.
'''
save(DEST/'REVISAO.md',report);save(OUT/'ENTREGA_016_A6_D2_revisao_DeepSeek.md',report)
files=[Path(__file__),response,response.with_suffix('.json'),D/'independent_harness_manifest.json',
       D/'harness_T20_v2.py',D/'harness_T20_v2_results.json',DEST/'results.json',DEST/'REVISAO.md']
new(DEST/'manifest.json',dict(opening_sha256=opening,artifacts=[dict(path=str(f),sha256=sha(f)) for f in files]))
ledger=OUT/'LEDGER_016.jsonl';event=dict(event='A6_DEEPSEEK_D2_LOCALLY_REVIEWED',at=now.isoformat(),
    provider='local',checks=len(checks),rc=0,new_external_execution=False,report_sha256=sha(DEST/'REVISAO.md'))
save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
p=HERE/'CONTINUIDADE.json';d=json.loads(p.read_bytes());d.update(at=now.isoformat(),deepseek_d2_local_review=str(DEST/'REVISAO.md'))
save(p,json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
