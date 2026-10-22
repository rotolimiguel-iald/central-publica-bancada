"""Seal the concrete screen cocycle, state the remaining induced-representation lemma."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C4'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,put,write,append
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
spec=[('NullScreenFrame_v2.lean','screen_02'),('BoostScreenPolarizations_v2.lean','polarizations_02'),
      ('StrictCocycleGauge.lean','gauge_01'),('NullFrameDecomposition_v2.lean','nullframe_02'),('TransverseCocycle_v3.lean','transverse_03')]
args=[];receipts=[]
for name,label in spec:
    p=D/(label+'.json');r=json.loads(p.read_bytes());src=D/name
    assert r['rc']==0 and r['source_sha256']==sha(src) and r['log_sha256']==sha(p.with_suffix('.log'))
    args.extend([str(src),str(p.with_suffix('.log'))]);receipts.append(dict(path=str(p),sha256=sha(p),**r))
auditor=OUT.parent/'PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/auditar_axiomas.py'
a=subprocess.run([sys.executable,'-X','utf8','-B',str(auditor),*args],capture_output=True);assert a.returncode==0,a.stdout
write(D/'AXIOM_AUDIT.json',a.stdout);audit=json.loads(a.stdout)
assert all(x['auditoria']=='PASSA' for x in audit)
count=sum(x['n_theorem_lemma_na_fonte'] for x in audit);assert count==26
attempts=[json.loads(p.read_bytes()) for pattern in ['screen_0*.json','polarizations_0*.json','gauge_0*.json','nullframe_0*.json','transverse_0*.json'] for p in D.glob(pattern)]
elapsed=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600
known=Decimal(json.loads((ROOT/'C3/LEDGER_TOTALS.json').read_bytes())['partial_metered_cost_usd'])+Decimal(json.loads((D/'orchestration/DEEPSEEK_KMS_RECEIPT.json').read_bytes())['cost_estimate_usd'])
result=dict(at=now.isoformat(),status='MEDIDA_WITH_CONCRETE_SCREEN_COCYCLE',theorems=count,all_trio=True,receipts=receipts,
    compile_attempts=len(attempts),compile_wall_seconds=sum(x['wall_seconds'] for x in attempts),
    compile_cpu_seconds=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in attempts),
    bench_hours=elapsed,ceiling_hours=16,exact_CAS_checks=46,
    named_remaining='GlobalHelicityInducedRepresentationMeasured',
    specification=['Extend the concrete regular-cone frames across measurable patches','Derive oriented SO(2) screen quotient for the proper orthochronous Lorentz group',
        'Implement the resulting U(1) characters of weights +1 and -1 as a strongly continuous unitary representation on the cone L2 space',
        'Identify its restriction with the existing contract boost and handle the null-axis exceptional sets'],
    literal_named_axiom_added=False,physical_partition_selected=False,full_induced_representation=False,regional_BW=False,
    partial_metered_cost_usd=str(known),failed_usage_unknown=True,gate_changed=False,opening_sha256=opening)
put(D/'RESULTS.json',result)
note=f'''[REAL — 26 teoremas no trio; DERIVED — diagnóstico; OPEN — representação induzida completa]

AberturaSHA256={opening}.

C4 entrega uma base transversal concreta e mensurável no cone regular
q≠0. O transporte usa o wedgeBoostMap do contrato. As duas polarizações
circulares são conjugadas e distintas; a fase do boost nesta base é zero.
A decomposição nula é provada, não presumida. Para transformações lineares
com transporte do momento e preservação métrica explicitados, o Lean prova
C(g∘h;x,z)=C(g;y,z) C(h;x,y), onde Cij=-⟨ei(z),g ej(x)⟩.
A componente proporcional ao momento nulo desaparece na próxima leitura.

Cinco fontes finais, 26 declarações auditadas, todas rc0 e somente o trio.
As tentativas falhas foram preservadas: álgebra polinomial exigiu multiplicar
as identidades hiperbólica/radial; o rewrite final foi substituído por
normalização explícita do pareamento. Nenhum axioma foi acrescentado.

**Crítica C2.3 parcialmente aceita e corrigida.** O teorema espectral A3 já
usa fibra isométrica genérica; não precisa de outro motor. A afirmação Kimi
«fase zero em qualquer trivialização» é falsa: χ(x)=x produz o cobordo
exp(i s), igual a−1 em s=π (Lean). A fase é U(1); não se pressupôs argumento
real global aditivo. O boost orbital não constrói sozinho uma rede ou BW.

A resposta1265 antiga também foi confrontada: sua seção levava k a p/r,
e sua inversa atanh(p1/r) estava errada. A seção corrigida
L=Bx(ξ)Rx(a,b)By(log r), a²+b²=1,r>0, leva k=(1,0,1,0) a p,
é Lorentz/det1 e é equivariante para Bx;46 verificações CAS exatas.
Isso é CAS, não uma prova Lean do grupo de Lorentz inteiro.

Outra correção: a lei de cociclo quase em toda parte para cada s,t fixos
não autoriza substituir t=x−s. A prova Lean de cobordo é PONTUAL.
Exemplo explícito [DERIVED]: C(s,x)=exp(ix²) se x=s, e1 fora disso.
Para s,t fixos a lei vale fora de {{s,s+t}}, mas a diagonal dá
b(x)=exp(ix²); b(x)/b(x−s)=exp(i(2sx−s²)), diferente de1 em geral.
Logo a extração daquela diagonal não prova a equivalência de representantes
a.e.; exige versão estrita. A revisão Kimi8c terminou por timeout, sem
resultado validado; esse diagnóstico local não é atribuído ao modelo.

**MEDIDA: GlobalHelicityInducedRepresentationMeasured permanece nomeado**
(especificação em RESULTS.json): quociente orientado SO(2), cartas/exceções
e ação unitária fortemente contínua de Lorentz inteiro no L² do cone, com
caracteres ±1. A composição finita acima reduz essa dívida; não a renomeia
como paga. Duas polarizações e um boost não substituem essa representação.
Não se selecionou partição nem se criou habitante regional/vácuo/Fock.

MiMo46f falhou por resposta SSE sem finalização; Kimi8c por timeout.
Não repetidos, uso/custo desconhecidos. DeepSeekaa respondeu à crítica KMS,
que será auditada em C5; custo medido USD0.03249732. Kimi b175, objetivo
distinto de crítica final C3, segue pelo coordenador. Nenhum voto é prova.

Recursos C4: {len(attempts)} compilações, parede{result['compile_wall_seconds']:.3f}s,
CPU{result['compile_cpu_seconds']:.3f}s, bancada{elapsed:.4f}h/teto16h.
Custo remoto conhecido parcial da missão USD{known}; desconhecidos não são zero.
Aceitação «teorema ou lema nomeado» atendida com o alcance acima.
Sem edição de kernel/um.py/gate. Próximo:C5, KMS de faixa e crítica C2.4.
'''
write(D/'RELATORIO.md',note.encode())
write(OUT/'ENTREGA_016_C4_cociclo_transversal.md',note.encode())
write(OUT/'ENTREGA_016_MEDIDA_C4_representacao_induzida.md',note.encode())
write(OUT/'ENTREGA_016_C_CRITICA_cociclo_fisico.md',note.encode())
files=[D/n for n,_ in spec]+[D/(l+ext) for _,l in spec for ext in ['.json','.log']]+[D/'AXIOM_AUDIT.json',D/'SECTION_CAS.json',D/'RESULTS.json',D/'RELATORIO.md']
put(D/'manifest.json',dict(at=now.isoformat(),files=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C4 MEDIDA:26teoremas/cociclo transversal; representação induzida nomeada | bancada{elapsed:.4f}h;CPU{result["compile_cpu_seconds"]:.3f}s | USDconhecido parcial{known};Kimi/falhas desconhecidos.\n')
st=ROOT/'A7/CONTINUIDADE.json';d=json.loads(st.read_bytes());d.update(at=now.isoformat(),C4_manifest=str(D/'manifest.json'),next=['C5 KMS de faixa e crítica C24','C6 Q2','ORDEM015 PartB','Auditoria/relatório final'],partial_metered_cost_usd=str(known),
    pending_orchestration='Kimi b175 C3 final critique running jobef185ce2-45eb-4708-993a-9582ade9b516, coordinator ownsworker86373. Kimi8c andMiMo46f terminal failed no retry. DeepSeekaa received, auditC5. d3 staged untilC6.')
put(st,d,True)
print(json.dumps(dict(status=result['status'],theorems=count,bench_hours=elapsed,known_cost=str(known))))
