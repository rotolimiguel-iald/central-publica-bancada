"""Keep the MiMo proposal and counterexamples; do not add a production gate."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(old)
        assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
job='fb3587cd-5807-4dab-9aa0-3ac178bc4deb';rec=json.loads((H/f'received_reviews/{job}.json').read_bytes())
audit=json.loads((H/'mimo_contact_bookkeeping_audit/results.json').read_bytes())
assert sha(H/f'received_reviews/{job}.md')==rec['response_sha256']
report=f'''[REAL — nove contraexemplos locais; DECLARADO — proposta MiMo preservada; OPEN — coeficiente Ward completo]
# A7.b — revisão do módulo de contabilidade proposto pelo MiMo
Abertura SHA256 `{opening}`. UTC {now}.

Job {job}; execução {rec['execution_id']}; resposta SHA256
`{rec['response_sha256']}`. Texto recuperado sem nova chamada e lido, inclusive
o trecho de funções inicialmente truncado na exibição. A proposta fornece
uma tabela das fontes antigas e um módulo textual; não calcula amplitudes.

**Decisão: não incorporar o módulo como novo leitor/gate.** Os testes locais
encontraram nove problemas delimitados:

1. O verificador do traço não lê o termo: aceita um coeficiente adulterado999.
2. O verificador de derivada aceita uma fórmula arbitrária não reconhecida.
3. O caso de polo simples é recusado sem uma via de fornecer a certidão exigida.
4. O fator de aridade zero é aceito no contato que exige n.
5. Um ledger vazio anuncia WARD_COEFFICIENT_EMITTED.
6. O mesmo ocorre com flags de erro: elas não entram na decisão.
7. Um registro com a mesma fórmula sobrescreve coeficiente sem colisão.
8. CT11 e CT12, parcelas aditivas da mesma variação, são tratados como duplicatas.
9. CT10 chama grad(chi)grad(u)/(1+u) de termo linear/livre inteiro. A separação
correta é grad(chi)grad(u) menos u grad(chi)grad(u)/(1+u); a segunda parcela
é precisamente o resto interagente já calculado na fonte v2.

Os resultados podem ser reproduzidos por mimo_contact_bookkeeping_audit.py,
rc0, CPU {audit['cpu_seconds']}s. O módulo original foi extraído byte a byte
do bloco Python recebido e preservado na bancada; imports conferidos:
future/dataclasses/enum/typing, sem acesso a rede, shell ou arquivos no módulo.
Os casos de teste propostos pelo modelo eram especificações, não implementações
de todos os detectores anunciados. Flags fornecidas pelo chamador não verificam
independentemente o coeficiente que deveriam auditar.

**Aproveitamento sem nova camada.** A distinção entre contato de Green,
variação com cutoff e defeito de extensão já está nos cálculos originais;
ela permanece. A tabela é referência documental da rodada que o MiMo recebeu,
não retrato automático dos avanços posteriores. A contabilização continua
ancorada em expressões e fontes, sem converter rótulos em prova matemática.
Não se acrescenta este gate paralelo ao programa, não se reabre a unidade
terminal e não se repete a chamada para corrigir um catálogo de metadados.

Consumo informado pelo executor: {rec['result_metadata'].get('usage')}.
Custo estimado informado: {rec['result_metadata'].get('cost_estimate_usd')}USD;
não equivale a fatura. A7.b permanece ativa e nenhum original/gate foi alterado.
'''
rp=O/'ENTREGA_016_A7b_revisao_MiMo_contabilidade.md';save(rp,report)
files=[H/f'received_reviews/{job}.md',H/f'received_reviews/{job}.json',
 H/'mimo_contact_bookkeeping_audit.py',H/'mimo_contact_bookkeeping_audit_run.log',
 H/'mimo_contact_bookkeeping_audit/PROPOSTA_MIMO_ORIGINAL.py',H/'mimo_contact_bookkeeping_audit/PRE_REGISTER.json',
 H/'mimo_contact_bookkeeping_audit/results.json',H/'mimo_contact_bookkeeping_audit/manifest.json',rp]
save(H/'mimo_contact_bookkeeping_audit/delivery_manifest.json',dict(at=now,opening_sha256=opening,
 artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
l=O/'LEDGER_016.jsonl';marker='A7_MIMO_CONTACT_BOOKKEEPING_LOCAL_REJECTION'
if marker.encode() not in l.read_bytes():
    ev=dict(event=marker,at=now,target='A-7.b',provider='local',review_job=job,
     counterexamples=9,cpu_seconds=audit['cpu_seconds'],report_sha256=sha(rp),new_external_execution=False)
    save(l,l.read_bytes()+(json.dumps(ev,ensure_ascii=False)+'\n').encode())
rows=[json.loads(x) for x in l.read_text('utf-8-sig').splitlines() if x.strip()];par={}
def root(k):
    par.setdefault(k,k)
    if par[k]!=k:par[k]=root(par[k])
    return par[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for r in rows:
    ix=ids(r)
    for k in ix[1:]:par[root(k)]=root(ix[0])
known={}
for r in rows:
    ix=ids(r);v=r.get('cost_estimate_usd',r.get('cost_usd',r.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
total=sum(known.values(),Decimal(0))
save(H/'mimo_contact_bookkeeping_audit/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(total),
 ledger_sha256=sha(l),unknown_cost_not_zero=True,billing_not_verified=True))
cp=H/'CONTINUIDADE.json';d=json.loads(cp.read_bytes());d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 mimo_contact_audit_manifest=str(H/'mimo_contact_bookkeeping_audit/delivery_manifest.json'),
 partial_metered_cost_usd=str(total))
d.setdefault('completed_this_turn',[]).append('MiMo contact bookkeeping received and locally audited:9counterexamples;proposal not adopted,existing formulas retained')
save(cp,d)
p=O/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n- {now} — A7.b PROGRESSO:MiMo contabilidade recebido,nove contraexemplos locais,CPU{audit["cpu_seconds"]}s;proposta não incorporada como gate. Custo parcialUS${total};ledger{sha(l)};abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),known_partial_cost=str(total),status='ACTIVE')))
