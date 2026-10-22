"""Audit KMS criticism, reuse existing Tomita, and name the precise regional remainder."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C5'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,put,write,append
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
args=[];final=[]
for name,label in [('FiniteKMSStrip_v4.lean','finitekms_04'),('ExistingTomitaAudit.lean','tomita_existing_01')]:
    p=D/(label+'.json');r=json.loads(p.read_bytes());src=D/name
    assert r['rc']==0 and r['source_sha256']==sha(src) and r['log_sha256']==sha(p.with_suffix('.log'))
    args.extend([str(src),str(p.with_suffix('.log'))]);final.append(dict(path=str(p),sha256=sha(p),**r))
auditor=OUT.parent/'PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/auditar_axiomas.py'
a=subprocess.run([sys.executable,'-X','utf8','-B',str(auditor),*args],capture_output=True);assert a.returncode==0,a.stdout
write(D/'AXIOM_AUDIT.json',a.stdout);au=json.loads(a.stdout);assert all(x['auditoria']=='PASSA' for x in au)
assert au[0]['n_theorem_lemma_na_fonte']==10 and len(au[1]['axiomas'])==8
can=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
files=[can/'TGLExt/ContinuousModularStandardSubspace.lean',can/'TGLExt/ContinuousModularReconstruction.lean',
    ROOT/'A1/minimal_imports/ContratoQG_v31_Minimal.lean',ROOT/'A2/FourierStandardTransport_v3.lean',ROOT/'A2/LightRayBoundaryBalance_v3.lean',
    ROOT/'A4/KMSStripConditional.lean',ROOT/'ADENDO_002_CRITICAS/C24_RECEIVED/KIMI_ORIGINAL.md',
    ROOT/'C4/orchestration/DEEPSEEK_KMS_ORIGINAL.md',
    ROOT.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/StandardSubspace.lean']
put(D/'READ_SOURCE_CUSTODY.json',dict(at=now.isoformat(),sources=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
attempts=[json.loads(p.read_bytes()) for pattern in ['finitekms_0*.json','tomita_existing_0*.json'] for p in D.glob(pattern)]
first=min(datetime.fromisoformat(x['started_at']) for x in attempts) if all('started_at' in x for x in attempts) else datetime.fromtimestamp((D/'finitekms_01.marker').stat().st_mtime,timezone.utc)
hours=(now-first).total_seconds()/3600
result=dict(at=now.isoformat(),status='MEDIDA_REGIONAL_PAIR_REQUIRED_NOT_ONLY_MATHLIB',new_analytic_theorems=10,
    imported_existing_declarations=8,all_trio=True,receipts=final,exact_matrix_checks=189,
    refuted_claims=['Cyclic/separating vector KMS forces trivial dynamics','KMS implies unilateral positive generator','Concrete closed Tomita still needs to be written'],
    rejected_overclaim='One-particle Hilbert admits no RegionalModularPair of any sort; no such impossibility follows from the sources',
    retained=['Scalar wavefunction boundary is not operator-order-swapped KMS','Positive translations do not identify geometric and modular boosts'],
    precise_remainders=['H_regional_modular_strip for the same regional algebra and vacuum','H_modular_equals_geometric for that same pair'],
    operator_pair_instantiated=False,mathlib_TODO_is_sufficient_diagnosis=False,
    existing_Tomita_reimplemented=False,compile_attempts=len(attempts),
    compile_wall_seconds=sum(x['wall_seconds'] for x in attempts),compile_cpu_seconds=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in attempts),
    bench_hours=hours,ceiling_hours=8,gate_changed=False,opening_sha256=opening)
put(D/'RESULTS.json',result)
note=f'''[REAL — 10 lemas analíticos e 8 declarações existentes auditadas no trio; DERIVED/CAS — contraexemplo matricial; OPEN — KMS regional]

AberturaSHA256={opening}.

**C5 remove duas falsas lacunas, sem reconstruir o que já existe.**
O Tomita concreto já tem domínio denso, grafo fechado, involutividade,
J S=T e Δ=S†S nos arquivos ContinuousModularStandardSubspace e
ContinuousModularReconstruction. O consumidor ExistingTomitaAudit importa
essas declarações e a ligação KMS existente:8 prints, rc0/trio. Nenhum
teorema foi reescrito. A2 já transporta esse subespaço e grafo por Fourier.
Assim, o TODO genérico da mathlib não descreve sozinho o estado da bancada.

A proposta L2 da crítica Kimi C2.4 é falsa como implicação abstrata.
No Hilbert–Schmidt M2(C), a álgebra age à esquerda, ρ=diag(1/3,2/3),
Ω=√ρ e U_t(X)=ρ^(-it)Xρ^(it). Ω é unitário, cíclico e separante,
pois X↦XΩ é invertível; U_tΩ=Ω, mas U_tE12=exp(it log2)E12.
O estado vetorial restrito à álgebra à esquerda é misto e fiel.
Ele não é o estado puro sobre todo B(Hilbert–Schmidt).

F_AB(z)=Σij ρi Aij Bji exp(iz(logρi−logρj)).
O Lean prova inteiricidade, limite uniforme na faixa0≤Imz≤1,
F_AB(t+i)=F_BA(−t) e fase−1 em t=π/log2. As duas correlações
vetoriais com as convenções EXATAS de KMSAt foram conferidas em189
identidades matriciais racionais/CAS, por base e bilinearidade.
Isso refuta o argumento L2; não é uma instância literal do W físico.
O primeiro CAS falhou porque SymPy nonzero=True tornou q real;
v2 declara q complexo e usa conjugate(q)=1/q na circunferência.
Não se alterou a fórmula para fazê-la passar.

Também não vale «KMS implica positividade unilateral»: neste exemplo
o gerador autoadjunto tem ±log2. Para A=E12,B=E21 a correlação
é exp(−iz log2)/3 e cresce como2^Imz/3 no semiplano superior,
embora seja limitada na faixa KMS. O argumento genérico de inexistência
de RegionalModularPair em um Hilbert de uma partícula não foi demonstrado;
não será adotado como proibição de pesquisa.

**O que fica nomeado:** a álgebra regional concreta, sua representação
e vetor Ω, a faixa H_regional_modular_strip desse par e
H_modular_equals_geometric para o MESMO par. O twist conjugado de
funções escalares A2 e a energia positiva A3 não fornecem por si a troca
de ordem de operadores. KMSStripConditional já encadeia as duas hipóteses
para β_R=2π e β_Killing=2π/κ; não precisa de outra função de ligação.
A segunda quantização/rede e a identificação física não foram construídas
neste alvo. MEDIDA: bloqueio de DADOS e correspondência regional, não
somente da biblioteca. Nenhuma impossibilidade geral foi proclamada.

DeepSeek respondeu de forma independente ao contraexemplo; a bancada
leu a resposta inteira, conferiu as convenções e realizou os controles
acima. Seu recibo permanece emC4/orchestration e foi contabilizado uma vez
no ledger:USD0.03249732; não somado novamente nesta entrega.
Custo conhecido parcial da missão USD2.7237508140; desconhecidos permanecem.

Recursos:{len(attempts)} compilações, parede{result['compile_wall_seconds']:.3f}s,
CPU{result['compile_cpu_seconds']:.3f}s;bancada{hours:.4f}h/teto8h.
Não toca um.py/kernel/gate. Próximo:C6, remanescente Q2 pela árvoreA7.
'''
write(D/'RELATORIO.md',note.encode())
for name in ['ENTREGA_016_C5_KMS_e_Tomita_existente.md','ENTREGA_016_MEDIDA_C5_par_regional.md','ENTREGA_016_C_CRITICA_KMS_faixa.md']:write(OUT/name,note.encode())
tracked=[D/'FiniteKMSStrip_v4.lean',D/'ExistingTomitaAudit.lean',D/'AXIOM_AUDIT.json',D/'HS_CAS.json',D/'verify_hilbert_schmidt_model_v2.py',D/'READ_SOURCE_CUSTODY.json',D/'RESULTS.json',D/'RELATORIO.md']
tracked += [D/(l+e) for l in ['finitekms_04','tomita_existing_01'] for e in ['.json','.log']]
put(D/'manifest.json',dict(at=now.isoformat(),files=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in tracked]))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C5 MEDIDA:KMS regional nomeado;10lemas+8reusos;189CAS;L2 recusado | bancada{hours:.4f}h;CPU{result["compile_cpu_seconds"]:.3f}s | USDparcial2.7237508140, semnova cobrança.\n')
p=ROOT/'A7/CONTINUIDADE.json';d=json.loads(p.read_bytes());d.update(at=now.isoformat(),C5_manifest=str(D/'manifest.json'),next=['C6 Q2 remaining according to A7 tree','ORDEM015 PartB','Finalaudit/report'])
put(p,d,True)
print(json.dumps(dict(status=result['status'],new_theorems=10,reused=8,cas=189)))
