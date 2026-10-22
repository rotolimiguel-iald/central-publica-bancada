"""Independent literal-Christoffel audit of MiMo's proposed -2/3 residual."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from functools import lru_cache
from decimal import Decimal
import sys,json,time,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6';D=C/'mimo_parametrix_audit_v2'
sys.path.insert(0,str(H))
import bilocal_first_curvature_engine as B
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,put,write,append

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc);start=time.process_time();checks=0
    source=BASE/'state/handoffs/78e92782-75b2-4c66-91d8-038e450213c0_delivery.json'
    j=json.loads(source.read_bytes())['job'];e=j['execution'];r=e['result'];assert e['status']=='result_ready'
    write(D/'MIMO_ORIGINAL.md',r['text'].encode('utf-8'))
    rec=dict(provider='mimo',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],source_sha256=sha(source),response_sha256=sha(D/'MIMO_ORIGINAL.md'),
        prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),usage=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],status='DECLARADO',remote_call_repeated=False)
    put(D/'RECEIPT.json',rec)
    def delta(a,b):return s.Integer(a==b)
    def gamma(coords,upper,i,a):return -(coords[i]*delta(upper,a)+coords[a]*delta(upper,i)-2*delta(i,a)*coords[upper])/3
    # MiMo claims sum_i partial_i Gamma^m_ia = -2 delta_ma/3. In dimension4 it is -delta_ma.
    for a,m in product(range(4),repeat=2):
        div=sum(s.diff(gamma(B.x,m,i,a),B.x[i]) for i in range(4))
        assert s.expand(div+delta(m,a))==0;checks+=1
    assert sum(s.diff(gamma(B.x,0,i,0),B.x[i]) for i in range(4))!=-s.Rational(2,3);checks+=1
    @lru_cache(None)
    def diff(f,side,i):return B.derivative(f,side,i)
    @lru_cache(None)
    def prop(o,ind):return B.metric(o,*ind)
    inds=[(a,b,c,d) for a in range(4) for b in range(a,4) for c in range(4) for d in range(c,4)]
    samples={};negative_controls={}
    for n,ind in enumerate(inds):
        for side,positions in [('X',(0,1)),('Y',(2,3))]:
            coords=B.x if side=='X' else B.y;rad=sum(t*t for t in coords)
            f0=prop(0,ind);f1=prop(1,ind)
            val=sum(diff(diff(f1,side,i),side,i) for i in range(4))
            val+=sum((rad*delta(i,jj)-coords[i]*coords[jj])/3*diff(diff(f0,side,i),side,jj) for i,jj in product(range(4),repeat=2))
            val-=sum(sum(gamma(coords,m,i,i) for i in range(4))*diff(f0,side,m) for m in range(4))
            for i in range(4):
                for pos in positions:
                    a=ind[pos]
                    for m in range(4):
                        changed=ind[:pos]+(m,)+ind[pos+1:];f=prop(0,changed);gam=gamma(coords,m,i,a)
                        val-=2*gam*diff(f,side,i)+s.diff(gam,coords[i])*f
            val-=2*f0
            p,q=positions
            if ind[p]==ind[q]:
                for m in range(4):
                    changed=list(ind);changed[p]=changed[q]=m;val+=2*prop(0,tuple(changed))
            # Impose the distance only AFTER all X/Y derivatives, never anchor y=0.
            poly=s.cancel(s.expand(val)*B.w**4)
            assert not s.denom(poly).has(B.w),(side,ind,poly)
            final=s.expand(poly.subs(B.w,sum((B.x[i]-B.y[i])**2 for i in range(4))))
            assert final==0,(side,ind,final);checks+=1
            if ind in ((0,1,0,1),(0,0,1,1)):
                samples[str((side,ind))]='0'
                # MiMo's proposed +2/3 potential modification introduces an actual residue.
                negative_controls[str((side,ind))]=str(s.Rational(2,3)*f0)
        if n%10==0:print(json.dumps(dict(stage='unanchored_parametrix',components=n+1,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
    assert B.metric(0,0,0,1,1)==-1/(2*B.w);checks+=1
    assert B.metric(0,0,1,0,1)==1/(2*B.w);checks+=1
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        derivative_of_connection='sum_i d_i Gamma^m_ia = -delta_ma, not -2 delta_ma/3',
        tensor_slot_constant='Two lower slots contribute +2 H0, not +4H0/3',
        true_offdiagonal_residue='0 at arbitrary x,y outside diagonal for both endpoints and all100components',
        S0011='-1/2, not0',mimo_modified_potential_residue=negative_controls,
        verdict='CLAIMED_RESIDUE_REFUTED_BY_LITERAL_CONNECTION_DIFFERENTIATION',
        sources_unchanged=True,potential_changed=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    text=f'''[DERIVED+CAS — confronto adversarial MiMo C6; candidato original preservado]

Abertura SHA256={opening}.

MiMo propôs resíduo −2K H0/3 e alteração do potencial de−2K para−4K/3.
A auditoria diferencia literalmente sua conexão de Christoffel:
sum_i partial_i Gamma^m_ia = −delta_ma em dimensão4, não−2delta_ma/3.
Assim, os dois índices covariantes dão+2K H0, não+4K H0/3.
A diferença é exatamente o resíduo que a resposta afirmava existir.
Também S_00,11=−1/2; o controle que a resposta dizia isolar só o traço
não tem S=0.

Verificamos novamente200equações, agora mantendo x e y arbitrários até
o fim, nas duas pontas e nos100componentes independentes. Todos os
resíduos são zero. O potencial sugerido pelo modelo introduziria
+2K H0/3: falha explícita, não adotada. A densidade não é aferível por
esse teste fora da diagonal; permanece auditada no contato da bancada.
Controles totais:{checks}; CPU{result['cpu_seconds']}s; comando audit_mimo_parametrix_v2.py, rc0. A primeira auditoria parou numa asserção de denominador: antes de impor w=(x-y)² a expressão tem polo de ordem4, não3. Mantida a tentativa falha; corrigido apenas o multiplicador de teste.

A resposta fica integralmente preservada, estatuto DECLARADO; a correção
é ao lado. Não ajustamos H0,H1, esquema ou operador. Não é loopQ2 completo,
continuação lorentziana nem alteração do gate. Custo MiMo medido no recibo
USD{r['cost_estimate_usd']}; contabilizado uma vez.
'''
    write(D/'DERIVACAO.md',text.encode());write(OUT/'ENTREGA_016_MEDIDA_C6_auditoria_MiMo_conexao.md',text.encode())
    files=[Path(__file__),H/'bilocal_first_curvature_engine.py',D/'MIMO_ORIGINAL.md',D/'RECEIPT.json',D/'results.json',D/'DERIVACAO.md']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files],opening_sha256=opening))
    event=dict(at=now.isoformat(),event='C6_EXTERNAL_RESULT_AUDITED',target='C6',**rec,audit_manifest_sha256=sha(D/'manifest.json'))
    ledger=(OUT/'LEDGER_016.jsonl').read_text('utf-8')
    assert not any(json.loads(line).get('event')==event['event'] and json.loads(line).get('job_id')==rec['job_id'] for line in ledger.splitlines() if line.strip())
    cp=H/'CONTINUIDADE.json';c=json.loads(cp.read_bytes());total=Decimal(c['partial_metered_cost_usd'])+Decimal(str(r['cost_estimate_usd']))
    append(OUT/'LEDGER_016.jsonl',json.dumps(event,ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6 ACTIVE: resíduo alegado por MiMo refutado, conexão +2H0;200equações bilocais sem ancoragem passam | CPU{result["cpu_seconds"]}s;parcial conhecido USD{total}.\n')
    c.update(at=now.isoformat(),C6_mimo_manifest=str(D/'manifest.json'),C6_mimo_status='AUDITED_CLAIMED_RESIDUE_REFUTED',partial_metered_cost_usd=str(total),own_live_process=None)
    put(cp,c,True);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
