from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, subprocess, sys

root=Path(__file__).resolve().parents[1]
folder=root/'A2'
out=root.parent/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,b):
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.rename(p)
def append(p,b):
    old=p.read_bytes()
    create(p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')),old)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(old+b)
    assert t.read_bytes()==old+b
    t.replace(p)
passed=[('BoundedTransformCore_v2.lean','bounded_core_02'),
        ('BoundedTransformKernel.lean','bounded_kernel_01'),
        ('BoundedTransformGap.lean','bounded_gap_01'),
        ('BoundedTransformFinite_v2.lean','bounded_finite_02')]
args=[sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py')]
records=[]
for file,label in passed:
    source=folder/file; log=folder/(label+'.log'); rp=folder/(label+'.json')
    r=json.loads(rp.read_bytes())
    assert r['rc']==0 and not r['newer_kernel_files'] and not r['scan_errors']
    assert r['source_sha256']==sha(source) and r['log_sha256']==sha(log)
    args.extend([str(source),str(log)])
    records.append({'source':file,'source_sha256':sha(source),'log':log.name,
                    'log_sha256':sha(log),'receipt':rp.name,'receipt_sha256':sha(rp)})
audit=subprocess.run(args,capture_output=True)
assert audit.returncode==0,audit.stdout+audit.stderr
create(folder/'bounded_transform_axioms.json',audit.stdout)
audits=json.loads(audit.stdout)
count=sum(a['n_theorem_lemma_na_fonte'] for a in audits)
attempts=[]
for pattern in ['bounded_core_0*.json','bounded_kernel_0*.json','bounded_gap_0*.json','bounded_finite_0*.json']:
    attempts.extend(json.loads(p.read_bytes()) for p in sorted(folder.glob(pattern)))
wall=sum(r['wall_seconds'] for r in attempts)
cpu=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in attempts)
bench=(now-min(datetime.fromisoformat(r['utc']) for r in attempts)).total_seconds()
manifest={'utc':now.isoformat(),'status':'ISOLATED_LEAN_AUDITED','declarations':count,
    'artifacts':records,'audit_sha256':sha(folder/'bounded_transform_axioms.json'),
    'attempts':len(attempts),'compile_wall_seconds':wall,'compile_cpu_seconds':cpu,
    'bench_elapsed_seconds':bench,'scope':'All bounded complex Hilbert-space operators; finite matrices via canonical star algebra equivalence. No microscopic or unbounded identification.',
    'proven':['actual CFC construction','kernel equality','contraction','gap lower bound','attainment transport','finite matrix realization'],
    'pending':['A-2.5.c unbounded LinearPMap','physical H_min identification reserved to operator']}
create(folder/'bounded_transform_manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
latest={}
for line in (out/'LEDGER_016.jsonl').read_text(encoding='utf-8').splitlines():
    if line:
        r=json.loads(line); key=r.get('request_id')
        if key: latest[key]={**latest.get(key,{}),**r}
cost=sum(Decimal(str(r.get('custo_usd',r.get('cost_usd')))) for r in latest.values() if r.get('custo_usd',r.get('cost_usd')) is not None)
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — {count} declarações compiladas e auditadas isoladamente]

# A-2.5.a e A-2.5.b — transformada limitada

Data UTC: {now.isoformat()}. ABERTURA sha256: `{opening}`.

Construído por cálculo funcional contínuo, para todo operador limitado D em Hilbert complexo:
`S = sqrt(I+D*D)`, `R=S^(-1)`, `b(D)=D R = D (I+D*D)^(-1/2)`.
Provadas a positividade estrita, a invertibilidade de S e a identidade
`||x||² = ||Rx||² + ||b(D)x||²`.

Conclusões compiladas:

- `ker b(D) = ker D`; S e R fixam pontualmente esse núcleo e preservam seu ortogonal.
- `||b(D)x|| ≤ ||x||`.
- Se `γ≥0` e `γ||y|| ≤ ||Dy||` no complemento ortogonal do núcleo, então
  `γ/sqrt(1+γ²) ||x|| ≤ ||b(D)x||` no mesmo complemento.
- Se um vetor atinge a razão γ para D, Sx atinge a razão transformada para b(D).
  Um limite inferior não é anunciado como mínimo espectral atingido sem essa hipótese.
- `finiteTransform` é uma matriz real de código (Matrix n n ℂ), obtida pela equivalência
  canônica star-algébrica com os operadores euclidianos. A fórmula, o núcleo e o gap
  foram transportados por essa equivalência. A prova comum atende a face finita e
  também ao operador limitado geral, sem duplicar argumentos.

Consulta prévia: V354BoundedPolar.lean já tem a decomposição polar e propriedades do
valor absoluto. Seu boundedAbsolute_ker é privado; a nova prova de ker b(D) usa a raiz
de I+D*D, sua inversa efetiva e fixação do núcleo, não um pressuposto de igualdade de núcleos.

Validação: {count} theorem/lemma cobertos por #print axioms; rc 0; apenas o trio
propext/Classical.choice/Quot.sound; nenhum sorry/axioma novo. Zero alteração detectada
no kernel e zero erro de leitura nos quatro recibos aprovados. Warnings de nomes antigos
de APIs e variável implícita preservados; não são falhas matemáticas.
Comando: `python -X utf8 -B A0/compile_isolated_v2.py <kernel> <fonte> <rótulo> <A2>`.
Tentativas falhas preservadas: import da ordem de operadores ausente/argumentos da
inversa; parâmetros implícitos da equivalência matricial. Nenhum lema excedeu seis ciclos.

Custódia: `{folder/'bounded_transform_manifest.json'}`.
Auditoria: `{folder/'bounded_transform_axioms.json'}`.
'''
for r in records:
    report+=f"\n- `{r['source']}`: `{r['source_sha256']}`; log `{r['log']}`: `{r['log_sha256']}`.\n"
report+=f'''
Máquina: {wall:.3f} s parede, {cpu:.3f} s CPU em {len(attempts)} tentativas.
Bancada decorrida: {bench:.3f} s. Nenhuma chamada externa nova para esta construção;
crítica Kimi anterior recebida e contabilizada separadamente, sem duplicação.
Gasto monetário conhecido agregado por request_id: US$ {cost}; valores desconhecidos
continuam desconhecidos, inclusive o custo monetário de Kimi.

Não move o gate nem identifica D com o Dirac microscópico da teoria. Essa identificação
nunca foi escolhida pela bancada. A-2.5.a/b: PAGO no escopo matemático acima.
Próximo ramo A-2.5.c: operador ilimitado LinearPMap, com domínio explícito; não transferir
automaticamente a prova de operador limitado. Controle adversarial A-2.3: revisão recebida,
mas a direção reversa domínio/faixa requerida pelos contraexemplos permanece pendente.
'''
create(out/'ENTREGA_016_MEDIDA_A2_5ab_transformada_limitada.md',report.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} — A-2.5.a/b PAGO: transformada limitada CFC, núcleo, contração, gap e face matricial; {count} declarações isoladas auditadas. Bancada {bench/3600:.6f} h; máquina parede {wall/3600:.6f} h, CPU {cpu/3600:.6f} h, contabilizados uma vez para a prova comum. Gasto conhecido US$ {cost}; A-2.5.c e identificação física pendentes.\n'.encode())
print(json.dumps(manifest,ensure_ascii=False))
