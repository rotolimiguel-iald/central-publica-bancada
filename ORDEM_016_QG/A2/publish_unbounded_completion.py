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
new=[('SameSquareDomain.lean','same_square_domain_01'),
     ('SelfadjointAbsoluteRoot.lean','selfadjoint_absolute_01'),
     ('UnboundedTransformConstruction_v2.lean','unbounded_construction_02'),
     ('UnboundedTransformKernelGap_v3.lean','unbounded_kernel_gap_02'),
     ('UnboundedTransformEnergy.lean','unbounded_energy_01'),
     ('UnboundedTransformProjectionControl.lean','unbounded_projection_control_01')]
passed=[]
for oldname in ['unbounded_transform_manifest.json','general_resolvent_manifest.json']:
    for r in json.loads((folder/oldname).read_bytes())['artifacts']:
        passed.append((r['source'],r['log'].removesuffix('.log')))
passed.extend(new)
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
create(folder/'unbounded_complete_axioms.json',audit.stdout)
audits=json.loads(audit.stdout)
count=sum(x['n_theorem_lemma_na_fonte'] for x in audits)
newcount=sum(x['n_theorem_lemma_na_fonte'] for x in audits[-len(new):])
attempts=[]
for pattern in ['same_square_domain_0*.json','selfadjoint_absolute_0*.json',
                'unbounded_construction_0*.json','unbounded_kernel_gap_0*.json',
                'unbounded_energy_0*.json','unbounded_projection_control_0*.json']:
    attempts.extend(json.loads(p.read_bytes()) for p in sorted(folder.glob(pattern)))
wall=sum(r['wall_seconds'] for r in attempts)
cpu=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in attempts)
previous=json.loads((folder/'general_resolvent_manifest.json').read_bytes())
first=json.loads((folder/'unbounded_transform_manifest.json').read_bytes())
bench=(now-datetime.fromisoformat(previous['utc'])).total_seconds()
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
latest={}
for line in (out/'LEDGER_016.jsonl').read_text(encoding='utf-8').splitlines():
    if line:
        r=json.loads(line); key=r.get('request_id')
        if key: latest[key]={**latest.get(key,{}),**r}
cost=sum(Decimal(str(r.get('custo_usd',r.get('cost_usd')))) for r in latest.values()
    if r.get('custo_usd',r.get('cost_usd')) is not None)
canonical=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\V354RegularSupport.lean')
lines=canonical.read_text(encoding='utf-8').splitlines()
anchors={term:[i+1 for i,s in enumerate(lines) if term in s] for term in
    ['def regularMinimalLock','theorem regularMinimalLock_relative_gap','theorem regularMinimalLock_ker']}
incoming=sorted((root.parent/'TUNEL/PARA_CHATGPT').glob('*.md'),key=lambda p:p.stat().st_mtime,reverse=True)[:3]
manifest=dict(utc=now.isoformat(),status='SELFADJOINT_UNBOUNDED_CONTRACT_CONSTRUCTED_AND_AUDITED',
    branch='A-2.5.c',declarations=count,new_declarations=newcount,artifacts=records,
    opening_sha256=opening,audit_sha256=sha(folder/'unbounded_complete_axioms.json'),
    new_attempts=len(attempts),new_compile_wall_seconds=wall,new_compile_cpu_seconds=cpu,
    new_bench_seconds=bench,total_compile_wall_seconds=first['compile_wall_seconds']+previous['compile_wall_seconds']+wall,
    total_compile_cpu_seconds=first['compile_cpu_seconds']+previous['compile_cpu_seconds']+cpu,
    total_bench_seconds=first['bench_elapsed_seconds']+previous['additional_bench_seconds']+bench,
    canonical_anchor=dict(path=str(canonical),sha256=sha(canonical),lines=anchors),
    incoming=[dict(name=p.name,sha256=sha(p)) for p in incoming],
    scope='Every self-adjoint LinearPMap on a complete complex Hilbert space: actual D sqrt((I+D²)^(-1)), full domain, contraction, exact kernel, gap lower-bound transport and attained norm-ratio transport.',
    control='Strict contraction on each nonzero vector. A nonzero idempotent cannot equal this transform. No uniform norm gap below one asserted.',
    pending=['Independent Kimi review of earlier packet','DeepSeek authorized inventory subject to route preview','Physical microscopic Dirac identification reserved; no gate change'])
