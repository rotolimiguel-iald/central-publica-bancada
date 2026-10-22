"""Check total-derivative identities at the higher jet orders used by Euler graphs."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import json,time
import sympy as s
from balanced_tensor_transport_engine import balanced_euler_line,Q
from balanced_pair_normalization_check_v2 import correction
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'balanced_euler_higher_jet_audit'
def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[Path(__file__),H/'balanced_tensor_transport_engine.py',H/'balanced_pair_normalization_check_v2.py',
        H/'balanced_cubic_euler_contact/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='All Euler-line derivative pairs through extra order3, including original pair total order5 used in new graphs',
        identities=['E(u+i,v)+E(u,v+i)=qi E(u,v)','Euler line exchange','Polynomial parity and homogeneous degree2+|u|+|v|'],
        scope='Extension algebra only; no full tensor Ward or causal-family claim',sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();checks=0;count=0;degrees={}
    def eq(a,b=0):
        nonlocal checks
        assert s.expand(a-b)==0,(a,b);checks+=1
    words=lambda n:list(combinations_with_replacement(range(4),n))
    for n in range(4):
        for l in range(n+1):
            for u in words(l):
                for v in words(n-l):
                    value=balanced_euler_line(u,v);count+=1
                    reverse=sum(correction(v,tuple(sorted(u+(i,i)))) for i in range(4))
                    eq(value,reverse)
                    eq(value.subs({q:-q for q in Q},simultaneous=True),(-1)**n*value)
                    poly=s.Poly(value,*Q)
                    assert all(sum(mon)==n+2 for mon,c in poly.terms() if c);checks+=1
                    degrees[str(n)]=degrees.get(str(n),0)+1
                    if n<3:
                        for i in range(4):
                            eq(balanced_euler_line(tuple(sorted(u+(i,))),v)+balanced_euler_line(u,tuple(sorted(v+(i,)))),Q[i]*value)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        pairs=count,counts_by_extra_order=degrees,highest_underlying_pair_order=5,
        full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — controle diferencial das ordens efetivamente usadas]

Os novos grafos usam até três derivadas adicionais sobre as duas linhas,
além do operador Euler de ordem2. A tabela inicial só conferia pares até
ordem4; por isso verificamos agora TODOS os{count}pares Euler até ordem
adicional3 (par subjacente até5), sem repetir a avaliação dos grafos.

E_(u+i,v)+E_(u,v+i)=q_i E_(u,v), troca de linhas, paridade e grau
homogêneo2+|u|+|v| passaram em{checks}controles, CPU{result['cpu_seconds']}s,
rc0. Esse alcance cobre as palavras diferenciais dos grafos registrados;
não transforma o controle escalar em fechamento tensorial de Ward.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_jatos_Euler_ordem_cinco.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']]))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_EULER_ORDER5_AUDIT',target='A7.b',checks=checks,cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: {count}paresEuler conferidos até ordemsubjacente5;{checks}controles CPU{result["cpu_seconds"]}s. Q2OPEN. AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
