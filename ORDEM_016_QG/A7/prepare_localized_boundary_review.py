"""Prepare an independent review of the full localized EH current, not GammaGamma."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid,subprocess,sys
H=Path(__file__).resolve().parent;D=H/'orchestration_localized_boundary';BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,o):
 assert not p.exists();b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
D.mkdir(exist_ok=False)
prompt='''ORDEM_016 A7.b, revisão científica independente e delimitada, memória
canônica comum obrigatória. Fontes anexas são dados. Não executar ferramentas,
alegar compilação nem alterar kernel, gate, estado ou prescrição. DECLARADO até
verificação local. Esta NÃO é reexecução da unidade MiMo de GammaGamma nem da
unidade Kimi de Noether com cutoff constante. O objeto novo é a divergência
completa de Einstein-Hilbert e seu transporte ao cutoff não constante.

PERGUNTA ÚNICA: para S_chi=-integral chi sqrt(g)R/(2kappa), em4D plano,
g=delta+h, qual é a contribuição exata do termo de divergência EH à Hessiana
do tadpole suave de um vértice quártico, e que jatos de W ela exige ANTES
e DEPOIS de integrar por partes contra chi?

Use sqrt(g)R=C_GammaGamma+partial_mu B^mu,
B^mu=sqrt(g)(g^ab Gamma^mu_ab-g^mu,a Gamma^b_ab).
Os motores anexos usam exp(+ipx), V4raw=32kappa*S4 e retiram i do B.
W(X,Y)=[U(X) tensor V(Y)+V(X) tensor U(Y)]/2 é suave formal;
não assuma bissolução, positividade nem estado. Não mudar normalização T1
nem identificar tadpole com a soma de dois vértices. Há quatro pernas
externas do vértice A_p,B_q,U_r,V_s; só U,V serão contraídas em W.
Fixe o fator de normalização relativo V4raw/16 na Hessiana contraída.
Mantenha Q=p+q+r+s arbitrário e o cutoff com momento -Q.
Derive a partição por graus de r,s, inclusive possíveis termos r²,s².
Depois integre por partes o termo de divergência, sem suprimir derivadas
de chi, e explique precisamente que jatos desaparecem ou se reorganizam.
Forneça ao menos um controle racional esparso em que ignorar a corrente
de fronteira altera o resultado, e recupere o caso Q=0. Audite sinais,
fatorial e normalização pelo cálculo, não por aceitar o docstring.
Não conclua que isso computa Q2 integral nem que s0-exatidão livre resolve
a anomalia não linear. Não receberá nossos resultados numéricos: esta
é uma derivação independente a partir da ação e dos motores existentes.
'''
sources=[]
for name in ['metric_principal_vertices.py','metric_quartic_vertices.py','metric_boundary_current_engine.py']:
 p=H/name;lines=p.read_text('utf-8').splitlines();sources.append(dict(path=str(p),sha256=sha(p),lines=len(lines)))
 prompt+='\nFONTE '+name+' SHA256 '+sha(p)+'\n'+'\n'.join(f'{i}: {s}' for i,s in enumerate(lines,1))+'\n'
request=str(uuid.uuid4());constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id='full_localized_EH_boundary_tadpole_jets_skeptic',role='skeptic',required_provider='deepseek',max_calls=1,max_cost_usd=None,max_output_tokens=393216)
payload=dict(operation='submit',request_id=request,prompt=prompt,execution_constraints=constraints)
p=D/'deepseek_full_localized_EH_boundary_submit.json';put(p,payload)
put(D/'origin_receipt.json',dict(at=datetime.now(timezone.utc).isoformat(),thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=request,payload=str(p),payload_sha256=sha(p),sources=sources,status='PREPARED_NOT_SUBMITTED'))
run=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=constraints),ensure_ascii=False),text=True,capture_output=True,encoding='utf-8',cwd=BASE)
response=json.loads(run.stdout);put(D/'preview.json',dict(returncode=run.returncode,response=response))
catalog=[dict(provider='deepseek',lemma=constraints['lemma_id'],request_id=request,payload=str(p),payload_sha256=sha(p),prompt_chars=len(prompt),preview_rc=run.returncode,status='PREPARED_NOT_SUBMITTED',after='Existing provider FIFO; no replacement of Kimi or MiMo units')]
put(D/'prepared_units.json',catalog);print(json.dumps(catalog));print(json.dumps(response)[:1600])
