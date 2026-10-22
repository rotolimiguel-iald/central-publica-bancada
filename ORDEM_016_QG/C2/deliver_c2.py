"""Audit the new width theorem and preserve the unproved necessity direction."""
from pathlib import Path
from datetime import datetime, timezone
import json, sys, subprocess
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'C2'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,write,put,append
now=datetime.now(timezone.utc)
auditor=OUT.parent/'PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/auditar_axiomas.py'
src=D/'WidthFromContraction_v2.lean'; log=D/'width_02.log'
r=json.loads((D/'width_02.json').read_bytes())
assert r['rc']==0 and sha(src)==r['source_sha256'] and sha(log)==r['log_sha256']
a=subprocess.run([sys.executable,'-X','utf8','-B',str(auditor),str(src),str(log)],capture_output=True)
assert a.returncode==0,a.stdout.decode('utf-8')
audit=json.loads(a.stdout); assert audit[0]['auditoria']=='PASSA'
write(D/'AXIOM_AUDIT.json',a.stdout)
old=ROOT/'A2/density_separation_manifest.json'; m=json.loads(old.read_bytes()); reused=[]
for item in m['records']:
    for key in ['source','receipt','log']:
        p=ROOT/'A2'/item[key]; assert sha(p)==item[key+'_sha256'],p
    rr=json.loads((ROOT/'A2'/item['receipt']).read_bytes()); assert rr['rc']==0
    reused.append(item)
put(D/'REUSED_DENSITY_CUSTODY.json',dict(origin=str(old),sha256=sha(old),records=reused,
    rebuilt_this_turn=False,original_theorems=m['compiled_theorems']))
receipts=[json.loads(p.read_bytes()) for p in sorted(D.glob('width_*.json'))]
wall=sum(x['wall_seconds'] for x in receipts); cpu=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in receipts)
elapsed=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
missing='IsotonyImpliesStripMultiplierCriterion'
result=dict(at=now.isoformat(),status='MEDIDA_WIDTH_CRITERION_PROVED_NECESSITY_NAMED',
    new_declarations=len(audit[0]['axiomas']),axioms_in_trio=True,compile_rc=0,
    proved='a>0,w>0: full-strip multiplier contraction and conjugate top boundary iff w=pi',
    removed_hypothesis='w<2*pi is derived, not assumed',
    retained_hypothesis='analytic multiplier criterion, in particular conjugate boundary',
    negative_control='width pi/2 contracts for a>0 but violates conjugate top boundary',
    reused='real Gaussian density and actual halfline_isotony for K at c=2*pi^2',
    remaining_lemma=missing,
    remaining_statement='For w>0, Kw=rapidityStandardSubspace(2*pi*w), actual U(a)Kw subset Kw for all a>=0 implies full-strip contraction and conjugate top-boundary criterion for multiplier exp(i*a*exp(z)), for a>0.',
    necessity_proved=False,regional_KMS_proved=False,physical_H2_constructed=False,
    external_critique_C22='Terminal provider APITimeoutError, no answer inferred and no repeat',
    compile_wall_seconds=wall,compile_cpu_seconds=cpu,bench_elapsed_hours=elapsed,ceiling_hours=12,
    gate_changed=False,canonical_written=False)
put(D/'RESULTS.json',result)
note=f'''[REAL — C2: critério de largura provado; necessidade a partir da isotonia nomeada]

AberturaSHA256={opening}.

Cinco enunciados novos compilaram com rc0 e axiomas somente do trio.
Para m_a(z)=exp(i a exp(z)), a>0 e w>0, ficou provado:
**contração em toda a faixa 0≤Im z≤w + borda conjugada ⇔ w=π**.
A restrição anterior w<2π foi retirada das hipóteses: se w≥2π,
o ponto z=3πi/2 tem norma exp(a)>1, contradizendo a contração.
A borda conjugada permanece essencial: a faixa π/2 contrai, mas falha
na borda. Positividade e contração sozinhas não selecionam π.

Foram reconferidos os hashes de fontes, recibos rc0 e logs do pacote
A2/density_separation_manifest.json: a densidade gaussiana real e
halfline_isotony para U e K efetivos já estavam pagos. Foram reutilizados,
nunca recriados nem contados como novas provas. O parâmetro desse K é
c=2π²; a largura analítica é π. A ponte Fourier existente identifica
a fase com log do símbolo do Delta construído, mas não é automaticamente
um teorema regional BW/KMS.

**Lema ainda não pago: {missing}.** Para w>0 e
K_w=rapidityStandardSubspace(2πw), deduzir de U(a)K_w⊆K_w para todo
a≥0 o critério analítico de contração e borda conjugada usado acima.
O novo resultado paga a conclusão a partir desse critério; não transforma
uma condição suficiente de preservação em condição necessária.
Não foi criado axiom Lean para ocultar essa lacuna. Este é o lema nomeado
previsto na aceitação C2. A crítica C2.2 terminou por APITimeoutError,
não por resultado matemático; a chamada terminal não foi repetida.

Auditoria: AXIOM_AUDIT.json; comando, logs e recibos width_01/02 preservados.
Recursos: {len(receipts)} compilações, parede {wall:.3f}s, CPU {cpu:.3f}s;
bancada {elapsed:.4f}h/teto12h. Não move o gate, não constrói H2 regional.
Próximo C3: integrar as doze fontes A6 mantendo corpos e hipóteses.
'''
write(D/'RELATORIO.md',note.encode())
write(OUT/'ENTREGA_016_C2_largura_e_isotonia.md',note.encode())
write(OUT/'ENTREGA_016_MEDIDA_C2_necessidade_do_criterio.md',note.encode())
refs=[p for p in D.iterdir() if p.is_file() and p.suffix!='.marker']
put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in refs],gate_changed=False))
append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='C2_WIDTH_CRITERION_AND_NAMED_NECESSITY',target='PartC.C2',remote_call=False,
    compile_wall_seconds=wall,compile_cpu_seconds=cpu,manifest_sha256=sha(D/'manifest.json')))+'\n')
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} C2MEDIDA:5lemas novos no trio;w<2pi derivado;isotonia=>criterio analitico ainda nomeado. Bancada{elapsed:.4f}h/12h;CPU{cpu:.3f}s;parede{wall:.3f}s. SHA256={sha(D/"manifest.json")}. Gateintacto;segueC3. AberturaSHA256={opening}.\n')
p=ROOT/'A7/CONTINUIDADE.json'; c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',next=['C3 integrate all twelve A6 sources with unchanged theorem bodies','C4 cocycle; C5KMS; C6Q2; PartB; finalaudit'],C2_manifest=str(D/'manifest.json'),own_live_processes=[])
c['remaining_full_goal']=['C3-C6','external critiques source audits','ORDEM015 PartB','final audit and report'];put(p,c,True)
print(json.dumps(result))
