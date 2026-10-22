"""Deliver exact phase/flat-source checks and a qualified first-K candidate."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT';D=H/'fourier_source_orientation_delivery';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,update=False):
    if p.exists():
        assert update,p
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old);assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b and b;t.replace(p)
def put(p,v,update=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode(),update)
groups=[('fourier_phase_convention','fourier_phase_convention_check.py','fourier_phase_convention_run.log'),
 ('pair_fourier_phase','pair_fourier_phase_check.py','pair_fourier_phase_run.log'),
 ('source_flat_full_fourier','source_flat_full_fourier_check.py','source_flat_full_fourier_run.log'),
 ('source_firstK_symbol','source_firstK_symbol_check.py','source_firstK_symbol_run.log'),
 ('source_firstK_log_partition','source_firstK_log_partition_check.py','source_firstK_log_partition_run.log'),
 ('source_firstK_symbol_v2','source_firstK_symbol_check_v2.py','source_firstK_symbol_v2_run.log')]
results=[json.loads((H/stem/'results.json').read_bytes()) for stem,_,_ in groups]
checks=sum(r.get('checks',r.get('independent_checks',0)) for r in results)
cpu=sum(r['cpu_seconds'] for r in results);now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
phase=O/'ENTREGA_016_A7b_fases_Fourier_e_fonte_plana.md'
write(phase,('''[DERIVED — convenções e fonte plana; REAL — CAS exato; OPEN — Ward causal completo]
# A7.b — fase de Fourier e orientação da fonte
'''+f'Abertura SHA256 `{opening}`. UTC {now}.\n\n'+'''
Para Fourier exp(-ip.x), o coeficiente racional do motor meromórfico multiplica
C_E*(-i)^m. Para exp(+ip.x), multiplica C_E*i^m. A frase i^m no motor não
pode ser usada sem dizer qual das duas convenções está sendo aplicada.

Derivação: a integral de Schwinger para H_l(x)z^(-(m+l+4)/2+a) dá
(-i)^l*pi²*2^(-m+2a)*Gamma(a-k)/Gamma(N-a)*H_l(p)*(p²)^(k-a),
k=(m-l)/2, N=(m+l+4)/2. A fase (-1)^k da Gamma combina para (-i)^m.
O regulador (1-a) e as derivadas dos logs são mantidos antes da parte finita.

Controle independente: R(d_j U_n)-d_j R(U_n) coincide com o contato local
já calculado para n=2,3,4, todos os eixos. Trinta verificações passaram.
Doze controles negativos com a fase oposta deixam um erro proporcional a
FourierLog, portanto não corrigível apenas por um contato local.

No PAR, a perna móvel usa exp(+ipx). Se m=nx+ny-2r, n=1+[xi>=0]+[yj>=0]
e P_j tem grau j, a fase é i^(m-j)*i^(n-2o+j)/i=(-1)^order.
Com os sinais da integração por partes e potenciais, reproduz o motor em
134 combinações. Nenhuma alteração dos números do par foi necessária.

Na FONTE plana, o teste em X usa exp(-ipX) e o ghost exp(+ipY).
O termo A tem fase +i; o termo B, com a derivada explícita do ghost, -i.
A integração angular independente reproduziu os contatos + referência
diferencial existentes: 18 controles, incluindo o caso não axial. Em
T=e11,p=v=e0, a imagem Einstein da fonte é -3/32, com log zero.
No caso não axial registrado ela é -63/16, também com log zero.

Esses resultados conferem a orientação plana e os sinais do par. Não
autorizam substituir E covariante por E(p) na fonte curva. A execução
completa do par de primeiraK ainda está no mesmo processo93180.
''').encode())
source=O/'ENTREGA_016_MEDIDA_fonte_curva_orientacao_Taylor.md'
coeff=results[-1]['coefficients']
write(source,('''[DERIVED — símbolo sob transporte Taylor declarado; REAL — CAS; OPEN — adjunção bilocal completa]
# A7.b — correção da orientação Taylor da fonte
'''+f'Abertura SHA256 `{opening}`. UTC {now}.\n\n'+'''
Tentativa preservada: source_full_fourier_engine.py passou no controle
plano, mas usou o polinômio P_j(x) junto da exponencial exp(-ipx).
A primeira curvatura divergiu do log covariante local já medido.
Separar a soma por grau externo localizou o erro exatamente em j=1.

A reversão do deslocamento exige P_j(-x)=(-1)^j P_j(x), além da troca
da exponencial. Em v2, apenas esse fator foi corrigido; kernels,
prescrição, medidas e multiplicadores meromórficos permanecem iguais.
Não se ajustou um coeficiente para zerar Ward. O predecessor fica no disco.

Na base [Tpv, (pTp)(pv)/p², trT(pv)], para p²>0 e retirados C_E, i e K,
o símbolo candidato de primeira curvatura tem coeficientes (1,L,L²):
'''+''.join(f'- {row}\n' for row in coeff)+'''

Três amostras determinam os coeficientes; o caso independente
p=(1,2,-1,1), v=(2,-1,1,3), T=e11 reproduz os três componentes.
O termo racional com 1/p² permanece: ausência de contato não é ausência
de kernel. As amostras de ajuste não são contadas como prova independente.

Após a correção, a parte sem log(z) explícito reproduz o log covariante
local anterior, na normalização -1/4. Os kernels com log(z) acrescentam
ao coeficiente de FourierLog exatamente Tpv/2+trT(pv)/4 nos controles,
incluindo o não axial. Portanto o log local UV sozinho não determina
todo o multiplicador de Fourier da fonte.

LIMITAÇÃO: esta é a soma do símbolo na ordenação Taylor especificada.
A identificação da adjunção bilocal, sua imagem pelo operador Einstein
curvo e a soma com os pares/tadpoles/W ainda não foram demonstradas.
Não é Q2. O Kimi recebeu separadamente a pergunta sobre adjunção, sem
estes números, preservando a independência da revisão.

Comandos: python -X utf8 -B source_firstK_symbol_check.py e
source_firstK_log_partition_check.py; depois source_firstK_symbol_check_v2.py,
todos no Python simbólico de A4. rc0, mas o primeiro resultado NÃO satisfez
a comparação matemática: os rc0 significam execução e ajuste, não aceitação
da hipótese. Logs e SHA constam do manifesto desta entrega.
Próximo: concluir o controle não axial do par e construir E da fonte sem
comutar indevidamente funções não locais de Box. Gate e originais intactos.
''').encode())
files=[Path(__file__),phase,source,H/'source_full_fourier_engine.py',H/'source_full_fourier_engine_v2.py',H/'source_fourier_v2_inputs.json']
for stem,script,log in groups:
    files += [H/script,H/log,H/stem/'PRE_REGISTER.json',H/stem/'results.json',H/stem/'manifest.json']
put(D/'manifest.json',dict(at=now,opening_sha256=opening,checks_reported=checks,negative_controls=12,cpu_seconds=cpu,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in files],full_Q2=False))
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
ledger=O/'LEDGER_016.jsonl';event=dict(at=now,event='A7_FOURIER_SOURCE_ORIENTATION_DELIVERED',target='A7.b',
 checks=checks,negative_controls=12,cpu_seconds=cpu,new_external_execution=False,full_Q2=False,
 delivery_manifest_sha256=sha(D/'manifest.json'))
write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
rows=[json.loads(line) for line in ledger.read_text('utf-8-sig').splitlines() if line.strip()];parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for row in rows:
    ix=ids(row)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for row in rows:
    ix=ids(row);cost=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and cost is not None:known[root(ix[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal());put(D/'COST_SUM.json',dict(at=now,ledger_sha256=sha(ledger),known_partial_usd=str(total),unknown_calls_not_zero=True))
progress=O/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n- {now} A7.b PROGRESS: fases e fonte plana verificadas; fonteK1 v1 MEDIDA e v2 corrigida por reversão Taylor. {checks} verificações reportadas +12 negativos; CPU{cpu}s. Adjunção curva e Q2 OPEN. Custo parcial conhecidoUS${total}; desconhecidos não são zero.\n'.encode(),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes());v.update(at=now,previous_goal_turn='PROGRESS',fourier_source_orientation_manifest=str(D/'manifest.json'))
v['completed_this_turn']=['Fourier phase: 30 checks/12 negative controls','Pair plus-plane ordering:134 checks','Flat source full Fourier:18 checks','FirstK source v1 mismatch measured; v2 reverses Taylor displacement and passes nonaxis; curved adjunction still OPEN']
v['own_live_processes']=[dict(session_id=93180,script='curved_pair_fourier_check.py',status='RUNNING_CONFIRMED',last_checked_utc=now)]
v['next']=['Poll own session93180; same run, nonaxis node100 atCPU1641s last log',
 'Inspect source_firstK_symbol_v2 and Fourier source report; do not use v1 curved coefficients',
 'Prove full source adjunction/Einstein composition before combining with pair; Kimi independent task staged',
 'A7.b until20:32UTC approximately, then required A7.c/d,A8,PartB and final audit']
put(p,v,True)
print(json.dumps(dict(delivered=True,artifacts=len(files),checks=checks,negative_controls=12,cpu_seconds=cpu,partial_known_cost_usd=str(total))))