create(folder/'unbounded_complete_manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
report=f'''[DERIVED — A-2.5.c: contrato construído e auditado para D auto-adjunto arbitrário]

# Transformada limitada: ramo ilimitado concluído no escopo matemático

UTC {now.isoformat()}. ABERTURA SHA256 `{opening}`.
Complementa os dois checkpoints anteriores; ambos preservados como linhagem.

**Resultado:** para todo LinearPMap D auto-adjunto em Hilbert complexo completo,
foi construída a aplicação limitada `b(D)=D sqrt(R)`, onde `R=(I+D²)^(-1)`.
Não há hipótese extra NormalizedGraphWitness no teorema final
`unboundedTransform_pays_contract`. D*D=D² é o recorte auto-adjunto usado aqui.

A cadeia efetivamente compilada é:
grafo fechado de D → projeção ortogonal → sobrejetividade I+D² → resolvente R
positivo, injetivo e ≤I → raiz positiva E de D² → dom(E)=dom(D), ||Ex||=||Dx||
por núcleo de grafo comum → ran(sqrt(R))=dom(D) → b(D) limitado.
Reutilizados os lemas V350; não se postulou a igualdade dos domínios.

Conclusões:
- `ker b(D)=ker D`, com núcleo ambiente incluindo a pertinência ao domínio.
- `||sqrt(R)x||²+||b(D)x||²=||x||²` e `||b(D)x||≤||x||`.
- Um limite inferior γ≥0 para D no complemento do núcleo transporta-se para
  γ/sqrt(1+γ²) no mesmo complemento. Não se cria gap positivo sem a hipótese.
- Todo u∈dom(D) tem um lift x com sqrt(R)x=u e b(D)x=Du; uma razão de normas
  atingida γ é transportada à razão γ/sqrt(1+γ²). A afirmação não substitui
  condições de não nulidade/pertinência ao setor ao declarar ótimo espectral.

**Controle relevante para H_min:** para todo x≠0, ||b(D)x||<||x||.
Logo, b(D) não pode ser um idempotente não nulo. Isto NÃO afirma ||b(D)||<1
uniformemente; a norma de operador pode aproximar/atingir 1 como supremo.
No canônico, regularMinimalLock é 1−P_F e seu próprio comentário já separa
o representante mínimo do operador microscópico. A igualdade de núcleos e
o transporte de gap não autorizam igualar literalmente esses operadores.
Fonte e linhas conferidas: `{canonical}`; SHA256 `{sha(canonical)}`;
âncoras `{json.dumps(anchors,ensure_ascii=False)}`.

**Validação:** {newcount} declarações novas, {count} no conjunto do ramo ilimitado,
todos theorem/lemma cobertos por #print axioms, rc 0, apenas
propext/Classical.choice/Quot.sound, zero sorry/axioma novo. Todos os recibos
aprovados têm zero alteração de kernel detectada e zero erro de leitura.
Erros intermediários de elaboração de composição e subtipo de domínio estão
preservados; máximo três ciclos nos arquivos deste ramo. Não houve lake build.
Comandos exatos, fontes e logs no manifesto completo:
`{folder/'unbounded_complete_manifest.json'}`.
Auditoria com nomes/axiomas/hashes: `{folder/'unbounded_complete_axioms.json'}`.
'''
for r in records[-len(new):]:
    report+=f"\n- `{r['source']}` SHA256 `{r['source_sha256']}`; log SHA256 `{r['log_sha256']}`.\n"
report+=f'''
Máquina nova: {wall:.3f}s parede / {cpu:.3f}s CPU, {len(attempts)} tentativas.
Bancada adicional: {bench:.3f}s. Totais do ramo no manifesto, sem dupla contagem.
Gasto externo conhecido por request_id: US$ {cost}; custo ausente não é zero.
Kimi revisa somente o pacote inicial, job f16dd00e-d6ff-48d4-943e-8c82f3911024,
sem repetição. DeepSeek recebeu autorização direta do operador para cinco fontes
e memória comum; envio depende da prévia da coordenação, não é contado como concluído.
Nenhuma fonte adicional foi autorizada por esse pedido. Duas rejeições automáticas
anteriores de envio foram preservadas; não foram contornadas, a autorização veio depois.

A-2.5.c PAGO no escopo matemático declarado; revisão externa ainda pendente.
Não identifica D com um Dirac físico, não muda um.py/kernel/gate e não confirma física.
Próximo alvo na árvore: A-3, representações de energia positiva em namespace próprio.
Consultada novamente a listagem PARA_CHATGPT; último arquivo é `{incoming[0].name}`.
'''
create(out/'ENTREGA_016_A2_5c_transformada_ilimitada.md',report.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} — A-2.5.c PAGO matemático: b(D) efetiva para LinearPMap auto-adjunto, domínio/raiz, núcleo, gap, energia; controle exclui igualdade com projetor não nulo. +{newcount} declarações, {count} no ramo. Bancada adicional {bench/3600:.6f}h; máquina {wall/3600:.6f}h parede / {cpu/3600:.6f}h CPU. Custo conhecido US$ {cost}, revisões externas pendentes. Próximo A-3.\n'.encode())
append(folder/'DEEPSEEK_PEDIDO_PENDENTE.md',f'\n\n[INPUT POSTERIOR — {now.isoformat()}] O operador respondeu diretamente: “Autorizar esse envio ao DeepSeek”, à pergunta que explicitava a API DeepSeek, memória científica comum e estes cinco arquivos, incluindo SelfadjointSquareResolvent.lean. Encaminhamento à sessão coordenadora aceito após essa resposta. Registro/execução continuam dependentes da prévia da fila; nenhuma ampliação do payload.\n'.encode())
print(json.dumps({k:v for k,v in manifest.items() if k!='artifacts'},ensure_ascii=False))
