"""Record the free gauge-fermion shift without upgrading the complete QME."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    b=x.encode() if isinstance(x,str) else x
    if p.exists():
        old=p.read_bytes()
        if b==old:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and b;t.replace(p)
def new(p,o):assert not p.exists();save(p,json.dumps(o,ensure_ascii=False,indent=2))
r=json.loads((HERE/'shifted_antifield/results.json').read_bytes());now=datetime.now(timezone.utc)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — diferencial livre e deslocamento do antifield; REAL — CAS finito; OPEN — contratermo completo]
# A7.b — manter b e cancelá-lo pela combinação correta

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.

A069 escreve S0=Sgf+<h*,Kc>-<barc*,b>. Para tornar explícita sua frase
«antibracket escolhido para gerar(7)», usamos sF=(S0,F)_σ, com
σ_A=(-1)^paridade(phi_A) multiplicando cada par canônico(phi_A,phi_A*).
Equivale às coordenadas Darboux tilde(phi_A*)=σ_A phi_A*; não é alteração
da teoria. Derivadas direita/esquerda e essa identificação são mantidas
juntas. Nesse dicionário, a ação escrita na069 dá

    s h=Kc; s barc=-b; s b=s c=0;
    s h*=Hh+C*b;
    s b*=Ch-ell^-1 b-barc*;
    s c*=-Q barc-K*h*; s barc*=Qc.

H é a Hessiana física livre ANTES de eliminar b, não a mínima gauge-fixada.
HK=0 e CK=Q garantem s²=0, usando adjuntos e coeficientes de fundo fixos.
Por exemplo s²c*=Qb-K*C*b=0 e s²b*=Q c-Q c=0. Não se pode misturar
esse dicionário com outro sinal canônico para os mesmos símbolos de antifields.

Segue, sem descartar b,

    hat_h*=h*+C*barc,
    s hat_h*=Hh+C*b-C*b=Hh.

O deslocamento tem paridade ímpar e gh=-1. Na normalização principal
Euclidiana usada no cálculo dos vértices, E=4κH e u=4κ hat_h* dão su=Eh.
Aplicamos então a identidade graduada já derivada à candidata

    F=A0/2 integral u_A B_AB c^μ partial_μu_B,
    B(A)=-A/6-I trA/12, A0=1/(8π²).

O coeficiente linear em h* de sF é4κA0 B[c·∂E+(div c)E/2]. Com
c constante e a convenção Fourier+i, a parte transversal reproduz a
forma4iκA0[-(p·v)(E/6+P_T trE/12)] anteriormente medida. Esse fator
é calculado, não uma identificação entre H e E sem normalização.

O CAS conferiu um bloco com um modo de gauge e outro físico independente,
H=diag(0,m/(4κ)), CK=Q=1: nilpotência10×10, números fantasma, deslocamento
e coeficiente;4checks+2negativos, rc0,CPU{r['cpu_seconds']}s. A prova
geral acima é por identidades de operadores; o bloco é controle de sinais,
não substituto da prova. Não houve compilação Lean nem chamada remota.

Ao expandir u aparecem também antighosts: esses termos são parte do gerador,
nunca omitidos. Para cutoffχ, a identidade módulo divergência traz
+(A0/2) integral(partial_μχ)J^μ após integração por partes. Não apagamos
esse contato. A realidade na involução escolhida, os demais momentos,
componentes longitudinais, contribuição não linear s1F, curvatura e anomalia
causal finita ainda precisam ser conferidos. O gerador completo não está
identificado com esta única parcela. Nenhum kernel, original ou gate alterado.
'''
rp=HERE/'shifted_antifield/DERIVACAO_DESLOCAMENTO.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_deslocamento_antifield_e_b.md',report)
files=[HERE/'shifted_antifield_check.py',HERE/'shifted_antifield_run.log',rp,
       HERE/'shifted_antifield/PRE_REGISTER.json',HERE/'shifted_antifield/results.json',
       CHAT/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md']
new(HERE/'shifted_antifield/manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
    artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
ledger=OUT/'LEDGER_016.jsonl'
event=dict(event='A7_FREE_SHIFTED_ANTIFIELD_NORMALIZATION',at=now.isoformat(),provider='local',target='A-7.b',
    checks=4,negative_controls=2,rc=0,cpu_seconds=r['cpu_seconds'],report_sha256=sha(rp),full_Q2=False)
save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if v is not None and key:costs[key]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)))
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now.isoformat(),shifted_antifield_manifest=str(HERE/'shifted_antifield/manifest.json'),
    next=['Match general principal R1 after shifted-antifield BV candidate; reality and nonlinear terms still open',
          'Recover DeepSeek D2 and temporal/cohomology reviews without another execution',
          'Continue causal finite anomaly and curved cutoff terms in A7b timebox'],
    partial_metered_cost_usd=total,
    pending_orchestration='DeepSeekD2completed;Kimi temporal executing;Kimi filtration now queued04dae5a6-b78a-4f0f-83c7-4cb1b6c3c0be;primitive_v2 awaits reconciliation')
d['completed_this_turn'].append('Free antifield shift cancels b with signs and normalization explicit;4checks+2negative controls')
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
p=OUT/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n- {now.isoformat()} — A7.b PROGRESSO: hat_h*=h*+C*barc cancela b no diferencial livre; normalização4κA0 conferida.4checks+2negativos;CPU{r["cpu_seconds"]}s. Vértice geral/Q2finitaOPEN. Custo parcialUS${total}. Abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),checks=4,negative_controls=2,full_Q2=False),ensure_ascii=False))
