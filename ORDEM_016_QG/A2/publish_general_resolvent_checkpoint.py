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
passed=[('ClosedLinearGraphResolvent_v2.lean','linear_graph_resolvent_02'),
        ('SelfadjointSquareResolvent.lean','selfadjoint_resolvent_01')]
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
create(folder/'general_resolvent_axioms.json',audit.stdout)
count=sum(x['n_theorem_lemma_na_fonte'] for x in json.loads(audit.stdout))
attempts=[]
for pattern in ['linear_graph_resolvent_0*.json','selfadjoint_resolvent_0*.json']:
    attempts.extend(json.loads(p.read_bytes()) for p in sorted(folder.glob(pattern)))
wall=sum(r['wall_seconds'] for r in attempts)
cpu=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in attempts)
start=datetime.fromisoformat(json.loads((folder/'unbounded_transform_manifest.json').read_bytes())['utc'])
bench=(now-start).total_seconds()
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
latest={}
for line in (out/'LEDGER_016.jsonl').read_text(encoding='utf-8').splitlines():
    if line:
        r=json.loads(line); key=r.get('request_id')
        if key: latest[key]={**latest.get(key,{}),**r}
cost=sum(Decimal(str(r.get('custo_usd',r.get('cost_usd')))) for r in latest.values()
    if r.get('custo_usd',r.get('cost_usd')) is not None)
manifest=dict(utc=now.isoformat(),status='ISOLATED_LEAN_AUDITED',branch='A-2.5.c',
    declarations=count,artifacts=records,opening_sha256=opening,
    predecessor_manifest_sha256=sha(folder/'unbounded_transform_manifest.json'),
    audit_sha256=sha(folder/'general_resolvent_axioms.json'),attempts=len(attempts),
    compile_wall_seconds=wall,compile_cpu_seconds=cpu,additional_bench_seconds=bench,
    scope='Every self-adjoint LinearPMap: explicit positive injective contraction R=(I+D²)^(-1), with full successive-domain equation and graph identity.',
    pending=['NormalizedGraphWitness for prescribed D: sqrt(R) domain, bounded signed D sqrt(R), commutation and normalization',
             'Physical identification remains reserved','Kimi scope review pending'])
create(folder/'general_resolvent_manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
report=f'''[DERIVED — {count} novas declarações Lean auditadas; resolvente geral construído]

# A-2.5.c — adendo: I+D² para o operador prescrito

UTC {now.isoformat()}. ABERTURA SHA256 `{opening}`.
Complementa ENTREGA_016_MEDIDA_A2_5c_grafo_resolvente.md, preservada.

Agora o resolvente foi construído para TODO D auto-adjunto em LinearPMap,
em Hilbert complexo completo; não é mais dado de entrada de uma família escolhida.

1. O grafo complexo fechado de D é colocado em WithLp 2 (H×H).
   A projeção ortogonal de (z,0) produz x∈dom(D) com
   ⟨z−x,u⟩=⟨Dx,Du⟩ para todo u∈dom(D).
2. Pela definição do adjunto e D*=D, Dx∈dom(D) e D²x=z−x.
   Portanto I+D² é sobrejetivo, conservando o domínio sucessivo real da operação.
3. Positividade e simetria de D² são derivadas da energia e do emparelhamento.
   A construção existente partialPositiveResolvent produz R=(I+D²)^(-1).
4. Provados 0≤R≤I, injetividade, a equação do inverso e
   resolventGraphOperator(R)=D² com igualdade de grafos/domínios.

Tudo acima foi compilado, incluindo a existência. Não se postulou a sobrejetividade
nem a positividade para o D auto-adjunto recebido. A densidade e o fechamento
vieram das propriedades de IsSelfAdjoint da Mathlib efetivamente consultada.

## Passagem ainda aberta e próxima construção

R geral está pago. Falta concluir a testemunha normalizada do MESMO D:
A=sqrt(R), ran(A)=dom(D), B=D A limitado e auto-adjunto, AB=BA, A²+B²=I.
O condicional de núcleo/gap já auditado então se aplica.
Rota localizada nos arquivos existentes: V350ResolventSquareRoot constrói |D|
com quadrado D²; V350PartialSquareGraphCore e V350GraphCoreNormTransfer permitem
comparar os domínios de |D| e D via igualdade de normas no domínio de D².
As etapas posteriores não são anunciadas como concluídas neste adendo.

## Custódia e custos

{count} theorem/lemma com #print axioms no trio permitido; rc 0 nos dois arquivos;
zero sorry/axioma novo, zero alteração de kernel detectada, zero erro de custódia.
A tentativa inicial falhou apenas ao normalizar projeções de par na identidade
vetorial final; está preservada. Warnings de variáveis sem uso não foram suprimidos.
Comandos integrais nos recibos (lake env lean -j1 -M8192, runner isolado).
Manifesto: `{folder/'general_resolvent_manifest.json'}`.
Auditoria: `{folder/'general_resolvent_axioms.json'}`.
'''
for r in records:
    report+=f"\n- `{r['source']}` SHA256 `{r['source_sha256']}`; log `{r['log']}` SHA256 `{r['log_sha256']}`.\n"
report+=f'''
Máquina adicional: {wall:.3f}s parede, {cpu:.3f}s CPU, {len(attempts)} tentativas.
Bancada desde o checkpoint anterior: {bench:.3f}s. Custo externo conhecido por
request_id: US$ {cost}; valores ausentes não são tratados como zero.
A sessão Orquestrar IAs na Central IALD registrou separadamente a revisão Kimi
dos quatro arquivos ANTERIORES: request c101844e-52f8-4aac-8dfb-881771481a24,
job f16dd00e-d6ff-48d4-943e-8c82f3911024; pendente, não duplicada, sem incluir
os dois arquivos deste adendo. A bancada não escreveu no ledger nessa janela.

A-2.5.c permanece EM CURSO. Nenhum original, um.py, kernel ou gate alterado.
Não houve seleção de Dirac físico/H_min nem afirmação de confirmação experimental.
'''
create(out/'ENTREGA_016_MEDIDA_A2_5c_resolvente_geral.md',report.encode())
p=out/'ENTREGA_016_PROGRESSO.md'
old=p.read_bytes()
create(p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')),old)
b=f'\n- {now.isoformat()} — A-2.5.c EM CURSO: +{count} declarações auditadas, sobrejetividade de I+D² e resolvente geral do D auto-adjunto prescrito. Domínio da raiz e B=D sqrt(R) pendentes. Bancada adicional {bench/3600:.6f}h; máquina {wall/3600:.6f}h parede / {cpu/3600:.6f}h CPU; custo conhecido US$ {cost}; Kimi pendente, sem duplicação.\n'.encode()
t=p.with_name(p.name+'.tmp')
with t.open('xb') as f: f.write(old+b)
assert t.read_bytes()==old+b
t.replace(p)
print(json.dumps(manifest,ensure_ascii=False))
