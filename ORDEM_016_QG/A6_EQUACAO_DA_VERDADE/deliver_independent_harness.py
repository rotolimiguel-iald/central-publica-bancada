from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json
HERE=Path(__file__).resolve().parent
D=HERE/'D_harness';OUT=HERE.parent.parent/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    raw=v if isinstance(v,bytes) else (v.encode() if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2).encode())
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(raw);assert tmp.read_bytes()==raw and raw;tmp.replace(p)
result=json.loads((D/'harness_T20_v2_results.json').read_bytes())
first=json.loads((D/'harness_T20_results.json').read_bytes())
assert result['status']=='PASS' and all(c['ok'] for c in result['checks'])
assert len(result['controls'])==9 and all(c['detected'] for c in result['controls'])
assert len(result['intervals'])==260 and all(c['strict_positive'] for c in result['intervals'])
assert len(result['matrix_trials'])==12 and all(c['ok'] for c in result['matrix_trials'])
assert result['source_sha256']==sha(D/'harness_T20_v2.py') and result['plan_sha256']==sha(D/'D2_PRE_REGISTRO.json')
assert result['configuration']['seed'] not in [20260923,7]
names=[c['name'] for c in result['checks']]
for needle in ['Hilbert-Schmidt','superoperator exponential','cross entropy','interval derivative','matrix logarithm']:
    assert any(needle in n for n in names),needle
maxres=max(Decimal(x['residual']) for x in result['matrix_trials'])
assert maxres<=Decimal(result['configuration']['residual_tolerance'])
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md');now=datetime.now(timezone.utc)
manifest=dict(status='REAL_D2_SCOPED',at=now.isoformat(),opening_sha256=opening,
 artifacts=[dict(path=str(D/name),sha256=sha(D/name)) for name in
            ['D2_PRE_REGISTRO.json','harness_T20.py','harness_T20.log','harness_T20_results.json',
             'harness_T20_v2.py','harness_T20_v2.log','harness_T20_v2_results.json']],
 checks=len(result['checks']),controls=len(result['controls']),interval_evaluations=len(result['intervals']),
 matrix_trials=len(result['matrix_trials']),max_matrix_residual=str(maxres),
 versions=result['versions'],seed=result['configuration']['seed'],
 total_wall_seconds=first['wall_seconds']+result['wall_seconds'],total_cpu_seconds=first['cpu_seconds']+result['cpu_seconds'],
 scope='Exact prescribed finite examples; finite interval grid and 50-digit comparisons; not a universal matrix theorem or a physical model.',
 gate_changed=False)
save(D/'independent_harness_manifest.json',manifest)
save(OUT/'ENTREGA_016_A6_D2_harness_independente.md',f'''[REAL — harness independente executado; DERIVED — identidades exatas dos exemplos]

# A6.D2 — duas verificações independentes na bancada

Abertura SHA256: `{opening}`.

Resultado: {manifest['checks']}/{manifest['checks']} grupos de checks, 9/9 controles negativos, 260 avaliações por aritmética de intervalos e 12 comparações de entropia relativa com logaritmo matricial. Semente {manifest['seed']} pré-registrada antes da geração. A fonte não importa V1 nem lê seus resultados.

No primeiro exemplo racional em dimensão 5, os projetores espectrais foram calculados como polinômios de Lagrange em H, em vez de usar diretamente os vetores para construí-los. O fluxo foi conferido pela EDO, condição inicial, semigrupo, Taylor até ordem 12, preservação da leitura e limite. O segundo exemplo usa matrizes racionais aleatórias; sua inércia (três modos positivos/dois nulos) decorre da congruência com a matriz 3×3 positiva definida, cujos menores principais exatos estão registrados. Esse segundo exemplo confere a projeção da série truncada até ordem 15; não se apresenta essa truncagem como igualdade da exponencial inteira.

Foram verificados dois leitores contínuos, amostragem em tempo positivo, 48 pares racionais (com resultados verdadeiros e falsos), núcleo/complemento, derivadas, perfil e nove controles negativos. O superoperador do qubit é explicitamente uma projeção ortogonal Hilbert–Schmidt, H=id−E=D†D, com exponencial exata E+exp(−s)(id−E).

Entropia: quatro pares (p,|c|²), incluindo p=1/2 e dois casos a 99% da fronteira de positividade, cada um com 65 pontos em s∈[0,10]. mpmath.iv a 60 dígitos confirmou 0<r<1 e limite inferior estritamente positivo da derivada em todos os 260 pontos. O caso de coerência zero é tratado separadamente como estado constante. A grade não prova positividade universal; essa é a proposição escalar Lean já auditada com suas hipóteses.

O logaritmo matricial foi construído por autodecomposição exata SymPy de matrizes hermitianas com coerência complexa; Tr(ρ(logρ−logσ)) foi comparado a S(σ)−S(ρ), cujo S(ρ) foi avaliado com autovalores calculados independentemente por mpmath.eighe. Precisão 50 dígitos, tolerância 10⁻⁴⁰, maior resíduo {maxres}. Não foi reutilizada a fórmula da diferença entrópica para calcular ambos os lados.

Duas execuções preservadas: a primeira já passou; a v2 acrescenta os três checks explícitos de Hilbert–Schmidt/exponencial/entropia cruzada exigidos por B3c. Tempo total {manifest['total_wall_seconds']:.6f}s parede e {manifest['total_cpu_seconds']:.6f}s CPU. D1 permanece separado, 51/51+9/9. D3 “22/22+5” continua NÃO_VERIFICÁVEL.

Manifesto: `{D/'independent_harness_manifest.json'}`. Não move gate, não mede σ, não altera originais. Próximo: ficha E.
''')
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes();marker='A6_D2_INDEPENDENT_HARNESS_20260924'
events=[json.loads(l) for l in old.decode('utf-8-sig').splitlines() if l.strip()]
costs={}
for e in events:
    c=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if c is not None and key:costs[key]=Decimal(str(c))
cost=sum(costs.values(),Decimal(0))
if marker.encode() not in old:
    entry=dict(event=marker,at=now.isoformat(),manifest=str(D/'independent_harness_manifest.json'),manifest_sha256=sha(D/'independent_harness_manifest.json'),external_execution=False)
    save(ledger,old+(json.dumps(entry,ensure_ascii=False)+'\n').encode())
progress=OUT/'ENTREGA_016_PROGRESSO.md';raw=progress.read_bytes()
if marker.encode() not in raw:
    save(progress,raw+f'\n- {now.isoformat()} — A6.D2 PAGO no escopo: 44 checks, 9 controles, 260 intervalos, 12 logs matriciais; residual máximo {maxres}. Máquina {manifest["total_wall_seconds"]/3600:.6f}h parede/{manifest["total_cpu_seconds"]/3600:.6f}h CPU; bancada não exclusiva. Estimativas externas US${cost}, incompletas. Abertura {opening}. D3 NÃO_VERIFICÁVEL. Não move gate; próximo E. [{marker}]\n'.encode())
print(json.dumps(dict(status=manifest['status'],checks=manifest['checks'],max_residual=str(maxres))))
