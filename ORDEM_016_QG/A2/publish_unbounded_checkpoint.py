from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, subprocess, sys

folder=Path(__file__).resolve().parent
root=folder.parent
out=root.parent/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,b):
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(b)
    assert t.read_bytes()==b
    t.rename(p)
def append(p,b):
    old=p.read_bytes()
    create(p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')),old)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(old+b)
    assert t.read_bytes()==old+b
    t.replace(p)
passed=[('UnboundedGraphTransform_v2.lean','unbounded_graph_02'),
 ('ResolventBoundedTransform_v3.lean','resolvent_bounded_03'),
 ('ContinuousBoundedTransform.lean','continuous_bounded_01'),
 ('NormalizedGraphContract_v2.lean','normalized_graph_02')]
args=[sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py')]
records=[]
for filename,label in passed:
    src=folder/filename; log=folder/(label+'.log'); rp=folder/(label+'.json')
    r=json.loads(rp.read_bytes())
    assert r['rc']==0 and not r['newer_kernel_files'] and not r['scan_errors']
    assert r['source_sha256']==sha(src) and r['log_sha256']==sha(log)
    args.extend([str(src),str(log)])
    records.append(dict(source=filename,source_sha256=sha(src),log=log.name,
        log_sha256=sha(log),receipt=rp.name,receipt_sha256=sha(rp)))
audit=subprocess.run(args,capture_output=True)
assert audit.returncode==0,audit.stdout+audit.stderr
create(folder/'unbounded_transform_axioms.json',audit.stdout)
count=sum(x['n_theorem_lemma_na_fonte'] for x in json.loads(audit.stdout))
attempts=[]
for pattern in ['unbounded_graph_0*.json','resolvent_bounded_0*.json',
                'continuous_bounded_0*.json','normalized_graph_0*.json']:
    attempts.extend(json.loads(p.read_bytes()) for p in sorted(folder.glob(pattern)))
wall=sum(r['wall_seconds'] for r in attempts)
cpu=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in attempts)
bench=(now-min(datetime.fromisoformat(r['utc']) for r in attempts)).total_seconds()
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
latest={}
for line in (out/'LEDGER_016.jsonl').read_text(encoding='utf-8').splitlines():
    if line:
        r=json.loads(line); key=r.get('request_id')
        if key: latest[key]={**latest.get(key,{}),**r}
cost=sum(Decimal(str(r.get('custo_usd',r.get('cost_usd')))) for r in latest.values()
    if r.get('custo_usd',r.get('cost_usd')) is not None)
incoming=sorted((root.parent/'TUNEL/PARA_CHATGPT').glob('*.md'),key=lambda p:p.stat().st_mtime,reverse=True)[:6]
manifest=dict(utc=now.isoformat(),status='PARTIAL_ISOLATED_LEAN_AUDITED',
    branch='A-2.5.c',declarations=count,artifacts=records,
    opening_sha256=opening,audit_sha256=sha(folder/'unbounded_transform_axioms.json'),
    attempts=len(attempts),compile_wall_seconds=wall,compile_cpu_seconds=cpu,
    bench_elapsed_seconds=bench,peak_process_committed_bytes=max(r['peak_process_committed_bytes'] for r in attempts),
    incoming=[dict(name=p.name,sha256=sha(p)) for p in incoming],
    scope='Normalized bounded-pair graphs with full LinearPMap domains; constructed resolvent family; existing continuous modular operator.',
    pending=['Existence of NormalizedGraphWitness for an arbitrary prescribed densely defined self-adjoint LinearPMap',
             'Independent adversarial review','Physical Dirac/H_min identification reserved to operator'])
create(folder/'unbounded_transform_manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
report=f'''[DERIVED — {count} declarações Lean auditadas; A-2.5.c parcialmente construído]

# A-2.5.c — domínio, resolvente e transformada limitada

UTC: {now.isoformat()}. ABERTURA sha256: `{opening}`.

## Resultado efetivo

Para A,B limitados auto-adjuntos, A injetivo, AB=BA e A²+B²=I,
o operador parcial já existente D=boundedGraphOperator(A,B) satisfaz:
dom(D)=ran(A), D(Ax)=Bx, ker(D)=ker(B), incluindo o domínio no núcleo ambiente.
Provados ||Ax||²+||Bx||²=||x||² e ||Bx||≤||x||.
Se γ≥0 é limite inferior de D no complemento do núcleo, então
γ/sqrt(1+γ²) é limite inferior de B no mesmo complemento.
Não se afirma que o limite inferior seja atingido, nem que exista gap positivo.

Quando A≥0, os lemas existentes de quadrado de LinearPMap dão, com domínio sucessivo:
R=A²=(I+D²)^(-1) e A=sqrt(R). Portanto B=D sqrt(R), com domínio pago.
Essa cadeia está ligada ao contrato `BoundedTransformPreservesKernelAndGap`
por `normalized_graph_pays_contract`. A testemunha `NormalizedGraphWitness`
contém dados de grafo, positividade, comutação e normalização; NÃO pressupõe
igualdade de núcleos nem conclusão do gap.

Realizações conferidas:
- Família existente `resolventSquareRoot R hR hi`, 0≤R≤I, R injetivo:
  A=sqrt(R), B=sqrt(I-R); identidade efetiva do inverso de I+D².
- `continuousModularOperator c`: ligação direta ao mesmo modelo contínuo da
  missão, A=spectralA(c), B=spectralB(c). Não se trocou D por uma matriz.

## Limite exato

Permanece OPEN construir `NormalizedGraphWitness D` para TODO D prescrito,
densamente definido e auto-adjunto em LinearPMap. As realizações acima não
demonstram essa quantificação universal. O contrato condicional está compilado,
mas a existência da testemunha genérica não foi adicionada como axioma nem sorry.
Próximo passo dentro de A-2.5.c: projeção sobre o grafo fechado linear para obter
o resolvente de I+D²; reutilizar a infraestrutura V350 e a transferência de domínio.
`V350ClosedAntilinearResolvent` fornece um modelo de prova, mas sua antilinearidade
impede aplicá-lo diretamente a D linear. Esta etapa não foi declarada paga.
Nenhuma identificação do Dirac físico/H_min foi escolhida pela bancada.

## Verificação e custódia

{count} theorem/lemma, todos cobertos por #print axioms; rc 0 nos quatro arquivos
aprovados; somente propext, Classical.choice, Quot.sound; zero sorry/axioma novo.
Nenhuma alteração de kernel detectada, nenhuma falha de varredura de custódia.
Comando exato em cada recibo: lake env lean -j1 -M8192, via compile_isolated_v2.py.
Falhas preservadas: projeção de pares, real de produto interno, hipótese de seção,
posição de comentário documental e substituição com domínio dependente.
Máximo três ciclos por arquivo, abaixo do teto de seis por lema.

Manifesto: `{folder/'unbounded_transform_manifest.json'}`.
Auditoria: `{folder/'unbounded_transform_axioms.json'}`.
'''
for r in records:
    report+=f"\n- `{r['source']}` SHA256 `{r['source_sha256']}`; log `{r['log']}` SHA256 `{r['log_sha256']}`.\n"
report+=f'''
Máquina: {wall:.3f}s parede, {cpu:.3f}s CPU em {len(attempts)} tentativas.
Bancada decorrida: {bench:.3f}s. Nenhuma chamada externa nova neste lote.
Gasto conhecido por request_id: US$ {cost}; custos desconhecidos permanecem assim.
Leitura da listagem PARA_CHATGPT registrada no manifesto; documento mais recente:
`{incoming[0].name}`. Não foi identificada nova escolha física do operador nesta rodada.

Originais, um.py, kernel e gate não alterados. A-2.5.c EM CURSO, com resultados
parciais medidos; relatório não encerra o ramo nem a missão. Cético ainda pendente.
'''
create(out/'ENTREGA_016_MEDIDA_A2_5c_grafo_resolvente.md',report.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} — A-2.5.c EM CURSO/MEDIDA: {count} declarações isoladas auditadas, grafo normalizado, inverso I+D², núcleo/gap e realização contínua; existência genérica pendente. Bancada {bench/3600:.6f}h; máquina {wall/3600:.6f}h parede / {cpu/3600:.6f}h CPU. Gasto conhecido US$ {cost}; nenhum provedor novo.\n'.encode())
print(json.dumps(manifest,ensure_ascii=False))
