"""Deliver Maxwell polynomial scope and preserve the operational quantum debt."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,re
R=Path(__file__).resolve().parents[1];D=R/'D2prime';OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import sha,save,write
now=datetime.now(timezone.utc)
source=D/'MaxwellPolynomial_v2.lean';receipt=D/'maxwell_02.json';log=D/'maxwell_02.log'
x=json.loads(receipt.read_bytes());assert x['rc']==0 and x['source_sha256']==sha(source) and x['log_sha256']==sha(log)
assert not x['newer_kernel_files'] and not x['scan_errors']
assert not re.search(r'\b(sorry|axiom)\b',source.read_text('utf-8'))
ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log.read_text('utf-8-sig'))
assert len(ax)==5 and all(set(v.split(', '))<={'propext','Classical.choice','Quot.sound'} for _,v in ax)
p=R/'A1/probes';old=json.loads((p/'local_stress_02.json').read_bytes());oldlog=p/'local_stress_02.log'
assert old['rc']==0 and old['source_sha256']==sha(p/'StressTensorDataLocal_v2.lean') and old['log_sha256']==sha(oldlog)
oa=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",oldlog.read_text('utf-8-sig'))
target=[(n,v) for n,v in oa if n.endswith('.forged_tensor_rejected')]
assert len(target)==1 and set(target[0][1].replace('\n','').split(', '))<={'propext','Classical.choice','Quot.sound'}
cycles=[json.loads((D/f'maxwell_{i:02}.json').read_bytes()) for i in [1,2]]
r=dict(at=now.isoformat(),status='MEDIDA_CLASSICAL_POLYNOMIAL_PAID_QUANTUM_WICK_INSTANCE_OPEN',new_declarations=dict(ax),source_sha256=sha(source),log_sha256=sha(log),receipt_sha256=sha(receipt),forged_control_reused=dict(source_sha256=old['source_sha256'],receipt_sha256=sha(p/'local_stress_02.json'),declaration=target[0][0]),named_lemma='MaxwellWickExpectationLocalMeasured',obligations=['Construct photon net representation and common dense domain for smeared field strengths','Define renormalized Wick two-point quadratic forms and expectation tensor, not products of one-point means','Derive vacuum subtraction, translation/boost covariance, integrable distributional conservation on admissible vectors','Establish microcausality/affiliation and prove SAME expectation belongs to StressTensorDataLocal on the selected W0'],classical_NEQ_quantum='Pointwise nonnegative classical null flux does not imply a positivity theorem for renormalized quantum expectations',cpu_seconds=sum(v['cpu_user_seconds']+v['cpu_kernel_seconds'] for v in cycles),wall_seconds=sum(v['wall_seconds'] for v in cycles),bench_hours=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600,opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),gate_changed=False,new_external_calls=0)
save(D/'RESULTS.json',r)
text=f'''[REAL — cinco teoremas de Maxwell clássico; OPEN — expectativa de Wick na rede do fóton]

Abertura016SHA256: {r['opening_sha256']}

D2′: expressão covariante (+---) de Maxwell escrita e verificada no Lean. Simetria, traço zero, valor nulo para campos clássicos nulos e T_nn=(E_y−B_z)²+(E_z+B_y)² foram demonstrados. A última igualdade implica positividade clássica. Não foi promovida a positividade da expectativa quântica renormalizada.

MaxwellPolynomial_v2.lean sha256 {sha(source)}; maxwell_02.log sha256 {sha(log)}. Cinco declarações, rc0, trio usual, zero sorry/axioma novo. Dois ciclos; um erro de redução de índice finito corrigido, fonte/log anteriores preservados. CPU{r['cpu_seconds']:.6f}s; parede{r['wall_seconds']:.6f}s; bancada{r['bench_hours']:.6f}h/teto10h.

O controle exigido já estava pago na A1.c: {target[0][0]}. Fonte e recibo antigo conferidos por hash, sem recompilar ou copiar o motor. Ele recusa o tensor forjado da A1.b2 por falha de simetria. Nenhuma nova declaração é contada por esse reaproveitamento.

MaxwellWickExpectationLocalMeasured continua NÃO PAGO. A expressão polinomial não fornece :F_ab F_cd: nem domínio denso/localidade de distribuições de operadores. São necessárias a rede do fóton e sua representação, subtração do vácuo e expectativas de dois campos, covariância e conservação distribucional com integrabilidade, no MESMO W₀. Usar produtos das médias de E e B substituiria a expectativa quadrática por outro objeto. O campo clássico zero também não demonstra o vácuo quântico.

Portanto não há habitante StressTensorDataLocal do fóton construído nesta entrega. A localidade operacional permanece [OPEN] conforme a alternativa expressa do adendo. Resultado aceito como MEDIDA parcial, sem criar axioma nem forçar o leitor. Próximo D3′: quadrado/conjugação/centro, com a distinção entre ponto fixo modular e momento físico.
'''
write(OUT/'ENTREGA_016_D2prime_Maxwell.md',text.encode())
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now.isoformat()} — D2′ MEDIDA:5 teoremas clássicos, controle forjado reaproveitado; MaxwellWickExpectationLocalMeasured aberto. Bancada{r["bench_hours"]:.6f}h, CPU{r["cpu_seconds"]:.6f}s. PróximoD3′. AberturaSHA256 {r["opening_sha256"]}.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=now.isoformat(),own_live_process=None,own_live_processes=[],D2prime_delivery=str(D/'RESULTS.json'),next='D3prime light-square/conjugation/stationary center; explicit modular-fixed versus physical-momentum distinction. D1 global photon rep and D2 quantum Wick expectation remain named. No new remote egress while three specific payloads await approval.');save(q,c,True)
print(json.dumps({k:r[k] for k in ['status','cpu_seconds','wall_seconds','bench_hours','named_lemma']},ensure_ascii=False))
