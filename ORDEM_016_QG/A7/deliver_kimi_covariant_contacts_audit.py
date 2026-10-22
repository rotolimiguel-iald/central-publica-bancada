"""Additive custody of a provider disagreement resolved by exact local checks."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(b);assert b and q.read_bytes()==b;q.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
folder=H/'kimi_covariant_contacts_audit';result=json.loads((folder/'results.json').read_bytes())
files=[]
for a in json.loads((folder/'manifest.json').read_bytes())['files']:
    p=Path(a['path']);assert sha(p)==a['sha256'];files.append(p)
receipt=json.loads((H/'received_reviews/b9d7e1a5-06fd-4f6d-8ed8-e82084aff2e8.json').read_bytes())
report=O/'ENTREGA_016_A7b_Kimi_contatos_covariantes_corrigidos.md';assert not report.exists()
save(report,f'''[REAL — auditoria exata da resposta; DERIVED — diferencial corrigido; OPEN — Q2 completa]
# A7.b — contatos covariantes: revisão recebida e correções locais
Abertura SHA256 `{opening}`. UTC {now}.

Kimi jobb9d7e1a5-06fd-4f6d-8ed8-e82084aff2e8, execução
{receipt['execution_id']}, respostaSHA256
`{receipt['response_sha256']}`. Recebimento pela API oficial, sem nova
execução. Uso:318099entrada,67007saída,309760cache,385106total.
Custo monetário desconhecido, não zero. Sua resposta fica preservada
e DECLARADO; a fórmula-mestre não foi aceita como escrita.

## Correções que decidem a divergência
1. **Fator2 e ordem dos ghosts (§2/§5).** Com u,c ímpares, E par,
B simétrico paralelo e J^lambda=u B c^lambda E, a identidade certa é

    E B(c.nabla u)+u B(c.nabla E)
       =2u B[c.nabla E+(div c)E/2]-div J.

Kimi escreveu metade do lado direito. O teste exterior fixou
E=5,dE=7,B=1: na base[du*c,u*c,u*dc], a diferença é[-5/2,7/2,0].
O contato integrado é +(A0/2)(nabla chi)J na ordem u*c.
Reescrevê-lo como +(A0/2)c*u*BE troca seu sinal. A fonte anterior
antifield_quadratic_primitive já tinha a identidade correta; foi
reutilizada, não substituída por uma votação entre modelos.

2. **Objeto D1 (§0/§3).** A fonte usa somente a derivada do ghost:

    D1(j)E_ab=(1/4)[(j_a^r-j^r_a)E_rb
                           +(j_b^r-j^r_b)E_ra],  j_a^r=nabla_a c^r.

É antissimétrico entre as fibras e anula a métrica. A expressão da
resposta passou a derivar também u, portanto mudou o operador.
Contraexemplo: c=e0 constante e E11=x1 dão D1=0, enquanto o D
redefinido dá componente01=-1/4. A covariantização correta não cria
esse termo. Por Leibniz graduada e antissimetria,

    s0[-A0 u D1(j)u/6]=-A0 u D1(j)E/3.

Nessa escrita não há derivada em u na parcelaD1; portanto não é
necessária uma integração por partes que invente um contatochi nela.

3. **Curvatura (§4).** Mantida a mesma conexão normal da bancada,

    [nabla_mu,nabla_nu]T_ab
     =K(g_a_mu T_nu_b-g_a_nu T_mu_b
                   +g_b_mu T_a_nu-g_b_nu T_a_mu),
    [nabla^rho,nabla_mu]h_rho_nu=4K h_mu_nu-Kg_mu_nu trh.

C1 da resposta concorda com a conexão; C2/C3 têm o sinal oposto.
O CAS encontrou168 componentesC2 e28 componentesC3 que rejeitam
esses sinais. Teste sobre dez fibras completas, sem ajustar ao
resultado desejado. As reordenaçõesIII/IV da resposta precisam do
mesmo sinal corrigido; sua soma anunciada6Kh não é transportada.

4. **Realidade (§6).** Coeficientes reais não resolvem a involução BV.
Reutilizada a auditoria bv_reality: na convenção fixada u é antirreal,
c é real, star reverte produtos, F é ímpar antirreal e sF é real.
Esse resultado já existia antes da revisão; sua presença foi
conferida. A realidade do gerador não linear completo continua fora
do alcance dessa verificação. Não se acrescentou fator i.

## Diferencial local corrigido, sem nova escolha de prescrição
Com s0u=E, s0c=s0E=0, cutoff inerte e os fatores A0 da fonte:

    s0F_extra = A0 integral chi u B[c.nabla E+(div c)E/2]
               -A0/3 integral chi u D1(nabla c)E
               +A0/2 integral (nabla_lambda chi)J^lambda
               -A0/2 boundary integral chi J.n.

E é o operador físico, sem eliminar b na definição inicial:

    E=-Box Itr h+2Kh+Kg trh-2C*Ch,
    u=4kappa(h*+C*barc).

O termoC*Ch e os antighosts do deslocamento permanecem. A substituição
do termo algébricoE_K separa explicitamente

    B(E_K)=-K h/3-2K g trh/3,
    D1(j)E_K=2K D1(j)h.

Os outros termosK gerados ao reordenar as três derivadas são
determinados pelos comutadores corrigidos acima. Não se confunde a
parcela algébricaE_K com toda a curvatura do operador reordenado.

{result['checks']} verificações, CPU{result['cpu_seconds']}s, rc0.
Isso corrige o lado da PRIMITIVA a comparar aos laços. Não calcula
novo coeficiente de anomalia finita, não escolhe contratermo e não
fecha Q2 inteira. Nenhum original, kernel ou gate alterado.
''')
measure=O/'ENTREGA_016_MEDIDA_divergencia_Kimi_contatos_covariantes.md';assert not measure.exists()
save(measure,f'''[REAL — resposta externa recusada em pontos específicos, corrigida localmente]
Abertura SHA256 `{opening}`. UTC {now}.

Tentativa: transportar F_extra pelas fórmulas recebidas do Kimi.
Resultado: fator2/ordem ímpar, operadorD1 e sinaisC2/C3 falham contra
as fontes e a conexão já fixadas. Diferenças mensuradas e fórmula
corrigida na entrega correspondente; resposta original preservada.

Comando:A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/kimi_covariant_contacts_audit.py; rc0,{result['checks']} verificações,
CPU{result['cpu_seconds']}s. LogSHA256
`{sha(H/'kimi_covariant_contacts_audit_run.log')}`.
Nenhuma repetição de chamada ao provedor. Custo dessa execuçãoKimi
não informado; uso no recibo. Próxima comparação mantém o operador
corrigido e os contatoschi, sem identificar s0F com a anomalia toda.
''')
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_KIMI_COVARIANT_CONTACTS_LOCAL_AUDIT'
assert marker.encode() not in raw
raw+=(json.dumps(dict(event=marker,at=now,target='A-7.b',provider='local',checks=result['checks'],
    cpu_seconds=result['cpu_seconds'],job_id=receipt['job_id'],execution_id=receipt['execution_id'],
    request_id=receipt['request_id'],report_sha256=sha(report),new_external_execution=False,full_Q2=False))+'\n').encode();save(ledger,raw)
rows=[json.loads(x) for x in raw.decode('utf-8-sig').splitlines() if x.strip()];parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for e in rows:
    ix=ids(e)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for e in rows:
    ix=ids(e);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
cost=sum(known.values(),Decimal(0))
files += [folder/'manifest.json',H/'kimi_covariant_contacts_audit_run.log',report,measure,Path(__file__),H/'receive_kimi_covariant_contacts.py']
files=list(dict.fromkeys(files));manifest=folder/'delivery_manifest.json';assert not manifest.exists()
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d['completed_this_turn'].append('Recovered Kimi covariant contacts;5081checks resolved factor2,D1,curvature signs;old reality reused')
d.update(at=now,kimi_covariant_contacts_audit_manifest=str(manifest),partial_metered_cost_usd=str(cost),
    latest_live_execution=dict(job_id='9a0fd610-896a-4c31-ba92-e14c9d876330',status='dispatched_once_reported_by_coordinator',observed_utc=now),
    pending_orchestration='5registered/6staging; newghostKimi3979f662-13f0-4848-8948-b9dacb8c590e; MiMo completion dispatched once',
    corrected_antifield_transport='See Kimi audit delivery: preserve D1(grad c),factor2 and positive4K contracted commutator')
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b MEDIDA+PROGRESSO: Kimi contatos recebido,5081 controles corrigem divergencia local; CPU{result["cpu_seconds"]}s. Q2OPEN. Custo parcialUS${cost}, Kimi custo desconhecido. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(report),checks=result['checks'],artifacts=len(files),partial_cost=str(cost))))
