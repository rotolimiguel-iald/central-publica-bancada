from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, subprocess, sys

root = Path(__file__).resolve().parents[1]
folder = root / 'A2'
out = root.parent / 'TUNEL/DO_CHATGPT'
now = datetime.now(timezone.utc)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p, data):
    assert not p.exists(), p
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f: f.write(data)
    assert tmp.read_bytes() == data
    tmp.rename(p)
def append(p, data):
    old = p.read_bytes()
    create(p.with_name(p.name + '.bak_' + now.strftime('%Y%m%d_%H%M%S_%f')), old)
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f: f.write(old + data)
    assert tmp.read_bytes() == old + data
    tmp.replace(p)

source = folder/'LightRayTwistWidth_v3.lean'
log = folder/'twist_width_04.log'
receiptpath = folder/'twist_width_04.json'
r = json.loads(receiptpath.read_bytes())
assert r['rc'] == 0 and not r['newer_kernel_files'] and not r['scan_errors']
assert r['source_sha256'] == sha(source) and r['log_sha256'] == sha(log)
audit = subprocess.run([sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py'),str(source),str(log)],capture_output=True)
assert audit.returncode == 0, audit.stdout + audit.stderr
create(folder/'twist_width_axioms.json',audit.stdout)
audits=json.loads(audit.stdout)
count=sum(a['n_theorem_lemma_na_fonte'] for a in audits)
attempts=[json.loads(p.read_bytes()) for p in sorted(folder.glob('twist_width_0*.json'))]
wall=sum(a['wall_seconds'] for a in attempts)
cpu=sum(a['cpu_user_seconds']+a['cpu_kernel_seconds'] for a in attempts)
bench=(now-min(datetime.fromisoformat(a['utc']) for a in attempts)).total_seconds()
manifest={'utc':now.isoformat(),'status':'ISOLATED_LEAN_AUDITED','declarations':count,
 'artifacts':[{ 'file':str(p),'sha256':sha(p)} for p in [source,log,receiptpath,folder/'twist_width_axioms.json']],
 'source_supersedes':[{ 'file':str(p),'sha256':sha(p)} for p in [folder/'LightRayTwistWidth.lean',folder/'LightRayTwistWidth_v2.lean']],
 'compile_wall_seconds':wall,'compile_cpu_seconds':cpu,'bench_elapsed_seconds':bench,
 'scope':'Twist uniqueness for a>0 and 0<w<2*pi; NOT an isotony iff theorem.',
 'canonical_kernel_changes':r['newer_kernel_files']}
create(folder/'twist_width_manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
latest={}
for line in (out/'LEDGER_016.jsonl').read_text(encoding='utf-8').splitlines():
    if line:
        item=json.loads(line)
        key=item.get('request_id')
        if key: latest[key]={**latest.get(key,{}),**item}
cost=sum(Decimal(str(v.get('custo_usd',v.get('cost_usd')))) for v in latest.values() if v.get('custo_usd',v.get('cost_usd')) is not None)
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — compilação isolada auditada; revisão externa da meia-inclusão pendente]

# A-2.3.d — largura da torção

Data UTC: {now.isoformat()}. ABERTURA sha256: `{opening}`.

Para a>0 e 0<w<2π, foi compilada a equivalência:
`(∀ x, m_a(x+iw) = conj(m_a(x))) ↔ w=π`, onde `m_a(z)=exp(i a exp(z))`.
O módulo no ponto x=0 força sin(w)=0; o intervalo aberto seleciona π.
{count} declarações auditadas, rc 0, axiomas apenas propext/Classical.choice/Quot.sound,
sem sorry e sem alteração detectada no kernel.

Controles demonstrados: torção falha em π/2 e 3π/2 para a>0;
para a<0, |m_a(iπ/2)|>1; para a=0, a torção vale para toda largura.
Falha de contração não foi promovida a falha da isotonia. A equivalência não demonstra
que π é a única largura de isotonia em todo regime nem identifica sozinha potências
modulares ilimitadas. A-2.3.d+ permanece opcional; o cético do teorema principal está em execução.

Comando: `C:\\Python314\\python.exe -X utf8 -B A0\\compile_isolated_v2.py <kernel> A2\\LightRayTwistWidth_v3.lean twist_width_04 <A2>`.
Tentativas anteriores preservadas: v1 falhou na coerção do zero na norma; v2 corrigiu o
lado da faixa e v3 corrigiu a mesma coerção no lado real. Uma tentativa intermediária
não iniciou elaboração por sandbox negar acesso a dependências; log preservado.
Máquina acumulada: {wall:.3f} s parede, {cpu:.3f} s CPU. Bancada decorrida: {bench:.3f} s.
Nenhuma chamada remota nova nesta etapa; total monetário conhecido no ledger: US$ {cost}.
Valores não informados pelos provedores continuam desconhecidos.

Fonte sha256: `{sha(source)}`.
Log sha256: `{sha(log)}`.
Manifesto completo: `{folder/'twist_width_manifest.json'}`.
Não move o gate. Próximo alvo: A-2.4, âncoras do vácuo; depois A-2.5.
'''
create(out/'ENTREGA_016_MEDIDA_A2_3d_largura_da_torcao.md',report.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} — A-2.3.d PAGO no escopo de twist_preserved_iff (8 declarações isoladas auditadas); não isotonia iff. Bancada {bench/3600:.6f} h; máquina parede {wall/3600:.6f} h, CPU {cpu/3600:.6f} h; gasto conhecido acumulado US$ {cost}; críticas da meia-inclusão pendentes.\n'.encode())
print(json.dumps(manifest,ensure_ascii=False))
